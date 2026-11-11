#!/usr/bin/env python3
"""Check a creator's draft against their brief: the words word for word, the rest listed to look at.

    python3 check_draft.py BRIEFS.md --creator NAME --transcript FILE [--brief WORDS] [--caption FILE] [--probe probe.json] [--json]

BRIEFS.md is the briefs doc (newest first) or one brief: each starts "## [creator] · [the video] · …" with
parts **1.** to **7.** (the brief skill's page), one brief per video. Of the briefs whose title holds NAME,
the one checked is the one whose title holds --brief's words; else, with a transcript, the one whose hooks
and ★ line fit what was said best; else the newest. The others are listed.
FILE is the transcript: .srt or .vtt with times, or plain text (then no times). --caption is the post
caption the creator sent, as a file or the text itself. --probe is draft.py's probe.json.

Ticks what words can settle, from the brief's own lines:
  - the hook: which of the brief's hooks was said first, and word for word or not, with the difference;
  - the ★ line: where it was said and word for word or not, with the difference;
  - the disclosure: #ad or the paid-partnership words in the caption or the words said;
  - 9:16 at 1080 x 1920 when the brief asks for it.
Lists the rest of the must-haves (the brief's "Fixed:" and "We approve it when …") and part 6's don'ts as
LOOK, for the frames and the words.
A one-word difference that sounds like the brief's word is marked "check by ear": transcribers mishear names.
Prints the earlier draft reviews under that brief, so the round can be counted. Exits 1 when a tick fails.
"""
import argparse, difflib, json, os, re, sys

PART = re.compile(r'^\s*\*\*([1-7])\.', re.M)
BULLET = re.compile(r'^\s*[-*•]\s+(.*)$', re.M)
QUOTE = re.compile(r'[“"]([^”"]{3,})[”"]')
CUE_TIME = re.compile(r'(\d+):(\d\d):(\d\d)[,.](\d{1,3})\s*-->\s*(\d+):(\d\d):(\d\d)[,.](\d{1,3})')
SHORT_TIME = re.compile(r'(?:(\d+):)?(\d\d):(\d\d)[.](\d{1,3})\s*-->\s*(?:(\d+):)?(\d\d):(\d\d)[.](\d{1,3})')
DISCLOSE = re.compile(r'#ad\b|#sponsored\b|paid[- ]partnership|\bsponsored\b|\bad\b(?=[^a-z]*$)', re.I)
NEGATED = re.compile(r"(?:\bnot|n't|\bno|\bnon)[\s-]+(?:a\s+)?$", re.I)


def disclosed(text):
    """The first disclosure in text that isn't negated ("not sponsored", "this isn't an ad")."""
    for m in DISCLOSE.finditer(text or ''):
        if not NEGATED.search(text[max(0, m.start() - 12):m.start()]):
            return m.group(0)
    return None
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'twenty thirty forty fifty sixty seventy eighty ninety'.split()


def spell(n):
    n = int(n)
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10 - 2] + ('' if n % 10 == 0 else ' ' + ONES[n % 10])
    return str(n)


def words(text):
    text = text.lower().replace('’', "'").replace('‘', "'").replace('&', ' and ').replace('%', ' percent')
    text = re.sub(r'\b(\d{1,2})\b', lambda m: spell(m.group(1)), text)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text)


def stamp(t):
    return '?' if t is None else f'{int(t // 60)}:{t % 60:04.1f}'


def secs(h, m, s, ms):
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + int(ms.ljust(3, '0')) / 1000


def read_transcript(path):
    """[(start seconds or None, text)] in order."""
    text = open(path, encoding='utf-8', errors='ignore').read()
    cues, cur = [], None
    for line in text.splitlines():
        m = CUE_TIME.search(line) or SHORT_TIME.search(line)
        if m:
            g = m.groups()
            cur = [secs(*g[:4]), '']
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit() and line.strip() != 'WEBVTT':
            cur[1] += ' ' + re.sub(r'<[^>]+>', '', line.strip())
    if not cues:
        return [(None, text)]
    return [(t, s.strip()) for t, s in cues]


def timed_words(cues):
    out = []
    for t, s in cues:
        out += [(t, w) for w in words(s)]
    return out


def close(a, b):
    """Sounds like the same word: a transcriber's slip on a name ("Potty" for "Potly"), not a new word."""
    if a == b:
        return True
    if min(len(a), len(b)) < 4:
        return False
    r = difflib.SequenceMatcher(None, a, b).ratio()
    return r >= 0.7 or (r >= 0.6 and a[0] == b[0])


def soft(seg, want):
    """seg with each near-miss of a brief word read as that word, for finding where a line was said."""
    have = set(want)
    return [w if w in have else next((x for x in want if close(x, w)), w) for w in seg]


def compare(want, said):
    """The differences between the brief's words and the words said, and whether they're only a near-miss of one word."""
    sm = difflib.SequenceMatcher(None, want, said, autojunk=False)
    diffs, ear = [], True
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            continue
        w, s = ' '.join(want[i1:i2]), ' '.join(said[j1:j2])
        diffs.append(f'"{w}" said as "{s}"' if op == 'replace' else f'"{w}" left out' if op == 'delete' else f'"{s}" added')
        if not (op == 'replace' and i2 - i1 == 1 and j2 - j1 == 1 and close(want[i1], said[j1])):
            ear = False
    return diffs, (ear and len(diffs) == 1)


def best_window(want, tw, start_only=False):
    """The stretch of the transcript closest to `want`: (ratio, start index, end index)."""
    n, best = len(want), (0.0, 0, 0)
    spans = range(0, 1) if start_only else range(0, max(1, len(tw) - 1))
    for i in spans:
        for k in range(max(1, n - 3), n + 4):
            seg = soft([w for _, w in tw[i:i + k]], want)
            if not seg:
                continue
            r = difflib.SequenceMatcher(None, want, seg, autojunk=False).ratio()
            if r > best[0]:
                best = (r, i, i + k)
    return best


def parse_briefs(path, creator):
    """Every brief in the doc whose title holds the creator's name, newest (first) first."""
    text = open(path, encoding='utf-8').read()
    heads = list(re.finditer(r'^## (.+)$', text, re.M))
    mine = [(h, i) for i, h in enumerate(heads) if creator.lower() in h.group(1).lower()]
    if not mine:
        names = '; '.join(h.group(1).strip() for h in heads) or 'none'
        sys.exit(f'no brief for "{creator}" in {path}. Briefs there: {names}')
    return [parse_one(text, heads, h, i) for h, i in mine]


def parse_one(text, heads, h, i):
    body = text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(text)]
    reviews = re.findall(r'^###\s*Draft review[^\n]*', body, re.M)
    body_brief = re.split(r'^###\s*Draft review', body, flags=re.M)[0]
    cuts = [m for m in PART.finditer(body_brief)]
    part = {}
    for j, m in enumerate(cuts):
        part[int(m.group(1))] = body_brief[m.start():cuts[j + 1].start() if j + 1 < len(cuts) else len(body_brief)]
    hooks = []
    for b in BULLET.findall(part.get(2, '')):
        q = QUOTE.findall(b)
        hooks.append(q[0] if q else re.sub(r'\*\*[^*]*\*\*|\([^)]*\)', '', b).strip(' :-–'))
    star = None
    for b in BULLET.findall(part.get(3, '')):
        if '★' in b:
            q = QUOTE.findall(b)
            star = q[0] if q else b.replace('★', '').strip(' :-–')
    p7 = part.get(7, '')
    fixed = re.search(r'Fixed:\s*([^.]*(?:\.\d[^.]*)*)\.', p7)
    approve = re.search(r'approve it when\s*([^\n]*?)(?:\.\s|\.$|$)', p7, re.I | re.M)
    donts = [re.sub(r"^\s*don'?t:?\s*", '', b, flags=re.I).strip() for b in BULLET.findall(part.get(6, ''))
             if re.match(r"\s*don'?t\b", b.replace('’', "'"), re.I)]
    return {'title': h.group(1).strip(), 'hooks': hooks, 'star': star, 'donts': donts,
            'fixed': fixed.group(1).strip() if fixed else '', 'approve': approve.group(1).strip() if approve else '',
            'format': bool(re.search(r'9:16|1080\s*[x×]\s*1920', p7)), 'reviews': reviews}


def fit(b, tw):
    """How well a brief's hooks (at the opening) and ★ line (anywhere) match what was said."""
    hook = max((best_window(words(x), tw[:len(words(x)) + 6])[0] for x in b['hooks']), default=0)
    star = best_window(words(b['star']), tw)[0] if b['star'] else 0
    return hook + star


def choose(briefs, want, tw):
    if want:
        hit = [b for b in briefs if want.lower() in b['title'].lower()]
        if not hit:
            sys.exit(f'no brief for that creator holds "{want}". Theirs: ' + '; '.join(b['title'] for b in briefs))
        return hit[0], 'its title holds "' + want + '"'
    if len(briefs) == 1:
        return briefs[0], ''
    if tw:
        b = max(briefs, key=lambda x: fit(x, tw))
        return b, 'its hooks and ★ line fit what was said best'
    return briefs[0], 'the newest; with no transcript, pass --brief to pick another'


def items(clause):
    clause = re.sub(r',?\s+and\s+', ', ', clause)
    return [x.strip(' .') for x in clause.split(',') if x.strip(' .')]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('briefs')
    ap.add_argument('--creator', required=True)
    ap.add_argument('--transcript')
    ap.add_argument('--brief', help="words from the title of the video's brief, when the creator has several")
    ap.add_argument('--caption')
    ap.add_argument('--probe')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    briefs = parse_briefs(a.briefs, a.creator)
    cues = read_transcript(a.transcript) if a.transcript else []
    tw = timed_words(cues)
    timed = any(t is not None for t, _ in cues)
    b, why = choose(briefs, a.brief, tw)
    others = [x['title'] for x in briefs if x is not b]
    out = {'brief': b['title'], 'why': why, 'other_briefs': others, 'earlier_reviews': b['reviews'], 'ticks': [], 'look': []}

    def tick(item, ok, said, note=''):
        out['ticks'].append({'item': item, 'ok': ok, 'evidence': said, 'note': note})

    # The hook: the first words said against each of the brief's hooks.
    if not tw:
        tick('hook word for word', None, 'no transcript', 'paste the transcript or captions to check the words')
    elif b['hooks']:
        tries = []
        for k, hook in enumerate(b['hooks']):
            want = words(hook)
            r, i, j = best_window(want, tw[:len(want) + 6], start_only=False)
            tries.append((r, k, hook, want, i, j))
        r, k, hook, want, i, j = max(tries)
        said = [w for _, w in tw[i:j]]
        if r < 0.5:
            opening = ' '.join(w for _, w in tw[:12])
            tick('hook word for word', False, f'none of the brief\'s hooks opens it; it opens on: "{opening}"',
                 'brief: ' + ' / '.join(f'"{h}"' for h in b['hooks']))
            said = None
        diffs, ear = compare(want, said) if said is not None else ([], False)
        which = 'the hook' if k == 0 else f'alternate {k}'
        at = stamp(tw[i][0]) if timed else 'the start'
        late = timed and tw[i][0] is not None and tw[i][0] > 1.5
        if said is None:
            pass
        elif not diffs:
            tick('hook word for word', True, f'{which}, said at {at}: "{hook}"', 'starts after 1.5 s' if late else '')
        else:
            tick('hook word for word', 'ear' if ear else False, f'{which} at {at}; brief: "{hook}"; said: "{" ".join(said)}"', '; '.join(diffs))
    # The ★ line: anywhere in what's said.
    if b['star'] and tw:
        want = words(b['star'])
        r, i, j = best_window(want, tw)
        said = [w for _, w in tw[i:j]]
        diffs, ear = compare(want, said)
        at = stamp(tw[i][0]) if timed else '?'
        if r < 0.5:
            tick('★ line said as written', False, f'not found; brief: "{b["star"]}"', 'nothing said comes close')
        elif not diffs:
            tick('★ line said as written', True, f'at {at}: "{b["star"]}"')
        else:
            tick('★ line said as written', 'ear' if ear else False, f'at {at}; brief: "{b["star"]}"; said: "{" ".join(said)}"', '; '.join(diffs))
    elif b['star']:
        tick('★ line said as written', None, 'no transcript', 'paste the transcript or captions to check the words')
    # The disclosure: the caption they sent, or said out loud. The platform label is switched on at posting.
    cap = ''
    if a.caption:
        cap = open(a.caption, encoding='utf-8').read() if os.path.exists(a.caption) else a.caption
    spoken = ' '.join(s for _, s in cues)
    if cap and disclosed(cap):
        tick('disclosure', True, f'in the caption: "{disclosed(cap)}"', 'the paid-partnership label is switched on at posting: check the live post')
    elif disclosed(spoken):
        tick('disclosure', True, 'said in the video', 'the paid-partnership label is switched on at posting: check the live post')
    elif cap:
        tick('disclosure', False, 'no #ad or paid-partnership words in the caption they sent', 'add #ad; the label is switched on at posting')
    else:
        tick('disclosure', None, 'no caption given', 'ask for the post caption; the label is switched on at posting')
    # The format the brief asks for.
    if b['format'] and a.probe and os.path.exists(a.probe):
        p = json.load(open(a.probe))
        tick('9:16 at 1080 x 1920', p.get('full_hd_vertical'), f"{p.get('width')} x {p.get('height')}, {p.get('seconds')} s")
    # Everything else the brief makes a must-have: looked at in the frames.
    covered = re.compile(r'hook|★|disclos|#ad|label|partnership', re.I)
    seen = set()
    for src, clause in (('Fixed', b['fixed']), ('approve it when', b['approve'])):
        for it in items(clause):
            key = re.sub(r'\W+', ' ', it.lower()).strip()
            if covered.search(it) or key in seen:
                continue
            seen.add(key)
            out['look'].append(f'{it} ({src})')
    if b['hooks']:
        out['look'].insert(0, 'the hook on screen from the first frame, the same words as said (part 2)')
    out['look'] += [f"don't: {d} (part 6): nothing said or shown does it" for d in b['donts']]
    if not a.json:
        print(f"Brief: {b['title']}" + (f" ({why})" if why else ''))
        if others:
            print('Their other briefs: ' + '; '.join(others))
        print(f"Earlier draft reviews under it: {len(b['reviews'])}" + ''.join(f'\n  {r}' for r in b['reviews']))
        if not tw:
            print('No transcript: the word checks wait for one.')
        elif not timed:
            print('The transcript has no times: notes give the line instead of the time.')
        for t in out['ticks']:
            mark = {True: 'OK  ', False: 'FIX ', 'ear': 'EAR ', None: '??  '}[t['ok']]
            print(f"{mark}{t['item']}: {t['evidence']}" + (f"\n      {t['note']}" if t['note'] else ''))
        for x in out['look']:
            print(f'LOOK {x}')
    else:
        print(json.dumps(out, indent=1, ensure_ascii=False))
    return 1 if any(t['ok'] is False for t in out['ticks']) else 0


if __name__ == '__main__':
    sys.exit(main())
