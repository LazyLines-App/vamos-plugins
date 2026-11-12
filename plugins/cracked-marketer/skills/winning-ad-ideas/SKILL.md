---
name: "winning-ad-ideas"
description: "Writes 10 Meta ad concepts for your brand, each remade from an ad that has kept running 30+ days, a competitor's, your category's or a brand that sells to your buyer, in the same format, each a different picture; three blind judges keep the strong ones, which go on your board with a code your content log tracks. Also what each launched this week. Use for \"ad ideas\", \"what ads should we run\" or \"make this week\", \"remake my competitors' best ads\" or \"/ads mysite.com\". One brand's whole teardown, its ads included, is playbook."
---

# Winning ad ideas

**The job:** ad concepts for the user's brand, each one an ad that's still running in their market, remade for them. Long-running is the only public sign an ad is worth copying: someone keeps paying for it. So every concept names its source ad and how long it has run, keeps that ad's format (a static stays a static, a video stays a video), takes its device and sentence shape, and puts the user's own product, words and claims in it. Ten concepts, ten different pictures, because Meta groups ads that look alike.

Worked concepts are in [references/concepts.md](references/concepts.md).

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

**1. The brand and the market.** Read `get_workspace` (free) for the brand, niche and tracked competitors, and with `file`, free, What works for me and the newest "Playbook: [their brand]", then the board's Reviews rows (their Ad week) and its ad concepts (rows whose Idea starts `WA-`) with their statuses: the judges' evidence in step 5. From the message take the site, the product, the market (the US unless they sell elsewhere) and the competitors they name. Name 3 to 5 neighbours yourself: brands that sell to the same buyer and aren't competitors (for a dog food brand, a collar, a supplement, a treat box). Without setup or any of these files, go ahead: a judge with no evidence sits out. Ask only when you can't tell what they sell. A store link reads as plain text in Vamos, so put the app's category in words.

**2. One research turn,** with `include_data: true`, `data_scope: "turn"` and `data_format: "inline"`. Say first that it is one Vamos turn, up to 60 credits. Send it as the user's request:

"Find the Meta ads still running in [category] in [market]: [competitor (site)], [competitor (site)] and the category's other advertisers, and these brands that sell to the same buyer: [neighbour], [neighbour], [neighbour]. I want the ones that have run 30 days or more, longest first, and, apart from them, the ads each of these launched in the last 7 days, up to 5 a brand. For each: the advertiser, days running, how many copies run, the format (static, video or carousel), what the image or the opening shot shows, the words on it and the first line said. Say how many ads you read of how many each brand runs, and which are catalog or product-feed ads. Brand: [brand, site]. Niche: [niche]."

A second turn only fills a gap you can name (fewer than 10 sources, so widen to the category), and you say so first.

**3. Pick the sources.** Rank by days running, then copies (×N), then how many advertisers run the same angle. One concept per source; copies of one ad, its other-market versions, ads whose headline and body match word for word, and ads the answer shows with the same person or thing in the same setting (one presenter's videos on one set) count once, as the longest runner, because remade for the user they'd be one picture. List the rest as repeat pictures. An unread picture alone never makes an ad a repeat: it keeps its rank when its words are in the rows or the answer. Set aside, and list them at the end:
- catalog and product-feed ads (a retailer's or a shop's feed), because their days measure stocking, not a concept;
- a page whose landing site isn't the brand's;
- an ad with neither its picture nor its words read: there's nothing to remake;
- ads under 30 days, which are new. Use one only when fewer than 10 sources have run 30 days, and label it with its days.

A neighbour's ad is a source like a competitor's. Ads launched in the last 7 days are never sources, even when fewer than 10 have run 30 days: they're what each brand is testing now, listed in the hand-over. Fewer than 10 sources gives fewer than 10 concepts, with the reason. Organic posts aren't sources: this is ads from ads.

**4. Write each concept** in the shape of the examples:
- **From:** the advertiser, the Ad Library link from the rows or the answer, days running, ×copies when they're given, the format the answer states (static, video or carousel), else "format not stated": a row's DCO is dynamic creative, and "creator ad" or "partnership" is who made it, so neither is a format.
- **The picture:** what the viewer sees first: the source's shot or layout, with the user's product or a real thing they have in it. When Vamos couldn't read it, build it from the ad's words and say so.
- **The line:** the source's sentence shape and length in the user's words. Set the two side by side: past the small words (a, the, no, you), they share none, so the catchphrase and labels are new too. A static gets the image words, as many as the source has, plus the headline field; a video gets the first line said and shown, then three beats.
- **Every fact about their product** in the line or the beats (what's in it, what it does, who uses it, its results or look, its price or offer) is one the user gave or the answer states about their brand; where you have none, it's a slot: `[your hero ingredient]`, `[your result]`. That holds where the source's line names one and where you write the line yourself. Never the competitor's line, numbers, celebrity or creator. A face that isn't a real customer presents; it never plays one.

Then name each picture as the user will shoot it, in about five words: the source's who or what, played by theirs, and where ("your pharmacist at the counter", "your tub on a gym bench"), and put the names at the top of the concepts as a numbered list. Two names that share both look alike in the feed, so they're one concept: put one back in its own source's setting, or set the shorter runner aside as a repeat picture. Every picture stays its own source's shot, because the shot is part of what kept running.

**5. Three blind judges.** Three fresh subagents, sent in one message so none sees another's verdict, each given the concepts, numbered, and only its own evidence:
- **The track record:** What works for me, the Reviews rows' Ad week (spend, CPA, the concept codes that ran) and the board's earlier concepts with their status. "Would this account's own history back each concept? Keep or kill, 1 to 5, and the result in their numbers that decides it. One their history has never tried is new to them, not disproved: keep it at 3."
- **The customer:** the customer groups in "Playbook: [their brand]", each with its count and lines. "Is each concept about something these customers actually say, in words they'd use? Keep or kill, 1 to 5, and the line that decides it."
- **The assassin:** the concepts and the brand's site alone. "Find the reason each one fails: unclear by the second line, a claim the site can't back, a competitor's ad with the logo swapped, a picture nobody stops for. Keep or kill, 1 to 5, and the reason."

A judge with no evidence yet sits out, and the hand-over says which and why. A concept is kept when most judges who sat keep it (2 of 3, or 2 of 2); the rest go under Skip with the deciding judge's line. A judge sitting alone kills nothing, since its source's days running are evidence too: every concept stays, with its score and its line as the fix to make before filming. Without subagents, judge in turn yourself, each from only its evidence, and say so. With no customer groups saved, offer `/cracked-marketer:playbook` on their own customers (about 30 to 50 credits), so the next run's customer judge sits.

**6. The board.** Every kept concept gets a code, `WA-[MMDD]-[n]` (today's date, numbered on from the day's highest code on the board), board or not. Each goes on the board Vamos settings names at To review, its Idea starting with its code, Format "Meta ad: static" (or video, carousel), Source its ad's link and days, and the line "put the code in the ad's name": the next content log finds it in their Ads Manager export. With no board, the reply holds them, codes included.

**7. Hand it over.** Open on what Vamos read, in one line, with only the counts its answer or rows state, and say so when it gave none or no rows came back: "Vamos read 40 ads from 6 guitar-lesson apps on 2 Nov; 18 have run 30+ days.", or with no total: "Vamos picked the guitar-lesson ads running 90+ days on 2 Nov and gave no total read." Then the kept concepts in their sources' order, longest-running first whatever their scores, each with its code and its judges' scores and lines; then Skip; then what was set aside and why; then what each brand launched this week, one line each with its link. Say once: long-running means someone keeps paying, not proof it sells, since nobody outside sees spend; stopped ads outside the EU and UK are not visible, never zero. Ask which to make: `/cracked-marketer:brief` for a creator to film, or `/cracked-marketer:make-video`. Nothing here posts, runs or buys an ad or contacts a creator.

**Check before the recap:** every link is one Vamos returned; every count, day count and ×copies matches the rows or the answer; each concept keeps its source's format; every fact a concept states about their product is the user's, the answer's, or a slot; no two pictures match; 10 concepts were written, or the reason fewer were; each judge saw only its own evidence; every kept concept has its code, and is on the board only when the board confirmed it.

If no Vamos tool is connected, say this needs the Vamos connector: the Connectors tab of the Cracked marketer plugin, or https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Vamos&connectorUrl=https%3A%2F%2Fmcp.getvamos.ai%2Fmcp
