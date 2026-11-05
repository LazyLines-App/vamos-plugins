---
name: viral-research
description: Finds what's going viral in a niche on TikTok, Instagram and YouTube, ranked by how far each video beat its creator's usual views, then turns it into ideas and scripts in the user's voice.
---

# Viral research

**The job:** what's going viral in a niche right now and why, then what the user should make from it. Three steps, and the user can stop after any of them.

**Inputs:** the niche or topic; the platforms (default TikTok, Instagram and YouTube); the window (default this week); for ideas and scripts, their account or handle and what they sell or teach. Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Ask the user for a missing input before you send, because Vamos can't ask once it's working.

**1. Research.** Ask Vamos, with `include_data: true`:
> What's going viral in [niche] on [platforms] [this week]: the videos furthest past their creator's usual views, each with its hook, its format and why it worked.

Deliver a table, one row per video: the post (linked), creator, views, × usual, hook, format, why it worked. Numbers and links exactly as Vamos gave them; "why" from its answer. When they want a sheet, build it from the `include_data` rows plus the "why" column, in Google Sheets when it's connected, otherwise as a file.

**2. Ideas.** Ask Vamos:
> Turn this into [7] ideas for my [platform] account, each built on one of these videos, with its hook. [I'm @handle.]

Show each idea with its hook and the video it comes from, and ask which to write.

**3. Scripts.** Ask Vamos:
> Write scripts for [the picked ideas] in my voice.

When Vamos's answer says no voice is saved, ask for their handle or two or three videos where they talk, and send that first. Deliver each script as its own block they can film, with its hook and source video above it.

**Check:** every row and idea links the video it rests on; every multiple came from Vamos; no idea is a bare category ("behind the scenes"); scripts use only their facts, with [your detail] where one is missing.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
