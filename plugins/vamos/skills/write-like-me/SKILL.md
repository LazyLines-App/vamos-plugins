---
name: write-like-me
description: Learns how the user talks from their own videos, then writes or rewrites scripts, hooks and captions in that voice, built on what's working. Use for "write like me", "make it sound less like AI".
---

# Write like me

**The job:** copy that sounds like them. Vamos builds a voice guide from the videos where they talk, saves it, and writes in it from then on.

**Inputs:** their handle, or two or three videos where they talk; what to write (a script on a topic, or a draft they paste to rewrite). Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Ask the user for a missing input before you send, because Vamos can't ask once it's working.

**Ask Vamos**, one message:
> Learn my voice from @handle, then [write a 30-second script about X / rewrite this so it sounds like me: …].

Once the voice is saved, "Write [X] in my voice" is enough.

**Deliver:** the piece, ready to film or post, and one line on what Vamos took from their voice (from its answer).

**Check:** it uses only their facts, with [your detail] where one is missing; the answer says which of their videos the voice came from.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
