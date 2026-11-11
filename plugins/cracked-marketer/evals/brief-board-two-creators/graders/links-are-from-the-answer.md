---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7701486741403766030|7693852189990636814|7692159679308270861|7698350012371193089|7697574017879788820|7702348333678988574)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:DeW-07isALn|DeeigBCT907|DeHA4sQz7Ok)\b)[\w-]+'
match: not_contains
# Every reference link is one the Vamos answer returned; a made-up link can't open.
---
