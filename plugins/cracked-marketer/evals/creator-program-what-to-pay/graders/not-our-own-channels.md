---
type: regex
target: last_message
pattern: '@getvamos\.ai\b|\bname\.vamos\b'
match: not_contains
# Vamos's own outreach channels and account naming are Vamos's practice, never the user's.
---
