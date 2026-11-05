---
name: get-started
description: Sets up Vamos for the user from their social accounts and site (profile, voice, creators to follow), then offers their first three asks. Use right after install, or for "set up Vamos".
---

# Get started

**The job:** a workspace that knows the user, so every later answer is about them, then a first result in the same sitting.

1. Call the Vamos connector's `auth_status`. When it isn't signed in, give the sign-in link it returns and stop until they're back.
2. **Needs:** their social accounts (handles or links) and what they sell and to whom, with their website if they have one. Ask for all of it in one short message, because setup built on guesses gives generic answers.
3. Call `set_up_workspace` with what they gave and poll it with `chat_completion_poll` until it's done. Vamos reads their posts, builds their profile, pillars and voice, and follows creators in their niche.
4. **Deliver** what was set up, as Vamos reported it: the accounts it read, their pillars, the voice, the creators it now follows. Once their account and five creators are tracked, the free Weekly brief starts arriving by email.
5. **Offer three first asks**, written for their niche and accounts, for example: what went viral in their niche this week; a breakdown of a competitor they named; whether an idea they have is worth posting.

**Check:** report as set up only what Vamos confirmed.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
