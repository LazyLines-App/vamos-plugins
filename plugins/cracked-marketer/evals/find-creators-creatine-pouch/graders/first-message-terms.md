---
type: regex
target: trace
flags: i
pattern: '(\[N\]|\b\d+)\s+(short\s+|creator\s+)?videos?\b[^\n"]{0,80}\bby\s+(\[date\]|\w)'
---
# Needs R2†: each first message gives the pay, the number of videos and by when (amounts or [N] videos by [date] slots). The messages go in the sheet, so this reads the trace, where the Write call holds them.
