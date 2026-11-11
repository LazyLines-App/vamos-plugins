# The formats

What makes each one work, measured on winners in short-form (other creators' posts, counted frame by frame), and how it's made on the user's own tools. Lengths are caps, not targets. Every format: 9:16 at 1080 × 1920 (statics 1080 × 1350 and 1080 × 1920, carousels 1080 × 1350), a real song the user has the rights to or none, nothing in Instagram's top 220 px, bottom 420 px or right 130 px.

## Narrated motion graphics

One voice tells the viewer something they didn't know, and every idea it names lands as a new picture they can read with the sound off. No face, no live footage. Up to 60 s.

- A new picture per idea, with something landing inside it every 0.5 to 1 s (median scene about 4 s).
- Frame 0 shows the premise: the headline, the typed ask, or one subject on a flat colour. A named place gets the signs a stranger knows on sight.
- The real outputs big and early, one at a time; one number readable on each proof.
- At most three text layers: a headline per scene, a counter, the narration captioned word by word low in the frame.
- Narrators run 3.0 to 4.5 words a second, wall to wall, over a bed with a hit on each cut.
- Made with: the voice (their TTS), scenes in HTML (HyperFrames), the real screens captured.

## Voice over a demo

The script read over the product really doing the thing. Up to 50 s.

- The tool is on screen from the first frame; the first result by 7 s (by 2 s in a screen recording).
- The screen moves inside the shot about 7 times every 10 s: typing, a cursor, a count-up, a scroll. A camera move is a hard punch-in or a pan that shows something new; a slow 2 to 5% push reads as a slide.
- A screen that must be read goes full frame, zoomed to its one line. Never a paragraph on screen.
- The payoff reads in one second: one number over the real screen, or the output full frame.
- Captions 1 to 3 words a phrase, one style throughout, one key noun a phrase in a second colour.
- Made with: their screens captured at native 2× in light mode (screenshots joined, never a 368-pixel browser recording), or a phone filming the laptop.

## Silent hook demo

A person reacts to their laptop under one line, then their real screen does the thing, touched step by step, until a result they can read. No voice, a song from frame 0. 9 to 52 s, median 23.

- The opening is a real person in a real room with one feeling and no words, held about 3.5 s. Over the same demo, one opening did 181,933 views and another 1,620: the opening and its line are the variable, the demo is the asset.
- The line is a feeling, a quoted complaint or a short story. Product claims lose (13 of 30 losers, 5 of 37 winners).
- The screen is an object in a room, filmed by a phone (10 of 11 winners), each shot 1.2 to 2.5 s with one target something touches.
- Native captions: one line a shot, 2 to 6 words; the longest card among 1,117 winners was 13 words.
- The payoff is one big thing, close and held 2 to 6 s, at 74 to 89% of the runtime.
- Made with: the user films their own reaction (or a teammate does) and films the demo off the screen with their phone.

### One demo, many hooks

"Make 10 videos from this recording": the demo stays the same and only the opening and its line change, so the views show which hook works.

- **They send** one demo, filmed off their screen by their phone and ending on the payoff, and 3 to 5 openings they film themselves, about 3 s each, one feeling, no words. Their own labelled AI character can play the openings; that's paid generation, so it goes on the priced list first ([models.md](models.md)).
- **Ten lines,** each from a proven hook in their niche: the board's Hooks tab, or one Vamos ask when it has fewer than ten: "For [brand] in [niche], on [platforms]: the 30 hooks that beat their creators' usual the most in the last 60 days, silent hook demos first, then any format in my niche. Each one's first line word for word, the text on screen in the first frame, what's shown, views, the multiple, the link and the date." Add those rows to the Hooks tab. Rewrite each as a feeling, a quoted complaint or a short story: the sentence and its pull stay, the topic becomes theirs. Product claims lose: "I spent $412 on coffee in October and had no idea" is a story; "Track every coffee automatically" is a claim.
- **The plan** is one table in the reply, a row a cut: the line, the hook it came from with its link and multiple, the opening it sits on. No voice and no stills round; their yes to the table is the go.
- **Render** free with `scripts/hook-cuts.py plan.json`: each cut is the opening with its line from frame 0, a hard cut to the same demo, the payoff and the keyword card, in a file named by its line. It checks every cut in code (size, length, the line on screen from frame 0, the hard cut, loudness) and prints PASS or DEFECT, then a TABLE of all ten lines (each with its source's `from`, link and multiple) and the NEXT step: paste both into the reply as printed.
- **Record, then read the winner:** right after the render, put each cut on the board's Hooks tab as its own row (its line, source and multiple) with Result "test: same demo, the hook changes"; a board kept as a Brain file takes them all in one `save_brain_file` with the whole board. Recording is part of the test, the way the hooks skill adds its rows, so it needs no extra yes: without the rows the test can't be read. The reply says the rows went on with that Result (or that the save didn't come back), and the recap's Next is the loop: "`/cracked-marketer:content-log` once the posts are 3 days old puts each cut's multiple in its row; the next ten lines start from the winner."

## AI UGC (a presenter)

A person talks to camera while, above them or full frame, the thing they describe happens on a real screen. Up to 50 s. The presenter is the user's own character, made from their own photo or a made one. It's labelled as AI, so it presents and never tells a story or a result as its own ("I paid off my card in a year" is a fake testimonial; "you could pay it off in a year" is fine).

- The proof on top (40 to 70% of the height), the caption on the seam, the face below.
- The face is one calm, unbroken take per line; cut at sentence ends. It's on camera for the hook, each section's opening words and the ask; the rest plays the proof full frame under its voice.
- Voice first, presenter last: the whole cut is agreed with the voice and a still of the face before any paid take ([models.md](models.md), the presenter chain).
- Made with: their TTS voice, their image and video generator for the face, their captured screens.

## Static ad

One image in Meta's Feed (4:5) and Stories and Reels (9:16).

- The words in the image are the hook: 4 to 12 words in the top third. The headline field carries the offer, 27 characters or fewer.
- The product's real output is the hero: a score, a ranked table, a real post with its numbers. A number as the hero, a real capture of a screen people scroll, or a phone photo of the real screen with a marker on it stop the thumb; a logo on a floating card is the category default to leave.
- Ads that look AI-made do worse. A new concept is a new picture, never new text on the same picture.
- Made with: HTML rendered to PNG at both sizes, the real material captured.

## Carousel

A still that's worth stopping for, then one change a slide. 2 to 13 slides.

- One frame, one change per slide: the same headline place and margins on every slide.
- The cover has one hero that reads at thumbnail size (type 200 to 330 px on 1080 wide, or one picture).
- Reading text 27 px or more; text inside screenshots is recognised, not read.
- A slide worth saving; the last slide has one job (a keyword as the biggest type, a follow, or "your turn").
- Made with: HTML rendered to PNG. Our own carousels' reach is unproven, so it's the user's call, not a default.

## Out of scope

Face swaps onto someone else's footage, an AI version of a real person's face or voice without that person's yes, and copying a video line for line. Offer the same structure made with the user's own footage or character.
