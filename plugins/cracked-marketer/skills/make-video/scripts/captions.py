#!/usr/bin/env python3
"""Captions broken where a speaker pauses, from the voice's word times.

  python3 captions.py words.json --script script.txt [--max-words 6] [--max-chars 28] > captions.json

A caption ends at a full stop, comma or other mark in the script, or at a pause in the voice. A longer phrase is
split into the fewest captions that fit, before words that start a phrase ("in your niche", "that did", "and
writes"), never after a little word that needs the next one ("scroll past are", "times their", "work can be").
Words keep their own times, so the build can still light them one by one. Prints JSON:
[{"text", "start", "end", "words": [{"word", "start", "end"}]}], which check-video.py reads with --captions.
Use --max-words 3 for a voice over a demo.
"""
import argparse, difflib, json, sys
import checklib as c

# A caption never ends on one of these unless a mark follows it: each needs the word after it.
NEEDS_NEXT = set('''a an the this that these those my your his her its our their each every some any no
of in on at to for with from by about into onto over under after before between through than as like per via
and or but so if because when while which who whose where whether what how why
is are was were be been being am do does did can could will would should shall may might must have has had
not very just also it's i'm you're we're they're there's here's i'll you'll we'll i'd you'd
'''.split())
# A phrase starts here: a long one splits before these first ("you're wrong", "in your niche", "and writes").
STARTS = set('''in on at to for with from by about into over under after before through than like
and or but so if because when while that which who whose where then
it's i'm you're we're they're there's here's i'll you'll we'll'''.split())
PRONOUNS = set('i you we they he she it'.split())
AUX = set('is are was were be am do does did can could will would should may might must have has had'.split())
MARKS = ('.', ',', '!', '?', ';', ':', '—', '–', '…')


def bare(w):
    return w.lower().replace('’', "'").strip('.,!?;:"\'()“”‘—–…')


def loud(w):
    w = w.strip('.,!?;:"\'()\u201c\u201d\u2018\u2019')
    return len(w) >= 8 or (len(w) >= 3 and w.isupper())


def ends_phrase(w):
    return w.rstrip('"\')”’').endswith(MARKS)


def needs_next(left, right):
    """True when `left` can't end a caption: a little word that needs the next one, or "you | can"."""
    a, b = bare(left['word']), bare(right['word'])
    return not ends_phrase(left['word']) and (a in NEEDS_NEXT or (a in PRONOUNS and b in AUX))


def break_cost(left, right):
    """What it costs to end a caption after `left` and start the next with `right` (lower is better)."""
    b = bare(right['word'])
    cost = 0.5 if b in STARTS else 1.0 if b in NEEDS_NEXT or (b.endswith('ing') and len(b) > 4) else 2.0
    return cost - min(right['start'] - left['end'], 0.3) * 2  # a small pause is a good place


def display_words(words, script):
    """The voice's timed words, shown as the script writes them where the two agree."""
    if not script:
        return [dict(w) for w in words]
    shown = script.split()
    key = lambda w: ' '.join(c.tokens(w))
    out = []
    sm = difflib.SequenceMatcher(None, [key(w) for w in shown], [key(w['word']) for w in words], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':  # the script's spelling and marks, but a number as the digits heard ("20 or 30 times")
            out += [dict(words[j], word=shown[i] if not any(ch.isdigit() for ch in words[j]['word'])
                         else words[j]['word'].rstrip('.,!?;:') + shown[i][len(shown[i].rstrip('.,!?;:')):])
                    for i, j in zip(range(i1, i2), range(j1, j2))]
        elif op == 'replace' and j2 > j1:  # a word the transcriber misheard ("Potly" as "Podly"): the script's
            # words over the voice's span, shared out by length, so a brand name is never captioned misspelled
            ws, t0, t1 = shown[i1:i2], words[j1]['start'], words[j2 - 1]['end']
            total, at = sum(len(w) for w in ws), t0
            for w in ws:
                end = at + (t1 - t0) * len(w) / total
                out.append({'word': w, 'start': round(at, 3), 'end': round(end, 3)})
                at = end
        elif op == 'insert':  # said but not in the script: captioned as said
            out += [dict(w) for w in words[j1:j2]]
    return out


def fits(ws, max_words, max_chars):
    return len(ws) <= max_words and len(' '.join(w['word'] for w in ws)) <= max_chars


def split(ws, max_words, max_chars):
    """The fewest, best-placed captions for one phrase (a small search over every place to break). A caption never
    ends on a word that needs the next one; when no other break fits, it runs past the word limit instead."""
    n = len(ws)
    best = [0.0] + [None] * n
    back = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(j):
            if best[i] is None or (j < n and needs_next(ws[j - 1], ws[j])):
                continue
            text = ' '.join(w['word'] for w in ws[i:j])
            over = 0 if j - i == 1 or fits(ws[i:j], max_words, max_chars) else 5.0 * (j - i - max_words + 1)
            cost = best[i] + 1.0 + over + 0.002 * len(text) ** 2 + (break_cost(ws[i - 1], ws[i]) if i else 0.0)
            if j - i == 1 and n > 1 and not loud(ws[i]['word']):
                cost += 1.5  # a lone word reads as an orphan, unless it is the word to shout ("HOOKS")
            if best[j] is None or cost < best[j]:
                best[j], back[j] = cost, i
    out, j = [], n
    while j:
        out.insert(0, ws[back[j]:j])
        j = back[j]
    return out


def phrases(words, max_words=6, max_chars=28, pause=0.35):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        gap = nxt['start'] - w['end'] if nxt else 9
        if ends_phrase(w['word']) or (gap >= pause and not (nxt and needs_next(w, nxt))):
            out += split(cur, max_words, max_chars)
            cur = []
    if cur:
        out += split(cur, max_words, max_chars)
    return out


def cues(groups, lead=0.2, tail=0.4):
    out = []
    for k, g in enumerate(groups):
        start = g[0]['start'] - lead
        if out:  # never before the last word of the caption before is half said: every word shows at its midpoint
            prev = groups[k - 1][-1]
            start = max(start, (prev['start'] + prev['end']) / 2 + 0.02)
            if out[-1]['end'] >= g[0]['start'] - lead - 1e-6:  # back to back: the one before ends as this starts
                out[-1]['end'] = round(start, 3)
        start = max(start, 0.0)
        nxt = groups[k + 1][0]['start'] - lead if k + 1 < len(groups) else None
        end = nxt if nxt is not None and nxt - g[-1]['end'] < 1.0 else g[-1]['end'] + tail
        out.append({'text': ' '.join(w['word'] for w in g), 'start': round(start, 3), 'end': round(end, 3),
                    'words': [{'word': w['word'], 'start': w['start'], 'end': w['end']} for w in g]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('words', help="the voice's word times (JSON)")
    ap.add_argument('--script', help='the script as a text file, for its marks and spelling')
    ap.add_argument('--max-words', type=int, default=6)
    ap.add_argument('--max-chars', type=int, default=28)
    a = ap.parse_args()
    script = c.said(open(a.script).read()) if a.script else None  # stage directions in [brackets] left out
    out = cues(phrases(display_words(c.load_words(a.words), script), a.max_words, a.max_chars))
    json.dump(out, sys.stdout, indent=1)
    print()
    for q in out:
        print(f'{q["start"]:6.2f}  {q["text"]}', file=sys.stderr)


if __name__ == '__main__':
    main()
