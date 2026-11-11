---
type: regex
target: last_message
pattern: 'instagram\.com/(?:p|reel)/(?!(?:De-jmrfPgtt|DfAIU7HxeAQ|DfDD57jAQ44|DfFdUJLlSl9|DfFoUcNjUPY|DfH7xYogP-_|DfNDxQ7PpaK|DfNaiUypqZs|DfNsJ5jDl5F|DfOQS5MBMMq|DfOQZKsCq-G|DfP7L2WDNSY|DfPfuoZgb0z|DfQPthjgKvd|DfQxYDJj4YE|DfRyn8ES13P|DfSKTk7TCMh|DfSUO0CDCCm|DfUjSQPD2A9|DfVSdbGDNMM|DfVnVB7jXF-|DfVzofmAND0|DfXlAChNJYE|DfXuVKgNRkH|DfYAhhFNTcz|DfYL42zxjSe|DfYTnaJFcMP|DfZpAJ_jjAx|DfZyLoixYht|DfaBXHqSimV|DfaEYAURc2w|DfaoftwJL9j|DfbGMx0geML|Dfc7SAVNFlD|DfdHyWYtqYl|Dfdx604DEPe|DfejqYoDHXp|DffDcvkJ91o|DffxQyBjSVQ|Dfh3rzntVdU|Dfh4i03vTam|DfiCCKNHMo8|DfigUn1xj8_|DfirogcJG8u|DfjxDWmH6Np|DfkCsRMknwQ|DfldrETE2eg|DfhOyGZD5Fs|DfgaPp5xtnO|Dfi1Uc2jvKG)(?![\w-]))[\w-]+'
match: not_contains
# Every post link in the reply is one the Vamos answer returned (built from the mock's own links); a made-up link can't open.
---
