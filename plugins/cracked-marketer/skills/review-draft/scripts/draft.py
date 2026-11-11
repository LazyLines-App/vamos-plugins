#!/usr/bin/env python3
"""Read a creator's draft video into what a review can look at: frames and a transcript.

    python3 draft.py VIDEO [--out DIR] [--captions FILE] [--model PATH] [--every 2]

Needs ffmpeg and ffprobe. Writes into DIR (default: draft/ beside where you run it):
  probe.json         length, width, height, 9:16 or not, whether it has sound
  sheet-01.jpg ...   frames in sheets of 8 (4 across, 2 down, left to right), each stamped
                     with its time: every 0.5 s to 3 s, then every --every seconds to the end
  transcript.srt     what's said, with times, from the first of:
                     1. --captions, or a .srt or .vtt beside the video with the same name
                        (the creator's captions file, e.g. CapCut's export);
                     2. whisper.cpp (whisper-cli), free and local, with a ggml model from --model,
                        $WHISPER_MODEL, ~/.cache/whisper.cpp or ~/whisper.cpp/models;
                     3. openai-whisper's `whisper` command.
                     With none of them it says so and how to get one; read the burned-in
                     captions off the sheets meanwhile.
Prints each sheet with its times, and where the transcript came from. Standard library only.
"""
import argparse, glob, json, os, shutil, subprocess, sys

MAX_FRAMES = 48


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(video):
    p = run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', video])
    if p.returncode:
        sys.exit(f"ffprobe couldn't read {video}: {p.stderr.strip()[:300]}")
    d = json.loads(p.stdout)
    v = next((s for s in d.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not v:
        sys.exit(f'{video} has no video stream')
    w, h = int(v.get('width') or 0), int(v.get('height') or 0)
    rot = 0
    for sd in v.get('side_data_list') or []:
        if 'rotation' in sd:
            rot = int(float(sd['rotation']))
    rot = int((v.get('tags') or {}).get('rotate', rot) or 0)
    if abs(rot) % 180 == 90:
        w, h = h, w
    dur = float((d.get('format') or {}).get('duration') or v.get('duration') or 0)
    audio = any(s.get('codec_type') == 'audio' for s in d.get('streams', []))
    vertical = bool(w and h and abs(w / h - 9 / 16) < 0.02)
    return {'file': os.path.basename(video), 'seconds': round(dur, 2), 'width': w, 'height': h,
            'nine_by_sixteen': vertical, 'full_hd_vertical': (w, h) == (1080, 1920), 'sound': audio}


def times(dur, every):
    ts = [x / 2 for x in range(0, 7) if x / 2 < dur]
    t = 3.0 + every
    while t < dur - 0.05:
        ts.append(round(t, 2))
        t += every
    if dur > 3.2 and dur - ts[-1] > 0.6:
        ts.append(round(max(dur - 0.3, 0), 2))  # the last frame: the ending
    while len(ts) > MAX_FRAMES:  # a long video: thin the frames after 3 s
        head, tail = ts[:7], ts[7:]
        ts = head + tail[::2]
    return ts


def frame(video, t, path, label):
    base = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', video, '-frames:v', '1']
    stamp = (f",drawtext=text='{label}':x=10:y=10:fontsize=30:fontcolor=white:box=1:boxcolor=black@0.7:boxborderw=6")
    for vf in (f'scale=360:-2{stamp}', 'scale=360:-2'):  # without a font library, no stamp
        if run(base + ['-vf', vf, '-q:v', '4', path]).returncode == 0 and os.path.exists(path):
            return vf != 'scale=360:-2'
    return None


def sheets(video, ts, out):
    tmp = os.path.join(out, '_frames')
    os.makedirs(tmp, exist_ok=True)
    stamped, n = True, 0
    for i, t in enumerate(ts):
        got = frame(video, t, os.path.join(tmp, f'f{i:03d}.jpg'), f'{t:.1f} s')
        if got is None:
            sys.exit(f"ffmpeg couldn't take a frame at {t:.1f} s")
        stamped = stamped and got
        n += 1
    for old in glob.glob(os.path.join(out, 'sheet-*.jpg')):
        os.remove(old)
    p = run(['ffmpeg', '-v', 'error', '-y', '-framerate', '1', '-i', os.path.join(tmp, 'f%03d.jpg'),
             '-vf', 'tile=4x2:padding=6:margin=6:color=white', '-q:v', '3', os.path.join(out, 'sheet-%02d.jpg')])
    if p.returncode:
        sys.exit(f"ffmpeg couldn't make the sheets: {p.stderr.strip()[:300]}")
    shutil.rmtree(tmp)
    return [ts[i:i + 8] for i in range(0, n, 8)], stamped


def find_model(arg):
    picks = [arg, os.environ.get('WHISPER_MODEL')]
    for d in ('~/.cache/whisper.cpp', '~/whisper.cpp/models', '~/.local/share/whisper.cpp', './models'):
        found = sorted(glob.glob(os.path.join(os.path.expanduser(d), 'ggml-*.bin')))
        picks += [f for f in found if '.en' in f] + found
    return next((p for p in picks if p and os.path.exists(p)), None)


def transcript(video, out, captions, model_arg, sound):
    dest = os.path.join(out, 'transcript.srt')
    stem = os.path.splitext(video)[0]
    side = [captions] if captions else [stem + '.srt', stem + '.vtt']
    for c in side:
        if c and os.path.exists(c):
            shutil.copy(c, dest)
            return f'the captions file {os.path.basename(c)}'
    if captions:
        sys.exit(f'no captions file at {captions}')
    if not sound:
        return None
    cli = shutil.which('whisper-cli') or shutil.which('whisper-cpp')
    model = find_model(model_arg)
    if cli and model:
        wav = os.path.join(out, 'audio.wav')
        if run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', wav]).returncode == 0:
            p = run([cli, '-m', model, '-f', wav, '-osrt', '-of', os.path.join(out, 'transcript'), '-np'])
            os.remove(wav)
            if p.returncode == 0 and os.path.exists(dest):
                return f'whisper.cpp ({os.path.basename(model)}), on this machine'
    if shutil.which('whisper'):
        p = run(['whisper', video, '--model', 'base.en', '--output_format', 'srt', '--output_dir', out, '--fp16', 'False'])
        made = os.path.join(out, os.path.splitext(os.path.basename(video))[0] + '.srt')
        if p.returncode == 0 and os.path.exists(made):
            os.replace(made, dest)
            return 'openai-whisper (base.en), on this machine'
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('video')
    ap.add_argument('--out', default='draft')
    ap.add_argument('--captions')
    ap.add_argument('--model')
    ap.add_argument('--every', type=float, default=2.0)
    a = ap.parse_args()
    if not (shutil.which('ffmpeg') and shutil.which('ffprobe')):
        sys.exit('needs ffmpeg and ffprobe (macOS: brew install ffmpeg). Without them, ask for the transcript and three screenshots instead.')
    if not os.path.exists(a.video):
        sys.exit(f'no file at {a.video}')
    os.makedirs(a.out, exist_ok=True)
    info = probe(a.video)
    json.dump(info, open(os.path.join(a.out, 'probe.json'), 'w'), indent=1)
    shape = '9:16' if info['nine_by_sixteen'] else 'not 9:16'
    print(f"{info['file']}: {info['seconds']} s, {info['width']} x {info['height']} ({shape}), "
          f"{'with sound' if info['sound'] else 'NO SOUND'}")
    groups, stamped = sheets(a.video, times(info['seconds'], a.every), a.out)
    for i, g in enumerate(groups, 1):
        print(f"{os.path.join(a.out, f'sheet-{i:02d}.jpg')}: " + ', '.join(f'{t:.1f} s' for t in g))
    if not stamped:
        print('  (no font library for the time stamps: the times above run left to right, top row first)')
    src = transcript(a.video, a.out, a.captions, a.model, info['sound'])
    if src:
        print(f"{os.path.join(a.out, 'transcript.srt')}: from {src}")
    elif not info['sound']:
        print('no transcript: the file has no sound')
    else:
        print('no transcript: no captions file beside the video and no local transcriber.\n'
              '  Free and local: brew install whisper-cpp, then\n'
              '  curl -L --create-dirs -o ~/.cache/whisper.cpp/ggml-base.en.bin '
              'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin  (142 MB), and run this again.\n'
              '  Or pass the creator\'s captions file with --captions. Meanwhile, read the burned-in captions off the sheets.')


if __name__ == '__main__':
    main()
