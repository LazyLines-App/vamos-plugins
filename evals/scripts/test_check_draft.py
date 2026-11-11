"""review-draft's check_draft.py against the brief skill's own example brief. Standard library only.

    python3 evals/scripts/test_check_draft.py

The creator's captions file stands in for the transcript: the hook said word for word, the ★ line
changed, and one transcript with only a misheard brand name (a transcriber's slip, not the creator's).
"""
import os, re, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CM = os.path.join(ROOT, 'plugins', 'cracked-marketer', 'skills')
CHECK = os.path.join(CM, 'review-draft', 'scripts', 'check_draft.py')
EXAMPLE = open(os.path.join(CM, 'brief', 'references', 'brief.md'), encoding='utf-8').read().split('<!-- example', 1)[1].split('-->', 1)[1]

SRT = """1
00:00:00,400 --> 00:00:04,340
My paycheck lands, and nine minutes later it's gone. On purpose.

2
00:00:11,650 --> 00:00:15,260
Potly moves it the second I get paid, so the rest is mine.
"""
MISHEARD = SRT.replace("Potly moves it the second I get paid, so the rest is mine.",
                       "Partly moves it the second I'm paid, so the rest is mine to spend.")


# A newer brief for the same creator, another video with other hooks, above the example one.
NEWER = """## Dana · Day ten, still fine · due Fri 27 Nov

**2. The first 3 seconds.** Say this word for word, on screen from the first frame:
- **Hook:** "Day ten and I still have money left."

**3. Three things to say.**
- ★ "The fun pot is the only budget I keep."

**7. What you send.** Due Fri 27 Nov. We approve it when the hook is word for word and the ★ line is in.

"""


def run(srt, *extra, briefs=None):
    d = tempfile.mkdtemp()
    briefs = briefs if briefs is not None else EXAMPLE + '\n### Draft review · round 1 · 2026-11-18 · Fix\n'
    for name, text in (('briefs.md', briefs), ('t.srt', srt)):
        with open(os.path.join(d, name), 'w', encoding='utf-8') as f:
            f.write(text)
    return subprocess.run([sys.executable, '-I', CHECK, os.path.join(d, 'briefs.md'), '--creator', 'dana',
                           '--transcript', os.path.join(d, 't.srt'), *extra], capture_output=True, text=True, timeout=60)


class CheckDraft(unittest.TestCase):
    def test_hook_word_for_word(self):
        out = run(SRT, '--caption', 'payday with @potly #ad')
        self.assertRegex(out.stdout, r'OK  hook word for word: the hook, said at 0:00\.4')

    def test_star_line_changed_fails_with_the_difference(self):
        out = run(SRT, '--caption', 'payday with @potly #ad')
        self.assertEqual(out.returncode, 1)
        self.assertRegex(out.stdout, r'FIX ★ line said as written: at 0:11\.7')
        self.assertIn('"i\'m" said as "i get"; "to spend" left out', out.stdout)

    def test_misheard_name_is_checked_by_ear_not_failed(self):
        out = run(MISHEARD, '--caption', 'payday with @potly #ad')
        self.assertRegex(out.stdout, r'EAR ★ line[^\n]*\n\s+"potly" said as "partly"')
        self.assertEqual(out.returncode, 0)

    def test_disclosure_from_the_caption(self):
        self.assertRegex(run(SRT, '--caption', 'payday with @potly #ad').stdout, r'OK  disclosure: in the caption: "#ad"')
        self.assertRegex(run(SRT, '--caption', 'payday with @potly').stdout, r'FIX disclosure: no #ad')
        self.assertRegex(run(SRT).stdout, r'\?\?  disclosure: no caption given')

    def test_the_rest_of_the_must_haves_are_listed_to_look_at(self):
        out = run(SRT).stdout
        self.assertIn('LOOK the app on screen by 3 s (Fixed)', out)
        self.assertIn('LOOK the app screen is readable (approve it when)', out)
        self.assertIn('LOOK the hook on screen from the first frame', out)

    def test_counts_earlier_reviews(self):
        self.assertIn('Earlier draft reviews under it: 1', run(SRT).stdout)


    def test_picks_the_brief_this_video_was_filmed_from(self):
        out = run(SRT, '--caption', '#ad', briefs=NEWER + EXAMPLE).stdout
        self.assertRegex(out, r'Brief: Dana · Payday in nine minutes[^\n]*\(its hooks and ★ line fit what was said best\)')
        self.assertIn('Their other briefs: Dana · Day ten, still fine', out)
        self.assertRegex(out, r'OK  hook word for word')
        named = run(SRT, '--brief', 'day ten', briefs=NEWER + EXAMPLE).stdout
        self.assertIn('Brief: Dana · Day ten, still fine', named)

    def test_a_negated_disclosure_is_not_one(self):
        self.assertRegex(run(SRT, '--caption', 'payday routine, not sponsored').stdout, r'FIX disclosure')

    def test_the_donts_are_listed_to_look_at(self):
        self.assertRegex(run(SRT).stdout, r"LOOK don't: promise savings amounts or say it fixes anyone's debt\. \(part 6\)")


if __name__ == '__main__':
    unittest.main()
