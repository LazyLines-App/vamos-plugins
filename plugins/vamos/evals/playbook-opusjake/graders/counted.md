---
type: regex
target: last_message
pattern: '(\b\d{1,3} of (?:the |their |his |her |top |bottom )*\d{1,3}\b[\s\S]*){3}|[Tt]op (?:quarter )?\(?\d{1,3}\)?\s*\|\s*[Bb]ottom (?:half )?\(?\d{1,3}'
# A pattern is counted, never one post's views: three "N of M" in the reply, or a table with Top N and Bottom M columns.
---
