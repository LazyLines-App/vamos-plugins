---
type: regex
target: last_message
pattern: '([Uu]sual|[Mm]edian)[^\n]{0,80}(42,606|42\.6\s?[Kk])|(42,606|42\.6\s?[Kk])[^\n]{0,80}([Uu]sual|[Mm]edian)'
# 42,606 over 34 posts. 42,466 and 42,746 are posts' own views, so "usual" or "median" must sit near it.
---
