---
type: regex
target: last_message
pattern: '\$(?:1[7-9]|2[0-3])(?:\.\d{1,2})?\s*(?:per|a|/|for every|for each)\s*(?:1,000|1[kK]|thousand)|(?:CPM|per 1,000)[^\n]{0,60}\$(?:1[7-9]|2[0-3])(?:\.\d{1,2})?'
# $400 over a floor near 20,000 views is about $19-20 per 1,000 views.
---
