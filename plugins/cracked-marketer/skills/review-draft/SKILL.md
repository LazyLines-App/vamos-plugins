---
name: "review-draft"
description: "Checks a UGC creator's draft video against the brief they filmed from, before you send notes: pass or fix, each fix a timestamped note to paste to them, and the brief's approve-when line ticked item by item (the hook word for word, the product on screen by 3 s, the ★ line as written, the disclosure). Tags your own notes as in the brief or a new ask, and counts the revision rounds. Use for \"check this draft\", \"does her video match the brief\", \"what notes do I send my creator\", or a draft that's late."
---

# Review a draft

**The job:** notes the user can paste to the creator today, judged only against the brief they filmed from. The brief is the contract: anything it doesn't ask for is a new ask, and the user decides whether to send it. [references/review.md](references/review.md) holds the review and a finished example.

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

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/cracked-marketer:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**1. The brief, free.** Find the brief this video was filmed from (there's one per video) where the brief skill keeps them: the Google Doc or Notion page "Briefs", `vamos/briefs.md`, or the Brain file "Briefs" (`get_workspace` with `file`), or the brief they paste. With no brief, ask for it in one line and stop: a review against no brief is taste, and every note would be a new ask. Read "Creator program: [brand]" the same free way for the rounds of notes agreed (one when it doesn't say), and the Marketing plan for the product's facts, so a note that adds a claim is checked against it. Count the draft reviews already under that brief. This skill spends no credits: Vamos reads public posts, not draft files.

**2. Read the draft** the way the host allows, and say what that covers:
- **With a shell** (Claude Code, Cowork): `python3 scripts/draft.py <video> --out draft/`. It saves the frames as sheets stamped with their times (every 0.5 s to 3 s, then every 2 s) and a transcript with times from their captions file (beside the video, or `--captions`), else whisper.cpp on this machine. Look at every sheet. With no transcript it prints the free local install: offer it, and meanwhile read the words off the captions burned into the sheets and say so.
- **Without a shell** (claude.ai): a video file can't be opened here. Ask once for the transcript or captions with times (CapCut exports them as SRT), screenshots of the first frame and the frame at 3 s, and the caption they'll post. Review what those show and list the rest as not checked.
- A link to a private draft (Drive, Dropbox, an unposted TikTok) can't be opened by any host: ask for the file.

**3. Check it:** `python3 scripts/check_draft.py <briefs file> --creator <name> --transcript draft/transcript.srt --probe draft/probe.json --caption "<their caption>"`, with the briefs doc saved as a markdown file first when it's a Google Doc, Notion page or Brain file. With several briefs for that creator it checks the one that fits what was said and lists the rest; add `--brief "<words from its title>"` when the user names the video. It takes the must-haves from the brief itself (the hooks, the ★ line, part 7's "Fixed:" and "We approve it when …") and ticks the word ones word for word, with what differs. EAR is a one-word slip a transcriber could have made, often a brand name: check that moment against the burned-in captions before calling it. LOOK lines are yours to judge from the sheets and the words: the hook on screen from the first frame, the product by 3 s, anything else the approve line names, and part 6's don'ts. Without a shell, set each line said beside the brief's words yourself.

**4. Write the review** in the order of [references/review.md](references/review.md):
- **Pass or fix**, by the must-haves only. One this host couldn't check is "to confirm", with what would settle it: the screenshot or file to send.
- **The approve-when list**, each item ✓, ✗ or to confirm, with its evidence: the words said beside the brief's, the frame where the product first shows.
- **Notes to send**, one per ✗, blockers first: the timestamp as minutes:seconds (3 s is 0:03), what to change and to what (the exact words for a line), one or two sentences, kind and specific, opening on one thing that works. Other parts of the brief they missed come after, as suggestions.
- **The user's own notes**, each tagged "in the brief" (name the part) or "new ask". A new ask stays out of the notes to send unless the user keeps it; past the agreed rounds it's theirs to agree with the creator, and may be paid.
- **Round** n of the agreed number.

No draft by the due date: write a two-line nudge naming the video and the date, for the user to send.

**5. Record it, without asking,** under that creator's brief in the briefs doc as `### Draft review · round n · [date] · Pass|Fix`, with the list and the notes, items to confirm included, so the next round counts from it. In the Brain file "Briefs", that's the whole doc saved back with `save_brain_file`. The user sends the notes; nothing goes to the creator from here.

**Check before the recap:** every ✗ has a note with its timestamp (or its line, when the transcript has no times); no note to send asks for something the brief doesn't, unless the user kept it; every word tick came from `check_draft.py` or a side-by-side you showed. Next is `/cracked-marketer:content-log` once it's posted: it checks the live post's disclosure and reads its views against the creator's usual.

Vamos is needed only for a brief or program kept in the Brain; a brief in a file or pasted is reviewed without it.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
