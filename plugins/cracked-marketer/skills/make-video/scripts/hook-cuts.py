#!/usr/bin/env python3
"""One demo, many hooks: renders one cut per line and checks each in code. Free; needs ffmpeg and ffprobe.

  python3 hook-cuts.py plan.json [--out cuts] [--only 3] [--font Bold.ttf]

plan.json:
  {"demo": "demo.mp4",              # their screen filmed off the laptop by their phone, ending on the payoff
   "payoff": "payoff.mp4",          # optional: the payoff as its own clip, played after the demo
   "demo_captions": "demo.srt",     # optional: the demo's own captions, one line a shot (the same in every cut)
   "card": "Comment RIP",           # the keyword card, held 2 s at the end
   "song": "song.m4a",              # optional: a song they have the rights to, from frame 0 (or add one in the app)
   "cuts": [{"line": "...", "opening": "openings/tired.mp4",
             "source": "https://www.instagram.com/p/...", "from": "@creator", "multiple": 181.2}, ...]}

Each cut is the opening with its line on screen from frame 0, a hard cut to the same demo, the payoff and the card.
Everything after the opening is identical across cuts, so the hook is the one thing that changes.
Writes <out>/NN-<line>.mp4 per cut and <out>/manifest.json. Prints PASS or DEFECT per cut (exit 1 on any DEFECT),
then the reply's table of every line in the plan with the hook it came from, and the next step.
"""
import argparse, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30
CAP = 52            # the silent hook demo's longest winner, seconds
CARD_S = 2.0
SIZE, LEADING = 68, 84      # caption px; line height
TOP = 330                   # caption block top: under Instagram's top 220 px
MAX_CHARS = 22              # per caption row at 68 px inside the 90 px / 130 px side margins
FONTS = ['/System/Library/Fonts/Supplemental/Arial Bold.ttf',
         '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
         '/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf',
         'C:/Windows/Fonts/arialbd.ttf']
EMOJI = re.compile('[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u200D]')

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('check_video', os.path.join(here, 'check-video.py'))
cv = importlib.util.module_from_spec(spec); spec.loader.exec_module(cv)

def ff(*args):
    p = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *args], capture_output=True, text=True)
    if p.returncode:
        sys.exit(f'ffmpeg failed: {p.stderr.strip()[-600:]}')

def duration(path):
    return float(cv.probe(path)['format']['duration'])

def frames(path):
    out = cv.run(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                  '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', path]).stdout
    return int(out.strip().split(',')[0])

def slug(line, n):
    words = re.sub(r"[^\w\s-]", '', EMOJI.sub('', line).lower()).split()
    return f'{n:02d}-' + '-'.join(words[:7])[:60]

def wrap(text):
    rows, row = [], ''
    for w in text.split():
        if row and len(row) + 1 + len(w) > MAX_CHARS:
            rows.append(row); row = w
        else:
            row = f'{row} {w}'.strip()
    return rows + ([row] if row else [])

def drawtext(text, font, tmp, enable=None, top=TOP, size=SIZE):
    """One centred drawtext per row; text goes through files so quotes and colons need no escaping,
    and expansion=none keeps a % (as in "90% of founders") from swallowing the row."""
    out = []
    for i, row in enumerate(wrap(text)):
        f = tempfile.NamedTemporaryFile('w', suffix='.txt', dir=tmp, delete=False)
        f.write(row); f.close()
        opt = (f"drawtext=fontfile='{font}':textfile='{f.name}':fontsize={size}:fontcolor=white"
               f":expansion=none:borderw=5:bordercolor=black:x=(w-text_w)/2:y={top + i * (size + 16)}")
        out.append(opt + (f":enable='{enable}'" if enable else ''))
    return out

NORM = f'scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},format=yuv420p,setsar=1'
ENC = ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS)]

def gray(path, first, count, w=270, h=480, crop=None):
    """Frames [first, first+count) as small grey byte strings."""
    vf = f"select='between(n,{first},{first + count - 1})'," + (f'crop={crop},' if crop else '') + f'scale={w}:{h},format=gray'
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', vf, '-vsync', '0', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    n = w * h
    return [raw[i:i + n] for i in range(0, len(raw) - n + 1, n)]

def diff(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / max(len(a), 1)

def check(cut, opening_norm, open_frames, rows, expected):
    """The checks with a right answer: size, length, the line on screen from frame 0, the hard cut, loudness."""
    defects, notes = [], []
    info = cv.probe(cut)
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    if (v['width'], v['height']) != (W, H):
        defects.append(f'size {v["width"]}x{v["height"]}, want {W}x{H}')
    dur = float(info['format']['duration'])
    if dur > CAP:
        defects.append(f'length {dur:.1f} s, over the {CAP} s cap')
    if abs(dur - expected) > 0.15:
        defects.append(f'length {dur:.2f} s, want {expected:.2f} s (opening + the demo + the card)')
    notes.append(f'{dur:.1f} s')

    for n, when in ((0, 'frame 0'), (open_frames - 1, 'the opening\'s last frame')):
        for r in range(rows):       # each row of the line, so a row that failed to draw is caught
            band = f'{W - 180}:{SIZE + 16}:90:{TOP + r * (SIZE + 16) - 8}'
            a = gray(cut, n, 1, 430, 42, band); b = gray(opening_norm, n, 1, 430, 42, band)
            if not a or not b or diff(a[0], b[0]) < 4:
                defects.append(f'row {r + 1} of the line is not on screen at {when}')
    if not defects:
        notes.append('line on screen from frame 0')

    f = gray(cut, open_frames - 2, 4)
    if len(f) < 4:
        defects.append('could not read the frames around the cut')
    else:
        before, at, after = diff(f[0], f[1]), diff(f[1], f[2]), diff(f[2], f[3])
        if at < 10 or at < 3 * max(before, after, 1):
            defects.append(f'no hard cut at {open_frames / FPS:.2f} s (change {at:.1f} against {before:.1f} and {after:.1f} '
                           'either side): a fade or a held frame')
        else:
            notes.append(f'hard cut at {open_frames / FPS:.2f} s')

    if any(s['codec_type'] == 'audio' for s in info['streams']):
        i, tp = cv.loudness(cut)
        loud_ok = i is not None and abs(i + 14) <= 1
        peak_ok = tp is not None and tp <= -1.5
        if not loud_ok:
            defects.append(f'loudness {i} LUFS, want -14 (+/-1)')
        if not peak_ok:
            defects.append(f'true peak {tp} dBTP, want -1.5 or lower')
        if loud_ok and peak_ok:
            notes.append(f'{i:.1f} LUFS')
    return defects, notes

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plan')
    ap.add_argument('--out', default='cuts')
    ap.add_argument('--only', type=int, help='render the first N cuts')
    ap.add_argument('--font', help='a bold .ttf/.otf for the line (their brand font, or TikTok Sans / Inter from Google Fonts)')
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    base = os.path.dirname(os.path.abspath(a.plan))
    p = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    font = a.font or next((f for f in FONTS if os.path.exists(f)), None)
    if not font:
        sys.exit('no bold font found: pass --font with a .ttf (TikTok Sans or Inter from Google Fonts)')
    cuts = plan['cuts'][:a.only] if a.only else plan['cuts']
    os.makedirs(a.out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix='hook-cuts-')
    try:
        # The body, rendered once: the demo (and payoff) with its own captions, then the keyword card.
        segs = [p(plan['demo'])] + ([p(plan['payoff'])] if plan.get('payoff') else [])
        inputs, chain = [], []
        for i, s in enumerate(segs):
            inputs += ['-i', s]
            chain.append(f'[{i}:v]{NORM}[s{i}]')
        n = len(segs)
        inputs += ['-f', 'lavfi', '-i', f'color=c=0x111111:s={W}x{H}:r={FPS}:d={CARD_S}']
        chain.append(f'[{n}:v]' + ','.join(drawtext(plan.get('card', ''), font, tmp, top=H // 2 - 120, size=110) or ['null'])
                     + f',format=yuv420p,setsar=1[s{n}]')
        caps = []
        for text, start, end in (cv.cues(p(plan['demo_captions'])) if plan.get('demo_captions') else []):
            caps += drawtext(' '.join(text.split()), font, tmp, enable=f'between(t,{start},{end})', top=1250)
        chain.append(''.join(f'[s{i}]' for i in range(n + 1)) + f'concat=n={n + 1}:v=1:a=0'
                     + (',' + ','.join(caps) if caps else '') + '[v]')
        body = os.path.join(tmp, 'body.mp4')
        ff(*inputs, '-filter_complex', ';'.join(chain), '-map', '[v]', *ENC, body)
        body_s = duration(body)

        manifest, failed = [], 0
        for k, c in enumerate(cuts, 1):
            line, flags = c['line'], []
            if EMOJI.search(line):
                flags.append('emoji left out of the burned line; add them in the app\'s text tool if you want them')
            text = ' '.join(EMOJI.sub('', line).split())
            if len(text.split()) > 13:
                flags.append(f'{len(text.split())} words: the longest card among 1,117 winners was 13')
            opening = os.path.join(tmp, f'open-{k}.mp4')
            ff('-i', p(c['opening']), '-vf', NORM, '-an', *ENC, opening)
            open_s, open_n = duration(opening), frames(opening)
            if not 2.0 <= open_s <= 4.5:
                flags.append(f'opening {open_s:.1f} s; winners hold about 3.5 s')
            rows = len(wrap(text))
            ins = ['-i', opening, '-i', body]
            fc = f'[0:v]{",".join(drawtext(text, font, tmp))}[o];[o][1:v]concat=n=2:v=1:a=0[v]'
            total = open_s + body_s
            amap = []
            if plan.get('song'):
                ins += ['-i', p(plan['song'])]
                fc += (f';[2:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(total - 0.6, 0):.3f}:d=0.6,'
                       'loudnorm=I=-14:TP=-2:LRA=11,aresample=48000[a]')
                amap = ['-map', '[a]', '-c:a', 'aac', '-b:a', '192k']
            out = os.path.join(a.out, slug(line, k) + '.mp4')
            ff(*ins, '-filter_complex', fc, '-map', '[v]', *amap, *ENC, '-t', f'{total:.3f}', '-movflags', '+faststart', out)
            defects, notes = check(out, opening, open_n, rows, total)
            failed += bool(defects)
            print(('DEFECT ' if defects else 'PASS   ') + out + ': ' + '; '.join(defects or notes))
            for f in flags:
                print('FLAG     ' + f)
            manifest.append({'file': out, 'line': line, 'opening': c['opening'], 'source': c.get('source'),
                             'multiple': c.get('multiple'), 'seconds': round(total, 2),
                             'checks': 'DEFECT: ' + '; '.join(defects) if defects else 'PASS', 'flags': flags,
                             'board': 'test: same demo, the hook changes'})
        json.dump(manifest, open(os.path.join(a.out, 'manifest.json'), 'w'), indent=1, ensure_ascii=False)
        print(f'{"FAIL" if failed else "PASS"}: {len(cuts) - failed} of {len(cuts)} cuts; manifest at {a.out}/manifest.json')
        # The table for the reply: every line in the plan, rendered or not, with the hook it came from.
        print('\nTABLE (paste in the reply; the same demo in every cut, only the opening and its line change)')
        print('| # | Line | Opening | From | Multiple | Cut |\n|---|---|---|---|---|---|')
        for k, c in enumerate(plan['cuts'], 1):
            src = f"[{c.get('from') or 'link'}]({c['source']})" if c.get('source') else 'none: find one'
            mult = f"{c['multiple']}x" if c.get('multiple') is not None else '-'
            done = manifest[k - 1]['checks'] if k <= len(manifest) else 'not rendered yet'
            print(f"| {k} | {c['line']} | {os.path.splitext(os.path.basename(c['opening']))[0]} | {src} | {mult} | {done} |")
        print('NEXT: content-log, once the posts are 7 days old, puts each cut\'s multiple in its Hooks-tab row '
              '(a cut already past the usual shows as "so far" sooner; Result "test: same demo, the hook changes"); '
              'the next ten lines start from the winner.')
        sys.exit(1 if failed else 0)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

if __name__ == '__main__':
    main()
