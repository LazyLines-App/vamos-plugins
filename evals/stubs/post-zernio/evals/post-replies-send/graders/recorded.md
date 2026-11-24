---
type: regex
target: { source: file, path: 'vamos/replied.json' }
pattern: '^(?=[\s\S]*7302000000000000001)(?=[\s\S]*17900000000000006)(?=[\s\S]*7302000000000000003)'
match: contains
---
Both sent replies are added to the ledger, beside last time's, so the next batch never answers them twice.
