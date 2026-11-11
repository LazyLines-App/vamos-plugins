#!/usr/bin/env python3
"""The checks with a right answer, run on the final before anyone watches it. Needs ffmpeg and ffprobe.

  python3 check-video.py final.mp4 --format narrated-motion-graphics \
      [--voice voice.wav] [--words words.json] [--captions captions.srt|.json] [--caption-text caption.txt]

DEFECT lines must be fixed (exit 1). FLAG lines are for a look, never auto-fixed.
words.json: [{"word": "Your", "start": 0.25, "end": 0.41}, ...] (word times, e.g. from Whisper).
captions: an .srt, or [{"text": "Your app", "start": 0.2, "end": 0.9}, ...].
"""
import argparse, json, re, subprocess, sys

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
        return [(c['text'], float(c['start']), float(c['end'])) for c in json.loads(text)]
    t = lambda s: sum(float(x) * m for x, m in zip(s.replace(',', '.').split(':'), (3600, 60, 1)))
    out = []
    for block in re.split(r'\n\s*\n', text.strip()):
        m = re.search(r'([\d:,.]+)\s*-->\s*([\d:,.]+)\s*\n(.*)', block, re.S)
        if m:
            out.append((m.group(3), t(m.group(1)), t(m.group(2))))
    return out

norm = lambda s: re.sub(r"[^\w']", '', s.lower())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('video')
    ap.add_argument('--format', default='other', choices=sorted(CAPS))
    ap.add_argument('--voice', help='the voice stem alone (lead-in and tail)')
    ap.add_argument('--words', help='word times of the voice')
    ap.add_argument('--captions', help='the captions as .srt or .json')
    ap.add_argument('--caption-text', help='the post caption, as a text file')
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

    if a.words and a.captions:
        words, cs = json.load(open(a.words)), cues(a.captions)
        missing = []
        for w in words:
            mid = (float(w['start']) + float(w['end'])) / 2
            on = {norm(x) for c in cs if c[1] <= mid <= c[2] for x in c[0].split()}
            if norm(w['word']) and norm(w['word']) not in on:
                missing.append(f'{w["word"]}@{mid:.2f}')
        if missing:
            defects.append(f'captions: {len(missing)} spoken word(s) not on screen at their midpoint: {", ".join(missing[:12])}')

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
