---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: '\[RIP\]'
match: not_contains
# The Brain names the brand, so the brief names it; a slot is only for what nobody has said (live run 2026-11-11 wrote "[RIP]", copied from the example's "[App]").
---
