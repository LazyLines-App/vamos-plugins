#!/usr/bin/env python3
"""The checks with a right answer, run on the final before anyone watches it, and again after every fix.
Needs ffmpeg; --script needs `npx hyperframes`; --beats needs tesseract (`brew install tesseract`).

  python3 check-video.py final.mp4 --format narrated-motion-graphics \
      [--voice voice.wav] [--words words.json] [--captions captions.json|.srt] [--caption-text caption.txt]
      [--script script.txt] [--beats beats.json]

Always: size, length, loudness, and frame 0 (the cover the feed shows) is a picture, not a blank or a fade.
--script   the final's audio is transcribed and every word set against the script: a word added, dropped or
           changed by a take or a splice is a DEFECT. A difference the clean read's own transcript (--words) also
           has is the transcriber, not the video, so it is a FLAG.
--captions every spoken word on screen at its midpoint, and no caption ends on a little word that needs the next
           ("scroll past are", "times their") unless a mark follows it.
--beats    beats.json, one entry a line: {"line": "...", "shows": "words that must be on screen"} and optionally
           "at" (the word in the line when it must show; default its last) or "t" (seconds, for a silent video or
           frame 0). The frame at that moment is read (tesseract) for those words. Every beat goes on a sheet,
           <video>-beats.png, with its line under it: look at it full size, and give it to the fresh reviewer.
DEFECT lines must be fixed (exit 1). FLAG lines are for a look, never auto-fixed.
words.json: [{"word": "Your", "start": 0.25, "end": 0.41}, ...] (word times, e.g. from `hyperframes transcribe`).
captions: captions.py's JSON, an .srt, or [{"text": "Your app", "start": 0.2, "end": 0.9}, ...].
"""
import argparse, textwrap, json, math, os, re, shutil, subprocess, sys, tempfile
import checklib as c
from captions import NEEDS_NEXT, ends_phrase, bare, display_words

CAPS = {  # longest the format runs, seconds
    'narrated-motion-graphics': 60, 'voice-over-demo': 50, 'ai-ugc': 50,
    'silent-hook-demo': 52, 'other': 90,
}
SIZE = (1080, 1920)

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe(path):
    out = run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,width,height,r_frame_rate:format=duration',
               '-of', 'json', path])
    if out.returncode:
        sys.exit(f'ffprobe could not read {path}: {out.stderr.strip()}')
    return json.loads(out.stdout)

def loudness(path):
    err = run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-']).stderr
    i = re.findall(r'I:\s+(-?[\d.]+) LUFS', err)
    tp = re.findall(r'Peak:\s+(-?[\d.]+) dBFS', err)
    return (float(i[-1]) if i else None), (float(tp[-1]) if tp else None)

def sound_span(path, floor='-40dB'):
    """First and last moment above the floor, in seconds."""
    err = run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', f'silencedetect=n={floor}:d=0.05', '-f', 'null', '-']).stderr
    starts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', err)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    dur = float(probe(path)['format']['duration'])
    first = ends[0] if starts and starts[0] <= 0.01 and ends else 0.0
    last = starts[-1] if starts and (len(starts) > len(ends) or ends[-1] >= dur - 0.01) else dur
    return first, last, dur

def freezes(path, secs=3.0):
    err = run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-vf', f'freezedetect=n=0.003:d={secs}', '-map', '0:v:0', '-f', 'null', '-']).stderr
    return list(zip(re.findall(r'freeze_start: ([\d.]+)', err), re.findall(r'freeze_duration: ([\d.]+)', err)))

def cues(path):
    text = open(path).read()
    if path.endswith('.json'):
        return [(q['text'], float(q['start']), float(q['end'])) for q in json.loads(text)]
    t = lambda s: sum(float(x) * m for x, m in zip(s.replace(',', '.').split(':'), (3600, 60, 1)))
    out = []
    for block in re.split(r'\n\s*\n', text.strip()):
        m = re.search(r'([\d:,.]+)\s*-->\s*([\d:,.]+)\s*\n(.*)', block, re.S)
        if m:
            out.append((m.group(3), t(m.group(1)), t(m.group(2))))
    return out


def first_frame(video, defects):
    """Frame 0 is the cover in the feed: it must be a picture, not one flat colour or a fade into the first scene."""
    f0 = c.flatness(video, 0.0)
    if f0 is not None and f0 < 4:
        defects.append(f'frame 0: one flat colour (detail {f0:.1f}), a blank or the start of a fade; the feed shows '
                       'frame 0 as the cover, so draw the first beat whole on it')


def beat_times(beats, timed):
    """Each beat's moments: its "t", or the start, middle and end of its "at" word (default the line's last word)."""
    out, pos = [], 0
    for b in beats:
        if 't' in b:
            out.append([float(b['t'])])
            continue
        last, where = c.find_line(b['line'], timed, pos)
        if last is None:
            out.append(None)
            continue
        lt = c.tokens(b['line'])
        k = len(lt) - 1
        if b.get('at'):
            at = c.tokens(b['at'])
            k = next((i for i in range(len(lt)) if lt[i:i + len(at)] == at), k)
        _, start, end, _ = timed[where[k] if where[k] is not None else last]
        out.append([(start + end) / 2, start, end])
        pos = last + 1
    return out


def need(want):
    """Words of a beat's "shows" that must be read: all of one or two, else three in five (OCR misses some)."""
    return want if want <= 2 else math.ceil(0.6 * want)


def caption_words(t, cs, words):
    """Words a caption may be showing at t: the cue on screen then, or, without the captions file, the words said
    in the 2 s before. They can't prove the screen shows a thing, since the caption shows them anyway."""
    if cs is not None:
        return {x for q in cs if q[1] <= t <= q[2] for x in c.screen_words(q[0])}
    return {x for w in words or [] if t - 2.0 <= w['end'] and w['start'] <= t + 0.3 for x in c.screen_words(w['word'])}


def check_beats(video, beats, timed, words, cs, defects, flags):
    """At the moment each line names its thing, is that thing on screen? Read off the frame, and put on a sheet."""
    tmp = tempfile.mkdtemp(prefix='beats-')
    ocr = c.have('tesseract')
    if not ocr and any(b.get('shows') for b in beats):
        defects.append('beats not read: install tesseract (brew install tesseract, or apt install tesseract-ocr) and run again')
    tiles = []
    for n, (b, ts) in enumerate(zip(beats, beat_times(beats, timed))):
        line = b.get('line') or ('the cover' if ts and ts[0] == 0 else 'a silent beat')
        if ts is None:
            defects.append(f'beat {n + 1}: "{line[:50]}" is not heard in the video')
            continue
        pngs = []
        for k, t in enumerate(ts):
            png = os.path.join(tmp, f'b{n:02d}-{k}.png')
            c.frame(video, t, png)
            pngs.append(png)
        shown = 0
        if ocr and b.get('shows'):
            missing, only_caption = [], True
            for k, png in enumerate(pngs):  # the word's middle first, then its start and end
                found, want, missing = c.shows_on_screen(b['shows'], c.ocr_words(png), caption_words(ts[k], cs, words))
                if want:
                    only_caption = False
                if want and found >= need(want):
                    shown = k
                    break
            else:
                if only_caption:
                    flags.append(f'beat {n + 1} at {ts[0]:.2f} s: every word it shows is also in its caption then, so only the '
                                 'beats sheet can tell; look at that tile')
                else:
                    defects.append(f'beat {n + 1} at {ts[0]:.2f} s: the line "{line[:60]}" says it shows "{b["shows"][:60]}", '
                                   f'but the screen then doesn\'t ({", ".join(missing[:6])} not on it); move that moment under the line')
        tiles.append((pngs[shown], f'{ts[shown]:.1f}s  {line}'))
    sheet = os.path.splitext(video)[0] + '-beats.png'
    make_sheet(tiles, sheet, tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f'SHEET {sheet}: each beat at its moment, with its line; look at it full size')


def make_sheet(tiles, out, tmp):
    if not tiles:
        return
    labelled = []
    for k, (png, label) in enumerate(tiles):
        txt = os.path.join(tmp, f'l{k}.txt')
        open(txt, 'w').write('\n'.join(textwrap.wrap(label, 40)[:3]))
        dst = os.path.join(tmp, f't{k:02d}.png')
        base = 'scale=360:640,pad=360:720:0:0:white'
        r = c.run(['ffmpeg', '-v', 'error', '-y', '-i', png, '-vf',
                   f"{base},drawtext=textfile='{txt}':x=8:y=648:fontsize=15:line_spacing=4:fontcolor=black", dst])
        if r.returncode:
            c.run(['ffmpeg', '-v', 'error', '-y', '-i', png, '-vf', base, dst])
        labelled.append(dst)
    cols = min(4, len(labelled))
    rows = (len(labelled) + cols - 1) // cols
    while len(labelled) < rows * cols:
        blank = os.path.join(tmp, f'blank{len(labelled)}.png')
        c.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=white:s=360x720', '-frames:v', '1', blank])
        labelled.append(blank)
    layout = '|'.join(f'{(i % cols) * 360}_{(i // cols) * 720}' for i in range(len(labelled)))
    args = []
    for p in labelled:
        args += ['-i', p]
    c.run(['ffmpeg', '-v', 'error', '-y'] + args + ['-filter_complex', f'xstack=inputs={len(labelled)}:layout={layout}', out]
          if len(labelled) > 1 else ['ffmpeg', '-v', 'error', '-y', '-i', labelled[0], out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--format', default='other', choices=sorted(CAPS))
    ap.add_argument('--voice', help='the voice stem alone (lead-in and tail)')
    ap.add_argument('--words', help='word times of the voice')
    ap.add_argument('--captions', help='the captions as .srt or .json')
    ap.add_argument('--caption-text', help='the post caption, as a text file')
    ap.add_argument('--script', help='the script as said, a text file: the final\'s audio is checked against it')
    ap.add_argument('--heard', help='a transcript of the final (word times), instead of transcribing it here')
    ap.add_argument('--beats', help='beats.json: what each line shows on screen')
    ap.add_argument('--language', default='en')
    ap.add_argument('--size', default='1080x1920')
    a = ap.parse_args()
    defects, flags = [], []

    info = probe(a.video)
    v = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    has_audio = any(s['codec_type'] == 'audio' for s in info['streams'])
    dur = float(info['format']['duration'])
    want = tuple(int(x) for x in a.size.split('x'))
    if not v or (v['width'], v['height']) != want:
        defects.append(f'size: {v and v["width"]}x{v and v["height"]}, want {want[0]}x{want[1]}')
    if dur > CAPS[a.format]:
        defects.append(f'length: {dur:.1f} s, over the {CAPS[a.format]} s cap for {a.format}')

    if has_audio:
        i, tp = loudness(a.video)
        if i is None or abs(i + 14) > 1:
            defects.append(f'loudness: {i} LUFS integrated, want -14 (+/-1)')
        if tp is None or tp > -1.5:
            defects.append(f'true peak: {tp} dBTP, want -1.5 or lower')
    elif a.format not in ('other', 'silent-hook-demo'):
        defects.append('no audio track')

    if a.voice:
        first, last, vdur = sound_span(a.voice)
        if first < 0.2:
            defects.append(f'lead-in: the voice starts at {first:.2f} s; start it about 0.25 s in, or players cut the first word')
        if dur - last < 0.2:
            defects.append(f'tail: the voice ends {dur - last:.2f} s before the file does; leave at least 0.2 s')

    first_frame(a.video, defects)

    words = c.load_words(a.words) if a.words else None
    script = open(a.script).read() if a.script else None
    # the voice's words as the script spells them (a brand name the transcriber mishears), with the voice's times
    spoken = display_words(words, c.said(script)) if words and script else words
    heard = None
    if script and has_audio:
        try:
            heard = c.load_words(a.heard) if a.heard else c.transcribe(a.video, a.language)
            for kind, said, got, t in c.word_diff(script, heard, words):
                line = f'words at {t:.2f} s: {c.say_diff(said, got)}'
                (defects if kind == 'DEFECT' else flags).append(line + ('' if kind == 'DEFECT' else ' (the clean read was heard the same way)'))
        except Exception as e:  # noqa: BLE001
            defects.append(f'words not checked ({str(e)[:160]}): transcribe the final another way (whisper, your TTS\'s speech to text) and pass its word times with --heard')

    cs = cues(a.captions) if a.captions else None
    if cs is not None:
        if spoken:
            missing = []
            for w in spoken:
                mid = (w['start'] + w['end']) / 2
                on = {x for q in cs if q[1] <= mid <= q[2] for x in c.tokens(q[0])}
                if any(x not in on for x in c.tokens(w['word'])):
                    missing.append(f'{w["word"]}@{mid:.2f}')
            if missing:
                defects.append(f'captions: {len(missing)} spoken word(s) not on screen at their midpoint: {", ".join(missing[:12])}')
        bad = [q[0].strip() for q in cs if q[0].split() and bare(q[0].split()[-1]) in NEEDS_NEXT and not ends_phrase(q[0].strip())]
        if bad:
            defects.append(f'captions: {len(bad)} end on a little word that needs the next one: '
                           + ', '.join(f'"{b}"' for b in bad[:8]) + '; break where the voice pauses (scripts/captions.py)')

    if a.beats:
        timed = c.timed_tokens(spoken or heard or [])  # the voice's own times are closer than a transcript's
        check_beats(a.video, json.load(open(a.beats)), timed, spoken or heard, cs, defects, flags)

    if a.caption_text:
        cap = open(a.caption_text).read()
        if re.search(r'https?://|www\.|\b[\w-]+\.(com|ai|io|app|co)\b', cap):
            defects.append('post caption holds a link; links in captions get posts restricted')
        if not re.search(r'#ad\b|[Pp]aid partnership|AI[- ]generated|made with AI|#ai\b', cap):
            flags.append('post caption: no disclosure line; add one when the video holds AI footage or is paid')

    for start, secs in freezes(a.video):
        flags.append(f'frozen: {float(secs):.1f} s from {float(start):.1f} s (fine for a held payoff, not under speech)')

    for d in defects:
        print('DEFECT', d)
    for f in flags:
        print('FLAG  ', f)
    print(f'{"FAIL" if defects else "PASS"}: {a.video} ({dur:.1f} s)')
    sys.exit(1 if defects else 0)

if __name__ == '__main__':
    main()
