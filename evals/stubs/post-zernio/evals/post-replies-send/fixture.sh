#!/bin/bash
# The folder as the first turn of post-replies-draft leaves it: waiting.json from replies.py pick, the drafts (two
# replies, the spam skipped, Dana's price question asked of the user) and send.json from replies.py plan.
set -e
mkdir -p vamos
cat > vamos/replied.json <<'J'
[{"comment_id": "7302000000000000003", "post_id": "7701234567890123456", "reply_id": "7302000000000000203", "at": "2026-11-24T15:00:00Z"}]
J
cat > waiting.json <<'J'
{"read_at": "2026-11-24T16:00:00+00:00",
 "comments": [
  {"n": 1, "comment_id": "7302000000000000001", "post_id": "7701234567890123456", "account_id": "66b2e19d8c3f5a7e9d0b1c2f", "platform": "tiktok", "handle": "penny.app", "post": "Every receipt from my first month on Penny, in 20 seconds.", "permalink": "https://www.tiktok.com/@penny.app/video/7701234567890123456", "author": "noah.k", "text": "wait you can scan receipts?? how", "likes": 31, "at": "2026-11-22T18:00:00Z"},
  {"n": 2, "comment_id": "7302000000000000002", "post_id": "7701234567890123456", "account_id": "66b2e19d8c3f5a7e9d0b1c2f", "platform": "tiktok", "handle": "penny.app", "post": "Every receipt from my first month on Penny, in 20 seconds.", "permalink": "https://www.tiktok.com/@penny.app/video/7701234567890123456", "author": "cash.guru.99", "text": "Follow me for free money tips 💰 link in bio", "likes": 0, "at": "2026-11-22T18:05:00Z"},
  {"n": 3, "comment_id": "17900000000000006", "post_id": "6750a1b2c3d4e5f6a7b8c901", "account_id": "66b2e19d8c3f5a7e9d0b1c2d", "platform": "instagram", "handle": "penny.app", "post": "3 payday mistakes that empty your account by Friday. Comment GUIDE and I'll sen", "permalink": "https://www.instagram.com/reel/DfPAY1/", "author": "jess.rivera", "text": "the friday one is SO me lol. I always pay rent last and panic", "likes": 22, "at": "2026-11-23T07:00:00Z"},
  {"n": 4, "comment_id": "17900000000000001", "post_id": "6750a1b2c3d4e5f6a7b8c901", "account_id": "66b2e19d8c3f5a7e9d0b1c2d", "platform": "instagram", "handle": "penny.app", "post": "3 payday mistakes that empty your account by Friday. Comment GUIDE and I'll sen", "permalink": "https://www.instagram.com/reel/DfPAY1/", "author": "dana.saves", "text": "How much is Penny after the free month?", "likes": 14, "at": "2026-11-21T08:10:00Z"}],
 "set_aside": {"answered": 3, "keyword": 1, "no_words": 1, "replied_before": 1},
 "skipped_accounts": [],
 "your_replies": ["thank youuu 🫶 took me 3 tries", "it does! connect it under Accounts 🙌", "Sent, check your DMs"]}
J
cat > drafts.json <<'J'
[{"n": 1, "reply": "yep! snap a photo and it fills in the amount and the shop for you 📸"},
 {"n": 2, "skip": "spam"},
 {"n": 3, "reply": "rent last = the friday panic special 😅 pay it first on payday and the rest of the week gets so much calmer"},
 {"n": 4, "ask": "What does Penny cost after the free month?"}]
J
cat > send.json <<'J'
{"calls": [
 {"n": 1, "comment_id": "7302000000000000001", "post_id": "7701234567890123456", "name": "comments_reply_to_inbox_post",
  "arguments": {"post_id": "7701234567890123456", "account_id": "66b2e19d8c3f5a7e9d0b1c2f", "comment_id": "7302000000000000001", "message": "yep! snap a photo and it fills in the amount and the shop for you 📸"}},
 {"n": 3, "comment_id": "17900000000000006", "post_id": "6750a1b2c3d4e5f6a7b8c901", "name": "comments_reply_to_inbox_post",
  "arguments": {"post_id": "6750a1b2c3d4e5f6a7b8c901", "account_id": "66b2e19d8c3f5a7e9d0b1c2d", "comment_id": "17900000000000006", "message": "rent last = the friday panic special 😅 pay it first on payday and the rest of the week gets so much calmer"}}]}
J
