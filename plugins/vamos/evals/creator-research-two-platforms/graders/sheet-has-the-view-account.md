---
type: regex
target: { source: file, path: 'creators-tempo.csv' }
pattern: '^(?=[^\n]*fitxchlo)(?=[^\n]*(?:^|,)\s*"?Instagram"?\s*(?:,|$))'
match: contains
flags: m
---
# Chloe's row is her Instagram account (261.1K typical views), the one Vamos's results view leads with. No Google Sheets in the eval host, so the sheet is the skill's CSV fallback, `creators-[brand].csv`.
