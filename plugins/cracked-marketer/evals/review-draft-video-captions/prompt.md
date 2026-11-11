---
description: "Claude Code, a local draft video. The scaffold writes the brief skill's own example brief (Dana, Potly) to vamos/briefs.md and makes her draft: a synthetic 18 s 1080x1920 video (macOS say + ffmpeg, burned-in captions) with her captions file beside it. On purpose: the hook is word for word, Potly first shows at 4.6 s (brief: by 3 s), the star line is changed, and the caption she sent has no #ad. The user adds one note the brief covers (the screens' pace, part 4) and one it doesn't (a 30-day free claim). Creator program: one round of notes. Tests the approve-when list ticked item by item, timestamped notes to paste, notes tagged in the brief or new ask, the round counted, and the review recorded. Run with --scaffold --allow-tools Bash Write Edit."
tags: [review-draft, claude-code, video, scaffold]
runs: 1
model: sonnet
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Bash, Write, Edit]
---

Dana sent her draft for Potly: drafts/dana-draft.mp4, with her CapCut captions file beside it. The caption she'll post is "payday routine 💸 @potly". Check it against her brief before I send her notes. Two notes of mine: the pots go by too fast, and can she say it's free for 30 days?
