---
type: regex
target: last_message
pattern: 'ROAS|[Bb]est[- ]performing ad|[Aa]d spend of|spen[dt]s? \$\d|revenue of \$'
match: not_contains
# Never claim spend, ROAS or revenue from public data; say longest-running, not best-performing.
---
