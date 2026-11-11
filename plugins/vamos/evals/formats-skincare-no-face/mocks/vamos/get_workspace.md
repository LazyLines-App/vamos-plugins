---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan": "PRO_MONTHLY", "brain": "Plain Barrier (a test brand): a small skincare brand with four products, competing on ingredient honesty, for people with reactive skin · niche: Skincare · pillars: Ingredient explainers, Routine building, What we do not sell", "voice": true, "files": ["Voice guide", "Vamos settings", "Things you've said", "What works for me", "Marketing plan"], "tracking": {"following": 3, "cap": 300, "accounts": ["@brand_one (instagram)", "@brand_two (tiktok)", "@brand_three (instagram)"]}, "routines": {"on": 0, "cap": 2, "list": []}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>"}.

### Voice guide
Clinical and unhyped. Names concentrations, admits what a product cannot do. No exclamation marks. Never opens on a rhetorical question.

### Vamos settings
Board: a Brain file called "Vamos board".
Platforms: Instagram, TikTok.
Ads: off.
Filming: no face on camera, ever: hands, product and text only; a voiceover is fine; one person films; simple edits.
Off limits: never claim a product cures or treats a condition; no before-and-after skin photos; never name or rate another brand's product.
Your calls: none yet.

### Things you've said
We sell four products, on purpose: a cleanser, a 3% ceramide barrier cream, an SPF 50 fluid and a 10% niacinamide serum.
Everything is fragrance-free.
We tell customers which of our products they don't need.

### What works for me
| Lesson | Status | Posts |
|---|---|---|
| Ingredient close-ups with the concentration on screen: 3 of 4 above my usual | Testing | 4 |

### Marketing plan
What we sell: four skincare products on our site.
90-day goal: 300 first orders.
The ask: "Comment ROUTINE and we'll send you the 4-step guide."
Posts by stage, last 20: reach 14, trust 5, buy 1. The thin stage is buy.
