# Vamos for Claude

Vamos is an AI agent for content research. This plugin adds the Vamos connector to Claude and a content system you can run end to end or one part at a time. In the order you'd run them:

1. **setup**: start here. Reads your socials and site, learns your voice from your own videos, finds and tracks your competitors, and makes the board where ideas wait for your yes. Run it again any time to see what's set up and what's next.
2. **playbook**: takes any brand or creator apart, counted: what they repeat, which patterns win against their misses, their hooks word for word, how they sell, their Meta ads, creators and what customers say in comments, reviews and Reddit if you want them, and the plays for your account.
3. **formats**: the formats to make next, ranked for you, with examples, proof, what it takes to film and two or three angles for your brand.
4. **hooks**: opening lines built from hooks that are working in your format and niche, in your voice. Keeps your hook database on the board.
5. **ideas**: what's working among your competitors, your niche and your audience's comments, turned into ideas in your audience's words, each backed by the post it came from, with the dates coming up that they fit.
6. **script**: the full script for an approved idea, in your voice, on a structure that works, with only facts you've said, checked before you see it.
7. **content-log**: your posts against your own usual, every pattern counted against the misses, and what to repeat, stop and turn into an ad, with the lessons recorded so every next run gets better. With an Ads Manager export, your ads' week too.
8. **loop**: runs ideas, scripts and the content log on a schedule, stopping where you choose for your yes.
9. **analyze**: any time, breaks down a video or a whole profile, proves why the hits worked against the creator's own posts made the same way, beat by beat on a page, and saves each structure for your scripts.

Plus **creator-research**: creators who really get views in your niche, starting with people already posting about your brand.

Vamos reads public posts and Meta's Ad Library and keeps your brand, voice, tracked accounts and lessons in your workspace. Claude does the judging and the writing with the method in each skill, and makes each result a page you can read, share or film.

## Install

1. Add the plugin from Claude's directory (Plugins > Discover > Vamos > Add).
2. Open the plugin's Connectors tab, press Connect and sign in to Vamos. A free account works.
3. Type `/vamos:setup`.

In Claude Code: `/plugin marketplace add LazyLines-App/vamos-plugins`, then `/plugin install vamos@vamos-plugins`.

## What it can't do

Vamos reads public posts and Meta's Ad Library. It does not post, edit videos, contact creators or run ads, and it can't read private analytics such as retention or reach unless you paste in a screenshot of your Insights. Nothing is posted, sent or paid for without your yes.

## Your data

- **Where your requests go:** to the Vamos connector (`https://mcp.getvamos.ai/mcp`). Vamos keeps your chats, brand profile, voice, saved files (such as Tracked accounts, Voice examples and What works for me) and tracked accounts in your Vamos workspace until you delete them, as [getvamos.ai/privacy-policy](https://getvamos.ai/privacy-policy) describes. Edit or delete any of it at [app.getvamos.ai/brain](https://app.getvamos.ai/brain).
- **Personal data it reads:** public posts and profiles. Creator research returns public creators' names, handles and the contact their bio shows.
- **Your board:** the skills keep your ideas, hooks and lessons in Notion or Google Sheets only when you have connected that app in Claude yourself; otherwise in a local `vamos/` folder or a Vamos Brain file. Pages are published as your own private Claude artifacts or saved as local files. No skill sends data anywhere else.
