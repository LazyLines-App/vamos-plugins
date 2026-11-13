# Vamos for Claude

Vamos is an AI agent for content research. This plugin adds the Vamos connector to Claude and a content system you can run end to end or one part at a time. In the order you'd run them:

1. **setup**: start here. Reads your socials and site, learns your voice from your own videos, finds and tracks your competitors, and makes your board, or uses the Notion or Sheet you already plan in, where ideas, scripts and posts wait for your yes. Run it again any time to see what's set up and what's next.
2. **playbook**: takes any brand or creator apart, counted: what they repeat, which patterns win against their misses, their hooks word for word, how they sell, their Meta ads, creators and what customers say in comments, reviews and Reddit if you want them, and the plays for your account.
3. **formats**: the formats to make next, ranked for you, with examples, proof, what it takes to film and two or three angles for your brand.
4. **hooks**: opening lines built from hooks that are working in your format and niche, in your voice. Keeps your hook database on the board.
5. **ideas**: what's working among your competitors, your niche and your audience's comments, turned into ideas in your audience's words, each backed by the post it came from, with the dates coming up that they fit.
6. **script**: the full script for an approved idea, in your voice, on a structure that works, with only facts you've said, checked before you see it.
7. **post**: your finished videos out on your accounts through your own Zernio, many accounts and many a day at the times you pick, after one yes to one table of every post. Each platform's AI label goes on for AI footage, the disclosure line goes in the caption, and every post is checked with Zernio before it goes.
8. **content-log**: your posts against your own usual, every pattern counted against the misses, and what to repeat, stop and turn into an ad, with the lessons recorded so every next run gets better. With an Ads Manager export, your ads' week too.
9. **loop**: runs ideas, scripts and the content log on a schedule, stopping where you choose for your yes, and posts the videos you mark Ready to post once you say those go out by themselves.
10. **analyze**: any time, breaks down a video or a whole profile, proves why the hits worked against the creator's own posts made the same way, beat by beat on a page, and saves each structure for your scripts.

Plus **creator-research**: creators who really get views in your niche, starting with people already posting about your brand.

Vamos reads public posts and Meta's Ad Library and keeps your brand, voice, tracked accounts and lessons in your workspace. Claude does the judging and the writing with the method in each skill, and makes each result a page you can read, share or film.

## How it runs

Your board is home. Setup makes it in your Notion (or a Google Sheet), or adds its columns to the content calendar you already keep there. Each idea, its script, the finished video and its post sit on one card:

1. New ideas land at To review. Approve the ones you'd make: drag the card, or tell Claude "approve 1 and 3".
2. Claude writes each approved idea's script in your voice, on its card.
3. You film and edit it in your own app, then put its link on the card and set it to Ready to post, or tell Claude where it is.
4. Say yes to one table and it posts on your Zernio, the posting service you sign in to with your own accounts (zernio.com, first two accounts free). A week on, the content log shows what worked, and the next ideas build on it.

Every run ends with the next step, and Claude runs it when you say yes, so there are no commands to remember. Ask "what's next?" any time to see what's waiting for you.

Any part works alone: ideas for this week, a script for your own idea, a breakdown of any video, or how last week's posts did. It fits what you already use: your own board, your own editor, and your own scheduler (post hands you each batch as a table for it).

## Install

In the Claude app (chat and Cowork):

1. Open Customize → Plugins → Add marketplace, enter `LazyLines-App/vamos-plugins`, and install Vamos. Once it's in Claude's directory, it's also under Discover.
2. Open the plugin's Connectors tab, press Connect and sign in to Vamos. A free account (200 credits, once) is enough to try it; a weekly loop needs a paid plan.
3. Type `/vamos:setup`.

In Claude Code: `/plugin marketplace add LazyLines-App/vamos-plugins`, then `/plugin install vamos@vamos-plugins`, then run `/mcp`, pick vamos and sign in. Then type `/vamos:setup`.

## What it can't do

Vamos reads public posts and Meta's Ad Library. Vamos itself never posts: the post skill sends your videos through your own Zernio account, which you connect in Claude. It does not edit videos, contact creators or run ads, and it can't read private analytics such as retention or reach unless you paste in a screenshot of your Insights. Nothing is posted, sent or paid for without your yes.

## Your data

- **Where your requests go:** to the Vamos connector (`https://mcp.getvamos.ai/mcp`). Vamos keeps your chats, brand profile, voice, saved files (such as Tracked accounts, Voice examples and What works for me) and tracked accounts in your Vamos workspace until you delete them, as [getvamos.ai/privacy-policy](https://getvamos.ai/privacy-policy) describes. Edit or delete any of it at [app.getvamos.ai/brain](https://app.getvamos.ai/brain).
- **Personal data it reads:** public posts and profiles. Creator research returns public creators' names, handles and the contact their bio shows.
- **Your board:** the skills keep your ideas, hooks and lessons in Notion or Google Sheets only when you have connected that app in Claude yourself; otherwise in a local `vamos/` folder or a Vamos Brain file. Pages are published as your own private Claude artifacts or saved as local files.
- **Posting:** the post skill sends the video files, captions and times you said yes to to your own Zernio account, which publishes them to your accounts. Vamos never sees your Zernio sign-in or your accounts' tokens. No skill sends data anywhere else.
