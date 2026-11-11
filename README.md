# Vamos plugins

Two plugins for Claude, each with the Vamos connector (`https://mcp.getvamos.ai/mcp`):
- **Vamos** (`vamos`, Content System): a content system for TikTok, Instagram and YouTube, for creators, coaches and service providers who film their own content. Nine skills in run order plus creator research. See [plugins/vamos/README.md](plugins/vamos/README.md).
- **Cracked marketer by Vamos** (`cracked-marketer`): the marketing hire for a brand or startup. Everything in Content System, plus finding and paying creators, their briefs, ad ideas from the ads that keep running, and the videos. See [plugins/cracked-marketer/README.md](plugins/cracked-marketer/README.md).

Vamos supplies the data (posts, comments, transcripts, ads) and keeps the user's state (brand, voice, tracked accounts, Brain files); each skill holds the method, and Claude does the judging, writing and checks and makes the page. How to change, test and release a skill is in [MAINTAINING.md](MAINTAINING.md); what changed is in [CHANGELOG.md](CHANGELOG.md).

Not a plugin: `skills/startup-deals` is a standalone skill for finding startup credits and perks (no connector). Install steps are in its README.
