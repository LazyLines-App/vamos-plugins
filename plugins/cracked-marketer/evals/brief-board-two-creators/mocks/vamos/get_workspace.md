---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan":"PRO_MONTHLY","brain":"Still Skin (a test brand): a fragrance-free barrier repair serum for people using retinoids and acids, sold on its site and TikTok Shop · niche: Skincare · pillars: Barrier basics, Retinoid routines, Bare-face mornings","voice":true,"files":["Voice guide","Vamos settings","Marketing plan","What works for me","Tracked accounts","Vamos board"],"tracking":{"following":3,"cap":300,"accounts":["@nate2trey_ (tiktok)","@welunette (tiktok)","@anitasskin (tiktok)"]},"routines":{"on":0,"cap":2,"list":[]}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>"}.

### Voice guide
Calm and plain, like a friend who reads ingredient lists. Short sentences. Never "holy grail", "glass skin" or "game changer". Says what a product does, never what it cures.

### Vamos settings
Board: a Brain file called "Vamos board".
Platforms: TikTok, Instagram.
Ads: on. We run Meta ads from creator posts.
Creators: we pay creators to post on their own accounts with the paid-partnership label.

### Marketing plan
What we sell: Still Skin Barrier Serum, $34, fragrance-free, with ceramides and panthenol, on stillskin.example and TikTok Shop.
90-day goal: 1,500 TikTok Shop orders.
The ask: "It's in my TikTok Shop link."
Rules: never say it treats acne or any condition; no before-and-after photos.
Posts by stage, last 20: reach 14, trust 5, buy 1. The thin stage is buy.

### What works for me
| Lesson | Status | Posts |
|---|---|---|
| Bare-face, no-filter openings: 3 of 4 above my usual | Testing | 4 |

### Tracked accounts
@nate2trey_ (TikTok): barrier explainers to camera. @welunette (TikTok): skincare routines. @anitasskin (TikTok): skin reveals.

### Vamos board
| Idea | Status | Source | Format | Hook | Added |
|---|---|---|---|---|---|
| If your moisturizer stings, your barrier is cooked: three signs, then the one fix | Approved | https://www.tiktok.com/@nate2trey_/video/7701486741403766030 | Talking to camera, one take | If your plain moisturizer stings, your skin barrier is cooked. | 2026-11-10 |
| A 15-second close-up of the serum on skin, like the Purito wave | To review | https://www.instagram.com/p/DeeigBCT907/ | 15-second close-up | | 2026-11-10 |
| Rating every serum in my drawer | Not for me | | | | 2026-11-08 |
