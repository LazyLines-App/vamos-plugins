# Cracked marketer by Vamos

The marketing hire a brand or startup would make, in Claude. It researches what's working on TikTok, Instagram and YouTube, plans and writes your content, logs what works and runs it all on a loop. It finds your creators, plans what to pay them, writes their briefs, checks their drafts and makes the videos. Ad ideas from the ads that keep running come next.

It includes everything in the Vamos plugin (Content System), so you never need both. Content System is for creators, coaches and service providers who film their own content. Cracked marketer is for a brand or startup that needs the whole marketing job done.

## Skills, in the order you'd run them

1. **setup**: start here. Reads your socials and site, learns your brand's voice, finds and tracks your competitors, and makes the board where ideas wait for your yes.
2. **find-creators**: a sheet of creators to pay for your videos (people already posting about you, creators your rivals use, creators brands rehire, fresh breakouts), each checked on niche and format, with the contact their bio shows and a first message for you to send.
3. **creator-program**: how many creators to start with, what to pay each per video against published deals, whose accounts they post on, the first DM and a follow-up at your offer, the first 30 days and how to read the results.
4. **playbook**: takes any brand or creator apart, counted: what they repeat, which patterns win against their misses, their hooks word for word, how they sell, their Meta ads and creators, and the plays for your brand.
5. **formats**: the formats to make next, ranked for you, with examples, proof, what it takes to film and three angles for your brand.
6. **hooks**: opening lines built from hooks that are working in your format and niche, in your voice.
7. **ideas**: what's working among your competitors, your niche and your audience's comments, turned into ideas in your audience's words, each backed by the post it came from.
8. **winning-ad-ideas**: ten Meta ad ideas for your brand, each remade from a competitor's or your category's ad that has kept running 30 days or more, in its format, each a different picture, with every product fact yours or a slot for you to fill.
9. **brief**: turns an approved idea into a one-page brief each creator can film from on their phone: the hook word for word, three talking points, what to show and what to send.
10. **script**: the full script for an approved idea, in your voice, on a structure that works.
11. **make-video**: the finished video, static ad or carousel from an approved script, idea or reference, on your own tools, with every paid shot priced and asked first.
12. **review-draft**: checks a creator's draft video against their brief before you send notes: pass or fix, timestamped notes to paste to them, the brief's must-haves ticked one by one, and your own notes tagged as in the brief or a new ask.
13. **content-log**: your posts, and your creators' posts, against your usual: every pattern counted against the misses, and what to repeat, stop and turn into an ad. For creators, each one's posts against their usual, cost per 1,000 views, the hooks that won across creators, and who to double down on.
14. **loop**: runs ideas, scripts and the content log on a schedule, stopping where you choose for your yes.
15. **analyze**: any time, breaks down a video you found, proves why it worked against the creator's own misses, and saves its structure for your scripts.

Each command reads `/cracked-marketer:<skill>`, for example `/cracked-marketer:setup`.

## Install

In Claude Code:

1. `/plugin marketplace add LazyLines-App/vamos-plugins`
2. `/plugin install cracked-marketer@vamos-plugins`
3. Connect Vamos when asked and sign in. A free account works.
4. Type `/cracked-marketer:setup`.

Cracked marketer installs from this marketplace only. It isn't in Claude's plugin directory.

## What it can't do

Vamos reads public posts and Meta's Ad Library. It does not post, contact creators or run ads, and it can't read private analytics such as retention or reach unless you paste in a screenshot of your Insights. Nothing is posted, sent or paid for without your yes.

## Your data

- **Where your requests go:** to the Vamos connector (`https://mcp.getvamos.ai/mcp`). Vamos keeps your chats, brand profile, voice, saved files and tracked accounts in your Vamos workspace until you delete them, as [getvamos.ai/privacy-policy](https://getvamos.ai/privacy-policy) describes. Edit or delete any of it at [app.getvamos.ai/brain](https://app.getvamos.ai/brain).
- **Personal data it reads:** public posts and profiles.
- **Your board:** the skills keep your ideas, hooks and lessons in Notion or Google Sheets only when you have connected that app in Claude yourself; otherwise in a local `vamos/` folder or a Vamos Brain file. Pages are published as your own private Claude artifacts or saved as local files. No skill sends data anywhere else.
