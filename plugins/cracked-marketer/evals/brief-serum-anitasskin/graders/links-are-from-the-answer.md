---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7692159679308270861)\b)\d+|instagram\.com/(?:p|reel)/[\w-]+'
match: not_contains
# Every reference link is one the Vamos answer returned; a made-up link can't open.
---
