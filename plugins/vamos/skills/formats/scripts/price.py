"""Read optional weekly-format measurements from a saved Vamos export, without network calls."""
import argparse
import datetime as dt
import json
import math
import pathlib
import re
import sys

MAX_BYTES = 16 * 1024 * 1024
MAX_ROWS = 10000
BLOCKS = '▁▂▃▄▅▆▇█'
INTEGER_FIELDS = ('weeks', 'posts', 'niche_posts', 'views_posts', 'multiple_posts')
MEASUREMENTS = ('share', 'median_views', 'median_multiple', 'views_age_days')
ROW_FIELDS = ('kind', 'format_id', 'name', 'niche', 'niche_role', 'week_start',
              *INTEGER_FIELDS, *MEASUREMENTS, 'views_basis', 'too_new')


def valid_row(row):
    """Validate the external row before using its values; never coerce missing measurements to zero."""
    if not isinstance(row, dict) or row.get('kind') != 'format_week':
        return False
    if any(not isinstance(row.get(key), str) or not row[key] or len(row[key]) > 500
           for key in ('format_id', 'name', 'niche')):
        return False
    if row.get('niche_role') not in ('yours', 'next_door') or row.get('views_basis') != 'latest':
        return False
    if type(row.get('too_new')) is not bool or not re.fullmatch(r'[a-z_]+', row['niche']):
        return False
    if any(type(row.get(key)) is not int or row[key] < 0 for key in INTEGER_FIELDS):
        return False
    if row['weeks'] > 8 or row['views_posts'] > row['posts'] or row['multiple_posts'] > row['posts']:
        return False
    for key in MEASUREMENTS:
        value = row.get(key)
        if key not in row or (value is not None and
                              (type(value) not in (int, float) or not math.isfinite(value) or value < 0)):
            return False
    if ((row['median_views'] is not None or row['views_age_days'] is not None) and row['views_posts'] == 0
            or row['median_multiple'] is not None and row['multiple_posts'] == 0):
        return False
    if row['share'] is not None and row['share'] > 1:
        return False
    if row['too_new'] and any(row[key] is not None for key in ('median_views', 'median_multiple', 'views_age_days')):
        return False
    week = row.get('week_start')
    if 'week_start' not in row:
        return False
    if week is not None:
        try:
            date = dt.date.fromisoformat(week)
        except (TypeError, ValueError):
            return False
        if date.isoformat() != week or date.weekday() != 0 or row['weeks'] != 1:
            return False
    return True


def summarise(data, selected=None):
    """Group validated source rows only for formats named in the answer, retaining their supplied values."""
    if isinstance(data, dict) and isinstance(data.get('data'), dict):
        data = data['data']
    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        raise ValueError('Expected a schema_version 1 answer-data export')
    result = {'formats': [], 'warnings': []}
    if 'format_weeks' not in data:
        return result
    rows = data['format_weeks']
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise ValueError('Weekly rows are not a bounded list')
    formats = data.get('formats', [])
    if not isinstance(formats, list):
        raise ValueError('Named formats are not a list')
    named = {}
    for item in formats:
        if (isinstance(item, dict) and isinstance(item.get('format_id'), str)
                and isinstance(item.get('name'), str) and item.get('cited') is not False
                and (selected is None or item['format_id'] in selected)):
            named.setdefault(item['format_id'], item['name'])
    groups, duplicates = {}, set()
    for row in rows:
        if not valid_row(row):
            result['warnings'].append('Skipped a malformed weekly measurement row')
            continue
        if row['format_id'] not in named:
            continue
        key = (row['format_id'], row['niche'], row['niche_role'])
        identity = (*key, row['week_start'])
        bucket = groups.setdefault(key, {})
        if identity in duplicates:
            continue
        if row['week_start'] in bucket:
            del bucket[row['week_start']]
            duplicates.add(identity)
            result['warnings'].append('Skipped conflicting duplicate weekly measurements')
            continue
        bucket[row['week_start']] = {field: row[field] for field in ROW_FIELDS}
    for format_id, name in named.items():
        niches = []
        for (group_id, niche, role), bucket in groups.items():
            if group_id != format_id or not bucket:
                continue
            weekly = sorted((row for week, row in bucket.items() if week is not None), key=lambda row: row['week_start'])
            if weekly and (dt.date.fromisoformat(weekly[-1]['week_start']) -
                           dt.date.fromisoformat(weekly[0]['week_start'])).days > 49:
                result['warnings'].append('Skipped measurements outside one eight-week window')
                continue
            niches.append({'niche': niche, 'role': role, 'summary': bucket.get(None), 'weekly': weekly})
        if niches:
            result['formats'].append({'format_id': format_id, 'name': name, 'niches': niches})
    return result


def number(value):
    """Keep the supplied precision while adding readable thousands separators."""
    return format(value, ',')


def markdown(value):
    """Keep source labels as table text rather than executable markup or injected sections."""
    return re.sub(r'([\\`*_{}\[\]()#+.!|<>])', r'\\\1', str(value).replace('\n', ' ').replace('\r', ' '))


def views(row):
    """State the actual view measurement and the number of posts behind it."""
    if row['too_new']:
        return 'too new'
    if row['median_views'] is None:
        return 'not measured'
    return f"median {number(row['median_views'])} views, N={row['views_posts']}"


def multiple(row):
    """State a supplied multiple with its own denominator, independently of view availability."""
    if row['too_new'] or row['median_multiple'] is None:
        return 'not measured'
    return f"median {number(row['median_multiple'])}×, N={row['multiple_posts']}"


def week_span(weekly):
    """Fill only missing positions between the supplied first and last publication weeks."""
    if not weekly:
        return []
    start = dt.date.fromisoformat(weekly[0]['week_start'])
    end = dt.date.fromisoformat(weekly[-1]['week_start'])
    return [(start + dt.timedelta(days=offset)).isoformat() for offset in range(0, (end - start).days + 1, 7)]


def spark(values):
    """Draw a zero-based text chart, retaining missing measurements as gaps."""
    maximum = max((value for value in values if value is not None), default=0)
    return ''.join('·' if value is None else BLOCKS[round(value / maximum * (len(BLOCKS) - 1))] if maximum else BLOCKS[0]
                   for value in values)


def to_markdown(summary, compact=False):
    """Render measured library supply and views without changing the format recommendation order."""
    return '\n\n'.join('\n'.join([f"## {markdown(item['name'])}", *format_lines(item, compact)]) for item in summary['formats'])


def format_lines(item, compact=False):
    """One format's measurement block under its heading: each niche's pooled line, chart and weeks."""
    lines = []
    for niche in item['niches']:
        role = 'yours' if niche['role'] == 'yours' else 'next door'
        lines.extend(['', f"### {markdown(niche['niche'].replace('_', ' '))} · {role}", '', 'Views are the latest stored counts, not a measurement at seven days.'])
        pooled = niche['summary']
        if pooled:
            share = 'not measured' if pooled['share'] is None else f"{pooled['share'] * 100:g}%"
            lines.append(f"{pooled['weeks']} readable weeks: {pooled['posts']:,}/{pooled['niche_posts']:,} library posts, share {share}. "
                         f"{views(pooled)}; {multiple(pooled)}.")
            if pooled['views_age_days'] is not None:
                lines.append(f"When views were recorded, posts were a median {number(pooled['views_age_days'])} days old.")
        weekly = niche['weekly']
        by_week = {row['week_start']: row for row in weekly}
        weeks = week_span(weekly)
        if not weeks:
            continue
        view_values = [by_week[week]['median_views'] if week in by_week and not by_week[week]['too_new'] else None for week in weeks]
        post_values = [by_week[week]['posts'] if week in by_week else None for week in weeks]
        lines.extend(['', f"Published weeks {weeks[0]} to {weeks[-1]}:", '```text',
                      'Views  ' + spark(view_values), 'Posts  ' + spark(post_values), '```',
                      'Each line scales from zero to its own maximum. · means no measurement; it is not zero.'])
        if compact:
            lines.append('')
            for week in weeks:
                row = by_week.get(week)
                if row is None:
                    lines.append(f'- {week}: not supplied.')
                    continue
                age = '' if row['views_age_days'] is None else f"; post age {number(row['views_age_days'])}d"
                lines.append(f"- {week}: {row['posts']:,}/{row['niche_posts']:,} library posts; {views(row)}{age}; {multiple(row)}.")
            continue
        lines.extend(['',
                      '| Published week | Library posts | Stored median views | Multiple |',
                      '| --- | --- | --- | --- |'])
        for week in weeks:
            row = by_week.get(week)
            if row is None:
                lines.append(f'| {week} | not supplied | not supplied | not supplied |')
                continue
            age = '' if row['views_age_days'] is None else f"; post age {number(row['views_age_days'])}d"
            lines.append(f"| {week} | {row['posts']:,}/{row['niche_posts']:,} | {views(row)}{age} | {multiple(row)} |")
    return lines


# A number with any grouping or decimal marks, compared by its digits so translated labels and separators still match;
# a chart line, compared as drawn.
TOKEN = re.compile('\\d(?:[\\d,.  \']*\\d)?|[' + BLOCKS + '·]{2,}')


def tokens(lines):
    """The values a block carries, in order, each with the line it sits on: everything a reader could copy wrongly."""
    return [(re.sub(r'\D', '', m.group(0)) if m.group(0)[0].isdigit() else m.group(0), number_line)
            for number_line, line in enumerate(lines) for m in TOKEN.finditer(line)]


def check(summary, reply, order=None, compact=False):
    """Find each format's generated block in a drafted reply, in card order, and name every line whose values changed."""
    items = summary['formats']
    if order:
        items = sorted(items, key=lambda item: order.index(item['format_id']) if item['format_id'] in order else len(order))
    reply_lines = reply.split('\n')
    found = tokens(reply_lines)
    values = [value for value, _ in found]
    cursor, problems = 0, []
    for item in items:
        block = format_lines(item, compact)
        wanted = tokens(block)
        size = len(wanted)
        best, at = -1, cursor
        for start in range(cursor, max(cursor, len(values) - size) + 1):
            score = sum(1 for k, (value, _) in enumerate(wanted) if start + k < len(values) and values[start + k] == value)
            if score > best:
                best, at = score, start
            if best == size:
                break
        if size and best == size:
            cursor = at + size
            continue
        if best * 2 < size:
            problems.append({'name': item['name'], 'kind': 'missing', 'block': block, 'lines': []})
            continue
        differ = []
        for k, (value, line) in enumerate(wanted):
            if at + k >= len(values) or values[at + k] != value:
                reply_line = reply_lines[found[at + k][1]] if at + k < len(found) else ''
                if not differ or differ[-1][0] != line:
                    differ.append((line, reply_line))
        problems.append({'name': item['name'], 'kind': 'changed', 'block': block,
                         'lines': [(block[line], reply_line) for line, reply_line in differ]})
        cursor = at + size
    return problems


def check_report(problems, count):
    """What to fix, in words the reply's writer can act on: each block's changed lines, then the block to put back."""
    if not problems:
        return f'All {count} measurement blocks match price.py.'
    out = []
    for problem in problems:
        if problem['kind'] == 'missing':
            out.append(f"Missing: {problem['name']}. The reply has no copy of its block; insert it under its card:")
        else:
            out.append(f"Changed: {problem['name']}. These lines differ from price.py:")
            out.extend(f"  price.py: {expected.strip()}\n  reply:    {seen.strip()}" for expected, seen in problem['lines'])
            out.append('Put the block back exactly as generated:')
        out.extend(['', *problem['block'], ''])
    return '\n'.join(out)


def main():
    """Read one bounded local export or stdin and emit JSON for matching cards, or a Markdown measurement block."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rows', help='Saved JSON export, or - for stdin. Download signed URLs once with curl first.')
    parser.add_argument('--json', action='store_true', help='Emit structured rows instead of Markdown')
    parser.add_argument('--format-id', action='append', help='Only emit these named formats; repeat for several')
    parser.add_argument('--compact', action='store_true', help='Keep weekly values in short lines instead of the full table')
    parser.add_argument('--check', metavar='REPLY', help='Check a drafted reply holds each block unchanged, in --format-id order')
    args = parser.parse_args()
    try:
        if args.rows == '-':
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        else:
            with pathlib.Path(args.rows).open('rb') as source:
                raw = source.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('Export exceeds 16 MiB')
        summary = summarise(json.loads(raw), set(args.format_id) if args.format_id else None)
        if args.check:
            reply = pathlib.Path(args.check).read_text(encoding='utf-8')
            problems = check(summary, reply, args.format_id, compact=args.compact)
            print(check_report(problems, len(summary['formats'])))
            return 1 if problems else 0
        if args.json:
            print(json.dumps(summary, ensure_ascii=False, allow_nan=False))
        else:
            text = to_markdown(summary, compact=args.compact)
            if text:
                print(text)
            for warning in summary['warnings']:
                print(warning, file=sys.stderr)
    except (OSError, ValueError, TypeError) as error:
        print(f"Could not read weekly format measurements: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
