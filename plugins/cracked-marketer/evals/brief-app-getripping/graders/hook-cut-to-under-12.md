---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: 'If anyone can build an app in a weekend, how do you get your first 100 users'
flags: i
match: not_contains
# The source's spoken hook is 17 words; a creator's hook is under 12, so it can't be carried over whole.
---
