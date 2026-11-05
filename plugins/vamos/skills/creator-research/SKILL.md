---
name: creator-research
description: Finds creators for a brand to work with: UGC creators or influencers who get views in its niche, and people already posting about it, ranked, with usual views, bio contact and brand deals.
---

# Creator research

**The job:** a ranked list of creators the brand could hire, judged on the views they really get and on whether they fit, with the contact their bio shows. People already posting about the brand come first, because they already like it.

**Needs:** what the brand sells ("protein bars" is enough). When neither the ask nor the workspace brand gives it, ask in one short question before you send, because Vamos can't ask once it's working.

**Defaults** (don't ask; name the ones you used in one line with the answer): both UGC creators and influencers unless they named one; TikTok, Instagram and YouTube unless they named one; no follower limit; people already posting about the brand when they named it. `create_chat` returns the brand their Vamos workspace holds, so use that brand rather than asking for it; when their ask is about a different brand, name that one in the ask.

Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. The user sees only what you show them, so carry Vamos's answer over whole (every row, hook, script and link) rather than pointing them to the Vamos chat.

**Ask Vamos**, with `include_data: true`:
> Find [UGC creators / influencers] for [brand, product] on [platform] who get views [under N followers], starting with people already posting about [brand], with their usual views, the contact in their bio and any brand deals.

**Deliver:** every creator Vamos returned, not a sample, as a sheet, one row per creator: the creator (linked), followers, usual views, how often they beat it, contact from their bio, brand deals (rivals flagged), the verdict. Build it from the `include_data` rows, in Google Sheets when it's connected. Then the near misses, one line each with the bar they miss.

**Check:**
- Every creator is an account Vamos returned.
- Contact comes only from what their bio shows.
- A creator who already works with a rival is flagged, not dropped.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
