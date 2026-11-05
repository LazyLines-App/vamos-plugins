---
name: "write-like-me"
description: "Learns how the user talks from their own videos, then writes or rewrites scripts, hooks and captions in that voice, built on what's working. Use for \"write like me\", \"make it sound less like AI\"."
---
# Write like me

**The job:** copy that sounds like them. Vamos builds a voice guide from the videos where they talk, saves it, and writes in it from then on.

**Needs:** what to write (a script on a topic, or a draft they paste to rewrite), and where their voice comes from: their handle, or two or three videos where they talk. When `create_chat` shows an empty workspace and they gave neither, ask for their handle in one short question, because Vamos can't ask once it's working. Rewriting a pasted draft needs only the draft.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Give them Vamos's answer as it came, every link and number in it, and its `answerUrl` so they can open all of it in Vamos.

**Ask Vamos**, one message:
> Learn my voice from @handle, then [write a 30-second script about X / rewrite this so it sounds like me: …].

Once the voice is saved, "Write [X] in my voice" is enough.

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
