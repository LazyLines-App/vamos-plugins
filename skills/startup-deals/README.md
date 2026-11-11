# Startup deals

A standalone skill. It finds the startup credits, grants and perks a founder can get for their stage, team size and country: it asks five questions once, then gives what to apply for first, the programs everyone lists that won't work for them and why, and what a marketing tool kit costs a month on official prices. Each program shown is re-read on its own page, with the date. It needs no account or connector, spends no credits, and applies to nothing for you.

## Install

- **claude.ai:** zip this folder (`startup-deals`) and upload it under Settings → Capabilities → Skills.
- **Claude Code:** copy this folder to `~/.claude/skills/startup-deals/`.

Then ask "what startup credits can I get?".

The list in `references/deals.md` is dated and some rows are secondhand; the skill says which. Test cases are in `evals/`.
