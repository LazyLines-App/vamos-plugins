---
name: "content-log"
description: "Logs what's working on your account: your posts against your own usual, each pattern counted against the misses, last week's predictions checked, and what to repeat, stop and turn into an ad. For creators you pay, each one's posts against their usual, cost per 1,000 views, the winning hooks and who to double down on. Records the lessons every other skill reads. Use for a Monday report, a hook log, \"how did my posts do\", \"why are my reels flopping\", \"which creator won this week\", or an Insights screenshot."
---

# Content log

**The job:** one sentence that says what to make next because of what happened, with their own numbers; three lists (Repeat, Stop, Turn into an ad), each with why; and a record every other skill reads first: the board's Lessons and Reviews tabs and the What works for me file. [references/content-log.md](references/content-log.md) holds the method.

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

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/vamos:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**1. Read the state, free.** `get_workspace`, then `get_workspace` with `file` for Vamos settings (where the board is, ads on or off, the creators who post for them), the Marketing plan and What works for me. When they pay creators, also what [references/creators.md](references/creators.md) lists first: the creator program, the briefs and their hooks. Then the board ([references/board.md](references/board.md)): Lessons, the last Reviews row and its predictions, the Hooks rows that posted. The period runs from the last review (default: the last 7 days). Without setup, ask for their handles in one line and go ahead: the lessons go in the reply and on the page, and `/vamos:setup` makes the board.

Saves, reach, watch time, profile visits and link clicks come only from Instagram Insights screenshots they paste. Ask once ("For saves, reach and watch time, paste each post's Insights screenshot; without them I'll judge on public numbers") and carry on with public numbers in the same run.

**2. One research turn for every platform,** with `include_data: true` and `data_scope: "turn"`.
> For [brand] (@handle) on [Instagram and TikTok]: read my posts from [start] to [end] fresh (views, likes, comments, shares, length, the hook word for word, what's in the first frame, what the comments ask for and how many want to buy), and my 30 posts before that.[ The same for the creators who post for us, @a and @b: their posts in those days[ including these links], saying which are about [brand] or a paid partnership with it, and each one's 30 posts before that.][ My tracked competitors' posts in those days that beat their usual by 2× or more.][ What my tracked brands started, kept and stopped in the Meta Ad Library.]

Keep the bracketed parts only when they have creators, tracked competitors or ads on.

**3. Count it.** As soon as the poll is done, run it from the project folder, where `tags.json` and `pay.json` go:
```
python3 <this skill's folder>/scripts/count.py "<the poll's data.json_url>" --since [start]
```
[scripts/count.py](scripts/count.py) downloads the rows itself and holds the usual's rules, so every run counts the same way. Give it the saved poll file's path instead when the answer was saved to a file, or `-` with the poll's `data` piped in whole when the rows came inline. Its usual and multiples are the ones you quote: Vamos's answer counts by its own rules, so its figures differ. Then write `tags.json` (each post id to its hook shape, format, angle, first frame, stage and creator, plus `intent`, the comments asking to buy, when there's no keyword close) and run it again with `--tags tags.json`, and `--ads` when ads are on, to count each pattern against the misses. Without a shell, count by the rules in [references/content-log.md](references/content-log.md) and show the counts. Put last review's predictions beside what happened.

**With creators,** that second run is where their numbers come from: tag each post made for the brand in `tags.json` (`"ours": true`, the creator, the brief's hook it used), write `pay.json` from the creator program, and add `--pay pay.json`, as [references/creators.md](references/creators.md) says. Its `creators:` block holds each post against its account's usual, what it cost per 1,000 views, each creator's scorecard and the hooks across creators: quote those.

**4. Write it** in the order in [references/content-log.md](references/content-log.md). It opens on the finding: one sentence with a pattern, its numbers and the decision. "Number-first openers: 5 of 5 above usual, median 2.4×, against 0 of 3 for greetings, so next week's three open on a number." Then the three lists, each item with its numbers and why in one line, marked as a guess when it is one:
- **Repeat.** A post at 5× usual or more gets 3 to 5 versions for next week, each written out as its own line; at 3 to 5×, one. A version is the hit's sentence as one clause, with only its subject swapped for one as big for the viewer. One creator's "Claude just killed LinkedIn" got 4,538 and "Claude just killed Instagram" got 429,776, so what you swap in is what to get right. A job swaps for a whole job, as big as "run your Instagram", in the hook's first clause only: "Claude can now write your captions for you in seconds, basically doing the boring part" becomes "Claude can now run your Instagram for you". Its number, its tail and how exact its task was stay out, even when the research or your own tags credit them: the bigger job is what next week tests.
- **Stop.** Only a Confirmed lesson with the action Stop: 3 or more posts from different weeks under usual, like "greetings as openers: 0 of 4 above usual, median 0.4×, from 3 weeks". One flop never goes here.
- **Turn into an ad** (when ads are on in Vamos settings): a post from this period at 5× usual or more, with 10,000+ views, and keyword comments or signups per 1,000 views at or above their usual. On a keyword close ("Comment PLAN") the comment count is the keyword; otherwise count the comments that ask to buy.

**With creators,** add the Creators section in [references/creators.md](references/creators.md); it comes first when the ask is about creators.

**5. Record, without asking:** these rows and the file are what the job is for, and the next run reads them; say in the recap what you saved. On the Lessons tab, add rows and move statuses by the rule. The Reviews tab gets one row a week; a second run that week updates it. Add a Result to each Hooks row that posted, and put the Repeat versions on the board at To review. Then save What works for me with `save_brain_file`, your new text whole, and with creators the program's Results part.

**6. The page.** Fill [assets/page.html](assets/page.html) as the `content-log` page ([assets/PAGE.md](assets/PAGE.md)): the finding as the lede, the three lists in `lists`, the post chart, the lessons. Add its link to Vamos settings with `save_brain_file`.

**Check before the recap:** every × came from `count.py` or your shown counts, with the read date; with creators, every cost, scorecard and hook count came from its `creators:` block; each private number names its screenshot; every list item and lesson shows how many posts it rests on; nothing is on Stop or Confirmed on fewer than 3 posts from different weeks. Next is `/vamos:ideas`, which now starts from these lessons.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
