---
name: "find-creators"
description: "Finds creators to pay for your brand's videos: people already posting about it, creators your rivals use, creators brands rehire and fresh breakouts, checked on niche and format, with their bio contact, in a sheet. Use for \"find UGC creators\", \"influencers for my brand\" or \"creators like @handle\"."
---

# Find creators

**The job:** a sheet of creators the brand could pay, every one Vamos found, each with how well they fit and how to reach them, and the few to start with. The user sends every message; this skill never contacts anyone.

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` (free) tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas, hooks and scripts need it, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** Open a Vamos chat with `create_chat` once per job, send each ask with `chat_completion_start`, and call `chat_completion_poll` until it's done. Follow-ups go in the same chat. Add `include_data: true` when you need the rows (with `include_transcripts: true` for up to 10 transcripts, and `data_format: "inline"` when you can't fetch a link). The rows are the posts the answer links; add `data_scope: "turn"` for every post the research read. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50, so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file` (free; `when_to_use` makes it a skill), always as its whole text, so read one first to add to it. The voice guide, content plan and profile notes change only in a Vamos chat, each as its own `chat_completion_start` message ("Save this as …"). Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** `get_credit_usage` and `get_messages` are free. Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 3 days old, leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. When Vamos answers that no file has that name, its error lists the exact names: retry once with the right one. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer:

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/cracked-marketer:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**0. Check, free.** `get_workspace` and `get_credit_usage`. A fresh workspace (no voice, nothing tracked, no pillars, no Vamos settings) gets setup first: say so in one line, start the setup skill yourself (never ask them to type a command), then come back to the creators. One that has any of those is set up, so never set it up again.

**1. The brief.** Take from the ask, then the workspace: what the brand sells and to whom, the niche, and its rivals (brands they name, else the tracked accounts that are brands, not creators). Ask one short question only when you can't tell what they sell. For the rest use their words, else these defaults (a handle they give names the brand, not the platforms): TikTok and Instagram, 5K to 100K followers, the brand's country, posted in the last 30 days, 25 creators.

**2. One research turn,** `create_chat` ("Creators: [brand]"), then `chat_completion_start` without `include_data`: the sheet comes from the answer's tables, because the rows hold about half the creators and no emails. Say first that a turn bills up to 60 credits and takes 7 to 15 minutes. Send:

> For [brand], [what it sells, to whom][ (this is about [brand], not my workspace's brand)]: find [25] creators on [platforms] we could pay to make videos for it. Niche: [niche]. Start with people already posting about [brand] or [category], then creators who've made partnership ads or tagged posts for [rivals], creators who've worked with 2 or more [category] brands, and creators whose latest video did far better than their usual with no brand deal yet. Keep only [5K to 100K] followers, based in [country], posted in the last 30 days. For each, read their last 6 posts and say how many are about [niche] and in how many they talk to camera[, and whether they film [the format they asked for]]; anyone under 3 of 6 on topic is a near miss. Two tables: creators with an email in their bio, then those whose only contact is a link in bio or a DM. Columns: handle, platform, followers, usual views, country, on topic (N of 6), talks to camera (N of 6), format, brand deals seen (any [category] brand, with when), contact, where you found them, why they fit. Then the near misses, each with what it misses.

Name the category's brands as a category ("any creatine, protein or supplement brand"), because Vamos flags a rival only when the ask says what counts as one. The "(this is about…)" part goes in only when `get_workspace` shows another brand. Search the niche, never "UGC creator", which finds people who teach UGC.

**3. More, when they asked for more than came back.** In the same chat: "Find [N] more on the same brief, none from your lists above." Price it first. Stop after 3 turns in all, or sooner when a turn adds fewer than 3 new creators; a handle you already have is a repeat, not a find.

**4. The sheet,** per [references/sheet.md](references/sheet.md): every creator from every table, one row each, nothing cut, in Google Sheets when it's connected, else `creators-[brand].csv`. Copy each contact exactly as Vamos gave it. A check Vamos didn't give reads "not checked". A creator under 3 of 6 on topic, outside the brief, or selling a rival product goes in the Near miss list with the reason. One who has posted for a rival stays on the Main list with the deal flagged as a check before paying: they've made paid videos in the category, and only they can say whether the deal is exclusive.

**5. Contacts past the bio.** Vamos reads only the email written in a bio. When the user has an Apify connector, offer to read the link-in-bio pages and Instagram contact buttons of the no-email rows on their own account, with the price (Apify lists about $4 per 1,000 Instagram profiles and $0.005 per email found on link pages), and run it only on their yes. Never sign in to a platform, guess a real name behind a handle, or get past a CAPTCHA. Otherwise the contact is the link in bio, or "DM".

**6. A first message per creator,** in the sheet, for the user to send. Write it per [references/sheet.md](references/sheet.md): about their own posts, the pay per video, no link.

**7. Hand it over**, opening on the count. For example:

> 11 creators fit the sourdough-kit brief, 8 with a bio email, in creators-crumb.csv, plus 6 near misses. Start with @a.bakes (bakes on camera and talks the whole way, 14,200 usual views), @b.loaves and @c.kitchen. Check before paying: @b.loaves's bio has a code for a flour brand. Nobody can see audience age or private deals, so ask each for an Insights screenshot. 120 credits over 2 turns, about 11 per creator who fits.

Then offer, priced, the next step that fits: another turn for more, or a read of the top 3 to 5 before paying: "For @a, @b and @c on [platform]: read each one's last 30 posts, their median views and the median of their 10 worst, every partnership ad, brand tag or discount code, and whether each recent breakout is organic (likes against views, no paid label)."

**Check before the recap:** the sheet's row count equals the distinct creators in Vamos's tables; every email in it appears in Vamos's answer on that creator; no main-list row is under 3 of 6 on topic or sells a rival product, and every rival deal is flagged; "posted for" or "partnership ad with", never "paid by", since an ad proves permission, not payment; nothing was sent; the reply gives credits per creator who fits (credits used over the Main list's count). Next is `/cracked-marketer:creator-program`, what to pay them and how to start.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
