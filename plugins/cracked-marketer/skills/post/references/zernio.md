# Posting through Zernio

Zernio is a scheduler the user signs in to with their own accounts. It publishes through each platform's official API at the set time, with nothing of theirs running. Read from docs.zernio.com on 2026-11-13; the keyword DM on 2026-11-24.

Tools beyond the everyday ones go through `call_tool` with a `name` and its `arguments`. When a name isn't found, `search_tools` with the words in quotes finds the current one.

## Connect

When Zernio isn't connected, say:
> Posting runs on your own Zernio, so your accounts' sign-ins stay with you. Make an account at zernio.com and connect your Instagram, TikTok and YouTube there (the first two accounts are free, then $6 an account a month, zernio.com/pricing on 13 Nov). Then add it to Claude: in the Claude app, Customize → Connectors → Add custom connector, URL `https://mcp.zernio.com/mcp`; in Claude Code, `claude mcp add --transport http zernio https://mcp.zernio.com/mcp`, then `/mcp` to sign in.

Without it, give the hand-off table below. Connect TikTok through Zernio's TikTok for Business app (every new connection is): it posts videos publicly with the AI label, and doesn't share the developer app's daily cap.

## The batch file

```json
{"timezone": "Europe/Madrid", "times": ["09:00", "13:00", "19:00"],
 "accounts": [{"id": "66b2e19d8c3f5a7e9d0b1c2d", "platform": "instagram", "handle": "@brand", "profile": "66a1f0c2a4b9d3e8f1a2b3c4"},
              {"id": "66b2e19d8c3f5a7e9d0b1c2f", "platform": "tiktok", "handle": "@brand", "profile": "66a1f0c2a4b9d3e8f1a2b3c4", "times": ["12:00", "20:00"]}],
 "existing": [{"account": "66b2e19d8c3f5a7e9d0b1c2d", "at": "2026-11-14T09:00:00+01:00", "file": "hook-2.mp4"}],
 "posts": [{"file": "cuts/drama-thanksgiving.mp4", "to": ["66b2e19d8c3f5a7e9d0b1c2d", "66b2e19d8c3f5a7e9d0b1c2f"]},
           {"file": "cuts/hook-3.mp4", "to": ["66b2e19d8c3f5a7e9d0b1c2d"], "at": "2026-11-15T18:30"}]}
```

- `accounts` from `accounts_list` (`platform` as Zernio names it: instagram, tiktok, youtube, facebook, twitter, threads, linkedin, pinterest; `profile` is its `profileId`, which the keyword DM needs). `times` are the Posting line's; an account's own win.
- `existing` from `posts_list` with `limit: 100` (its default is 10), status scheduled, then status published for the last 24 hours: each platform entry's account, time and file (`metadata.vamos_file`), for the batch's accounts only.
- `"tiktok_drafts": true` on the standing-yes path (SKILL.md, While they're away): TikTok rows go to the account's TikTok inbox (`tiktokSettings.draft`), where the user adds the caption and posts. TikTok holds 5 waiting drafts per account in any 24 hours, and a 6th fails until they post or discard one.
- A post with no `at` takes each account's next free time; `"at": "now"` only when the user asked for now.
- The post sheet, `<file>.post.json`, holds `caption`, `ai` (true or false), `people` (none, filmed, made, agreed or likeness), and when they apply `title` (YouTube), `disclosure`, `promotes` (own, partner or none) and `partner` (the brand's handle). A brand's own product video is `promotes: own`: TikTok asks for that disclosure too. `comment_dm` sets the keyword DM (below); on a post in batch.json it wins over the sheet's.

## The keyword DM

When a post asks viewers to comment a word, its `comment_dm` holds the answer:
```json
"comment_dm": {"word": "PENNY", "dm": "Here's the payday template, {{first_name}}: https://penny.app/template",
               "reply_after_dm": "Sent, check your DMs", "reply": "It's at penny.app/template"}
```
`"comment_dm": "none"` when the user answers those comments themselves. plan.py turns it into each row's `dm_rule`, a per-post rule on Zernio's comment-to-DM (`comment_automations_create_comment_automation`):
- Instagram and Facebook: the DM, then `reply_after_dm` under the comment when given. The link goes in the DM's words, since Instagram can refuse buttons to commenters who don't follow the account. `{{first_name}}` fills in from the commenter.
- TikTok, Threads, LinkedIn and YouTube have no DM to a comment, so the rule posts `reply` under the comment there: where to find it ("it's in my bio"). TikTok needs the TikTok for Business connection.
- X and Pinterest can't answer comments through Zernio, and a TikTok inbox draft is posted from the app, so those rows get a FLAG and no rule.

The rule answers comments made while it's on, matching the word as a whole word, once per person. Each DM sent is one Zernio automation run: 2,000 a month free, then $2 per 1,000 on the user's Zernio bill, and one outbound message (10,000 a month free) (docs.zernio.com/pricing, 11-24).

Send it after its post's create, with `post_id` set to the id the create returned. When Zernio answers that the post is already live, send it again with `platform_post_id` (the id `posts_get` shows for it) in place of `post_id`. A 409 means another rule already covers that post: show which and ask. `comment_automations_list_comment_automation_logs` with the rule's `automation_id` shows who got it and why any failed.

## Upload

Each file once, then its `publicUrl` goes in every row that posts it:
1. `call_tool` with `name: "media_get_media_presigned_url"` and `arguments: {"filename": "drama-thanksgiving.mp4", "content_type": "video/mp4", "size": <bytes>}`.
2. `curl -sf -X PUT -H "Content-Type: video/mp4" --data-binary @cuts/drama-thanksgiving.mp4 "<uploadUrl>"` (an empty 200 is success).
3. Write `urls.json` (`{"cuts/drama-thanksgiving.mp4": "<publicUrl>"}`) and run `python3 scripts/plan.py batch.json --urls urls.json`.

Uploads wait in Zernio's storage for 7 days, so create the posts within a week of uploading. A host with no shell uses `media_generate_upload_link`: the user drops the files on that page and `media_check_upload_status` returns their URLs.

## Check, then send

- `validate_post` with each row's `validate` (free, publishes nothing). It catches missing media, caption and hashtag limits and Reel rules. It doesn't check the label fields; plan.py sets those.
- TikTok rows: `call_tool` with the row's `dry_run`, which checks the post without creating it.
- Instagram, when an account is near its cap: `call_tool` `instagram_get_instagram_publishing_limit` with its `account_id`; Meta's live number wins over the one in plan.py.
- X: each post through the API costs $0.015 from the user's Zernio balance, $0.20 with a link in it (X's rate, passed on; docs.zernio.com on 13 Nov). plan.py prints the batch's total.
- After the yes, `call_tool` with each row's `create` (`name: "posts_create_post"`), one row a call. Send each row once: a retry of the same video and caption to the same account within 24 hours comes back 409, which means it's already there.

## When it fails

- "You have created too many posts in the last 24 hours via the API" (TikTok): the account hit TikTok's own limit. Move the row to the next day.
- 429 with a cooldown: a daily cap. Move the row past it; Zernio holds a post over its hourly cap and publishes it itself.
- A post that failed at publish time shows in `posts_list` with status failed and its reason. Say which and why in the next digest; `posts_retry` sends it again once it's fixed.

## The hand-off

With no Zernio, or for a row by hand, give one table they can work down:

| When | Account | File | Caption, word for word | Switch on |
|---|---|---|---|---|
| Sat 09:00 | @brand (Instagram) | drama-thanksgiving.mp4 | … Made with AI. | the AI label (Advanced settings → AI label) |
| Sat 12:00 | Brand Page (Facebook) | drama-thanksgiving.mp4 | … Made with AI. | the AI label when you add the Reel |

Then mark each row Posted on the board once it's up.
