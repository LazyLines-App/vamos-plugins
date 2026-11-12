---
name: "setup"
description: "Start here. Sets Vamos up for your brand in one sitting: reads your socials and site, learns your voice from your own videos, finds and tracks your competitors, and makes the board where ideas wait for your yes. Run it again any time to see what's set up, where to edit it, and what to run next."
---

# Setup

**The job:** by the end, Vamos knows the brand, writes like them, tracks the accounts that matter, and the user has seen it work and knows where to change each part. Setup is also the home: on a workspace set up here before, skip to step 7 and show the home page.

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas need it, and so do hooks and scripts while its `voice` is false, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** One Vamos chat per job (`create_chat`); follow-ups go in it. Add `include_data: true` when you need the rows. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50 posts (30 ads, creators or formats), so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file`, always as its whole text, so read one first to add to it. Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 3 days old, leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer:

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/cracked-marketer:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**0. Check, free.** Call `get_workspace` and `get_credit_usage`. The workspace is one of three:
- **Set up here before:** `files` has Vamos settings. Read it with `get_workspace` (`file: "Vamos settings"`) and go to step 7. Competitors they name now go in one ask: "For [brand], track these competitors' accounts alongside the ones I already track: [handles]. Change nothing else." Check `tracking.following` against `cap` first, and price it as one turn. A voice they ask to rebuild is step 3's part 1 alone in the Setup chat, its rebuild sentence included, priced as one turn, then steps 4 to 7 for the voice.
- **Set up elsewhere** (the Vamos app, the sign-in page, an older run): `voice` is true, `tracking.following` is above 0, or `brain` lists pillars. Skip step 2 and keep the voice, Brain and tracked accounts it has; steps 3 to 5 add what's missing (competitors, the Marketing plan, Vamos settings). Say why in one line, at the start and again in the final message: "Vamos already knows your brand, so I'll keep it and add what's missing."
- **Fresh:** none of those. Run every step, with step 2 once.

Before the first billed step, say what's coming against their balance: the workspace's first `set_up_workspace` and the saves are free, and Vamos waives an account's first chat turn ever, so on a new account the research turn is free. Every later run bills: the voice guide message, each voice correction, any follow-up, and `set_up_workspace` or the research turn sent again.

**1. Ask once,** in one short numbered message, before any research. Vamos can't ask questions once it's working, so a guess here becomes a generic voice.
1. Each social account (handle and platform), the website, and who talks on camera for the brand: the founder on their own account, someone on the brand's, or nobody.
2. What they sell and who it's for, in a line.
3. Competitors they already know, and creators they work with.
4. Will they show their face, use their voice, film alone?
5. Do they care about Meta ads? (No means no credits on ads, anywhere in the plugin.)
6. The goal for the next 90 days (reach, leads, sales, a launch), and what a viewer should do after watching.

Leave out what their message or `get_workspace` already answers, and say "skip any you don't know". When nothing's left, or they said go ahead, ask nothing and carry on.

**2. Set up the workspace,** fresh workspaces only. `set_up_workspace` with up to 8 accounts, the website, their line as `about`, the competitors they named as `competitors` and the creators they work with as `track`: named accounts are tracked for free there. It takes about 3 minutes. With no `track`, it also follows up to 6 niche creators.

**3. One research turn,** in the chat setup returned (on a workspace set up before this run, `create_chat` "Setup"), with `include_data: true` and `include_transcripts: true`. Fill in [ ]. Drop part 3's Meta pages when ads are off, and the [fresh only] sentences on a workspace set up before this run, so the voice and tracked accounts it has stay. When nobody talks on camera, parts 1 and 4 and the voice work in steps 4 to 6 follow [references/written-voice.md](references/written-voice.md):
> For [brand], [their line], on [platforms]:
> 1. Read my last 40 videos on [the account they talk on] where I talk, from the last 6 months, leaving out partner posts and reposts. [fresh only: Rebuild my voice guide from how I really talk, quoting my real opening lines, closers and phrases.]
> 2. Give each of those posts as a row: link, date, views, likes, comments, length, format, the hook word for word, and the caption's call to action.
> 3. Find my 4 closest competitors, 4 accounts that sell something else to the same audience, and 2 much bigger accounts in my space [beside the ones I named]. Give each one's handles, website and Meta page, and track them with my own accounts [and the creators I work with], within my plan's limit. [fresh only: Unfollow setup's picks that don't fit.]
> 4. List the first-person facts I've said on camera (numbers, history, people, results, opinions), each word for word with its video link and timestamp.
> 5. From my website and bio: what I sell with prices, the offer people buy first, where they buy, and each way my posts and bio ask people to act (link, comment keyword, discount code, free guide, trial).

When the answer leaves parts out, carry on with what it gave and offer, in the recap, one follow-up turn for the rest. Send it only on their yes.

**4. Your own work, no credits.** Read [references/voice.md](references/voice.md) and [references/brain-files.md](references/brain-files.md), then, working from what the answer and the workspace carry and naming what's missing:
- compute their usual and each post's multiple from their own rows;
- run `python3 scripts/textstats.py profile` on the transcripts (up to 10 come back) for the voice numbers;
- from those transcripts, pick the 5 Voice examples and one held-out video for the test;
- keep each fact from part 4 you can find in a transcript, caption, ad or page you hold, and mark the rest "check with them";
- label each of their posts reach, trust or buy by what it does and asks for, and count each stage's posts and median multiple;
- draft the Brain files: Tracked accounts, Things you've said, What works for me, Marketing plan, Vamos settings.

**5. Save, free.** `save_brain_file` once per drafted file, and once for Voice examples with the five transcripts in full. A file is saved when its `action` comes back; send a failed one once more, and report the rest as not saved. When step 3 rebuilt the voice guide, send "Replace my voice guide with the one you rebuilt above", with what voice.md found missing, in the research chat.

**6. The voice test.** Have a fresh subagent write a 20-second script on the held-out video's idea from the voice guide and the Voice examples only, never that video's transcript, and show it beside their real one (with no subagents, skip the test and say so). Ask: "Which lines aren't you?" Send each answer to Vamos as a voice correction ("I never say X. I'd say Y."). This is the moment they see it work, so keep it short.

**7. The board and the home page.** With no board yet, make one ([references/board.md](references/board.md)), save Vamos settings again with its link, and seed its Lessons tab with each trait from What works for me. Then fill [assets/page.html](assets/page.html) as the `setup` page ([assets/PAGE.md](assets/PAGE.md)):
- what was read: posts, date range, how many had speech;
- the three voice habits you're surest of, each with a real line;
- the tracked accounts, with why each one is there;
- what works for them so far, with its numbers;
- their funnel: what they sell and where people buy, their posts by stage with each stage's median multiple, and the stage that's thin for their goal;
- where to edit each part: the Voice page `https://app.getvamos.ai/brain?view=voice`, the Brain `https://app.getvamos.ai/brain`, tracked accounts `https://app.getvamos.ai/creators`, formats for their niche `https://app.getvamos.ai/formats`, the board, or just tell Claude ("I never say X", "stop tracking @x");
- the skills in run order: find-creators, creator-program, playbook, formats, hooks, ideas, winning-ad-ideas, brief, script, make-video, review-draft, content-log, loop, and analyze any time.

**Check before the recap:** every account they gave appears on the page or is named as not read; every quoted line is theirs, from a transcript, a caption, an ad or their site. Next is `/cracked-marketer:ideas`, the cheapest way to their first posts; with credits to spare, `/cracked-marketer:playbook` on their top competitor.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
