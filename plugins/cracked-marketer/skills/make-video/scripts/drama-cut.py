#!/usr/bin/env python3
"""Cut a drama from its takes, in code. Needs ffmpeg (with libass for the subtitles).

  python3 drama-cut.py shots.json final.mp4

shots.json (paths relative to it):
  {"song": "song.mp3", "song_drop": 41.2, "drop_on": "turn", "drop_offset": 0.3, "song_gain": 0.35,
   "buzz": true, "subs": {"font": "Arial", "size": 46},
   "shots": [{"name": "bar", "src": "takes/bar.mp4", "in": 0.0, "dur": 2.85,
              "voice": "voices/dad-1.wav", "vdelay": 0.3, "line": "Your brother just bought a house."},
             {"name": "turn", "src": "build/turn.mp4", "in": 0, "dur": 2.0, "turn": true}, ...]}

- Each shot is the take from `in` for `dur` seconds, snapped to whole frames at 24 fps (a length that rounds
  off frames drifts every later line off its mouth), scaled and cropped to 1080x1920, joined with hard cuts.
- A shot's `voice` is its character's clean read, placed `vdelay` seconds into the take (place-line.py's
  number; 0 for a --fit file). The takes' own sound is dropped, so each character keeps one voice.
- Each line is a small subtitle while its voice sounds (yellow, black edge, lower middle; `subs` changes the font,
  size, colour, outline and margin, in the video's pixels); final.srt holds the same cues for check-video.py.
- The song runs under everything, its drop (`song_drop`, seconds into the track) landing on the start of the
  shot `drop_on` names (else the shot marked "turn": true) plus `drop_offset`, ducked under each line; `pre_drop_boost` lifts a quiet intro before the drop (4.2 evened
  one out); `buzz` adds a phone buzz on the drop. Mastered to -14 LUFS.

Prints the length, the shots, where the turn lands (a FLAG outside 40 to 70% of the runtime), and a FLAG for a
last line over six words. Writes final.timeline.json.
"""
import json, os, re, shutil, subprocess, sys, tempfile

FPS, W, H = 24, 1080, 1920


def run(*a):
    return subprocess.run(a, capture_output=True, text=True)


def span(path):
    """First and last moment the file sounds, in seconds."""
    err = run('ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'silencedetect=n=-40dB:d=0.05', '-f', 'null', '-').stderr
    dur = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path).stdout.strip())
    starts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', err)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    first = ends[0] if starts and starts[0] <= 0.01 and ends else 0.0
    last = starts[-1] if starts and (len(starts) > len(ends) or ends[-1] >= dur - 0.01) else dur
    return first, last


def ts(x):
    h, m = int(x // 3600), int(x % 3600 // 60)
    return f'{h:02d}:{m:02d}:{x % 60:06.3f}'.replace('.', ',')


def length(path):
    r = run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path)
    try:
        return float(r.stdout.strip())
    except ValueError:
        sys.exit(f'{path}: not a video ffprobe can read')


def ats(x):
    return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'


def main():
    cfg_path, out = sys.argv[1], sys.argv[2]
    cfg = json.load(open(cfg_path))
    root = os.path.dirname(os.path.abspath(cfg_path))
    at = lambda p: p if os.path.isabs(p) else os.path.join(root, p)
    shots = cfg['shots']
    t, clips, voices, cues, turn_at, short = 0.0, [], [], [], None, []
    for s in shots:
        nf = round(s['dur'] * FPS)
        src = at(s['src'])
        if not os.path.exists(src):
            sys.exit(f'{s["name"]}: {src} is not there')
        have = length(src) - s.get('in', 0.0)
        if have < nf / FPS - 0.05:
            short.append(f'{s["name"]} runs {have:.2f} s from its in, {nf / FPS:.2f} s wanted: its last frame is held')
        clips.append((src, s.get('in', 0.0), nf))
        if s.get('turn'):
            turn_at = t
        if s.get('voice'):
            v = at(s['voice'])
            start = t + s.get('vdelay', 0.0) - s.get('in', 0.0)
            first, last = span(v)
            voices.append((v, start, s.get('vgain', 1.0)))
            if s.get('line'):
                cues.append((start + first - 0.05, start + last + 0.25, s['line']))
        s['_start'] = round(t, 3)
        t += nf / FPS
    total = t

    inputs, fc = [], []
    for i, (src, ss, nf) in enumerate(clips):
        inputs += ['-ss', str(ss), '-t', f'{nf / FPS + 0.2:.3f}', '-i', src]
        fc.append(f'[{i}:v]fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,'
                  f'tpad=stop_mode=clone:stop=-1,trim=end_frame={nf},setpts=PTS-STARTPTS[v{i}]')
    fc.append(''.join(f'[v{i}]' for i in range(len(clips))) + f'concat=n={len(clips)}:v=1:a=0[vc]')

    srt = os.path.splitext(out)[0] + '.srt'
    with open(srt, 'w') as f:
        for n, (a, b, line) in enumerate(cues, 1):
            f.write(f'{n}\n{ts(max(0, a))} --> {ts(min(total, b))}\n{line}\n\n')
    # the burned-in lines: an .ass at the video's own size, so the style's sizes and margins are in its pixels
    st = {'font': 'Arial', 'size': 46, 'colour': '&H0050E6FF', 'bold': -1, 'outline': 3, 'marginv': 490, **cfg.get('subs', {})}
    work = tempfile.mkdtemp(prefix='drama-cut-')   # a plain path, so ffmpeg's filter needs no quoting
    ass = os.path.join(work, 'subs.ass')
    with open(ass, 'w') as f:
        f.write('[Script Info]\nScriptType: v4.00+\nPlayResX: %d\nPlayResY: %d\n\n[V4+ Styles]\n' % (W, H)
                + 'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, '
                'Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, '
                'MarginV, Encoding\n'
                f"Style: Sub,{st['font']},{st['size']},{st['colour']},&H00FFFFFF,&H00000000,&H64000000,{st['bold']},0,0,0,100,100,0,0,1,"
                f"{st['outline']},1,2,90,90,{st['marginv']},1\n\n[Events]\n"
                'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
                + ''.join(f'Dialogue: 0,{ats(max(0, a))},{ats(min(total, b))},Sub,,0,0,0,,{line}\n' for a, b, line in cues))
    shutil.copy(ass, os.path.splitext(out)[0] + '.ass')
    has_ass = 'libass' in run('ffmpeg', '-hide_banner', '-filters').stdout
    fc.append(f"[vc]ass='{ass}'[vout]" if has_ass and cues else '[vc]null[vout]')

    ai, labels = len(clips), []
    for k, (path, start, g) in enumerate(voices):
        inputs += ['-i', path]
        d = max(0, int(start * 1000))
        fc.append(f'[{ai}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={g},adelay={d}|{d},apad=whole_dur={total}[d{k}]')
        labels.append(f'[d{k}]')
        ai += 1
    mix = []
    if labels:
        fc.append(''.join(labels) + f'amix=inputs={len(labels)}:normalize=0,asplit=2[dlg][sc]')
        mix.append('[dlg]')
    # the drop lands on drop_on's shot (by name), else on the shot marked "turn": true
    drop = None
    on = next((s for s in shots if s['name'] == cfg.get('drop_on')), None) or next((s for s in shots if s.get('turn')), None)
    if cfg.get('drop_on') and on is None:
        sys.exit(f'drop_on names "{cfg["drop_on"]}", and no shot has that name or "turn": true')
    if on is not None and (cfg.get('drop_on') or 'song_drop' in cfg):
        drop = on['_start'] + cfg.get('drop_offset', 0.0)
    if cfg.get('song'):
        lead = 0.0   # seconds of quiet before the song, when its drop comes sooner in the track than the turn in the cut
        song_start = cfg.get('song_start', 0.0)
        if drop is not None and 'song_drop' in cfg:
            song_start = cfg['song_drop'] - drop
            lead, song_start = max(0.0, -song_start), max(0.0, song_start)
        inputs += ['-ss', f'{song_start:.3f}', '-t', f'{total + 1:.3f}', '-i', at(cfg['song'])]
        boost = f"volume='if(lt(t,{drop - 0.05:.3f}),{cfg['pre_drop_boost']},1)':eval=frame," if drop is not None and cfg.get('pre_drop_boost') else ''
        delay = f'adelay={int(lead * 1000)}|{int(lead * 1000)},' if lead else ''
        fc.append(f"[{ai}:a]aformat=sample_rates=48000:channel_layouts=stereo,volume={cfg.get('song_gain', 0.35)},{delay}{boost}"
                  f"afade=t=out:st={max(0, total - 0.6):.3f}:d=0.6[mus]")
        ai += 1
        if labels:
            fc.append('[mus][sc]sidechaincompress=threshold=0.02:ratio=4:attack=20:release=350[musd]')
            mix.append('[musd]')
        else:
            mix.append('[mus]')
    if cfg.get('buzz') and drop is not None:
        d = int(drop * 1000)
        fc.append(f"aevalsrc='0.22*sin(2*PI*165*t)*gt(sin(2*PI*28*t),0)*(lt(t,0.22)+gt(t,0.36)*lt(t,0.58))':s=48000:d=0.7,"
                  f"lowpass=f=900,aformat=channel_layouts=stereo,adelay={d}|{d},apad=whole_dur={total}[buzz]")
        mix.append('[buzz]')
    if not mix:
        sys.exit('no voices and no song: a drama needs its lines or a song under it')
    fc.append(''.join(mix) + f'amix=inputs={len(mix)}:normalize=0,atrim=0:{total:.3f}[aout]')

    tmp = os.path.join(work, 'pass1.mov')
    r = run('ffmpeg', '-v', 'error', '-y', *inputs, '-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', '[aout]',
            '-c:v', 'libx264', '-crf', '16', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS),
            '-c:a', 'pcm_s16le', '-t', f'{total:.3f}', tmp)
    if r.returncode:
        shutil.rmtree(work, ignore_errors=True)
        sys.exit(r.stderr[-2000:])
    # two-pass loudness, so the file lands on -14 LUFS and -1.5 dBTP rather than near them
    m = run('ffmpeg', '-hide_banner', '-nostats', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json',
            '-f', 'null', '-').stderr
    j = json.loads(m[m.rindex('{'):m.rindex('}') + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    r = run('ffmpeg', '-v', 'error', '-y', '-i', tmp, '-c:v', 'copy', '-af', ln + ',aresample=48000', '-c:a', 'aac',
            '-b:a', '192k', '-movflags', '+faststart', out)
    shutil.rmtree(work, ignore_errors=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])

    for s in shots:
        s['start'] = s.pop('_start')
    json.dump({'total': round(total, 3), 'shots': shots, 'subs': cues, 'turn_at': turn_at},
              open(os.path.splitext(out)[0] + '.timeline.json', 'w'), indent=1)
    print(f'{out}: {total:.2f} s, {len(clips)} shots, {len(clips) - 1} cuts, {len(cues)} lines; subtitles in {srt}'
          + ('' if has_ass else ' (this ffmpeg has no libass, so they are not burned in: burn them or add them at upload)'))
    for line in short:
        print('FLAG  ', line)
    if turn_at is None:
        print('FLAG   no shot is marked "turn": true, so where the turn lands is not checked')
    else:
        share = turn_at / total
        print(f'turn at {turn_at:.2f} s, {share:.0%} of the runtime')
        if not 0.4 <= share <= 0.7:
            print(f'FLAG   the turn lands at {share:.0%}; winners turn at about half way (45 to 65%)')
    if cues:
        words = len(cues[-1][2].split())
        if words > 6:
            print(f'FLAG   the last line is {words} words; the hero\'s last line works at two to six')
    if not 15 <= total <= 30:
        print(f'FLAG   {total:.1f} s; dramas that won ran 15 to 30 s')


if __name__ == '__main__':
    main()
