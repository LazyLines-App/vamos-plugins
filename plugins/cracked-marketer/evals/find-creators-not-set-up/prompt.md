---
description: 'Fresh workspace (this case''s own get_workspace, create_chat and get_credit_usage mocks: FREE plan, no voice, no files, nothing tracked). Levi, 11-11: find-creators does setup on its first run when the workspace isn''t set up, and never sets up twice. Tests that setup runs first and set_up_workspace is called at most once.'
tags: [find-creators, setup]
runs: 1
model: sonnet
max_turns: 24
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob]
---

Find creators to make UGC videos for my brand. I sell a barrier repair skincare serum ($38) to women 25 to 40. My Instagram is @glowbyamy and my site is glowbyamy.com. TikTok and Instagram, US.
