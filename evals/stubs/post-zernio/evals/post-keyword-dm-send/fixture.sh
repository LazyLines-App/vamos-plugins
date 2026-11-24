#!/bin/bash
# The folder as the first turn of post-keyword-dm leaves it: the two uploaded videos, their sheets, urls.json and the
# batch the skill wrote, with the GUIDE video's comment_dm (the checklist link the user gave, in the DM's words).
set -e
mkdir -p cuts
ffmpeg -v error -y -f lavfi -i color=c=0x2f855a:s=1080x1920:r=24:d=3 -f lavfi -i sine=f=330:d=3 -c:v libx264 -pix_fmt yuv420p -c:a aac cuts/payday-mistakes.mp4
ffmpeg -v error -y -f lavfi -i color=c=0x2b6cb0:s=1080x1920:r=24:d=3 -f lavfi -i sine=f=440:d=3 -c:v libx264 -pix_fmt yuv420p -c:a aac cuts/receipts-hook.mp4
cat > cuts/payday-mistakes.post.json <<'J'
{"caption": "3 payday mistakes that empty your account by Friday. Comment GUIDE and I'll send you the checklist.", "ai": false, "people": "filmed", "promotes": "own"}
J
cat > cuts/receipts-hook.post.json <<'J'
{"caption": "Every receipt from my first month on Penny, in 20 seconds.", "ai": false, "people": "filmed", "promotes": "own"}
J
cat > urls.json <<'J'
{"cuts/payday-mistakes.mp4": "https://media.zernio.com/u/7f3d/payday-mistakes.mp4",
 "cuts/receipts-hook.mp4": "https://media.zernio.com/u/7f3b/receipts-hook.mp4"}
J
cat > batch.json <<'J'
{"timezone": "Europe/Madrid", "times": ["09:00"],
 "accounts": [{"id": "66b2e19d8c3f5a7e9d0b1c2d", "platform": "instagram", "handle": "@penny.app", "profile": "66a1f0c2a4b9d3e8f1a2b3c4"},
              {"id": "66b2e19d8c3f5a7e9d0b1c2f", "platform": "tiktok", "handle": "@penny.app", "profile": "66a1f0c2a4b9d3e8f1a2b3c4"}],
 "existing": [],
 "posts": [{"file": "cuts/payday-mistakes.mp4", "to": ["66b2e19d8c3f5a7e9d0b1c2d", "66b2e19d8c3f5a7e9d0b1c2f"],
            "comment_dm": {"word": "GUIDE", "dm": "Here's your payday checklist, {{first_name}}: https://penny.app/checklist", "reply_after_dm": "Sent! Check your DMs", "reply": "It's at penny.app/checklist"}},
           {"file": "cuts/receipts-hook.mp4", "to": ["66b2e19d8c3f5a7e9d0b1c2d", "66b2e19d8c3f5a7e9d0b1c2f"]}]}
J
