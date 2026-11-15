---
type: regex
target: { source: file, path: 'creators-tempo.csv' }
pattern: '^(?=[^\n]*fitxchlo)(?=[^\n]*(?:^|,)\s*"?TikTok"?\s*(?:,|$))'
match: not_contains
flags: m
---
# Her TikTok (19.4K) goes in Why them ("also TikTok, 19.4K"), not a second row, so the team works down one row per person.
