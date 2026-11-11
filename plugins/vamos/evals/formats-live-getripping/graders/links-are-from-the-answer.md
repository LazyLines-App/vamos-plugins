---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7690318295072787743|7692491140322430221|7693250740550110478|7699973205003373837|7702272117307460894|7702847645542518037|7703328985404427533|7703660754154655006|7704503022704954638|7704753281876167949|7704785041460595982|7705168597579992334|7705177979449593101)\b)\d+|instagram\.com/(?:p|reel)/(?!(?:Dd8jH5StTSp|Dd9SetChJ5K|DdI0AtajaTc|DdX3o8OTlFJ|DdcIz2whCT5|De2xso4tIzK|De6mrPKMMtJ|DeMh-r3ttwt|DePUzt2tBiZ|DeSJC_lp9TB|DeZQgiSTyXD|Dechlk8ANSU|DecoA5rJqSr|DekMIkHIVZQ|DekMrilP-NR|Deyxc-WscUu|DfF-e74FIlW|DfHR2L0yufU|DfHYarntuGf|DfHsbxKBmVb|DfIbcsTEuUf|DfJ5KUOTo0q|DfJBgWLsuwb|DfKOceCRfew|DfNWN82R0wR|DfO3K2iiFmu|DfPSylwT83S|DfQHg1Ku0z5|DfSDZ6Qozfu|DfSETEJS_8W|DfTHrMZuxcU|DfV19B_xccE|DfWBHYlhydE|DfX6B6jSeTQ|DfXj7tpKZ2z|DfXjgHmJ4B9|DfYTnaJFcMP|DfZ2tM9Si_Q|DfZuiqSoNZT|Dfa3yzAAxH6|DfcoEvND95m|DffkKZsNSnn|DfgMn0pN0jl|DfglwSXjtBR|Dfhfu-7yXzX|DfiCCKNHMo8|DfiCJVdpqbc|Dfjbz1ANZlJ)(?![\w-]))[\w-]+|youtube\.com/shorts/(?!(?:3NDIHrvyVCM)(?![\w-]))[\w-]+'
match: not_contains
---
# Every post link in the reply is one the live Vamos answer or its rows returned (built from the mock's own links); a made-up link can't open.
