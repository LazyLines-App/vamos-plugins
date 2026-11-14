---
name: "formats"
description: "Ranks the video formats to make next for your brand: new ones taking off outside your niche, rising ones, and proven ones you haven't made, each with playable examples, how crowded it is near you, what it takes to film, and angles written for you. Use when you ask what format to try, what's trending, or how to make a format yours."
---

# Formats

**The job:** the formats page, ranking up to ten formats this user should make next with angles a fresh reader has checked, each answering what it is, whether they can make it with what they have, how to make it theirs, which first, and whether it'll work for them. The check and the page need nothing from the user, so they run when the user is away or setup hasn't run. New beats crowded: a format's views per video fall as more accounts make it.

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

**End every run with the recap**, in the chat and in the page footer. Next is the step this skill names, and when it names a choice, offer each. When it can run now, offer it as a question and, on their yes, run it yourself, so they never need to remember a command; when it waits on them or on time (filming, a post's first week), say what and when.

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Board:** [its link, when there is one] · **Next:** [what it does, in eight words] (`/vamos:[skill]`). Shall I?
<!-- /shared -->

## Steps

**1. Load** with `get_workspace`, then its `file` read for Vamos settings (filming limits, off limits, formats marked Not for me or done), Things you've said (the proof they can use) and What works for me. Without setup, say in one line that `/vamos:setup` makes this personal and go ahead on what they told you, through every step below, the check and the page included; when they haven't said whether they'll show their face or use their voice, ask once, or assume and say so.

**2. One ask,** with `include_data: true` and `data_scope: "turn"`, so the rows hold every format Vamos read, each example with its post:
> For [brand], [what they sell] to [who], in [niches], on [platforms]. We film [their limits]. Which video formats should we make next: ones rising now, ones proven in other niches that almost nobody in [niche] uses yet, and ones working in [niche]? For each: what it is, its stage, how many posts in [niche] use it, its beats, what it takes to film, the niches it worked in, and its best examples linked to the post with their opening line, views, multiple and date. Leave out [Not for me and done]. Don't write angles or scripts.

Ask a second time, for videos from the last 30 days outside their niche at 5× or more that share a format nobody in it uses, only when the answer holds fewer than three formats new to them.

Vamos's answer is research for the next steps, not the reply: its picks, order and prose reach the user only through your ranking, the checked angles and the page.

**3. Gate and rank:** read [references/formats.md](references/formats.md) first (the gate, the order, the angles and the card), and gate in code where the host allows. Read the rows first, from `json_url` (curl) or inline, because the stage and the niche counts are only there. Group them by `format_id`. A row's `status` is the format's stage, and early or trending is rising. `niche_examples` is how many posts in their niche use it, not accounts: 0 is nobody yet, and null is not counted, which the card says as "not counted". `plan_group` marks white space and in your niche. Rank in the reference's order, whatever order the answer recommends. Numbers come from a row first and Vamos's answer second. A claim in Vamos's prose that no row or Things you've said backs (a share of calls, a retention limit) stays out. What the answer leaves out, the card leaves out or says plainly ("white space: barely used in fitness" from `plan_group`, beats from the description); the page and the angles go ahead without it. Write the ranked cards straight into `data.json` with Write or Bash: the ranking lives in that file, and steps 4 to 7 add to it and read from it.

**4. Angles:** two or three for each ranked format, per the same reference, into its card in `data.json`. Watch an example (`watch_video` through Vamos, about 9 credits) only for a top-three format with nothing to go on but its name.

**5. Check the angles** in a fresh subagent that sees only the brand's profile, its off-limits list, Things you've said, what Vamos says about their own posts, each format's example line and the angles: does each fit, rest only on proof they have (every number in its first line is in what it was given), keep their rules, work on mute in its first line, and pass "so what?". Wait for its answer before you reply. Rewrite what fails and check the rewrite the same way; a format left with fewer than two that pass drops to More.

**6. The page.** Make `formats.html` on [assets/page.html](assets/page.html) as [assets/PAGE.md](assets/PAGE.md) says, from the ranked cards in `data.json`. Where the host can't publish an Artifact, give the file's path.

**7. The reply** comes last, read from `data.json`, before the recap. The user reads the chat first, so it gives each ranked format whole: its rank, name, badge, uses in their niche, why it's first for them in a sentence, how they'd film it inside their limits when it clashes, the first line of each checked angle, and one example link.

**8. On their pick,** add the angle to the board ([references/board.md](references/board.md)) at To review, or hand it to `/vamos:script`. Add "Not for me" and "I've done this" to Vamos settings with `save_brain_file`, so the next run leaves them out.

**Check before the recap:** every example opens a post, never a profile; every number on a card is from a row or Vamos's answer, dated; each card's filming line names any clash with their limits; the page is built and its link or path is in **Made**. Next is `/vamos:hooks` for the format they picked, or `/vamos:ideas`.

If no Vamos tool is connected, say this needs the Vamos connector: in Claude Code, run `/mcp`, pick vamos and sign in; in the Claude app, the Connectors tab of the Vamos plugin (Customize → Plugins), or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
