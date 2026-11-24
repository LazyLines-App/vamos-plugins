#!/bin/bash
# The folder after an earlier post batch: vamos/posted.json holds the GUIDE keyword rule on the payday reel, and
# vamos/replied.json one reply sent last time (@mia's "is penny free").
set -e
mkdir -p vamos
cat > vamos/posted.json <<'J'
[{"file": "cuts/payday-mistakes.mp4", "account": "66b2e19d8c3f5a7e9d0b1c2d", "post_id": "6750a1b2c3d4e5f6a7b8c901", "at": "2026-11-20T09:00:00+01:00", "rule_id": "6750e1f2a3b4c5d6e7f8a9b1", "keyword": "GUIDE"},
 {"file": "cuts/receipts-hook.mp4", "account": "66b2e19d8c3f5a7e9d0b1c2f", "post_id": "6750a1b2c3d4e5f6a7b8c904", "at": "2026-11-21T12:00:00+01:00"}]
J
cat > vamos/replied.json <<'J'
[{"comment_id": "7302000000000000003", "post_id": "7701234567890123456", "reply_id": "7302000000000000203", "at": "2026-11-24T15:00:00Z"}]
J
