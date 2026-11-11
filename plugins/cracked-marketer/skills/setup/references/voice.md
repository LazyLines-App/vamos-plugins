# The voice

A voice is built from how someone talks on camera, so it reads their own talking videos: 30 to 40 from the last 6 months, partner posts and reposts left out. A website or captions describe the brand; they don't say how the person speaks.

## What the guide holds

Vamos writes the guide on the Voice page. Check that the rebuilt one has each of these, with real lines quoted, and write what's missing from the transcripts you hold into step 5's voice guide message:
- **Openers:** 2 to 4 shapes, each with its real line, and their 10 best real first lines word for word, each with its multiple.
- **How a video moves:** up to 3 spoken formats, their beats and the words they move on with ("so", "and here's the kicker").
- **Proof and stories:** how they back a point (numbers, screenshots, names) and how they tell a story.
- **Words:** fillers with their job ("right?" as a paragraph break), slang, swearing, UK or US spelling.
- **Humour:** its kind and how often. "None" is a real answer, and then no jokes get written.
- **Closers:** the closing lines word for word, and what they ask for.
- **Signature phrases:** up to 9, each with how many times it was said.
- **Never says:** what the niche and AI writing default to that they don't ("game-changer", "here's the thing"), each with a swap. Tells they do use stay.
- **On screen:** text casing, length and emoji, when text appears, and how they film (talking head, walk-and-talk, voice over B-roll).

About 25 to 40 real lines in all. More turns the guide into a template the writer copies.

## The numbers

Count them in code, never by eye: `python3 scripts/textstats.py profile transcripts.json`, where each item is `{"text", "seconds"}` from the rows. It gives words per second, sentence length (median and p90), the share of sentences of 5 words or fewer, questions, "you" and "I" per 100 words, contractions and tells. Note how many transcripts it counted (the answer carries up to 10). Scripts use words per second × the target seconds as their length.

## Voice examples

Five whole transcripts, chosen for spread: different formats, hook types and lengths, one top performer and one typical post, all from the last 6 months. Each is labelled with its format, seconds and multiple. Five is enough: more examples raise the chance a script copies one.

## The held-out video and the test

Keep one typical talking video out of the examples. Write a 20-second script on its idea, in their voice, at their words per second, opening on one of their real opener shapes, with any "I" fact taken from Things you've said or left as `[your …]`. Show the two side by side, then ask "Which lines aren't you?". Each line they point at is a voice correction: send it to Vamos ("I never say X. I'd say Y.") so every later script and every Vamos chat has it.

## When there's too little speech

Under 10 talking videos: say so, build from what there is, and mark the guide thin in Vamos settings. Offer two ways to fill it: an account they want to sound like, or a few transcripts or voice notes they paste.
