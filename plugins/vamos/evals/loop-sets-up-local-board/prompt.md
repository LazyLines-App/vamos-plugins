---
description: "Notion's demo workspace (real free reads, 2026-11-11, Free plan, 153 credits) after a full setup that left the board as a local file. The user gives every answer. Tests: the price from get_credit_usage against 153; the board moved off the laptop (no Notion or Google tool here, so the Vamos board Brain file) before any cloud schedule; the board and the settings saved free with save_brain_file (the suite mock answers created), and no recurrence word in any Vamos ask; the scheduled task's prompt runs the loop with the board and the approval setting. From before save_brain_file, kept for any chat ask: a type: agent chat_completion_start picks a fixture by what the message saves (board, settings, both, other); run-save-board is the real answer from the live loop run on demo1 (2026-11-11 13:26 UTC, 1 credit; brand RIP/@getripping swapped to Notion/@notionhq) and run-save-settings the real answer from the second live run (2026-11-11 17:06 UTC, 1 credit, the exact settings ask of the current skill; it names no time zone, so the runner's own zone cannot clash with it); run-save-both and run-other are the earlier real 11-11 save turn (15 credits) with its file list cut to what that message saved. Run with --scaffold (fixture.sh writes vamos/board.md)."
tags: [loop, real-mock, scaffold]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep]
---

Set our content system to run by itself, even with my laptop closed. Stop after ideas so I can approve them. Ideas on Monday and Thursday mornings, the content log on Monday. I'm in Claude Code. Go ahead even if my credits only cover a week, I'll upgrade.
