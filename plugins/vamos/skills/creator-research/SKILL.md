---
name: creator-research
description: Finds creators for a brand to work with: UGC creators or influencers who get views in its niche, and people already posting about it, ranked, with usual views, bio contact and brand deals.
---

# Creator research

**The job:** a ranked list of creators the brand could hire, judged on the views they really get and on whether they fit, with the contact their bio shows. People already posting about the brand come first, because they already like it.

**Inputs:** the brand and product; UGC creators (who make ads for brands), influencers (who post to their own audience), or both; the platform; any follower or budget limit. Send each ask with the Vamos connector's `chat_completion_start` and poll until it's done; follow-ups go in the same Vamos chat. Ask the user for a missing input before you send, because Vamos can't ask once it's working.

**Ask Vamos**, with `include_data: true`:
> Find [UGC creators / influencers] for [brand, product] on [platform] who get views [under N followers], starting with people already posting about [brand], with their usual views, the contact in their bio and any brand deals.

**Deliver:** a sheet, one row per creator: the creator (linked), followers, usual views, how often they beat it, contact from their bio, brand deals (rivals flagged), the verdict. Build it from the `include_data` rows, in Google Sheets when it's connected. Then the near misses, one line each with the bar they miss.

**Check:**
- Every creator is an account Vamos returned.
- Contact comes only from what their bio shows.
- A creator who already works with a rival is flagged, not dropped.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
