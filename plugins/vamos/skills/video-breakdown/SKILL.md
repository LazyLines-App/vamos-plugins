---
name: "video-breakdown"
description: "Watches any TikTok, Reel or Short and says why it worked: the hook, the beats, the comments, its views against the creator's usual, and the user's own version. Use for \"why did this go viral\"."
---
# Video breakdown

**The job:** why one video worked and how to make theirs: the hook (spoken and on screen), the beats, what the comments say, its multiple of the creator's usual, and their version.

**Needs:** the link. A video file can't be watched here, so when they attach one, ask for its link, because Vamos can't ask once it's working.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Give them Vamos's answer as it came, every link and number in it, and its `answerUrl` so they can open all of it in Vamos.

**Ask Vamos**, one message:
> Watch this and break it down: [link]. Why did it work, how did it do against the creator's usual, and what do the comments say? [How would I make my version for my niche?]

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
