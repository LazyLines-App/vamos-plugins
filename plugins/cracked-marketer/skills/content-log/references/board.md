# The board

The board is the user's home: each idea, its script, the finished video and its post sit on one row, and each waits there for their yes. They set a status to Approved, and the next run makes it. Every run reads it first, so its link, kind and column names are on Vamos settings' Board line.

**Their own board first.** When they already plan content in a Notion database, a Google Sheet or another tool connected in Claude, use it, so they keep working where they work: add the columns below that it lacks and the statuses below as Status options, and use the columns it already has under their own names (their "Stage" as Status, their "Publish date" as Goes out). Rename or remove nothing of theirs. Write the names on the Board line: `Board: [link], Notion, Ideas = "Content calendar", Status = "Stage", Goes out = "Publish date".`

**Otherwise make one,** in the first of these the host has:
1. **Notion** (best to look at and to drag): a page "Vamos" holding four databases, Ideas, Hooks, Lessons and Reviews. Ideas gets a board view grouped by Status, with each card's cover the source post's thumbnail (its `cdn.lazylines.ai` link), and a calendar view by Goes out. Each idea is a page whose body holds its script once written.
2. **Google Sheet**: make it with Google Drive's `create_file`, then fill it with Google Sheets. One tab each, Status as a dropdown.
3. **A local file**, in Claude Code or Cowork: `vamos/board.md`, one table each. A scheduled cloud run can't see it, so `/cracked-marketer:loop` moves it first.
4. **A Brain file called Vamos board**, when there's nothing else. Vamos keeps it, so it works on every host.

When the calendar they keep is in a tool that isn't connected in Claude, ask them to connect it at https://claude.ai/customize/connectors and say "done", and use it then. With neither Notion nor Google Sheets connected and no calendar of their own, say in one line that connecting Notion there gives them a board to drag cards on. Either way, carry on with 3 or 4 when they'd rather not, and move the board at the first run after they connect it.

The page a skill publishes is a view of the board, made for reading and filming. Approving happens on the board or in the chat.

## Ideas

| Column | Holds |
|---|---|
| Idea | The idea in one sentence, in the user's words |
| Status | To review, Picked, Approved, Script ready, Made, Ready to post, Scheduled, Posted, Not for me, Stale |
| Source | The post, comment or format it came from, linked, with its multiple |
| Why it's yours | What only this brand can show |
| Stage | Reach, trust or buy, from the Marketing plan |
| Format | The format it's made in |
| Hook | The first line, once written |
| Script | The script, or its link |
| File | The finished video, once made: its path on this computer, or a link |
| Post | Where it went: each account, time and Zernio post id once scheduled, then its link once live |
| Goes out | The date and time it posts, once scheduled: the calendar's date |
| Uses lesson | The lesson it rests on, if any |
| Added | The run's date |

Only the user sets Approved, Ready to post or Not for me. `/cracked-marketer:post` sets Scheduled after their yes to its table and Posted once the post is live; a video they post themselves, they mark Posted. Picked is set only by the loop on "run everything", and `/cracked-marketer:script` writes Picked rows like Approved ones. A row left at To review for 14 days becomes Stale at the next run, which says so; silence is never a yes. In any chat, "approve 1, 3 and 5" counts, and the skill writes the status.

## Hooks

The user's hook database: proven hooks the runs found, and the ones written for them.

| Column | Holds |
|---|---|
| Hook | The first line word for word |
| On screen | The first frame's text |
| Format | The format it ran in |
| Niche | The niche it came from |
| Shape | Its shape from the hooks craft ("Somebody just built", "The loss") |
| Source | The post, linked, with views, multiple and date; or the idea it was written for |
| Added | The date it was added |
| Result | Once posted: views, multiple, and the post's age when read |

## Lessons

| Column | Holds |
|---|---|
| Lesson | One sentence with its numbers |
| Evidence | Post links with views, multiples and the date read; a post under 7 days old is listed as pending |
| Posts | How many posts at least 7 days old it rests on |
| Status | Hunch (under 3 posts), Testing, Confirmed (3 or more, from different weeks), Dropped |
| Action | Make more, Stop, Test next |

A lesson moves up only when a new post at least 7 days old backs it. One flop makes a Hunch, never a Stop. Setup fills the first rows; after that only `/cracked-marketer:content-log` changes them, and every other skill reads them.

## Reviews

One row a week from `/cracked-marketer:content-log` (a second run that week updates it): the date and period, the usual, the hit rate (share of the last 20 posts above 1× and above 2×) and the median ×, the predictions made for next time, the ad ids seen per tracked brand, and, with an Ads Manager export, the Ad week: spend, CPA and ROAS, and each concept code that ran with its CPA.
