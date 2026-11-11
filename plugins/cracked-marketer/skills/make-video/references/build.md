# Building it

## Tools

- **HyperFrames** (HTML rendered to video, Apache-2.0): `npx skills add heygen-com/hyperframes` for its skills, then the CLI: `npx hyperframes init <dir>`, `lint`, `check --json` (layout and contrast), `snapshot --at <t,…>` (stills), `transcribe` (word times), `render --quality delivery --output final.mp4`. Write the version into the project and keep it for the whole video. Node 22+ and FFmpeg. Its hosted `compose` and `render_video` tools don't run from Claude Code; use the CLI.
- **Fonts** from Google Fonts (Inter, Geist, TikTok Sans are open-licensed) or the user's brand fonts. Never bundle a font file you can't share.
- **The user's brand:** their colours, type and logo, read from their site or Brain. Never Vamos's or anyone else's look.
- **Statics and carousels:** the same HTML, rendered to PNG with `snapshot` (or a headless browser): statics at 1080 × 1350 and 1080 × 1920, carousels at 1080 × 1350.

## Real things first

Every screen is captured from the real product (screenshots at native 2×, light mode, joined with ffmpeg), filmed off the screen with a phone, or rebuilt from real components. People are their real public profile captures (avatar, handle, follower line), never drawn icons. A reference's media links die within days: download what you need when you find it.

## Key frames (the user's gate)

Build the HTML, snapshot one still per beat at its key moment (with its caption and the line it sits on), and show them in order. One round of the user's notes; fix what has a right answer, list the taste for them. Render only frames they passed.

## Captions and words

- Every spoken word is captioned exactly as said, showing at its midpoint; keep the word times even when the screen groups words.
- One style throughout. Never the spoken line twice on screen (a title on screen is the caption).
- Contrast 4.5:1 (3:1 at 58 px and up); a boxed caption fixes a busy ground.
- 48 px of ground inside any card around text.

## Cut and sound

- The voice starts 0.25 s in. A cut or caption lands 0.2 to 0.3 s before its word, on the song's beat.
- One thing moves per screen; smooth over snappy; stagger reveals.
- A real song the user has the rights to, or none; the bed about 16 dB under the voice at one level, no ducking. Effects only where a hand acts or a result lands, measured against the loudest 50 ms of music under them.
- No model can judge a mix: measure it, then the user listens.
- Master to −14 LUFS, −1.5 dB true peak.

## Checks before anyone watches it

1. `npx hyperframes check --json`: fix every error (layout, overlap, contrast).
2. `python3 scripts/check-video.py final.mp4 --format <format> --voice voice.wav --words words.json --captions captions.srt --caption-text caption.txt`: size, length cap, loudness, true peak, the lead-in, the tail, every word captioned, no link in the caption, frozen stretches. Fix every DEFECT; FLAGs are for a look.
3. Look at it yourself: a 4 fps strip around every cut (`ffmpeg -ss <t> -t 2 -i final.mp4 -vf "fps=4,scale=270:-1,tile=8x1" -frames:v 1 strip-<t>.png`), full size. A defect seen at one moment gets looked for across the whole video.
4. A fresh subagent that didn't build it, shown the strips and the script, not your notes: does each beat show what its line says, and does anything read as drawn or fake? Where the host has no subagents, skip it and say so.

## Deliver

One final in its aspect ratio with its exact file name, the post caption (no link in it), the disclosure line when it holds AI footage or is paid, and the AI label to switch on at upload. Then the numbers 2 and 7 days after it posts, through `/cracked-marketer:content-log`.
