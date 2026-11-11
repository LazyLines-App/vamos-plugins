---
name: "script"
description: "Writes a reel, TikTok, Short or voiceover script, or a caption, in your own voice from your Vamos workspace, using only what you've really said about yourself: for an idea on your board, one you give, a story of yours, or a draft that sounds like AI. Use for \"write my next reel\", \"write a reel about…\", \"write like me\", \"make this sound less like AI\"."
---

# Script

**The job:** a script they'd film without rewriting: it sounds like them, it's built on something that already worked, and it says nothing about them that isn't true. [references/script.md](references/script.md) holds the craft and an example; read it before writing.

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` (free) tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas, hooks and scripts need it, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** Open a Vamos chat with `create_chat` once per job, send each ask with `chat_completion_start`, and call `chat_completion_poll` until it's done. Follow-ups go in the same chat. Add `include_data: true` when you need the rows (with `include_transcripts: true` for up to 10 transcripts, and `data_format: "inline"` when you can't fetch a link). The rows are the posts the answer links; add `data_scope: "turn"` for every post the research read. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50, so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file` (free; `when_to_use` makes it a skill), always as its whole text, so read one first to add to it. The voice guide, content plan and profile notes change only in a Vamos chat, each as its own `chat_completion_start` message ("Save this as …"). Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** `get_credit_usage` and `get_messages` are free. Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 3 days old, leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. When Vamos answers that no file has that name, its error lists the exact names: retry once with the right one. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer:

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/vamos:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**1. The idea.** The rows at Approved or Picked on the board ([references/board.md](references/board.md)), or the idea they give you. Its hook is the row's Hook, or theirs; an idea with no hook gets one first, the `/vamos:hooks` way. With no idea yet ("write my week of reels"), run `/vamos:ideas` first. A draft they paste is a rewrite (below).

**2. Read, free.** `get_workspace`, then `get_workspace` with `file` for each of Voice guide, Voice examples, Things you've said, Vamos settings and Marketing plan that its `files` lists, and each Brain skill starting "Structure:" that its `skills` lists. These reads are free and hold their voice, so no Vamos turn loads or writes it.

**3. The find, one paid turn at most.** When an idea comes from a find and the row doesn't carry its transcript, ask once for every find in the run, with `include_data` and `include_transcripts` so the transcripts come in the rows: "Give me the beats (what's said and what's on screen) of [links]."

**4. Plan** the promise, the skeleton and the target words, per [references/script.md](references/script.md).

**5. Write it** in one go, out loud, in their language (their Voice examples', else their ask's): Said and On screen lines per beat, every "I" sentence sourced or left as a `[your …]` slot, then the caption.

**6. Check in code,** on every draft, rewrites and drafts that are mostly slots included: the code leaves `[your …]` slots out of every count and reports the words left for them. Save the Said lines (hook first, slots as written) as `script.txt`, the find's transcript as `find.txt` and their voice numbers as `voice-numbers.json`, then run
`python3 scripts/textstats.py check script.txt --profile voice-numbers.json --seconds [N] --sources find.txt`
Leave out `--sources` with no find and `--profile` with no numbers; the tells still count. Fix what fails (overlap with the find over 15% outside the hook, length 15% off, tells they don't use) and rerun; warnings are information. Only the find is a source, because their own repeated lines are their voice. With no code tool, say you skipped it.

**7. Cold read** in a fresh subagent, per [references/script.md](references/script.md). Rewrite what it marks.

**8. Hand it over.** Show the whole script in the reply: Said and On screen by beat, then the caption, the `[your …]` slots they must fill with the words step 6 left for them, and the checks in one line. Put the same on the idea's row and set it to Script ready. When their edits show a habit ("I'd never say 'folks'"), send it to Vamos as a voice correction in its own message.

**A rewrite** of their draft (a script, hook or caption) needs only step 2: keep their facts, order and length and add no claim of your own, take out the tells they never use, turn a question they answer themselves into a plain line that still names what's coming, run step 6, and show the new version in full.

Next is filming it, then `/vamos:content-log` a week after it posts.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
