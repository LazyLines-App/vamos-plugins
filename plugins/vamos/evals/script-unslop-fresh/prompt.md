---
description: "The unslop promise on a short-form script (\"paste your draft into /vamos:script, a free Claude skill that cuts these and leaves a blank for your story\"). A fresh workspace (Free, nothing set up: formats-thin-answer-no-setup's real empty read) pastes a reel script in plain Claude's own format, holding the seven tells Claude writes most in short-form scripts against viral ones (evals/scripts/measure_tells.py): asterisks inside a line, \"That's not X. That's Y.\", \"isn't about X. It's about Y.\", an unsourced \"Research shows\", \"The best part?\", \"Save this\" and \"follow for more\". Its hook, and the caption, is a story the AI made up about them. The rewrite runs before setup and with no paid turn, cuts every tell, keeps the draft's facts, and leaves the made-up story as [your …] slots. The prompt is a slash command, so the skill loads without a Skill call and there is no skill-fired grader."
tags: [script, rewrite, tells, short-form, no-setup, promise]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write]
---

/vamos:script make this sound less like AI. It's a reel for my bakery's Instagram. I won't be around to answer questions, so go with sensible defaults.

# 30-Second Reel: How My Bakery Grew on Instagram

**[0:00–0:03] HOOK**
*Visual: You pulling the first tray of croissants out of the oven, steam rising.*
**VO:** "I had 40 followers and a tray of burnt croissants. Here's what changed."

**[0:03–0:12] THE CHANGE**
*Visual: Phone propped against the flour bin, filming the oven door.*
**VO:** "I post one reel **every single morning**: the first tray coming out of the oven. That's not a content plan. That's just my morning."

**[0:12–0:22] WHY IT WORKS**
*Visual: Close-up of hands scoring dough, then the counter at 7 a.m.*
**VO:** "Research shows people trust a business more when they see the work behind it. The best part? It takes me two minutes. Posting isn't about perfect videos. It's about showing up."

**[0:22–0:30] CTA**
*On-screen text: "First tray out at 7 ☕"*
**VO:** "Save this for your next post, and follow for more behind the scenes. Come by at 7 for the first tray."

**Caption:** From 40 followers and burnt croissants to this 🥐 Come by at 7 for the first tray.
