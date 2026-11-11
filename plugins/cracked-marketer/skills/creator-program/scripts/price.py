"""Price creators off their own numbers, and check the pay table's dates.

  python3 price.py floor ROWS.json --fee 400 [--exclude id,id] [--handle name]
      ROWS.json is a saved chat_completion_poll answer (its data.videos) or a list of rows.
      Counts posts at least 3 days old (by counts_as_of). Sets aside boosts (likes under 0.5% of
      views, or tagged paid or sponsored), reposts (the same caption as an earlier post, within 2 s
      of its length) and the ids in --exclude. Usual = their median; floor = the median of the 10
      worst of the last 30. Prints the cost per 1,000 views of the fee at the floor and at the usual.
  python3 price.py offer --base 60 --usual 4200
      The default offer: the base per video, +1x the base at 3x their usual within 7 days,
      +2x more at 10x, so the bonus caps at 3x the base and a video at 4x.
  python3 price.py table PAY.md [--today 2026-11-11]
      Every deal row needs a per-video figure, a source link and a date. Prints each row's age;
      rows over 90 days old are flagged OLD. Exits 1 on a row that's missing one.
"""
import argparse, datetime as dt, json, re, statistics as st, sys


def parse_time(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def load_rows(path):
    d = json.load(open(path))
    if isinstance(d, dict):
        d = (d.get('data') or {}).get('videos') or d.get('videos') or []
    return d


def floor(args):
    rows = load_rows(args.rows)
    if args.handle:
        rows = [r for r in rows if ((r.get('creator') or {}).get('handle') or '').lower() == args.handle.lower().lstrip('@')]
    skip = set(filter(None, (args.exclude or '').split(',')))
    stamps = [parse_time(r['counts_as_of']) for r in rows if r.get('counts_as_of')]
    asof = max(stamps) if stamps else dt.datetime.now(dt.timezone.utc)
    ok, out, seen = [], [], {}
    for r in sorted(rows, key=lambda r: r.get('posted_at') or ''):
        cap = (r.get('caption_head') or '').strip().lower()
        dur = r.get('duration_seconds')
        earlier = seen.setdefault(cap, []) if cap else []
        repost = dur is not None and any(d is not None and abs(d - dur) <= 2 for d in earlier)
        earlier.append(dur)
        if r.get('views') is None or not r.get('posted_at'):
            out.append((r.get('id'), 'no views or date'))
        elif r.get('paid_partnership') or r.get('sponsors'):
            out.append((r.get('id'), 'paid'))
        elif r['views'] and (r.get('likes') or 0) < 0.005 * r['views']:
            out.append((r.get('id'), 'boost: likes under 0.5% of views'))
        elif repost:
            out.append((r.get('id'), 'repost'))
        elif r.get('id') in skip:
            out.append((r.get('id'), 'excluded'))
        elif (asof - parse_time(r['posted_at'])).total_seconds() < 3 * 86400:
            out.append((r.get('id'), 'under 3 days old'))
        else:
            ok.append(r)
    if len(ok) < 10:
        sys.exit(f'only {len(ok)} posts count; need at least 10 for a floor')
    usual = st.median(r['views'] for r in ok)
    last = sorted(ok, key=lambda r: r['posted_at'], reverse=True)[:30]
    worst = sorted(r['views'] for r in last)[:10]
    fl = st.median(worst)
    print(f'posts counted: {len(ok)} (read as of {asof:%Y-%m-%d}); set aside: ' + (', '.join(f'{i} ({why})' for i, why in out) or 'none'))
    print(f'usual (median of {len(ok)}): {usual:,.0f}')
    print(f'floor (median of the 10 worst of the last {len(last)}): {fl:,.1f}  [10 worst: {", ".join(f"{v:,}" for v in worst)}]')
    if args.fee:
        per = lambda v: f'${args.fee / v * 1000:,.2f}' if v else 'no number (0 views)'
        print(f'${args.fee:,.0f} a video = {per(fl)} per 1,000 views at the floor, {per(usual)} at the usual')


def offer(args):
    b, u = args.base, args.usual
    print(f'base ${b:,.0f} a video')
    print(f'+${b:,.0f} if it reaches {3 * u:,.0f} views (3x their usual) within 7 days')
    print(f'+${2 * b:,.0f} more if it reaches {10 * u:,.0f} views (10x) within 7 days')
    print(f'most the bonus adds: ${3 * b:,.0f}; most a video can cost, base and bonus: ${4 * b:,.0f}')


def table(args):
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    lines = [l for l in open(args.path) if l.startswith('|')]
    head = [c.strip().lower() for c in lines[0].strip('|\n').split('|')]
    bad = 0
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip('|\n').split('|')]
        if len(cells) != len(head):
            break  # the next table
        row = dict(zip(head, cells))
        if 'per video' not in row:
            break
        who, per, src, date = row.get('who', ''), row['per video'], row.get('source', ''), row.get('date', '')
        miss = [n for n, v in (('per video', re.search(r'\d', per)), ('source', 'http' in src), ('date', re.search(r'\d{4}', date))) if not v]
        if miss:
            bad += 1
            print(f'MISSING {", ".join(miss)}: {who}')
            continue
        m = re.search(r'(\d{4})-(\d\d)-(\d\d)', date)
        if m:
            age = (today - dt.date(*map(int, m.groups()))).days
            print(f'{"OLD " if age > 90 else ""}{age:>4} days  {who}  ({per})')
        else:
            print(f'year only  {who}  ({per}, {date})')
    sys.exit(1 if bad else 0)


p = argparse.ArgumentParser()
sub = p.add_subparsers(dest='cmd', required=True)
f = sub.add_parser('floor'); f.add_argument('rows'); f.add_argument('--fee', type=float); f.add_argument('--exclude'); f.add_argument('--handle')
o = sub.add_parser('offer'); o.add_argument('--base', type=float, required=True); o.add_argument('--usual', type=float, required=True)
t = sub.add_parser('table'); t.add_argument('path'); t.add_argument('--today')
a = p.parse_args()
{'floor': floor, 'offer': offer, 'table': table}[a.cmd](a)
