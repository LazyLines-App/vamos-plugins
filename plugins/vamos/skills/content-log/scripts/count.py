#!/usr/bin/env python3
"""Count a content log from Vamos rows.

    python3 count.py SOURCE [--tags tags.json] [--since YYYY-MM-DD] [--ads]

SOURCE is where the rows are, and count.py reads them itself:
  - the poll's `data.json_url` (an http, https or file: link), downloaded here;
  - a saved poll answer (a file whose `data` holds the rows, or a `json_url`
    that is then downloaded), or the downloaded rows file;
  - `-` with the poll's `data` piped in on stdin, when the rows came inline.
tags.json maps a post id (or url) to its tags, e.g.
{"DfYab6Ftp98": {"hook": "Claude just killed X", "format": "pixel scene", "intent": 412}};
`intent` (buying-intent comments) replaces the comment count for the ad rule.
Length is tagged from the row. Standard library only.

Prints, per account: the usual and what was set aside, each post since --since
(default: 7 days before the read) with its multiple or "too early", the hit
rate, each tag counted against the misses, and with --ads the posts that pass
the ad rule.
"""
import argparse, json, re, statistics as st, sys
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen

NAMES = {'tiktok': 'TikTok', 'youtube': 'YouTube', 'linkedin': 'LinkedIn'}
PAID = re.compile(r'#ad\b|#sponsored|paid partnership|\bsponsored\b|#partner', re.I)


def ts(s):
    d = datetime.fromisoformat(s.replace('Z', '+00:00'))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)  # a stamp with no zone is read as UTC


def load(src, hops=0):
    if src == '-':
        text = sys.stdin.read()
    elif re.match(r'(https?|file):', src):
        try:  # Vamos's data links refuse Python's default User-Agent (Cloudflare 1010)
            with urlopen(Request(src, headers={'User-Agent': 'vamos-content-log/1'}), timeout=60) as f:
                text = f.read().decode('utf-8')
        except OSError as e:
            sys.exit(f"couldn't download the rows ({e}); save them with curl -sL and pass the file")
    else:
        text = open(src, encoding='utf-8').read()
    blob = json.loads(text)
    if isinstance(blob, list) and blob and isinstance(blob[0], dict) and blob[0].get('type') == 'text':
        blob = json.loads(''.join(b.get('text', '') for b in blob))  # a host's saved tool result
    data = blob.get('data', blob) if isinstance(blob, dict) else None
    if isinstance(data, dict) and 'videos' not in data and 'rows' not in data and data.get('json_url'):
        if hops:
            sys.exit('the linked file holds another link, not rows')
        return load(data['json_url'], 1)
    return blob


def rows_of(blob):
    if isinstance(blob, list):
        return blob
    data = blob.get('data', blob)
    return data.get('videos', data.get('rows', []))


def length_tag(sec):
    if sec is None:
        return None
    return 'under 15 s' if sec < 15 else '15 to 30 s' if sec < 30 else '30 to 60 s' if sec < 60 else 'over 60 s'


def num(n):
    return f'{n:,.1f}'.rstrip('0').rstrip('.') if n % 1 else f'{int(n):,}'


def account(posts, tags, since, ads):
    posts = sorted(posts, key=lambda r: r['posted_at'])
    for r in posts:
        r.setdefault('id', r.get('url') or '?')
    seen, aside, judged = [], [], []
    for r in posts:
        age = (ts(r['counts_as_of']) - ts(r['posted_at'])).total_seconds() / 86400
        r['_age'] = age
        cap = (r.get('caption_head') or '').strip().lower()
        likes, views = r.get('likes'), r.get('views') or 0
        why = None
        if age < 3:
            why = 'too early (under 3 days)'
        elif r.get('paid_partnership') or r.get('sponsors') or PAID.search(cap):
            why = 'tagged paid'
        elif likes is not None and views and likes / views < 0.005:
            why = f'likely boosted ({likes / views:.2%} likes)'
        else:
            for p in seen:
                d1, d2 = p.get('duration_seconds'), r.get('duration_seconds')
                if cap and cap == (p.get('caption_head') or '').strip().lower() and d1 and d2 and abs(d1 - d2) <= 2:
                    why = f"repost of {p['id']}"
                    break
        seen.append(r)
        r['_aside'] = why
        (aside if why else judged).append(r)
    if not judged:
        print('  no post is old enough to judge')
        return
    usual = st.median(r['views'] for r in judged)
    cpk = lambda r: (tags.get(r['id'], {}).get('intent', r.get('comments') or 0)) / r['views'] * 1000 if r['views'] else 0
    usual_cpk = st.median(cpk(r) for r in judged)
    for r in posts:
        r['_x'] = r['views'] / usual if usual else 0.0
    print(f'  usual: {num(usual)} views, the median of {len(judged)} posts read on {posts[-1]["counts_as_of"][:10]}')
    for r in aside:
        if not r['_aside'].startswith('too early'):
            print(f"  set aside: {r['id']} {num(r['views'])} views, {r['_aside']}")
    last = judged[-20:]
    xs = [r['_x'] for r in last]
    print(f'  hit rate, last {len(last)}: {sum(x > 1 for x in xs)} above 1x, {sum(x > 2 for x in xs)} above 2x, median {st.median(xs):.1f}x')
    print(f'  comments per 1,000 views: usual {usual_cpk:.2f}')
    print(f'  since {since:%Y-%m-%d}:')
    for r in posts:
        if ts(r['posted_at']) < since:
            continue
        state = r['_aside'] if r['_aside'] else f"{r['_x']:.1f}x"
        print(f"    {r['posted_at'][:10]} {r['id']} {num(r['views'])} views, {state}, {cpk(r):.1f} comments per 1,000, {r['_age']:.1f} days old | {(r.get('caption_head') or '')[:70]}")
    keys = sorted({k for t in tags.values() for k in t if k != 'intent'} | {'length'})
    for key in keys:
        groups = {}
        for r in judged:
            v = length_tag(r.get('duration_seconds')) if key == 'length' else tags.get(r['id'], tags.get(r.get('url'), {})).get(key)
            if v:
                groups.setdefault(v, []).append(r)
        if not groups:
            continue
        print(f'  {key}:')
        for v, rs in sorted(groups.items(), key=lambda kv: -st.median(r['_x'] for r in kv[1])):
            up = [r for r in rs if r['_x'] > 1]
            weeks = len({ts(r['posted_at']).isocalendar()[:2] for r in rs})
            print(f"    {v}: {len(up)} of {len(rs)} above usual, median {st.median(r['_x'] for r in rs):.1f}x, from {weeks} week{'s' if weeks > 1 else ''}"
                  + ('' if len(rs) >= 3 else ' (a Hunch: under 3 posts)'))
    if ads:
        hits = [r for r in judged if ts(r['posted_at']) >= since and r['_x'] >= 5 and r['views'] >= 10000 and cpk(r) >= usual_cpk]
        print('  turn into an ad (5x or more, 10,000+ views, comments per 1,000 at or above usual): ' + (', '.join(f"{r['id']} ({r['_x']:.1f}x, {num(r['views'])} views, {cpk(r):.1f} per 1,000)" for r in hits) or 'none'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', help='json_url, a saved poll or rows file, or - for stdin')
    ap.add_argument('--tags')
    ap.add_argument('--since')
    ap.add_argument('--ads', action='store_true')
    a = ap.parse_args()
    rows = [r for r in rows_of(load(a.source)) if r.get('views') is not None and r.get('posted_at')]
    if not rows:
        sys.exit('no rows with views and a date')
    stamp = max((r['counts_as_of'] for r in rows if r.get('counts_as_of')), default=None) or datetime.now().astimezone().isoformat()
    for r in rows:
        r.setdefault('counts_as_of', stamp)
        r['counts_as_of'] = r['counts_as_of'] or stamp
    tags = json.load(open(a.tags, encoding='utf-8')) if a.tags else {}
    tags = {k.rstrip('/').rsplit('/', 1)[-1]: v for k, v in tags.items()}
    read = max(ts(r['counts_as_of']) for r in rows)
    since = ts(a.since + 'T00:00:00+00:00') if a.since else read - timedelta(days=7)
    by = {}
    for r in rows:
        by.setdefault((r.get('platform', ''), r.get('handle') or (r.get('creator') or {}).get('handle', '')), []).append(r)
    for (platform, handle), posts in by.items():
        print(f"@{handle} on {NAMES.get(platform.lower(), platform.title())}, {len(posts)} posts read")
        account(posts, tags, since, a.ads)


if __name__ == '__main__':
    main()
