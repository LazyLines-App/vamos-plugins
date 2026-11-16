"""script's textstats.py check against the AI tells /vamos:script cuts, on short-form video scripts.
Standard library only, free, no network.

    python3 evals/scripts/test_textstats.py

Each tell has a spoken Before line from a reel, TikTok or Short (six are plain Claude's own, from
evals/scripts/shortform/ai.jsonl); it must fail the check, named by the tell (or, for a made-up story, as a story
nothing the user said holds), and its After must pass. OnShortForm holds the list to the corpus: no tell may trip more
than 3% of viral transcripts, and the list must catch most plain-Claude drafts in both niches (measure_tells.py prints
the counts). A user's own habit stays: a tell their transcripts use passes.
"""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRIPT = os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'script', 'scripts', 'textstats.py')
sys.path.insert(0, os.path.dirname(SCRIPT))
sys.path.insert(0, HERE)
import textstats  # noqa: E402
import measure_tells  # noqa: E402

# (tell, before, after): a spoken line with the tell, and the fix the check asks for.
SPOKEN = [
    ("markdown asterisks", "The American Dental Association recommends replacing your toothbrush every **3 to 4 months**.",  # Opus
     "The American Dental Association recommends replacing your toothbrush every 3 to 4 months."),
    ("chatbot opener", "Certainly! Here's your script: your toothbrush is older than you think.", "Your toothbrush is older than you think."),
    ("check-mark list", "✅ Brightens ✅ Evens your tone", "It brightens and evens your tone."),
    ("it's not X, it's Y", "That's not admin work. That's revenue you're setting on fire.", "That's revenue you're setting on fire."),  # Sonnet
    ("not only, but also", "This serum not only brightens your skin but also fades dark spots.", "This serum fades dark spots."),
    ("in today's world", "In today's fast-paced world, nobody waits for a slow drain.", "Nobody waits for a slow drain."),
    ("here's the thing", "Here's the thing: most freelancers overpay their taxes.", "Most freelancers overpay their taxes."),
    ("let's dive in", "Three protein myths. Let's dive in.", "Three protein myths."),
    ("leverage", "Leverage your best reel.", "Use your best reel."),
    ("game-changer", "This one stretch is a game-changer.", "This one stretch loosens your lower back."),
    ("quietly", "Small bakeries are quietly taking over TikTok.", "Small bakeries are taking over TikTok."),
    ("no fluff", "No fluff. Here are the three mistakes.", "Here are the three mistakes."),
    ("excited to share", "I'm so excited to share that our new serum is finally here.", "Our new serum is here."),
    ("let that sink in", "Most shows die before episode ten. Let that sink in.", "Most shows die before episode ten."),
    ("it's not what you think", "One thing kills most podcasts, and it's not what you think.", "One thing kills most podcasts."),
    ("stop X, start Y", "Stop guessing your prices. Start charging what you're worth.", "Charge what you're worth."),
    ("this matters because", "This matters because your first second decides who stays.", "Your first second decides who stays."),
    ("studies show", "Research shows your body keeps using larger doses; it just takes longer to process them.",  # Opus
     "[your source] shows your body keeps using larger doses; it just takes longer to process them."),
    ("slogan closer", "Your future self will thank you.", ""),
    ("self-answered question", "But the best part? They say they finally trust themselves.", "They say they finally trust themselves."),  # Sonnet
    ("buzzword", "This app will level up your mornings.", "This app plans your mornings."),
    ("follow for more", "Follow for more money tips that actually make sense.", ""),  # Opus
    ("save this", "Save this for your next busy night.", ""),  # Sonnet
    ("em dash", "Batch five episodes — before you launch.", "Batch five episodes before you launch."),
    ("story", "I had 40 followers and a tray of burnt croissants.", "I had [your number] followers and [your real start]."),  # Sonnet's hook, 11-15
]


def run(text, prof=None, facts=""):
    return textstats.check(text, prof or {}, None, [], facts)


class TheTells(unittest.TestCase):
    def test_every_tell_has_a_spoken_line(self):
        self.assertEqual({t for t, _, _ in SPOKEN} - {"story"}, {n for n, _, _ in textstats.TELLS})

    def test_each_before_fails_on_its_tell(self):
        for tell, before, _ in SPOKEN:
            with self.subTest(tell=tell):
                res = run(before)
                self.assertTrue(res["fails"], f"{tell}: nothing failed on {before!r}")
                if tell == "story":
                    self.assertEqual([s["text"] for s in res["stories"]], [before])
                else:
                    self.assertIn(tell, [t["tell"] for t in res["tells"]], json.dumps(res["tells"]))

    def test_each_after_passes(self):
        for tell, _, after in SPOKEN:
            with self.subTest(tell=tell):
                res = run(after)
                self.assertEqual(res["fails"], [], f"{tell}: {after!r} still fails")

    def test_the_whole_script(self):
        # Every Before as one pasted script: each tell is named, and the story with them.
        script = "\n".join(b for _, b, _ in SPOKEN)
        res = run(script)
        missing = {t for t, _, _ in SPOKEN if t != "story"} - {t["tell"] for t in res["tells"]}
        self.assertFalse(missing, f"not named in the whole script: {missing}")
        self.assertIn("I had 40 followers and a tray of burnt croissants.", [s["text"] for s in res["stories"]])
        fixed = "\n".join(a for _, _, a in SPOKEN if a)
        self.assertEqual(run(fixed)["fails"], [])


class OnShortForm(unittest.TestCase):
    """The list against the corpus: viral transcripts against plain-Claude drafts (evals/scripts/shortform/)."""

    @classmethod
    def setUpClass(cls):
        cls.counts = measure_tells.counts()

    def test_no_tell_trips_viral_scripts(self):
        row = self.counts["all"]
        for name, _, _ in textstats.TELLS:
            with self.subTest(tell=name):
                self.assertLessEqual(row[name][0], 0.03 * row["human"], f"{name} fires on {row[name][0]} of {row['human']} viral scripts")

    def test_the_list_catches_claude_in_each_niche(self):
        for niche in ("ai-tech-marketing", "local-and-service"):
            with self.subTest(niche=niche):
                row = self.counts[niche]
                viral, claude = row["any"][0] / row["human"], row["any"][1] / row["ai"]
                self.assertGreaterEqual(claude, 0.5, f"{niche}: Claude {claude:.0%}")
                self.assertGreaterEqual(claude, 3 * viral, f"{niche}: viral {viral:.0%}, Claude {claude:.0%}")

    def test_the_spoken_closers_are_common_in_claude_drafts(self):
        # The two tells added for short-form: each in at least 10% of Claude's drafts in both niches.
        for niche in ("ai-tech-marketing", "local-and-service"):
            for name in ("follow for more", "save this"):
                with self.subTest(niche=niche, tell=name):
                    row = self.counts[niche]
                    self.assertGreaterEqual(row[name][1], 0.10 * row["ai"])


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
        # Rewrites that keep the tell's shape (the last two from script-unslop-fresh replays, 2026-11-16).
        for tell, line in (("stop X, start Y", "Stop posting at random. Post with a plan."),
                           ("it's not X, it's Y", "The routine isn't about perfection. It's about showing up."),
                           ("it's not X, it's Y", "The routine isn't about making every post perfect. You just show up."),
                           ("it's not X, it's Y", "You don't need it perfect. You just need to show up."),
                           ("it's not X, it's Y", "That's not a plan, that's a wish."),
                           ("this matters because", "Our serum is live. It matters because most serums sting."),
                           ("follow for more", "Follow for part two."),
                           ("it's not X, it's Y", "It's not a content plan. It's just my morning."),
                           ("follow for more", "Follow for tomorrow's tray.")):
            with self.subTest(line=line):
                self.assertIn(tell, [t["tell"] for t in run(line)["tells"]])

    def test_on_screen_and_caption_are_checked(self):
        res = textstats.check("Post daily.", {}, None, [], "", "✅ Post daily ✅ Reply to comments\nI had 40 followers and a tray of burnt croissants.")
        self.assertEqual(res["words"], 2)
        self.assertIn("check-mark list", [t["tell"] for t in res["tells"]])
        self.assertEqual(len(res["stories"]), 1)


class TheirHabits(unittest.TestCase):
    def test_a_tell_they_use_stays(self):
        prof = textstats.profile([{"text": "That's the trick. Follow for more bakery tips.", "seconds": 4}])
        self.assertIn("follow for more", prof["tells_used"])
        self.assertEqual(textstats.check("Follow for more sourdough tips.", prof, None, [], "")["fails"], [])

    def test_a_tell_their_videos_use_stays(self):
        # An older profile has no tells_used; their Voice examples (voice.txt) show the habit.
        old = {"words_per_second": 4.41, "tells_per_100_words": 0.03}
        line = "Follow for more Claude skills."
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
        # Shapes viral videos say as often as Claude writes them: "not just X, it's Y", a list of three, "genuinely",
        # "follow me for more".
        for line in ("First, you post, and then you reply.", "So, yeah, and then I left.", "Post daily, reply to comments, and track your views.",
                     "Eggshells, rice, and pasta.", "That isn't a problem if you post daily.", "And it's not one skill either. It's 11 of them.",
                     "It's not just for cleaning. It's for cooking too.", "This genuinely works.", "Follow me for more bakery tips.", "Follow along for tomorrow's tray.",
                     "I don't plan it. It's just my morning.",
                     "Follow the recipe for more flavour.", "I think this works.", "Stop the car. Then wait.", "Bake 5 – 10 loaves.",
                     "This will certainly work."):
            with self.subTest(line=line):
                self.assertEqual(run(line)["tells"], [], line)


class TheCommand(unittest.TestCase):
    def test_cli_exits_1_and_names_each_fix(self):
        with tempfile.TemporaryDirectory() as d:
            path, facts = os.path.join(d, 'script.txt'), os.path.join(d, 'facts.txt')
            with open(path, "w") as f: f.write("Leverage your best post. I had 40 followers and a tray of burnt croissants.\n---\n✅ Post daily")
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
