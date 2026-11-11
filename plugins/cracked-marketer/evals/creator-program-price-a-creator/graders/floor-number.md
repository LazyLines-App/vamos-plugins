---
type: regex
target: last_message
pattern: '[Ff]loor[^\n]{0,120}(?:\b(?:1[89]|2[0-2]),\d{3}\b|\b(?:1[89]|2[0-2])(?:\.\d)?\s?K\b)|(?:\b(?:1[89]|2[0-2]),\d{3}\b|\b(?:1[89]|2[0-2])(?:\.\d)?\s?K\b)[^\n]{0,120}floor'
# The floor is the median of the 10 worst of his last 30 posts: about 20,000 to 21,000 by the rule.
---
