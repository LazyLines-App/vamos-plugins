#!/usr/bin/env python3
"""Check the kept hooks before showing them.

  python3 scripts/check.py kept.json source.txt

kept.json: a list of {"said", "on_screen", "shown", "source"}. "said" is "none" on a silent format;
"source" is the proven post's or ad's link, "hooks.md @handle" for a proven hook from references/hooks.md,
or "their line" for a hook built from the user's own line.
source.txt: the Vamos answer or the Hooks tab the proven hooks came from (any text holding their links).

Prints "ok", or one line per problem and exits 1.
"""
import json, os, re, sys

REFERENCE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "hooks.md")).read()
LINK = re.compile(r"(?:tiktok\.com/@[\w.]+/video/\d+|instagram\.com/(?:p|reel)/[\w-]+|youtube\.com/(?:watch\?v=|shorts/)[\w-]{11}|youtu\.be/[\w-]{11}|facebook\.com/ads/library/\?id=\d+)")


def words(text):
    return re.findall(r"[a-z0-9']+", (text or "").lower())


def grams(hook, n=4):
    out = set()
    for field in ("said", "on_screen"):
        w = words(hook.get(field))
        if w != ["none"]:
            out |= {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
    return out


def key(link):
    return re.sub(r"^.*?(?=tiktok|instagram|youtube|youtu\.be|facebook)", "", link).replace("/reel/", "/p/").rstrip("/")


def main(kept_path, source_path):
    hooks = json.load(open(kept_path))
    known = {key(m) for m in LINK.findall(open(source_path).read())}
    problems = []
    if not 1 <= len(hooks) <= 5:
        problems.append(f"{len(hooks)} hooks: keep one main hook and up to four alternatives")
    for i, h in enumerate(hooks, 1):
        for field in ("said", "on_screen", "shown"):
            if not str(h.get(field) or "").strip():
                problems.append(f"hook {i}: no {field}")
        source = str(h.get("source") or "").strip()
        if not source:
            problems.append(f"hook {i}: no source")
        elif source.lower().startswith("hooks.md"):
            handles = [h.rstrip(".") for h in re.findall(r"@[\w.]+", source)]
            if not handles or not all(re.search(re.escape(h) + r"(?![\w.])", REFERENCE) for h in handles):
                problems.append(f"hook {i}: source not in references/hooks.md ({source})")
        elif source.lower() != "their line":
            found = [key(m) for m in LINK.findall(source)]
            if not found or not all(f in known for f in found):
                problems.append(f"hook {i}: source not in the answer ({source})")
        if words(h.get("said")) in ([], ["none"]) and len(words(h.get("on_screen"))) > 9:
            problems.append(f"hook {i}: {len(words(h.get('on_screen')))} words on screen; a silent hook is read in one glance, about seven words")
    for i in range(len(hooks)):
        for j in range(i + 1, len(hooks)):
            shared = grams(hooks[i]) & grams(hooks[j])
            if shared:
                problems.append(f"hooks {i + 1} and {j + 1} share \"{sorted(shared)[0]}\": make each a different way in")
    print("\n".join(problems) or "ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
