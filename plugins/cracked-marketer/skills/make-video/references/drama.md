# Making a drama

The path one drama took from premise to finished file on 2026-11-12: 6 frames, 5 voice lines, 8 video jobs, no retakes, 1 h 35 min, most of it the video model's queue. What makes a drama work is in [formats.md](formats.md), Drama. Prices and the hand-off are in [models.md](models.md).

## 1. The premise

The whole little story in five parts before any line is written, for the user's yes:
- **who, and where:** a room everyone has been in (a family table, a passport desk, a boss's office, a doorway);
- **the bar:** who sets it, to the hero's face, and the line that says it;
- **the turn:** the user's product doing its thing in the scene, a picture readable in a second, at about half way;
- **the payoff:** the room's faces, and who now needs whom;
- **the last line,** the hero's: two to six words, a callback or a role swap.

It passes when a stranger would retell it in one breath: "her dad says her brother just bought a house and she's still renting, then her phone on the table lights up with her deposit saved, and her brother asks how" (a budgeting app's drama). Write three premises in the user's niche and let them pick. From a reference drama, keep its structure and the job of each beat; its people, room and jokes are its own, so write them new.

## 2. The script

Structure: the bar, the flat answer, the picture, the last word. 20 to 25 s, 30 to 50 words, 6 to 10 shots.

| Beat | Seconds | What happens |
|---|---|---|
| The bar | 0 to 3 | Who and where, in a wide with the person who sets the bar in it, and the line said to the hero's face |
| It lands | 3 to 8 | The question turns to the hero; one flat line back |
| The room | 8 to 12 | A laugh, pity, a look: one or two reaction shots, no lines |
| The turn | 12 to 16 | The product's picture in its own shot, then full frame for 1 to 2 s so one line reads |
| The faces | 16 to 18 | One or two reactions; something tips over |
| The last word | 18 to 22 | The hero's close-up and the last line; then out |

The plan (SKILL.md step 3) is the shot list: each shot's seconds, framing, who's in it, its line, its start frame, and how it's made. The turn's screen is the user's real product, captured, never a mock.

## 3. The cast

One close-up portrait per speaking character, from a written look (age, hair, clothes, one prop), on the user's image model. Make the first, then each next one with the first as a reference so the look holds. Faces clearly different from each other. Every face is a character the user made: never a real person, a celebrity or someone who hasn't agreed. A character the brand reuses keeps its portrait for the next drama.

## 4. The start frames

One still per acted shot: the wide with all the portraits as references, the insert for the turn (the phone or screen from above, its screen black so the real capture goes in), and any reaction the portraits can't start. A close-up starts from its character's portrait. Name each shot's character from its start frame when writing the take's prompt, never from memory: a prompt that describes the dad over the brother's frame keeps the frame's face and loses the line.

GPT Image 2.6 held the faces and the look across all six frames on the first try (2026-11-12). Nano Banana Pro flagged every drama frame "nsfw" the same night, with references and without, charging nothing; when it refuses, switch models rather than rewording.

Show the portraits and the start frames in order (step 5's key frames) before any take is paid for.

## 5. One voice per character

One TTS voice per character for every line in every shot, one line a file, each read checked against the script word for word. Make 2 or 3 reads of a line and keep the one whose transcript matches. A clean voice per character is why the cut uses these files, not the takes' own sound.

## 6. The takes, priced and asked first

One video job per acted shot: its start frame, the line's voice as a black video in the video-reference slot, audio generation on, a locked camera, the action in one sentence, and "only [character] speaks". A shot with no line gets the action alone. List every take with its model, seconds and price, and the total with retakes, and wait for the yes to that list ([models.md](models.md), A drama's list).

Submit one job at a time and wait for it, voices too: four voice lines sent at once came back refused (429), and each video job took about 7 minutes. When a job is submitted by hand or through a chat, ask for the job's id back and poll it yourself, rather than letting the chat sit on the wait.

## 7. Check each take

- `python3 scripts/check-take.py take.mp4 --voice voice-video.mp4 --line "the line" --use <in>-<out>`: the words it says, its sound against the read, and the eyes over the part used.
- A take that says the line's words but at its own pace or later is **re-timed**, not broken: `python3 scripts/place-line.py take.mp4 voice.wav` finds where the mouth says it and places the clean line there (`vdelay`), or splits the line at its pause and fits each part (`--fit`). Re-score it; a re-timed take is fixed in the cut before anyone pays for a retake. One take that moved its line to after a slow sunglasses-off beat (1.9 s later than planned) played better than the plan: find the mouth first, then place the line.
- A take with other words, a changed face, or warped hands is redone alone.
- Look at a 4 fps strip of every take, full size: lips close on b, m and p, the face stays the same first to last.

## 8. The cut

`python3 scripts/drama-cut.py shots.json final.mp4` builds it: each take trimmed to its in and out, every shot snapped to whole frames at 24 fps (lengths rounded off frames drift the late lines off the mouths), hard cuts at 1080 × 1920, the clean voices at their places, small subtitles of each line, the song under all of it with its drop on the turn, ducked under each line, mastered to −14 LUFS. It prints the turn's place in the runtime and flags a turn outside 40 to 70%, or a last line over six words.

```json
{"song": "song.mp3", "song_drop": 41.2, "drop_on": "turn", "drop_offset": 0.3,
 "shots": [
  {"name": "bar", "src": "takes/bar.mp4", "in": 0.0, "dur": 2.85, "voice": "voices/dad-1.wav", "vdelay": 0.3, "line": "Your brother just bought a house."},
  {"name": "answer", "src": "takes/answer.mp4", "in": 0.1, "dur": 1.6, "voice": "voices/hero-1.wav", "vdelay": 0.3, "line": "Still renting."},
  {"name": "turn", "src": "build/turn.mp4", "in": 0, "dur": 2.0, "turn": true},
  {"name": "last", "src": "takes/last.mp4", "in": 0.0, "dur": 4.2, "voice": "voices/hero-2.wav", "vdelay": 2.49, "line": "I just rent."}]}
```

`vdelay` is where the line starts inside the take (place-line.py's number), `in` where the cut enters the take. The turn's shot is the user's real capture composited onto the black screen of its start frame, or the capture full frame; build it in HTML (HyperFrames) or ffmpeg before the cut.

## 9. Check, deliver, label

- `python3 scripts/check-video.py final.mp4 --format drama --script script.txt --captions final.srt --caption-text caption.txt --beats beats.json`, with a beat at the turn (`{"t": <turn time + 0.5>, "shows": "<a word on the product's screen>"}`), then the 4 fps contact sheet of the whole cut and every cut full size, then the fresh reviewer (build.md, Checks). Fix and run them all again after every fix.
- The caption carries the ask (the keyword and what it sends) and the disclosure line; the post gets the platform's AI label, since the cast and their voices are AI. The post sheet says `"ai": true, "people": "made"`.
