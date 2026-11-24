# Their numbers from Zernio

Zernio reads each connected account's own analytics through the platforms' APIs, so posts made anywhere count, not only those posted through Zernio (on a personal LinkedIn profile, only Zernio's). These reads are free on Zernio's usage-based plan; its older plans need the analytics add-on, and an answer with `hasAnalyticsAccess: false` or `analytics_addon_required` means it's missing: say so in one line and use screenshots. Read from Zernio's API spec (zernio.com/openapi.json) on 2026-11-24.

Call each read through `call_tool` with its `name` and `arguments`, the arguments in snake_case as below. When a name isn't found, `search_tools` with the words in quotes finds the current one.

## The posts ("post analytics")

One call per account from `accounts_list`:
```json
{"name": "analytics_get_analytics", "arguments": {"account_id": "66b2e19d8c3f5a7e9d0b1c2d", "source": "all", "from_date": "<a year before the period's end>", "to_date": "<the period's end>", "limit": 50}}
```
Newest come first. Ask for `"page": 2` only when page 1 holds fewer than 30 posts from before the period and `pagination.pages` says there are more. count.py reads each answer from its file: the one the host saved, or, for one that came inline, `zernio-instagram-1.json` written as it came.

What the platforms give (Zernio writes 0 for a number a platform doesn't report):
- Every platform: views (X: impressions), reach, likes, comments, shares.
- Saves: Instagram, TikTok, X, Pinterest.
- Average watch time: Instagram Reels, Facebook Reels, TikTok. Skipped in the first 3 s: Instagram Reels. Watched to the end, profile visits and link clicks from the post: TikTok.
- Where viewers left, second by second: TikTok and Facebook Reels (Facebook's is a sample of plays Meta picks). Instagram gives averages only, so a Reel's curve comes from its retention screenshot.
- `isAd`: paid delivery is in the numbers, so count.py sets the post aside.

TikTok's watch numbers, profile visits and curve come with accounts connected through the TikTok for Business app, which is how Zernio connects TikTok now; an older connection shows them as 0.

## YouTube's curve ("YouTube video retention")

One call per YouTube video in the period, 2 to 3 days after it goes up:
```json
{"name": "analytics_get_you_tube_video_retention", "arguments": {"account_id": "<its account>", "video_id": "<the id in its link>", "to_date": "<today>"}}
```
Pass the answer to count.py with the rest. A young or small video's curve comes back empty, with the reason in `note`.

## Followers ("follower stats")

```json
{"name": "accounts_get_follower_stats", "arguments": {"account_ids": "<their account ids, comma-separated>", "from_date": "<the period's length before its start>", "granularity": "daily"}}
```
Zernio reads followers once a day. count.py prints each account's growth over the period beside the same span before it. Followers are read for the user's own connected accounts.
