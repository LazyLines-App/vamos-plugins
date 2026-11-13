---
name: "make-video"
description: "Makes the finished video, static ad or carousel from an approved script, idea or reference video, on your own tools: narrated motion graphics, an animated explainer, a voice over a product demo, AI UGC, a silent hook demo, a drama acted by characters you made. Picks the format, prices every paid shot and asks first, shows key frames, builds it in code and checks it before you post. Use for \"make this into a video\", \"make a motion graphics video\", \"an explainer video for our app\", \"a narrated video from this script\", \"a demo video with a voiceover\", \"make an AI UGC ad\", \"make a drama\", \"a skit with AI actors\", \"make the next one like this reel\", \"make 10 videos from one recording\", \"test hooks on the same demo\", \"can these takes go in the cut\", or a static or carousel to make."
---

# Make the video

**The job:** an approved script, idea or reference turned into one finished file the user can post, made on their own tools. Vamos researches and writes; it never renders. Claude plans, builds the HTML, drives the user's own generator and checks the result in code. Writing a new script is `/cracked-marketer:script`; ad concepts are `/cracked-marketer:winning-ad-ideas`.

The formats and what makes each work: [references/formats.md](references/formats.md). Models, prices and the presenter chain: [references/models.md](references/models.md). Tools, frames, captions, sound and the checks: [references/build.md](references/build.md). A drama, premise to cut: [references/drama.md](references/drama.md).

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas need it, and so do hooks and scripts while its `voice` is false, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** One Vamos chat per job (`create_chat`); follow-ups go in it. Add `include_data: true` when you need the rows. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50 posts (30 ads, creators or formats), so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file`, always as its whole text, so read one first to add to it. Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 7 days old (views still climb before that), leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). A younger post that already beats it shows as "N× so far"; one that doesn't is too early to judge. Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer. Next is the step this skill names, and when it names a choice, offer each. When it can run now, offer it as a question and, on their yes, run it yourself, so they never need to remember a command; when it waits on them or on time (filming, a post's first week), say what and when.

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Board:** [its link, when there is one] · **Next:** [what it does, in eight words] (`/cracked-marketer:[skill]`). Shall I?
<!-- /shared -->

## Steps

**1. Take what they gave.** A script or idea pasted, or named from the board, goes as it is. A reference video gets one Vamos ask, naming the brand and niche: "Watch [link] and give its beats with timings: what's shown, what's on screen and what's said, the hook word for word, its format and length. For [brand], [niche]. Don't save anything." From a reference, keep its hook sentence with the topic swapped ("I am never using Shopify again" becomes "I'm never buying drugstore retinol again"), and what each beat does and when it lands; its other lines, scenes, jokes and examples are its own, so write each one new from the new topic.

**2. Pick the format** from [formats.md](references/formats.md): the one the idea names; otherwise the cheapest that fits the job, since most need no paid generation (narrated motion graphics, a voice over a demo, a static, a carousel, a hook demo with their own opening, then AI UGC and the drama). Many videos from one screen recording is the silent hook demo's [one demo, many hooks](references/formats.md) test. A face swap onto someone else's footage, or an AI version of a real person who hasn't agreed, is out: say so in a line and offer the same structure with their own footage or their own labelled character. A drama's cast are characters the user makes in step 5.

**3. The plan, one message, then wait for their go.** Beat by beat: the line, what the viewer sees, and how it's made (captured, filmed by them, built in HTML, generated). What the viewer sees is the thing the line names, readable at the word that names it: under "then writes yours", the written hook, not the chat while it loads. Then what they supply (screens, a song they have the rights to, keys); every paid step as the priced list in [models.md](references/models.md), one line a clip with its model, seconds and price, then the total; the AI label and disclosure line when it holds an AI face; and what comes next, with the checks it passes before they watch it. For example:

> **Format:** a voice over a demo, 35 s, no face. Every line is something the app does on screen, so the proof carries it.
> | Beat | Line | Seen | Made by |
> |---|---|---|---|
> | 0:00 | "Most budgets die in week two." | Your app's empty month, a cursor on day 14 | Captured, your app |
> | 0:04 | "Mine lives in my lock screen." | The widget filling as a coffee is logged | Captured, your phone |
> | … | | | |
> **You send:** a login I can capture, or your screenshots; a song you have the rights to, or none.
> **Paid:** the voice on your ElevenLabs (about 500 characters). Nothing else is paid.
> **Next:** a still of each beat for your OK, then the build, checked in code before you watch it: loudness at −14 LUFS, every caption against the voice, the length.
> Yes to this and its price, and I'll make the voice.

A drama's plan comes in two messages: its premise, the whole story in five parts, for their pick, then the shot list with the cast and the priced takes ([drama.md](references/drama.md), 1 and 2).

The plan's yes covers the free steps, the voice and the listed images. Paid video takes get their own yes, asked with the cut they go into (step 6).

**4. Capture the real things** ([build.md](references/build.md), Real things first). Make the voice now when there is one, so the frames and the cut follow its timing.

**5. Key frames for their OK,** before any cut is built: one still per beat, in order, taken at the word where its line names its thing, with its caption. For a drama: the cast portraits, then each shot's start frame. One round of notes.

**6. Build, sound, and the paid takes.** Build the cut from the frames they passed, with the voice and, where a face goes, its still. When there are paid takes, show that cut with their priced list and, when the user submits them by hand, the hand-off ([models.md](references/models.md)); the takes run on the yes to it. A paid generation goes only on a yes to its priced list, even after an earlier "go ahead". Each take that comes back goes through `scripts/check-take.py` before it goes in the cut. A drama's takes go one job at a time, each line placed where its take says it (`scripts/place-line.py`), and its cut is `scripts/drama-cut.py` ([drama.md](references/drama.md), 6 to 8).

**7. Check before they watch it** ([build.md](references/build.md), Checks): `hyperframes check`, then `scripts/check-video.py` with the script and the beats until it prints PASS, then its beats sheet and a 4 fps strip around every cut looked at full size, then a fresh reviewer. Fix every defect, then run every check again on the new file; a taste call is one line for them.

**8. Deliver** one named file, the post caption with no link in it, the disclosure line, and the AI label to switch on at upload when it holds AI footage. Beside the file, write its post sheet, `<file>.post.json`, so `/cracked-marketer:post` labels it right:
> {"caption": "…", "disclosure": "Made with AI.", "ai": true, "people": "made", "promotes": "own", "title": "…", "format": "drama"}

`ai` is true when any face, voice or footage in it was generated. `people` is none, filmed (real people the user filmed, who agreed), made (characters the user made) or agreed (an AI version of the user, or of someone who agreed in writing). `promotes` is own for the user's own product, partner with `partner` set for a paid one, none otherwise; `title` is for YouTube. Put the file's path in its board row's File column. Next is `/cracked-marketer:post` to schedule it on their accounts, then `/cracked-marketer:content-log` once it has run 2 and 7 days.

**Check before the recap:** nothing paid was generated without a yes to its priced list; from a reference, each line but the hook's sentence set beside the reference's line at that beat shares no person, scene, time of day or joke with it; every screen and person on it is real or labelled; check-video.py printed PASS on the delivered file, after the last fix; its post sheet says `"ai": true` when anything in it was generated.

Vamos is needed for a reference's watch, the board, and the proven hooks a hook test starts from; a pasted script is made without it.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Cracked marketer plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
