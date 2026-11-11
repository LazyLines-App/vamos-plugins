#!/usr/bin/env python3
"""Drop the posts that can't be finds, before anything is judged or watched.

    python3 filter.py rows.json [--board board.md] [--min-views 10000] [--today YYYY-MM-DD]

rows.json is a Vamos poll answer (its data.videos), the data file a poll's json_url links to, or a list
of rows. --board is any text holding the board: a post whose link or id is in it is already there.

Keeps a post with views at the floor or over, 2x its creator's usual or more, 150 s or less, posted
within 21 days of the day its numbers were read (counts_as_of; else --today; else today), not on the
board. The same video on two platforms (one creator, lengths within 2 s) is one find: the one with more
views stays. Labels, never drops: "unscored" (no multiple), "long" (over 80 s: its hook or topic only),
"paid" (a paid partner post), "boost?" (likes under 0.5% of views).

Prints {"kept": [...], "dropped": [...]} as JSON. Standard library only.
"""
import argparse, datetime, json, re, sys

MIN_X, MAX_DAYS, MAX_SECONDS, WHOLE_SECONDS, BOOST_RATE = 2.0, 21, 150, 80, 0.005


def rows_of(data):
    if isinstance(data, list):
        return data
    data = data.get("data", data) if isinstance(data, dict) else {}
    return data.get("videos") or data.get("rows") or []


def day(s):
    return datetime.date.fromisoformat(str(s)[:10]) if s else None


def post_id(url):
    return (url or "").rstrip("/").split("/")[-1].split("?")[0]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("rows")
    ap.add_argument("--board")
    ap.add_argument("--min-views", type=int, default=10_000)
    ap.add_argument("--today")
    a = ap.parse_args(argv)
    rows = rows_of(json.load(open(a.rows, encoding="utf-8")))
    board = open(a.board, encoding="utf-8").read() if a.board else ""
    today = day(a.today) or datetime.date.today()
    kept, dropped = [], []
    for r in rows:
        url, views = r.get("url"), r.get("views") or 0
        x, secs = r.get("outlier_score"), r.get("duration_seconds")
        posted, read = day(r.get("posted_at")), day(r.get("counts_as_of")) or today
        days = (read - posted).days if posted else None
        handle = (r.get("creator") or {}).get("handle") or ""
        why = (
            f"under {a.min_views:,} views" if views < a.min_views else
            f"under {MIN_X:g}x its creator's usual" if x is not None and x < MIN_X else
            f"over {MAX_SECONDS} s" if secs and secs > MAX_SECONDS else
            f"posted {days} days before the read, over {MAX_DAYS}" if days is not None and days > MAX_DAYS else
            "already on the board" if board and post_id(url) and re.search(r"(?<![\w-])" + re.escape(post_id(url)) + r"(?![\w-])", board) else ""
        )
        if why:
            dropped.append({"url": url, "why": why})
            continue
        labels = []
        if x is None:
            labels.append("unscored")
        if secs and secs > WHOLE_SECONDS:
            labels.append("long")
        if r.get("paid_partnership") or r.get("sponsors"):
            labels.append("paid")
        if views and r.get("likes") is not None and r["likes"] < BOOST_RATE * views:
            labels.append("boost?")
        kept.append({"url": url, "handle": handle, "platform": r.get("platform"), "views": views, "x": x,
                     "days": days, "seconds": secs, "labels": labels, "caption": r.get("caption_head")})
    # The same video on two platforms: one creator (handles alike once punctuation goes), lengths within 2 s.
    kept.sort(key=lambda k: -k["views"])
    out = []
    for k in kept:
        key = re.sub(r"[^a-z0-9]", "", k["handle"].lower())
        twin = next((o for o in out if key and re.sub(r"[^a-z0-9]", "", o["handle"].lower()) == key
                     and o["platform"] != k["platform"] and k["seconds"] and o["seconds"]
                     and abs(k["seconds"] - o["seconds"]) <= 2), None)
        if twin:
            dropped.append({"url": k["url"], "why": f"twin of {twin['url']}"})
        else:
            out.append(k)
    json.dump({"kept": out, "dropped": dropped}, sys.stdout, ensure_ascii=False, indent=1)
    print(f"\nkept {len(out)} of {len(rows)}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
