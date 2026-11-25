# The content factory, step by step

How we run our short-form content with Claude: find what's working, turn it into ideas and scripts, storyboard, build, post, learn, and run it again every week. Every step, with the exact prompts, our rules word for word, a real example where we have one, what it costs and what goes wrong.

**Paste this into Claude and it sets you up:**

```
Read https://raw.githubusercontent.com/LazyLines-App/vamos-plugins/main/guides/factory.md and set me up.
```

Tested on: Cracked marketer 0.2.27 (24 Nov 2026). Last updated 25 Nov 2026.

---

## For Claude: how to run this guide with the person

You are setting up a content system for the person who sent you this file. Work through it with them one chapter at a time.

1. **First, find out where you are running.** The setup differs:
   - **The Claude app** (claude.ai or the desktop app, chat or Cowork): you can't install plugins yourself. Tell the person exactly what to click (chapter 1, "In the Claude app"), wait for "done". New tools show up only in a new chat, so ask them to open a new chat and paste the same line again; you'll pick up at chapter 1's Check.
   - **Claude Code** (terminal or the desktop app's Code tab): you can run the install commands yourself with Bash (chapter 1, "In Claude Code"). The person restarts Claude Code once after the install, then types `claude --continue` (or pastes the line again) to come back to you. They also sign in to Vamos once, in a browser: tell them when.
   - Chapters 1 to 4, 8 and 9 work in both. Chapters 5 to 7 (storyboard, building and posting the videos) need Claude Code on the Mac or Linux computer that holds the video files.
2. **Ask once, in one message:** the six questions in chapter 1, step 4, word for word, as soon as the plugin and Vamos are in place (in the Claude app, in the new chat), plus two for chapters 2 and 3: which competitor to take apart first, with its handle on each platform copied from its profiles, and whether the board goes in Notion, a Google Sheet or a file (connect that app now if it's one of the first two). Skip what they already told you.
3. **One chapter at a time.** At the start of each, say in two lines what it gives them, how long it takes and what it costs. At the end, run the chapter's **Check** list yourself. Move on only when every item passes, or the person says skip.
4. **Run the skills yourself.** Each `/cracked-marketer:<skill>` line in this guide is a skill you can run when the person asks for that step, the same as if they typed it. If your host doesn't let you start a skill, ask them to type the line.
5. **Do the work; they make the calls.** Run every command and prompt you can. Hand them only what needs their hands: a sign-in, a payment, an approval, filming. Never post, send, pay or spend outside Vamos credits without their yes to the exact list.
6. **Allow the tool prompts the skills raise** (downloading Vamos's data file, a web search, publishing a page), or tell the person to. A refused download means the skill reads fewer rows.
7. **Say what it costs before it runs.** Credits come from Vamos (`get_credit_usage` reads the balance). Paid video, voice and posting tools bill the person's own accounts.
8. **When something fails,** say what failed in one line, try the fix in the chapter's "When it goes wrong", and if that doesn't work, tell them where to ask (chapter 13). Don't improvise a workaround that skips a stop.
9. **Report a result, not a log.** After each chapter: what they now have, its link, and the next step as a question.

Start with chapter 0 in three lines, then chapter 1.

---

## The map

```
📁 Content factory
┃
┣ 📁 0. What you'll have, and what it costs
┣ 📁 1. Setup ............... install, connect, your answers ready
┣ 📁 2. First win ........... one competitor taken apart, in about 30 minutes
┃
┣ 📁 3. Find ................ what's working in your niche, as ideas on your board
┣ 📁 4. Ideas and script .... the hook, the script, the caption, in your voice
┣ 📁 5. Storyboard .......... a still for every beat before anything is paid for
┣ 📁 6. Build ............... one recipe per format
┃   ┣ 📁 Narrated motion graphics
┃   ┣ 📁 Voice over a demo
┃   ┣ 📁 Silent hook demo (one demo, many hooks)
┃   ┣ 📁 Static ad and carousel
┃   ┣ 📁 AI presenter
┃   ┗ 📁 Drama
┣ 📁 7. Post ................ your accounts, your times, the keyword DM
┣ 📁 8. Learn ............... what worked, counted, and what to make more of
┣ 📁 9. The weekly loop ..... it runs again by itself, stopping for your yes
┃
┣ 📁 10. When an output is bad
┣ 📁 11. Under the hood: how we run it
┣ 📁 12. What it won't do
┗ 📁 13. Next
```

Find → script → storyboard → build → post → learn, and again. You pick the ideas, read the scripts, and say yes to anything that costs money or goes public.

---

## 0. What you'll have, and what it costs

**By the end of chapter 3** (about an hour): your brand set up in Claude, your competitors tracked, a board of ideas, each backed by a post that's working now, waiting for your yes.

**By the end of chapter 9** (an afternoon, plus 1 to 2 hours for the video tools): scripts in your voice, videos built on your own tools, posts scheduled on Instagram, TikTok and YouTube with the right AI labels (Facebook, Threads and LinkedIn posts that hold AI are posted by hand), a Monday report of what worked, and the research and writing running every week with your laptop closed. You still film what needs a face and say yes to each batch of posts. Once scheduled, posts go out with your laptop closed. (You can also let the loop schedule what you mark Ready by itself; it does that from the computer that holds the videos, and TikTok then waits in its inbox for you to tap Post.)

### Words you'll see

- **Vamos:** the research connector. It reads public Instagram, TikTok and YouTube posts and the Meta Ad Library for Claude. The plugins are free; research runs on Vamos credits.
- **Plugin, marketplace:** a plugin adds skills to Claude. A marketplace is where Claude installs it from; ours is added as `LazyLines-App/vamos-plugins` (its GitHub address) and then called `vamos-plugins`, as in `cracked-marketer@vamos-plugins`.
- **Connector:** what lets Claude reach another app (Vamos, Notion, Zernio). You sign in to it once.
- **Median, outlier:** an account's median is its typical views. A post with 5 times that is a "5× outlier": it did far better than that account usually does, which a big view count alone doesn't tell you.
- **Find:** a post that's working now, picked as the start of an idea.
- **Board:** where ideas, scripts and posts wait for your yes: a Notion database, a Google Sheet, or a file.
- **Brain:** your Vamos workspace's saved files (your voice guide, your competitors, what works for you). You can read and edit them at app.getvamos.ai/brain.
- **Cowork:** the Claude desktop app's mode for tasks that run on a schedule.
- **Zernio:** the scheduler that posts to your accounts (chapter 7).

### What works today

| Station | What runs it | Status |
|---|---|---|
| Setup and your brand | `/cracked-marketer:setup` | Works today |
| First win: a competitor taken apart | `/cracked-marketer:playbook` | Works today |
| Find | `/cracked-marketer:ideas`, `formats`, `winning-ad-ideas` | Works today |
| Hooks, script, caption | `/cracked-marketer:hooks`, `script` | Works today |
| Storyboard | `/cracked-marketer:make-video` (its plan and key frames) | First cut |
| Build: narrated motion graphics, voice over a demo, silent hook demo, static, carousel | `/cracked-marketer:make-video` | First cut |
| Build: AI presenter, drama | `/cracked-marketer:make-video` | Experimental |
| Post | `/cracked-marketer:post` with Zernio | First cut |
| Learn | `/cracked-marketer:content-log` | Works today |
| The weekly loop | `/cracked-marketer:loop` | Works today; check its first run |

**Works today:** strangers' brands have run it and the outputs passed. **First cut:** it runs end to end and its code checks pass, but it hasn't yet been through a full outside test; expect one fix round. **Experimental:** it works on our accounts; quality varies, so treat a result as a draft.

### What it costs

| Tier | You need | Price (read 25 Nov 2026) |
|---|---|---|
| Research and writing (chapters 1 to 4, 8, 9) | Claude Pro, or Max for heavy weeks | $20 a month (Pro) |
| | Vamos, the research connector | Free: 200 credits, once. Pro: $49 a month for 2,000 credits |
| | Notion or a Google Sheet for your board | Free |
| + video (chapters 5, 6) | Claude Code (comes with Pro and Max) on a Mac or Linux computer | Included |
| | Node 22, FFmpeg, Python 3, Tesseract, HyperFrames | Free |
| | ElevenLabs for the voice | Free plan has 10,000 credits a month; Starter is $6 a month |
| | A video generator, only for AI presenter and drama shots (Higgsfield, Kie or fal) | About $5 for a 15-second presenter take at 720p |
| + posting (chapter 7) | Zernio | First 2 accounts free, then $6 an account a month. Keyword DMs: 2,000 a month free, then $2 per 1,000. X posts $0.015 each |

**Vamos credits per run** (each run says its cost before and after):

| Run | About |
|---|---|
| Setting up your workspace | Free |
| Setup's research turn (your voice, competitors) | 60 to 70 |
| A new account's first research turn | Free |
| A playbook on one competitor | 50 to 60 |
| An ideas run | 50 to 60 |
| A content log | 15 |
| The Monday research pack | up to 60 |
| A script you approve | up to about 60 (not yet measured) |
| **The weekly loop** (ideas twice, content log once, the pack) | **130 to 200 a week, plus your scripts** |

These are estimates; a run's real cost depends on how much it reads, and each run tells you before and after. In our test run on a new free account, chapters 1 to 3 (first win, setup, one ideas run) used 132 of the 200 free credits. The weekly loop needs a paid plan (Vamos Pro).

### Time

| Step | First time |
|---|---|
| Install and connect | 10 minutes |
| First win | 20 to 30 minutes, most of it Vamos reading |
| Setup (your voice, competitors, board) | 15 to 30 minutes |
| Video tools install | 1 to 2 hours, once |
| One narrated video, script to file | 1 to 2 hours, with your two reviews |
| A normal week once it runs | About an hour of your yeses |

---

## 1. Setup

**What it does:** installs the plugin, connects Vamos, and gets your answers ready so setup runs once without questions.
**What comes out:** Claude with 16 marketing skills (setup, playbook, formats, hooks, ideas, winning-ad-ideas, script, make-video, post, content-log, loop, analyze, find-creators, creator-program, brief, review-draft), each run as `/cracked-marketer:<skill>`, signed in to your Vamos workspace.
**Status:** works today. **Time:** 10 minutes. **Cost:** free.

A long setup day on Claude Pro can hit its 5-hour usage limit. Nothing is lost: when it resets, open the same chat (in Claude Code, `claude --continue`) and say "carry on".

### Step 1. The accounts

| Account | Why | Where |
|---|---|---|
| Claude (Pro or above) | Runs everything | claude.ai |
| Vamos | Reads TikTok, Instagram, YouTube and the Meta Ad Library: watches the videos, reads the comments, finds what's working | app.getvamos.ai/sign-up (or "Continue with Google" when you connect) |
| Notion or Google | Your board: ideas, scripts and posts wait there for your yes | notion.so or a Google Sheet |
| Zernio (chapter 7) | Posts to your accounts at your times | zernio.com |

If you sign up to Vamos with email, open the confirmation email before you connect: an unconfirmed email can't sign in from Claude.

### Step 2. Install the plugin

**In the Claude app** (claude.ai or the desktop app, on any paid plan; the person clicks, Claude waits):
1. Open Customize, then Plugins, then Add marketplace.
2. Enter `LazyLines-App/vamos-plugins`.
3. Install **Cracked marketer**.
4. On the plugin's Connectors tab, connect **Vamos** and sign in.
5. Open a new chat (new tools show up there) and paste the setup line again.

**In Claude Code** (Claude can run these):

```
claude plugin marketplace add LazyLines-App/vamos-plugins
claude plugin install cracked-marketer@vamos-plugins
```

Then restart Claude Code (`claude --continue` brings the chat back), type `/mcp`, pick **vamos** and sign in. Or type the same as slash commands inside a session: `/plugin marketplace add LazyLines-App/vamos-plugins`, then `/plugin install cracked-marketer@vamos-plugins`.

**Which plugin:** Cracked marketer is for a brand, app or agency: it holds everything in our other plugin (Content System) plus creators, briefs, ad ideas and making videos. Install one, not both.

### Step 3. Sign in to Vamos

The sign-in page asks Claude's request to reach your workspace. Sign in, then:
- **"Set up your Brain"**: press **Skip**. Chapter 3's setup does it with more: your voice, your competitors and your board.
- "Choose a workspace" appears only when you have two or more. Pick the brand you're setting up.

### Step 4. Your answers, ready

Setup asks these once, in one message, before it spends anything. Vamos can't ask you questions while it works, so a guess here becomes a generic voice. Have them ready:

```
1. Each social account (handle and platform), the website, and who talks on camera for the brand: the founder on their own account, someone on the brand's, or nobody.
2. What you sell and who it's for, in a line.
3. Competitors you already know, and creators you work with.
4. Will you show a face, use your voice, film alone? And where do you plan and post now (a Notion or Sheet calendar, a scheduler, the app itself)?
5. Do you care about Meta ads? (No means no credits spent on ads, anywhere.)
6. The goal for the next 90 days (reach, leads, sales, a launch), and what a viewer should do after watching.
```

These are setup's own questions, word for word.

### Check (Claude)

- [ ] `get_credit_usage` returns a balance (Vamos is connected and signed in to the right workspace).
- [ ] Claude can see the cracked-marketer skills (setup, playbook, ideas, script, make-video, post, content-log, loop and the rest) in its own skill list.
- [ ] The person's six answers are in this chat (asked after the tools showed up).

### When it goes wrong

- **No Vamos tools:** in Claude Code run `/mcp`, pick vamos, sign in. In the Claude app, open the plugin's Connectors tab, or add it by URL: Customize → Connectors → Add custom connector, `https://mcp.getvamos.ai/mcp`.
- **"This email isn't verified yet":** open the confirmation email from Vamos (it works for 24 hours), then sign in again.
- **The skills don't show after installing in Claude Code:** restart Claude Code.

---

## 2. First win: one competitor taken apart

**What it does:** reads a competitor's last 40 posts, finds what works for them counted against their misses, and writes five plays for your brand, each with a first line you could post today.
**What comes out:** the five plays in the chat, and a page, "Plays to steal from [competitor]", with the plays and everything the run read. In the Claude app the page opens beside the chat; in Claude Code it's a Markdown file in your folder. A copy is saved to your Vamos Brain as "Playbook: [competitor]", so later runs build on it.
**Status:** works today. **Time:** 20 to 30 minutes, most of it Vamos watching. **Cost:** on a new Vamos account the main turn is free (its first research turn), so a few credits; else about 50 to 60.

### Run it

Use the competitor's handles, not the brand name, one per platform, copied from their profiles: a brand's handle often differs between Instagram and TikTok.

```
/cracked-marketer:playbook @their-instagram on Instagram and @their-tiktok on TikTok. I sell [what you sell] to [who].
```

### Our rules for this step, word for word

From the playbook skill:

> **The job:** what a brand or creator does that works, and exactly how the user would use it on their own account. Patterns, counted: "8 of their 15 best posts open on a bold claim, against 4 of their 30 weakest". A single big post is only ever the example of one.

> **Top quarter against bottom half,** by outlier score: 3 to 5 traits each counted "N of M" ("bold-claim opener: 8 of 15 top, 4 of 30 bottom"), and the trait the bottom half has more of, which goes under Skip. Under 20 posts, a trait is a hunch.

> **A pair per trait:** a hit and a miss made the same way where the trait is the main difference. Two changed layers make a guess, and you say so.

How the median is counted, in every skill:

> compute the account's median yourself: the median views of posts at least 7 days old (views still climb before that), leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). A post's views over that median is its outlier score, written "N× outlier"

### A real example

**Input:** the test run of this guide, on a fresh Vamos account (25 Nov 2026), for OLIPOP, a prebiotic soda:

```
/cracked-marketer:playbook @drinkpoppi on Instagram and @poppi on TikTok. I sell OLIPOP, a prebiotic soda with less sugar, to millennials and Gen Z who grew up on regular soda.
```

**What it cost:** 6 credits (the main research turn was the account's free first one; a follow-up for the likes cost 6). Vamos read for 13 minutes.

**Output, play 1 of 5, as it came back:**

> **1. A one-line bit with no sell.**
> - **Seen:** a performed one-line bit or reaction is in 4 of their top 8 TikToks and 1 of the bottom 16. The hit is Couture Santa vest, 190,960 views, 47× outlier, 8 s. The miss is Rob reads holiday copy, 3,727 views, 0.92× outlier. Both are one static shot of the same person in the same campaign. The hit performs a joke and the miss reads promo copy. Celebrity is in both, so it doesn't explain the gap, but it may raise the ceiling.
> - **Your first line:** an off-camera voice asks "And this?" and Sam answers "Vintage." (their "And this?" / "Couture.").
> - **Outline:** Sam poses in a thrifted retro jacket; the voice asks; Sam says the one word; Sam turns, and the back reads "Vintage Cola", can in hand.
> - **Watch:** views on day 3 against your own TikTok median, and shares per 1,000 views.
> - **Paste:** "Write 5 TikTok bits of 10 seconds or less for Sam to film in one static take for OLIPOP Vintage Cola: an off-camera question, a one-word answer, a visual reveal, no sales line and no health claim."

It also caught two traps a person would fall for. Poppi's three posts with over a million views had likes at 0.04 to 0.14% of views, so it set them aside as paid reach rather than copy them. And the TikTok handle we gave, @poppi, was a stranger's account, so it read @drinkpoppi instead.

**Why it passed:** the pattern is counted (4 of the top 8 against 1 of the bottom 16); the hit and the miss are the same person, shot and campaign, so the difference is the joke; and the first line can be filmed this week by one person. The page names its picks ("the flavor is Vintage Cola, the on-camera teammate is called Sam") so nothing is left in brackets.

### What good looks like

- Every pattern says "N of M" and links a hit and a miss.
- Every play names your product and has all five parts: Seen, Your first line, Outline, Watch, Paste.
- Nothing says spend, ROAS, revenue or "best-performing": Vamos reads public posts, not anyone's ad account.
- A huge view count with very few likes is set aside: likes under 0.5% of views usually mean the post was paid for, so it can't teach what works without a budget. Brands boost a lot; in our test 5 of Poppi's 12 checked TikToks read as boosted.

### When it goes wrong

- **The wrong account came back:** you named a brand, not a handle, or the handle is someone else's on that platform. Run it again with the brand's own `@handle` from its profile. In our test, TikTok's @poppi turned out to be a personal account; Vamos said so and read the brand's @drinkpoppi instead.
- **Patterns rest on 2 or 3 posts:** the account posts little. The playbook marks them as hunches; pick a competitor that posts weekly.
- **Ads came back empty in the US:** Meta shows stopped ads only for ads that ran in the EU or UK. The playbook says "stopped ads aren't visible" rather than zero.

### Check (Claude)

- [ ] The recap (the skill's closing line: what was made, credits used and left, the next step) names the page or says the plays are in the chat.
- [ ] Five plays, each with five parts, none with a [bracket] left to fill.
- [ ] The recap shows credits used and left.

Next: chapter 3 makes it yours.

---

## 3. Find: what's working, as ideas on your board

**What it does:** sets Vamos up for your brand once (your voice, your competitors, your board), then each run reads what's working among your competitors, your niche and your comments, and turns what you can make yours into ideas, each backed by the post it came from.
**What comes out:** a board (Notion, a Google Sheet, or a file) with ideas at **To review**, each with its source post, its outlier score and why it's yours.
**Status:** works today. **Time:** setup 15 to 30 minutes once; each ideas run about 15 minutes, most of it Vamos reading. **Cost:** setting up the workspace is free; setup's research turn was 66 credits in our test run, and an ideas run about 50 to 60.

### Step 1. Make it yours (once)

```
/cracked-marketer:setup
```

Setup uses your six answers from chapter 1 and asks only for what's missing. Then it:
1. sets up your workspace and tracks your accounts and up to 8 competitors and creators;
2. reads your last 40 videos where someone talks, and builds your voice guide from how you really talk;
3. finds your closest competitors, accounts that sell something else to the same audience, and two bigger ones;
4. writes your Brain files: Tracked accounts, Things you've said, What works for me, Marketing plan, Vamos settings;
5. **tests the voice:** a fresh Claude writes a 20-second script on one of your videos it never saw, and shows it beside your real one. It asks: "Which lines aren't you?" Answer it; each answer becomes a voice correction;
6. makes your board, or adds its columns to the content calendar you already keep.

Connect Notion or Google Drive in Claude first (Customize → Connectors) if you want the board there. Without either, the board is a Brain file in Vamos (or `vamos/board.md` in your folder in Claude Code).

### Step 2. Find

```
/cracked-marketer:ideas
```

It asks Vamos, in one turn, for your tracked accounts' biggest outliers this week, your niche's biggest in the last 14 days from accounts you don't track, and what people ask in the comments on your posts and your competitors'. Then a script drops what can't be a find, and Claude judges the rest.

Two more ways in:
- `/cracked-marketer:formats`: the formats to make next, ranked: the Meta ad formats your category keeps running 30 days or more, then the video formats taking off.
- `/cracked-marketer:winning-ad-ideas`: ten Meta ad ideas, each remade from an ad that has kept running 30 days or more.

### Our rules for this step, word for word

The numbers bar, in code (`filter.py`), before anything is judged:

> Keeps a post with views at the floor or over, a 2x outlier or more (outlier_score), 150 s or less, posted within 21 days of the day its numbers were read

Then the five tests, all must be true:

> 1. **It's from their space, or its format or hook carries over to their subject as it is.** Any language.
> 2. **Why it worked can be theirs.** Not the creator's fame, a personal story or result, a prize giveaway, someone else's job or product. A video that rode a one-off launch is only worth its hook or format, and only while it's hot.
> 3. **It needs no authority they don't have.** Advice that lands because of who says it, a health or money claim, or a ranking on someone's taste needs a name they may not have.
> 4. **Their product or know-how gives the payoff,** the way someone who wants it would really get it. Bolted on is a skip.
> 5. **It has something big in it:** a specific new thing, result or number that makes someone stop, or a free thing people comment to get. A want people already have isn't enough, however many views the post got.

Steal only the part that carried it:

> - **Format:** how it's shot, cut and told.
> - **Hook:** the opening line or picture, and its framework.
> - **Script:** the beats in their order.
> - **Topic:** what it's about and the problem under it, when their audience thinks "I need this" in one read.
>
> A part that didn't clearly carry it isn't stolen: maybes fail.

The straight swap comes first:

> Keep the find's sentence, and its picture when the picture carried it. Swap its subject for theirs at the same size and keep every other word

> How the swap reads:
> - "Somebody just built a Claude Code agent whose only job is to get you customers" became "Somebody just built a Claude agent whose only job is to make you go viral."
> - "i'm giving away our ENTIRE meta creative playbook" became "I'm giving away our ENTIRE content playbook."
> - One find's eight spread across narrow wants ("…tell you why your last reel got no views", "…stalk your competitors for you", "…do your doomscrolling for you") and every one was rejected ("all of these angles really suck"): the find's own sentence at the whole field's size was missing.

### It learns from your no

On the board, set an idea you won't make to **Not for me** and write why in a few words. The next run reads it:

> A call reaches as far as its reason, not its words, and the reason covers its act whatever it's done to: "no hauls, because I don't push people to buy more" also rules out "10 things I bought this month"

An idea left at To review for 14 days goes to Stale. Silence is never a yes.

### A real example

**Input:** the same test run as chapter 2 (OLIPOP, 25 Nov 2026): `/cracked-marketer:setup` with the six answers, then `/cracked-marketer:ideas`. Nothing else was typed.

**What it cost:** setup 66 credits and 17 minutes; ideas 60 credits and 15 minutes. Chapters 1 to 3 together used 132 of the 200 free credits.

**Output:** 4 finds and 12 ideas on the board. One find and the straight swap it led with, as they landed:

> **Source:** @nataliecamilay float, 486,043 views, 10.9× outlier so far (4 days old at the read)
> **Idea:** The Christmas Vintage Cola Float You Need This Season
> **Why it's yours:** A cola float is the soda they grew up on, made with your can. Make no sugar claim about the finished float.
> **Format:** Finished drink first, hands-only recipe, about 18 s

**Why it passed:** the find is from their space (a drink recipe), the idea keeps its sentence and swaps only the subject, OLIPOP's can is the payoff rather than a logo at the end, and the row flags the one claim it mustn't make. It also lined up with play 2 from chapter 2 (the float recipe), found from a different account.

**What it got wrong, and what to do:** three ideas were close wordings of one meme, so you'd approve one and mark the others Not for me with "same idea". And the brand had only one video where someone from the team talks, so the voice guide was thin; with fewer than 10 talking videos, give setup an account to sound like or paste a few transcripts.

### What good looks like

- Each find heads its ideas, linked, with its outlier score and its hook word for word.
- Three to five ideas per find, the straight swap first.
- No idea repeats a promise already on your board.

### When it goes wrong

- **Ideas feel generic, or setup says your voice is thin:** setup learns your voice from videos where someone talks, and needs about 10. With fewer (a new account, or a brand that posts product shots), give it an account to sound like, or paste three transcripts or captions you wrote yourself and say "use these as my voice".
- **Your own biggest posts look like outliers but have few likes:** they were probably boosted. Say so, and they're left out of what works for you.
- **Finds are from big accounts with nothing to steal:** that's test 2 failing. Mark them Not for me with "fame, not the idea".
- **Views look old:** each row carries the date its numbers were read. Ask "read these again fresh" for the ones you'd make.

### Check (Claude)

- [ ] `get_workspace` lists Vamos settings with a Board line.
- [ ] The board has ideas at To review, each with a source link, and a multiple when the source is a post (an idea from a comment carries the comment's likes).
- [ ] The person knows how to approve: set a row to Approved, or say "approve 1 and 3".

---

## 4. Ideas and script: the hook, the script, the caption

**What it does:** writes the first line from hooks that are working now in your format and niche, then the whole script in your voice on the skeleton of the post that worked, checked in code and by a fresh reader.
**What comes out:** on the idea's card: the hook with up to four others, the script as Said and On screen lines by beat, the caption, and any `[your …]` slot only you can fill.
**Status:** works today. **Time:** 5 to 10 minutes a script. **Cost:** hooks: one Vamos research turn, only when your board has fewer than 10 proven hooks; script: at most one turn, to read the find's beats. We haven't measured these yet: budget up to about 60 credits a script (the size of an ideas run). Each turn's price is said first, and it asks before running when you have less.

### Run it

Approve an idea on the board, then:

```
/cracked-marketer:script
```

It writes every Approved idea. For one of your own:

```
/cracked-marketer:script [your idea, in a line]
```

A draft that sounds like AI:

```
/cracked-marketer:script make this sound like me: [paste it]
```

Only the hook: `/cracked-marketer:hooks [the idea]`.

### Our rules for this step, word for word

**The hook.** Find the one thing a stranger would stop for (from the hooks skill):

> name, in a few words, the one thing in this video a stranger would stop for: something strange, something they'll watch change, or a claim bigger than feels safe, never their problem said back, which they know already.

Keep a hook only if all five are yes (from our own script rules):

> Does it open a loop only the video closes? Is it new, more than one sentence typed into Claude? Does our audience want it every week and understand every word? Does it sound like a friend talking? Is it one thought, topic first, you can believe?

At frame 0, text, picture and voice together, so the viewer has the whole context at once.

The cold hook read. A fresh Claude that hasn't seen the idea gets only the hooks and this, word for word:

```
Would you stop scrolling on each, yes or no, and why in a line? Which words would you need explained, and what does each line leave you wanting to know?
```

Fix the words it marks. A hook it wouldn't stop on is rewritten from the same proven post, or dropped.

**The script** (from the script skill):

> - **A stranger gets every line the moment they hear it,** with no idea what the video is about. Each line answers the question the line before left.
> - **Start near the peak.** No intro. The line after the hook starts paying it; the next one or two sell what's coming or answer the doubt the viewer has right now.
> - **Value early, the best payoff last,** one idea.
> - **The video is worth it without the product.** The user's product comes in once, after the value has landed, as the faster way or the answer to "how did you do that?".
> - **Every "I" sentence comes from Things you've said, a line the voice guide quotes, or this chat.** Anything else only they know is a `[your …]` slot. A creator can't post a script that makes up their past.

Our own caps: the main rehook lands at 38 to 79% of the runtime, and 60 seconds is the ceiling: about 240 words with a presenter, 200 for a narrator. A video from a find runs no longer than its original.

**The checks, in code,** on every draft (`textstats.py check`): the AI tells your own videos don't use, any story about you that nothing you've said holds, overlap with the find over 15% outside the hook, and length more than 15% off.

**The cold read** of the whole script, word for word:

```
You're scrolling and this plays. In one sentence, what is it and what do you get? Line by line, what did each one tell you? Mark any line you had to guess at or read twice, any word that means nothing to you, and any line nobody would say out loud to a friend.
```

If its sentence isn't the promise, the marked lines are rewritten, not cut: cutting the turns makes it flat.

**The caption** (from our post-copy rules):

> A caption is a line or two someone reads in a second, then the comment word. It never explains the video; the video does that.
> - The first line is what they'd say about it to a friend: the result, a reaction, a number, a tease or a joke, often the hook said shorter.
> - Then the keyword and what its DM sends, in a few words: "Comment SYSTEM and I'll send you the setup".

Real captions as posted, from our examples file (hashtags left off; / is a new line):

> - @kartikeysinggh, 4.55M views: Youtube + claude / This youtube skill is going viral. / Comment "youtube" to get step by step guide in your Dms.
> - @canwebuildthis, 2.1M views: she said no sixty-one times. that's the job. / what's the pettiest thing you've made your AI redo?
> - @chase_ai_ on TikTok, 1.2M views: claude hacks your TV
> - @opusjake, 784K views: Comment "stack" and I'll send the fully optimized AI tool guide for any task
> - @minolee.mp4, 326K views, a 232× outlier: comment CLAUDE for my free editing skill 🤑
> - @minolee.mp4, 193K views, a 137× outlier: 200M views of content experience in 1 claude plugin / comment SLOP for it
> - @chenbuildsai, 111K views, 7.5K comments: This open-source Claude prompt pushes your website onto Google's first page, and it runs for free ⬇️ / Comment "CLIMB" and I'll send you the link 📩 (Follow so the DM lands)

### A real example: one of ours, posted

**Input:** an idea on our board: "Claude runs your Instagram while you sleep", in the Claude conversation format (a person talks to Claude, Claude answers on screen).

**Output, the hook as posted** on one of our Instagram accounts, 13 Nov 2026:

> Her: "Claude, I'm going to sleep. Don't do anything weird." Claude: "Your Instagram's safe with me."

**The caption as posted:**

> Comment SLEEP and I'll send you the free setup that has tomorrow's post waiting when you wake up.
> Claude, with a free plugin called Vamos, finds the video of yours that blew up, drops what didn't work, and writes the next one: the hook, the script and the caption.
> Set it once and it lands in your inbox every morning.

**What happened:** 7,171 views, a 4.2× outlier (the account's median is 1,688, from its 4 Instagram posts at least 7 days old on 25 Nov), and 134 comments, most of them the keyword.

**Why the hook passed:** a stranger knows the job in one read (someone handing their Instagram to Claude overnight), the loop only the video closes is "what did it do while she slept", it sounds like two people talking, and it's one thought. **What we'd change:** the caption's second and third lines explain the video. Our caption rule came after posts like this one: the first line and the keyword do the work.

### What good looks like

- The cold reader's one sentence is the promise you wanted.
- Every `[your …]` slot names exactly what goes there.
- The checks line reads: tells 0, stories sourced, overlap under 15%, length on target.

### When it goes wrong

- **It doesn't sound like you:** tell it "I never say X, I'd say Y". That goes into your voice guide for every later script.
- **The hook is the problem said back** ("Struggling with content?"): that fails "something a stranger would stop for". Ask for hooks from proven posts in your format: `/cracked-marketer:hooks`.
- **It made up a story about you:** the code check catches it and turns it into a `[your …]` slot. If one gets through, say so; it's a bug worth reporting (chapter 13).

### Check (Claude)

- [ ] The script skill's own check (`textstats.py check`, which ships inside the plugin) printed no fails on the final draft. In the Claude app, where no script runs, the skill does the same checks by reading.
- [ ] The cold read ran on the text alone (a fresh subagent in Claude Code; in the Claude app, a separate pass that reads only the script) and its sentence matches the promise.
- [ ] The script is on the idea's card, set to Script ready.

---

## 5. Storyboard: a still for every beat before any spend

**What it does:** turns an approved script into a plan, beat by beat (the line, what the viewer sees, how it's made), prices every paid step, then shows one still per beat for your OK before anything is built or paid for.
**What comes out:** the plan as one message; then key frames, one still per beat, in order.
**Needs:** Claude Code on your Mac and chapter 6's Install once, done first.
**Status:** first cut. **Time:** 10 to 20 minutes, plus your review. **Cost:** free, except paid images on an AI format (about $0.09 an image, on your generator account).

### Run it

```
/cracked-marketer:make-video [the script, or "the script on card 3"]
```

It stops twice before building: once for the plan and its price, once for the frames.

### Our rules for this step, word for word

The gate (from make-video):

> **3. The plan, one message, then wait for their go.** Beat by beat: the line, what the viewer sees, and how it's made (captured, filmed by them, built in HTML, generated). What the viewer sees is the thing the line names, readable at the word that names it

> **5. Key frames for their OK,** before any cut is built: one still per beat, in order, taken at the word where its line names its thing, with its caption.

The priced list, before any paid generation:

> Before any paid video generation, show one list and wait for the user's yes to it. "Go ahead" before they've seen the list is not a yes to it.

A plan looks like this (the skill's own example):

> **Format:** a voice over a demo, 35 s, no face. Every line is something the app does on screen, so the proof carries it.
> | Beat | Line | Seen | Made by |
> |---|---|---|---|
> | 0:00 | "Most budgets die in week two." | Your app's empty month, a cursor on day 14 | Captured, your app |
> | 0:04 | "Mine lives in my lock screen." | The widget filling as a coffee is logged | Captured, your phone |
> **You send:** a login I can capture, or your screenshots; a song you have the rights to, or none.
> **Paid:** the voice on your ElevenLabs (about 500 characters). Nothing else is paid.

### What good looks like

- Each still shows the thing its line names, readable on a phone.
- Frame 0 has text, a picture and the first words together: it works as the cover.
- Every screen is real: captured from your product or filmed off your screen. People are their real public profiles or labelled AI characters.

### When it goes wrong

- **A still shows the chat loading instead of the result:** that beat fails "the thing the line names". Say which beat; only that one is redrawn.
- **The look is generic:** give it your site or a post whose look you want. It reads your colours, type and logo from there.

### Check (Claude)

- [ ] The person said yes to the plan and its price.
- [ ] They've seen every still and gave one round of notes.

---

## 6. Build: one recipe per format

**What it does:** builds the video from the frames you passed, makes the voice, cuts it to the voice, then checks it in code before you watch it.
**What comes out:** one named video file, its caption with no link in it, the disclosure line and AI label when it holds AI footage, and a post sheet (`<file>.post.json`) that chapter 7 reads.
**Status:** first cut for recipes 1 to 4; experimental for 5 and 6. **Time:** install 1 to 2 hours once; then 1 to 2 hours a video with your reviews. **Cost:** the voice on your ElevenLabs; a paid generator only for recipes 5 and 6. Vamos credits: none, except recipe 3's lines from proven hooks (one hooks turn, chapter 4).

### Install once (Claude Code, Mac or Linux)

Building hasn't been tested on Windows. On Windows, run chapters 1 to 4, 8 and 9 in the Claude app, build the videos in your usual editor from the script, and schedule them in Zernio's own app.

In the Claude app, nothing can run these for you, so start Claude Code once yourself: open Terminal (Cmd+Space, type Terminal), paste the first line below, then type `claude` and sign in with your Claude account. From then on, paste this guide's line there too and Claude runs the rest with you:

```
# Claude Code in the terminal, if `claude --version` doesn't answer (sign in with your Claude account when it starts)
curl -fsSL https://claude.ai/install.sh | bash
# Homebrew, if `brew --version` doesn't answer (Mac)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# Node 22 or newer, FFmpeg, Python 3 and Tesseract
brew install node ffmpeg python tesseract
# HyperFrames: HTML rendered to video
npx skills add heygen-com/hyperframes
```

On Linux: `apt install ffmpeg python3 tesseract-ocr` and Node 22 from nodejs.org.

Then, in Claude Code, add the plugin and Vamos there too (chapter 1, "In Claude Code": the two install lines, a restart, then `/mcp` → vamos), and connect your board's app (`/mcp` lists Notion or Google if you add them, or paste the script into the chat instead of naming its card).

For the voice, an ElevenLabs API key: make an account at elevenlabs.io and create a key under your profile's API keys. Add the line `export ELEVENLABS_API_KEY=…` to your `~/.zshrc` (your terminal's settings file), open a new terminal, and start Claude Code there with `claude`, so the key is always set and never sits in a chat.

**Time:** 1 to 2 hours the first time. **Check (Claude):** `node --version` shows 22 or above; `ffmpeg -version`, `python3 --version` and `tesseract --version` all answer; `npx hyperframes --version` answers.

### The checks every build passes (all formats)

From make-video, word for word:

> 1. `npx hyperframes check --json`: fix every error (layout, overlap, contrast).
> 2. `python3 scripts/check-video.py final.mp4 …`: size, length cap, loudness, true peak, the lead-in, the tail, frame 0 as a cover, every word captioned and each caption ending on a whole phrase, no link in the caption, frozen stretches; the final's own audio heard against the script, word for word; and each beat's screen at the word that names its thing.
> 3. Look at it yourself: the beats sheet the check writes, and a 4 fps strip around every cut … full size. A defect seen at one moment gets looked for across the whole video.
> 4. A fresh subagent that didn't build it, shown the beats sheet, the strips and the script, not your notes: does each frame show what its line names, does frame 0 work as the cover, does any face read asleep or as the wrong feeling, and does anything read as drawn or fake?
>
> After any fix, run 1 to 4 again on the new file

Sound: master to −14 LUFS, −1.5 dB true peak; the voice starts 0.25 s in; a song you have the rights to, or none. At most three review rounds with you: if it isn't right by the third, the script or the format is the problem, not the edit.

Every format: 9:16 at 1080 × 1920, nothing in Instagram's top 220 px, bottom 420 px or right 130 px.

### Recipe 1. Narrated motion graphics (first cut)

**Best for:** teaching something the viewer didn't know, with your product's real outputs as proof. No face, no filming.
**You supply:** screenshots or a login to capture; your brand's site for colours and type.
**Paid:** the voice only (about 1,000 ElevenLabs characters for 60 seconds).

What makes it work (from the formats file):

> One voice tells the viewer something they didn't know, and every idea it names lands as a new picture they can read with the sound off. No face, no live footage. Up to 60 s.
> - A new picture per idea, with something landing inside it every 0.5 to 1 s (median scene about 4 s).
> - The real outputs big and early, one at a time; one number readable on each proof.
> - Narrators run 3.0 to 4.5 words a second, wall to wall, over a bed with a hit on each cut.

```
/cracked-marketer:make-video narrated motion graphics from the script on card [n]
```

**A real run:** a 2026-11-18 demo for Grüns, a daily nutrition gummy, came back as one file with this post sheet beside it:

```json
{"caption": "60+ ingredients, 21 vitamins & minerals and 6 g of fiber in one gummy pack a day. Meet Grüns. Voiceover is AI-generated.", "disclosure": "Voiceover is AI-generated.", "ai": true, "people": "none", "promotes": "own", "title": "Chew 60+ ingredients before work", "format": "narrated-motion-graphics"}
```

Why that sheet matters: `"ai": true` because the voice was generated, so chapter 7 switches the AI label on and keeps the disclosure line. The caption came before our caption rule in chapter 4; by that rule it would be one short line and a comment word.

### Recipe 2. Voice over a demo (first cut)

**Best for:** an app or tool that shows its value on screen.
**You supply:** your screens (captured at native 2× in light mode, or filmed off the laptop with a phone).

> - The tool is on screen from the first frame; the first result by 7 s (by 2 s in a screen recording).
> - The screen moves inside the shot about 7 times every 10 s: typing, a cursor, a count-up, a scroll.
> - The payoff reads in one second: one number over the real screen, or the output full frame.

```
/cracked-marketer:make-video a voice over a demo of [what it does] from the script on card [n]
```

### Recipe 3. Silent hook demo, and one demo with many hooks (first cut)

**Best for:** testing hooks cheaply. A person reacts to their laptop under one line, then the real screen does the thing.
**You supply:** one demo filmed off your screen by your phone, ending on the payoff; 3 to 5 openings you film yourself, about 3 seconds each, one feeling, no words.
**Paid:** nothing. The render is free.

> Over the same demo, one opening did 181,933 views and another 1,620: the opening and its line are the variable, the demo is the asset.
> The line is a feeling, a quoted complaint or a short story. Product claims lose (13 of 30 losers, 5 of 37 winners).

```
/cracked-marketer:make-video make 10 videos from this recording: [path to the demo] with these openings: [paths]
```

It writes ten lines from proven hooks in your niche, shows them as one table for your yes, renders all ten with `hook-cuts.py`, and records each on your board's Hooks tab so chapter 8 can tell you which line won.

### Recipe 4. Static ad and carousel (first cut)

**Best for:** Meta ads from chapter 3's winning-ad-ideas, and save-worthy carousels.

> - The words in the image are the hook: 4 to 12 words in the top third. The headline field carries the offer, 27 characters or fewer.
> - The product's real output is the hero
> - A new concept is a new picture, never new text on the same picture.

Carousels: one change per slide, a cover that reads at thumbnail size, reading text 27 px or more, and a last slide with one job.

```
/cracked-marketer:make-video the static for [the idea's code, e.g. WA-1118-1]
```

### Recipe 5. AI presenter (experimental)

**Best for:** a face talking to camera when nobody on the team will film. The presenter is your own labelled character, from your own photo or a made one, never a real person who hasn't agreed.
**You supply:** a photo of your presenter (yourself, or someone who agreed in writing), or say "make one"; an account on a video generator (Higgsfield, Kie or fal). With its connector or command line set up, Claude prices and runs each take; without, it gives you each take as steps to press.
**Paid:** about $5 for a 15-second take at 720p on Higgsfield (Seedance 2.5, about 7 credits a second, read 10 Nov). The voice and the cut are agreed with a still of the face before any take is paid for.

```
/cracked-marketer:make-video an AI presenter video from the script on card [n]
```

> It's labelled as AI, so it presents and never tells a story or a result as its own ("I paid off my card in a year" is a fake testimonial; "you could pay it off in a year" is fine).

### Recipe 6. Drama (experimental)

**Best for:** reach. A small cast acts a 15 to 30 second story; your product turns it.
**You supply:** the same generator account as recipe 5; the cast is made as labelled AI characters.
**Paid:** up to about 120 credits on Higgsfield (about $6) at 480p, or about 270 (about $13) at 720p, retakes included. Every take is priced and asked first.

```
/cracked-marketer:make-video a drama from the script on card [n]
```

> - **The bar is said to the hero's face by someone with power over them, in a room everyone knows**
> - **The turn is a picture at 45 to 65% of the runtime,** in its own shot, readable in a second on a phone
> - **The last line is the hero's, two to six words,** a callback to the bar or a role swap

### When a build goes wrong

- **check-video.py prints a DEFECT:** fix it and run every check again; a fix to one beat can break another, the ending most of all.
- **A caption shows the wrong word:** the captions follow the voice's own word times. Make the voice again if the read differs from the script.
- **The render fails in the Claude app or Cowork:** building needs Claude Code on your computer.

---

## 7. Post: your accounts, your times, the keyword DM

**What it does:** schedules your finished videos on your own accounts through your own Zernio, at each account's best times from its own numbers, after one yes to one table. Sets each platform's AI label, the disclosure line, and the DM everyone who comments your keyword gets.
**What comes out:** posts scheduled on Zernio (they go out with your laptop closed), each row on your board set to Scheduled. Run it in Claude Code on the computer that holds the video files.
**Status:** first cut. **Time:** 20 minutes to connect; then a minute a batch. **Cost:** Zernio's (chapter 0). Vamos credits: none.

### Install once

1. Make a Zernio account at zernio.com and connect your Instagram, TikTok and YouTube there. Connect TikTok through Zernio's TikTok for Business app.
2. Add Zernio to Claude:
   - Claude app (to check, move or cancel what's scheduled from any chat): Customize → Connectors → Add custom connector, URL `https://mcp.zernio.com/mcp`.
   - Claude Code (where posting runs, beside the video files):
     ```
     claude mcp add --transport http zernio https://mcp.zernio.com/mcp
     ```
     then `/mcp` to sign in.

Vamos never sees your Zernio sign-in or your accounts' tokens.

### Run it

```
/cracked-marketer:post
```

The first time, it asks which accounts post which videos, how many a day, and proposes times from each account's own numbers. Then it shows the batch as one table: account, time, file, caption, AI label, disclosure, keyword DM. Nothing goes out without your yes to that table.

For the keyword DM, end the video and the caption on the ask ("Comment GUIDE and I'll send you the checklist") and tell Claude what the DM sends. On Instagram and Facebook, everyone who comments the word gets the DM with the link. TikTok, Threads, LinkedIn and YouTube have no DM to a comment, so it posts a public reply there saying where to find it. Never write "link in bio": the comment word does the work.

### Our rules for this step, word for word

> - an AI label on every post that holds AI footage, faces or voice, set in the platform's own field; where the API has none (Facebook, Threads, LinkedIn), that row is posted by hand with the label on;
> - the disclosure line in the caption ("Made with AI." when the sheet gives none), and #ad on a paid partnership;
> - nothing posts an AI version of a real person who hasn't agreed; the user's own AI twin, or someone's with their written yes, posts with the label;
> - each account stays under its platform's posts in 24 hours (TikTok 15, Facebook 30, Instagram 100)
> - the same video twice on one account within 24 hours is refused

> A yes covers that table only: a row changed after it ("move 3 to 18:00") is shown again and needs its own yes.

### A real example

Our post from chapter 4 ended on "Comment SLEEP", and the DM sent the setup. It drew 134 comments on 7,171 views. A caption by our rule today would be:

```
Claude ran her Instagram while she slept

Comment SLEEP and I'll send you the setup
```

### When it goes wrong

- **A row prints DEFECT:** the table names why (a missing label, an account over its daily cap). Fix it, or drop the row.
- **TikTok:** when you say yes to the table, TikTok rows post at their times like the others (TikTok asks that you've watched each video; your yes is that). Only on the hands-off path (chapter 9), where nobody saw a table, does TikTok get each video in the account's TikTok inbox instead, for you to add the caption and tap Post, up to 5 waiting a day.
- **No Zernio:** post gives you the batch as a table for your own scheduler, AI label column included.

### Check (Claude)

- [ ] `accounts_list` shows the person's accounts.
- [ ] The table was shown, and every created post went out after the yes.
- [ ] Each AI row has its label on, or is listed as by hand.

---

## 8. Learn: what worked, counted

**What it does:** reads your posts against your own median, counts each pattern against the misses, checks last week's predictions, and writes what to repeat, stop and turn into an ad. Records the lessons every other skill reads first.
**What comes out:** one sentence that says what to make next and why, three lists (Repeat, Stop, Turn into an ad), and new rows on the board's Lessons tab.
**Status:** works today on public numbers; reach, saves and watch time through Zernio are a first cut. **Time:** about 5 minutes. **Cost:** about 15 credits.

### Run it

```
/cracked-marketer:content-log
```

Run it once posts are 7 days old. Monday is the default.

### Our rules for this step, word for word

> **Repeat.** A 5× outlier or more gets 3 to 5 versions for next week, each written out as its own line; at 3 to 5×, one. A version is the hit's sentence as one clause, with only its subject swapped for one as big for the viewer. One creator's "Claude just killed LinkedIn" got 4,538 and "Claude just killed Instagram" got 429,776, so what you swap in is what to get right.

> **Stop.** Only a Confirmed lesson with the action Stop: 3 or more posts from different weeks under the median … One flop never goes here, and a post under 7 days old is never a flop, here or in a hunch.

> - **Hunch:** under 3 posts. **Testing:** being tried on purpose. **Confirmed:** 3 or more posts from different weeks. **Dropped:** a test that failed twice.

> Views with no profile visits is a profile or call-to-action problem, not a content one.

### A real example

**Input:** a content log on Wispr Flow's accounts (a demo, 18 Nov 2026).

**Output, the Lessons it wrote:**

> - Hunch: a prop-led voiceover film (TikTok words milestone) is the one clean outlier, 5.4x; same film on IG 0.7x, so test per platform.
> - Hunch: launch demos land near the median (1.0x to 1.2x) and carry no download CTA; add one.
> - Correction: the IG keyboard film (561,943 views) has likes at 0.40% of views, so it reads as boosted; it is not counted as a 20.0x organic outlier. Check Instagram Insights.

**Why it passed:** the biggest post by views was set aside as likely boosted (likes under 0.5% of views), so it didn't teach a false lesson; every lesson rests on fewer than 3 posts and says Hunch; and it ends with a prediction to check next week.

### Check (Claude)

- [ ] Every × came from `count.py`, with the date read.
- [ ] Nothing is on Stop or Confirmed with fewer than 3 posts from different weeks.
- [ ] What works for me was saved.

---

## 9. The weekly loop

**What it does:** runs ideas, scripts and the content log on a schedule, with your laptop closed, stopping where you choose.
**What comes out:** new ideas on your board twice a week, scripts for the ones you approve, a Monday report, and a digest after each run.
**Status:** works today; check its first run. **Time:** 10 minutes to set up. **Cost:** 130 to 200 credits a week (Vamos Pro).

### Run it

```
/cracked-marketer:loop
```

It asks once:

> Where should it stop for you?
> 1. After ideas (default): new ideas wait on the board; scripts are written only for the ones you approve.
> 2. After ideas and after scripts: each script waits for your OK too.
> 3. Run everything and show me: it picks the best ideas by your lessons and writes their scripts. Nothing is sent or paid for, and nothing is posted but what you mark Ready to post, once you've said those go out by themselves.
>
> Which days for ideas (default Monday and Thursday), and which day for the content log (default Monday)?

Then it schedules one task per job, an hour or more apart. The default is **Cowork** (the Claude desktop app from claude.ai/download: Scheduled, New task), which runs with the laptop closed. Add the plugin there too (Customize → Plugins) and connect Vamos on its Connectors tab. Where Claude can't create the task itself, it gives you each task's days, time and prompt to paste into New task. If you only use Claude Code, its desktop app's Scheduled tab runs the same tasks, but only while the app is open and the laptop awake; posting from the loop runs there, on the computer that holds the videos.

### The schedule we'd start with

| Day | Runs | Credits |
|---|---|---|
| Monday 08:00 | Ideas, then scripts for what you approved | about 50, plus up to 60 a script |
| Monday 10:00 | Content log | about 15 |
| Monday 11:00 | Research pack (ad concepts, what customers say) | up to 60 |
| Thursday 08:00 | Ideas | about 50 |

Your part: approve ideas on the board (5 minutes), read scripts (10 minutes each), film or OK the builds, say yes to the post table.

### Check (Claude)

- [ ] The person pressed **Run now** on each task and answered every tool prompt with **Always allow**: a scheduled run that stops on a permission prompt never finishes.
- [ ] New rows from that run are on the board. "Succeeded" alone only means the session ended.

---

## 10. When an output is bad

The most useful thing we've learned: **a bad output is fixed where it came from, not on the page.** Rewriting the one script by hand fixes nothing; the next one comes out the same.

### The method

1. **Get the case:** the bad output word for word, and what's wrong with it in your own words.
2. **Find what made it:** which skill ran, and what it read (your voice guide, What works for me, Vamos settings, the board, the find). Ask Claude: "Which skill made this, and what did it read?"
3. **Name the one root cause before you change anything.** Check in this order and stop at the first that explains it:
   1. **Contradiction:** two instructions pull apart, and the one with an example wins.
   2. **Asked for, never supplied:** a line demanded something nothing gave it (a customer quote with no quotes read), so it was invented.
   3. **Missing a tool:** it needed a source or a tool it didn't have.
   4. **Too narrow:** a rule or an example forces a weak answer.
   5. **Never reached:** the right line sits in a file that step didn't read.
   6. **Unclear:** the line is there and was misread. Reword it.
   7. **A ban it keeps breaking:** say what to do instead.
   8. **Taught by the examples:** a habit the examples model.
   9. **The input:** a weak idea or a find that never qualified.
4. **Fix the smallest thing at that cause.** Usually a deletion, a better example, or one line in the file the step reads. For your brand that's almost always a Brain file you can edit: the voice guide, Things you've said, What works for me, or a Not for me reason. Tell Claude: "Fix this at the cause, in my Brain."
5. **Run it again on the same input**, and one that was already good, so the fix didn't break it.

Our rule for it: subtract before you add. Most fixes are a deletion. A line stays only if a real failure needed it.

### A real example

**The note** (on our own captions, 12 Nov): "the captions should be something short catchy easy to read, not explain the video."
**The cause:** our caption instructions asked for the steps of the video, and their example caption was ours, three lines long. Example beat rule.
**The fix:** the rule became "a line or two someone reads in a second, then the comment word", and the long example was replaced by nine real captions that went viral, with ours rewritten beside them. That's the rule in chapter 4.

---

## 11. Under the hood: how we run it

This is how we run it for our own accounts, not the path to follow. You don't need any of it: the plugin is the runnable version, and we keep it current (chapter 13).

We split the system into bots, one folder each, so when an output is bad we look in the bot that made it:

```
factory/
┣ scout/          finds what's working and turns each find into script items
┣ researcher/     the research sheet for each item
┣ writer/         the script, the hook, and its score
┣ drama-writer/   a drama's story, script and film plan
┣ storyboarder/   the plan, the frames, their checks and redraws
┣ builder/        the finished video
┣ post-copy/      the caption
┣ note-debug/     finds the root cause of each note (chapter 10)
┗ shared/         words several bots send
```

Each bot folder holds `BOT.md` (its job, what it takes in and hands over, the stop, its steps, its cost, and where to look when its output is bad), `instructions/` (every word its steps send a model), `tools.json`, `tests/` and `notes.md` (each note with its root cause and fix, newest first).

One bot's card, as it is (post-copy, shortened):

> **Its one job:** the words that go out with a finished video: the caption on Instagram and TikTok, and the X and LinkedIn posts for a launch film.
> **Takes in:** the approved script (its hook, what it hands the viewer, its keyword and what its DM sends), and the account it posts on.
> **When its output is bad:**
> - The caption explains the video, or runs long: The caption, above; then its examples.
> - The keyword or its ask is wrong: The close and the keywords; then the script's What they get.

**Our stops:** the idea, the script, the storyboard (which is also the yes for its paid shots), and the post. Nothing moves or spends past a stop without a yes.

**What it costs us:** we test every change against a control, so our own Claude usage is far above a single brand's: the storyboard bot alone used about $760 of Claude in the 14 days to 25 Nov, across 189 runs. A single brand on the plugin runs on a Claude subscription.

---

## 12. What it won't do

- Film for you, or make a video in the Vamos app. Videos are built on your own tools (chapter 6).
- Read competitors' private numbers: watch time, saves, reach, demographics, spend, ROAS, sales. Vamos reads public posts and the Meta Ad Library.
- Read your own reach, saves or watch time without your Zernio connected or your Insights screenshot.
- Promise views or virality, or predict a view count.
- Research LinkedIn or X by search: it can open a post you link, but not search them. Instagram, TikTok, YouTube and Meta ads are searched.
- Post without the AI label, or make AI video undetectable.
- Use a real person's face or voice without their written yes. No face swaps onto someone else's footage.
- Make AI video for free: paid shots spend your generator's credits.
- Run outside your Claude plan's limits: a long week on Pro can hit its 5-hour limit.
- Post to TikTok fully hands-off, or post AI video by itself to Facebook, Threads or LinkedIn (those are posted by hand with the label on). More than about 15 posts a day on one TikTok account.
- And by our own rule, not a technical limit: it never sends DMs or emails to creators, never pays anyone, never spends ad budget, and never posts without your yes.

---

## 13. Next

- **Updates:** we ship new versions to the marketplace as formats and models change. In Claude Code, run `claude plugin marketplace update vamos-plugins`, then `claude plugin update cracked-marketer@vamos-plugins`, then restart. What changed is in the changelog: github.com/LazyLines-App/vamos-plugins/blob/main/CHANGELOG.md
- **Help:** the in-app chat at app.getvamos.ai (the ? menu, then Live chat), or contact@getvamos.ai. Tell us the chapter and step where you got stuck; we fix the guide at the cause.
- **The ready-made factory:** everything in this guide, already set up and kept up to date as formats and models change, with nothing to configure. We're building it. Tell us in the in-app chat if you'd want it.
