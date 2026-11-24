---
type: tool_used
tool: mcp__plugin_post-zernio_zernio__call_tool
input_match: '^(?=[\s\S]*"comment_automations_create_comment_automation")(?=[\s\S]*"post_id"\s*:\s*"6750a1b2c3d4e5f6a7b8c90[1-9]")'
min: 1
---
The keyword rule is bound to the post Zernio just created (the id its create returned), so it arms when that post goes out and answers only that post's comments.
