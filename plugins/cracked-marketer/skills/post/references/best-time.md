# The best times to post

Each account's times come from its own numbers: its posts of the last year, the ones made outside Zernio too, and on Instagram when its followers are online. The reads are free on Zernio's usage-based plan; its older plans need the analytics add-on, and an answer with `hasAnalyticsAccess: false` or `analytics_addon_required` means it's missing: say so in one line and take their times. Read from Zernio's API spec (zernio.com/openapi.json) on 2026-11-24.

## The reads

Each through `call_tool` with its `name` and `arguments`. Save each answer in `vamos/times/` as it came, or pass the path where the host saved it.

1. Each account's posts, one call per account from `accounts_list`:
```json
{"name": "analytics_get_analytics", "arguments": {"account_id": "66b2e19d8c3f5a7e9d0b1c2d", "source": "all", "from_date": "<365 days before today>", "to_date": "<today>", "limit": 100, "view": "summary"}}
```
When `pagination.pages` is more than 1, read each next `page` too.

2. Each Instagram account's followers online, per hour over the last 30 days (Meta gives it from 100 followers):
```json
{"name": "analytics_get_instagram_online_followers", "arguments": {"account_id": "66b2e19d8c3f5a7e9d0b1c2d"}}
```

Then, from the folder that holds `vamos/`:
```
python3 scripts/times.py vamos/times/*.json --tz Europe/Madrid --slots 2
```
`--tz` is the Posting line's time zone, else the one the user named, else the computer's (`readlink /etc/localtime` names it) when it isn't UTC; with none of these, ask it in the step's one message. `--slots` is how many a day they post: the Posting line's, else what they said, else 2.

## What times.py does

- It counts posts at least 7 days old, and leaves out ads and paid partnerships, whose views were bought.
- It scores each post against the 20 posts around it, so an account's growth over the year doesn't credit the hours it happened to use in its good months.
- It compares 3-hour windows that hold at least 5 posts each, and a window leads only when its lead is bigger than shuffling the same posts' times gives 9 times in 10.
- It puts Meta's followers-online hours on the user's own clock.
- It proposes the leading time, then the busiest follower hours, then the time they post at most, then test times where their numbers are thin, each 3 hours apart, and writes `times.json`.

## Showing it

Per account, the windows table and what it says, then its TIMES line as the proposal, each time with its reason, all in terms of their posts and their followers. Where the numbers can't tell (too few posts, or nearly all at one time), say so in a line, and give the test times their job: "Post at both for the next month, then ask me when to post: the read will compare them." A lead says when their posts have done best; the post itself decides most of what it gets.

The times come from their own numbers only: the published best-time studies disagree with each other (Buffer's and Metricool's 2026 Instagram times differ), and none is about their followers.

The agreed times go on the Posting line, per account, and into batch.json as each account's `times`.

## Without Zernio

Ask for their times. Their apps show when their followers are on (Instagram: Professional dashboard → Total followers → Most active times; TikTok: Analytics → Followers → Follower activity): a screenshot gives the busiest hours.
