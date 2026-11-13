---
name: "ideas"
description: "Finds what's going viral in your niche, with your competitors, in their comments on TikTok, Instagram and YouTube, and turns what you can make yours into ideas backed by the post, on your board. Also says whether your own idea is worth making, from lookalikes that hit and missed. Use for \"what's going viral\", \"content ideas\", \"scroll for me\", \"what should I post\", \"which of these should I make\", \"is this worth making\", \"what my followers keep asking for\". Meta ad concepts from the ads that keep running are winning-ad-ideas."
---

# Ideas

**The job:** ideas the user would film, each backed by a post that's working now, in their audience's words. The find is the proof; the idea is what they make of it.

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

**1. Read the rules and their state.** Read [references/ideas.md](references/ideas.md) on every run, set up or not: the bar, the swap and the count are there. Then, free, with `get_workspace` and its `file`, read Vamos settings, the Marketing plan, What works for me, Tracked accounts and the board ([references/board.md](references/board.md)) where Vamos settings puts it. Its new Not for me notes go under Your calls and its 14-day rows go to Stale, saved in step 6.

**2. One research turn** for all their platforms, with `include_data: true` and `data_scope: "turn"`, so the filter sees every post read:
> For [brand], [what they sell] to [who], on [platforms]:
> 1. The 20 posts from my tracked accounts in the last 7 days that beat each creator's usual the most.
> 2. The 20 posts beating their usual most in [niche] in the last 14 days, from accounts I don't track. Search [2 or 3 searches in their audience's words].
> 3. What people ask in the comments on my last 20 posts and my tracked competitors' best posts this month, word for word, with likes, grouped by ask; for each ask, my post whose hook or caption already answers it, linked, or "not made yet"; and for each post how many comments want to buy (where to get it, the price, the link).
> Give each post: link, creator, views, multiple, date, length, format, the hook word for word, and whether it's an ad or paid.

When they ask about one competitor's comments or ads, send only that, naming the competitor. When they ask what their followers keep asking for, send only part 3, for their own posts.

**3. Filter in code, then judge.** Save the rows (`data` when it holds them, else curl its `json_url`) and the board as text, and run `python3 scripts/filter.py rows.json --board board.txt` (no `--board` when there's none; `--min-views 2000` in a small niche); it prints what's kept, with labels, and what's dropped and why. Comment asks and ads skip it. Judge what's left on the five tests in [references/ideas.md](references/ideas.md), group the same promise, and pick. Watch only the picks whose video carried them and whose beats the answer doesn't already give, in one turn: "Watch these [N] posts and give each one's beats, what's said and what's on screen." Only on a host with no shell, make the same cuts by hand and say so.

**4. Write** each pick per [references/ideas.md](references/ideas.md): what made it work, then three to five ideas, the straight swap first. Each idea carries its source, linked, with the row's multiple (or, for a comment ask, the likes), why it's theirs, its stage (reach, trust or buy) from the Marketing plan, and the lesson it uses when one from What works for me fits ("Uses lesson: number-first openers, 5 of 5 above usual"). Rank finds that fit a Confirmed lesson higher, give the thin stage at least a third of the ideas, all from finds that pass, and when What works for me has a Hunch, make one of a find's ideas a week test it.

**Dates coming up.** With your web search (free), find the dates in the next six weeks their audience cares about: holidays, awareness months, the niche's own days, each linked to where you found it. Give each date the idea from this run that fits it best and the day to post by, or "no idea fits yet": a date alone never makes an idea. They follow the finds in the reply, and that idea's board row ends its Why it's yours with "post by [day] for [date]". With no web search, leave them out and say so.

**5. The page and the reply.** Fill [assets/page.html](assets/page.html) as the `ideas` page ([assets/PAGE.md](assets/PAGE.md)) on every run, set up or not: each find's card with its thumbnail and multiple, what made it work, and its ideas under it. Your reply in the chat has the same shape, each find headed by its post, linked, with its multiple and its hook word for word (for a comment ask, the post the comments are on, the likes, and "made" with their post linked or "not made yet"), then its ideas. When they asked what their followers keep asking for, every ask you name gets that mark, the ones you set aside too, and a made one links the post that answers it.

**6. The board.** Add each idea at To review where Vamos settings puts it; a Brain-file board is one `save_brain_file` with the whole board, and new Your calls lines go into Vamos settings the same way. With no board yet, the page and the reply hold them. The Approval setting says where a run stops for their yes; To review is that stop, so it never holds back the page or the board.

**Their own ideas** (one, or a few to choose between): one turn, with `include_data: true` and `data_scope: "turn"`:
> For [brand], [what they sell] to [who], on [platforms]: is each of these worth posting? [their ideas, numbered]. For each, read lookalikes on its topic and format (the format in any niche), each against its creator's usual: how many you read, how many beat their usual, and the best 3 and the worst 3, linked.

Each idea gets a verdict from both sides, in Vamos's own counts, and "too few to judge" under 3 lookalikes:
> **1. Sourdough starter mistakes: worth making.** 5 of 8 lookalikes beat their usual. Best: [@a](link) 22×, [@b](link) 9×, [@c](link) 4×. Worst: [@d](link) 0.4×, [@e](link) 0.6×, [@f](link) 0.9×.

Then check it against the bar in [references/ideas.md](references/ideas.md), their calls and the board, say plainly which is worth making and why, and give the best ways to make it theirs.

**7. Tell them how to approve:** set a row to Approved on the board, or reply here ("approve 1 and 3"), and `/cracked-marketer:brief` briefs the ones a creator will film, or `/cracked-marketer:script` writes the ones the team makes ("approve 1 for us, 3 for creators").

**Check before the recap:** the page is built; each find has three to five ideas and every idea links its find; no idea repeats a promise on the board or does what a call's reason in Vamos settings rules out; the page and the reply count as on the board only the rows Vamos or the board confirmed. Next is `/cracked-marketer:brief` for the approved ones a creator will film, or `/cracked-marketer:script` for the ones the team makes.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Cracked marketer plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
