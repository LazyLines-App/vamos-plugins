---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan":"PRO_MONTHLY","brain":"Hollow Peak Active (a test brand): a small activewear brand selling squat-proof leggings and matching sets, founder-filmed · niche: Fitness apparel · pillars: Try-ons, Gym fits, Behind the brand","voice":true,"files":["Voice guide","Vamos settings","Marketing plan","What works for me","Tracked accounts","Vamos board"],"tracking":{"following":3,"cap":300,"accounts":["@gymshark (tiktok)","@gymshark (instagram)","@alphalete (instagram)"]},"routines":{"on":0,"cap":2,"list":[]}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>"}.

### Voice guide
Direct, upbeat, no hype words. The founder talks to one woman who lifts. Says what the fabric does, never "flattering". Shows the squat test, says the price plainly.

### Vamos settings
Board: a Brain file called "Vamos board".
Platforms: TikTok, Instagram.
Ads: on. We run Meta ads, about $40 a day, static and video.
Loop stops: after ideas, after script.
Your calls:
- 2026-11-02 · Not for me: "Our athlete collab announcement", because we can't pay athletes.

### Marketing plan
What we sell: Squat-proof leggings at $58 and the Everyday set at $96, on our store (link in bio).
90-day goal: 600 orders.
The ask: "Code FIRST15 for 15% off your first order."
Posts by stage, last 20: reach 12, trust 6, buy 2. The thin stage is buy.

### What works for me
| Lesson | Status | Posts |
|---|---|---|
| The squat test in the first 2 seconds: 3 of 4 above my usual | Confirmed | 4 |
| Saying the price on screen | Hunch | 1 |

### Tracked accounts
@gymshark (TikTok, Instagram): the category leader, ads and organic. @alphalete (Instagram): a rival brand.

### Vamos board
| Idea | Status | Source | Stage | Added |
|---|---|---|---|---|
| The squat test: 5 leggings, one light, which ones go see-through | To review | A try-on find | Trust | 2026-11-03 |
| Packing 40 orders on a Sunday | Made | My own post | Trust | 2026-10-26 |
