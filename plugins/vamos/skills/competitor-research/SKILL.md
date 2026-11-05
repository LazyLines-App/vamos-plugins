---
name: competitor-research
description: Tears down a competitor, brand or category: posts that beat their usual, the Meta ads they keep running, the creators they pay and how, and what to copy. Use for a brand's ads or creator program.
---

# Competitor research

**The job:** everything that works for a competitor, in one report: their posts that beat their usual on TikTok, Instagram and YouTube, the Meta ads they've kept running longest, the creators and partners they pay and how that program runs, what to copy and the gap they leave.

**Needs:** the competitor (a handle, a link or a brand name), several of them, or a category. "My competitors" needs a workspace brand; when there is none, ask in one short question which brands they mean, because Vamos can't ask once it's working.

**Defaults** (don't ask): every platform, with organic, ads and creator program; what to copy for the workspace's brand, or general lessons when it has none; a program of their own only when they ask, at the budget they name. `create_chat` returns the brand their Vamos workspace holds, so use that brand rather than asking for it; when their ask is about a different brand, name that one in the ask.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. The user sees only what you show them, so carry Vamos's answer over whole (every row, hook, script and link) rather than pointing them to the Vamos chat.

**Ask Vamos**, one message, for the whole teardown; when they ask about one part (their ads, their creators), ask for that part alone, as fully:
> Break down [competitor] as a competitor of [brand name]: their organic posts on TikTok, Instagram and YouTube that beat their usual, the Meta ads they keep running longest, the creators they pay and how that program works, and what I should copy.

With no competitor named: "Find my top competitors for [brand name] and break them down the same way."

When they want the program for themselves: "Build me a creator program like theirs for [brand name] at [budget or goal]."

**Deliver:**
- A report they can share. What works for them: posts and ads, each linked with its numbers. Their creator program: the accounts, the line or script they share (word for word), how often they post, what they kept running. What to copy, and the gap.
- For several competitors, a comparison table on top.
- A program of their own: how many creators and of what kind, the brief, the first hooks, the cadence, how to judge and cut.
- A sheet of every post and ad, on request: ask `get_messages` with `include_data: true` and build it from the rows.

**Next:** offer a weekly watch: send "every Monday, send me what they posted and launched" to the same chat.

**Check:**
- Every claim links a post or an ad.
- An ad wins on days running and versions, never on spend: Meta doesn't publish it.
- An account counts as part of their program only on evidence (a bio link, a tag, a disclosed partnership, a shared script).
- The report says which platforms had nothing.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
