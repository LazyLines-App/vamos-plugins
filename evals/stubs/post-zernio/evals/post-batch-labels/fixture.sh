#!/bin/bash
# Three finished 9:16 videos with their post sheets, as make-video writes them, already uploaded to Zernio (urls.json).
# On purpose: the drama is AI with made characters (label on, disclosure in the caption), the receipts video is the
# founder's own phone footage (label off), and the third is an AI likeness of a real creator (never posted).
set -e
mkdir -p cuts
ffmpeg -v error -y -f lavfi -i testsrc2=s=1080x1920:r=24:d=3 -f lavfi -i sine=f=330:d=3 -c:v libx264 -pix_fmt yuv420p -c:a aac cuts/dinner-drama.mp4
ffmpeg -v error -y -f lavfi -i color=c=0x2b6cb0:s=1080x1920:r=24:d=3 -f lavfi -i sine=f=440:d=3 -c:v libx264 -pix_fmt yuv420p -c:a aac cuts/receipts-hook.mp4
ffmpeg -v error -y -f lavfi -i color=c=0xc53030:s=1080x1920:r=24:d=3 -f lavfi -i sine=f=550:d=3 -c:v libx264 -pix_fmt yuv420p -c:a aac cuts/mrbeast-reacts.mp4
cat > cuts/dinner-drama.post.json <<'J'
{"caption": "Her dad did not see that coming. Comment PENNY and I'll send you the payday template.", "disclosure": "Made with AI.", "ai": true, "people": "made", "promotes": "own", "format": "drama"}
J
cat > cuts/receipts-hook.post.json <<'J'
{"caption": "Every receipt from my first month on Penny, in 20 seconds.", "ai": false, "people": "filmed", "promotes": "own"}
J
cat > cuts/mrbeast-reacts.post.json <<'J'
{"caption": "MrBeast reacts to the Penny payday split", "ai": true, "people": "likeness", "promotes": "own"}
J
cat > urls.json <<'J'
{"cuts/dinner-drama.mp4": "https://media.zernio.com/u/7f3a/dinner-drama.mp4",
 "cuts/receipts-hook.mp4": "https://media.zernio.com/u/7f3b/receipts-hook.mp4",
 "cuts/mrbeast-reacts.mp4": "https://media.zernio.com/u/7f3c/mrbeast-reacts.mp4"}
J
