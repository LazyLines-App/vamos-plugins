---
description: "A no-face skincare brand (test brand Plain Barrier) asks which formats to make. Mock assembled from a real Vamos agent run on 2026-11-10 (asks-v3, skincare fit5, $0.61 agent): the answer text, whose best example links a profile, not a post, and format rows built from the plan it read (16 formats, 48 examples; nothing rising). Tests the face and claims limits as a gate, white space over the crowded staples, profile links dropped, and numbers kept to the answer and rows."
tags: [formats, assembled-mock]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Bash, Write]
---

which video formats should we make next? I won't be around to answer questions, so go with sensible defaults.
