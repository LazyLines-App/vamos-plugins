---
type: regex
target: last_message
pattern: 'instagram\.com/(?:p|reel)/(?!(?:De-jmrfPgtt|DfAIU7HxeAQ|DfDD57jAQ44|DfFoUcNjUPY|DfH7xYogP-_|DfNDxQ7PpaK|DfNaiUypqZs|DfNsJ5jDl5F|DfOQZKsCq-G|DfP7L2WDNSY|DfPfuoZgb0z|DfQPthjgKvd|DfSUO0CDCCm|DfVSdbGDNMM|DfVnVB7jXF-|DfVzofmAND0|DfYTnaJFcMP|DffxQyBjSVQ|DfiCCKNHMo8|DfkCsRMknwQ)(?![\w-]))[\w-]+'
match: not_contains
# Every post link in the reply is one the Vamos answer returned (built from the mock's own links); a made-up link can't open.
---
