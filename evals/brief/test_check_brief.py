"""The brief checker's own test: the rules that always hold, each broken once on a good brief.

  python3 evals/brief/test_check_brief.py

Free. Uses the skill's scripts/check_brief.py on the example in the skill's references/brief.md and on
the connector's real 2026-10-31 brief (fixtures/vamos-anitasskin-2026-10-31.md), which must fail.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHECK = os.path.join(ROOT, 'plugins', 'cracked-marketer', 'skills', 'brief', 'scripts', 'check_brief.py')
REF = os.path.join(ROOT, 'plugins', 'cracked-marketer', 'skills', 'brief', 'references', 'brief.md')
GOOD = open(REF).read().split('<!-- example: the checker\'s test runs on the brief below -->', 1)[1]
ROWS = 'https://www.tiktok.com/@example/video/1 https://www.tiktok.com/@example/video/2'


def run(text, rows=None):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'briefs.md')
        open(p, 'w').write(text)
        args = [sys.executable, CHECK, p]
        if rows is not None:
            r = os.path.join(d, 'rows.txt')
            open(r, 'w').write(rows)
            args += ['--rows', r]
        out = subprocess.run(args, capture_output=True, text=True)
        return out.returncode, out.stdout


CASES = [
    ('the example passes', GOOD, ROWS, 0, 'PASS'),
    ('the connector brief of 10-31 fails', open(os.path.join(HERE, 'fixtures', 'vamos-anitasskin-2026-10-31.md')).read(), None, 1, 'words; a brief is 300 to 500'),
    ('a table fails', GOOD.replace('**5. Watch these.**', '| Beat | Shot |\n|---|---|\n\n**5. Watch these.**'), ROWS, 1, 'a table'),
    ('a multiple fails', GOOD.replace('skip its music.', 'it did 22× her usual.'), ROWS, 1, 'analysis'),
    ('a 12-word hook fails', GOOD.replace('"This is the only thing I do on payday."', '"This is honestly the only thing I always do on my payday."'), ROWS, 1, 'hook of 12 words'),
    ('a fourth hook fails', GOOD.replace('- "Day ten and I\'m not broke. Here\'s why."', '- "Day ten and I\'m not broke. Here\'s why."\n- "Payday, but make it boring."'), ROWS, 1, '4 hooks'),
    ('hooks not on screen fails', GOOD.replace('put the same words on screen from the first frame', 'keep it natural'), ROWS, 1, 'same words go on screen'),
    ('four beats fail', GOOD.replace('- ★ "Potly', '- Show the totals.\n- ★ "Potly'), ROWS, 1, '4 beats'),
    ('no must-say fails', GOOD.replace('- ★ "Potly', '- "Potly'), ROWS, 1, 'must-say'),
    ('no product by 3 s fails', GOOD.replace('then Potly open by 3 s.', 'then Potly open.').replace('the app on screen by 3 s', 'the app on screen'), ROWS, 1, 'by 3 s'),
    ('an invented link fails', GOOD, 'https://www.tiktok.com/@example/video/1', 1, 'link not in the Vamos answer'),
    ('links after a # or ? in the answer pass', GOOD, '## Beats? #skincare ' + ROWS, 0, 'PASS'),
    ('a link that only starts like a row fails', GOOD, 'https://www.tiktok.com/@example/video/12 https://www.tiktok.com/@example/video/2', 1, 'link not in the Vamos answer'),
    ('no disclosure fails', GOOD.replace('- Disclosure: turn on the paid-partnership label and put #ad in the caption.\n', ''), ROWS, 1, 'disclosure'),
    ('no due date fails', GOOD.replace('Due Fri 20 Nov at [upload link]', 'At [upload link]'), ROWS, 1, 'due date'),
    ('a missing part fails', GOOD.replace('**6. Do and don\'t.**', 'Do and don\'t.'), ROWS, 1, 'parts'),
    ('too short fails', GOOD.split('**4. What to show.**')[0] + '**4.** by 3 s\n**5.** https://www.tiktok.com/@example/video/1\n**6.** #ad\n**7.** Due Fri, approve when done.', ROWS, 1, 'a brief is 300 to 500'),
    ('1080 × 1920 is not a multiple', GOOD, ROWS, 0, 'PASS'),
]

failed = 0
for name, text, rows, code, want in CASES:
    got, out = run(text, rows)
    ok = got == code and want in out
    failed += not ok
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok else f'\n{out}'))
print(f'{len(CASES) - failed} of {len(CASES)} checks pass')
sys.exit(1 if failed else 0)
