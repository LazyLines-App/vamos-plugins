"""Shared code for the make-video checks: words, transcripts, frames, on-screen text and eyes. Needs ffmpeg.

Transcripts come from `npx hyperframes transcribe` (whisper, run on this machine). On-screen text comes from
tesseract (`brew install tesseract`). Eyes come from Apple Vision through `eyes.swift` (macOS). A check whose tool
is missing says so as a FLAG and the rest still run.
"""
import array, difflib, json, math, os, re, shutil, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def duration(path):
    out = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]).stdout.strip()
    return float(out or 0)


# ---- words -------------------------------------------------------------------------------------------------

ONES = ('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen '
        'seventeen eighteen nineteen').split()
TENS = 'zero ten twenty thirty forty fifty sixty seventy eighty ninety'.split()


def say_number(n):
    if n < 20:
        return [ONES[n]]
    if n < 100:
        return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [ONES[n // 100], 'hundred'] + (say_number(n % 100) if n % 100 else [])
    if n < 1000000:
        return say_number(n // 1000) + ['thousand'] + (say_number(n % 1000) if n % 1000 else [])
    return [str(n)]


def tokens(text):
    """Words as said, lower case, numbers spelled out ("20" and "twenty" are the same word)."""
    out = []
    for raw in re.split(r"[\s\-–—/]+", text.replace('’', "'")):
        w = raw.lower().strip(".,!?;:\"()[]{}*_~`“”‘")
        w = w.strip("'")
        if not w:
            continue
        m = re.fullmatch(r'\$?(\d[\d,]*)(?:\.(\d+))?(%|x|×)?', w)
        if m:
            n = int(m.group(1).replace(',', ''))
            out += say_number(n)
            if m.group(2):
                out += ['point'] + [ONES[int(d)] for d in m.group(2)]
            out += {'%': ['percent'], 'x': ['times'], '×': ['times']}.get(m.group(3), [])  # "30x" is said "thirty times"
            continue
        w = re.sub(r"[^\w']", '', w)
        if w:
            out.append(w)
    return out


def load_words(path):
    """Timed words from a JSON list of {word|text, start, end} (Whisper, HyperFrames transcribe, ElevenLabs)."""
    data = json.load(open(path))
    if isinstance(data, dict):
        data = data.get('words') or data.get('transcription')
    if not isinstance(data, list) or (data and not all(isinstance(w, dict) and 'start' in w and 'end' in w for w in data)):
        raise ValueError(f'{path}: want a JSON list of {{"word", "start", "end"}} word times')
    out = []
    for w in data:
        text = w.get('word', w.get('text', ''))
        if str(text).strip():
            out.append({'word': str(text).strip(), 'start': float(w['start']), 'end': float(w['end'])})
    return out


def timed_tokens(words):
    """[(token, start, end, index of the source word)] with numbers spelled out."""
    out = []
    for i, w in enumerate(words):
        for t in tokens(w['word']):
            out.append((t, w['start'], w['end'], i))
    return out


def sound_span(path, floor='-40dB'):
    """First and last moment above the floor, in seconds."""
    err = run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', f'silencedetect=n={floor}:d=0.3',
               '-f', 'null', '-']).stderr
    starts = [float(x) for x in re.findall(r'silence_start: (-?[\d.]+)', err)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', err)]
    dur = duration(path)
    first = ends[0] if starts and starts[0] <= 0.01 and ends else 0.0
    last = starts[-1] if starts and (len(starts) > len(ends) or ends[-1] >= dur - 0.01) else dur
    return first, last, dur


def transcribe(media, language='en'):
    """The words heard in a file's audio, with times, from `npx hyperframes transcribe`. A word whisper times past
    the file's end (it often adds a "you" in the closing silence) is dropped."""
    tmp = tempfile.mkdtemp(prefix='heard-')
    try:
        wav = os.path.join(tmp, 'a.wav')
        r = run(['ffmpeg', '-v', 'error', '-y', '-i', media, '-vn', '-ac', '1', '-ar', '16000', wav])
        if r.returncode or not os.path.exists(wav):
            raise RuntimeError(f'no audio in {media}')
        cmd = ['npx', '-y', 'hyperframes', 'transcribe', wav, '-d', tmp, '--json']
        if language and language != 'en':
            cmd += ['-m', 'small', '-l', language]
        r = run(cmd, timeout=900)
        path = os.path.join(tmp, 'transcript.json')
        if not os.path.exists(path):
            raise RuntimeError('hyperframes transcribe gave no transcript: ' + (r.stderr or r.stdout)[-300:])
        dur = duration(wav)
        return [w for w in load_words(path) if (w['start'] + w['end']) / 2 < dur]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def said(script):
    """The script as said: stage directions in brackets ("[the demo, voice only]") left out."""
    return re.sub(r'\[[^\]]*\]', ' ', script or '')


def word_diff(script, heard, read=None):
    """Every place the heard words differ from the script: [(kind, said, heard, t)], kind DEFECT or FLAG.
    script: text. heard: timed words. read: timed words of the clean voice read; a difference the read's own
    transcript has at the same place is a transcriber miss (a brand name, say), so it is a FLAG."""
    s = tokens(said(script))
    h = timed_tokens(heard)
    known = set()
    if read:
        r = [t[0] for t in timed_tokens(read)]
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, s, r, autojunk=False).get_opcodes():
            if op != 'equal':
                known.update(range(max(i1 - (op == 'insert'), 0), max(i2, i1 + 1)))
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, s, [t[0] for t in h], autojunk=False).get_opcodes():
        if op == 'equal':
            continue
        span = set(range(max(i1 - (op == 'insert'), 0), max(i2, i1 + 1)))
        t = h[j1][1] if j1 < len(h) else (h[-1][2] if h else 0.0)
        kind = 'FLAG' if span and span <= known else 'DEFECT'
        out.append((kind, ' '.join(s[i1:i2]) or '-', ' '.join(t_[0] for t_ in h[j1:j2]) or '-', t))
    return out


def say_diff(said, heard, where='the video'):
    """One word difference in plain words: added, dropped or changed."""
    if said == '-':
        return f'{where} adds "{heard}"'
    if heard == '-':
        return f'{where} drops "{said}"'
    return f'the line says "{said}", {where} says "{heard}"'


def find_line(line, timed, start_at=0):
    """Where a line is said: (index of its last matched token, index of each line token or None)."""
    lt = tokens(line)
    seq = [t[0] for t in timed[start_at:]]
    sm = difflib.SequenceMatcher(None, seq, lt, autojunk=False)
    where = [None] * len(lt)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            where[b + k] = start_at + a + k
    hits = [w for w in where if w is not None]
    if len(hits) < max(1, len(lt) // 2):
        return None, where
    return max(hits), where


# ---- frames, text on screen, faces ---------------------------------------------------------------------------

def frame(video, t, out, width=None):
    vf = ['-vf', f'scale={width}:-2'] if width else []
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(t, 0):.3f}', '-i', video, '-frames:v', '1'] + vf + [out])
    return os.path.exists(out)


def flatness(video, t=0.0):
    """Spread of brightness in a frame (0 = one flat colour), from a 108 x 192 grey copy."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', video, '-frames:v', '1', '-vf',
                          'scale=108:192', '-pix_fmt', 'gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    if not raw:
        return None
    m = sum(raw) / len(raw)
    return math.sqrt(sum((x - m) ** 2 for x in raw) / len(raw))


def have(tool):
    return shutil.which(tool) is not None


def screen_words(text):
    """Words as they read on screen: lower case, marks off, numbers kept as written ("30.4x")."""
    out = []
    for raw in re.split(r"[\s\-\u2013\u2014/|]+", text.replace('\u2019', "'")):
        w = raw.lower().strip(".,!?;:\"'()[]{}*_~`\u201c\u201d\u2018")
        w = re.sub(r"[^\w'.%]", '', w)
        if w:
            out.append(w)
    return out


def ocr_words(png):
    """Words readable in a frame. Tesseract reads it four ways (grey and inverted, full and half size), since big
    type on a photo and small light text on dark each read in only some of them."""
    words, tmp = [], png + '.ocr.png'
    for vf in ('format=gray', 'format=gray,negate', 'scale=iw/2:-2,format=gray', 'scale=iw/2:-2,format=gray,negate'):
        run(['ffmpeg', '-v', 'error', '-y', '-i', png, '-vf', vf, tmp])
        if os.path.exists(tmp):
            words += screen_words(run(['tesseract', tmp, '-', '--psm', '11']).stdout)
    if os.path.exists(tmp):
        os.remove(tmp)
    return words


def shows_on_screen(shows, seen, caption=()):
    """How many of the words a beat must show are readable, small words and the caption's own words aside:
    (found, wanted, missing)."""
    want = [w for w in screen_words(shows) if len(w) >= 3 or any(ch.isdigit() for ch in w)] or screen_words(shows)
    want = [w for w in want if w not in caption]
    got = set(seen)
    hit = lambda w: w in got or any(difflib.SequenceMatcher(None, w, g).ratio() >= 0.8 for g in got if len(g) >= 3)
    found = [w for w in want if hit(w)]
    return len(found), len(want), [w for w in want if w not in found]


def eyes(video, start, end, fps=8):
    """[(t, 'open'|'shut'|None)] for frames from start to end, the last frame before end included, or None when
    Apple Vision isn't here. Shut means the lids are under 0.6 of this take's own open gap, or the eye box has lost
    its dark iris (under 0.35 of the take's own). The take's own open eye is its 80th percentile, so it needs the
    whole take: pass the take, not the cut."""
    if not have('swift') or not os.path.exists(os.path.join(HERE, 'eyes.swift')):
        return None
    tmp = tempfile.mkdtemp(prefix='eyes-')
    try:
        dur = duration(video)
        run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', f'fps={fps},scale=720:-2', os.path.join(tmp, 'f%04d.png')])
        last = max(min(end, dur) - 0.05, 0)
        frame(video, last, os.path.join(tmp, 'last.png'), 720)
        files = sorted(f for f in os.listdir(tmp) if f.endswith('.png'))
        r = run(['swift', os.path.join(HERE, 'eyes.swift')] + [os.path.join(tmp, f) for f in files], timeout=600)
        rows = {}
        for line in r.stdout.splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            name = os.path.basename(d['image'])
            t = last if name == 'last.png' else (int(name[1:5]) - 1) / fps
            rows[name] = (t, d)
        faces = [d for t, d in rows.values() if d.get('face')]
        if not faces:
            return [(t, None) for t, d in sorted(rows.values(), key=lambda x: x[0]) if start <= t <= end]
        q = lambda xs: sorted(xs)[int(0.8 * (len(xs) - 1))]
        gap0 = q([min(d['gapL'], d['gapR']) for d in faces])
        dark0 = q([(d['darkL'] + d['darkR']) / 2 for d in faces])
        out = []
        for t, d in sorted(rows.values(), key=lambda x: x[0]):
            if not (start - 0.01 <= t <= end):
                continue
            if not d.get('face'):
                out.append((t, None))
                continue
            shut = min(d['gapL'], d['gapR']) < 0.6 * gap0 or (d['darkL'] + d['darkR']) / 2 < 0.35 * dark0
            out.append((t, 'shut' if shut else 'open'))
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def envelope_match(take, voice):
    """How closely a take's sound follows the voice it was given (RMS envelopes, 20 ms, best lag within 0.3 s).
    0.9 or more: it kept your read. Lower: the model re-voiced it, so the lips follow words you didn't make."""
    def env(p):
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '8000', '-f', 's16le', '-'],
                             capture_output=True).stdout
        a = array.array('h')
        a.frombytes(raw[:len(raw) // 2 * 2])
        n = 160
        return [math.sqrt(sum(x * x for x in a[i:i + n]) / n) for i in range(0, len(a) - n, n)]

    def corr(x, y):
        m = min(len(x), len(y))
        x, y = x[:m], y[:m]
        if m < 10:
            return 0.0
        mx, my = sum(x) / m, sum(y) / m
        sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
        sx = math.sqrt(sum((a - mx) ** 2 for a in x))
        sy = math.sqrt(sum((b - my) ** 2 for b in y))
        return sxy / (sx * sy) if sx and sy else 0.0

    t, v = env(take), env(voice)
    if not t or not v:
        return None
    return max(corr(t[k:], v) if k >= 0 else corr(t, v[-k:]) for k in range(-15, 16))
