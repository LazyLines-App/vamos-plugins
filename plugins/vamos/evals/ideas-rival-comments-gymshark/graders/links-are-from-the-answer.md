---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7661334167342320918|7691025416613645590|7691391322615221526|7692505765805968643|7693245610920529174|7696616410914606358)(?![\w-]))\d+|instagram\.com/(?:p|reel)/(?!(?:DdttvvwsKwS|DecZdnlRgRK|Dee5_vfI9nA|Der2mXShxrN|DfSm3O7o1HJ)(?![\w-]))[\w-]+'
match: not_contains
# Every post link in the reply is one the Vamos answer returned (built from the mock's own links); a made-up link can't open.
---
