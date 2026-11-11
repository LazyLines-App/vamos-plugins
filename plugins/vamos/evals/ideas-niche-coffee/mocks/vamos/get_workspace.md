---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan":"PRO_MONTHLY","brain":"Slow Pour (a test brand): home coffee and pour-over for beginners, filmed in a home kitchen · niche: Coffee · pillars: Pour-overs, Recipe tests, Morning coffee","voice":true,"files":["Voice guide","Vamos settings","Marketing plan","What works for me","Tracked accounts","Vamos board"],"tracking":{"following":4,"cap":300,"accounts":["@ethanrodecoffee (tiktok)","@cocoespresso (tiktok)","@jameshoffmann (instagram)","@morgandrinkscoffee (tiktok)"]},"routines":{"on":0,"cap":2,"list":[]}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>"}.

### Voice guide
Plain, warm, a little dry. Short sentences. Says "you" to one person at a kitchen counter. Never says "hack", "game changer" or "barista secret". Opens on the cup or the pour, talks after. Measures in grams and seconds.

### Vamos settings
Board: a Brain file called "Vamos board".
Platforms: TikTok, Instagram.
Ads: off. We don't run Meta ads.
Loop stops: after ideas, after script.
Your calls:
- 2026-11-04 · Not for me: "Rating every café in my city", because I don't rate other people's coffee on camera.

### Marketing plan
What we sell: The Slow Pour Guide, a $19 PDF of 12 pour-over recipes, from the link in bio.
90-day goal: 300 guide sales.
The ask: "Comment POUR and I'll send you the guide."
Posts by stage, last 20: reach 15, trust 4, buy 1. The thin stage is buy.

### What works for me
| Lesson | Status | Posts |
|---|---|---|
| Recipe tests that end on a taste verdict: 4 of 5 above my usual | Confirmed | 5 |
| A pour with no talking in the first 2 seconds | Hunch | 2 |

### Tracked accounts
@ethanrodecoffee (TikTok): coffee recipe tests. @cocoespresso (TikTok): a barista behind the counter. @jameshoffmann (Instagram): coffee explainers. @morgandrinkscoffee (TikTok): coffee reviews.

### Vamos board
| Idea | Status | Source | Stage | Added |
|---|---|---|---|---|
| What happens when you put [a weird ingredient] in your coffee? I test it so you don't have to, and give you the verdict | Stale | An October recipe-test find | Reach | 2026-10-14 |
| My 4-minute morning V60, start to finish | Made | My own post | Trust | 2026-10-20 |
| Why your pour-over tastes sour, in one cup | Not for me | A September find | Trust | 2026-09-30 |
