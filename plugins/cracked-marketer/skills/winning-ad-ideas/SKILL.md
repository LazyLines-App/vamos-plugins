---
name: "winning-ad-ideas"
description: "Writes 10 Meta ad concepts for your brand, each remade from a competitor's or your category's ad that has kept running 30+ days, in the same format, each a different picture. Use for \"ad ideas\", \"what ads should we run\", \"remake my competitors' best ads\" or \"/ads mysite.com\". One brand's whole teardown, its ads included, is playbook."
---

# Winning ad ideas

**The job:** ad concepts for the user's brand, each one an ad that's still running in their market, remade for them. Long-running is the only public sign an ad is worth copying: someone keeps paying for it. So every concept names its source ad and how long it has run, keeps that ad's format (a static stays a static, a video stays a video), takes its device and sentence shape, and puts the user's own product, words and claims in it. Ten concepts, ten different pictures, because Meta groups ads that look alike.

Worked concepts are in [references/concepts.md](references/concepts.md).

<!-- shared: working-with-vamos -->
## Working with Vamos

- **Setup first.** `get_workspace` (free) tells you whether setup has run: no Vamos settings in its `files` means it hasn't. Ideas, hooks and scripts need it, because they're written in the user's voice: say so in one line, then start the setup skill yourself (never ask them to type a command) and carry on with their ask. Every other skill suggests it in one line and goes ahead if they'd rather not.
- **Asks.** Open a Vamos chat with `create_chat` once per job, send each ask with `chat_completion_start`, and call `chat_completion_poll` until it's done. Follow-ups go in the same chat. Add `include_data: true` when you need the rows (with `include_transcripts: true` for up to 10 transcripts, and `data_format: "inline"` when you can't fetch a link). The rows are the posts the answer links; add `data_scope: "turn"` for every post the research read. The file link holds up to 200 rows, so one ask covers every platform; inline stops at 50, so ask per platform only when you read inline. Say "read N of M" when you get fewer. When a poll's answer is saved to a file, read it in parts (jq, or Read with an offset) and don't ask again.
- **Name the brand, niche and platforms in every ask**, because the workspace may be about another brand.
- **One-off wording.** Say "the last 7 days", "each" or "all". Vamos saves a recurring routine when an ask says every, daily, weekly or schedule, so keep those words for when the user asks for a Vamos routine.
- **Saves.** Write a Brain file or skill with `save_brain_file` (free; `when_to_use` makes it a skill), always as its whole text, so read one first to add to it. The voice guide, content plan and profile notes change only in a Vamos chat, each as its own `chat_completion_start` message ("Save this as …"). Report a save only when its `action` comes back or Vamos's answer confirms it.
- **Credits.** `get_credit_usage` and `get_messages` are free. Before a step that spends, say what it will do and roughly what it costs against their balance. Credits used is the poll's `creditsCharged`, and what's left is `get_credit_usage`'s balance, read before the recap; when you couldn't read one, say so.
- **Numbers.** Every number you show comes from Vamos (a row or its answer) or your own code, with the date it was read. For the user's own posts and for a playbook or analyze target, compute "usual" yourself: the median views of posts at least 3 days old, leaving out boosted posts (likes under 0.5% of views, or tagged paid) and reposts (the same caption as an earlier post, within 2 s of its length). Elsewhere use Vamos's multiple and say so.
- **Fresh reads.** A cold read is a fresh subagent that sees only the text. Where the host has no subagents, skip it and say so on the page.

**Where things live.** The user's state is in Vamos, where every host and every Vamos chat can read it and the user can edit it at `https://app.getvamos.ai/brain`: the profile, pillars and Voice page; the Brain files Tracked accounts, Voice examples, Things you've said, What works for me, Marketing plan, Vamos settings, and one dated "Playbook: [brand]" per brand taken apart; and a Brain skill per structure, each named "Structure: [name]". The board (Notion, a Google Sheet, `vamos/board.md` or a Brain file, as Vamos settings says) holds the ideas, hooks, lessons and reviews. To read a Brain file or skill (the voice guide is a file, a structure is a skill), call `get_workspace` with `file` set to its title, without the summary `files` or `skills` shows after it: free, and the full text. When Vamos answers that no file has that name, its error lists the exact names: retry once with the right one. Never spend a turn reading one.

**End every run with the recap**, in the chat and in the page footer:

> **Made:** [what, with its link] · **Credits:** [used], [left] left · **Next:** `/cracked-marketer:[skill]`, [what it does, in eight words]
<!-- /shared -->

## Steps

**1. The brand and the market.** Read `get_workspace` (free) for the brand, niche and tracked competitors. From the message take the site, the product, the market (the US unless they sell elsewhere) and the competitors they name. Ask only when you can't tell what they sell. A store link reads as plain text in Vamos, so put the app's category in words.

**2. One research turn,** with `include_data: true`, `data_scope: "turn"` and `data_format: "inline"`. Say first that it is one Vamos turn, up to 60 credits. Send it as the user's request:

"Find the Meta ads still running in [category] in [market]: [competitor (site)], [competitor (site)] and the category's other advertisers. I want the ones that have run 30 days or more, longest first. For each: the advertiser, days running, how many copies run, the format (static, video or carousel), what the image or the opening shot shows, the words on it and the first line said. Say how many ads you read of how many each brand runs, and which are catalog or product-feed ads. Brand: [brand, site]. Niche: [niche]."

A second turn only fills a gap you can name (fewer than 10 sources, so widen to the category), and you say so first.

**3. Pick the sources.** Rank by days running, then copies (×N), then how many advertisers run the same angle. One concept per source; copies of one ad, its other-market versions, ads whose headline and body match word for word, and ads the answer shows with the same person or thing in the same setting (one presenter's videos on one set) count once, as the longest runner, because remade for the user they'd be one picture. List the rest as repeat pictures. An unread picture alone never makes an ad a repeat: it keeps its rank when its words are in the rows or the answer. Set aside, and list them at the end:
- catalog and product-feed ads (a retailer's or a shop's feed), because their days measure stocking, not a concept;
- a page whose landing site isn't the brand's;
- an ad with neither its picture nor its words read: there's nothing to remake;
- ads under 30 days, which are new. Use one only when fewer than 10 sources have run 30 days, and label it with its days.

Fewer than 10 sources gives fewer than 10 concepts, with the reason. Organic posts aren't sources: this is ads from ads.

**4. Write each concept** in the shape of the examples:
- **From:** the advertiser, the Ad Library link from the rows or the answer, days running, ×copies when they're given, the format the answer states (static, video or carousel), else "format not stated": a row's DCO is dynamic creative, and "creator ad" or "partnership" is who made it, so neither is a format.
- **The picture:** what the viewer sees first: the source's shot or layout, with the user's product or a real thing they have in it. When Vamos couldn't read it, build it from the ad's words and say so.
- **The line:** the source's sentence shape and length in the user's words. Set the two side by side: past the small words (a, the, no, you), they share none, so the catchphrase and labels are new too. A static gets the image words, as many as the source has, plus the headline field; a video gets the first line said and shown, then three beats.
- **Every fact about their product** in the line or the beats (what's in it, what it does, who uses it, its results or look, its price or offer) is one the user gave or the answer states about their brand; where you have none, it's a slot: `[your hero ingredient]`, `[your result]`. That holds where the source's line names one and where you write the line yourself. Never the competitor's line, numbers, celebrity or creator. A face that isn't a real customer presents; it never plays one.

Then name each picture as the user will shoot it, in about five words, who or what of theirs and where ("your founder at the counter", "your tub on a gym bench"), and put the names at the top of the concepts as a numbered list. Two names that share both look alike in the feed, so they're one concept: put one back in its own source's setting, or set the shorter runner aside as a repeat picture. Every picture stays its own source's shot, because the shot is part of what kept running.

**5. Hand it over.** Open on what Vamos read, in one line, with only the counts its answer or rows state, and say so when it gave none or no rows came back: "Vamos read 40 ads from 6 guitar-lesson apps on 2 Nov; 18 have run 30+ days.", or with no total: "Vamos picked the guitar-lesson ads running 90+ days on 2 Nov and gave no total read." Then the concepts, longest-running source first, then what was set aside and why. Say once: long-running means someone keeps paying, not proof it sells, since nobody outside sees spend; stopped ads outside the EU and UK are not visible, never zero. Ask which to make: `/cracked-marketer:brief` for a creator to film, or `/cracked-marketer:make-video`. Nothing here posts, runs or buys an ad or contacts a creator.

**Check before the recap:** every link is one Vamos returned; every count, day count and ×copies matches the rows or the answer; each concept keeps its source's format; every fact a concept states about their product is the user's, the answer's, or a slot; no two pictures match; the count is 10 or the reason it isn't.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
