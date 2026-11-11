---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7694647027623415054|7698189750175321357|7702910409141013791)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:Dd4f5Ydzebw|DfPl9-xNfPH)\b)[\w-]+|(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)[\w-]{11}'
match: not_contains
# Every post link in the reply is one Vamos returned (built from the mock's own ids); a made-up link can't open.
---
