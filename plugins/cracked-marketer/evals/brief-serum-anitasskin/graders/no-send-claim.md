---
type: regex
target: last_message
pattern: '\b(?:I(?:''ve| have)?|I just)\s+(?:sent|emailed|messaged|DM''?d|shared)\b[^\n]{0,60}\b(?:brief|briefs|it|them)\b'
flags: i
match: not_contains
# The skill never sends a brief; the user shares the doc.
---
