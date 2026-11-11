---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7683168068620668167|7683319712373148944|7686121671828245790|7688498659603909902|7694654519137062151|7694814576369519903|7695103651404156190|7695108383505943830|7696912351257382157|7698714912024972551|7702611402485206302|7702617865907735839|7704304298783411463|7704432053055524109|7704779962569592094)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:DcqmO6ARg8i|Dd6VuENRUfK|Dd6XTqHxqlJ|DeNJlzshpeg|DecLV66NFLP)\b)[\w-]+|(?:youtube\.com/(?:watch\?v=|shorts/)|youtu\.be/)[\w-]{11}'
match: not_contains
# Bar 9: every post link in the reply is one Vamos returned; a made-up link can't open.
---
