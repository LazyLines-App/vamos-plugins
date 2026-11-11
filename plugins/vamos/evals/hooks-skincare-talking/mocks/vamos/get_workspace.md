---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan":"PRO_MONTHLY","brain":"Lowtide (a test brand): a fragrance-free barrier cream for skin that stings, $26, sold on its own site · niche: Skincare · pillars: Sensitive skin, Ingredient myths, Simple routines","voice":true,"files":["Voice guide","Vamos settings","Marketing plan","What works for me","Things you've said","Vamos board"],"tracking":{"following":5,"cap":300,"accounts":["@drabby6 (tiktok)","@lucyellelouise (tiktok)","@skincare.w.mare (tiktok)","@the.ayla.journey (instagram)","@hudsonsqrd (instagram)"]},"routines":{"on":0,"cap":2,"list":[]}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>"}.

### Voice guide
Blunt, warm, a bit tired of the beauty industry. Talks to one person with red, tight cheeks. Short sentences. Starts on the problem, never on herself.
Openers she uses: "Okay, so", "If your face…", "Nobody tells you".
Her best real first lines: "Okay, so your toner is the reason your cheeks are red." / "Nobody tells you sunscreen can sting." / "If your face feels tight after you wash it, stop doing this."
On screen: lowercase, one line, no emoji.
Never says: "glass skin", "holy grail", "game changer", "obsessed", "skin goals".

### Vamos settings
Board: a Brain file called "Vamos board".
Platforms: TikTok, Instagram.
Ads: off.
Loop stops: after ideas, after script.

### Marketing plan
What we sell: Lowtide Barrier Cream, $26, fragrance-free, from the link in bio.
90-day goal: 400 orders.
The ask: "Comment STING and I'll send you the 3-step routine."
Posts by stage, last 20: reach 12, trust 6, buy 2.

### What works for me
| Lesson | Status | Posts |
|---|---|---|
| Talking to camera, close up, with my red cheeks in frame: 3 of 4 above my usual | Confirmed | 4 |

### Things you've said
- "I had eczema on my hands for six years."
- "I tested the cream on my own face for a year before we sold it."
- "I'm not a dermatologist."

### Vamos board
## Ideas
| Idea | Status | Source | Stage | Format | Hook | Added |
|---|---|---|---|---|---|---|
| Why your moisturiser stings right after you wash your face | Approved | My own comments: "why does everything burn?" | Trust | Talking to camera, close up, 20 s | | 2026-11-08 |
| My 3-step routine for skin that stings | To review | My own post | Buy | Talking to camera | | 2026-11-08 |

## Hooks
| Hook | On screen | Format | Niche | Shape | Source | Added | Result |
|---|---|---|---|---|---|---|---|
