---
type: regex
target: last_message
pattern: 'ads/library/\?(?:[^\s)]*&)?id=(?!(?:1025582776672337|1038200852444149|1626168029107634|1646639583745376|1690745282247537|2295881991252751|900592785633479|993246029777156)\b)\d+'
match: not_contains
# Every Ad Library link in the reply is one Vamos returned in this run.
---
