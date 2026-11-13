---
type: llm
focus:
  source: file
  path: vamos/board.md
---
This is the user's board after the run. Before it, Lessons held L1 Confirmed (4 posts, 2 weeks), L2 Testing (0 posts) and L3 Hunch (idea-list videos, 1 post). Every post since is under 7 days old, and a post counts toward a lesson only once it's 7 days old: the "Claude can now ... for you" post DfYTnaJFcMP is 12.1x so far at 4.9 days (two more Claude posts are younger), and the idea-list post "Worst app ideas" DfVSdbGDNMM is too early at 6.1 days.
PASS if no lesson is Confirmed on fewer than 3 posts from different weeks (so L2 is not Confirmed), no lesson's action is Stop on fewer than 3 posts (so L3 is not Stop), and no post under 7 days old is counted in a lesson's posts (L2 stays at 0 posts and L3 at 1; a note that a young post is pending is fine).
FAIL if L2 is Confirmed, L3 is Stop or Confirmed, a post under 7 days old is counted in a lesson's posts, or the Lessons table is gone.
