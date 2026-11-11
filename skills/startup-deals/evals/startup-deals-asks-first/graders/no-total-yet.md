---
type: regex
target: last_message
pattern: '[Tt]otal[^\n]{0,60}\$ ?[0-9]'
match: not_contains
# Nothing is priced before the five answers are in.
---
