---
description: "Claude Code, Zernio connected (mocked through this stub plugin), two finished videos in cuts/ with their post sheets, uploaded (urls.json). One video's caption asks viewers to comment GUIDE, and the user gives the checklist link. Tests the keyword DM's core check: the same table and the same yes carry the rule, the DM on Instagram with the link in it, the public reply on TikTok (no DM to a comment there), and nothing (no post, no rule) is created before the yes. Run evals/stubs/post-zernio/sync.sh, then claude plugin eval evals/stubs/post-zernio --scaffold --allow-tools Bash Write Edit 'mcp__plugin_post-zernio_zernio__*' 'mcp__plugin_post-zernio_vamos__*'."
tags: [post, zernio, scaffold, keyword-dm]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write, Edit]
---

Post the two videos in cuts/ to our Instagram and TikTok (@penny.app on both), one a day from tomorrow at 9am Madrid time. The mistakes one asks people to comment GUIDE: everyone who does should get the checklist, https://penny.app/checklist. They're uploaded already; the links are in urls.json.
