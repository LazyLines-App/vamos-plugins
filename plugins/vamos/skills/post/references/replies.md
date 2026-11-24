# Replies through Zernio

Zernio reads the comments on the user's connected accounts, the posts made outside Zernio included, and posts a reply under a comment as the account. Read from Zernio's API spec (zernio.com/openapi.json) and its pricing pages on 2026-11-24.

Call each through `call_tool` with its `name` and `arguments`, in snake_case as below. When a name isn't found, `search_tools` with the words in quotes finds the current one. With no Zernio connected, say what to connect ([zernio.md](zernio.md), Connect).

## Read

The posts with comments, every connected account in one call:
```json
{"name": "comments_list_inbox_comments", "arguments": {"since": "<7 days ago, ISO>", "min_comments": 1, "limit": 100, "view": "summary"}}
```
`account_id` or `platform` narrows it to the accounts they name. While `pagination.hasMore`, call again with `cursor` set to its `nextCursor`.

Then each post's comments, one call per row, with that row's `id` and `accountId`:
```json
{"name": "comments_get_inbox_post_comments", "arguments": {"post_id": "<the row's id>", "account_id": "<the row's accountId>", "limit": 100, "view": "summary"}}
```
replies.py reads each answer from its file in `vamos/comments/`: the one the host saved, copied there, or, for one that came inline, `comments-<platform>-<n>.json` written as it came. Keep the list answers there too: they name each post and account. Clear the folder before a new batch's reads.

The words their keyword DMs answer are in `vamos/posted.json`, or `comment_automations_list_comment_automations` lists each rule's `keywords`.

pick sets aside a comment with more replies than the page carried, since the user's answer may be among them. To look at one, call again with its `comment_id` (Instagram, Facebook, TikTok).

Zernio holds a read for up to 10 minutes; a reply sent shows at once. Rows marked `isAd` are comments on the user's ads, which this leaves out: say how many, and that they're answered in Ads Manager.

## Where it works

Instagram, Facebook, TikTok, YouTube, X, Threads, LinkedIn, Bluesky and Reddit. TikTok needs the TikTok for Business connection (Zernio's current one); an older connection shows under SKIPPED. On X the account owner switches on X's inbox in Zernio first (`X_INBOX_NOT_ENABLED`). Pinterest has no comment replies through Zernio.

## Send

Each of `send.json`'s calls as it is:
```json
{"name": "comments_reply_to_inbox_post", "arguments": {"post_id": "7701234567890123456", "account_id": "66b2e19d8c3f5a7e9d0b1c2f", "comment_id": "7302000000000000001", "message": "you just snap it, it reads the total for you"}}
```
Then add it to `vamos/replied.json`, a list: `{"comment_id": "...", "post_id": "...", "reply_id": "<data.commentId from the answer>", "at": "<now>"}`.

A reply under a comment costs nothing on Zernio: its message meter counts DMs, not comment replies (docs.zernio.com/pricing/inbox). The inbox comes with Zernio's usage-based plan; an older plan answers 403 "Inbox addon required": say so in one line.

## When it fails

- 422: the platform refused it (a locked thread, a deleted comment, a post too old for comments). Drop that row and say which.
- 403 on one account: it can't comment there; name the account.
- 429: the account's platform quota is spent for now. Send the rest later and say when.
- A timeout or 5xx: the reply may be up. Read that post's comments before sending it again.
