---
name: content-strategy
description: Judges content before it goes out (a draft, reel or idea, or which of several to make: post, don't, or one change) and plans it: a strategy and calendar. Use for "should I post this", "is it good".
---

# Content strategy

Two jobs: a plan for a period, and a check on one piece before it goes out.

## Plan

**The job:** the strategy a team signs off: who it's for and why they'd care, what only this brand can say, its pillars, the formats working in its niche now, then a dated calendar at the pace they can film.

**Needs:** the brand. Use the workspace brand from `create_chat`, or the brand, handle or niche they named. When neither exists, ask in one short question for their brand or handle, because Vamos can't ask once it's working.

**Defaults** (don't ask; name the ones you used in one line with the answer): the platforms they named, else TikTok and Instagram; the next quarter, or the period they named; three posts a week; the goal of reaching people who could buy. `create_chat` returns the brand their Vamos workspace holds, so use that brand rather than asking for it; when their ask is about a different brand, name that one in the ask.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. The user sees only what you show them, so carry Vamos's answer over whole (every row, hook, script and link) rather than pointing them to the Vamos chat.

**Ask Vamos:**
> Build our [Q1] content strategy for [brand] on [platforms]: who it's for, what only we can say, our pillars, the formats working in our niche, and a dated calendar at [N] posts a week toward [goal].

**Deliver:** a document they can share: the strategy, then the calendar as a table (date, pillar, format, hook, the example it builds on). Offer the calendar as a sheet, and to keep the plan in Vamos: send "save this as my content plan" to the same chat.

## Check a draft

**The job:** a verdict (post it, don't, or post it with one change), the lookalikes it rests on, and that change written out.

**Needs:** the draft, or the ideas to choose between: a link (a public post, an unlisted YouTube link, a direct .mp4), the script or idea in words, or what the video shows and says. A video file can't be read here, so when they attach one, ask for a link, or for its first spoken line and on-screen text word for word.

**Defaults** (don't ask): Vamos already knows the workspace brand, so add their niche, platform and size only as they said them. A link to someone else's post is the reference they're copying: the verdict is on their version of it.

**Ask Vamos:**
> Should I post this? [the draft]. [What they said about their account, if anything.]

**Deliver:** the verdict first, as Vamos gave it; the one change; the lookalikes with their numbers. Offer the rewrite: "rewrite it with that change", in the same chat.

**Check:**
- Plan: every format links a real example; every date falls in the period; the pace matches what they said.
- Draft: the verdict says how many lookalikes it rests on; it never promises views.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
