---
name: content-strategy
description: Use when they ask which idea to make, or whether a draft or reel is ready to post: the call rests on how lookalike posts did, which Vamos reads. Also audits their posts and plans content.
---
# Content strategy

Three jobs: a plan for a period, an audit of their own posts, and a check on one piece, or a choice between ideas, before anything goes out.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Give them Vamos's answer as it came, every link and number in it, and its `answerUrl` so they can open all of it in Vamos.

## Plan

**The job:** the strategy a team signs off: who it's for and why they'd care, what only this brand can say, its pillars, the formats working in its niche now, then a dated calendar at the pace they can film.

**Needs:** the brand: the workspace brand, or the brand, handle or niche they named. When there's neither, ask for their brand or handle in one short question, because Vamos can't ask once it's working. `create_chat` shows the brand their Vamos workspace holds; use it rather than asking, and name a different brand in the ask when theirs is about one.

**Ask Vamos:**
> Build our [Q1] content strategy for [brand] on [platforms]: who it's for, what only we can say, our pillars, the formats working in our niche, and a dated calendar [at N posts a week] [toward the goal].

**Next:** offer the calendar as a sheet, and to keep the plan in Vamos: send "save this as my content plan" to the same chat.

## Audit their account

**The job:** how their own recent posts did against their usual: what beat it and why, what fell under it, what to make again.

**Needs:** their handle, or the account the workspace holds. When there's neither, ask for it in one short question.

**Ask Vamos:**
> Audit my [platform] @[handle]: my last [30] posts against my usual, which beat it and why, which fell under it, and what I should make again.

## Check a draft, or pick between ideas

**The job:** a verdict (post it, don't, or post it with one change), the lookalikes it rests on, and that change written out.

**Needs:** the draft or the ideas: a link (a public post, an unlisted YouTube link, a direct .mp4), the script or idea in words, or what the video shows and says. A video file can't be read here, so when they attach one, ask for a link, or for its first spoken line and on-screen text word for word.

**Ask Vamos:**
> Should I post this? [the draft, or the ideas to choose between]. [What they said about their account.]

**Next:** offer the rewrite: "rewrite it with that change", in the same chat.

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
