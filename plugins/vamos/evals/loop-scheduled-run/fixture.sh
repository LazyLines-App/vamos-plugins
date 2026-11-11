#!/bin/bash
# The user's local board before a scheduled ideas run (approval: Ask me after ideas).
set -e
mkdir -p vamos
cat > vamos/board.md <<'BOARD'
# Vamos board: RIP (@getripping)

## Ideas

| # | Idea | Status | Source | Why it's yours | Stage | Format | Hook | Script | Uses lesson | Added |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Your rival's 1-star App Store reviews are your launch list | Approved | https://www.instagram.com/p/DfSKTk7TCMh/ (14x) | RIP makes the reel from the reviews in minutes | Reach | Narrated motion graphics | "Your rival's 1-star reviews are your launch list." | | | 2026-11-05 |
| 2 | Why your launch got 0 downloads: you launched to nobody | To review | https://www.instagram.com/p/DfRyn8ES13P/ (117,445 views) | Founders who shipped and heard nothing | Trust | Narrated motion graphics | | | | 2026-10-20 |
| 3 | Three places to launch an app that aren't Product Hunt | To review | https://www.instagram.com/p/Dfc7SAVNFlD/ (7,093 views) | A list RIP's audience asks for in comments | Reach | List | | | | 2026-11-09 |
| 4 | A build-in-public diary of RIP's week | Not for me | own idea | | Trust | Talking head | | | | 2026-11-02 |
| 5 | Steal 100 users from your competitor | Posted | own post | | Reach | Narrated motion graphics | "Steal 100 users from your competitor." | done | | 2026-10-28 |

## Hooks

| Hook | On screen | Format | Niche | Shape | Source | Added | Result |
|---|---|---|---|---|---|---|---|

## Lessons

| Lesson | Evidence | Posts | Status | Action |
|---|---|---|---|---|
| A named job for Claude in the first line beats general founder advice | 3 posts at 8x+ against 4 at under 1x | 7 | Testing | Make more |

## Reviews

| Date | Period | Usual | Hit rate | Median x | Predictions | Ad ids |
|---|---|---|---|---|---|---|
BOARD
