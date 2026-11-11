---
description: "A two-person B2B video studio (test brand Fieldnote, the Chat eval's fixture) asks which formats to try. Mock assembled from a real Vamos agent run on 2026-11-10 (asks-v3, fieldnote fit5, $0.47 agent): the answer text, which invents two claims and links one profile, and format rows built from the plan it read (11 formats, 33 examples). Tests that invented numbers stay out, the content rules hold in every angle, and white space gets its slot."
tags: [formats, assembled-mock]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Bash, Write]
---

what short-form formats should we try? most of what I see feels made for influencers, not B2B. I won't be around to answer questions, so go with sensible defaults.
