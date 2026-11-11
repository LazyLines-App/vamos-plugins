#!/usr/bin/env python3
"""The ideas skill's code filter (plugins/vamos/skills/ideas/scripts/filter.py), checked on real rows.

    python3 evals/ideas/test_filter.py

Free: no Claude, no Vamos. The rows are the real coffee answer saved in
plugins/vamos/evals/ideas-niche-coffee/mocks/vamos/chat_completion_poll.md (read 2026-11-05), plus
copies of one row with a single field changed, so each rule is tested on its own.
"""
import copy, json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILTER = os.path.join(ROOT, "plugins/vamos/skills/ideas/scripts/filter.py")
POLL = os.path.join(ROOT, "plugins/vamos/evals/ideas-niche-coffee/mocks/vamos/chat_completion_poll.md")


def run(rows, *args):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "rows.json")
        json.dump(rows, open(p, "w"))
        r = subprocess.run([sys.executable, FILTER, p, *args], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        return json.loads(r.stdout)


def by_id(out):
    kept = {k["url"].rstrip("/").split("/")[-1]: k for k in out["kept"]}
    dropped = {k["url"].rstrip("/").split("/")[-1]: k["why"] for k in out["dropped"]}
    return kept, dropped


def main():
    poll = json.loads(open(POLL).read())
    fails = []

    def check(name, ok):
        print(("ok   " if ok else "FAIL ") + name)
        if not ok:
            fails.append(name)

    # 1. The whole poll answer is accepted as it came; real rows, read 2026-11-05.
    kept, dropped = by_id(run(poll))
    check("reads a poll answer's data.videos", len(kept) + len(dropped) == 10)
    check("the same video on two platforms is one find, the bigger kept",
          "DfPrX1wjuQL" in kept and "twin" in dropped.get("7703603391464770829", ""))
    check("a row with no multiple is kept and labelled unscored",
          "7704009912354950413" in kept and "unscored" in kept["7704009912354950413"]["labels"])
    check("over 80 s is kept for its hook or topic only",
          "long" in kept["DfNcVq_BhSa"]["labels"] and "long" not in kept["DfSWJo8Rvgq"]["labels"])
    check("ages are counted from the read date, not today",
          kept["7702184324623387917"]["days"] == 7)
    check("the multiple is the row's, untouched", kept["DfSWJo8Rvgq"]["x"] == 137.45)

    base = poll["data"]["videos"][5]  # @3llunx, 3,864,663 views, 137.45x, 11 s, posted 11-03, read 11-05

    def one(**change):
        r = copy.deepcopy(base)
        for k, v in change.items():
            r[k] = v
        r["url"] = "https://www.instagram.com/p/TEST/"
        return r

    def why(row, *args):
        out = run({"videos": [row]}, *args)
        return out["dropped"][0]["why"] if out["dropped"] else ""

    check("under 2x is dropped", "2x" in why(one(outlier_score=1.6)))
    check("2x exactly is kept", why(one(outlier_score=2.0)) == "")
    check("over 150 s is dropped", "150" in why(one(duration_seconds=151)))
    check("posted more than 21 days before the read is dropped",
          "21" in why(one(posted_at="2026-10-10T00:00:00.000Z")))
    check("under the views floor is dropped", "views" in why(one(views=4000)))
    check("--min-views lowers the floor for a small niche", why(one(views=4000), "--min-views", "2000") == "")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as b:
        b.write("| Idea | Source |\n| x | https://www.instagram.com/p/TEST/ 137x |\n")
    check("a post already on the board is dropped", "board" in why(one(), "--board", b.name))
    os.unlink(b.name)
    out = run({"videos": [one(likes=5000)]})
    check("likes under 0.5% of views is a label, never a drop",
          not out["dropped"] and "boost?" in out["kept"][0]["labels"])
    out = run({"videos": [one(paid_partnership=True)]})
    check("a paid partner post is a label, never a drop", not out["dropped"] and "paid" in out["kept"][0]["labels"])
    out = run([one()])
    check("a bare list of rows is accepted", len(out["kept"]) == 1)

    print(f"\n{len(fails)} failed" if fails else "\nall passed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
