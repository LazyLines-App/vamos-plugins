"""script's textstats.py check against the 20 AI tells the "20 ways to unslop AI content" video promises
/vamos:script cuts. Standard library only, free, no network.

    python3 evals/scripts/test_textstats.py

Each Before line must fail the check, named by the tell (or, for the made-up story, as a story nothing the user said
holds); each After line, the video's fix, must pass. A user's own habit stays: a tell their transcripts use passes.
"""
import json, os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPT = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'script', 'scripts', 'textstats.py')
sys.path.insert(0, os.path.dirname(SCRIPT))
import textstats  # noqa: E402

# (tell, before, after), the video's before and after for each of the 20.
TWENTY = [
    ("markdown asterisks", "**Pro tip:** open with your result.", "Pro tip: open with your result."),
    ("it's not X, it's Y", "The routine isn't about perfection. It's about showing up.", "The routine is about showing up."),
    ("chatbot opener", "Certainly! Here's your hook: open with your result.", "Open with your result."),
    ("check-mark list", "✅ Post daily ✅ Reply to comments", "Post daily and reply to comments."),
    ("in today's world", "In today's fast-paced world, small bakeries win on Instagram.", "Small bakeries win on Instagram."),
    ("leverage", "Leverage your best post.", "Use your best post."),
    ("game-changer", "This hook is a game-changer.", "This hook gets people to stay past the first second."),
    ("genuinely", "This genuinely works.", "This works."),
    ("no fluff", "No fluff. Here are the steps.", "Here are the steps."),
    ("list of three", "Give them something to keep, like a checklist, a tip, or a template.", "Give them something to keep, like a checklist or a tip."),
    ("let's dive in", "Let's dive in.", ""),
    ("excited to share", "I'm excited to share that my course is live.", "My course is live."),
    ("let that sink in", "Most bakers never post twice. Let that sink in.", "Most bakers never post twice."),
    ("it's not what you think", "One thing grows a bakery account, and it's not what you think.", "One thing grows a bakery account."),
    ("quietly", "Small bakeries are quietly taking over Instagram.", "Small bakeries are taking over Instagram."),
    ("slogan closer", "Consistency is the new currency.", ""),
    ("stop X, start Y", "Stop posting at random. Start posting with a plan.", "Post with a plan."),
    ("this matters because", "This matters because your first line decides who stays.", "Your first line decides who stays."),
    ("studies show", "Studies show posting daily doubles your reach.", "[your source] shows posting daily doubles your reach."),
    ("story", "I had 40 followers and a tray of burnt croissants.", "I had [your number] followers and [your real start]."),
]


def run(text, prof=None, facts=""):
    return textstats.check(text, prof or {}, None, [], facts)


class TheTwenty(unittest.TestCase):
    def test_each_before_fails_on_its_tell(self):
        for tell, before, _ in TWENTY:
            with self.subTest(tell=tell):
                res = run(before)
                self.assertTrue(res["fails"], f"{tell}: nothing failed on {before!r}")
                if tell == "story":
                    self.assertEqual([s["text"] for s in res["stories"]], [before])
                else:
                    self.assertIn(tell, [t["tell"] for t in res["tells"]], json.dumps(res["tells"]))

    def test_each_after_passes(self):
        for tell, _, after in TWENTY:
            with self.subTest(tell=tell):
                res = run(after)
                self.assertEqual(res["fails"], [], f"{tell}: {after!r} still fails")

    def test_the_whole_draft(self):
        # The twenty as one pasted ChatGPT draft: every tell is named, and the story with them.
        draft = "\n".join(b for _, b, _ in TWENTY)
        res = run(draft)
        named = {t["tell"] for t in res["tells"]}
        missing = {t for t, _, _ in TWENTY if t != "story"} - named
        self.assertFalse(missing, f"not named in the whole draft: {missing}")
        self.assertIn("I had 40 followers and a tray of burnt croissants.", [s["text"] for s in res["stories"]])
        fixed = "\n".join(a for _, _, a in TWENTY if a)
        self.assertEqual(run(fixed)["fails"], [])


class Stories(unittest.TestCase):
    def test_a_story_they_told_passes(self):
        facts = "I've baked every weekend since 2021. I had 40 followers when I opened the shop."
        self.assertEqual(run("I've baked every weekend since 2021.", facts=facts)["fails"], [])
        self.assertEqual(run("I had 40 followers when I opened the shop.", facts=facts)["fails"], [])

    def test_a_number_they_never_gave_fails(self):
        facts = "I had 40 followers when I opened the shop."
        res = run("I had 400 followers when I opened the shop.", facts=facts)
        self.assertEqual(len(res["stories"]), 1)

    def test_numbers_match_in_any_spelling(self):
        facts = "I posted 30 times over the last two weeks and got 3,100,000 views."
        self.assertEqual(run("I posted thirty times in two weeks and got 3.1 million views.", facts=facts)["fails"], [])

    def test_a_slot_with_a_made_up_number_beside_it_fails(self):
        res = run("I had 40 followers and [your real start].")
        self.assertEqual(len(res["stories"]), 1)

    def test_present_tense_and_offers_are_not_stories(self):
        for line in ("Comment RIP and I'll send you the system.", "We bake everything before 6 am.", "I need you to try this.",
                     "You launch, you post, and you get three likes."):
            with self.subTest(line=line):
                self.assertEqual(run(line)["stories"], [])


class TheRest(unittest.TestCase):
    def test_half_fixes_still_fail(self):
        # Rewrites seen in replays that kept the tell's shape.
        for tell, line in (("stop X, start Y", "Stop posting at random. Post with a plan."),
                           ("it's not X, it's Y", "The routine isn't about making every post perfect. You just show up."),
                           ("it's not X, it's Y", "You don't need it perfect. You just need to show up."),
                           ("this matters because", "My course is live. It matters because most bakers post at random.")):
            with self.subTest(line=line):
                self.assertIn(tell, [t["tell"] for t in run(line)["tells"]])

    def test_on_screen_and_caption_are_checked(self):
        res = textstats.check("Post daily.", {}, None, [], "", "\u2705 Post daily \u2705 Reply to comments\nI had 40 followers and a tray of burnt croissants.")
        self.assertEqual(res["words"], 2)
        self.assertIn("check-mark list", [t["tell"] for t in res["tells"]])
        self.assertEqual(len(res["stories"]), 1)


class TheirHabits(unittest.TestCase):
    def test_a_tell_they_use_stays(self):
        prof = textstats.profile([{"text": "Honestly this genuinely changed how I post. Genuinely.", "seconds": 4}])
        self.assertIn("genuinely", prof["tells_used"])
        res = textstats.check("This genuinely works.", prof, None, [], "")
        self.assertEqual(res["fails"], [])

    def test_a_tell_their_videos_use_stays(self):
        # An older profile has no tells_used; their Voice examples (voice.txt) show the habit.
        old = {"words_per_second": 4.41, "tells_per_100_words": 0.03}
        line = "And it's not one skill either. It's 11 of them."
        self.assertTrue(textstats.check(line, old, None, [], "")["fails"])
        self.assertEqual(textstats.check(line, old, None, [], "", "", "Voice example: " + line)["fails"], [])
        self.assertTrue(textstats.check("Leverage your best post.", old, None, [], "", "", line)["fails"])

    def test_a_draft_in_facts_does_not_excuse_its_tells(self):
        # facts.txt backs stories only; a pasted draft that lands there keeps its tells.
        draft = "Stop posting at random. Start posting with a plan."
        self.assertTrue(textstats.check(draft, {}, None, [], draft)["fails"])

    def test_a_story_from_their_videos_passes(self):
        res = textstats.check("I had 40 followers when I started.", {}, None, [], "", "", "When I started I had 40 followers and no plan.")
        self.assertEqual(res["stories"], [])

    def test_plain_lines_pass(self):
        for line in ("First, you post, and then you reply.", "So, yeah, and then I left.", "Post daily, reply to comments, and track your views.",
                     "That isn't a problem if you post daily.", "I think this works.",
                     "Stop the car. Then wait.", "Bake 5 \u2013 10 loaves.", "This will certainly work."):
            with self.subTest(line=line):
                self.assertEqual(run(line)["tells"], [], line)


class TheCommand(unittest.TestCase):
    def test_cli_exits_1_and_names_each_fix(self):
        with tempfile.TemporaryDirectory() as d:
            path, facts = os.path.join(d, 'script.txt'), os.path.join(d, 'facts.txt')
            with open(path, "w") as f: f.write("Leverage your best post. I had 40 followers and a tray of burnt croissants.\n---\n\u2705 Post daily")
            with open(facts, "w") as f: f.write("I sell sourdough.")
            p = subprocess.run([sys.executable, SCRIPT, 'check', path, '--facts', facts], capture_output=True, text=True)
            self.assertEqual(p.returncode, 1, p.stdout + p.stderr)
            out = json.loads(p.stdout)
            self.assertIn('say "use"', [t["fix"] for t in out["tells"]])
            self.assertIn("check-mark list", [t["tell"] for t in out["tells"]])
            self.assertEqual(out["words"], 14)  # the Said lines only: the On screen text after --- isn't counted
            self.assertEqual(len(out["stories"]), 1)


if __name__ == '__main__':
    unittest.main()
