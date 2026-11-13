---
name: "post"
description: "Posts your finished videos to your own accounts through your own Zernio: many accounts, many a day, at the times you pick, and while you're away, after one yes for the batch. Shows the batch as one table first (account, time, file, caption, AI label, disclosure), checks every post with Zernio before it goes, switches on each platform's AI label for AI footage and never posts an AI likeness of a real person. Use for \"post these\", \"schedule this week's videos\", \"post to all my accounts\", \"post 3 a day\", \"let Claude post for me\", \"run my Instagram\", \"what's scheduled\", or to move or cancel a scheduled post."
---

# Post

**The job:** the videos the user approves go out on their own accounts at the times they pick, with each platform's AI label and the disclosure line where they belong, after one yes to one table. It runs on the user's own Zernio, which posts at the set times with their laptop closed. Vamos never sees their Zernio sign-in or their accounts' tokens. The videos are their own edits of `/vamos:script`'s scripts.

The Zernio calls, the upload and the hand-off: [references/zernio.md](references/zernio.md).

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas need it, and so do hooks and scripts while its `voice` is false, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** One Vamos chat per job (`create_chat`); follow-ups go in it. Add `include_data: true` when you need the rows. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50 posts (30 ads, creators or formats), so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file`, always as its whole text, so read one first to add to it. Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 7 days old (views still climb before that), leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). A younger post that already beats it shows as "N× so far"; one that doesn't is too early to judge. Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer:

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/vamos:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**1. The posting tool.** Look for Zernio's tools (`accounts_list`, `validate_post`, `call_tool`; their prefix depends on the host). With none, say in one line what to connect ([zernio.md](references/zernio.md), Connect), then give the batch as the hand-off table, its captions and labels from plan.py run on the accounts they name, and post nothing. Another scheduler gets the same table: this skill sets the AI label only through fields checked live on Zernio.

**2. The accounts and times.** Read Vamos settings' Posting line (`get_workspace` with `file`, free). The first time, `accounts_list`, then ask once, in one message: which accounts post which videos, how many a day each, at what times, in which time zone. Save the answer as that Posting line, with `save_brain_file` and the file's whole text:
> Posting: Zernio. @brand (instagram, tiktok) and @brand.two (instagram): 09:00, 13:00, 19:00 (Europe/Madrid). Ready to post goes out by itself: no.

The last part stays "no" until the user says their yes covers every video they mark Ready to post (step 7).

**3. The batch.** Each finished file with its post sheet: `<file>.post.json` beside it, written by make-video, or the board's rows at Ready to post with their file ([references/board.md](references/board.md)). A file with no sheet gets one from the user, in one message for the whole batch: its caption, whether it holds AI-made footage, an AI face or an AI voice, and whose face is in it. Never guess those two answers: they decide the label. For the batch's `existing`, read what's on those accounts with `posts_list` and `limit: 100`, once with status scheduled and once with status published (keep the last 24 hours), each with its account, time and file (`metadata.vamos_file`).

**4. Plan in code.** Write `batch.json` and run `python3 scripts/plan.py batch.json` ([zernio.md](references/zernio.md), The batch file). It fills each account's next free times, holds every rule below and prints the table. Fix every DEFECT before anything goes to Zernio. The rules:
- an AI label on every post that holds AI footage, faces or voice, set in the platform's own field; where the API has none (Facebook, Threads, LinkedIn), that row is posted by hand with the label on;
- the disclosure line in the caption ("Made with AI." when the sheet gives none), and #ad on a paid partnership;
- nothing posts an AI version of a real person who hasn't agreed; the user's own AI twin, or someone's with their written yes, posts with the label;
- each account stays under its platform's posts in 24 hours (TikTok 15, Facebook 30, Instagram 100; the caps are in plan.py, read 2026-11-13);
- the same video twice on one account within 24 hours is refused, counting what's already on Zernio, and the same video on two accounts of one platform is flagged, since the platforms keep reposts from new viewers.

**5. Upload and check each post.** Upload each file to their Zernio, run plan.py again with `--urls`, then `validate_post` on every row's `validate`, and the TikTok rows' `dry_run`. Nothing is published by either. A row that fails is fixed and checked again, or dropped and said so.

**6. The yes.** Show the table as plan.py printed it, its FLAG lines, and one line:
> Yes posts these 12 at these times on your Zernio, labels and captions as shown. TikTok asks that you've watched each video and agree to post it: your yes is that. Nothing goes out without it.

When the batch has X rows, add what plan.py's BATCH line says X bills, from their Zernio balance.

Wait for it. A yes covers that table only: a row changed after it ("move 3 to 18:00") is shown again and needs its own yes.

**7. Send and record.** On the yes, run plan.py once more on the same batch (re-read `existing` first). A row whose time moved, because its slot passed while the table waited, is shown again for a new yes: Zernio publishes a past time the moment it's sent. Then send each row's `create` as it is: `call_tool` with its `name` and `arguments`, one row a call. Never the short `posts_create`: it can't carry the AI label. Keep each returned post id in `vamos/posted.json` and on the board's row (Status Scheduled, its Post column: account, time and id). Zernio publishes each at its time, laptop closed. Say "now" only when the user asked for now.

**While they're away.** Once the user says their yes covers every video they mark Ready to post, write "Ready to post goes out by itself: yes" on the Posting line. Then each `/vamos:loop` ideas run plans those rows, from each row's File, into the next free times and sends them with every rule above, `"tiktok_drafts": true` in batch.json: nobody saw that table, so TikTok gets each video in the account's TikTok inbox, and the user adds the caption and taps Post there (up to 5 waiting a day). A row with a DEFECT, a FLAG, a file this run can't open, or by hand waits for them in the digest. Until then the loop's digest shows the batch's table and waits. The run reads the files where they are, so it runs on the computer that holds them; what it has scheduled goes out with that computer off.

**Move, cancel, check.** "Move 3 to 18:00": `posts_update` with the new time. "Cancel 3": `posts_delete` (a published post can't be deleted). "What's scheduled": `posts_list` with `limit: 100` as a table. A published post sets its board row to Posted with its link, for `/vamos:content-log` at 2 and 7 days.

**Check before the recap:** nothing was created before the yes to its table; every created row went out with plan.py's arguments unchanged; every AI row has its label on or is listed by hand; the recap counts what's scheduled, what's by hand and what was dropped.

> **Made:** 12 posts scheduled on your Zernio, Sat 09:00 to Mon 19:00, 1 by hand on Facebook · **Credits:** 0 used, [left] left · **Next:** `/vamos:content-log`, each post's numbers at 2 and 7 days

Vamos is needed for the Posting line and the board; with neither, the batch is the files the user names and the Posting answer stays in this chat.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Vamos plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
