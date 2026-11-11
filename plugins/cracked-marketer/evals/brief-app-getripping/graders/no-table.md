---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: '^\s*\|'
flags: m
match: not_contains
# A phone page has no tables; the beats are talking points.
---
