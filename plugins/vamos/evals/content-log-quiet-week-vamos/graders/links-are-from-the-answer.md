---
type: regex
target: last_message
pattern: 'instagram\.com/p/(?!(?:C4ZIDs0tbj6|DeHQuo8oW0\-|DejaMVRj\-7i|DfIciDSiqTz|DfPXiP0RhNl|DfRxSG6OU79|DfShbk\-B_E_)(?![\w-]))[\w-]+|tiktok\.com/@[\w.]+/video/(?!(?:7555835578428706070|7560659670407433494|7693170798533594371|7702568062091808013|7702578674981276942|7703560808797703455)(?!\d))\d+'
match: not_contains
---
# Every post link is one the rows or the answer gave. (?![\w-]) not \b: some ids end in '-'.
