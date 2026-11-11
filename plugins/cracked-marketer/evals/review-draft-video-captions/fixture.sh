#!/bin/bash
# Dana's brief (the brief skill's example brief) in the briefs doc, and her draft: a synthetic 18 s video made here
# with macOS `say` and ffmpeg (1080x1920, burned-in captions, a kitchen scene to 4.6 s, then the Potly app screen),
# plus her captions file. What it gets wrong, on purpose: Potly first shows at 4.6 s (the brief says by 3 s) and the
# star line is changed ("I'm paid" said as "I get paid", "to spend" left out). The hook is word for word.
# Needs macOS (say, /System/Library/Fonts/Helvetica.ttc) and ffmpeg with drawtext.
set -e
mkdir -p vamos drafts
cat > vamos/briefs.md <<'BRIEF'
# Briefs: Potly
## Dana · Payday in nine minutes · due Fri 20 Nov

**1. The video:** you on payday, splitting your paycheck in Potly before you spend a cent, for people paid every two weeks who are broke by day ten. It's yours because your payday vlogs already catch the moment the money lands.

**2. Your hook.** Say it to camera and put the same words on screen from the first frame. Film each one; we pick in the edit.
- "My paycheck lands, and nine minutes later it's gone. On purpose."
- "This is the only thing I do on payday."
- "Day ten and I'm not broke. Here's why." Only if it's true for you.

**3. What you say,** in your own words. ★ = say it as written.
- The money lands and you open Potly right there, before coffee, before Amazon.
- You drag it into three pots: bills, fun money, and the one you don't touch. Say why the fun pot matters to you.
- ★ "Potly moves it the second I'm paid, so the rest is mine to spend."

**4. What to show.** The bank notification on your phone, then Potly open by 3 s. Film your phone with a second phone, screen brightness up, no glare. The path: Home, then Payday, then drag each pot; hold each screen for 2 seconds so it reads. End on the three pot totals, then your face. Use test numbers or blur your real balance.

**5. Watch these.**
- https://www.tiktok.com/@example/video/1 takes the phone-in-hand opening; skip its music.
- https://www.tiktok.com/@example/video/2 shows how fast she gets from the notification to the app.

**6. Do and don't.**
- Do: film your real payday routine, with the app as one step in it, not a list of features.
- Do: give the pots your own names.
- Don't: promise savings amounts or say it fixes anyone's debt.
- Disclosure: turn on the paid-partnership label and put #ad in the caption.

**7. What you send.** Due Fri 20 Nov at [upload link]: the raw take (no music, captions or filters) and a captioned draft, 9:16 at 1080 × 1920. Fixed: the ★ line, the app on screen by 3 s, the disclosure. Yours: the setting, the order of the first two beats, your words. Rights and pay are as in your agreement with Potly. We approve it when the hook is word for word, the app screen is readable, and the ★ line is in.
BRIEF
cd drafts
W=$(mktemp -d)
LINES=(
  "My paycheck lands, and nine minutes later it's gone. On purpose."
  "I drag it into three pots before I even make coffee."
  "Bills, fun money, and the one I don't touch."
  "Potly moves it the second I get paid, so the rest is mine."
  "Day ten and I'm still not broke."
)
[ -n "$HOOK" ] && LINES[0]="$HOOK"
t=0.4
: > "$W/list.txt"
: > dana-draft.srt
ffmpeg -v error -f lavfi -i anullsrc=r=22050:cl=mono -t 0.4 -c:a pcm_s16le "$W/gap0.wav"
echo "file '$W/gap0.wav'" >> "$W/list.txt"
i=0
DRAW=""
for L in "${LINES[@]}"; do
  i=$((i+1))
  say -v Samantha -r 175 -o "$W/l$i.aiff" "$L"
  ffmpeg -v error -i "$W/l$i.aiff" -ar 22050 -ac 1 -c:a pcm_s16le "$W/l$i.wav"
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/l$i.wav")
  ffmpeg -v error -f lavfi -i anullsrc=r=22050:cl=mono -t 0.5 -c:a pcm_s16le "$W/g$i.wav"
  echo "file '$W/l$i.wav'" >> "$W/list.txt"; echo "file '$W/g$i.wav'" >> "$W/list.txt"
  end=$(python3 -c "print(round($t+$d,2))")
  python3 - "$i" "$t" "$end" "$L" >> dana-draft.srt <<'PY'
import sys
i, a, b, text = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
f = lambda x: '%02d:%02d:%02d,%03d' % (x // 3600, x % 3600 // 60, int(x % 60), round((x % 1) * 1000))
print(i); print(f(a) + ' --> ' + f(b)); print(text); print()
PY
  python3 -c "import sys;w=sys.argv[1].split();h=(len(w)+1)//2;open(sys.argv[2],'w').write(' '.join(w[:h])+chr(10)+' '.join(w[h:]))" "$L" "$W/c$i.txt"
  DRAW="$DRAW,drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile=$W/c$i.txt:fontsize=48:line_spacing=12:fontcolor=white:box=1:boxcolor=black@0.75:boxborderw=14:x=(w-text_w)/2:y=1380:enable='between(t,$t,$end)'"
  t=$(python3 -c "print(round($end+0.5,2))")
done
ffmpeg -v error -f concat -safe 0 -i "$W/list.txt" -c:a pcm_s16le "$W/voice.wav"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$W/voice.wav")
F=/System/Library/Fonts/Helvetica.ttc
python3 -c "import sys;w=sys.argv[1].split();h=(len(w)+1)//2;open(sys.argv[2],'w').write(' '.join(w[:h])+chr(10)+' '.join(w[h:]))" "${TOP:-${LINES[0]}}" "$W/top.txt"
# 0 to 4.6 s: the creator in her kitchen; from 4.6 s: the Potly app screen.
SCENE="drawbox=x=0:y=0:w=iw:h=ih:color=0x2f4f4f@1:t=fill:enable='lt(t,4.6)',drawtext=fontfile=$F:text='[Dana at her kitchen counter\, phone in hand]':fontsize=40:fontcolor=white@0.8:x=(w-text_w)/2:y=600:enable='lt(t,4.6)',drawtext=fontfile=$F:textfile=$W/top.txt:fontsize=60:line_spacing=14:fontcolor=white:x=(w-text_w)/2:y=260:enable='lt(t,4.6)'"
APP="drawbox=x=140:y=260:w=800:h=1300:color=white@1:t=fill:enable='gte(t,4.6)',drawtext=fontfile=$F:text='Potly':fontsize=90:fontcolor=0x1a7f5a:x=200:y=320:enable='gte(t,4.6)',drawtext=fontfile=$F:text='Payday · \$2\,140 landed':fontsize=44:fontcolor=black:x=200:y=460:enable='gte(t,4.6)',drawtext=fontfile=$F:text='Bills  \$1\,250':fontsize=52:fontcolor=black:x=200:y=620:enable='gte(t,4.6)',drawtext=fontfile=$F:text='Fun money  \$390':fontsize=52:fontcolor=black:x=200:y=760:enable='gte(t,4.6)',drawtext=fontfile=$F:text='Do not touch  \$500':fontsize=52:fontcolor=black:x=200:y=900:enable='gte(t,4.6)'"
ffmpeg -v error -y -f lavfi -i "color=c=0x101418:s=1080x1920:r=30:d=$dur" -i "$W/voice.wav" \
  -vf "$SCENE,$APP$DRAW" -c:v libx264 -preset veryfast -crf 30 -pix_fmt yuv420p -c:a aac -b:a 64k -shortest dana-draft.mp4
rm -rf "$W"
true
