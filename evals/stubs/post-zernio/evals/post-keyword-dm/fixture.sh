#!/bin/bash
# Two finished 9:16 videos with their post sheets, as make-video writes them, already uploaded to Zernio (urls.json).
# The mistakes video's caption asks for a comment word (GUIDE); its sheet has no comment_dm, and the user's message
# gives the link. Both are the founder's own phone footage (label off), so the keyword rule is the only thing under test.
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
