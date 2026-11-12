#!/bin/bash
# Synthetic fixtures (nothing binary in git): the start image and the two voice videos a founder takes to Higgsfield.
set -e
command -v say >/dev/null || { echo 'needs macOS say'; exit 1; }
mkdir -p voice
ffmpeg -v error -y -f lavfi -i testsrc2=s=1080x1920 -frames:v 1 start.png
say -v Samantha -r 170 -o hook.aiff "You don't need to edit for hours."
say -v Samantha -r 170 -o ask.aiff "Comment RIP and I'll send you the template."
for n in hook ask; do  # the clean read on black, 0.25 s in
  ffmpeg -v error -y -f lavfi -i color=black:s=480x854:r=24 -i $n.aiff -af "adelay=250:all=1,apad=pad_dur=0.5" \
    -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac voice/$n-voice.mp4
done
rm -f hook.aiff ask.aiff
