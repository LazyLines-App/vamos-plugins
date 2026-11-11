---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7693598549140983060|7694417232625110293|7694865163022863636|7695169259369925908|7696273482702753044|7697008038795939092|7698128359049530645|7698422110502276365|7699251672798743828|7700349941637500173|7700412759304932614|7701460757967293716)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:Dd_k1shyA2I|De4q8RtoL29|DeZ8jBHIugh|DehkjQlO5Xl|DewtQ0KIVKk|DfFdUJLlSl9)\b)[\w-]+|(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)(?![\w-]{11}\b)[\w-]{11}'
match: not_contains
# Every post link in the reply is one Vamos returned (built from the mock's own ids); a made-up link can't open. The mock is the whole live answer of 2026-11-11 (round 3's ask, 60 credits).
---
