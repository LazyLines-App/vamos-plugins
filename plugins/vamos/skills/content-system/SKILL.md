---
name: content-system
description: Runs the user's content research every week while they sleep: sets up voice and competitors, a Monday email of what to post, and a weekly review that writes next week's posts and learns from them.
---

# Content system

**The job:** a loop that gets better every week. Research what's working, analyze how their own posts did, create next week's content in their voice, and learn: save what worked so the next week starts from it.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat.

## Set it up (once)

**Needs:** their accounts (handles or links) and what they sell and to whom. Ask for both in one short message before you start, with their website if they have one, because Vamos can't ask once it's working and setup built on guesses writes a generic week.

1. Call the Vamos connector's `set_up_workspace` with their accounts, website and what they do, and poll it until done. Vamos reads their posts, builds their profile, pillars and voice, and follows creators in their niche. Once their account and five creators are tracked, the free Weekly brief starts.
2. Ask Vamos:
   > Track [the competitors they named / my top competitors].
3. Before scheduling, say what it costs: each weekly run spends Vamos credits (a research run is usually 20 to 60; `get_credit_usage` shows what they have), and Free allows one routine. Then ask Vamos:
   > Every [Monday at 8:00], send me what went viral in my niche and from my competitors that week, how my own posts did against my usual and why, and the three posts I should make next.

   Vamos saves it as a routine that emails each run.

Deliver what was set up: the accounts read, the voice, the competitors tracked, and the routine with the date of its first run.

## Each week (when they ask, or as a Claude scheduled task on a paid plan)

1. **Research and analyze.** Ask Vamos:
   > Review my week: which of my posts beat my usual and why, which didn't, and what went viral in my niche and from my competitors.
2. **Learn.** Pick the two or three lessons that answer shows, with their numbers, and ask Vamos in its own message, since Vamos saves on a turn that isn't researching:
   > Save to my content plan what we learned this week: [the lessons].
3. **Create.** Ask Vamos:
   > Plan next week: [N] posts built on what's working and what we learned, each with its hook and the video it builds on.

   Then, for the ones they pick:
   > Write scripts for [the picked ones] in my voice.

Deliver the week in one place: what worked and what didn't (linked, with multiples), the lessons saved, next week's plan, the scripts.

**Check:**
- Report as saved only what Vamos confirmed it saved.
- Every lesson carries a number Vamos gave.
- Every idea links the video it builds on.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
