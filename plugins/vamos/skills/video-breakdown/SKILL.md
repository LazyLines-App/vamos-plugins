---
name: video-breakdown
description: Watches any TikTok, Reel or Short and breaks it down: the hook, the beats, the comments, how it did against the creator's usual views, why it worked, and the user's own version.
---

# Video breakdown

**The job:** why one video worked and how to make theirs: the hook (spoken and on screen), the beats, what the comments say, its multiple of the creator's usual, and their version.

**Inputs:** the link (a video file can't be watched here, so ask for the link); their niche, for their version. Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Ask the user for a missing input before you send, because Vamos can't ask once it's working.

**Ask Vamos**, one message:
> Watch this and break it down: [link]. Why did it work, how did it do against the creator's usual, what do the comments say, and how would I make my version for [my niche]?

**Deliver:** the hook word for word (spoken and on screen), the beats, comment themes with counts, the multiple with its views, why it worked, their version.

**Check:** quotes come word for word from the transcript or the screen; the multiple came from Vamos.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
