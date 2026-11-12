---
name: "playbook"
description: "Takes a brand, competitor or creator apart into a playbook for your account: what works for them, counted against their misses, their hooks, how they sell, their Meta ads, paid creators and what their customers say in comments, reviews and Reddit when you ask, and five plays for your brand. Use for \"break down [brand]\", a competitor's strategy, ads, paid creators or unhappy customers, what your own customers say about you, or what to steal from a creator like Hormozi."
---

# Playbook

**The job:** what a brand or creator does that works, and exactly how the user would use it on their own account. Patterns, counted: "8 of their 15 best posts open on a bold claim, against 4 of their 30 weakest". A single big post is only ever the example of one.

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

**1. The target and the user.** Get the target's handle on each platform and its site; ask only when two different accounts could be meant. A person selling their own thing is a creator; otherwise a brand. The user's own product comes from their ask, else from `get_workspace`; when neither says what they sell, ask in one line before spending, because every play is written for it.

**2. Read what they asked for.** A breakdown, a competitor, a creator or "what should I steal" is the organic turn alone (about 50 to 60 credits). Ads and paid creators (about 15 to 60) and what customers say (about 30 to 50) run when the ask names them; organic joins them only when they asked for everything. Say in one line what you'll read and its cost, then go. Offer the rest at the end with its price.

**3. The organic turn,** one ask for the platforms they named, else every platform the target posts on, with `include_data: true` and `data_scope: "turn"`:
> For [user's brand], I'm studying [target] ([handle on each platform], [site]). Read their last 40 posts on [platforms] and say how each one was made: its format, its opening hook word for word, and whether it asks for a comment keyword out loud. Then what they sell and the path from a free thing to a paid one.

**4. If the top posts came back with no hook or format** (an account Vamos hasn't read before), one more turn before you name any hook:
> Watch [target]'s top [N] posts and 5 posts made the same way that did a third as well or less: [links]. Give each one's beats with timings, what's said and what's on screen.

Quote hook words only for posts Vamos watched or described; the rest are counted from what their rows carry.

**5. Count it yourself,** in code where the host allows:
- **Usual** as in Numbers, per platform, from the target's own posts, not those on collaborators' accounts. Tagged paid is #ad, partner, sponsored or Paid partnership; a brand tag alone isn't paid. Each post's multiple is its views over the usual.
- **Top quarter against bottom half,** by multiple: 3 to 5 traits each counted "N of M" ("bold-claim opener: 8 of 15 top, 4 of 30 bottom"), and the trait the bottom half has more of, which goes under Skip. Under 20 posts, a trait is a hunch.
- **A pair per trait:** a hit and a miss made the same way where the trait is the main difference. Two changed layers make a guess, and you say so.
- Their hook formulas, their keyword calendar (which keyword, on how many posts, from when to when), and reach posts against lead posts.
- Mark each claim Seen (in the data) or Inferred (your read of it).

**6. Ads and paid creators, when asked,** with `include_data: true`:
> For [user's brand], I'm studying [target]'s Meta ads, page [page id or name], site [site]: how many are running and how many stopped, the headline families with how many ads use each, landing pages, formats, and partnership ads with each creator's Instagram or TikTok handle. Say how many ads you checked of how many there are.

Each ad row carries `days_running`. Rank the rows by it yourself, in code, and give the top three with days, headline and link: what they keep paying for. Say what was read ("checked 80 partnership ads; 30 came back as rows; the longest-running of the 30 has run 41 days"). Zero stopped ads for a brand outside the EU and UK is "not visible".

**7. What customers say,** when the ask names customers, reviews, complaints or Reddit, for a competitor or their own brand (about 30 to 50 credits), with `include_data: true`:
> For [user's brand], I'm reading what [target]'s customers say. 1. The comments on [target]'s top 10 posts of the last 30 days on [platforms] and on their longest-running ads that give a reason: why they bought, what they switched from, the moment they started looking, what stopped them, what they compare it to, what went wrong (complaints, cancel and refund asks), word for word, with likes and the link. 2. Search the web for Reddit threads and reviews (their site, Trustpilot, Amazon) about [target] from the last 12 months, each quoted word for word with its link and date. Say how many comments, threads and reviews you read.

Add their survey answers when they give a CSV. Label every line yourself with one group by what it says: why they bought, what they switched from, the moment they started looking, what stopped them, what they compare it to, what went wrong (complaints, cancel and refund asks). Count the labels in code. Each group gets its count, its sources and its two clearest lines word for word, linked; a line that gives no reason is counted, not quoted. Then write three hooks from the biggest of the groups the ask is about, in the customers' own words and, for a competitor, one switch idea for the user's board.

**8. Write the plays as tool calls, not yet as the reply (step 11):** into `data.json`, the page's data (step 9). Five, each from a counted pattern, each in five parts: Seen, Work, Watch, Your first line, Paste.

> **A keyword per offer, rotated by launch.** Seen: 47 of his 60 posts ask for a comment keyword; WIN ran on 30 posts (10-16 to 11-05), then SALES on 10 (11-03 to 11-07) for the Black Friday launch. Work: one free thing and a DM reply. Watch: comments per 1,000 views on lead posts. Your first line: "If you can't read your own numbers, you can't raise your rates." (his "If you can't sell anything, you can't make money.", 3.35×, with your subject). Paste: "Write 5 reels for RateSheet, my pricing calculator for freelancers, that end on 'Comment RATES and I'll send you the calculator'…"

The first line is what the user can say or put on screen today, word for word: their real hook with the user's subject swapped in, or, when their hit opens on a picture, the user's opening shot and the exact words on screen, as in the play under step 11. A detail you don't know (which language they teach, the mascot's or a feature's name, the discount) gets a likely pick, said once above the plays ("Spanish and a mascot called Lolo are my picks: swap in yours"), then used in every line and Paste, so none of them has a [bracket] left to fill. A trait that rests on their fame, budget or a one-off event goes under "Skip", with why. Then their first week: seven days, what to post, which formula, the number to check on day 7.

**9. The page, before the reply,** on every run, a quick question too: it spends no credits, and it is where they keep the plays. Write the `playbook` page's data ([assets/PAGE.md](assets/PAGE.md)) to `data.json`: the counted traits in `who` (`titles: {"who": "What wins, counted"}`; `line` the trait with its count, `proof` its pair, `post` the hit), their formats, their hooks with the user's versions, the customer groups when read (in `who` after any traits, `titles.who` "What customers say, counted" when they're alone; `line` the group with its count and sources, `proof` its clearest line and where it's from, `post` the post it was under, or `{url, hook}` for a review or thread), the five plays as `plays`, each entry whole (`title`, `seen`, `work`, `watch`, `line`, `paste`, and the `post` it comes from), and the first week. Then run `python3 [this skill's folder]/scripts/fill.py data.json playbook.html --embed`. Write or Bash in your tools means you can write files, so write it: `playbook.html` is the recap's Made link. A host with neither skips the page and says so in the recap.

**10. Save** with `save_brain_file` a Brain file "Playbook: [target], [date]" with the patterns, the keyword calendar, any ad ids and the customer groups with their counts and lines, so next month's run can say what they stopped and the next ad concepts can stand on the groups. Add the page's link to Vamos settings.

**11. The reply,** last: the sections of [references/playbook.md](references/playbook.md). The user reads the chat first and keeps the page, so each play is in the reply whole, its five parts word for word as in `data.json`:

> **2. Name what they cancel.**
> - **Seen:** "Cancel these 3 subscriptions" heads 5 of the 31 ad rows; the longest-running of the 31, at 48 days.
> - **Work:** a creator's phone, the old bills struck through.
> - **Watch:** your cost per trial on it against your other ads after 7 days.
> - **Your first line:** open on your app's bill list, three subscriptions struck through; on screen, "I cancelled these in 40 seconds."
> - **Paste:** "Write 5 Meta ad headlines for Penny, my budgeting app, that name what the viewer cancels…"

**Check before the recap:** every pattern carries "N of M" and links a hit and a miss from the rows; the usual is yours, by the rule, and any Vamos baseline is called Vamos's; every play has its five parts in the reply and on the page, and names the user's product, and every ad play the days its ad has run; nothing says spend, ROAS, revenue, "best-performing" or "every ad they ever ran"; the page is written, it is the recap's Made link, and its strip says what was read, when, and the credits. Offer what wasn't read with its price. Next is `/cracked-marketer:formats`, or `/cracked-marketer:analyze` on their best post.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
