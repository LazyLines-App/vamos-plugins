---
name: "loop"
description: "Runs your content system on a schedule, even with your laptop closed: ideas on the days you pick, scripts for the ones you approve, a weekly content log with your paid creators' results, stopping where you want to say yes. Use when an ask says every Monday, every week or while I sleep: to automate your content, run a creator program's week by itself, keep research running, check that a scheduled run worked, or change, pause or stop the schedule."
---

# Loop

**The job:** ideas, scripts and the content log run by themselves and stop only where the user wants to decide. Each run reads the board first, so a status they set there (Approved) is what the next run acts on. Its runs write ideas and scripts, so it needs setup the way they do.

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

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/vamos:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Set it up

**1. Ask once,** in one message, and take the steps below after they answer:
> Where should it stop for you?
> 1. After ideas (default): new ideas wait on the board; scripts are written only for the ones you approve.
> 2. After ideas and after scripts: each script waits for your OK too.
> 3. Run everything and show me: it picks the best ideas by your lessons and writes their scripts. Nothing is posted, sent or paid for.
>
> Which days for ideas (default Monday and Thursday), and which day for the content log (default Monday)?

With a "Creator program: [brand]" in the Brain and the brief skill in this plugin, add that the content log's day is also the creators' week ([references/creators.md](references/creators.md)): their results, each one's next brief, and the code asks, chases and payout list, all drafted for them to send.

**2. Price it** from `get_credit_usage`: an ideas run is about 50 credits, a content log about 15 (about 20 with creators, plus up to 45 for their briefs' research turn: 42 for three creators on 2026-11-12); saves are free. Say the week's total against what's left (Free's 200 don't renew). When it doesn't fit, offer fewer ideas days and set nothing up until they choose.

**3. Move a local board** off the laptop: to Notion or a Google Sheet when the host has one, else with `save_brain_file` as the Brain file Vamos board, the board word for word.

**4. Save the settings** with `save_brain_file` as Vamos settings: its whole text, with its Approval, Loop and Board lines replaced by these (when you don't know their time zone, drop the brackets rather than describe it):
> Approval: Ask me after ideas. Loop: ideas Monday and Thursday 08:00, content log Monday 10:00 ([their time zone]). Board: [link].

**5. Schedule one task per job,** an hour or more apart, on a scheduler that loads this plugin:
- **Cowork** (Claude desktop app: Scheduled, New task) runs with the laptop closed and loads the plugins on their claude.ai account, so first add this plugin in Customize → Plugins and connect Vamos there.
- **The Claude Code desktop app** (Code: Scheduled, New task, Only on this computer) loads this laptop's plugins, but runs only while the app is open and the laptop awake; a run it sleeps through runs once on wake.
- **A Claude Code cloud task** (`/schedule`) runs with the laptop closed but loads no plugins: only the claude.ai connectors it includes and the skills committed to its repository. It works once every skill folder beside this one is in that repository's `.claude/skills/` (offer to copy and commit them, again after each plugin update; ask before pushing) and Vamos is added at claude.ai connectors. Its prompt then starts "Use the loop skill:" in place of the command.

`/loop` stops when the session closes. When you can't create the task here, give them each task's days, time and prompt to paste:
> /vamos:loop run ideas for [brand] ([@handle] on [platforms], [niche]). Board: [link]. Settings: the Vamos settings Brain file. Approval: [setting].

The content log's task says `run content-log`. With no scheduler, they run `/vamos:loop run ideas` by hand, and Vamos's free Weekly brief (Settings → Weekly brief) emails them what's new. Make a Vamos Routine only when they ask: each run spends credits, and one made from here is saved switched off until they turn it on in Vamos.

**6. Check the first run.** Ask them to press Run now on each task (about 50 credits for ideas, 15 for the content log) and answer every Vamos and board tool prompt with always allow: a scheduled run that stops on a permission prompt never finishes. Succeeded only means the session ended (a task that couldn't load the loop still shows it), so the proof is the board: new rows from that run (ideas at To review, or the content log's lessons) and its digest. When they come back, read the board yourself and say which it is; no new row means the task didn't load the loop or Vamos, so name the scheduler from step 5 to move to.

## Each run: `/vamos:loop run [job]`

A fresh session knows only Vamos settings (`get_workspace` with `file`, free) and the board. Nobody is there to answer, so where a skill would ask, take its default and say so in the digest.

- **ideas:** `/vamos:script` for the rows they set to Approved, then `/vamos:ideas`, whose new ideas wait at To review. On "run everything", run `/vamos:ideas` first, mark the two or three best by What works for me as Picked (the only status a run sets), then `/vamos:script` for the Picked rows.
- **content-log:** `/vamos:content-log` on public numbers. First check the Brain for a "Creator program: [brand]" (`get_workspace`, free): when there is one and this plugin has the brief skill, read [references/creators.md](references/creators.md) before anything else and run all four of its steps, so content-log is its first step and the digest is the one there.

Anything that spends outside Vamos credits, posts, emails, pays or messages someone waits for their yes. A run that finds nothing new says so in one line and spends nothing more.

**End with the digest**, as the recap:
> **Waiting for you:** 3 new ideas at To review, 1 script at Script ready · **Credits:** 51 used, 132 left · **Board:** [link] · **Next:** Thursday 08:00. Approve on the board, or reply "approve 1, 3".

To change, pause or stop it, edit or delete the scheduled tasks and update Vamos settings.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
