---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan":"PRO_MONTHLY","brain":"Potly (a test brand): a budgeting app that splits each paycheck into pots the moment it lands, for people paid every two weeks · niche: Personal finance apps · pillars: Payday routines, Money pots, Broke by day ten","voice":true,"files":["Voice guide","Vamos settings","Marketing plan","What works for me","Creator program: Potly"],"tracking":{"following":2,"cap":300,"accounts":["@monzo (tiktok)","@copilotmoney (instagram)"]},"routines":{"on":0,"cap":2,"list":[]}}

With a `file`, return that Brain file's text from the sections below as {"title": "<its title>", "text": "<the section's text>"}, matching the title without regard to case. For a title that isn't here, return {"error":"No Brain file called <the title>. Files: Voice guide, Vamos settings, Marketing plan, What works for me, Creator program: Potly"}.

### Voice guide
Plain and warm. Short sentences. Talks about pots, not budgets.

### Vamos settings
Board: vamos/board.md in the project folder. Briefs: vamos/briefs.md.
Platforms: Instagram @potly.app.
Ads: off.
Creators who post for us: @dana.paydays (TikTok), @lee.splits (Instagram), @ria.saves (TikTok), each on their own account; Dana also makes one video a month for @potly.app.
Pages: none yet.

### Marketing plan
What we sell: Potly, a budgeting app, free to download, $4.99 a month for automatic pots. iOS and Android.
The ask: "Link in bio." Each creator has a signup code.
Stages: reach (creator videos), trust (payday routines), buy (the code).
Rules: never promise savings amounts; never say it fixes debt.

### What works for me
Read: 2026-11-04 · Account: @potly.app Instagram · Usual: 57,900 views over 20 posts.
Hunch: payday-moment openers, 2 of 2 above usual.

### Creator program: Potly
Weeks 1 and 2 run Oct 29 to Nov 12. Each creator posts on their own account unless noted; one round of notes per video.

| Creator | Platform | Usual (read 2026-10-28) | Base per video | Bonus within 7 days | Videos due |
|---|---|---|---|---|---|
| @dana.paydays | TikTok | 2,200 | $75 | +$75 at 6,600 views; +$150 more at 22,000 | 4 by Nov 12, one of them on Potly's Instagram (@potly.app) |
| @lee.splits | Instagram | 2,730 | $75 | +$75 at 8,200 views; +$150 more at 27,300 | 4 by Nov 12 |
| @ria.saves | TikTok | 1,840 | $60 | +$60 at 5,500 views; +$120 more at 18,000 | 4 by Nov 12 |

Bonus pool for the month: $500. Paid-partnership label and #ad on every post. Money is per video, paid weekly for posted videos.

Reading results: each video at 7 days against its creator's usual. A winner is 5x its account's usual within 48 hours, or comments asking where to get Potly. Keep or stop each creator at day 14 on reliability and draft quality.
