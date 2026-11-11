---
description: "A scheduled ideas run as a fresh session, on RIP's demo workspace (@getripping, real free reads 2026-11-11 plus a Vamos settings file written for this test) with the board as a local file (fixture.sh). A type: agent chat_completion_start sends a load ask to fixtures/run-load.json (RIP's real Voice guide read, 2026-11-11, as a poll answer) and any other ask to fixtures/run-research.json (the real 11-11 ideas answer for @getripping, 51 credits). The prompt is a slash command, so the skill loads without a Skill call and there is no skill-fired grader. There is no saved answer for a whole loop run; the live 3-day run fills one. Approval is Ask me after ideas: only the Approved row gets a script, the 22-day-old row goes Stale, the fresh row stays, Not for me and Posted are untouched, new ideas land at To review, and the run ends with the digest. Run with --scaffold --allow-tools Write Edit Bash."
tags: [loop, scaffold, live-fills]
runs: 1
model: sonnet
max_turns: 60
timeout_seconds: 1500
allowed_tools: [Skill, Read, Glob, Grep]
---

/vamos:loop run ideas for RIP (@getripping on Instagram, Apps & SaaS). Board: vamos/board.md in this folder. Settings: the Vamos settings Brain file. Approval: Ask me after ideas.
