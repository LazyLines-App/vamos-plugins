---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan": "PRO_MONTHLY", "brain": "Fieldnote (a test brand): a two-person studio that turns B2B software companies' customer calls into short-form video · niche: Business & Marketing · pillars: Objections from real calls, Sales-call teardowns, Operator notes", "voice": true, "files": ["Voice guide", "Vamos settings", "Things you've said", "What works for me", "Marketing plan"], "tracking": {"following": 2, "cap": 300, "accounts": ["@operator_one (instagram)", "@operator_two (tiktok)"]}, "routines": {"on": 0, "cap": 2, "list": []}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>"}.

### Voice guide
Dry, specific and slightly contrarian. An operator talking to another operator. British spelling. Never open with a definition or a statistic. Prefers "we found" over "studies show".

### Vamos settings
Board: a Brain file called "Vamos board".
Platforms: Instagram, TikTok (and LinkedIn by hand).
Ads: off.
Filming: the founder on camera, phone in hand, one take, one location; text overlays only, no motion graphics.
Off limits: never open with a statistic we cannot source; refer to clients as "the client", never "brands" or "partners"; no client names on screen.
Your calls: none yet.

### Things you've said
We work with 6 clients at a time, mostly Series A B2B software companies.
We started in 2023 running content for a logistics SaaS.
Each client gets four pieces a week the founder can film in one sitting.
Our hooks come word for word from objections in the client's recorded sales calls.

### What works for me
| Lesson | Status | Posts |
|---|---|---|
| A real objection as the first line, answered to camera in 40 seconds: 3 of 4 above my usual | Testing | 4 |

### Marketing plan
What we sell: a monthly video retainer for B2B software companies.
90-day goal: 2 discovery calls a week from organic.
The ask: "Book a 20-minute call from the link in bio."
Posts by stage, last 20: reach 9, trust 10, buy 1. The thin stage is buy.
