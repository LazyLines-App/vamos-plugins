---
type: regex
target: last_message
pattern: '(Paste[\s\S]*){5}'
match: contains
# Every play has its five parts in the reply, Paste included (step 11 and the check before the recap): the user reads the chat first. eval-3's Grüns replies scored 1.00 with no Paste on any play.
---
