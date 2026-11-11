#!/usr/bin/env python3
"""The hooks skill's code check (plugins/vamos/skills/hooks/scripts/check.py), on a real saved answer.

    python3 evals/hooks/test_check.py

Free: no Claude, no Vamos. The source is the real skincare answer saved in
plugins/vamos/evals/hooks-skincare-talking/mocks/vamos/chat_completion_poll.md (read 2026-11-05).
Each test changes one thing about a good set of kept hooks, so each rule is tested on its own.
"""
import copy, json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CHECK = os.path.join(ROOT, "plugins/vamos/skills/hooks/scripts/check.py")
SOURCE = os.path.join(ROOT, "plugins/vamos/evals/hooks-skincare-talking/mocks/vamos/chat_completion_poll.md")

GOOD = [
    {"said": "Doctor, why does my moisturiser sting right after I wash my face?",
     "on_screen": "why does my moisturiser sting?",
     "shown": "my red cheeks, close up, the jar in my hand",
     "source": "https://www.tiktok.com/@drabby6/video/7702617865907735839"},
    {"said": "POV: the cream that's supposed to calm your skin is the thing burning it.",
     "on_screen": "pov: the cream is the problem",
     "shown": "a cheek going pink as the cream goes on",
     "source": "https://www.tiktok.com/@lucyellelouise/video/7702626777377639713"},
    {"said": "none",
     "on_screen": "my moisturiser stings and it's not even new 😭",
     "shown": "her eye roll at the mirror",
     "source": "https://www.tiktok.com/@skincare.w.mare/video/7703088459241573662"},
]


def run(hooks):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "kept.json")
        json.dump(hooks, open(p, "w"))
        r = subprocess.run([sys.executable, CHECK, p, SOURCE], capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr


def bad(change, expect):
    hooks = copy.deepcopy(GOOD)
    change(hooks)
    code, out = run(hooks)
    assert code == 1, f"expected a failure for {expect!r}, got:\n{out}"
    assert expect in out, f"expected {expect!r} in:\n{out}"


def main():
    code, out = run(GOOD)
    assert code == 0 and out.strip() == "ok", out

    bad(lambda h: h.extend(copy.deepcopy(GOOD)), "6 hooks")
    bad(lambda h: h.clear(), "0 hooks")
    bad(lambda h: h[0].update(shown=""), "hook 1: no shown")
    bad(lambda h: h[1].pop("on_screen"), "hook 2: no on_screen")
    bad(lambda h: h[0].update(source="https://www.tiktok.com/@drabby6/video/7700000000000000000"), "hook 1: source not in the answer")
    bad(lambda h: h[1].update(source=""), "hook 2: no source")
    bad(lambda h: h[1].update(said="Doctor, why does my moisturiser sting so much?"), "hooks 1 and 2 share")
    bad(lambda h: h[2].update(on_screen="when your moisturiser stings and it's not even a new one you bought last week either"), "hook 3: 16 words on screen")

    # their own line is a source; a silent hook's said can be "none"; case and punctuation don't hide a shared phrase
    ok = copy.deepcopy(GOOD)
    ok[0]["source"] = "their line"
    assert run(ok)[0] == 0
    shared = copy.deepcopy(GOOD)
    shared[1]["said"] = "DOCTOR... why does MY moisturiser sting, honestly?"
    assert "share" in run(shared)[1]

    # a proven hook from the reference names its handle, and the handle must be in references/hooks.md
    ok[1]["source"] = "hooks.md @codyshacks."
    assert run(ok)[0] == 0, run(ok)[1]
    bad(lambda h: h[1].update(source="hooks.md @nobody.real"), "hook 2: source not in references/hooks.md")
    bad(lambda h: h[1].update(source="hooks.md"), "hook 2: source not in references/hooks.md")
    bad(lambda h: h[1].update(source="hooks.md @opus"), "hook 2: source not in references/hooks.md")  # a prefix of @opusjake is not a handle
    print("ok: 16 checks")


if __name__ == "__main__":
    main()
