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
    sections = []
    for item in summary['formats']:
        lines = [f"## {markdown(item['name'])}"]
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
        sections.append('\n'.join(lines))
    return '\n\n'.join(sections)


def main():
    """Read one bounded local export or stdin and emit JSON for matching cards, or a Markdown measurement block."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rows', help='Saved JSON export, or - for stdin. Download signed URLs once with curl first.')
    parser.add_argument('--json', action='store_true', help='Emit structured rows instead of Markdown')
    parser.add_argument('--format-id', action='append', help='Only emit these named formats; repeat for several')
    parser.add_argument('--compact', action='store_true', help='Keep weekly values in short lines instead of the full table')
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
