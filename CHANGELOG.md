# Changelog

One line per change, under the version it ships in. See [MAINTAINING.md](MAINTAINING.md).

## vamos 0.2.24
- A post's multiple of its account's median views is its outlier score, written "N× outlier", and the baseline is the median, never "usual" (Levi, 2026-11-18). A live analyze answer said "That's 6.9× the account's usual of 868,629"; it now reads "got 5,974,383 views, a 6.9× outlier: the account's median is 868,629 (its 33 Reels at least 7 days old among the last 40)". Under 1× is "0.4× outlier" or "under the median". The shared Numbers rule, analyze, playbook, content-log (its `count.py` prints "median:" and "N.Nx outlier"), ideas (its Vamos asks are for the biggest outliers; `filter.py` says "under a 2x outlier"), hooks, formats, setup, the board's Reviews row and the READMEs all say it, and the skills say it even where Vamos's answer says "usual". creator-research's sheet column is Median views (was Typical views). Graders named usual-by-the-rule are median-by-the-rule and expect "median" beside the number; analyze-video-instagram-getripping, analyze-video-tiktok-chloejp and content-log-week-opusjake get `says-outlier` and `never-usual`.

## cracked-marketer 0.2.22
- The shared outlier wording above, and Cracked marketer's own skills say it too: creator-program (`price.py offer --median`, which replaces `--usual`, and the bonus at "a 3x outlier"), find-creators (the sheet's median views column), brief (its Vamos ask; the creator's page still carries no outlier score or median), make-video and review-draft.

## vamos 0.2.23
- formats reads the optional weekly library measurements with a local parser, preserving missing values, true zero, readable weeks and the counts behind medians. Compact Markdown charts name stored views and the post age when those views were read. Older exports keep the existing reply.

## cracked-marketer 0.2.21
- The shared formats weekly-measurement reader above; ad-only replies retain their existing path.

## cracked-marketer 0.2.20
- The script check's tells below (Cracked marketer's script and setup share `textstats.py`).

## vamos 0.2.22
- script's AI tells are measured on short-form video scripts: 419 viral Reels, TikToks and Shorts (what they say, word for word; 259 AI, tech and marketing, 160 local and service businesses) against 108 short-form scripts from plain Claude (Sonnet 5.5 and Opus 5.5, 40 and 68 in the same niches), in `evals/scripts/shortform/`, counted by `evals/scripts/measure_tells.py`. A script with any tell: main's list 121 of 419 viral (28.9%) and 57 of 108 Claude (52.8%); now 52 of 419 (12.4%) and 73 of 108 (67.6%), and in each niche (AI/tech/marketing 16.2% against 85.0%, local and service 6.2% against 57.4%).
- "It's not X, it's Y" fired on 65 viral scripts (15.5%) and 27 Claude drafts (25.0%). People say "it's not just X, it's Y" on camera as often as Claude writes it (that shape: 10 viral, 4 Claude), so it now catches only the shapes Claude owns: "isn't about X. It's about Y", "That's not X. That's Y", "You don't need X. You need Y", and "It's not a content plan. It's just my morning.", a rewrite's half-fix seen in a replay (4 viral, 1.0%; 7 Claude, 6.5%).
- Dropped: the list of three (30 viral, 7.2%; 9 Claude, 8.3%) and "genuinely" (13 viral, 3.1%; 1 Claude, 0.9%).
- Added the two spoken closers Claude ends a script on: "follow for more" ("follow for …", so "Follow for tomorrow's tray", a replay's half-fix, fails too: 9 viral, 2.1%; 45 Claude, 41.7%), and "save this" (9 viral, 2.1%; 12 Claude, 11.1%). "Follow me for more" stays, because viral creators say it (6 viral, 0 Claude), and so does a comment-keyword closer, because it's the user's offer.
- The other 21 are unchanged. Each fires on 2.1% of viral scripts or fewer. Markdown asterisks are in 38 Claude scripts (35.2%; a transcript can't hold them); seven fire on neither side.
- script-unslop-fresh's draft is now a 30-second bakery reel in plain Claude's own format with the seven tells it writes most, its hook and caption the made-up story. The free unit test gives every tell a spoken line (six are Claude's own) and holds the list to the corpus.

## cracked-marketer 0.2.19
- The script check and rewrite below (Cracked marketer's script and setup share `textstats.py`). Its formats skips Content System's new faceless rule, since a brand's "we won't be on camera" is the team's and its creators film themselves: with a team version of the rule, formats-ads-skincare-both remade Bad, Good, Great as "your team makes it, hands and cutouts only" (job-and-maker failed; main 1/1).

## vamos 0.2.21
- script's code check (`textstats.py check`) names every AI tell it finds, with its fix, and fails on each one the user doesn't say themselves. It now catches the 20 the "20 ways to unslop AI content" video promises: markdown asterisks, "Certainly! Here's your hook:", check-mark lists, "it's not X, it's Y" (and "isn't X. You just Y"), "in today's fast-paced world", leverage, game-changer, genuinely, quietly, "No fluff", the third example in a list of three, "Let's dive in", "I'm excited to share", "Let that sink in", "and it's not what you think", "Stop X. Start Y.", "This matters because", an unsourced "Studies show" (kept as "[your source] shows …"), and a slogan closer ("… is the new currency"). On main it catches 3 of the video's 20 Before lines (in today's, game-changer, let's dive in). A tell the user says themselves stays: one their Voice examples use (`--voice`), or one setup's voice numbers now list (`tells_used`). The old rate rule went, because with the longer list it failed an existing user's own line (opusjake's "And it's not one skill either. It's 11 of them."). facts.txt backs stories only, so a pasted draft saved there by mistake can't excuse its own tells (one replay kept "Stop posting at random. Start posting with a plan." while its check printed no fails).
- The check also reads a story about the user ("I had 40 followers and a tray of burnt croissants") against what they've really said (`--facts`: Things you've said and their words in the chat outside any draft; `--voice`: their Voice examples). A story whose numbers or words nothing they said holds fails, and the skill leaves it as `[your …]` slots in the same shape. The On screen lines and the caption, after a `---` line in script.txt, are checked for tells and stories too, without counting toward length.
- A pasted draft is rewritten before setup and with no paid turn, and its made-up story becomes slots, said in one line and put back when they say it's true; the recap's Next is setup. A rewrite used to keep "their facts", so the AI's invented story stayed. New case script-unslop-fresh (the video's 20 Before lines as one pasted draft) and the free unit test `evals/scripts/test_textstats.py` (each Before line fails on its tell, each After line passes).
- formats: when the user won't be on camera, the formats it ranks need no face and no voice of theirs unless they narrate or say they'll record a voiceover; a format that needs a face goes to More and each card says how it's made with on-screen text, hands, the product or a screen. Before, "assume and say so" left the voice open, and one of two runs remade Vamos's on-camera pick "with hands and a voiceover". New case formats-faceless-fresh.
- playbook-notion-tiktok-instagram gets five-first-lines and best-against-worst, which hold the playbook promise (about 80 posts across TikTok and Instagram, best counted against weakest, five plays each with Your first line). The README's formats and script lines say what they now do.

## cracked-marketer 0.2.18
- formats' ad ask and winning-ad-ideas' research turn no longer set `data_scope: "turn"`, so their rows are the ads Vamos's answer lists, the ones its results view shows in Claude Desktop. With turn scope, rows held every ad Vamos read, and a concept or ad format could rest on an ad that wasn't on screen. An ad format's gate reads the answer's advertiser count with its ads' days running. formats-ads-supplements' grader is now rows-are-the-ads-on-screen.
- formats' reply example shows each card's job and who makes it. Also the Working with Vamos, formats and playbook changes below.

## vamos 0.2.20
- The formats reply is the ranked list, then More, then the recap, with an example of how it opens. A data caveat goes on the card it changes. The working stays out of the reply: the angle check, a second ask, what was left out of Vamos's prose, and why the ask was scoped. formats-other-niche-rip on the same mocks: reply-has-no-process-notes 3/3 (main 0/2), answers-the-ask 2/3 (main 0/2); one run still opened with "RIP itself is in Apps & SaaS".
- Working with Vamos: the reply is about what the user named, and the workspace stays background, named only when they ask about it. A fresh read's check is the skill's working, so the reply carries what passed. In Desktop, the Tempo creators reply opened "Your Vamos workspace is set up for RIP", and formats replies said "A fresh reviewer checked every angle".
- playbook's check before the recap asks for the likely pick named above the plays, so no line has a [bracket] left. The check used to ask for a slot like `[your price]`, which contradicted step 8, and the Wispr page in Desktop kept "[age]" and "[your landing page]".
- creator-research gives a creator on two platforms one row: the account with the higher typical views, the one the results view leads with. The other account goes in Why them ("also TikTok, 19.4K"). In Desktop the Tempo reply's "best views" used Chloe's TikTok while the view led with her Instagram. New case creator-research-two-platforms: 2/2, main 0/2 (main writes both rows).
- The formats mocks (coach, skincare, b2b, other-niche RIP, and Cracked marketer's ads-skincare) are cut to the formats each answer names, which is what the default scope returns. Their graders name only those five formats.

## cracked-marketer 0.2.17
- The formats and playbook changes below.

## vamos 0.2.19
- formats ranks the formats Vamos's answer names, the ones its results view draws on screen in Claude Desktop. The ask no longer sets `data_scope: "turn"`, which added every format Vamos read (71 in one run, 15 readable) after the cited ones, so the reply ranked formats that were not on screen and called two that were "cooling, not ranked". Now every format in the rows is ranked in the reference's order, and one that fails the gate goes to More with its reason. The reply opens on the ranked list, and the job line no longer sells the angles as "checked by a fresh reader". New graders on formats-other-niche-rip: rows-are-the-formats-on-screen passes 2/2 (0/2 on main); reply-has-no-process-notes still fails, as on main, because the reply mentions the angle check in passing.
- playbook writes each play on the page the way the reply shows it: a numbered name, then Seen, Your first line, Outline, Watch and Paste as a list. Step 8's example was one paragraph, and Claude Desktop's page ran the five parts together ("history. - Seen: … - Your first line: …"). Skip is a list too. New grader page-lists-each-play on playbook-duolingo-tiktok.

## cracked-marketer 0.2.16
- The playbook change below.

## vamos 0.2.18
- creator-research's sheet is one short row per creator: Creator, Platform, Followers, Typical views, Contact, Why them (up to 15 words, a competitor's deal marked), Draft DM and Status. 0.2.17 asked for each creator's "content, audience, views, deals and contact", and the Tempo sheet in Claude Desktop came out as 18 tall rows with half the columns off screen. The Draft DM is two sentences the user sends from their own account; the reply names the three who stand out.
- playbook's page is "Plays to steal from [target]": the plays come first, then what they stand on. A play's parts are Seen (what they run, linked, and why it keeps running), Your first line, Outline (the three or four beats after it), Watch and Paste; Outline replaces Work, so the user can film the play from the page.
- playbook answers a question about what a brand runs ("what Meta ads is Huel running, and which have run longest?") in the reply, with what it means for the user's brand, and offers the plays as Next: no page and no plays nobody asked for. Every other ask, "what to steal" included, still gets the five plays and the page. New case playbook-ads-question-gruns.

## cracked-marketer 0.2.15
- The formats and Working with Vamos changes below.

## vamos 0.2.17
- A niche their brand isn't in is an ask for another account: formats runs every step for a general account in that niche, angles included, opens with the scope ("Fitness accounts in general, on TikTok, Instagram and Shorts.") and offers in Next to make them for the account they name. In Desktop on 0.2.16 the reply ended "I didn't write content angles because you don't have a fitness brand".
- The setup suggestion is for asks about their own brand. On a fitness ask from an app's workspace with no setup, Claude turned it into "Your workspace is set up for RIP, so this isn't tailored". Opus still adds a clause like that on about half of the eval runs (formats-other-niche-rip).
- formats no longer says Vamos shows its formats under its answer; the connector doesn't draw that view.
- creator-research carries the Working with Vamos block, so its reply ends with the recap and the credits used (the Tempo run used 48 and never said so), and each creator's line is about their content, audience, views, deals and contact.

## cracked-marketer 0.2.14
- The playbook page change below.

## vamos 0.2.16
- The playbook page no longer says Vamos's own view shows the posts and ads with their pictures: the connector doesn't draw that view yet, so the reasons for a page without pictures are the Artifact viewer and the sandbox, and each post or ad is a link.

## cracked-marketer 0.2.13
- The Content System change below.

## vamos 0.2.15 (Content System)
- The ask decides: a brand, niche or platform the user names wins over the workspace's, and the ask runs in the same turn. Asked "What trending formats are working in fitness?" from a workspace about an app, Claude Desktop stopped to ask "Who are these fitness formats for?" before any research; formats now asks Vamos about the niche in general and says so in one line.
- Credits are reported in the recap, not announced before a step: Claude asks first only when what's left is below a step's cost. The old line put "the research run costs up to 60 of your 90 remaining credits" into that question; the run cost 17.
- formats assumes face and voice when the user hasn't said, and says so, instead of asking.
- Where the host has no subagents (the Claude app), the fresh check runs as a separate pass instead of being skipped with a note: the fitness reply ended "The skill normally runs a fresh outside check on every angle before showing them. I skipped that step".

## cracked-marketer 0.2.12
- The Content System change below. Formats makes no page; an ad format's card is in the reply.

## vamos 0.2.14 (Content System)
- A plain ask finds its skill: "What Meta ads is Huel running, and which have run longest?" loads playbook. In the Claude app the SessionStart hook arrives only after the first tool call, so the skill descriptions carry the routing alone.
- Only playbook makes a page, and it is a Markdown document the host lays out itself, with no pictures and no counters: the Artifact viewer blocks images from other sites and the sandbox has no network, while Vamos's own view under its answer shows the posts and ads with their pictures. The HTML shell and `embed.py` are gone.
- setup, formats, ideas, content-log and analyze make no page: the reply, Vamos's own view and the board hold what they found.
- playbook's reply is short: the strip, the answer, what wins counted, the part the ask named, and the plays. The other sections are on the page.
- playbook writes its plays straight into the page, so the page can't be skipped: on Sonnet replays it was left out on 2 of 3 runs, main included.
- formats keeps no `data.json`: it was the page's data, and the reply said "I didn't write data.json".

## cracked-marketer 0.2.11
- The Content System change below: each page is Claude's own write-up of the run, in the quiet answer-report look. An ad format's card says its ads, advertisers and longest days running in plain words.

## vamos 0.2.13 (Content System)
- Each skill's page is Claude's own write-up of what the run found: the answer first, then the sections that run needs, named and ordered for it. The page kit is a short style shell in the answer-report look (light and dark, the orange only for what wins) with a few pieces to use or skip; the fixed sections, counters, pixel title and field schema are gone. `embed.py` puts a finished page's pictures inline and takes out any that fail, so no empty box is left (it replaces `fill.py`). The playbook page keeps the five plays with their Paste to copy; setup's keeps what is set and how it runs from here.
- The page is written in plain words, the way you'd explain it to them. formats' card is cut to what picking a format needs (what it is, why it's first, how many posts in their niche use it, how they'd film it, an example or two, its angles); the stage, beats, range or a risk go in when they help. The playbook page tells the plays in plain words.

## cracked-marketer 0.2.10
- The Content System changes below (the path, the board as home, the next step on a yes).
- setup's path names both ways a video gets made: a creator films it from its brief, or make-video makes it.
- script offers make-video when the team wants the video made.
- "approve 1 for us, 3 for creators" says which ideas the team makes and which a creator films.
- The install works in the Claude app too: Customize → Plugins → Add marketplace, `LazyLines-App/vamos-plugins`.

## vamos 0.2.12 (Content System)
- Every run ends with its next step as a question (both, when the skill names a choice), and Claude runs it on your yes, so there are no commands to remember. The recap links your board.
- setup tells you how it runs from here (ideas at To review, your yes, the script, your video, one table to post, the content log) and that any part works alone.
- "what's next?", "where am I?" or "show my board" opens setup's home: what waits for your yes, with the board's link, and the next step (scripts, filming, the post, or new ideas).
- The board fits what you already use: setup asks where you plan and post, adds its columns to your own Notion or Sheet content calendar instead of making a new one, and hands posting batches to your own scheduler (Later, Buffer, Metricool).
- A new Notion board shows each card with its source video's thumbnail, and a calendar of what goes out. When the calendar you keep isn't connected in Claude, setup asks you to connect it first; with none at all, it says in one line what connecting Notion gives and moves the board there once you do.
- A finished video goes on by its link on the card and Ready to post, from any host, or by telling Claude where it is. The path says what Zernio is.
- "approve 1 and 3" in the chat works on every host, not only Claude Code.
- loop picks the scheduler for you: Cowork by default (with the desktop app's download and the plugin's install path), the Claude Code desktop app when a run needs this computer's files, a cloud task only when you ask.
- Connecting Vamos in Claude Code is named everywhere it's needed: `/mcp`, pick vamos, sign in. The README gives one install path for the Claude app and says what a free account covers.

## cracked-marketer 0.2.9
- The Content System changes below (post, and the board's File and Post columns).
- make-video makes dramas: a short scene acted by characters you made, one voice per character, every take priced and asked first. drama-cut.py builds the cut on whole frames with the song's drop on the turn; place-line.py fits a take that said its line at its own pace, before anyone pays for a retake.
- make-video writes a post sheet beside each finished file (caption, disclosure, whether it holds AI footage, whose face), so post sets the right label.

## vamos 0.2.11 (Content System)
- New skill, post: schedules your finished videos on your own Zernio, many accounts and many a day, after one yes to one table (account, time, file, caption, AI label, disclosure). Zernio checks every post first. AI footage gets each platform's AI label and the disclosure in the caption; on Facebook, Threads and LinkedIn, whose APIs have no label field, an AI video is posted by hand. An AI version of a real person who hasn't agreed is never posted.
- loop posts what you mark Ready to post once you say those go out by themselves. TikTok then gets them as drafts in your TikTok inbox, where you tap Post.
- The board adds File and Post columns.

## cracked-marketer 0.2.8
- The Content System changes below (the usual at 7 days).
- creator-program prices a creator from their posts at least 7 days old, and make-video's hook test reads each cut's multiple once it's 7 days old (a cut already past the usual shows as "so far" sooner).

## vamos 0.2.10 (Content System)
- The usual counts posts at least 7 days old, as Vamos's own usual does (it was 3 days). A younger post already above it shows as "N× so far" and can go on Repeat or the ad list; one under it is too early, never a miss. Hit rate, patterns and lessons count only posts at least 7 days old. Reposts and paid posts are set aside at any age.
- content-log keeps a prediction open when the post it rests on is still too early, and checks it at the next review.
- content-log gives every paid creator a call (more, wait or drop) with the number behind it. A creator whose posts are still too early waits.

## cracked-marketer 0.2.7
- The Content System changes below (playbook's stopped ads and slots, content-log's cohort grid).
- ideas leaves competitors' running Meta ads to winning-ad-ideas.
- find-creators looks for creators who film the formats the category's long-running Meta ads use and the brand's own ads don't, and the sheet adds each creator's best recent post with its multiple and date.
- creator-program tracks each wave of creators on one cohort grid: Test and Core stages, counted 30 days after a creator's first video (our proposal), who moves up, who stops and who gets a raise.

## vamos 0.2.9 (Content System)
- playbook's ads read asks for each stopped ad's end date. Meta shows stopped ads only for ads that ran in the EU or UK. Where they come back, it counts what the ads running 30+ days share against stopped ads that ran 14 days or less. With none back, it says stopped ads aren't visible and ranks on days running alone.
- playbook writes a product fact you didn't give as a slot (`[your price]`) instead of making one up.
- content-log's creator record keeps the creator program's cohort grid up to date.

## cracked-marketer 0.2.6
- The four Content System changes below (content-log's ad account, playbook's customer read, ideas' dates, loop's exports).
- winning-ad-ideas reads your neighbours' running ads beside your competitors', lists what each brand launched this week, and has three blind judges score its concepts: your account's track record, your customers' own words, and an assassin who looks for the reason each fails. A judge without evidence sits out, and a judge sitting alone kills nothing. Every kept concept gets a code (`WA-1112-1`) to put in the ad's name, so the content log finds it in your Ads Manager export.
- loop can run a Monday research pack: playbook's customer read when the last one is missing or over 28 days old, then winning-ad-ideas, opening on the ad account's week.
- loop sends each Approved row by who makes it: brief when a creator films it, script for the rest, and a Meta static is named for make-video.

## vamos 0.2.8 (Content System)
- content-log reads two ad-level Ads Manager exports beside your posts, never instead of them: the account's week against last week (spend, CPA or cost per lead, ROAS), risers, fallers and stopped ads, the words in your ad names that win, and which ad concepts ran, by the code in the ad name (`scripts/ads.py`). Vamos sees no spend, so every spend figure comes from your export.
- playbook's read of what customers say covers comments, reviews and Reddit (through a web search), plus a survey CSV when you give one. It counts the lines into groups in code and writes hooks from the biggest group.
- ideas pins the dates coming up in the next six weeks to this run's ideas when a web search is available. A date alone never makes an idea.
- loop's content log uses the Ads Manager exports in the project folder when ads are on.

## cracked-marketer 0.2.5
- formats ranks the Meta ad formats your category keeps paying to run 30+ days, statics included: a format ranks only when 2 or more advertisers have run it that long, and every card says its job (reach, trust or buy) and who makes it (your creators or your team).
- setup works when nobody talks on camera: it asks who does, and when nobody does it writes the brand voice from the site, captions and Meta ad copy, then tests it against a real caption it held back.
- hooks reads the opening lines of the category's long-running Meta ads beside the posts that beat their creators' usual. A line read from the ad itself is a proven hook, ranked by days running; one from the ad's copy only is marked "ad copy".
- ideas, analyze, hooks and formats name the next step by who makes it: brief when a creator films it, script or make-video when your team does.
- "competitor" instead of "rival" throughout, README included.

## vamos 0.2.7 (Content System)
- A skill page's card can carry a stat and an example's meta line; pages without them are unchanged. check.py accepts Ad Library links.
- "competitor" instead of "rival" in ideas and playbook.

## cracked-marketer 0.2.4
- Every skill page shows a handle with one @, whether the run wrote it with one or not: a setup page listed its rivals as "@@clickup".

## vamos 0.2.6 (Content System)
- Every skill page shows a handle with one @, whether the run wrote it with one or not: a setup page listed its rivals as "@@clickup".

## cracked-marketer 0.2.3
- content-log's Turn into an ad holds a breakout to the keyword comments per 1,000 views that the account's posts of its size get, not its plain usual: that rate falls as views grow, so the old test passed 14 breakouts on 10 brand accounts and this one 32 (`count.py --ads`).

## vamos 0.2.5 (Content System)
- content-log's Turn into an ad holds a breakout to the keyword comments per 1,000 views that the account's posts of its size get, not its plain usual: that rate falls as views grow, so the old test passed 14 breakouts on 10 brand accounts and this one 32 (`count.py --ads`).

## cracked-marketer 0.2.2
- creator-program says how many creators to message for the number you want filming (about 30 each, marked rough, with dated reply and sign rates and how sure each is), sends them in waves with follow-ups on day 4 and day 10, and sizes the next wave on your own rate. find-creators treats its sheet as the first wave, drafts the two follow-ups, prices the rest of the names, and its first message gives the pay, the number of videos and by when.
- creator-program writes the ad-use terms before anyone films (run their posts as Spark or partnership ads through a per-post code: 60 days, 30% of the base, our proposal beside dated published ranges; terms already agreed stand) and the code ask a creator can follow and trust. content-log writes that ask out for each creator's winner, with the agreed fee or a slot, whatever the ads setting.
- loop: on the content-log day, a creator program gets the creators' week: results (a read under 2 days old is reused for free), one brief per creator, and drafts of the code asks, chases for videos past due, the payout list (bonus pool paid in order, each code's fee, summed in code) and codes ending within 5 days. Nothing is sent or paid. Its description names the creators' week and "every Monday".
- brief prices its research turn at what it cost live: up to 60 credits, about 40 for three creators.

## vamos 0.2.4 (Content System)
- loop's description routes "every Monday" and "every week" asks; each run reads a creator program first when there is one (none in Content System), so nothing changes in a Content System run.

## vamos 0.2.3 (Content System)
- The six old command names (competitor-research, content-strategy, content-system, video-breakdown, viral-research, write-like-me) are gone, as 0.2.0 said they would be.
- The shared Vamos block is about 120 tokens shorter: what the connector's own tools now say (polling, the 60-credit cap, a save as its own message, the row switches, which reads are free) is no longer repeated.
- setup no longer says setting up again re-reads every account or rewrites the voice (a repeat only adds), and says the free first chat turn is an account's first ever.
- Hooks and scripts need setup only while there is no voice guide; with a voice and no board, hooks keep the hooks in the chat, as before.
- The start hook routes formats and breakdowns to their skills.

## cracked-marketer 0.2.1
- make-video loads for a plain ask for narrated motion graphics, an animated explainer, a narrated video or a demo with a voiceover; before, a detailed motion-graphics brief went straight to building, with no plan, price, stills or checks.
- make-video's check-video.py hears the finished video's own audio against the script (a take or a fix that changes a word fails), fails a first frame of one flat colour (the feed's cover), and with `--beats` reads the screen at the word each line names its thing, writing a beats sheet for the look and the fresh reviewer. Every check runs again after each fix.
- make-video breaks captions at phrases with `scripts/captions.py` (never after "are", "their", "can", running a caption long rather than break there) and spells them as the script does where the transcriber mishears a name; check-video.py fails a caption that ends on a word that needs the next one.
- make-video checks each generated take with `scripts/check-take.py`: its sound must still be the read it was given (a re-voiced take is redone alone, never patched), its words match the line (a word the transcriber mishears in your read too is only flagged), and its eyes are open over the part used and on the cut frame.
- make-video shows the stills before any cut is built, and asks the paid takes' yes with the cut they go into (built with the voice and a still of the face), not with the plan; models.md gives the step-by-step hand-off for a founder who submits takes by hand (omni reference, the voice video in the video reference slot, audio on, the credits on the button as the price) and the Seedance prompts that worked, with what each got right and missed.
- winning-ad-ideas judges look-alikes on the user's remakes, not the source ads: two sources only count as one picture when their headline and body match word for word or the answer shows the same person or thing in the same setting, and each picture is named as the user will shoot it ("your pharmacist at the counter"), the source's who played by theirs.
- The shared Vamos block is about 120 tokens shorter: what the connector's own tools now say (polling, the 60-credit cap, a save as its own message, the row switches, which reads are free) is no longer repeated. setup no longer says setting up again re-reads every account or rewrites the voice (a repeat only adds), and says the free first chat turn is an account's first ever. Hooks and scripts need setup only while there is no voice guide.
- setup's home page lists Cracked marketer's own run order, from find-creators to analyze. The start hook routes creators to find, pay or brief, ad ideas, formats, breakdowns and making the video to their skills; the description and README name every job.

## cracked-marketer 0.2.0
- New skill, review-draft: checks a creator's draft video against the brief they filmed from. Pass or fix; each fix a timestamped note to paste to the creator; the brief's must-haves ticked one by one (the hook word for word, the hook on screen, the product by 3 s, the ★ line as written, the disclosure) by `check_draft.py`, against the brief that video was filmed from when a creator has several (it picks by what was said, or `--brief`), with part 6's don'ts listed to look at and "not sponsored" never read as a disclosure; your own notes tagged "in the brief" or "new ask"; the revision round counted against the program's. In Claude Code it reads the video itself (`draft.py`: ffmpeg frames, and a transcript from the creator's captions file or whisper.cpp, free and local); on claude.ai it works from the transcript and screenshots you give. No Vamos credits.
- content-log reads creators' results (below); brief points to review-draft next; creator-program saves each creator's videos, due dates and rounds of notes for them.

## vamos 0.2.2 (Content System)
- content-log: for creators you pay, each one's posts for the brand against the usual of the account they went up on (never counted in that usual, even when tagged paid), where a miss broke, cost per 1,000 views from the program's deal, posted against due, hooks pooled across creators with the dead ones, and who to double down on with each kept creator's next-brief change (`count.py --pay`, `references/creators.md`). Every linked post counts whatever the period, share links (`?igsh=…`) match their post, a link that matches no row is named, a program's bonus pool caps the bonuses in posting order, and hooks rank by how many tries beat their usual. Flags a post for the brand with no paid-partnership label or #ad.

## vamos 0.2.1 (Content System)
- hooks says the one thing once: no setup for the next words to knock down, and never the viewer's problem said back. A stunt or before-and-after you'll film needs no line from Things you've said.

## cracked-marketer 0.1.1
- hooks says the one thing once: no setup for the next words to knock down, and never the viewer's problem said back. A stunt or before-and-after you'll film needs no line from Things you've said. (the shared hooks skill)

## vamos 0.2.0 (Content System)
- A session-start hook tells Claude to load the matching skill before calling a Vamos tool directly, so "what's going viral" and ad asks run through the skill (in Cracked marketer too).
- content-log replaces results: every pattern counted against the misses, three lists (repeat, stop, turn into an ad), and private numbers only from Instagram Insights screenshots you paste.
- setup reads your workspace first (`get_workspace`, free). On a workspace that's already set up it keeps your voice and Brain and only adds competitors, so it never runs or bills a second setup.
- setup passes the competitors and creators you name into Vamos's setup, where they're tracked for free; runs its research turn in setup's own chat; asks only what your message and the workspace don't already say; counts a Brain file as saved only when the workspace lists it; and offers one priced follow-up when the research leaves parts out, instead of sending it. The price it states is "at most 60 credits a turn".
- Every skill saves Brain files and structures with `save_brain_file`, free and with no Vamos turn: setup's files, analyze's structures (as Brain skills), content-log's What works for me, ideas' Brain-file board and calls, formats' Not for me, loop's board and settings. The voice guide, content plan and profile notes still change in a Vamos chat. A save is reported only when it comes back.
- setup says what it costs: setting up and saving the Brain files are free, and on a fresh workspace so is the research turn; a research turn on a workspace set up before, the voice guide message, each voice correction and any follow-up bill at most 60 credits each.
- script and analyze read your structures free from `get_workspace`'s skills, so the one paid turn is only for the find.
- Every skill: a repost is the same caption as an earlier post within 2 s of its length, and a boosted post has likes under 0.5% of views or is tagged paid, wherever the usual is computed.
- analyze reads a whole profile as well as a video (its hits against its misses, the patterns counted, each structure that repeats), reads every post the research saw for the usual, sets tagged paid posts aside with the boosts, saves a structure even while it is unproven, and makes a page: the hit beside its miss, beat by beat. A flop is set beside a post made the same way that did 3× as well, instead of being asked why it did so well.
- analyze: a re-cut counts in the usual and can be the pair. With no rows it offers to save the structure instead of saving it. On the page, a post with no thumbnail shows its hook as text instead of an empty frame, and the usual's line shows under the kinds when there is no pair.
- Every skill: credits used is the poll's `creditsCharged`, or says it couldn't read it; an answer saved to a file is read in parts, not asked for again; rows can cover every post the research read (`data_scope: "turn"`).
- playbook: reads only what you asked for (organic by default, ads, paid creators or unhappy customers when you ask), one ask for every platform, and no scope question before it starts. An account Vamos hasn't read gets a watch turn before any hook is quoted. The usual follows analyze's repost rule. The ask no longer dictates a row format to Vamos. A worked play shows the shape (Seen, work, number to watch, your first line on their real hook, a prompt to paste); counted traits go on the page.
- playbook: every play has five named parts (Seen, Work, Watch, Your first line, Paste), the page is built on every run before the reply, and the reply then gives every play whole, the same five parts as the page, ads give the longest-running with its days, and the usual counts only the target's own posts, not collaborators'.
- Every skill: reads the voice guide and Brain files free with `get_workspace`, not a paid Vamos turn, and asks once for every platform (the file link carries 200 rows).
- ideas: filters the rows in code before judging or watching (`scripts/filter.py`: 2×, 21 days from the read, 150 s, the board, one find per video posted on two platforms), keeps three to five ideas per find with the straight swap first, turns an ad find into an ad in its own format, and makes a comment ask an idea only when it is a specific want or a buy ask.
- script writes in your voice from free reads (voice guide, Voice examples, Things you've said), spends at most one turn, on the find's transcript, keeps the find's beats in your own words (overlap is checked against the find only, since your repeated lines are your voice), leaves a `[your …]` slot for any story only you know, shows the whole script in the reply, writes in your language, and fires on "write my next reel" and "write a reel about [a story of yours]".
- hooks reads your voice and board free, reuses the Hooks tab (your hook database) when it holds 10 or more proven hooks from the last 14 days (not the ones it wrote), asks for proven hooks by what you sell and your format, judges and fixes a hook you wrote with your original beside each change, rewrites a hook a cold reader misreads from the same post or line or drops it, and checks the kept hooks in code (sources, three layers, no shared phrase, a silent line in one glance). It says a stunt or a before and after in a sentence of its own, holds the on-screen line to the same tests as the said one, puts your own best lines through the same advice filter as proven posts, keeps a silent line to about seven words, and credits every hook to the post or the line of yours it keeps.
- loop: a scheduled task runs `/vamos:loop run [job]`, so each run follows your approval setting and ends with a digest; on "run everything" it finds ideas before it writes their scripts. It moves a local board off your laptop before scheduling, prices the week from measured costs (ideas about 50 credits, a content log about 15), and suggests the free Weekly brief instead of a Vamos Routine.
- formats ranks what's new to you first (rising, then proven elsewhere and barely used in your niche, then in-niche formats you haven't made) and shows how many posts in your niche use each ("not counted" when Vamos didn't count); one Vamos ask, rows for every format it read, the lead example plays from its video link; a profile link or a claim no row backs never reaches the card; the reply lists the ranking with each angle's first line.
- formats keeps two or three angles a format (fewer than two that pass sends it to More), asks Vamos for each example's opening line for the straight swap, and says so in the reply when nothing is rising.
- formats reads each format's stage from the row's `status` (early or trending is rising) and the niche count from `niche_examples`, ranks in its own order, not the order Vamos recommends; the page and the checked angles are the job, so they run with no setup or when the user is away; waits for the angle check and checks rewritten angles again; builds the page with `fill.py`, whose format card now leads with posts in your niche and a stage badge.
- Renamed: competitor-research is playbook, video-breakdown is analyze, viral-research is ideas, content-system is loop; content-strategy and write-like-me split into setup, ideas, content-log, script and hooks. The old commands still work in this release and go in the next.

## cracked-marketer 0.1.0 (first release)
- New plugin: Cracked marketer by Vamos, the marketing hire for a brand or startup. Holds Content System's nine skills, built from the same source. Every Content System line above is in it too. Its own skills are below.
- Same Vamos connector as Content System. Installs from this marketplace only.
- creator-program prices the creators you found off their worst videos, lists what to agree before anyone films, and ends with each creator's first DM and a day-4 follow-up at that offer; brief puts each creator's pay and terms from the program in their brief.
- find-creators: a sheet of every creator Vamos finds for your brief (people already posting about you, creators your rivals use, creators brands rehire, fresh breakouts), each with how many recent posts are on topic and on camera, deals seen, the contact from their bio and a first message for you to send; sets up the workspace first when it is new, never twice.
- creator-program: plans a brand's creator program: how many creators, what to pay each per video against a dated table of published deals, whose accounts they post on, a 30-day test when nothing has won yet, and how to read results. Prices a creator off their floor (the median of their 10 worst recent posts) in code, answers a rates question free, and saves the plan as a Brain file for brief and content-log.
- winning-ad-ideas: 10 Meta ad concepts for your brand, each remade from a competitor's or your category's ad that has run 30+ days, in its format, each a different picture; catalog ads and ads under 30 days are set aside.
- brief: turns an approved idea into a one-page brief each creator can film from on their phone (the hook word for word, three talking points, the product on screen by 3 s, reference videos, what to send), checked in code, in one briefs doc; the proof stays with you, and it never sends anything.
- make-video: makes the finished video, static ad or carousel from an approved script, idea or reference, on your own tools. Six formats (narrated motion graphics, a voice over a demo, a silent hook demo with your own opening, AI UGC with your own labelled presenter, a static ad, a carousel); every paid shot priced with its model, length and cost and asked first; voice before presenter; key frames before the build; `scripts/check-video.py` checks size, length, loudness, lead-in, captions and the post caption before you watch it. Vamos never renders; your tools do. One demo, many hooks: "make 10 videos from this recording" turns one phone-filmed demo and 3 to 5 of your own openings into ten cuts, each line from a proven hook with its link and multiple, rendered free by `scripts/hook-cuts.py` and checked in code (length, the line on screen from frame 0, the hard cut); content-log's multiples pick the winner for the next ten. A remake keeps the reference's hook sentence with the topic swapped.
- startup-deals is a standalone skill (below), not part of Cracked marketer.

## startup-deals (standalone skill, `skills/startup-deals/`)
- The startup credits, grants and deals you can get, after five questions (money raised, accelerator or VC, company age, team size, country): what to apply for first, what won't work for you and why, each re-read on the program's own page, and the kit's monthly price from official prices only.
- A skill of its own, not part of either plugin, so it isn't tied to the content system. It needs no Vamos connector or account: it asks for stage, team size and country, spends no credits anywhere, and its answer no longer ends with the Vamos recap line. The Vamos plan in the kit's price is assumed Pro unless the founder says otherwise. Install: zip the folder and upload it in claude.ai under Settings, Capabilities, Skills; in Claude Code, copy it to `~/.claude/skills/startup-deals/`.
