---
name: "creator-research"
description: "Finds creators for a brand to work with: UGC creators or influencers who get views in its niche, and people already posting about it, ranked, with usual views, bio contact and brand deals."
---
# Creator research

**The job:** a ranked list of creators the brand could hire, judged on the views they really get and on whether they fit, with the contact their bio shows. People already posting about the brand come first, because they already like it.

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas need it, and so do hooks and scripts while its `voice` is false, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. On an ask about their own brand, every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** One Vamos chat per job (`create_chat`); follow-ups go in it. Add `include_data: true` when you need the rows. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50 posts (30 ads, creators or formats), so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **The ask decides.** A brand, niche or platform the user names wins over the workspace's, so run their ask as they put it, in the same turn. Name the brand, niche and platforms in every Vamos ask, because the workspace may be about another brand. For a niche their brand isn't in, ask about that niche in general, and open the reply with that scope in a few words ("Fitness accounts in general, on TikTok, Instagram and Shorts.").
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file`, always as its whole text, so read one first to add to it. Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** Run what the ask needs and report the cost in the recap; ask first only when what they have left is below a step's cost. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 7 days old (views still climb before that), leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). A younger post that already beats it shows as "N× so far"; one that doesn't is too early to judge. Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, do the same check yourself in a separate pass that reads only that text.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. Never spend a turn reading one.

**End every run with the recap** in the chat, and as the last line of the page when the skill makes one. Next is the step this skill names, and when it names a choice, offer each. When it can run now, offer it as a question and, on their yes, run it yourself, so they never need to remember a command; when it waits on them or on time (filming, a post's first week), say what and when.

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Board:** [its link, when there is one] · **Next:** [what it does, in eight words] (`/vamos:[skill]`). Shall I?
<!-- /shared -->

**Needs:** what the brand sells ("protein bars" is enough). When neither the ask nor the workspace brand gives it, ask for it in one short question before you send, because Vamos can't ask once it's working. `create_chat` shows the brand their Vamos workspace holds; use it rather than asking, and name a different brand in the ask when theirs is about one.

**Ask Vamos**, with `include_data: true`:
> Find [UGC creators / influencers] for [brand, product] on [platform] who get views [under N followers], starting with people already posting about [brand], with their usual views, the contact in their bio and any brand deals.

The list is the deliverable and runs long, so build it as a sheet from the rows, one per creator, in Google Sheets when it's connected, otherwise as a file, and say in your reply who stands out. Each creator's line is about their content, audience, views, deals and contact, because the list gets passed around a team.

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Vamos plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
