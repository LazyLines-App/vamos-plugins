---
type: regex
target: last_message
pattern: '([Ww]ant me to|[Ss]hall I|[Ss]hould I|I can|[Hh]appy to|[Ii]f you (want|like|''d like)|[Ss]ay (the word|"?yes|"?save)|[Rr]eply)[^\n]{0,120}\b[Ss]av(e|ing)\b|\b[Ss]ave (it|this|the structure)[^\n]{0,80}\?'
weight: 0.5
# No rows came back in this case, so the skill offers to save the structure in one line rather than saving it (Levi, 11-11).
---
