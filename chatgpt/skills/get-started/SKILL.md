---
name: get-started
description: Set up the user's Vamos workspace from their social accounts, website and what they do, so its research and writing fit their brand. Use when the user first connects Vamos, asks to set it up, or a Vamos tool reports the workspace has nothing set up.
---

Vamos fits every answer to the workspace's brand, voice and the creators it follows. A new workspace has none of these, so its answers stay generic until it is set up.

1. Call `get_workspace` first; it's free. If the workspace already has a voice, tracked accounts or pillars, it is set up: don't call `set_up_workspace`, because a second setup bills again and can undo the first. Tell the user in one line that Vamos already knows their brand, and start their request.
2. Otherwise, in one message, ask the user for:
   - their social accounts: @handle and platform, or profile links (Instagram, TikTok, YouTube, LinkedIn, X, Facebook);
   - their website, if they have one;
   - in their own words, what they do, what they sell and who it is for.

   Setup needs at least one account or the website, because it reads them.
3. Call `set_up_workspace` with `accounts`, `website` and `about` from what the user shared, in their words. Leave out anything they did not give.
4. Call `chat_completion_poll` with the `runId` it returns until `status` is `done`. Setup reads their profiles and site, so it takes a few minutes.
5. From the `result`, tell the user what Vamos set up (brand profile, content pillars, voice, the creators it now follows) and anything it still needs from them.

If the user arrived with a request, start it with the Vamos skill that fits it and ask for these details in the same reply: setup runs in its own chat, alongside their request.

The user's instructions take precedence over this skill.
