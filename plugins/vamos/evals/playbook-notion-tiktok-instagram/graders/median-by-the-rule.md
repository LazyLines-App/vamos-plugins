---
type: regex
target: last_message
pattern: '[Mm]edian[\s\S]{0,200}?(11,01[12]|11\.0\s?[Kk])|(11,01[12]|11\.0\s?[Kk])[\s\S]{0,200}?[Mm]edian'
# TikTok median 11,011.5 over 32 of Notion's own 40 (8 set aside: likes under 0.5% of views; every post is months older than 7 days). "median" within 200 characters of the number, so a list that names the median on one line and the number on the next still counts.
---
