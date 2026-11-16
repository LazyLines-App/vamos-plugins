"""How often each of script's AI tells fires on short-form video scripts: viral transcripts against plain-Claude drafts.

    python3 evals/scripts/measure_tells.py

The corpus is in evals/scripts/shortform/:
- human.jsonl: what viral Reels, TikToks and Shorts say, word for word (public posts' transcripts), in two niches:
  "ai-tech-marketing" (creators we studied, mostly AI, tech and marketing) and "local-and-service" (searched
  2026-11-16 for the trades, coaches, shops and services the AI side writes for).
- ai.jsonl: plain Claude (Sonnet 5.5 and Opus 5.5, `claude -p` with no system prompt beyond "You are Claude" and no tools)
  asked for a short-form script the way a user asks, in the same two niches. `said` is the spoken lines, `screen` the on-screen text and caption it wrote.

A tell is counted once per script. It earns its place when it fires on few viral scripts (the check fails a user's
script on it) and on many more Claude drafts. Standard library only, free, no network.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'plugins', 'vamos', 'skills', 'script', 'scripts'))
import textstats  # noqa: E402

CORPUS = os.path.join(HERE, 'shortform')


def load(name):
    with open(os.path.join(CORPUS, name)) as f:
        return [json.loads(line) for line in f if line.strip()]


def named(text):
    return {h[0] for h in textstats.tell_hits(text)}


def counts():
    """{niche or "all": {"human": n, "ai": n, tell: (human scripts it fires on, AI drafts it fires on)}}"""
    human, ai = load('human.jsonl'), load('ai.jsonl')
    out = {}
    for niche in ('all', 'ai-tech-marketing', 'local-and-service'):
        h = [named(d['text']) for d in human if niche in ('all', d['niche'])]
        a = [named(d['said']) for d in ai if niche in ('all', d['niche'])]
        row = {"human": len(h), "ai": len(a), "any": (sum(1 for s in h if s), sum(1 for s in a if s))}
        for name, _, _ in textstats.TELLS:
            row[name] = (sum(name in s for s in h), sum(name in s for s in a))
        out[niche] = row
    return out


def pct(n, d):
    return f"{n:>4} {100 * n / d:5.1f}%" if d else "   -"


if __name__ == '__main__':
    c = counts()
    cols = [('all', 'all'), ('ai-tech-marketing', 'AI/tech/marketing'), ('local-and-service', 'local and service')]
    print(f"{'':28}" + "".join(f"{label:>36}" for _, label in cols))
    print(f"{'':28}" + "".join(f"{'viral ' + str(c[k]['human']):>18}{'Claude ' + str(c[k]['ai']):>18}" for k, _ in cols))
    for name in [n for n, _, _ in textstats.TELLS] + ['any']:
        print(f"{name:28}" + "".join(f"{pct(c[k][name][0], c[k]['human']):>18}{pct(c[k][name][1], c[k]['ai']):>18}" for k, _ in cols))
