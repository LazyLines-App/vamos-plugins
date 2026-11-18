---
type: regex
target: mock_calls
pattern: "biggest outliers from my tracked accounts|from accounts I don't track"
match: not_contains
weight: 0.5
# A followers' ask sends only the comments part, not the tracked-accounts or discovery parts (SKILL.md step 2).
---
