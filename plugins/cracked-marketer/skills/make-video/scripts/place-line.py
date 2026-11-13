#!/usr/bin/env python3
"""Find where a take's mouth says its line, so the clean voice is placed there and not where the plan put it.
Needs ffmpeg.

  python3 place-line.py take.mp4 voice.wav [--fit fitted.wav]

The take's own sound (audio generation on) follows its lips, so the clean read is slid along the whole take
and set where the two sounds match best. Prints `vdelay`, the second in the take where the line starts (put it
in shots.json), and the match. Under 0.80 the take re-timed the line inside it (a pause stretched, a word
dragged): --fit splits the read at its pauses, places each part where the take says it at the pace that
matches it (0.8 to 1.25 times), and writes fitted.wav to use as the shot's voice, with vdelay 0. A take whose words
differ from the line is not re-timed: check-take.py --line catches it, and it's redone.

The match is 1.00 for the same sound; 0.80 or more reads as in sync on a phone.
"""
import argparse, array, math, subprocess, sys

HOP = 0.02   # 20 ms
PAD = int(0.2 / HOP)
TEMPOS = [round(0.8 + 0.05 * i, 2) for i in range(10)]   # 0.80 to 1.25: atempo under 1 slows the read down


def envelope(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    a = array.array('h')
    a.frombytes(raw[:len(raw) // 2 * 2])
    n = int(8000 * HOP)
    return [math.sqrt(sum(x * x for x in a[i:i + n]) / n) for i in range(0, len(a) - n + 1, n)]


def corr(x, y):
    m = min(len(x), len(y))
    if m < 10:
        return 0.0
    x, y = x[:m], y[:m]
    mx, my = sum(x) / m, sum(y) / m
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sxy / (sx * sy) if sx and sy else 0.0


def best_lag(take, part, lo=0, hi=None):
    """The frame in the take where part matches best, searched from lo to hi; and the match there."""
    hi = len(take) - len(part) if hi is None else min(hi, len(take) - len(part))
    best = (-1.0, lo)
    for k in range(max(0, lo), max(lo, hi) + 1):
        c = corr(take[k:k + len(part)], part)
        if c > best[0]:
            best = (c, k)
    return best[1], best[0]


def stretch(env, tempo):
    """The envelope as it would be read at tempo times the pace."""
    n = max(1, round(len(env) / tempo))
    return [env[min(len(env) - 1, int(i * tempo))] for i in range(n)]


def parts(env, min_gap=0.15):
    """The read split at its pauses: (start, end) frames of each run of speech."""
    floor = max(env) * 0.1 if env else 0
    out, start, quiet = [], None, 0
    for i, v in enumerate(env + [0] * int(min_gap / HOP + 1)):
        if v > floor:
            if start is None:
                start = i
            quiet = 0
        elif start is not None:
            quiet += 1
            if quiet * HOP >= min_gap:
                out.append((start, i - quiet + 1))
                start, quiet = None, 0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('take')
    ap.add_argument('voice')
    ap.add_argument('--fit', help='write the read fitted to the take here')
    a = ap.parse_args()
    take, voice = envelope(a.take), envelope(a.voice)
    if not take or max(take) == 0:
        sys.exit('the take has no sound: turn audio generation on, or place the line by eye on a 4 fps strip')
    runs = parts(voice)
    if not runs:
        sys.exit('the voice file is silent')
    first, last = runs[0][0], runs[-1][1]
    speech = voice[first:last]
    k, score = best_lag(take, speech)
    vdelay = (k - first) * HOP
    print(f'vdelay {vdelay:.2f}  (the read\'s first word at {k * HOP:.2f} s in the take; match {score:.2f})')
    if score >= 0.8 or not a.fit:
        if score < 0.8:
            print('re-timed: the take says the line at its own pace; run again with --fit fitted.wav')
        elif a.fit:
            print(f'no fit needed, so {a.fit} was not written: use the clean read with vdelay {vdelay:.2f}')
        return
    if len(runs) < 2:
        print('one run of speech with no pause to split at: place it at vdelay and look at the strip, or redo the take')
        return
    # place each part where the take says it, in order, at the pace (0.8 to 1.25 times) that matches it best
    placed, lo = [], max(0, k - int(0.5 / HOP))
    for s, e in runs:
        best = (-1.0, lo, 1.0)
        for tempo in TEMPOS:
            part = stretch(voice[s:e], tempo) + [0] * PAD   # the quiet after it counts, so a part read too short loses
            kk, c = best_lag(take, part, lo, lo + int(2.0 / HOP) + len(part))
            if c > best[0]:
                best = (c, kk, tempo)
        c, kk, tempo = best
        placed.append((s, e, kk, c, tempo))
        lo = kk + round((e - s) / tempo)
    filters = []
    for i, (s, e, kk, c, tempo) in enumerate(placed):
        print(f'part {i + 1}: {s * HOP:.2f}-{e * HOP:.2f} s of the read at {kk * HOP:.2f} s in the take, pace {tempo:.2f}x (match {c:.2f})')
        filters.append(f'[0:a]atrim={s * HOP:.3f}:{e * HOP:.3f},asetpts=PTS-STARTPTS,atempo={tempo:.3f},'
                       f'adelay={int(kk * HOP * 1000)}|{int(kk * HOP * 1000)}[p{i}]')
    filters.append(''.join(f'[p{i}]' for i in range(len(placed))) + f'amix=inputs={len(placed)}:normalize=0[out]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.voice, '-filter_complex', ';'.join(filters), '-map', '[out]',
                    '-ar', '48000', a.fit], check=True)
    fitted = envelope(a.fit)
    print(f'fitted: {a.fit}, match {corr(take, fitted + [0] * max(0, len(take) - len(fitted))):.2f}; '
          'use it as the shot\'s voice with vdelay 0, then look at the strip')


if __name__ == '__main__':
    main()
