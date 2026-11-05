---
name: viral-research
description: Finds what's going viral in a niche on TikTok, Instagram and YouTube, ranked against each creator's usual views, and turns it into content ideas and a week of scripts. Use for "content ideas".
---

# Viral research

**The job:** what's going viral in a niche right now and why, then what the user should make from it. Three steps. Stop after the step they asked for: research for "what's going viral", ideas for "content ideas", and all three without pausing for scripts, "write my week" or /viral-week.

**Needs:** the niche or topic. When it's missing and the workspace brand doesn't give it, ask for it in one short question before you send, because Vamos can't ask once it's working.

**Defaults** (don't ask; name the ones you used in one line with the answer): TikTok, Instagram and YouTube; this week; their handle when they gave one. `create_chat` returns the brand their Vamos workspace holds, so use that brand rather than asking for it; when their ask is about a different brand, name that one in the ask.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. The user sees only what you show them, so carry Vamos's answer over whole (every row, hook, script and link) rather than pointing them to the Vamos chat.

**1. Research.** Ask Vamos, with `include_data: true`:
> What's going viral in [niche] on [platforms] [this week]: the videos furthest past their creator's usual views, each with its hook, its format and why it worked.

Deliver a table, one row per video: the post (linked), creator, views, × usual, hook, format, why it worked. Numbers and links exactly as Vamos gave them; "why" from its answer. When they want a sheet, build it from the `include_data` rows plus the "why" column, in Google Sheets when it's connected, otherwise as a file, or as CSV in your reply when no file can be saved.

**2. Ideas.** Ask Vamos:
> Turn this into [7] ideas for my [platform] account, each built on one of these videos, with its hook. [I'm @handle.]

Show each idea with its hook and the video it comes from. When they asked only for ideas, ask which to write; when they asked for scripts or their week, go straight on with the strongest ones.

**3. Scripts.** Ask Vamos:
> Write scripts for [the picked ideas, or the 7 strongest for a week] in my voice.

When Vamos's answer says no voice is saved, deliver the scripts and pass on its one line asking for their handle or two or three videos where they talk. Deliver each script as its own block they can film, with its hook and source video above it.

**Check:** every row and idea links the video it rests on; every multiple came from Vamos; no idea is a bare category ("behind the scenes"); scripts use only their facts, with [your detail] where one is missing.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
