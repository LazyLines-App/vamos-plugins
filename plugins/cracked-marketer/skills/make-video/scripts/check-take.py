#!/usr/bin/env python3
"""Check one generated take before it goes into the cut. Needs ffmpeg; the words need `npx hyperframes`; the
eyes need macOS (Apple Vision, through eyes.swift).

  python3 check-take.py take.mp4 [--voice voice-video.mp4] [--line "Comment HOOKS and I'll send you the setup."]
                        [--use 0-3.0]

--voice   the black video with the clean read that went to the model: the take's sound must still be that read
          (envelope match 0.9 or more). Under it, the model re-voiced the take and the lips follow its words.
--line    what the take must say: every word heard is set against it.
--use     the stretch of the take the cut uses, in seconds (default: all of it). The eyes are read over it: open
          for most of it, and open on its first and last frame, where the cut lands.

DEFECT lines mean the take is redone alone or the cut moves (exit 1). FLAG lines are for a look.
"""
import argparse, sys
import checklib as c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('take')
    ap.add_argument('--voice', help='the voice video the model was given')
    ap.add_argument('--line', help='the words the take must say')
    ap.add_argument('--use', help='START-END in seconds, the part the cut uses')
    ap.add_argument('--language', default='en')
    a = ap.parse_args()
    defects, flags = [], []
    dur = c.duration(a.take)
    start, end = (float(x) for x in a.use.split('-')) if a.use else (0.0, dur)

    if a.voice:
        m = c.envelope_match(a.take, a.voice)
        if m is None:
            defects.append('sound: the take has no audio; turn audio generation on, or the lips have no voice to follow')
        elif m < 0.9:
            defects.append(f're-voiced: the take\'s sound follows your read at {m:.2f} (want 0.90 or more), so the model '
                           'made its own voice and the lips follow it; redo this take alone')
        else:
            print(f'voice: the take kept your read ({m:.2f})')

    if a.line:
        try:
            heard = c.transcribe(a.take, a.language)
            print('heard:', ' '.join(w['word'] for w in heard))
            # the clean read, heard the same way: a word the transcriber always mishears (a brand) is then a FLAG,
            # not a redo that would be misheard again
            read = c.transcribe(a.voice, a.language) if a.voice else None
            for kind, said, got, t in c.word_diff(a.line, heard, read):
                (defects if kind == 'DEFECT' else flags).append(f'words at {t:.2f} s: {c.say_diff(said, got, "the take")}'
                                                                + ('' if kind == 'DEFECT' else ' (your read was heard the same way)'))
        except Exception as e:  # noqa: BLE001
            flags.append(f'words not checked: {e}')

    seen = c.eyes(a.take, start, end)
    if seen is None:
        flags.append('eyes not measured (needs macOS): look at a 4 fps strip of the take for shut eyes and the cut frame')
    else:
        known = [(t, s) for t, s in seen if s]
        if len(known) < max(3, len(seen) // 2):
            flags.append('eyes: no face found in most frames; look at the strip')
        else:
            shut = [t for t, s in known if s == 'shut']
            share = len(shut) / len(known)
            print(f'eyes: open in {len(known) - len(shut)} of {len(known)} frames from {start:.2f} to {end:.2f} s')
            if share > 0.35:
                defects.append(f'eyes: shut or lowered in {share:.0%} of {start:.2f}-{end:.2f} s (from {shut[0]:.2f} s), '
                               'so the face reads as asleep, not as the line\'s feeling; redo the take without a blink or a look down')
            elif known[0][1] == 'shut':
                defects.append(f'eyes: shut on the first frame used ({known[0][0]:.2f} s); start the cut where they are open')
            elif known[-1][1] == 'shut':
                open_before = [t for t, s in known if s == 'open' and t < known[-1][0]]
                fix = f'; cut at {open_before[-1]:.2f} s, the last open frame' if open_before else ''
                defects.append(f'eyes: the cut at {end:.2f} s lands as the eyes close{fix}')

    for d in defects:
        print('DEFECT', d)
    for f in flags:
        print('FLAG  ', f)
    print(f'{"FAIL" if defects else "PASS"}: {a.take} ({start:.2f}-{end:.2f} s used)')
    sys.exit(1 if defects else 0)


if __name__ == '__main__':
    main()
