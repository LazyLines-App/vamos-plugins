# Changelog

One line per change, under the version it ships in. See [MAINTAINING.md](MAINTAINING.md).

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
