---
description: "Set up here before: get_workspace lists Vamos settings and the other setup files (DERIVED from the real demo1 state after setup, with the six file titles added). The runner gives one answer per tool, so a file read returns the same state. The home visit must be free: no set_up_workspace and no billed Vamos turn, and it ends with where to edit and what to run next."
tags: [setup, home, derived-mock]
runs: 1
model: sonnet
max_turns: 16
timeout_seconds: 300
allowed_tools: [Skill, Read, Glob]
---

Run setup again for @getripping. What do you have set up for me in Vamos, where do I change it, and what should I run next?
