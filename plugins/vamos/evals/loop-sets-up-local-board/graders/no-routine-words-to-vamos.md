---
type: tool_used
tool: mcp__plugin_vamos_vamos__chat_completion_start
input_match: '\b([Ee]very (day|week|weekday|weekend|morning|month|hour|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|night|evening)|EVERY|[Dd]aily|[Ww]eekly|[Ss]chedul\w*|[Rr]outines?)\b'
min: 0
max: 0
---
# G4 (regex narrowed 2026-11-11 to recurrence phrases, so the user's own words such as "every teammate" in a whole-file save do not count): a recurrence word in what Claude sends Vamos can save a Vamos Routine (switched off since #1471, still a slot and clutter). Scheduling lives in the host, never in a Vamos ask.
