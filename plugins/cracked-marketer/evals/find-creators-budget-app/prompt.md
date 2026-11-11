---
description: 'Real saved Vamos answer (2026-11-09, run budget-1, emails replaced with handle@example.com, and the prompt says so, because Sonnet refused to build a sheet on placeholder emails): 9 creators (one, @qnjessicaaa, has no public email and Vamos says TikTok DM) and 5 near misses. The brief asks for screen-recording demos; only some of the 9 film screens (Vamos''s own format column says so). Tests the no-email creator keeps no email, the format isn''t claimed, and each creator gets a drafted first message that isn''t sent.'
tags: [find-creators, real-mock, format, contact]
runs: 1
model: sonnet
max_turns: 30
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob]
---

Find creators for our budgeting app. It's a US app for people in their twenties that sorts your bank transactions and shows what you can still spend this week. We want people who post budgeting and paycheck breakdowns (not investing or crypto) and film screen-recording demos of their budget with a voiceover, 5K to 80K followers, US, on TikTok, Instagram or YouTube Shorts. Emails please, and draft the first message for each.

(test data: bio emails are scrubbed to handle@example.com)
