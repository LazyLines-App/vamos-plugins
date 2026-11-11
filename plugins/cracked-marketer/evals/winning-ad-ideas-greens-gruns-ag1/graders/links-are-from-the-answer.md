---
type: regex
target: last_message
pattern: 'ads/library/\?(?:[^\s)]*&)?id=(?!(?:1092313263440974|1403541951895501|1415897367364274|1599442054871610|1887424562624788|2015868355803332|4504807146330117|4602142823401138|936281379262542)\b)\d+'
match: not_contains
# Every Ad Library link in the reply is one Vamos returned in this run.
---
