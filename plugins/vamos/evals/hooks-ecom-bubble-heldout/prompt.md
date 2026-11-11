---
description: "Held out from round 3's fixes: a public DTC skincare brand (Bubble Skincare, Slam Dunk Hydrating Moisturizer) asks, from a workspace set up for another brand (the demo test brand RIP), for hooks for a talking-to-camera UGC ad on TikTok and Instagram, chat only. The mock is the live vamos-demo answer of 2026-11-11 to the round-3 ask (60 credits, 20 rows ranked by views, paid partnerships left out); get_workspace is the RIP workspace. The prompt does not name the skill: on 2026-11-11 it did not route until "in your voice" and "keeps them as your hook database" left the description (0 of 3 before, 3 of 3 after, mocked). Tests the ad format (the product on screen by 3 s), borrowing a viral talking-to-camera sentence rather than an expert's tip, and no save when asked not to."
tags: [hooks, research, ad, held-out, real-mock]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Bash, Write]
---

write hooks for a UGC ad for Bubble Skincare's Slam Dunk Hydrating Moisturizer: a creator talking to camera, for TikTok and Instagram. This workspace is set up for my other brand, so write for Bubble, not that brand's voice. Keep the hooks in this chat, don't save them to my board. I won't be around to answer questions, so go with sensible defaults.
