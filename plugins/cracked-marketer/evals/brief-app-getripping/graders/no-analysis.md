---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: '\d\s?×(?!\s?\d)|\b\d+(?:\.\d+)?x\b|\busual\b|\boutlier|\bmedian\b'
flags: i
match: not_contains
# Never our analysis on the creator's page: multiples and the usual stay with the user.
---
