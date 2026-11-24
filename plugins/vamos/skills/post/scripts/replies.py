#!/usr/bin/env python3
"""Answer the comments on the user's posts through their own Zernio: which comments still wait for an answer, and
the exact replies their yes sends. Standard library only, no network.

  python3 replies.py pick <file or folder> [...] [--replied vamos/replied.json] [--words GUIDE,PENNY]
                          [--since 2026-11-20 | --days 14] [--now ISO] [--max 60] [--out waiting.json]
  python3 replies.py plan drafts.json [--waiting waiting.json] [--replied vamos/replied.json] [--out send.json]

pick reads saved Zernio answers (a folder means its *.json): comments_list_inbox_comments (posts, accounts, ad rows)
and comments_get_inbox_post_comments (one post's comments). Each top-level comment is set aside when it is the
account's own, hidden, can't be replied to, older than --since (or --days), already in the --replied ledger, already
answered by the account, carries more replies than were read, asks for a --words keyword the DM rule answers, or has no
words; the rest wait, numbered, newest post first and most liked first. It writes waiting.json and prints them, what
was set aside, the accounts Zernio skipped, and YOUR REPLIES: how the user writes their own.

plan reads drafts.json, one entry per waiting comment: {"n": 1, "reply": "..."}, {"n": 2, "skip": "spam"} or
{"n": 4, "ask": "What does it cost?"} (a fact only the user knows; that comment waits). It prints the table for the
user's yes, ASK, FLAG (the same words twice: platforms read repeats as spam) and DEFECT lines (fix them: exit 1, no
send file), and writes send.json: each reply's comments_reply_to_inbox_post call, to send as it is.
"""
import argparse, datetime as dt, json, os, re, sys

# A reply's length in characters, read 2026-11-24: TikTok's reply API (through Sprinklr's TikTok Business docs);
# Instagram's 2,200-character comments; X's 280; Threads' 500-character posts; LinkedIn's 1,250-character comments;
# YouTube's 10,000; Facebook's 8,000; Bluesky's 300. Pinterest has no comment replies through Zernio.
LIMITS = {'tiktok': 150, 'instagram': 2200, 'facebook': 8000, 'youtube': 10000, 'twitter': 280,
          'threads': 500, 'linkedin': 1250, 'bluesky': 300, 'reddit': 10000}
REASONS = {'own': 'your own', 'hidden': 'hidden', 'cannot_reply': "can't be replied to",
           'too_old': 'older than {cutoff}', 'replied_before': 'answered in an earlier batch',
           'answered': 'already answered by you', 'unsure': 'with more replies than were read: open it before answering',
           'keyword': 'asking for a keyword your DM rule answers', 'no_words': 'with no words (emoji only)',
           'ads': "on your ads, left out: they're answered in Ads Manager"}


def read(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def write(path, value):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def ledger(path):
    if not path or not os.path.exists(path):
        return set()
    return {x if isinstance(x, str) else x.get('comment_id') for x in read(path)}


def time(text):
    """A platform's time as UTC; a time it can't read sorts first and is never called too old."""
    if not text:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    text = re.sub(r'([+-]\d\d)(\d\d)$', r'\1:\2', str(text).replace('Z', '+00:00'))   # +0000, as Facebook writes it
    try:
        value = dt.datetime.fromisoformat(text)
    except ValueError:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    return value.replace(tzinfo=dt.timezone.utc) if value.tzinfo is None else value.astimezone(dt.timezone.utc)


def owner(comment):
    return (comment.get('from') or {}).get('isOwner') is True


def short(text, limit):
    text = str(text or '')
    return text if len(text) <= limit else text[:limit - 1] + '…'


def pick(a):
    now = time(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    cutoff = time(a.since) if a.since else now - dt.timedelta(days=a.days)
    cutoff_words = a.since if a.since else f'{a.days} days'
    words = [w.strip() for w in a.words.split(',') if w.strip()]
    answered = ledger(a.replied)
    paths = []
    for path in a.inputs:
        paths.extend([os.path.join(path, f) for f in sorted(os.listdir(path)) if f.endswith('.json')]
                     if os.path.isdir(path) else [path])
    posts, threads, skipped, unread = {}, [], [], []
    counts = dict.fromkeys(REASONS, 0)
    ads = set()
    for path in paths:
        try:
            data = read(path)
        except (ValueError, OSError):
            unread.append(path)
            continue
        if isinstance(data, dict) and isinstance(data.get('data'), list):
            for row in data['data']:
                if row.get('isAd'):
                    ads.add(row.get('id'))
                else:
                    posts[row.get('id')] = row
            meta = data.get('meta') or {}
            for item in meta.get('failedAccounts', []):
                why = item.get('error', '')
                if item.get('code'):
                    why += f" ({item['code']})"
                skipped.append({'account_id': item.get('accountId', ''), 'handle': item.get('accountUsername', ''),
                                'platform': item.get('platform', ''), 'why': why})
            for item in meta.get('accountsSkipped', []):
                skipped.append({'account_id': item.get('accountId', ''), 'handle': item.get('accountUsername', ''),
                                'platform': item.get('platform', ''), 'why': "Zernio can't read comments there"})
        elif isinstance(data, dict) and isinstance(data.get('comments'), list) and isinstance(data.get('meta'), dict):
            threads.append(data)
        else:
            unread.append(path)
    counts['ads'] = len(ads)
    for path in unread:
        print(f'UNREAD {path}: not a Zernio comments answer')
    seen, waiting, yours, newest = set(), [], [], {}
    for thread in threads:
        meta = thread['meta']
        post_id = meta.get('postId', '')
        if post_id in ads:
            continue
        post = posts.get(post_id) or {}
        fallback = thread.get('post') or {}
        for c in thread['comments']:
            cid = c.get('id')
            if cid in seen:
                continue
            seen.add(cid)
            at = time(c.get('createdTime'))
            newest[post_id] = max(newest.get(post_id, at), at)
            for item in [c] + (c.get('replies') or []):
                if owner(item) and item.get('message'):
                    yours.append((time(item.get('createdTime')), item['message']))
            text = c.get('message') or ''
            if owner(c): reason = 'own'
            elif c.get('isHidden') is True: reason = 'hidden'
            elif c.get('canReply') is False: reason = 'cannot_reply'
            elif c.get('createdTime') and at.year > 1 and at < cutoff: reason = 'too_old'
            elif cid in answered: reason = 'replied_before'
            elif any(owner(r) for r in c.get('replies') or []): reason = 'answered'
            elif c.get('repliesHasMore') is True: reason = 'unsure'
            elif len(re.findall(r'\b\w+\b', text)) <= 4 and any(re.search(r'(?<!\w)' + re.escape(w) + r'(?!\w)', text, re.I) for w in words): reason = 'keyword'
            elif not any(ch.isalnum() for ch in text): reason = 'no_words'
            else: reason = 'waiting'
            if reason != 'waiting':
                counts[reason] += 1
                continue
            person = c.get('from') or {}
            waiting.append({'comment_id': cid, 'post_id': post_id, 'account_id': meta.get('accountId', ''),
                            'platform': meta.get('platform', ''), 'handle': post.get('accountUsername') or meta.get('accountId', ''),
                            'post': (post.get('content') or fallback.get('text') or '')[:80],
                            'permalink': post.get('permalink') or fallback.get('permalink') or '',
                            'author': person.get('username') or person.get('name') or person.get('id') or '',
                            'text': text, 'likes': c.get('likeCount') or 0, 'at': c.get('createdTime') or ''})
    waiting.sort(key=lambda c: (-time((posts.get(c['post_id']) or {}).get('createdTime')).timestamp()
                                if (posts.get(c['post_id']) or {}).get('createdTime') else -newest[c['post_id']].timestamp(),
                                c['post_id'], -c['likes'], time(c['at'])))
    more = max(0, len(waiting) - a.max)
    waiting = waiting[:a.max]
    for n, c in enumerate(waiting, 1):
        c['n'] = n
    unique = []
    for _, text in sorted(yours, key=lambda x: x[0], reverse=True):
        if text not in unique:
            unique.append(text)
    unique = unique[:12]
    write(a.out, {'read_at': now.isoformat(), 'comments': waiting, 'set_aside': counts,
                  'skipped_accounts': skipped, 'your_replies': unique})
    previous = None
    for c in waiting:
        if c['post_id'] != previous:
            print(f"@{c['handle']} ({c['platform']}) · \"{c['post']}\" · {c['permalink']}")
            previous = c['post_id']
        print(f"  #{c['n']} @{c['author']} ({c['likes']} likes, {c['at'][:10]}): {c['text']}")
    if not waiting: print('NOTHING WAITING')
    if more: print(f'MORE {more} more waiting: answer these first, then run pick again')
    print('SET ASIDE')
    for reason, count in counts.items():
        if count: print(f"{count} {REASONS[reason].format(cutoff=cutoff_words)}")
    for s in skipped:
        print(f"SKIPPED {('@' + s['handle']) if s['handle'] else s['account_id']} ({s['platform']}): {s['why']}")
    # The ledger is what keeps a comment from being answered twice: say which one was read, or that none was.
    if a.replied and os.path.exists(a.replied):
        print(f'LEDGER {a.replied}: {len(answered)} comments answered in earlier batches')
    else:
        print(f'LEDGER {a.replied}: no file here, so no earlier batch was counted. Run pick from the folder that holds '
              'vamos/, or pass --replied with its path.')
    print('YOUR REPLIES')
    for text in unique: print(text)
    return 0


def plan(a):
    waiting = read(a.waiting)['comments']
    by_n = {c['n']: c for c in waiting}
    drafts = read(a.drafts)
    answered = ledger(a.replied)
    defects, flags, asks, rows, seen, repeats = [], [], [], [], set(), {}
    skips = 0
    for entry in drafts:
        n = entry.get('n')
        if isinstance(n, str) and n.strip().lstrip('#').isdigit():
            n = int(n.strip().lstrip('#'))   # "3" or "#3" as the model may write it
        if n in seen:
            defects.append(f'#{n}: given twice')
        seen.add(n)
        c = by_n.get(n)
        if c is None:
            defects.append(f'#{n}: not in waiting')
        choices = [k for k in ('reply', 'ask', 'skip') if k in entry]
        if len(choices) != 1:
            defects.append(f'#{n}: give exactly one of reply, ask or skip')
            continue
        if not c: continue
        if c['comment_id'] in answered:
            defects.append(f'#{n}: already in the replied ledger')
        kind = choices[0]
        if kind == 'ask': asks.append((c, entry[kind])); continue
        if kind == 'skip': skips += 1; continue
        reply = entry['reply']
        if not isinstance(reply, str) or not reply.strip():
            defects.append(f'#{n}: empty reply'); continue
        platform = c['platform']
        if platform not in LIMITS: defects.append(f'#{n}: no reply through Zernio on {platform}')
        elif len(reply) > LIMITS[platform]: defects.append(f'#{n}: reply exceeds {platform} limit of {LIMITS[platform]} characters')
        if re.search(r'\[.*?\]|\{\{|\}\}|TODO|XXX', reply, re.S):
            defects.append(f'#{n}: reply has an unfilled slot')
        key = reply.strip().casefold()
        if key in repeats: flags.append(f'#{n} and #{repeats[key]} use the same reply')
        else: repeats[key] = n
        rows.append((c, reply))
    rows.sort(key=lambda x: x[0]['n'])
    asks.sort(key=lambda x: x[0]['n'])
    def cell(s): return str(s).replace('|', r'\|').replace('\n', ' ')
    print('| # | Account | Post | Comment | Reply |')
    print('|---|---|---|---|---|')
    for c, reply in rows:
        values = [c['n'], f"@{c['handle']} ({c['platform']})", short(c['post'], 40),
                  short(f"@{c['author']}: {c['text']}", 80), reply]
        print('| ' + ' | '.join(cell(v) for v in values) + ' |')
    for c, question in asks: print(f"ASK #{c['n']} @{c['author']}: \"{c['text']}\" → {question}")
    for flag in flags: print('FLAG ' + flag)
    for defect in defects: print('DEFECT ' + defect)
    print(f"REPLIES {len(rows)} on {len({c['post_id'] for c, _ in rows})} posts · {len(asks)} waits on your answer · {skips} skipped · {len(set(by_n) - seen)} not drafted")
    if defects: return 1
    calls = [{'n': c['n'], 'comment_id': c['comment_id'], 'post_id': c['post_id'],
              'name': 'comments_reply_to_inbox_post',
              'arguments': {'post_id': c['post_id'], 'account_id': c['account_id'],
                            'comment_id': c['comment_id'], 'message': reply}} for c, reply in rows]
    write(a.out, {'calls': calls})
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='command', required=True)
    p = sub.add_parser('pick')
    p.add_argument('inputs', nargs='+')
    p.add_argument('--replied', default='vamos/replied.json')
    p.add_argument('--words', default='')
    p.add_argument('--days', type=int, default=14)
    p.add_argument('--since', help='a date: comments before it are set aside (wins over --days)')
    p.add_argument('--now')
    p.add_argument('--max', type=int, default=60)
    p.add_argument('--out', default='waiting.json')
    q = sub.add_parser('plan')
    q.add_argument('drafts')
    q.add_argument('--waiting', default='waiting.json')
    q.add_argument('--replied', default='vamos/replied.json')
    q.add_argument('--out', default='send.json')
    a = ap.parse_args()
    return pick(a) if a.command == 'pick' else plan(a)


if __name__ == '__main__':
    sys.exit(main())
