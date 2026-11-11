---
type: regex
target: last_message
pattern: '(?<![Cc]omment )\[[a-z][a-z -]{2,30}\](?!\()'
match: not_contains
# A first line is written out, never a template with a blank slot ("[funny line] or do your Lingo Loop lesson"). Markdown links are left out by the lookahead, and "comment [keyword]", which names the mechanic a brand lacks (the live Notion reply wrote "I found no spoken \"comment [keyword]\""), by the lookbehind.
---
