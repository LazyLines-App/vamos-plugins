---
name: video-breakdown
description: Watches any TikTok, Reel or Short and says why it worked: the hook, the beats, the comments, its views against the creator's usual, and the user's own version. Use for "why did this go viral".
---

# Video breakdown

**The job:** why one video worked and how to make theirs: the hook (spoken and on screen), the beats, what the comments say, its multiple of the creator's usual, and their version.

**Needs:** the link. A video file can't be watched here, so when they attach one, ask for its link, because Vamos can't ask once it's working.

**Defaults** (don't ask): their version for the workspace's niche, or for the niche the video is in when the workspace has none. When they ask whether to post their own video, that's the content-strategy check, not this.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. The user sees only what you show them, so carry Vamos's answer over whole (every row, hook, script and link) rather than pointing them to the Vamos chat.

**Ask Vamos**, one message:
> Watch this and break it down: [link]. Why did it work, how did it do against the creator's usual, what do the comments say, and how would I make my version for [my niche]?

**Deliver:** the hook word for word (spoken and on screen), the beats, comment themes with counts, the multiple with its views, why it worked, their version.

**Check:** quotes come word for word from the transcript or the screen; the multiple came from Vamos.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
