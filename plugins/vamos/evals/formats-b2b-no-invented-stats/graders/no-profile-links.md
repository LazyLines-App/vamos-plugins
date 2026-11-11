---
type: regex
target: last_message
pattern: 'instagram\.com/(?!p/|reel/|reels/)[\w.]+/?\)|tiktok\.com/@[\w.]+/?\)'
match: not_contains
---
# An example opens the post, never a profile (gate: "every example shown opens"). The mocks' answers each link one profile as a "best example".
