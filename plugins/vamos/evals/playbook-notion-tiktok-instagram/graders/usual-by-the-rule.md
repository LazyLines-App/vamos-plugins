---
type: regex
target: last_message
pattern: '([Uu]sual|[Mm]edian)[\s\S]{0,200}?(11,01[12]|11\.0\s?[Kk])|(11,01[12]|11\.0\s?[Kk])[\s\S]{0,200}?([Uu]sual|[Mm]edian)'
# TikTok usual 11,011.5 over 32 of Notion's own 40 (8 set aside: under 3 days or likes under 0.5% of views). "usual" or "median" within 200 characters of the number, so a list that names the usual on one line and the number on the next still counts.
---
