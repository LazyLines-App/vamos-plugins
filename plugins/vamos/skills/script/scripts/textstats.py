"""Voice numbers and script checks, counted in code so no model has to count.

  python3 textstats.py profile transcripts.json > voice-numbers.json
      transcripts.json: [{"text": "...", "seconds": 31.5}, ...]  (their own talking videos)

  python3 textstats.py check script.txt --facts facts.txt --voice voice.txt --profile voice-numbers.json --seconds 30 --sources a.txt b.txt
      script.txt: the Said lines, hook first; then, optionally, a line "---" and the On screen lines and the caption,
      which are checked for tells and stories but not counted. Sources: the find's transcript.
      facts.txt: what the user has really said (Things you've said, their own words in the chat outside any draft).
      voice.txt: their Voice examples, the transcripts of their own videos.
      `[your …]` slots are left out of every count; with slots, length fails only when the words around them are already over.

Each tell the script has is listed with its fix, and fails unless the user says it themselves: voice.txt holds it, or the
profile's `tells_used` does. Each sentence that tells a story about the
user (I had, I was, when I, my first…) fails unless facts.txt or voice.txt holds its numbers and most of its words; a sentence
with a slot fails only on a number outside the slot.

Standard library only. Prints JSON. `check` exits 1 when a check fails, and says which; sentence length only warns.
"""
import argparse, json, re, statistics, sys

# (name, pattern, fix). Matched case-blind on text with curly quotes made straight.
TELLS = [
    ("markdown asterisks", r"\*\*?[^*\n]+\*\*?|\*\*|__[^_\n]+__", "drop the asterisks and keep the words"),
    ("chatbot opener", r"\bcertainly\b|(?:^|[.!?]\s+)(?:absolutely|of course|sure|great question)\s*[!,.]|\bhere'?s (?:your|the|a|an)(?: \w+){0,2} (?:hook|script|caption|rewrite|version|draft|post|reel|breakdown)\b:?|\byou'?re absolutely right\b",
     "cut it and start on the content"),
    ("check-mark list", r"[✅✔✓☑]", "say the items as one plain sentence: \"Post daily and reply to comments.\""),
    ("it's not X, it's Y",
     r"\b(?:(?:is|are|was|were)(?:n'?t| not)|(?:it|this|that|he|she)'?s not|(?:they|you|we)'?re not|not (?:just|only|about)|never about)\b[^.!?\n]{0,80}?[.!?;:,—–-]+\s*(?:but\s+|and\s+)?(?:(?:it|this|that|they|you|we|he|she)(?:'s|'re| is| are| was| were)|(?:you|we|they|it) (?:just|only|simply))\b"
     r"|(?:^|[.!?]\s+)not (?:a|an|the|just|about)\b[^.!?\n]{1,40}[.!?]\s+(?:a|an|the|it'?s|just|about)\b"
     r"|\b(?:you|we) (?:don'?t|do not) need\b[^.!?\n]{0,60}[.!?,;:\u2014\u2013-]+\s*(?:but\s+)?(?:you|we) (?:just |only )?need\b",
     "say only the second half, plainly: \"The routine is about showing up.\""),
    ("not only, but also", r"\bnot only\b.*\bbut also\b", "say the second half"),
    ("in today's world", r"\bin today'?s\b|\bin this day and age\b|\bfast[- ]paced\b|\bever[- ](?:evolving|changing)\b|\bin (?:the|this) (?:digital|modern) (?:age|era|world)\b", "cut it and start on the point"),
    ("here's the thing", r"\bhere'?s the thing\b", "cut it"),
    ("let's dive in", r"\blet'?s (?:dive|jump|get) (?:right )?in(?:to(?: it)?)?\b|\bdeep[- ]dive\b|\bwithout further ado\b", "cut it; the next line starts"),
    ("leverage", r"\bleverag(?:e|es|ed|ing)\b", "say \"use\""),
    ("game-changer", r"\bgame[- ]?chang(?:er|ers|ing)\b", "say what it does"),
    ("genuinely", r"\bgenuinely\b", "cut it"),
    ("quietly", r"\bquietly\b", "cut it"),
    ("no fluff", r"\b(?:no|zero) (?:fluff|filler)\b|\bwithout the fluff\b|\bfluff[- ]free\b", "cut it"),
    ("excited to share", r"\b(?:i'?m|i am|we'?re|we are)(?: so| really| super| very| beyond| incredibly)? (?:excited|thrilled|happy|proud|delighted|pleased|honou?red|stoked) to (?:share|announce|introduce|tell you|say|launch|unveil|reveal)\b",
     "say the news plainly: \"My course is live.\""),
    ("let that sink in", r"\blet that sink in\b|\bread that again\b", "cut it"),
    ("it's not what you think", r"\b(?:it'?s|it is|this is|that'?s|the answer is|the reason is)(?: probably)? not what you(?:'d)? (?:think|expect)\b|\b(?:might|will|may) (?:surprise|shock) you\b", "cut it and say the thing"),
    ("stop X, start Y", r"\bstop [^.!?\n]{1,60}?[.!?,;]\s*(?:and )?start\b|(?:^|[.!?]\s+)stop [^.!?\n]{1,60}?[.!?]\s+[a-z]", "keep only the second half, plainly: \"Post with a plan.\""),
    ("this matters because", r"\b(?:this|that) matters\b|\bit matters because\b|\bwhy (?:this|that|it) matters\b", "cut it and keep what follows"),
    ("studies show", r"\b(?:studies|research|science|(?<!my )(?<!our )data|experts|scientists|statistics|surveys|doctors) (?:show|shows|showed|suggest|suggests|say|says|prove|proves|found|finds|confirm|confirms)\b|\baccording to (?:studies|research|experts|science|data)\b|\bresearch has shown\b",
     "keep the claim and make its source a slot: \"[your source] shows …\""),
    ("slogan closer", r"\bis the new \w+|\byour future self will thank you\b|\bthe rest is history\b|\bthat'?s the power of\b|\band that'?s the (?:secret|magic)\b",
     "end on the last useful line, or their own closer"),
    ("self-answered question", r"\bthe (?:best part|result|answer|catch|secret|kicker|twist|truth)\?", "say it as a plain line that names what's coming"),
    ("buzzword", r"\bunlock(?:s|ed|ing)?\b|\bdelve\b|\bseamless(?:ly)?\b|\belevate\b|\blevel up\b", "say the plain word"),
    ("em dash", r"—|\s–\s", "a full stop or a comma"),
]
TELL_RES = [(n, re.compile(p, re.I | re.M), f) for n, p, f in TELLS]

# A list of three: "like a checklist, a tip, or a template", "your time, your money, and your energy", "faster, smarter, and cheaper".
WORD = r"[a-z][a-z']*"
ITEM = rf"{WORD}(?: {WORD}){{0,2}}"
LIST3 = re.compile(rf"(?<![\w'])({ITEM}), ({ITEM}),? (?:and|or) ({ITEM})", re.I)
LEAD = re.compile(r"^(?:like|such as|including|whether it'?s|from)\s+", re.I)

def straight(text):
    return text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')

def lists_of_three(text):
    hits = []
    for m in LIST3.finditer(text):
        led = bool(LEAD.match(m.group(1)))
        items = [LEAD.sub("", m.group(1)).split(), m.group(2).split(), m.group(3).split()]
        if not all(items):
            continue
        same_start = len({it[0].lower() for it in items}) == 1
        single = all(len(it) == 1 for it in items)
        if led or same_start or single:
            hits.append(m.group(0))
    return hits

def tell_hits(text):
    text = straight(text)
    hits = [(name, m.group(0).strip(), fix) for name, rx, fix in TELL_RES for m in rx.finditer(text)]
    hits += [("list of three", h, "keep the two that matter most: \"like a checklist or a tip\"") for h in lists_of_three(text)]
    return hits

def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [p.strip() for p in parts if re.search(r"\w", p)]

def words(text):
    return re.findall(r"(?:[^\W_]|')+", straight(text).lower())

def per100(n, total):
    return round(100 * n / total, 2) if total else 0.0

def tell_count(text):
    return len(tell_hits(text))

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
    joined = "\n".join(it["text"] for it in items)
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
        "tells_used": sorted({h[0] for h in tell_hits(joined)}),
    }

SLOT = re.compile(r"`?\[your [^\]]*\]`?", re.I)

# A sentence about the user's own past: what only they can say is true.
OWN = re.compile(r"\b(?:i|i'm|i've|i'd|me|my|mine|we|we've|our|us)\b", re.I)
STORY = re.compile(
    r"\b(?:i|we)(?: \w+)? (?:had|was|were|\w{3,}ed|used|made|lost|grew|went|got|spent|sold|quit|hit|did|took|left|began|ran|built|wrote|found|felt|thought|knew|saw|came|became|told|said|paid|won|bought|burnt|broke|threw|fell|met|sent|kept|gave)\b"
    r"|\b(?:i|we)'ve(?: \w+)? \w+|\bmy (?:first|old|last|biggest|worst)\b|\bwhen (?:i|we)\b|\b(?:years?|months?|weeks?|days?) ago\b|\bback (?:in|when)\b|\bused to\b", re.I)
NUMBER_WORDS = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUMBER_WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90})
NUM = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(k|m|million|thousand|billion|bn)?\b", re.I)
SCALE = {"k": 1e3, "thousand": 1e3, "m": 1e6, "million": 1e6, "billion": 1e9, "bn": 1e9}
STOP = set("""a an the and or but so if then than that this these those there here it its it's is are was were be been being am
to of in on at by for with from up down out off over into onto about as just very really also too not no yes
i i'm i've i'd i'll me my mine we we're we've our us you your you're he she they them their his her him
do did does done have has had having get got make made go went one all any some every each more most much many
what when where who why how which while because like hundred thousand million billion""".split())

def numbers(text):
    out = set()
    for m in NUM.finditer(text):
        try:
            out.add(round(float(m.group(1).replace(",", "")) * SCALE.get((m.group(2) or "").lower(), 1), 3))
        except ValueError:
            pass
    out |= {float(NUMBER_WORDS[w]) for w in words(text) if w in NUMBER_WORDS}
    return out

def content(text):
    return {w for w in words(text) if len(w) > 2 and w not in STOP and w not in NUMBER_WORDS and not w[0].isdigit()}

def stories(script, facts):
    fact_nums, fact_words, out = numbers(facts), content(facts), []
    for s in sentences(straight(script)):
        bare = SLOT.sub(" ", s)
        if not (OWN.search(bare) and STORY.search(bare)):
            continue
        missing = sorted(n for n in numbers(bare) if n not in fact_nums)
        if SLOT.search(s):
            if missing:
                out.append({"text": s, "why": "a number about them outside the slot that nothing they said holds"})
            continue
        cw = content(bare)
        held = len(cw & fact_words) / len(cw) if cw else 1.0
        if missing or held < 0.5:
            out.append({"text": s, "why": "a story about them that nothing they said holds"})
    return out

def split_said(text):
    """The Said lines, and what follows a line of "---" (On screen and the caption), which only the tells and stories read."""
    parts = re.split(r"(?m)^-{3,}\s*$", text, maxsplit=1)
    return parts[0], parts[1] if len(parts) > 1 else ""

def ngrams(w, n=4):
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}

def check(script, prof, seconds, sources, facts="", extra="", voice=""):
    told = stories(script + "\n" + extra, facts + "\n" + voice)
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
    hits = tell_hits(script + "\n" + SLOT.sub(" ", extra))
    out["tells_per_100_words"] = per100(len(hits), len(w))
    theirs = set(prof.get("tells_used", [])) | {h[0] for h in tell_hits(voice)}
    bad = [h for h in hits if h[0] not in theirs]
    out["tells"] = [{"tell": n, "text": t, "fix": f} for n, t, f in bad]
    fails += [f"{n}: \"{t}\" ({f})" for n, t, f in bad]
    out["stories"] = told
    fails += [f"{s['why']}: \"{s['text']}\" (make each detail only they know a [your …] slot)" for s in told]
    out["fails"], out["warnings"] = fails, warns
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["profile", "check"])
    ap.add_argument("path")
    ap.add_argument("--profile")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--sources", nargs="*", default=[])
    ap.add_argument("--facts", nargs="*", default=[])
    ap.add_argument("--voice", nargs="*", default=[])
    a = ap.parse_args()
    if a.mode == "profile":
        print(json.dumps(profile(json.load(open(a.path))), indent=2))
    else:
        prof = json.load(open(a.profile)) if a.profile else {}
        facts = "\n".join(open(f).read() for f in a.facts)
        said, extra = split_said(open(a.path).read())
        voice = "\n".join(open(f).read() for f in a.voice)
        res = check(said, prof, a.seconds, [open(s).read() for s in a.sources], facts, extra, voice)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(1 if res["fails"] else 0)
