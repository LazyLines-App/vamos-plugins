---
name: "analyze"
description: "Watches any TikTok, Reel or Short, or a whole profile, and says why the hits worked against the same creator's posts made the same way, beat by beat, then saves each structure so your scripts can follow it. Use for \"why did this go viral\", \"grade my reel\", \"break this down\", or a creator's hits and misses."
---

# Analyze

**The job:** why a video did what it did, set beside a post from the same account made the same way that did a third as well or less, and the structure the user's scripts can follow. Two modes:
- **A video** (a link): its reason, layer by layer, beside its miss.
- **A profile** (an @handle and a platform): its hits against its misses, the patterns, and each structure that repeats.

A brand's whole teardown, with its ads and how it sells, is `/cracked-marketer:playbook`. The method is [references/structure.md](references/structure.md).

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

**1. Take the link or the handle.** Ask nothing unless it won't open, or a handle comes without its platform.

**2. One research turn,** with `include_data: true` and `data_scope: "turn"`, so the rows are every post Vamos read and not only the ones its answer links. Send it as the user's request, with the platform's word for the posts (Reels, TikToks, Shorts) and the niche:
- **Video:** "How did [link] do against [account]'s own posts made the same way, and why? Watch it and give its beats with timings: what's shown, what's on screen and what's said, the hook word for word in all three, and its format. Read [account]'s last 40 [Shorts] as rows with views, likes, date and length. Then watch the 2 posts from [account] made the same way that did furthest from it (a third as well or less if it beat the account's usual, 3× as well or more if it didn't), and give their beats the same way; if there are none, the closest post in [niche] made the same way. Niche: [niche]."
- **Profile:** "Read [@handle]'s last 40 [TikToks] as rows with views, likes, date and length, and say how each was made (its format and hook). Then watch their 3 biggest posts and, for each, a post made the same way that did a third as well or less, and give each one's beats with timings: what's shown, what's on screen and what's said, the hook word for word. Niche: [niche]."

If no rows came back, ask once more in the same chat for the rows. If there are still none, use Vamos's usual and multiple, say they're Vamos's, and call the reason unproven.

**3. Find the reason** per [references/structure.md](references/structure.md): the usual, what was set aside, the pair, layer by layer, and how sure. For a profile, also the kinds of post with their medians, a pair per hit, and the patterns, counted. Read the comments only when the reaction is the question.

**4. Save each structure,** unproven or holds, when the rows came back. With no rows, don't save: end the hand-over with a one-line offer to save it. `get_workspace` lists the Brain skills starting "Structure:"; read each with its `file` for its format, signature and status, and decide add or update by the signature. Write it in the fields of structure.md and save it with `save_brain_file`: title "Structure: [name]" (an update keeps the old title), the whole text, and `when_to_use` saying in one line which videos it fits. An unproven structure is saved with its status, so the next pair can move it to holds.

**5. The page.** Make `analyze.html` on [assets/page.html](assets/page.html) as [assets/PAGE.md](assets/PAGE.md) says, from this breakdown. Where you can't write files, give the same in the chat.

**6. Hand it over**, opening on the verdict. For example:

> "I fixed my rental for $200" did 412,000 views, 14× the account's usual of 29,400 (the median of 38 posts at least 7 days old, read 11 Nov; one #ad post set aside). Made the same way, "Rental fixes under $50" did 31,000 (1.1×). The hit opens on the finished room, the miss on the empty one, and the hit runs 20 s shorter. Two layers changed, so it's a guess until a second pair agrees.

A profile opens on its strongest pattern, counted, as in structure.md. Then:
- the beats, hit and miss side by side, with both links;
- the structure: its slots, what never changes, its status, and whether its save came back with an `action`;
- when setup has run, one script draft for their brand on it, the `/cracked-marketer:script` way, or the offer of one.

When it's their own video, say the lesson in one line; `/cracked-marketer:content-log` weighs it against their other posts.

**Check before the recap:** every number is in a row or is your arithmetic on the rows; each link is one Vamos returned; the miss is from the same account (or the niche, when said) and is not a repost of the hit; "holds" only with two pairs, or one pair and the medians. Next is `/cracked-marketer:brief` on an approved idea with this structure for a creator to film, or `/cracked-marketer:script` for one the team makes.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Cracked marketer plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
