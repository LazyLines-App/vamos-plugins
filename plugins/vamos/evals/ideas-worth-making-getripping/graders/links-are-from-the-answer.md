---
type: regex
target: last_message
pattern: 'instagram\.com/(?:p|reel)/(?!(?:Dc5-veTh1wi|DcBV4NftT_8|DcvuLHhCMcw|Dd9IRTKtNq5|DdG9h-PThCg|De-pZOex_QN|De2XgbKS5h_|De2gIiFuH8i|De4cvBZNZqw|De5XtoHpWa_|De6vL4rPnqV|DeFRGNIvmwy|DecLtbaPpQq|DeegB_QAbGw|DefHIfUp_jw|DehiDUjo-Nh|Del_LnvSbn5|DeqZ-1hqX_n|Det9LROz91S|Deup8efBYrr|DexrwTwC7JM|DeymmV_o0YL|Dezas5xtAOw|DezlA43DYja|DfAkcH5PdHl|DfEWlTiKSYk|DfFETZstoE9|DfFdUJLlSl9|DfJQqJsiNNf|DfJkzsyT2d5|DfM7c0_COag|DfNj1BWOj3F|DfSKPIpjhtL|DfVc2JuhmyD|DfX9qVvCBVl|DfXEzBZMIFz|DfXULlKxXEz|DfY32Bfzh3m|DfZ4ybMlFru|DfZera8SxIR|DfZw_8bFHWP|DfaBXHqSimV|Dfc1_4oIoEY|DffAJJJsIa0|DffFOrDtPVh|DffwAIJuf8z|DfiCCKNHMo8|DfieHm4ICHc|DfigUn1xj8_|DfiyA53t5le)(?![\w-]))[\w-]+'
match: not_contains
# Every post link in the reply is one the Vamos answer returned (built from the mock's own links); a made-up link can't open.
---
