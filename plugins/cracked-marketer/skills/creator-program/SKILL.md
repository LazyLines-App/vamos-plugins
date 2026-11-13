---
name: "creator-program"
description: "Plans a brand's creator (UGC) program and prices its creators: how many to message and start with, what to pay each one per video against a dated table of published deals, the terms to agree before anyone films (running their videos as Spark or partnership ads: the window and the fee), the first DM and follow-ups with that offer, the code ask, whose accounts they post on, the first 30 days, how to read results, and each wave of creators on one grid with who moves up and who stops. Use for \"start a creator program\", \"what should we pay UGC creators\", \"how many creators do I need to message\", \"is $300 a video fair for @creator\", \"price these creators off their worst videos\", \"write the DM to the creators we found\", \"usage rights so we can run their videos as ads\", \"write the Spark code ask\", \"who gets a raise\", tracking a second wave of creators, or running creators for an app or shop."
---

# Creator program

**The job:** a program a founder can forward: how many creators and how many to message to get them, what each is paid per video and why, which accounts they post on, how a winner runs as an ad, the first 30 days, and how to tell a win from a flop. Money is always per video. Every number is either a published deal, with whose it is and when, or our proposal, marked as ours. The user sends every message and signs every deal; this skill drafts.

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

**1. Read what's there, free.** `get_workspace` and `get_credit_usage`. With `get_workspace`'s `file`, read the Marketing plan (what they sell, where people buy) and any "Creator program: [brand]" from an earlier run, which this run updates.

**2. A rates question.** With no handle ("what do creators charge?", "a creator quoted $250, is that crazy?"): answer from [references/pay.md](references/pay.md) with no Vamos turn. Give the deals per video with whose and when, place their quote among them, and say what decides it: that creator's views at their floor, and whether ad use is included. Offer to price the creator from their handle, with its cost (one turn, at most 60 credits), and stop there. With a handle ("is @creator's $400 fair?"): say that cost in one line, run step 5, and answer with their floor, your offer and the deals beside it.

The same goes, free, for how many creators to message to get N filming ([references/outreach.md](references/outreach.md): the count, the waves, the follow-ups, each rate with how sure it is; any money total is creators × videos each × pay, summed in code) and for running creators' videos as ads ([references/ads.md](references/ads.md): the terms, the code ask written out for their creator and platform, where they paste the code). When "Creator program: [brand]" exists, change only the part asked about, using its creators and prices as saved, and save it back (step 7). None of this needs a Vamos turn: links they send for their creators' posts are saved as given, and content-log checks them when it reads results.

**3. Take what they've told you; the rest has a default,** listed at the end of the answer for them to correct. Ask first only when the budget is missing.
> 1. Posts on creators' own accounts, ad files for your ads, or both? (posts)
> 2. The monthly budget for creators? (ask)
> 3. Do you sell online with a link or code you can track per creator? (from the Marketing plan)
> 4. Has a post of yours already gone well past your usual? A link if so. (no)
> 5. Creators in mind? Handles, or run `/cracked-marketer:find-creators` first. (none yet)

**4. The category turn:** say its cost against their balance in one line (one turn, at most 60) and run it, since the plan stands on it:
> I'm planning a creator program for [brand] ([what it is, who it's for, price], [site and handles]). Who already wins with creators in [category] on TikTok and Instagram? Name the brands or apps, the creators they use with handles, whether those creators post on their own accounts or the brand's, the formats and hooks that went well past their usual in the last 90 days, and how those videos show the product. Add any pay terms a brand or creator has published, with the link and date.

**5. Price each named creator,** in one turn with `include_data: true`:
> For [brand]'s creator program: give me the last 30 posts of [handles] on [platform] as rows, with views, likes, date and whether each is a paid partnership.

Then `python3 scripts/price.py floor <rows file> --fee <their ask> --handle <handle>` (it sets boosts, paid posts and reposts aside itself) and `python3 scripts/price.py offer --base <base> --usual <usual>`. Pick the base from the deals and their floor. Without a shell, do the same arithmetic and say so.

**6. Write the program** in the order of [references/program.md](references/program.md), using its rules where they fit this brand. Run `python3 scripts/price.py table references/pay.md` and say a deal is old when it's flagged. For each named creator, end with the message the user sends from their own account: two or three sentences naming one real post of theirs, what [brand] is, your offer per video with the bonus thresholds (and that the pool is shared, when it is) and how it's paid, the number of videos and by when, and one question, with no deadline or scarcity the user didn't give; then a one-line follow-up for day 4 and a last one for day 10, with no reply. A draft earlier in this chat with another price comes again with this one.

**7. Save** with `save_brain_file` a Brain file "Creator program: [brand]" with the creators and their offers, each one's wave, stage (Test or Core), videos and due dates, the rounds of notes agreed, the pay model and its numbers, the ad-use terms (window and fee), the messages to send and, once they say, their own reply and yes rates, the accounts, the test grid and how results are read, so brief, review-draft and content-log work from it.

**Check before the recap:** every offer is per video and the month's money, the ad-use reserve included, adds up within the budget (sum it in code); every outside number has whose and when; the 3-second opening, the paid-partnership label, the ad-use terms (what, the window, the fee) and how many to message are in; any message to a creator is a draft for the user. Next is `/cracked-marketer:find-creators` when there are no creators yet, else `/cracked-marketer:ideas` for the test's angles, then `/cracked-marketer:brief`.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Cracked marketer plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
