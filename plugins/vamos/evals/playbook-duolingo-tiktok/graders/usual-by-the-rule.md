---
type: regex
target: last_message
pattern: '([Uu]sual|[Mm]edian)[^\n]{0,80}(823,63[89]|823\.6\s?[Kk]|824\s?[Kk])|(823,63[89]|823\.6\s?[Kk]|824\s?[Kk])[^\n]{0,80}([Uu]sual|[Mm]edian)'
# 823,638.5 over 32 TikToks at least 7 days old; "usual" or "median" must sit near it.
---
