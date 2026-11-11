---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7672759331221228831|7685313664848629014|7686992117905788174|7688031053855968525|7691450082717142294|7697076172470897934|7699148249558551841|7700169568416746785)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:Dd4ciV6Nhku|Dd7y3grM3N1|DdKHMX_hOxP|DdQzpt4scjz|DdRgjTTPOWm|DdRvVcAvW1O|DdreHDbBVmV|DdsmfXmuNu0|Ddz-Dk5MdIM|DeDLvvGR4wX|DeEdTJwgo1M|DeS64J6sUf6|DebomhQPQjL|DecmAK_SNVi|DejYvsaI0og|DekUNwSkoqR|DekqzGJxmrW|DelnqSZz2PW|DepZndSNQuq|DfAQEzXRMRi|DfPP1HtsIrf|DfQQjI5jhlV|DfUHeg7BRgf|DfYmgOrComb|DfcSTe8h2vK|Dfcr8TJMKCV)(?![\w-]))[\w-]+'
match: not_contains
---
# Every post link in the reply is one the Vamos answer or its rows returned (built from the mock's own links); a made-up link can't open.
