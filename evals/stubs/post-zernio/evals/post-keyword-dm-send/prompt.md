---
description: "The yes turn of post-keyword-dm: the batch planned earlier is in the folder (batch.json, the GUIDE video's comment_dm with the checklist link in it), and the user says yes. Zernio is mocked; call_tool is an agent mock that gives each created post its own id. Tests that each keyword rule goes out after its post with that post's id (so Zernio arms it when the post publishes), the DM with the link on Instagram, no DM on TikTok, and no rule on the video that doesn't ask. Run evals/stubs/post-zernio/sync.sh, then claude plugin eval evals/stubs/post-zernio --scaffold --allow-tools Bash Write Edit 'mcp__plugin_post-zernio_zernio__*' 'mcp__plugin_post-zernio_vamos__*'."
tags: [post, zernio, scaffold, keyword-dm]
runs: 1
model: sonnet
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write, Edit]
---

Earlier you planned my two videos in this folder (batch.json) and showed me the table, with the GUIDE DM for the mistakes one. Yes, post them.
