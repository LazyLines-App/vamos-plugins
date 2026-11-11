---
description: Smoke case for the mock plumbing. The workspace is already set up (the suite's get_workspace mock), the user asks for setup anyway, and set_up_workspace must never be called. Since 34c5029 the skill reads get_workspace first, so this passes; a failure is a finding about the skill.
tags: [smoke, setup, mocks]
runs: 1
model: sonnet
max_turns: 12
timeout_seconds: 240
allowed_tools: [Skill]
---

Set Vamos up for my brand. My Instagram is @glowbyamy, my site is glowbyamy.com, and I sell a skincare serum.
