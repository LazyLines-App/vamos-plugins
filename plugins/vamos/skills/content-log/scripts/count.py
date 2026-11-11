#!/usr/bin/env python3
"""Count a content log from Vamos rows.

    python3 count.py SOURCE [--tags tags.json] [--since YYYY-MM-DD] [--ads] [--pay pay.json]

SOURCE is where the rows are, and count.py reads them itself:
  - the poll's `data.json_url` (an http, https or file: link), downloaded here;
  - a saved poll answer (a file whose `data` holds the rows, or a `json_url`
    that is then downloaded), or the downloaded rows file;
  - `-` with the poll's `data` piped in on stdin, when the rows came inline.
tags.json maps a post id (or url) to its tags, e.g.
{"DfYab6Ftp98": {"hook": "Claude just killed X", "format": "pixel scene", "intent": 412}};
`intent` (buying-intent comments) replaces the comment count for the ad rule.
Length is tagged from the row. Standard library only.

Creators the brand pays: tag each post made for the brand {"ours": true, "creator": "@handle",
"hook": "the brief's hook it used"}, on the creator's account or the brand's. An ours post is judged
against the usual of the account it posted on, even when tagged paid, and never counts toward that
usual. pay.json holds each creator's deal from the creator program:
{"@handle": {"base": 60, "bonus": [[12600, 60], [42000, 120]], "due": 4, "sales": 3}},
where bonus is [views reached, dollars added], due the videos agreed for the period, and sales (or
signups) the user's own count from a code or link; a post's "paid" tag replaces the worked-out cost.
A top-level "pool": 500 caps the bonuses, paid in posting order until it's spent.

Prints, per account: the usual and what was set aside, each post since --since
(default: 7 days before the read) with its multiple or "too early", the hit
rate, each tag counted against the misses, and with --ads the posts that pass
the ad rule.
"""
import argparse, json, os, re, statistics as st, sys
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
            if src.startswith('file:') and not src.startswith('file:/'):
                sys.exit(f"no {src[5:]} under {os.getcwd()}: a file: link is relative to the folder the poll ran in,"
                         " so run count.py from that folder, by its full path")
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


def key(link):
    """A post id from an id or a link, share-link query (?igsh=…, ?is_from_webapp=…) and fragment dropped."""
    return re.split(r'[?#]', link or '')[0].rstrip('/').rsplit('/', 1)[-1]


def tag_of(tags, r):
    return tags.get(r['id'], tags.get(key(r.get('url')), {}))


def account(posts, tags, since, ads):
    posts = sorted(posts, key=lambda r: r['posted_at'])
    for r in posts:
        r.setdefault('id', r.get('url') or '?')
    seen, aside, judged, ours = [], [], [], []
    for r in posts:
        age = (ts(r['counts_as_of']) - ts(r['posted_at'])).total_seconds() / 86400
        r['_age'] = age
        cap = (r.get('caption_head') or '').strip().lower()
        likes, views = r.get('likes'), r.get('views') or 0
        why = None
        if tag_of(tags, r).get('ours'):
            r['_ours'] = True
            r['_aside'] = 'too early (under 3 days)' if age < 3 else None
            r['_boost'] = likes is not None and views and likes / views < 0.005
            ours.append(r)
            continue
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
    for r in ours:
        r['_usual'] = usual
    cpk = lambda r: (tags.get(r['id'], {}).get('intent', r.get('comments') or 0)) / r['views'] * 1000 if r['views'] else 0
    usual_cpk = st.median(cpk(r) for r in judged)
    for r in posts:
        r['_x'] = r['views'] / usual if usual else 0.0
    print(f'  usual: {num(usual)} views, the median of {len(judged)} posts read on {posts[-1]["counts_as_of"][:10]}'
          + (' (thin: under 10 posts)' if len(judged) < 10 else ''))
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
        mark = f" [ours, by {tag_of(tags, r).get('creator') or '?'}]" if r.get('_ours') else ''
        print(f"    {r['posted_at'][:10]} {r['id']}{mark} {num(r['views'])} views, {state}, {cpk(r):.1f} comments per 1,000, {r['_age']:.1f} days old | {(r.get('caption_head') or '')[:70]}")
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


def band(r):
    """Where a post for the brand broke, by its views (an app operator's bands); the product's own numbers decide past 100,000."""
    v = r['views']
    if v < 1000:
        return 'under 1,000: the opening failed'
    if v < 10000:
        return '1,000 to 10,000: people left before the product'
    if v >= 100000:
        return '100,000+: judge it on sales or signups'
    return '10,000 to 100,000: judge it against the usual'


def cost(r, deal, tag, pool):
    """What the deal pays for this post. pool is [dollars left] when the program caps bonuses, else None."""
    if 'paid' in tag:
        return float(tag['paid']), f"${num(float(tag['paid']))} as tagged"
    if not deal:
        return None, 'no deal in pay.json'
    total, parts = float(deal.get('base', 0)), [f"${num(float(deal.get('base', 0)))} base"]
    for at, extra in deal.get('bonus') or []:
        if r['views'] >= at:
            give = extra if pool is None else min(extra, pool[0])
            if pool is not None:
                pool[0] -= give
            total += give
            parts.append(f"+${num(extra)} at {num(at)}" + ('' if give == extra else ' (pool spent)' if not give else f" (only ${num(give)} left in the pool)"))
    return total, ' '.join(parts)


def handle_of(r, default='?'):
    """The account a row is from: its handle, or its creator's (a dict or a plain handle)."""
    c = r.get('creator')
    return r.get('handle') or (c.get('handle') if isinstance(c, dict) else c) or default


def creators(rows, tags, pay):
    """Every post tagged ours, whatever --since says: the program's period is the user's links."""
    ours = sorted((r for r in rows if r.get('_ours')), key=lambda r: r['posted_at'])
    if not ours:
        print('creators: no post is tagged ours')
        return
    who = lambda r: (tag_of(tags, r).get('creator') or '@' + handle_of(r)).lower()
    deals = {k.lower(): v for k, v in (pay or {}).items() if isinstance(v, dict)}
    print("creators: the posts made for the brand, each against the usual of the account it posted on;"
          " bonuses are worked out from the views at the read, so for a post past 7 days check its day-7 views")
    pool = (pay or {}).get('pool')
    if pool is not None:
        tiers = sum(x for r in ours if 'paid' not in tag_of(tags, r)
                    for at, x in (deals.get(who(r), {}).get('bonus') or []) if r['views'] >= at)
        print(f"  bonus pool ${num(pool)}: the tiers reached add ${num(tiers)}"
              + (f", ${num(tiers - pool)} past the pool, so the costs below pay bonuses in posting order until it's spent: check that's how you pay it"
                 if tiers > pool else ', inside the pool'))
    left = None if pool is None else [float(pool)]
    costs = {id(r): cost(r, deals.get(who(r), {}), tag_of(tags, r), left) for r in ours}
    by = {}
    for r in ours:
        by.setdefault(who(r), []).append(r)
    for c in sorted(set(by) | set(deals)):
        rs = sorted(by.get(c, []), key=lambda r: r['posted_at'])
        deal = deals.get(c, {})
        print(f'  {c}:')
        spent, views, judged = 0.0, 0, []
        for r in rs:
            t = tag_of(tags, r)
            usual = r.get('_usual')
            paid, how = costs[id(r)]
            spent += paid or 0
            views += r['views']
            if r['_aside']:
                state = r['_aside']
            elif usual:
                judged.append(r)
                state = f"{r['views'] / usual:.1f}x the usual of {num(usual)}" + ('' if r['views'] >= usual else f", {band(r)}")
            else:
                state = 'no usual for this account'
            boost = ', likes under 0.5%: views may include paid' if r.get('_boost') else ''
            label = '' if (r.get('paid_partnership') or PAID.search(r.get('caption_head') or '')) else ', no paid-partnership label in the row and no #ad in the caption read: check the post'
            sofar = ' so far' if r['_aside'] else ''
            per = f", ${paid / r['views'] * 1000:,.2f} per 1,000{sofar}" if paid is not None and r['views'] else ''
            acct = handle_of(r)
            print(f"    {r['posted_at'][:10]} {r['id']} on @{acct}: {num(r['views'])} views, {state}, {r['_age']:.1f} days old{boost}{label}; "
                  f"paid {('$' + num(paid) + sofar + ' (' + how + ')') if paid is not None else how}{per} | hook: {t.get('hook') or '?'}")
        xs = [r['views'] / r['_usual'] for r in judged]
        due = deal.get('due')
        line = f"    scorecard: {len(rs)} posted" + (f" of {due} due" if due else '')
        if xs:
            line += f", {sum(x > 1 for x in xs)} of {len(xs)} judged above usual, median {st.median(xs):.1f}x"
        if spent and views:
            line += f"; paid ${num(spent)} for {num(views)} views, ${spent / views * 1000:,.2f} per 1,000"
        for word in ('sales', 'signups'):
            if deal.get(word) is not None:
                s_ = deal[word]
                line += f"; {s_} {word} from your numbers" + (f", ${spent / s_:,.2f} each" if s_ and spent else '')
        print(line)
    hooks = {}
    for r in ours:
        h = tag_of(tags, r).get('hook')
        if h:
            hooks.setdefault(h, []).append(r)
    if hooks:
        print('  hooks across creators (posts for the brand):')
        def rank(kv):
            judged = [r for r in kv[1] if not r['_aside'] and r.get('_usual')]
            return (-sum(r['views'] > r['_usual'] for r in judged), -max((r['views'] / r['_usual'] for r in judged), default=0))
        for h, rs in sorted(hooks.items(), key=rank):
            best = max(rs, key=lambda r: (bool(r.get('_usual')), r['views'] / r['_usual'] if r.get('_usual') else r['views']))
            up = [r for r in rs if not r['_aside'] and r.get('_usual') and r['views'] > r['_usual']]
            early = sum(1 for r in rs if r['_aside'])
            dead = len(rs) >= 5 and max(r['views'] for r in rs) < 10000
            bx = f", {best['views'] / best['_usual']:.1f}x" if best.get('_usual') else ''
            print(f"    \"{h}\": {len(rs)} tr{'y' if len(rs) == 1 else 'ies'} by {len({who(r) for r in rs})} creator{'s' if len({who(r) for r in rs}) > 1 else ''}, "
                  f"{len(up)} above usual{f', {early} too early' if early else ''}, best {num(best['views'])}{bx} ({who(best)})"
                  + (' DEAD: 5+ tries, none past 10,000' if dead else ''))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source', help='json_url, a saved poll or rows file, or - for stdin')
    ap.add_argument('--tags')
    ap.add_argument('--since')
    ap.add_argument('--ads', action='store_true')
    ap.add_argument('--pay')
    a = ap.parse_args()
    rows = [r for r in rows_of(load(a.source)) if r.get('views') is not None and r.get('posted_at')]
    if not rows:
        sys.exit('no rows with views and a date')
    stamp = max((r['counts_as_of'] for r in rows if r.get('counts_as_of')), default=None) or datetime.now().astimezone().isoformat()
    for r in rows:
        r.setdefault('counts_as_of', stamp)
        r['counts_as_of'] = r['counts_as_of'] or stamp
    tags = json.load(open(a.tags, encoding='utf-8')) if a.tags else {}
    tags = {key(k): v for k, v in tags.items()}
    read = max(ts(r['counts_as_of']) for r in rows)
    since = ts(a.since + 'T00:00:00+00:00') if a.since else read - timedelta(days=7)
    by = {}
    for r in rows:
        by.setdefault((r.get('platform', ''), handle_of(r, '')), []).append(r)
    for (platform, handle), posts in by.items():
        print(f"@{handle} on {NAMES.get(platform.lower(), platform.title())}, {len(posts)} posts read")
        account(posts, tags, since, a.ads)
    known = {r['id'] for r in rows} | {key(r.get('url')) for r in rows}
    lost = [k for k in tags if k not in known]
    if lost:
        print('tags that match no row (check the link; a short link like vm.tiktok.com needs the full one): ' + ', '.join(lost))
    if any(t.get('ours') for t in tags.values()):
        creators(rows, tags, json.load(open(a.pay, encoding='utf-8')) if a.pay else {})
    elif a.pay:
        print('creators: no post is tagged ours, so there is nothing to cost: tag each post made for the brand {"ours": true, "creator": "@handle", "hook": "..."} in --tags')


if __name__ == '__main__':
    main()
