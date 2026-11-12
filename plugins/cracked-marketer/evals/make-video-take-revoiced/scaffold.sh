#!/bin/bash
# Synthetic fixtures, made fresh each run (nothing binary in git): two presenter takes "back from Seedance" with an
# ffmpeg test pattern for the face. The hook take carries the read it was given; the ask take came back re-voiced
# (another voice, faster, an added "And"), the way one trial take in two did on 11-12. macOS `say` makes the voices.
set -e
command -v say >/dev/null || { echo 'needs macOS say'; exit 1; }
mkdir -p voice takes
say -v Samantha -r 170 -o hook.aiff "You don't need to edit for hours."
say -v Samantha -r 170 -o ask.aiff "Comment RIP and I'll send you the template."
say -v Daniel -r 215 -o ask-revoiced.aiff "And comment RIP, and I'll send you the template."
for n in hook ask; do  # the voice video Seedance was given: the clean read on black, 0.25 s in
  ffmpeg -v error -y -f lavfi -i color=black:s=480x854:r=24 -i $n.aiff -af "adelay=250:all=1,apad=pad_dur=0.5" \
    -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac voice/$n-voice.mp4
done
ffmpeg -v error -y -f lavfi -i testsrc2=s=480x854:r=24 -i hook.aiff -af "adelay=250:all=1,apad=pad_dur=0.5" \
  -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac takes/take-hook.mp4
ffmpeg -v error -y -f lavfi -i testsrc2=s=480x854:r=24 -i ask-revoiced.aiff -af "adelay=150:all=1,apad=pad_dur=0.6" \
  -shortest -c:v libx264 -pix_fmt yuv420p -c:a aac takes/take-ask.mp4
rm -f hook.aiff ask.aiff ask-revoiced.aiff
printf '%s\n' "You don't need to edit for hours." "[the demo, voice only]" "Comment RIP and I'll send you the template." > script.txt
