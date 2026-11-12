# Cracked marketer by Vamos

The marketing hire a brand or startup would make, in Claude. It researches what's working on TikTok, Instagram and YouTube, plans and writes your content, logs what works and runs it all on a loop. It finds your creators, plans what to pay them, writes their briefs, checks their drafts, writes ad ideas from the ads that keep running and makes the videos.

It holds all nine Content System skills (find-creators does creator research's job), so you never need both. Content System is for creators, coaches and service providers who film their own content. Cracked marketer is for a brand or startup that needs the whole marketing job done.

## Skills, in the order you'd run them

1. **setup**: start here. Reads your socials and site, learns your brand's voice (from the videos of whoever talks on camera, the founder or someone on your account, else from your site, captions and ads), finds and tracks your competitors, and makes the board where ideas wait for your yes.
2. **find-creators**: a sheet of creators to pay for your videos (people already posting about you, creators your competitors use, creators brands rehire, fresh breakouts), each checked on niche and format, with the contact their bio shows and a first message for you to send.
3. **creator-program**: how many creators to start with, what to pay each per video against published deals, whose accounts they post on, the first DM and a follow-up at your offer, the first 30 days and how to read the results.
4. **playbook**: takes any brand or creator apart, counted: what they repeat, which patterns win against their misses, their hooks word for word, how they sell, their Meta ads and creators, what customers say in comments, reviews and Reddit, counted into reasons, and the plays for your brand.
5. **formats**: the formats to make next, ranked for you: the Meta ad formats your category keeps running 30 days or more, statics included, then the video formats taking off, each with the job it does, examples, whether your creators can film it and two or three angles for your brand.
6. **hooks**: opening lines built from hooks that are working in your format and niche and from the first lines of the Meta ads your category keeps running, in your voice.
7. **ideas**: what's working among your competitors, your niche and your audience's comments, turned into ideas in your audience's words, each backed by the post it came from, with the dates coming up that they fit.
8. **winning-ad-ideas**: ten Meta ad ideas for your brand, each remade from a competitor's, your category's or a neighbouring brand's ad that has kept running 30 days or more, in its format, each a different picture, with every product fact yours or a slot for you to fill. Three blind judges (your track record, your customers' words, an assassin) keep the strong ones, which go on your board with a code your content log tracks; plus what each brand launched this week.
9. **brief**: turns an approved idea into a one-page brief each creator can film from on their phone: the hook word for word, three talking points, what to show and what to send.
10. **script**: the full script for an approved idea, in your voice, on a structure that works.
11. **make-video**: the finished video, static ad or carousel from an approved script, idea or reference, on your own tools, with every paid shot priced and asked first.
12. **review-draft**: checks a creator's draft video against their brief before you send notes: pass or fix, timestamped notes to paste to them, the brief's must-haves ticked one by one, and your own notes tagged as in the brief or a new ask.
13. **content-log**: your posts, and your creators' posts, against your usual: every pattern counted against the misses, and what to repeat, stop and turn into an ad. For creators, each one's posts against their usual, cost per 1,000 views, the hooks that won across creators, and who to double down on. With an Ads Manager export, your ads' week: spend and CPA against last week, risers and fallers, the words in your ad names that win, and which concepts ran.
14. **loop**: runs ideas, scripts and the content log on a schedule, stopping where you choose for your yes, and on Mondays the research pack: your ad account's week, what customers say and judged ad concepts.
15. **analyze**: any time, breaks down a video or a whole profile, proves why the hits worked against the creator's own posts made the same way, and saves each structure for your scripts.

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
