---
name: "creator-research"
description: "Finds creators for a brand to work with: UGC creators or influencers who get views in its niche, and people already posting about it, ranked, with usual views, bio contact and brand deals."
---
# Creator research

**The job:** a ranked list of creators the brand could hire, judged on the views they really get and on whether they fit, with the contact their bio shows. People already posting about the brand come first, because they already like it.

**Needs:** what the brand sells ("protein bars" is enough). When neither the ask nor the workspace brand gives it, ask for it in one short question before you send, because Vamos can't ask once it's working. `create_chat` shows the brand their Vamos workspace holds; use it rather than asking, and name a different brand in the ask when theirs is about one.

**Ask Vamos**, with `include_data: true`:
> Find [UGC creators / influencers] for [brand, product] on [platform] who get views [under N followers], starting with people already posting about [brand], with their usual views, the contact in their bio and any brand deals.

The list is the deliverable and runs long, so build it as a sheet from the rows, one per creator, in Google Sheets when it's connected, otherwise as a file, and say in your reply who stands out.

**Check:** before you reply, make sure Vamos's answer covers each part of what they asked; ask for what's missing in the same chat.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Vamos plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
