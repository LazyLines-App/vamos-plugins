#!/usr/bin/env python3
"""The ad account's week, counted from an Ads Manager export.

    python3 ads.py this-week.csv [--last last-week.csv] [--codes codes.txt] [--json]

Reads an ad-level CSV export (Ads Manager → Reports → Export), one week per file. Columns are found
by name: Ad name, Amount spent and Purchases are needed (Leads for a lead-gen account, whose CPA is
then cost per lead); purchase value or ROAS adds ROAS. Prints
the columns and dates it read, the totals against last week, the top ads by spend, risers and
fallers (stopped ads included), spend and CPA by each word in the ad names, and the concept codes
winning-ad-ideas puts on the board (WA-1112-3, WA_1112_3) found in ad names, with their results.
Standard library only.
"""
import csv, datetime, json, re, statistics, sys
from collections import defaultdict

CODE = re.compile(r'(?<![A-Za-z])WA[-_ ]?\d{4}[-_ ]\d+', re.I)
SPLIT = re.compile(r'[\s_\-|/·:,()\[\]]+')
norm = lambda c: 'WA-' + '-'.join(re.findall(r'\d+', c))
SIGN = {'USD': '$', 'GBP': '£', 'EUR': '€', 'CAD': 'CA$', 'AUD': 'A$', 'NZD': 'NZ$'}


def col(header, *wants, avoid=()):
    for w in wants:
        for h in header:
            low = h.lower()
            if w in low and not any(a in low for a in avoid):
                return h
    return None


def money(v):
    v = re.sub(r'[^\d.,\-]', '', str(v or ''))
    # The last , or . is the decimal mark when two digits follow it (1.234,56 or 99,50); any other is a thousands mark.
    m = re.fullmatch(r'(.*)[.,](\d{1,2})', v)
    v = re.sub(r'[.,]', '', m.group(1)) + '.' + m.group(2) if m else re.sub(r'[.,]', '', v)
    try:
        return float(v) if v not in ('', '-', '.') else 0.0
    except ValueError:
        return 0.0


def day(v):
    try:
        return datetime.date.fromisoformat(str(v).strip()[:10])
    except ValueError:
        return None


def read(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return {}, {}
    h = [x for x in rows[0] if x]  # a row longer than the header puts its extra cells under None
    exact = lambda want: next((x for x in h if x.strip().lower() == want), None)
    name = col(h, 'ad name')
    spend = col(h, 'amount spent', 'spend')
    buys = exact('purchases') or col(h, 'purchases', avoid=('value', 'cost', 'roas', 'rate', 'in-app'))
    counts = 'purchases'
    if not buys:
        buys, counts = exact('leads') or col(h, 'leads', avoid=('value', 'cost', 'rate')), 'leads'
    value = col(h, 'purchases conversion value', 'conversion value', 'purchase value')
    roas = col(h, 'purchase roas', 'roas')
    imps = exact('impressions') or col(h, 'impressions', avoid=('cpm', 'cost'))
    if not (name and spend and buys):
        sys.exit(f'{path}: needs the Ad name, Amount spent and Purchases (or Leads) columns (Results counts other objectives too, '
                 f'so add Purchases or Leads under Columns → Customize columns); found {h}')
    cur = re.search(r'\(([A-Z]{3})\)', spend)
    starts = [d for d in (day(r.get(col(h, 'reporting starts') or '')) for r in rows) if d]
    ends = [d for d in (day(r.get(col(h, 'reporting ends') or '')) for r in rows) if d]
    meta = {'columns': {'ad': name, 'spend': spend, 'purchases': buys, 'value': value or roas, 'impressions': imps},
            'currency': cur.group(1) if cur else None, 'counts': counts, 'from': None, 'to': None, 'export_total': None}
    if starts and ends:
        meta['from'], meta['to'] = str(min(starts)), str(max(ends))
        span = (max(ends) - min(starts)).days + 1
        if span > 7:
            sys.exit(f'{path} covers {span} days ({min(starts)} to {max(ends)}). Export one week per file: Last 7 days, and the 7 days before.')
    named = [r for r in rows if (r.get(name) or '').strip()]
    # The export's summary row: blank-named, or labelled "Total" or "Results from N ads" with the others' sum.
    # A real ad that happens to spend what the rest did together stays an ad.
    whole = sum(money(r.get(spend)) for r in rows if not (r.get(name) or '').strip())
    near = lambda a, b: abs(a - b) <= 0.01 * b
    for r in named:
        if not re.fullmatch(r'\s*(total|results from \d+.*)\s*', r[name], re.I):
            continue
        others = [x for x in named if x is not r]
        rest, rest_buys = (sum(money(x.get(k)) for x in others) for k in (spend, buys))
        if rest and near(money(r.get(spend)), rest) and near(money(r.get(buys)), rest_buys):
            whole, named = money(r.get(spend)), others
            break
    meta['export_total'] = round(whole, 2) or None
    ads = defaultdict(lambda: {'spend': 0.0, 'buys': 0.0, 'value': 0.0, 'imps': 0.0})
    for r in named:
        a = ads[r[name].strip()]
        s = money(r.get(spend))
        a['spend'] += s
        a['buys'] += money(r.get(buys))
        a['value'] += money(r.get(value)) if value else money(r.get(roas)) * s if roas else 0.0
        a['imps'] += money(r.get(imps)) if imps else 0.0
    # An ad that didn't deliver this week isn't one of the week's ads; against last week it shows as stopped.
    return {n: a for n, a in ads.items() if a['spend'] or a['buys']}, meta


def sums(ads):
    t = {k: sum(a[k] for a in ads.values()) for k in ('spend', 'buys', 'value', 'imps')}
    return stats(t) | {'ads': len(ads)}


def stats(a):
    out = {'spend': round(a['spend'], 2), 'purchases': round(a['buys'], 1)}
    out['cpa'] = round(a['spend'] / a['buys'], 2) if a['buys'] else None
    out['roas'] = round(a['value'] / a['spend'], 2) if a['spend'] and a['value'] else None
    out['cpm'] = round(a['spend'] / a['imps'] * 1000, 2) if a['imps'] else None
    return out


def words(ads, total):
    by = defaultdict(lambda: {'spend': 0.0, 'buys': 0.0, 'value': 0.0, 'imps': 0.0, 'n': 0})
    for n, a in ads.items():
        for w in {w for w in SPLIT.split(n) if len(w) > 1 and not w.isdigit() and w.lower() != 'wa' and not re.fullmatch(r'v\d+', w, re.I)}:
            b = by[w.lower()]
            for k in ('spend', 'buys', 'value', 'imps'):
                b[k] += a[k]
            b['n'] += 1
    rows = [{'word': w, 'ads': b['n'], 'share': round(b['spend'] / total, 3) if total else None} | stats(b)
            for w, b in by.items() if b['n'] >= 2 and b['n'] < len(ads)]
    return sorted(rows, key=lambda r: -r['spend'])[:15]


def main(argv):
    if not argv or argv[0].startswith('-'):
        sys.exit(__doc__)
    opt = lambda k: argv[argv.index(k) + 1] if k in argv else None
    now, meta = read(argv[0])
    last, last_meta = read(opt('--last')) if opt('--last') else ({}, {})
    if last_meta.get('to') and meta.get('from') and last_meta['to'] >= meta['from']:
        sys.exit(f"--last ({last_meta['from']} to {last_meta['to']}) must end before this week starts ({meta['from']}): "
                 "pass this week's export first, then --last with the week before.")
    codes = set()
    if opt('--codes'):
        codes = {norm(c) for c in CODE.findall(open(opt('--codes')).read())}
    t = sums(now)
    rows = sorted(({'ad': n} | stats(a) for n, a in now.items()), key=lambda r: -r['spend'])
    cpas = [r['cpa'] for r in rows if r['cpa'] and r['spend'] >= 0.01 * t['spend']]
    moved = []
    zero = {'spend': 0.0, 'buys': 0.0, 'value': 0.0, 'imps': 0.0}
    for n in set(now) | set(last) if last else ():
        a, b = now.get(n, zero), last.get(n, zero)
        if n in last:
            moved.append({'ad': n, 'spend_change': round(a['spend'] - b['spend'], 2), 'cpa_now': stats(a)['cpa'],
                          'cpa_last': stats(b)['cpa'], 'stopped': n not in now})
    moved.sort(key=lambda r: -r['spend_change'])
    found = defaultdict(list)
    for r in rows:
        for c in CODE.findall(r['ad']):
            found[norm(c)].append(r)
    out = {
        'read': meta,
        'read_last': last_meta or None,
        'this_week': t,
        'last_week': sums(last) if last else None,
        'median_cpa': round(statistics.median(cpas), 2) if cpas else None,
        'top_by_spend': rows[:10],
        'risers': [m for m in moved if m['spend_change'] > 0][:5],
        'fallers': [m for m in reversed(moved) if m['spend_change'] < 0][:5],
        'new_this_week': [r['ad'] for r in rows if r['ad'] not in last][:10] if last else None,
        'words': words(now, t['spend']),
        'codes_ran': {c: found[c] for c in sorted(found)},
        'codes_not_found': sorted(codes - set(found)),
    }
    if '--json' in argv:
        print(json.dumps(out, indent=1))
        return
    lw = out['last_week'] or {}
    K = 'CPA' if meta['counts'] == 'purchases' else 'cost per lead'
    sign = SIGN.get(meta['currency'], f"{meta['currency']} " if meta['currency'] else '$')
    f = lambda v, p='': '-' if v is None else f'{p}{v:,.2f}'
    c = meta['columns']
    print(f"Read {argv[0]}: {meta['from'] or 'dates not in the export'} to {meta['to'] or '-'}; columns {c['ad']!r}, {c['spend']!r}, {c['purchases']!r}, {c['value']!r}")
    if meta['export_total'] is not None:
        ok = abs(meta['export_total'] - t['spend']) <= 0.01 * max(t['spend'], 1)
        print(f"The export's own total row: {f(meta['export_total'], sign)} ({'matches' if ok else 'DIFFERS from'} the ads' sum)")
    print(f"This week: {t['ads']} ads, spend {f(t['spend'], sign)}, {t['purchases']:g} {meta['counts']}, {K} {f(t['cpa'], sign)}, ROAS {f(t['roas'])}"
          + (f" | last week ({last_meta.get('from') or '?'} to {last_meta.get('to') or '?'}): spend {f(lw.get('spend'), sign)}, {K} {f(lw.get('cpa'), sign)}, ROAS {f(lw.get('roas'))}" if lw else ''))
    print(f"Median {K} of ads with 1%+ of spend: {f(out['median_cpa'], sign)}")
    print('Top by spend:')
    for r in out['top_by_spend']:
        print(f"  {r['ad']}: {f(r['spend'], sign)}, {K} {f(r['cpa'], sign)}, ROAS {f(r['roas'])}")
    for k in ('risers', 'fallers'):
        if out[k]:
            print(f'{k.capitalize()}:')
            for m in out[k]:
                print(f"  {m['ad']}: spend {m['spend_change']:+,.2f}, {K} {f(m['cpa_last'], sign)} → {f(m['cpa_now'], sign)}" + (' (stopped)' if m['stopped'] else ''))
    print('Words in ad names (2+ ads), by spend:')
    for w in out['words']:
        share = '-' if w['share'] is None else f"{w['share']:.0%}"
        print(f"  {w['word']}: {w['ads']} ads, {share} of spend, {K} {f(w['cpa'], sign)}, ROAS {f(w['roas'])}")
    if out['codes_ran'] or codes:
        print('Concepts that ran, by the code in the ad name:')
        for code, rs in out['codes_ran'].items():
            for r in rs:
                print(f"  {code} in {r['ad']}: {f(r['spend'], sign)}, {K} {f(r['cpa'], sign)}")
        if out['codes_not_found']:
            print(f"  not in the export: {', '.join(out['codes_not_found'])}")


if __name__ == '__main__':
    main(sys.argv[1:])
