---
name: competitor-research
description: Tears down a competitor, brand or category: posts that beat their usual, the Meta ads they keep running, the creators they pay and how, and what to copy. Use for a brand's ads or creator program.
---
# Competitor research

**The job:** everything that works for a competitor, in one report: their posts that beat their usual on TikTok, Instagram and YouTube, the Meta ads they've kept running longest, the creators and partners they pay and how that program runs, what to copy and the gap they leave.

**Needs:** the competitor (a handle, a link or a brand name), several of them, or a category. "My competitors" needs a workspace brand; when there is none, ask which brands they mean in one short question, because Vamos can't ask once it's working. `create_chat` shows the brand their Vamos workspace holds; use it rather than asking, and name a different brand in the ask when theirs is about one.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Give them Vamos's answer as it came, since it's written for them.

**Ask Vamos**, one message, for the whole teardown; when they ask about one part (their ads, their creators, what their audience asks in the comments), ask for that part alone, as fully:
> Break down [competitor] as a competitor of [brand name]: their organic posts on TikTok, Instagram and YouTube that beat their usual, the Meta ads they keep running longest, the creators they pay and how that program works, and what I should copy.

With no competitor named: "Find my top competitors for [brand name] and break them down the same way."

When they want the program for themselves: "Build me a creator program like theirs for [brand name] at [budget or goal]."

When they want a sheet of every post and ad, read the answer back with `get_messages` and `include_data: true` and build it from the rows.

**Next:** offer a weekly watch: send "every Monday, send me what they posted and launched" to the same chat.

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
