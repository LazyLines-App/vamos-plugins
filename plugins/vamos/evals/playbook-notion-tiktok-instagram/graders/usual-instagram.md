---
type: regex
target: last_message
pattern: '([Uu]sual|[Mm]edian)[\s\S]{0,200}?(30,70[0-3]|30\.7\s?[Kk])|(30,70[0-3]|30\.7\s?[Kk])[\s\S]{0,200}?([Uu]sual|[Mm]edian)'
# Instagram usual is 30,702 over Notion's own 26 Reels; the answer's 40 includes 14 partner posts that are not Notion's own.
weight: 0.5
---
