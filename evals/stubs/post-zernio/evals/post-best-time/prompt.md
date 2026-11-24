---
description: "Claude Code, Zernio connected (mocked through this stub plugin), @vamos.demo on Instagram and TikTok, no Posting line yet. The user asks when to post. Zernio's answers: the posts are real readings of two of our accounts (the studio's last reading of each post, 2026-11-24), renamed @vamos.demo with every id remapped: 30 Instagram Reels, 23 of the 29 settled ones posted 15:00-18:00 Madrid time, and the 6 TikToks of the last year. The Instagram followers-online read is derived (Zernio's documented shape, made-up numbers; busiest 21:00, then 14:00 three hours clear). Answer key (evals/scripts/test_times.py): Instagram can't compare times, so 14:00 and 21:00 from followers online; TikTok's 6 posts are too few, so 13:00 and 19:00 as tests. Tests the core check of the times: proposed from the user's own numbers, each with its reason, honest about what the numbers can't tell, asked before anything is saved or posted. Run evals/stubs/post-zernio/sync.sh, then claude plugin eval evals/stubs/post-zernio --scaffold --allow-tools Bash Write Edit 'mcp__plugin_post-zernio_zernio__*' 'mcp__plugin_post-zernio_vamos__*'."
tags: [post, zernio, scaffold, best-time, assembled-mock]
runs: 1
model: sonnet
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write, Edit]
---

When should I post? I'm @vamos.demo on Instagram and TikTok, based in Madrid, and I want to post twice a day on each.
