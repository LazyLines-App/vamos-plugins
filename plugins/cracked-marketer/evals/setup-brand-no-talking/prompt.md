---
description: "Cracked marketer setup for a brand whose account has nobody talking on camera (Notion, a public B2B app). Mocks copied from the Content System case setup-elsewhere-notion: get_workspace derived from a real demo workspace's state (set up elsewhere, voice false, no Brain files, 6 tracked) and the real research answer from 2026-11-11 (32 credits, 13 @notionhq rows with captions and transcripts). Tests that the research turn reads the site, captions and Meta ads instead of 'videos where I talk', rebuilds the voice from how they write (voice is false), and that Vamos settings records a written voice."
tags: [setup, cracked-marketer, written-voice, real-mock]
runs: 1
model: sonnet
max_turns: 40
timeout_seconds: 1200
allowed_tools: [Skill, Read, Glob, Bash, Write]
---

Set up Vamos for my brand. I'm @notionhq on Instagram, site notion.com. Notion is a workspace app for notes, docs, projects and AI agents; we sell to teams and companies (Free, then Plus at about $10 per seat, then Business). A competitor I know is @clickup. No creators yet. Nobody on our team talks to camera: our posts are product demos with text and a voiceover, plus customer stories. We run Meta ads. Goal for the next 90 days: more team workspaces signing up, then upgrading. That's everything, go ahead.
