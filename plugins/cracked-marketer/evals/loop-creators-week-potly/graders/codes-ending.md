---
type: llm
---
A Spark code that runs out mid-campaign stops the ad, or one left running passes the agreed window (needs W3: it records each code's expiry and flags any within 5 days).
PASS if the reply flags @maya.money's Spark code (asked 2026-09-15 for 60 days, so it ends about 2026-11-14) as ending within days, and says to renew it or stop the ad.
FAIL if that code isn't mentioned, or its end date is wrong by more than 2 days.
