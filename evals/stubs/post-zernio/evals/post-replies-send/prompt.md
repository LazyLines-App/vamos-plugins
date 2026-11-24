---
description: "The yes turn of post-replies-draft: waiting.json, drafts.json and send.json are in the folder as replies.py left them (two replies, the spam skipped, Dana's price question asked of the user), and the user says yes without answering Dana. call_tool is an agent mock that gives each reply its own id. Tests that exactly the two approved replies go out, word for word, under the right comments, Dana's question gets no reply, and each sent reply is recorded in vamos/replied.json so it's never answered twice. Run evals/stubs/post-zernio/sync.sh, then claude plugin eval evals/stubs/post-zernio --scaffold --allow-tools Bash Write Edit 'mcp__plugin_post-zernio_zernio__*' 'mcp__plugin_post-zernio_vamos__*'."
tags: [post, zernio, scaffold, replies]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write, Edit]
---

Earlier you drafted replies to the comments on our posts (waiting.json, drafts.json and send.json are in this folder) and showed me the table. Yes, send them. I'll get back to you on the price question.
