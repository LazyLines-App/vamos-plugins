---
type: regex
target: { source: file, path: 'vamos/briefs.md' }
pattern: 'instagram\.com/(?:p|reel)/(?!(?:De6vL4rPnqV|De9cC_LvdX2|De_6j9Igksw|DeyONJqtX5i|Deyxc\-WscUu|DfDhKcRBy4a|DfFdUJLlSl9|DfGU2ZJxS6I|DfHpm7lzeQA|DfIbcsTEuUf|DfNWN82R0wR|DfOln6xJdnj|DfRMlPVtlNW|DfS9tS4IcP6|DfSRbmrxiIG|DfSk3e0PLtl|DfW4MGAtDBW|DfZpAJ_jjAx|Dfccs5jo0HD|DflEPfUlfKI)(?![\w-]))[\w-]+|tiktok\.com/@[\w.]+/video/\d+'
match: not_contains
# Every reference link is one of the 20 rows saved from the live run (2026-11-11) or a link in its answer.
---
