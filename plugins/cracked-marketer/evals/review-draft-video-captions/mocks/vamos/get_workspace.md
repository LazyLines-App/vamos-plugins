---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan":"PRO_MONTHLY","brain":"Potly (a test brand): a budgeting app that splits each paycheck into pots the moment it lands, for people paid every two weeks · niche: Personal finance apps · pillars: Payday routines, Money pots, Broke by day ten","voice":true,"files":["Voice guide","Vamos settings","Marketing plan","Creator program: Potly"],"tracking":{"following":2,"cap":300,"accounts":["@monzo (tiktok)","@copilotmoney (instagram)"]},"routines":{"on":0,"cap":2,"list":[]}}

With a `file`, return that Brain file's text from the sections below, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>. Files: Voice guide, Vamos settings, Marketing plan, Creator program: Potly"}.

### Voice guide
Plain and warm. Short sentences. Talks about pots, not budgets.

### Vamos settings
Board: vamos/board.md in the project folder. Briefs: vamos/briefs.md.
Platforms: TikTok, Instagram.
Ads: on.
Creators: @dana.paydays on TikTok, posting on her own account with the paid-partnership label.

### Marketing plan
What we sell: Potly, a budgeting app, free to download, $4.99 a month for automatic pots. iOS and Android.
The ask: "Link in bio."
Rules: never promise savings amounts; never say it fixes debt. No free-trial claim has been approved.

### Creator program: Potly
Creators: @dana.paydays (TikTok), $90 a video, +$90 at 9,000 views and +$180 more at 30,000 within 7 days. 2 videos due by Fri 20 Nov.
Notes: one round of notes per video, as agreed with each creator.
Ad use: 60 days through a Spark code, $40 a video. Paid-partnership label and #ad on every post.
