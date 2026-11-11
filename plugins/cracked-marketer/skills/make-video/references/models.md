# Models, prices and the presenter chain

## Which model for each shot (prices read 2026-11-10)

Prices move weekly. The user's tool's own quote wins: when their generator connector or CLI can price a job (a quote, a cost estimate, a credits-per-second table), ask it first and show its number with the date. Use this table only when it can't, and say the price is from this date.

| Shot | Model (where) | Price | Notes |
|---|---|---|---|
| A still: a start frame, a product shot, a scene | Nano Banana Pro (Kie, Higgsfield, fal) | about $0.09 an image | 2K costs the same. Seedream 5.0 Pro is about 2.5 Higgsfield credits |
| A presenter talking, lip-synced to a voice | Seedance 2.5, 720p (Higgsfield) | about 7 credits a second ($0.32 to $0.47) | 480p is about 3 credits a second: draft there, finish at 720p |
| The same, without a start frame | Seedance 720p (Kie) | about $0.315 a second | Kie's route can't take a start frame with reference media |
| A short 1080p clip | Seedance 2.0 1080p (Higgsfield) | 180 credits for 15 s | |
| The voice | ElevenLabs (their key), or another TTS | their plan's characters | Cheap next to video |

Higgsfield sold 1,200 credits for $59 on its CLI plan (about $0.05 a credit). A 15 s presenter take at 720p is about 105 credits, so about $5.

## The priced list

Before any paid video generation, show one list and wait for the user's yes to it. "Go ahead" before they've seen the list is not a yes to it. Images are cheap: list them, and make them on a yes to the list. Example:

> Paid, on your Higgsfield (prices from its quote, 11 Nov):
> 1. Start frame, Nano Banana Pro, 1 image: about $0.09
> 2. Presenter, Seedance 2.5 720p, the hook (4 s): 28 credits
> 3. Presenter, the ask (3 s): 21 credits
> Total about 49 credits (about $2.45) of your 300. Everything else is your voice and HTML.
> Make these? I'll make the voice and the cut first, so you'll see the whole video with a still of her before the presenter takes run.

Draft at the cheaper size when the user wants to see motion first; one take per line, and redo a broken moment alone, never the whole video.

## The presenter chain

1. **The face** starts from the user's own photo or a character they made, on a resting, closed-mouth frame. Never a real person who hasn't agreed, and never another creator's footage.
2. **The voice first,** on their TTS: spell the brand the way it sounds, make 2 or 3 reads and keep the one whose transcript matches the script word for word. Don't push it through effects; a cleaned-up TTS read beats a processed one.
3. **The cut** is built and agreed with that voice and a still of the face.
4. **The takes,** on the yes to the priced list: the voice goes to the model as a black video carrying the clean voice (an MP3 gets re-voiced), with a 0.25 s lead. A calm prompt; never describe a phone in the hand. Past about 20 s a take drifts: split at a line end.
5. **Check each take:** every word matches, the lips close on b, m and p, the face is the same first to last, no warping hands or teeth, and the cut lands after a word's end on a closed mouth. A take that fails is redone alone.
6. **The label:** the post carries the platform's AI label and a disclosure line.
