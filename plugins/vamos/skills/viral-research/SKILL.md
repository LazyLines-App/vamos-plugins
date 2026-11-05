---
name: "viral-research"
description: "Finds what's going viral in a niche on TikTok, Instagram and YouTube, ranked against each creator's usual, then turns it into ideas and a week of scripts. Use for \"content ideas\", \"scroll for me\"."
---
# Viral research

**The job:** what's going viral in a niche right now and why, then what to make from it. Three steps; run the ones their ask covers, one after another.

**Needs:** the niche or topic. When neither the ask nor the workspace brand gives it, ask for it in one short question before you send, because Vamos can't ask once it's working. `create_chat` shows the brand their Vamos workspace holds; use it rather than asking, and name a different brand in the ask when theirs is about one.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Give them Vamos's answer as it came, every link and number in it, and its `answerUrl` so they can open all of it in Vamos.

**1. Research.** Ask Vamos:
> What's going viral in [niche] on [platforms] [this week]: the videos furthest past their creator's usual views, each with its hook, its format and why it worked.

When they want a sheet, send it with `include_data: true` and build the sheet from its rows, in Google Sheets when it's connected, otherwise as a file.

**2. Ideas.** Ask Vamos:
> Turn this into [7] ideas for my [platform] account, each built on one of these videos, with its hook. [I'm @handle.]

**3. Scripts.** Ask Vamos:
> Write scripts for [the ideas they picked, or the strongest seven for a week] in my voice.

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
