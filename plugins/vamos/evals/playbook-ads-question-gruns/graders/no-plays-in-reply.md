---
type: regex
target: last_message
pattern: '(Paste[\s\S]*){3}'
match: not_contains
# The user asked a question, so the reply is its answer, not five plays with their prompts to paste.
---
