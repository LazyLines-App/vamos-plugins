---
type: regex
target: last_message
pattern: 'ads/library/\?(?:[^\s)]*&)?id=(?!(?:1004602658511964|1473422833870752|1906409439981762|2917960288546714|3718705438271185|677175875421059|715482381204671|798467206500886|960629446378954)\b)\d+'
match: not_contains
# Every Ad Library link in the reply is one Vamos returned in this run.
---
