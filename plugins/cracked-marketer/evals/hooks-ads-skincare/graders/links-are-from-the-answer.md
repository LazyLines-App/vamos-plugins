---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7702491811004124447|7702617865907735839|7702626777377639713|7703088459241573662|7704469685395377438)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:DfLjNrlBf92|DfPl9-xNfPH)\b)[\w-]+|(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)(?!(?:O8vBobeolfM)\b)[\w-]{11}|ads/library/\?(?:[^\s)]*&)?id=(?!(?:1025582776672337|1038200852444149|1626168029107634|1690745282247537|2295881991252751|900592785633479|993246029777156)\b)\d+'
match: not_contains
---
# Every post and Ad Library link in the reply is one Vamos returned (built from the mock's own ids).
