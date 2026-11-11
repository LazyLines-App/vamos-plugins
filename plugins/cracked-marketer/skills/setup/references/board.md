# The board

The board is where each idea and script waits for the user's yes. They change a status to Approved, and the next run makes it. Every run reads it first, so its link and kind are in Vamos settings.

Make it in the first of these the host has:
1. **Notion** (best to look at and to drag): a page "Vamos" holding four databases, Ideas, Hooks, Lessons and Reviews, with a board view of Ideas grouped by Status.
2. **Google Sheet**: make it with Google Drive's `create_file`, then fill it with Google Sheets. One tab each.
3. **A local file**, in Claude Code or Cowork: `vamos/board.md`, one table each. A scheduled cloud run can't see it, so `/cracked-marketer:loop` moves it first.
4. **A Brain file called Vamos board**, when there's nothing else. Vamos keeps it, so it works on every host.

The page a skill publishes is a view of the board, made for reading and filming. Approving happens on the board.

## Ideas

| Column | Holds |
|---|---|
| Idea | The idea in one sentence, in the user's words |
| Status | To review, Picked, Approved, Script ready, Made, Posted, Not for me, Stale |
| Source | The post, comment or format it came from, linked, with its multiple |
| Why it's yours | What only this brand can show |
| Stage | Reach, trust or buy, from the Marketing plan |
| Format | The format it's made in |
| Hook | The first line, once written |
| Script | The script, or its link |
| Uses lesson | The lesson it rests on, if any |
| Added | The run's date |

Only the user sets Approved, Not for me or Posted. Picked is set only by the loop on "run everything", and `/cracked-marketer:script` writes Picked rows like Approved ones. A row left at To review for 14 days becomes Stale at the next run, which says so; silence is never a yes. In Claude Code, "approve 1, 3 and 5" in the chat counts, and the skill writes the status.

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
| Evidence | Post links with views, multiples and the date read |
| Posts | How many posts it rests on |
| Status | Hunch (under 3 posts), Testing, Confirmed (3 or more, from different weeks), Dropped |
| Action | Make more, Stop, Test next |

A lesson moves up only when a new post backs it. One flop makes a Hunch, never a Stop. Setup fills the first rows; after that only `/cracked-marketer:content-log` changes them, and every other skill reads them.

## Reviews

One row a week from `/cracked-marketer:content-log` (a second run that week updates it): the date and period, the usual, the hit rate (share of the last 20 posts above 1× and above 2×) and the median ×, the predictions made for next time, and the ad ids seen per tracked brand.
