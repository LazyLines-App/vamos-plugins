---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7702402047127162143|7702551918077349134|7703026068470418719|7703328985404427533|7703705136194915597)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:DfGTs_4TQS1|DfJCT_Oj1wZ|DfLA_BtSbdM|DfQSDUBNVlB|DfSpn3OFYYH)\b)[\w-]+|(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)(?!(?:8z8rwiEyjhY|xAwDCkG8QzU)\b)[\w-]{11}'
match: not_contains
# Every post link in the reply is one Vamos returned (built from the mock's own ids); a made-up link can't open.
---
