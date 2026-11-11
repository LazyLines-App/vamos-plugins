---
type: regex
target:
  source: file
  path: vamos/board.md
pattern: '\|\s*(Approved|Picked)\s*\|'
match: not_contains
---
# On Ask me after ideas the run never sets Approved or Picked; the one Approved row moves on to Script ready.
