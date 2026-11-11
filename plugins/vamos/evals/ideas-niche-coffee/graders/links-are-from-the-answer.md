---
type: regex
target: last_message
pattern: 'tiktok\.com/@[\w.]+/video/(?!(?:7702184324623387917|7702272490298461470|7703603391464770829|7704009912354950413|7704456688207711501)(?![\w-]))\d+|instagram\.com/(?:p|reel)/(?!(?:DfFjWLQpq_c|DfNcVq_BhSa|DfPrX1wjuQL|DfSWJo8Rvgq|DfTB0oixcOJ)(?![\w-]))[\w-]+'
match: not_contains
# Every post link in the reply is one the Vamos answer returned (built from the mock's own links); a made-up link can't open.
---
