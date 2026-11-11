---
type: tool_used
tool: mcp__plugin_vamos_vamos__save_brain_file
input_match: '"title"\s*:\s*"What works for me'
min: 1
weight: 0.5
---
# The next run reads its lessons from What works for me, so the run saves it (free). The suite's save_brain_file mock always answers "created", so a save claim is true exactly when this call was made; the trace-read no-unconfirmed-save was dropped for that reason (its judge sees a cut trace on this long run and failed a run whose call it couldn't see).
