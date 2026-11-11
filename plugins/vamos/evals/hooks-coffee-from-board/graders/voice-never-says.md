---
type: regex
target: last_message
pattern: '\b[Hh]ack|[Gg]ame[ -]changer|[Bb]arista secret'
match: not_contains
weight: 0.5
# The voice guide's never-says.
---
