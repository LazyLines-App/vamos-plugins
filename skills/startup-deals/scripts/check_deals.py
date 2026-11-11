"""Check the deals list before it ships or after an edit.

  python3 scripts/check_deals.py [references/deals.md]

Fails when a row has no source tag and date, or when a kit price that could be summed isn't official.
Warns when a row is over 30 days old, so the list gets re-read.
"""
import datetime, os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'references', 'deals.md')
SOURCE = re.compile(r'^(official|secondhand|unverified) · (\d{4}-\d{2}-\d{2})$')
today = datetime.date.today()
problems, warnings, rows, section = [], [], 0, ''

for n, line in enumerate(open(path), 1):
    if line.startswith('## '):
        section = line[3:].strip()
    cells = [c.strip() for c in line.strip().strip('|').split('|')] if line.startswith('|') else []
    if len(cells) < 4 or cells[0] in ('Program', 'Piece') or set(cells[0]) <= set('-'):
        continue
    rows += 1
    m = SOURCE.match(cells[-1])
    if not m:
        problems.append(f'line {n}: last cell must be "official|secondhand|unverified · YYYY-MM-DD": {cells[-1]!r}')
        continue
    age = (today - datetime.date.fromisoformat(m.group(2))).days
    if age > 30:
        warnings.append(f'line {n}: {cells[0]} read {age} days ago')
    if section.startswith("The kit") and re.search(r'\d', cells[2]) and 'not in a total' not in cells[2] and m.group(1) != 'official':
        problems.append(f'line {n}: {cells[0]} has a price but is {m.group(1)}; mark it "not in a total"')

print('\n'.join(['warn: ' + w for w in warnings] + problems) or f'ok: {rows} rows')
sys.exit(1 if problems else 0)
