---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: 'Purito|15-second close-up|get ready with me'
flags: i
match: not_contains
# Only the Approved row is briefed; the To review row (a 15-second close-up) and the Not for me row stay off the doc.
---
