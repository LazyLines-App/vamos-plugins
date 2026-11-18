---
name: "script"
description: "Writes a reel, TikTok, Short or voiceover script, or a caption, in your own voice from your Vamos workspace, using only what you've really said about yourself: for an idea on your board, one you give, a story of yours, or a draft that sounds like AI. Use for \"write my next reel\", \"write a reel about…\", \"write like me\", \"make this sound less like AI\"."
---

# Script

**The job:** a script they'd film without rewriting: it sounds like them, it's built on something that already worked, and it says nothing about them that isn't true. [references/script.md](references/script.md) holds the craft and an example; read it before writing.

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas need it, and so do hooks and scripts while its `voice` is false, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. On an ask about their own brand, every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** One Vamos chat per job (`create_chat`); follow-ups go in it. Add `include_data: true` when you need the rows. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50 posts (30 ads, creators or formats), so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **The ask decides.** A brand, niche or platform the user names wins over the workspace's, so run their ask as they put it, in the same turn, and write the reply about what they named: the workspace is background, named only when they ask about it. Name the brand, niche and platforms in every Vamos ask, because the workspace may be about another brand. For a niche their brand isn't in, ask about that niche in general, and open the reply with that scope in a few words ("Fitness accounts in general, on TikTok, Instagram and Shorts.").
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file`, always as its whole text, so read one first to add to it. Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** Run what the ask needs and report the cost in the recap; ask first only when what they have left is below a step's cost. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute the account's median yourself: the median views of posts at least 7 days old (views still climb before that), leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). A post's views over that median is its outlier score, written "N× outlier": "got 5,974,383 views, a 6.9× outlier: the account's median is 868,629 (its 33 Reels at least 7 days old among the last 40)". Under 1× it's "0.4× outlier" or "under the median". Say "median" and "outlier" even where Vamos's answer says "usual". A younger post that already beats the median shows as "N× outlier so far"; one that doesn't is too early to judge. Elsewhere use Vamos's multiple as the outlier score and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, do the same check yourself in a separate pass that reads only that text. The check is your working: the reply carries what passed.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. Never spend a turn reading one.

**End every run with the recap** in the chat, and as the last line of the page when the skill makes one. Next is the step this skill names, and when it names a choice, offer each. When it can run now, offer it as a question and, on their yes, run it yourself, so they never need to remember a command; when it waits on them or on time (filming, a post's first week), say what and when.

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Board:** [its link, when there is one] · **Next:** [what it does, in eight words] (`/vamos:[skill]`). Shall I?
<!-- /shared -->

## Steps

**1. The idea.** The rows at Approved or Picked on the board ([references/board.md](references/board.md)), or the idea they give you. Its hook is the row's Hook, or theirs; an idea with no hook gets one first, the `/vamos:hooks` way. With no idea yet ("write my week of reels"), run `/vamos:ideas` first. A draft they paste is a rewrite (below).

**2. Read, free.** `get_workspace`, then `get_workspace` with `file` for each of Voice guide, Voice examples, Things you've said, Vamos settings and Marketing plan that its `files` lists, and each Brain skill starting "Structure:" that its `skills` lists. These reads are free and hold their voice, so no Vamos turn loads or writes it.

**3. The find, one paid turn at most.** When an idea comes from a find and the row doesn't carry its transcript, ask once for every find in the run, with `include_data` and `include_transcripts` so the transcripts come in the rows: "Give me the beats (what's said and what's on screen) of [links]."

**4. Plan** the promise, the skeleton and the target words, per [references/script.md](references/script.md).

**5. Write it** in one go, out loud, in their language (their Voice examples', else their ask's): Said and On screen lines per beat, every "I" sentence sourced or left as a `[your …]` slot, then the caption.

**6. Check in code,** on every draft, rewrites and drafts that are mostly slots included. Save the Said lines (hook first, slots as written), a line `---`, then the On screen lines and the caption as `script.txt`, and what they've really said as `facts.txt` (Things you've said and their own words in this chat outside any draft, even one line), then run
`python3 scripts/textstats.py check script.txt --facts facts.txt --voice voice.txt --profile voice-numbers.json --seconds [N] --sources find.txt`
with their Voice examples saved as `voice.txt`, their voice numbers as `voice-numbers.json` and the find's transcript as `find.txt`. Leave out each of those flags whose file they don't have; the tells and stories still count. Slots are left out of every count, with the words left for them reported. Fix each fail it lists and rerun: a tell their own videos don't use, with the fix it names; a story about them that nothing they've said holds, as a `[your …]` slot in the same shape; overlap with the find over 15% outside the hook; length 15% off. Warnings are information. Only the find is a source, because their own repeated lines are their voice. With no code tool, say you skipped it.

**7. Cold read** in a fresh subagent, per [references/script.md](references/script.md). Rewrite what it marks.

**8. Hand it over.** Show the whole script in the reply: Said and On screen by beat, then the caption, the `[your …]` slots they must fill with the words step 6 left for them, and the checks in one line. Put the same on the idea's row and set it to Script ready. When their edits show a habit ("I'd never say 'folks'"), send it to Vamos as a voice correction.

**A rewrite** of their draft (a script, hook or caption) runs as soon as they paste it, before setup and with no Vamos connected too, because it keeps their words. Do step 2's reads when Vamos is there, then keep their order, length and facts (what they sell, their news, their steps) and add no claim of your own. Take out the tells they never use, and turn a question they answer themselves into a plain line that still names what's coming. A story or number about their own past that nothing they've said holds becomes a slot in the same shape that names what goes there ("I had [your number] followers and [your real start]."), on screen and in the caption too, because AI drafts make these up: say so in one line, and put it back when they say it's true. Then run step 6 until it passes, and show the new version in full, then the slots to fill. Before setup, the recap's Next is `/vamos:setup`, so the next one sounds like them.

Next is filming it, on them: once it's edited, they tell you where the file is (it goes on the row's File), and `/vamos:post` posts it.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Vamos plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
