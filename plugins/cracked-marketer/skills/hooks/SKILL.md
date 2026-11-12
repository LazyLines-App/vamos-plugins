---
name: "hooks"
description: "Writes the first line of a video, carousel or ad, built from real hooks that beat their creators' usual in that format, niche and kind of product, and from the opening lines of the Meta ads your category keeps running. Also judges and fixes a hook you wrote. Use for any hook, opening line, cover or first frame."
---

# Hooks

**The job:** a first line that stops a stranger, for this idea in this format, in the user's voice, built from hooks that are working now. [references/hooks.md](references/hooks.md) holds the craft; read it before writing.

Needs the idea and the format: take them from the board, the formats page or the user, and ask in one line for whichever is missing. A hook the user wrote is the idea.

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas need it, and so do hooks and scripts while its `voice` is false, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** One Vamos chat per job (`create_chat`); follow-ups go in it. Add `include_data: true` when you need the rows. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50 posts (30 ads, creators or formats), so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file`, always as its whole text, so read one first to add to it. Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 3 days old, leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer:

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/cracked-marketer:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**1. Load, free.** `get_workspace`, then its `file` reads: Voice guide, Things you've said, What works for me, Vamos settings, and the board when it's a Brain file. With a voice but no Vamos settings, keep the hooks in the chat and suggest `/cracked-marketer:setup` in one line for the board.

From the board, take the idea's row and the Hooks tab: Hook, On screen, Format, Niche, Shape, Source (link, views, multiple, date read), Added, Result. The Hooks tab is the user's hook database.

**2. Proven hooks.** When the Hooks tab has 10 or more proven hooks (Source a post, not an idea) from the last 14 days in their niche, write from those and spend nothing. Otherwise ask Vamos once, with `include_data: true`:
> For [brand], which sells [what they sell] in [niche], on [platforms]: the 30 most-viewed hooks of the last 90 days that beat their creator's usual, from [format] posts made for [their buyer] in my niche or any niche that sells to the same buyer, then any format in my niche. Rank by views and give each one's multiple. Leave out paid partnerships, and give only the posts' own first lines, none written for me. Give each one: the first line word for word, the text on screen in the first frame, what's shown, the format, the niche, views, the multiple, the link and the date. [unless Vamos settings has Ads off: Then the 20 Meta ads still running in [category] in [market] that have run longest, 30 days or more, from [competitors] and the category's other advertisers. Give each ad: the advertiser, the Ad Library link, days running, copies, the format, the first line said and the words on screen in the first frame (a static: the words on the image and its headline), and whether you read them from the ad itself or only from its copy.]

The words are in the answer's text; the views and links are in its rows. An ad's line read from the ad itself is a proven hook, ranked by days running where a post ranks by views. Vamos opens only some ads, so a line read only from an ad's copy is labelled "ad copy": the text above the ad, not its opening.

**3. Write about ten** for this idea in this format, per [references/hooks.md](references/hooks.md). First name, in a few words, the one thing in this video a stranger would stop for: something strange, something they'll watch change, or a claim bigger than feels safe, never their problem said back, which they know already. When the idea has none yet, give them one to film: a small stunt, or their own before and after. A stunt or a before and after is said plainly in a sentence of its own, the way the reference's stunt and before-and-after hooks say theirs, because the thing carries the line: "I emailed 75 million people and asked them each for $1." (@codyshacks). Any other thing goes into one proven hook's own sentence: its words and its pull stay, and what the thing doesn't need is cut, so the thing is said once, in one breath (test 4).

Write from the proven hooks and from their own first lines that worked (What works for me, or the voice guide's best lines); the voice guide's templates set the voice, not the sentence. Take those whose sentence passes the five tests on its own, this format first, most views first. A tip or advice worked because of who said it, theirs included: it stops their followers, who know them, and not a stranger. Skip it whatever its multiple, and a story only another creator lived too. When fewer than three pass, widen to the reference's proven hooks and say so.

Keep the main hook and up to four alternatives, each built from one post, reference hook or line of theirs; drop any that keeps only a shape, or starts from nothing. Anything a hook says they did, had or got, other than the stunt or before and after they'll film for this video, comes from Things you've said, or stays a `[your …]` slot; when the slot is what pulls, drop the hook.

When the user brought a hook, step 2 still runs, so judge it against the proven hooks: say plainly whether it works and why, then keep their words and change the least: their line or its smallest fix is the main hook, with their original beside each change.

**4. Check.** Where there's a shell, write the kept hooks to `kept.json` (`said`, `on_screen`, `shown`, `source`: the post's or ad's link, "hooks.md @handle" for one from the reference, or "their line") and the answer or the Hooks tab to a text file, then run `python3 scripts/check.py kept.json <that file>` and fix what it prints. Then the cold read: a fresh subagent sees only the kept hooks, not the idea: "What do you think this video is about? Would you keep watching? Which word would you need explained?" Wait for its answer; a hook it misreads or wouldn't keep watching is rewritten from the same proven post or line, or dropped, and only then show them.

**5. Show and keep them,** all in the final message. Every kept hook, alternatives too, gets the same lines: **Said** ("none" on a silent format) · **On screen** · **Shown** · **Built from** the post or ad whose sentence it keeps, by its link and multiple (an ad: its days running; a reference hook: its @handle and numbers), or their line, quoted. Below the hooks, the ads' opening lines it read, each with its advertiser, days running and link, so they see what the category keeps paying to open with. Then one save to the board: the main hook on the idea's row, and in the Hooks tab every new proven hook (one row per link) and the written ones (Source: the idea). Next is `/cracked-marketer:brief` when a creator films it, or `/cracked-marketer:script` when the team makes it.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
