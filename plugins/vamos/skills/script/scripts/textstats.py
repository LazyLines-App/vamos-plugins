"""Voice numbers and script checks, counted in code so no model has to count.

  python3 textstats.py profile transcripts.json > voice-numbers.json
      transcripts.json: [{"text": "...", "seconds": 31.5}, ...]  (their own talking videos)

  python3 textstats.py check script.txt --profile voice-numbers.json --seconds 30 --sources a.txt b.txt
      script.txt: the Said lines only, hook first. Sources: the find's transcript.
      `[your …]` slots are left out of every count; with slots, length fails only when the words around them are already over.

Standard library only. Prints JSON. `check` exits 1 when a check fails, and says which; sentence length only warns.
"""
import argparse, json, re, statistics, sys

TELLS = [
    r"here'?s the thing", r"game[- ]changer", r"let'?s dive in", r"\bunlock\b", r"\bdelve\b",
    r"\b(?:it|this|that)'?s not (?:just )?(?:\w+ ){0,3}\w+,? (?:it|this|that)'?s\b", r"\bthe best part\?", r"\bin today'?s\b", r"\bseamless(?:ly)?\b",
    r"\belevate\b", r"\blevel up\b", r"\bnot only\b.*\bbut also\b", r"—",
]

def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [p.strip() for p in parts if re.search(r"\w", p)]

def words(text):
    return re.findall(r"(?:[^\W_]|')+", text.lower())

def per100(n, total):
    return round(100 * n / total, 2) if total else 0.0

def tell_count(text):
    low = text.lower()
    return sum(len(re.findall(p, low)) for p in TELLS)

def profile(items):
    rates, lens, all_words, all_sents, qs, short = [], [], [], [], 0, 0
    for it in items:
        w = words(it["text"])
        if it.get("seconds"):
            rates.append(len(w) / float(it["seconds"]))
        for s in sentences(it["text"]):
            n = len(words(s))
            lens.append(n)
            short += n <= 5
            qs += s.rstrip().endswith("?")
        all_words += w
        all_sents += sentences(it["text"])
    total = len(all_words)
    lens.sort()
    joined = " ".join(it["text"] for it in items)
    return {
        "videos": len(items),
        "words_per_second": round(statistics.median(rates), 2) if rates else None,
        "words_per_sentence_median": statistics.median(lens) if lens else None,
        "words_per_sentence_p90": lens[int(0.9 * (len(lens) - 1))] if lens else None,
        "short_sentence_share": round(short / len(lens), 2) if lens else None,
        "questions_per_100_words": per100(qs, total),
        "you_per_100_words": per100(sum(x in ("you", "your", "you're", "yours") for x in all_words), total),
        "i_per_100_words": per100(sum(x in ("i", "i'm", "my", "me", "i've", "i'd") for x in all_words), total),
        "contractions_per_100_words": per100(sum("'" in x for x in all_words), total),
        "tells_per_100_words": per100(tell_count(joined), total),
    }

SLOT = re.compile(r"`?\[your [^\]]*\]`?", re.I)

def ngrams(w, n=4):
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}

def check(script, prof, seconds, sources):
    slots = len(SLOT.findall(script))
    script = SLOT.sub(" ", script)
    sents = sentences(script)
    body = " ".join(sents[1:]) if len(sents) > 1 else ""
    body_grams = ngrams(words(body))
    src_grams = set().union(*(ngrams(words(s)) for s in sources)) if sources else set()
    overlap = round(len(body_grams & src_grams) / len(body_grams), 2) if body_grams else 0.0
    w = words(script)
    out, fails, warns = {"words": len(w), "slots": slots, "overlap_outside_hook": overlap}, [], []
    if overlap > 0.15:
        fails.append(f"overlap {overlap:.0%} with the sources outside the hook (15% at most)")
    if prof.get("words_per_second") and seconds:
        target = round(prof["words_per_second"] * seconds)
        out["target_words"] = target
        if slots and len(w) > 1.15 * target:
            fails.append(f"{len(w)} words before the {slots} slots are filled, over a target of {target}")
        elif slots:
            out["words_left_for_slots"] = max(0, target - len(w))
        elif abs(len(w) - target) > 0.15 * target:
            fails.append(f"{len(w)} words against a target of {target} (within 15%)")
    lens = sorted(len(words(s)) for s in sents)
    if lens and prof.get("words_per_sentence_median"):
        med, theirs = statistics.median(lens), prof["words_per_sentence_median"]
        out["words_per_sentence_median"] = med
        if abs(med - theirs) > 0.15 * theirs:
            warns.append(f"median sentence {med} words against their {theirs} (within 15%)")
    tells = per100(tell_count(script), len(w))
    out["tells_per_100_words"] = tells
    if tells > (prof.get("tells_per_100_words") or 0):
        fails.append(f"{tells} tells per 100 words against their {prof.get('tells_per_100_words') or 0}")
    out["fails"], out["warnings"] = fails, warns
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["profile", "check"])
    ap.add_argument("path")
    ap.add_argument("--profile")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--sources", nargs="*", default=[])
    a = ap.parse_args()
    if a.mode == "profile":
        print(json.dumps(profile(json.load(open(a.path))), indent=2))
    else:
        prof = json.load(open(a.profile)) if a.profile else {}
        res = check(open(a.path).read(), prof, a.seconds, [open(s).read() for s in a.sources])
        print(json.dumps(res, indent=2))
        sys.exit(1 if res["fails"] else 0)
