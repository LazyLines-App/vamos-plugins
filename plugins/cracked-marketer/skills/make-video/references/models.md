# Models, prices and the presenter chain

## Which model for each shot (prices read 2026-11-10)

Prices move weekly. The user's tool's own quote wins: when their generator connector or CLI can price a job (a quote, a cost estimate, a credits-per-second table), ask it first and show its number with the date. Use this table only when it can't, say the price is from this date, and when they submit by hand, the credits on their generate button are the quote (the hand-off below).

| Shot | Model (where) | Price | Notes |
|---|---|---|---|
| A still: a start frame, a product shot, a scene | Nano Banana Pro (Kie, Higgsfield, fal) | about $0.09 an image | 2K costs the same. Seedream 5.0 Pro is about 2.5 Higgsfield credits |
| A presenter talking, lip-synced to a voice | Seedance 2.5, 720p (Higgsfield) | about 7 credits a second ($0.32 to $0.47) | 480p is about 3 credits a second: draft there, finish at 720p |
| The same, without a start frame | Seedance 720p (Kie) | about $0.315 a second | Kie's route can't take a start frame with reference media |
| A short 1080p clip | Seedance 2.0 1080p (Higgsfield) | 180 credits for 15 s | |
| The voice | ElevenLabs (their key), or another TTS | their plan's characters | Cheap next to video |
| A drama's cast and start frames | GPT Image 2.6 (Higgsfield) | about 1 credit an image (read 2026-11-12) | Held six frames' faces on the first try; Nano Banana Pro refused every drama frame as "nsfw" that night |
| A drama's acted take, lip-synced | Seedance 2.5 (Higgsfield), 480p / 720p / 1080p | about 3 / 7 / 16 credits a second (read 2026-11-12) | One job at a time, about 7 minutes each on 11-12 |

Higgsfield sold 1,200 credits for $59 on its CLI plan (about $0.05 a credit). A 15 s presenter take at 720p is about 105 credits, so about $5.

## The priced list

Before any paid video generation, show one list and wait for the user's yes to it. "Go ahead" before they've seen the list is not a yes to it. Images are cheap: list them, and make them on a yes to the list. Example:

> Paid, on your Higgsfield (prices from its quote, 11 Nov):
> 1. Start frame, Nano Banana Pro, 1 image: about $0.09
> 2. Presenter, Seedance 2.5 720p, the hook (4 s): 28 credits
> 3. Presenter, the ask (3 s): 21 credits
> Total about 49 credits (about $2.45) of your 300. Everything else is your voice and HTML.
> These run on your yes once you've seen the whole video with a still of her: I'll make the voice and the cut first.

Draft at the cheaper size when the user wants to see motion first; one take per line, and redo a broken moment alone, never the whole video. The list goes to them with the cut, built with the voice and a still of the face (SKILL.md step 6), so they say yes to the takes having seen what they go into.

## A drama's list

A 22 s drama is about 7 acted takes of 4 to 5 s, about 29 s of video. Price each take, then add 30% for retakes (about one take in three re-times or re-voices its line, and a re-timed one is fixed in the cut for free):

> Paid, on your Higgsfield (prices from its quote, 12 Nov):
> 1. Cast and start frames, GPT Image 2.6, 6 images: about 6 credits
> 2. Takes, Seedance 2.5 480p, 7 shots, 29 s: 87 credits
> 3. Retakes, up to 30%: up to 26 credits
> Total up to about 120 credits (about $6) of your 1,200. At 720p the takes are 203 credits, about 270 in all (about $13).
> The frames come first for your OK; the takes run on your yes once you've seen them with the voices.

## The hand-off, when the user submits the takes

With no generator connected, or when they'd rather press the button, give each take as steps they follow in order. On Higgsfield with Seedance 2.5:

1. Video, Seedance 2.5, **omni reference** mode, 9:16, the size on the list.
2. The start image in the **start frame** slot.
3. For a talking take, the voice video (the black video carrying the clean read) in the **video reference** slot, never as an audio reference: the lips follow a video reference.
4. **Audio generation on**, or the take comes back silent and the lips follow nothing.
5. Duration: the line's length plus the 0.25 s lead, rounded up to whole seconds, and 4 s at the least; the cut uses only the part it needs.
6. The prompt, pasted word for word.
7. Read the credits on the generate button before pressing it; if it's more than the list said, stop and tell me.
8. Download the MP4 with its sound and save it in this project as `takes/take-<line>.mp4` (`takes/take-hook.mp4`), then tell me. I check it before it goes in the cut.

## The presenter chain

1. **The face** starts from the user's own photo or a character they made, on a resting, closed-mouth frame. Never a real person who hasn't agreed, and never another creator's footage.
2. **The voice first,** on their TTS: spell the brand the way it sounds, make 2 or 3 reads and keep the one whose transcript matches the script word for word. Don't push it through effects; a cleaned-up TTS read beats a processed one.
3. **The cut** is built and agreed with that voice and a still of the face.
4. **The takes,** on the yes to the priced list: the voice goes to the model as a black video carrying the clean voice (an MP3 gets re-voiced), with a 0.25 s lead. Start from a prompt below; never describe a phone in the hand. Past about 20 s a take drifts: split at a line end.
5. **Check each take** in code first: `python3 scripts/check-take.py take.mp4 --voice voice-video.mp4 --line "the line" --use 0-3.0`. It fails a take whose sound is no longer the read (about one take in three comes back re-voiced: its own voice, faster, a word added), a word that differs from the line, and eyes shut or lowered over the part used or on the frame the cut lands on. Then look at a 4 fps strip: the lips close on b, m and p, the face is the same first to last, no warping hands or teeth, the cut lands after a word's end on a closed mouth, and the face reads as the line's feeling at phone size. A take that fails is redone alone; a re-voiced take's sound is never kept or patched.
6. **The label:** the post carries the platform's AI label and a disclosure line.

## Prompts that worked (Seedance 2.5, November 2026)

Each held the start image's face and room. Change the person, the room and the feeling; keep the rest.

- **A presenter talking, lip-synced to the voice video:** "A calm man talks straight to camera in a softly lit apartment, speaking the words in the audio with natural lip-sync. Small, relaxed head and eyebrow movement, shoulders loose, his hands stay still. Locked camera, the framing and background don't change. Mouth closed at the start and the end." One take kept the read exactly, face steady, hands still; the next came back re-voiced, 17% faster with a word added. These lines hold the read better: "He speaks with the exact voice, pace and rhythm of the audio in Video 1. Video 1 is audio only; never show its black picture. He says these lines in order, each once: [lines]. After the last word he stops talking and closes his mouth." Even with them, check every take's sound.
- **A silent reaction opening:** "Locked camera, a young man sits at a desk with a laptop in front of him, soft warm window light. He looks into the lens with a flat, deadpan expression. He holds the flat stare, slowly raises one eyebrow a few millimetres, and gives one slow blink. Mouth stays closed the whole time. No talking, no phone, no text, no other people. Same face, same grey t-shirt, same room." Eyes open, mouth closed, the same face for 2.8 s; then the blink it asks for shut the eyes, so cut before it or leave the blink out. The eyebrow was too small to read at phone size: ask for one move big enough to see.
- **What missed:** "his eyes drop to the laptop screen, he lets out a tired slow blink." The eyes stayed down or shut for 2.4 s and the face read as asleep, not tired. Ask for the feeling with the eyes on the lens; leave out looks down and slow blinks.
