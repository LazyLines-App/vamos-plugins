# Vamos for Claude

Vamos is your AI content strategist. This plugin adds the Vamos connector to Claude and seven skills, one for each main job:

- **viral-research**: what's going viral in your niche on TikTok, Instagram and YouTube, ranked against each creator's usual views, then ideas and scripts in your voice.
- **competitor-research**: a competitor's best organic posts on every platform, the Meta ads they keep running, their creator program, and what to copy.
- **creator-research**: creators who really get views in your niche, starting with people already posting about your brand, with the contact in their bio.
- **write-like-me**: learns your voice from your own videos and writes in it.
- **video-breakdown**: watches any TikTok, Reel or Short and explains why it worked and how to make yours.
- **content-strategy**: a strategy and dated calendar, and a verdict on any draft before you post it.
- **content-system**: sets up your voice and competitors, then each week researches, reviews your posts, writes next week's content and saves what it learned.

Vamos reads public posts and Meta's Ad Library, ranks them against each creator's usual views, and writes from what it found.

## Install

1. Add the plugin from Claude's directory (Plugins > Discover > Vamos > Add).
2. Open the plugin's Connectors tab, press Connect and sign in to Vamos. A free account works.

In Claude Code: `/plugin marketplace add LazyLines-App/vamos-plugins`, then `/plugin install vamos@vamos-plugins`.

## What it can't do

Vamos reads public posts and Meta's Ad Library. It does not post, edit videos, contact creators or run ads, and it can't read private analytics such as retention or reach unless you paste them in.

## Your data

- **Where your requests go:** to the Vamos connector (`https://mcp.getvamos.ai/mcp`). Vamos keeps your chats, brand profile, voice and saved files in your Vamos workspace until you delete them, as [getvamos.ai/privacy-policy](https://getvamos.ai/privacy-policy) describes.
- **Personal data it reads:** public posts and profiles. Creator research returns public creators' names, handles and the contact their bio shows.
- **Google Sheets:** `viral-research` and `creator-research` build a sheet in Google Sheets only when you have connected Google Sheets in Claude yourself and ask for a sheet. Otherwise they make a file. No skill sends data anywhere else.
