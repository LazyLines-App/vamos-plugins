"""Check creator briefs against the rules that always hold.

  python3 scripts/check_brief.py briefs.md [--rows rows.json] [--only "Maya"] [--json]

briefs.md holds one or more briefs, each starting with a line "## [creator] · …" and seven parts
marked **1.** to **7.** (references/brief.md). --rows is the Vamos answer or rows file (any text):
every link in part 5 must appear in it. --only checks the briefs whose title contains the text.
Exits 1 when any brief fails; prints what to fix.
"""
import json, re, sys

PART = re.compile(r'^\s*\*\*([1-7])\.', re.M)
BULLET = re.compile(r'^\s*[-*•]\s+(.*)$', re.M)
LINK = re.compile(r'https?://[^\s)\]>"]+')
ANALYSIS = re.compile(r'\d+(?:[.,]\d+)?\s?×(?!\s?\d)|\b\d+(?:\.\d+)?x\s+(?:usual|their|her|his|its|the|our|your|average)\b'
                      r'|\b(?:usual|outlier|median|engagement rate|algorithm)\b', re.I)
BY_3S = re.compile(r'\b(?:3|three)\s?(?:s|sec|secs|seconds)\b|first frame|0\s?[–-]\s?3\b', re.I)
DISCLOSE = re.compile(r'#ad\b|paid[- ]partnership|branded content|promotional content', re.I)
SLOT = re.compile(r'\[(?![^\]]*\]\()([^\]\n]{1,80})\]')


def words(text):
    text = LINK.sub('link', text)
    return [w for w in re.findall(r"[\w'’]+", text)]


def norm(url):
    url = url.split('?')[0].split('#')[0].rstrip('/.,;:!').lower()
    return re.sub(r'^https?://(www\.|m\.)?', '', url)


def hook_text(line):
    q = re.findall(r'[“"]([^”"]+)[”"]', line)
    return q[0] if q else re.sub(r'\*\*[^*]*\*\*|\([^)]*\)', '', line).strip(' :-–')


def check(title, body, rows):
    errors, notes = [], []
    n = len(words(body))
    if not 300 <= n <= 500:
        errors.append(f'{n} words; a brief is 300 to 500')
    if re.search(r'^\s*\|', body, re.M):
        errors.append('a table; a phone page has none (talking points are bullets)')
    for m in ANALYSIS.finditer(body):
        errors.append(f'analysis on the creator\'s page: "{m.group(0)}" (multiples and the usual stay with you)')
    found = [int(x) for x in PART.findall(body)]
    if found != list(range(1, 8)):
        errors.append(f'parts {found}; need **1.** to **7.** once each, in order')
        return n, errors, notes
    cuts = [m.start() for m in PART.finditer(body)] + [len(body)]
    part = {i + 1: body[cuts[i]:cuts[i + 1]] for i in range(7)}

    hooks = [hook_text(b) for b in BULLET.findall(part[2])]
    if not 2 <= len(hooks) <= 3:
        errors.append(f'{len(hooks)} hooks; part 2 is the hook and one or two alternates, one bullet each')
    for h in hooks:
        k = len(words(h))
        if k >= 12:
            errors.append(f'hook of {k} words; under 12: "{h}"')
    if not re.search(r'on screen', part[2], re.I):
        errors.append('part 2 must say the same words go on screen from the first frame')

    beats = BULLET.findall(part[3])
    if len(beats) != 3:
        errors.append(f'{len(beats)} beats; part 3 is 3 talking points')
    if not any('★' in b for b in beats):
        errors.append('no must-say line marked ★ in part 3')

    if not BY_3S.search(part[4]):
        errors.append('part 4 must put the product on screen by 3 s')

    links = LINK.findall(part[5])
    if not 1 <= len(links) <= 3:
        errors.append(f'{len(links)} reference links; part 5 has 1 to 3 (2 or 3 when the research found them)')
    if rows is not None:
        have = {norm(u) for u in LINK.findall(rows)}
        for u in links:
            if norm(u) not in have:
                errors.append(f'link not in the Vamos answer: {u}')

    if not DISCLOSE.search(part[6] + part[7]):
        errors.append('no disclosure in part 6 or 7: the platform label (paid partnership, branded content) or #ad')
    if not re.search(r'\bdue\b', part[7], re.I):
        errors.append('part 7 has no due date')
    if not re.search(r'approve', part[7], re.I):
        errors.append('part 7 must say when it is approved')

    slots = list(dict.fromkeys(SLOT.findall(body)))
    if slots:
        notes.append('slots to fill: ' + '; '.join(f'[{s}]' for s in slots))
    return n, errors, notes


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 2
    path, rows, only, as_json = argv[0], None, None, '--json' in argv
    if '--rows' in argv:
        rows = open(argv[argv.index('--rows') + 1], errors='ignore').read()
    if '--only' in argv:
        only = argv[argv.index('--only') + 1]
    text = open(path).read()
    heads = list(re.finditer(r'^## (.+)$', text, re.M))
    briefs = [(h.group(1).strip(), text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)])
              for i, h in enumerate(heads)]
    if only:
        briefs = [b for b in briefs if only.lower() in b[0].lower()]
    if not briefs:
        print('no briefs found: each starts with a line "## [creator] · [the video]"')
        return 1
    out, failed = [], 0
    for title, body in briefs:
        n, errors, notes = check(title, body, rows)
        failed += bool(errors)
        out.append({'brief': title, 'words': n, 'ok': not errors, 'errors': errors, 'notes': notes})
    if as_json:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    else:
        for r in out:
            print(('PASS ' if r['ok'] else 'FAIL ') + f"{r['brief']} ({r['words']} words)")
            for e in r['errors']:
                print('  - ' + e)
            for x in r['notes']:
                print('  · ' + x)
        print(f'{len(out) - failed} of {len(out)} pass')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
