#!/bin/bash
# The user's board as the last review left it (2026-11-03), with two ad concepts from winning-ad-ideas, and two
# Ads Manager exports (made up for this case, Meta's real column names). Post numbers are from the case's rows.
set -e
mkdir -p vamos
cat > vamos/board.md <<'BOARD'
# Vamos board: RIP (@getripping)

## Ideas

| Idea | Status | Source | Why it's yours | Stage | Format | Hook | Script | Uses lesson | Added |
|---|---|---|---|---|---|---|---|---|---|
| Claude posts your trial reels for you | Posted | own idea | RIP makes the reels the trial runs on | Reach | Narrated motion graphics | Claude can now post trial reels for you | vamos/scripts/trial-reels.md | L2 | 2026-11-03 |
| Two app ideas to build this weekend | Posted | own idea | Founders ask what to build | Reach | Narrated motion graphics | Build these 2 software ideas this weekend | — | — | 2026-10-30 |
| WA-1103-1 Your trial reel's money screen, before and after | Approved | a 96-day Meta ad, static | RIP's own trial numbers | Buy | Meta ad: static | Day 1 → Day 7. | — | — | 2026-11-03 |
| WA-1103-2 Two founders at podcast mics, the app on a phone | Approved | a 120-day Meta ad, video | RIP's founder customers | Buy | Meta ad: video | You built it and nobody came? | — | — | 2026-11-03 |

## Hooks

| Hook | On screen | Format | Niche | Shape | Source | Added | Result |
|---|---|---|---|---|---|---|---|
| Claude can now post trial reels for you | Claude can now post trial reels for you | Narrated motion graphics | Apps & SaaS | Claude can now … for you | Idea "Claude posts your trial reels for you" | 2026-11-03 | |
| Are any vibe coded apps actually making money? | Are any vibe coded apps actually making money? | Narrated motion graphics | Apps & SaaS | The question | https://www.instagram.com/p/DemP8MaD20j/ (169,878 views, 4.1×, read 2026-11-03) | 2026-10-20 | 169,878 views, 4.1×, 17 days old |

## Lessons

| Id | Lesson | Evidence | Posts | Status | Action |
|---|---|---|---|---|---|
| L1 | Openers that call out vibe coders' money problem: 3 of 4 above usual, median 2.1× | DemP8MaD20j 169,878 (4.1×), De-jmrfPgtt 89,276 (2.2×), De78Pr4DABW 81,146 (2.0×), De9czaFgIqc 27,938 (0.7×); read 2026-11-03 | 4 (2 weeks) | Confirmed | Make more |
| L2 | A "Claude can now … for you" opener | Being tried on purpose; no post yet | 0 | Testing | Test next |
| L3 | Idea-list videos run under usual: 0 of 1 above | DfNDxQ7PpaK 5,936 (0.1×), read 2026-11-03 | 1 | Hunch | Test next |

## Reviews

| Date | Period | Usual | Hit rate (last 20: above 1×, above 2×) | Median × | Predictions for next time | Ad ids seen |
|---|---|---|---|---|---|---|
| 2026-11-03 | 2026-10-27 to 2026-11-03 | 41,005 views over 24 posts | 10 of 20, 2 of 20 | 0.94× | P1: the "Claude can now post trial reels for you" video beats 3× usual. P2: another idea-list video stays under usual. | — |
BOARD
cat > ads-2026-11-04_2026-11-10.csv <<'CSV'
Reporting starts,Reporting ends,Ad name,Amount spent (USD),Purchases,Purchases conversion value,Impressions,Cost per purchase (USD)
,,Total,1000.00,26,,,
2026-11-04,2026-11-10,RIP_MG_Money_v1,420.00,12,1188.00,42000,35.00
2026-11-04,2026-11-10,RIP_Static_Money_v2 WA-1103-1,260.00,9,891.00,26000,28.89
2026-11-04,2026-11-10,RIP_MG_IdeaList_v1,180.00,2,198.00,18000,90.00
2026-11-04,2026-11-10,RIP_Static_Money_v1,90.00,3,297.00,9000,30.00
2026-11-04,2026-11-10,RIP_Static_Trial_v1,50.00,0,0.00,5000,
CSV
cat > ads-2026-10-28_2026-11-03.csv <<'CSV'
Reporting starts,Reporting ends,Ad name,Amount spent (USD),Purchases,Purchases conversion value,Impressions,Cost per purchase (USD)
,,Total,830.00,15,,,
2026-10-28,2026-11-03,RIP_MG_Money_v1,300.00,8,792.00,30000,37.50
2026-10-28,2026-11-03,RIP_MG_IdeaList_v1,260.00,4,396.00,26000,65.00
2026-10-28,2026-11-03,RIP_Static_Trial_v1,120.00,2,198.00,12000,60.00
2026-10-28,2026-11-03,RIP_Static_Price_v1,150.00,1,99.00,15000,150.00
CSV
