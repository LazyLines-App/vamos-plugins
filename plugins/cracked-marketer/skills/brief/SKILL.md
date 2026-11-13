---
name: "brief"
description: "Turns an approved idea into a one-page brief each UGC creator can film from on their phone: the hook word for word, three talking points, what to show, reference videos and what to send, in one briefs doc. Use for a creator brief, briefing creators, or what to tell creators so it stops looking like an ad."
---

# Brief

**The job:** a page the creator could film from today without asking anything, so the video looks like theirs and not an ad. [references/brief.md](references/brief.md) holds the page and a finished example; read it before writing.

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

**1. What to brief.** The board's Approved rows, or the idea or video they give you, and the creators they name for it. With no creator named, write one brief for `[creator]`. Read Vamos settings, the Marketing plan and any "Creator program: [brand]" free with `get_workspace` and `file`: what they sell, its facts and rules, where it's bought, and each creator's pay and terms, which go in their brief.

**2. One research turn** for every brief in the run (up to 60 credits, about 40 for three creators; say so first), with `include_data: true`, `data_scope: "turn"` and `include_transcripts: true`:
> For [brand] ([what it sells]) in [niche], on [platforms]: give the beats of [each source link] with timings: what's said, what's on screen and when the product first shows. For each, find 2 more videos in the same format in [niche] from the last 30 days that did well above their creator's usual, with links. [For @creator1, @creator2: each one's most-viewed recent post.] Research only; save nothing.

That one turn covers the run: use the references it returns, leaving out any it calls seeded, boosted or partner-tagged, and say in the hand-over how many it found.

**3. Write each brief** on the page in [references/brief.md](references/brief.md), one per creator, in their setting:
- **The hook:** the row's Hook, or the source's spoken hook cut under 12 words, plus one or two alternates. The creator says it, and the same words sit on screen from the first frame.
- **Three talking points:** the source's structure retold for this product, in words the creator would use; ★ marks the product line they say as written.
- **The product itself** is on screen by 3 s, whatever the source opens on, inside their day: where they find it or use it, not a list of benefits. An app's screen, phone or laptop, is filmed with a second phone.
- **Facts** come from the Marketing plan, the Brain or the user. Anything else is a `[slot]`, and a result or story told as the creator's own, the source's hook and story included, is a slot for theirs or a line said only if it's true for them, never the first hook or the ★ line.
- **Proof stays with the user.** The creator's page carries no multiples, views against a usual or tables; the hand-over does.

**4. Check.** Save the briefs and the poll's answer to files and run:
`python3 scripts/check_brief.py briefs.md --rows answer.json`
It fails on length (300 to 500 words), a missing part, a hook of 12 words or more, anything but three talking points, no ★, no product by 3 s, a link not in the answer, a table, a multiple or "usual", and no disclosure, due date or approval line. Fix and rerun until every brief passes. Then a cold read: a fresh subagent reads one brief as the creator and lists what it would ask before filming. Answer each question in the brief, then run the checker again: the brief that ships is the one it passed.

**5. Hand it over.** Put the new briefs at the top of one briefs doc, newest first: a Google Doc called "Briefs" when Google Drive is connected, else a Notion page "Briefs" beside the board, else `vamos/briefs.md` in the project folder wherever you can write files, and a Brain file "Briefs" (one `save_brain_file` with the whole doc) only where you can't. Put each brief's link in its idea's Script column at Script ready. In the chat, per brief: its link, the slots to fill, and one line of proof for the user (the source, its views and Vamos's multiple). They share the doc with each creator themselves.

**Check before the recap:** the checker passed or the hand-over says which brief didn't and why; every reference opens from the answer's links; no brief states a fact or result nobody gave you. Next is `/cracked-marketer:review-draft` when a draft comes in, then `/cracked-marketer:content-log` once the creators post.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Cracked marketer plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
