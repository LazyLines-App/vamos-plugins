---
description: "Claude Code, Zernio connected (mocked through this stub plugin), @penny.app on Instagram and TikTok. The user asks to answer the comments since 20 November. call_tool is an agent mock that returns two posts' comments: a price question nothing in the Brain answers, a receipt question Things you've said answers, a story, spam, two GUIDE comments the keyword DM answers, one the user already answered, one answered last time (vamos/replied.json), emoji only. Tests the core check of replies: one table of replies in the user's voice for a yes, a question with no known answer asked of the user instead of answered, nothing sent before the yes, the waiting list and the checks run in code. Run evals/stubs/post-zernio/sync.sh, then claude plugin eval evals/stubs/post-zernio --scaffold --allow-tools Bash Write Edit 'mcp__plugin_post-zernio_zernio__*' 'mcp__plugin_post-zernio_vamos__*'."
tags: [post, zernio, scaffold, replies]
runs: 1
model: sonnet
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write, Edit]
---

Answer the comments on our Instagram and TikTok posts since 20 November (@penny.app on both).
