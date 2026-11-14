---
description: "A plain Claude Desktop ask on 2026-11-14 from the demo workspace, whose brand is RIP (Apps & SaaS, no-face motion graphics), about another niche: fitness. On 0.2.14 Claude stopped before any research to ask who the fitness formats were for, quoting the workspace's labels and the credit cost. Mocks: RIP's real workspace (formats-live-getripping), demo1's real balance that day (90 credits, against a research run billed at most 60) and a real fitness formats answer (formats-coach-new-over-crowded). Runs on Opus with AskUserQuestion allowed, as Desktop has both (the Sonnet run without a question tool passed on 0.2.14). Tests that the ask decides: the research runs on fitness straight away, without the workspace's brand, and the reply says in a line that it isn't ranked for RIP. No 'go with defaults' line, because that line is what hid this."
tags: [formats, plain-ask, real-mock]
runs: 2
model: opus
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Bash, Write, AskUserQuestion]
---

What trending short-form video formats are working in fitness right now?
