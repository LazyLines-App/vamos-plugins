---
type: llm
focus:
  source: file
  path: vamos/board.md
---
This is the board after a scheduled ideas run. Before the run the Ideas table had 5 rows (numbered 1 to 5).
PASS if the Ideas table now has at least one new idea row beyond those 5 and every new row's status is To review.
FAIL if no new idea row was added, or any new row has another status (Approved, Picked, Script ready or anything else).
