# Plugin evals (mocked Vamos)

Replays of the Vamos skills with `claude plugin eval`. The Vamos connector is replaced by saved real answers, so a run spends no Vamos credits and sees the same data every time: a change in score is the skill, not the data. Each run still costs Claude usage (about $0.07 to $0.10 for a short case on Sonnet).

The routing cases are separate: `evals/routing` at the repo root.

## Layout

```
plugins/vamos/evals/
  mocks/vamos/<tool>.md       suite-wide default answer for each tool the skills call
  mocks/vamos/_tools.json     the connector's real tool descriptions and input schemas (prod tools/list, 2026-11-11)
  mock-library/vamos/*.md     spare real answers (not read by the runner; copy one into a case)
  <case>/prompt.md            the user's message, plus run limits
  <case>/graders/*.md         one check per file
  <case>/mocks/vamos/<tool>.md   this case's own answer; overrides the suite's file for that tool
```

How the runner works (Claude Code 2.1.318, https://code.claude.com/docs/en/plugin-evals.md):

- Cases are found under `evals/` of the plugin directory (`plugins/vamos/evals`). Run from `plugins/vamos`. `--eval-dir` or `experimental.evals` in `plugin.json` could move them; we use the default.
- The mock folder name is the server name in `.mcp.json` (`vamos`), the file name is the tool name. In the run the tools are named `mcp__plugin_vamos_vamos__<tool>`; use that name in graders.
- A tool with no mock file is not available to Claude. Mocked tools need no `--allow-tools`.
- The file body is returned as the tool result. `{{input.<field>}}` inserts a field of the call's input. Frontmatter (all optional): `expect:` (guard the input; a violation aborts the run with score 0), `error: true`, `type: agent` (a judge model answers as the server; costs a judge call per tool call, and varies).
- A case's `mocks/` overrides the suite's file by file, so two cases can get different answers for the same tool.
- The remote OAuth server stays mocked: the run's `mocks` block lists the `vamos` server as `kind: shadow`, `calls.unmocked` is empty, there is no sign-in step, and the Vamos credit balance is the same before and after. The real server only starts with `--allow-real-servers` (for tools that have no mock) or `--mocks off`.
- One answer per tool, whatever the input. The default `chat_completion_poll` is a finished reel breakdown; a case about formats or a playbook swaps in its own (below). A skill that needs two different polls in one run needs a `type: agent` mock or `{{input.runId}}` plumbing; none of ours does yet.

## Graders that matter here

```yaml
# never called (grades the tool name, not the text)
type: tool_used
tool: mcp__plugin_vamos_vamos__set_up_workspace
min: 0
max: 0
```

```yaml
# called exactly once
type: tool_used
tool: mcp__plugin_vamos_vamos__set_up_workspace
min: 1
max: 1
```

```yaml
# what the mocks were asked and answered (a regex over every mocked call, free)
type: regex
target: mock_calls
pattern: set_up_workspace
match: not_contains
```

`tool_used: Skill` with `input_match` says whether the skill fired; it is reported but not scored in a with/without run. `llm` graders cost a judge call each; keep them for short outputs. A grader's `pattern` with a colon needs quotes in YAML.

## Add a case from a saved answer

1. Find the answer. Every connector call is in the Claude Code transcripts under `~/.claude/projects/`.
   ```
   scripts/mock-from-transcript.py list <session-id | transcript.jsonl> --tool chat_completion_poll --done-only --min-chars 3000
   ```
   The list shows the question each poll answered.
2. Save it into the case, scrubbed:
   ```
   scripts/mock-from-transcript.py write <session-id> --id <toolu_...> --case my-case --name chat_completion_poll --max-chars 6000
   ```
   It removes emails, phones, tokens, signed-URL parameters, workspace ids and page cursors, and gives chat and run ids stable made-up values. `--drop-match REGEX` removes rows that name a customer; `--replace OLD=NEW` swaps a private name; `--expect` adds a guard on what the skill sent. Read the file before you commit: the repo is public.
3. Or reuse a spare: `scripts/mock-from-transcript.py use poll-playbook-notion --case my-case`.
4. Write `my-case/prompt.md` (the way a user types it; do not name the skill) and one or two graders: one on the result, one on the steps.
5. Run it:
   ```
   cd plugins/vamos
   claude plugin eval . --case my-case --runs 1 --ablation none --max-cost-usd 1 --no-publish --trust-plugin \
     --output-dir /tmp/eval-out --json /tmp/eval-out/run.json
   ```
   In the JSON, `cases[].arms.with[].mocks.calls` has `total` calls, `unmocked: []` and `costUsd: 0`; `graders` has each verdict.

## Cost controls

- `--runs 1` while building a case; the default is 3 per arm. `--ablation none` skips the no-plugin arm (half the cost). Use the with/without arms only when you want the plugin's lift.
- `--max-cost-usd N` stops before a run that would pass N. Set `model: sonnet` and `max_turns` in `prompt.md`.
- `--no-publish` keeps the report local (the default publishes it to claude.ai when the account can). `--output-dir` and `--report` keep results out of the repo; `evals/results/` is gitignored if you forget. A `--keep-temp` folder is sealed and large: `chmod -R 700` it, read it, delete it.
- Disk is tight on this machine (about 1 GB free): delete the output folder after reading the JSON.

## Real servers cost credits

Nothing here starts the real Vamos server unless you ask. `--allow-real-servers` (for tools with no mock) and `--mocks off` start it as you, outside the sandbox, with your Vamos sign-in; `chat_completion_start` and `set_up_workspace` then spend real credits. Never pass them for a routine run, and never from a workspace whose Brain you care about. Free reads (`get_workspace`, `get_credit_usage`, `list_chats`, `get_messages`, `auth_status`) are how new answers are saved; the paid ones are saved from an earlier live session's transcript, never by a call made for the mock.

## Where each mock came from

Dates are when the answer was saved; the sessions are Claude Code transcripts on the M3. Nothing private is kept: workspace name "Levi" is "Demo", private chat titles, Brain files and routines are dropped, creator emails are `person@example.com`.

| Mock | Source |
| --- | --- |
| `mocks/auth_status` | free read on the connected workspace, 2026-11-10 (workspace name replaced) |
| `mocks/get_credit_usage` | free read, 2026-11-10 (Pro monthly plan, 2,000 credits) |
| `mocks/get_workspace` | free read, 2026-11-10: an already set-up workspace; tracked accounts cut from 220 to 6, three private Brain files and routines dropped, the counts left as they were |
| `mocks/list_chats` | plugin test run, 2026-11-05: 8 of 60 chats, including the real `title: null` first row |
| `mocks/create_chat` | UGC test run, 2026-11-09 |
| `mocks/chat_completion_start` | UGC test run, 2026-11-09 |
| `mocks/chat_completion_poll` | kit smoke test, 2026-11-05: "Break down this reel" on a public Instagram post (same as `poll-analyze-reel`) |
| `mocks/chat_completion_cancel` | test run, 2026-11-09 |
| `mocks/get_messages` | creators-sheet test run, 2026-11-09 (page cursor set to null) |
| `setup-elsewhere-notion/mocks` | the real demo2 run, 2026-11-11 (`vamos-demo2`, a fresh Free workspace, @notionhq on Instagram): the research poll (32 credits, 13 @notionhq rows inline with transcripts, 10 comparison accounts) with private people's names replaced and the partner rows dropped. `get_workspace` is **derived** (the real setup answer says the Brain, the website, @clickup and five creators were saved, so voice false, no files, 6 tracked); `get_messages` is built from the poll |
| `setup-home-notion/mocks` | `get_workspace` and `get_credit_usage` are the real reads after that run's save turn (voice true, seven Brain files, 11 tracked, 153 credits) |
| `mock-library/poll-setup-notion` | the real `set_up_workspace` answer for that run (0 credits, 146 s); the runner gives one answer per tool, so it cannot sit beside the research poll in one case |
| `mocks/_tools.json` | prod's tools/list on 2026-11-11 (Chat #1502), read on demo1 (`vamos-demo`) from a `claude -p` session's tool definitions with no Vamos tool called, and checked against `src/mcp/tools/saveBrainFile.ts` on Chat main: 11 tools, `save_brain_file` new, get_workspace's `file` now names skills, chat_completion_start's `content` asks for a save as its own message |
| `mocks/save_brain_file` | **real shape**: the live demo1 call on 2026-11-11 answered `{"title":"Plugin build test 1111","kind":"file","action":"created"}`, then `"unchanged"` for the same text; the mock echoes `{{input.title}}` and always says `created`, `kind: file` (one answer per tool, so a skill save reads as a file too) |
| `setup-fresh-getripping/mocks/save_brain_file` | **real text from the code** (`saveBrainFile.ts`, the failed index read), saved with `error: true`: every save fails, so the case checks no failed save is reported as saved |
| `mocks/set_up_workspace` | the same shape `chat_completion_start` returns (`startWorkspaceSetup` calls the same run starter); the saved start from 2026-11-09. No prod `set_up_workspace` answer was saved yet |
| `playbook-notion-tiktok-instagram/mocks` | the real demo1 run, 2026-11-11 (`vamos-demo`, @getripping's workspace, Notion on TikTok and Instagram, 60 credits, 675 s): Vamos's answer with its 40-post tables cut to 10 rows each; the `data` block is the live run's 200-row file, cut to the 80 cited posts (Notion's own 40 TikToks, 26 Reels and 14 partner Reels) and slimmed to the fields a count needs. The first try inlined the full 42,000-character answer plus the full rows (86,000 characters); the runner saved that to a file the sandbox would not let the skill read, so the case is kept under about 45,000 characters |
| `formats-live-getripping/mocks` | the real demo1 formats run, 2026-11-11 after Chat #1502 (`vamos-demo`, 19 credits): the result text, and the run's `json_url` rows file put in the inline shape (34 of 105 format rows: the cited ones, up to four examples per format plus any the text links, with `status` and `niche_examples`; the 8 cited of 151 video rows; creator names dropped; chat and run ids made up). Cut from 62K to 42K characters: at 62K the eval host saved the poll to a file its sandbox wouldn't let the run read (eval-3, 11-11), while the 47K round-1 mock was read inline. The link and number graders still list every row of the 50. `get_workspace` is the earlier no-setup read |
| `mock-library/poll-analyze-reel` | kit smoke test, 2026-11-05 |
| `mock-library/poll-analyze-vs-usual` | kit round 1, 2026-11-05: a reel against the creator's usual views |
| `mock-library/poll-formats-skincare` | kit round 2, 2026-11-05: five formats in skincare |
| `mock-library/poll-ideas-fitness` | kit round 3, 2026-11-05: seven ideas from viral fitness videos |
| `mock-library/poll-playbook-notion` | 2026-11-09: a brand's last 30 days (cut to about 5,000 characters) |
| `mock-library/poll-playbook-cal-ai` | value-line test, 2026-11-09: a brand's growth taken apart (cut) |
| `mock-library/poll-creators-olipop` | kit round 1, 2026-11-05: creators already posting about a brand (emails scrubbed, cut) |
| `mock-library/poll-ads-gymshark` | kit round 8, 2026-11-05: a brand's Meta ads (cut) |
| `mock-library/poll-comments-gymshark` | kit round 2, 2026-11-05: what an audience asks for in comments |
| `mock-library/poll-voice-guide` | 2026-11-05: Vamos's own provisional voice guide |
| `mock-library/poll-working` | 2026-11-09: a run still `working` |
| `mock-library/get-messages-chat-not-found` | 2026-11-09: the real error for an unknown chat (saved with `error: true`) |
| `mock-library/chat-completion-cancel` | 2026-11-09 |
| `mock-library/get-workspace-fresh` | **derived from the connector code** (`composeWorkspaceState` on an empty workspace), not saved from a call: FREE plan, no voice, no files, nothing tracked. The real one (with `cap`) is in `setup-fresh-getripping/mocks/` |
| `mock-library/create-chat-fresh` | **derived from the code** (`createChat` with the `SETUP_NOTE` and no `brain`) |
| `mock-library/get-credit-usage-free` | **derived**: the Free plan's 200 credits |
| `mock-library/set-up-workspace-already-running` | **derived from the code**: what a second `set_up_workspace` gets while the first runs |
| `setup-fresh-getripping/mocks/*` (get_workspace, get_credit_usage, set_up_workspace, chat_completion_poll), `setup-asks-once/mocks/*` | **real**: demo1's setup of @getripping, 2026-11-11 09:00 UTC (`vamos-demo`, Free, 200 + 2,000 credits): the fresh state, the set_up_workspace start and its finished answer (`creditsCharged: 0`, 173 s), ids remapped by the script. chat_completion_start echoes `{{input.chatId}}` (derived); create_chat is `create-chat-fresh` |
| `setup-home-getripping/mocks/get_workspace` | **derived**: the real post-setup state with the six setup file titles added; a `file` read returns the same state (one answer per tool) |
| `setup-home-getripping/mocks/create_chat` | **derived**: `create_chat`'s shape with that workspace's real `brain` line |
| `analyze-video-tiktok-chloejp/mocks/chat_completion_poll` | kit round 2, 2026-11-05: "Watch this and break it down" on a public TikTok; real, unchanged (2 ids remapped) |
| `analyze-profile-duolingo-tiktok/mocks/chat_completion_poll` | **real**: the skill's own profile ask, live on the demo workspace (2026-11-11 09:05 UTC, `vamos-demo`, 17 credits): 40 cited TikTok rows inline and three pairs with timed beats. The answer was 63,692 characters, so Claude Code saved it to a file; read from that file and scrubbed with this script's `scrub_value`, then the 10 uncited rows, thumbnail links, null fields and the repeated creator fields past handle, name and followers were dropped (45,978 characters). The answer's line "Nothing has been saved to the Brain" is kept: the live ask said not to save, and the case still expects the save ask, since rows came back |
| `analyze-video-instagram-getripping/mocks/chat_completion_poll` | **assembled from real reads**, not a Vamos chat answer: the account's 40 posts (vamos-research `fetch_link`, 2026-11-10 22:49 UTC) as `data` rows in the poll's row schema, plus `watch_video` of the hit and the miss (22:51 UTC) written up as the answer text. No number in it is made up; `creditsCharged` is null |
| `analyze-profile-opusjake/mocks/chat_completion_poll` | **assembled from real reads**: the account's 40 posts (vamos-research `fetch_link`, 2026-11-10 11:16 UTC) as rows, plus 10 word-timed local transcripts from the studying-winners study; the answer text describing the rig is ours, from the study's frames |
| `analyze-video-youtube-erikcupsa/mocks/chat_completion_poll` | **real**: the pilot's live run (2026-11-10 23:13 UTC, `vamos-mcp` signed in, 14 credits): a Short's reason against the account's own posts, with its 40 Shorts as rows. Thumbnails removed, captions cut to 80 characters, the answer text cut at 11,000 characters (the timed-beats part of the second comparison is `[trimmed for the mock]`), the 10 uncited rows dropped, and one sentence ("Nothing was saved to the Brain or a board") removed because the live ask said it and the eval's prompt doesn't. The uncut answer was 73,015 characters and Claude Code saved it to a file instead of showing it; a mock that size does the same, and the eval sandbox can't read that file (the run said so and stopped). Keep a mock under about 50,000 characters |
| `content-log-week-opusjake/mocks/chat_completion_poll` | **assembled from real reads**: a copy of `analyze-profile-opusjake`'s mock (40 posts, vamos-research `fetch_link`, 2026-11-10 11:16 UTC) |
| `content-log-week-opusjake-link/mocks/chat_completion_poll` | **assembled from real reads**: the same answer and rows as `content-log-week-opusjake`, with `data` as the connector's default sends it (counts and a file link); `fixture.sh` writes the rows to the `file:vamos-data/...` link, relative to the run's folder, since the sandbox has no network and can't read `/tmp` |
| `content-log-quiet-week-vamos/mocks/chat_completion_poll` | **real**: kit full test, 2026-11-05, "Review my week" on Vamos's own @getvamosai (16 credits, no rows); scrubbed, unchanged |
| `content-log-board-getripping/mocks/chat_completion_poll` | **assembled from real reads**: `analyze-video-instagram-getripping`'s 40 rows (`fetch_link`, 2026-11-10 22:49 UTC) with a short answer text of ours written from the rows, then (11-11) the live demo1 answer's sections on the recent posts, what the audience asks for and what to change next (2026-11-11 14:20 UTC), their numbers set to these rows and competitor links left out. That detail (the hit's spoken run-on ", basically forcing people to notice your product", and narrow asks like "turn a customer complaint into a Reel opener") is what live Repeat versions were built from; `creditsCharged` null |
| `content-log-two-platforms-live/mocks/chat_completion_poll` | **real**: the content-log live run on demo1 (`vamos-demo`, 2026-11-11 10:44 UTC, 14 credits), "Content log for RIP (@getripping) on Instagram and TikTok, last 7 days": a 25,098-character answer on 7 Instagram posts and the 30 before, TikTok "no public videos", `data` is counts plus a file link (signed parameters removed), so the 37 cited rows are not in it. Scrubbed by the helper, nothing else changed |
| `content-log-board-getripping/mocks/get_workspace` | **ours**: a set-up workspace for the case (Vamos settings with ads on and a local board, Marketing plan, What works for me); the brand line follows demo1's setup on 11-11. One answer serves both the index and a `file` read |
| `ideas-niche-coffee/mocks/chat_completion_poll` (and `ideas-own-ideas-coffee`) | **real**: kit round 2, 2026-11-05 (60 credits): "What's going viral in coffee on TikTok and Instagram this week", 10 inline rows read 2026-11-05, unchanged but for remapped ids |
| `ideas-rival-comments-gymshark/mocks/chat_completion_poll` | **real**: kit round 2, 2026-11-05 (15 credits): what Gymshark's audience keeps asking for in the comments, quoted with likes; every commenter's handle replaced with "a commenter" |
| `ideas-ad-find-gymshark/mocks/chat_completion_poll` | the spare `poll-ads-gymshark` (kit round 8, cut) |
| `ideas-*/mocks/get_workspace`, `create_chat` | **ours**: two test brands (Slow Pour, home coffee; Hollow Peak Active, leggings). `get_workspace` is a `type: agent` mock, since a `{{file:fixtures/{input.file}.json}}` fixture refuses a title with a space and errors when `file` is absent (probed 2026-11-11) |
| `ideas-live-getripping/mocks/*` | **real**: the ideas skill's own live run on `vamos-demo` (2026-11-11 10:39 UTC, Sonnet, 51 credits, 767 s). `chat_completion_poll` is the one research turn's answer for RIP (Apps & SaaS, Instagram, five tracked accounts) with 47 cited public posts in the text; the real `data` held only counts and a `json_url` for 200 rows; the scrubbed link can't be fetched, so `data.videos` carries the first 50 of those rows inline, as Vamos's inline data does (public posts, fetched from the run's own link on 11-11; null fields, ids and shares dropped; the 47 cited come first), and `filter.py` keeps 22 of them at the 10,000-view floor (41 of the 200 on the live file). All 200 inline made the answer 118,000 characters, so Claude Code saved it to a file the eval sandbox won't let a run read (eval-3). Signed-URL parameters and ids scrubbed by the helper. `get_workspace` and `create_chat` are the same run's answers (workspace has no Vamos settings, so setup hasn't run) |
| `ideas-followers-asks-getripping/mocks/chat_completion_poll` | **real**: the skill's comments ask for RIP's own posts, live on demo1 (2026-11-11 14:36 UTC, `vamos-demo`, 12 credits, 286 s): the asks on the last 20 Instagram posts, each marked answered by a hook or caption or "not made yet", with the 20 posts as inline rows. Scrubbed with the helper's `scrub_value`; every commenter's handle replaced with "a commenter"; null fields and ids dropped |
| `ideas-worth-making-getripping/mocks/chat_completion_poll` | **real**: the skill's worth-posting ask on two RIP ideas, live on demo1 (2026-11-11 14:41 UTC, `vamos-demo`, 21 credits, 426 s): lookalikes counted against each creator's usual, best and worst 3 per idea, 50 inline rows (12 cited). The answer came back 55,000 characters, so Claude Code saved it to a file; read from there, scrubbed the same way, null fields dropped (39,879) |
| `ideas-followers-asks-getripping`, `ideas-worth-making-getripping` `get_workspace` | a `type: agent` mock of demo1's **real** free reads on 2026-11-11 (the workspace line, Vamos settings, the empty Brain-file board and the voice guide, as another skill's live run read them that afternoon); any other title gets the real `ERR_INVALID_INPUT` line. `create_chat` is that run's shape with the poll's chat id |
| `script-board-getripping/mocks/chat_completion_poll` | **real**: the script skill's own find ask, live on the demo workspace (2026-11-11 13:24 UTC, `vamos-demo`, 2 credits): the Vamos prose summarised the beats and declined the verbatim transcript, and the transcript came in `data.videos[0].transcript` (no word timings; the reel read 835,043 views that day, 613,124 on the board). Scrubbed with this script; the rest of the case (`get_workspace` voice guide, board) stays as in the case's description
| `script-es-mariaduran/mocks/vamos/get_workspace` | **assembled from a real read**: one live demo1 ask (2026-11-11 17:24 UTC, `vamos-demo`, 6 credits, `include_transcripts`) for six of @mariadurancontent's newest talking reels; four transcripts kept verbatim as Voice examples (one came back as noise, one empty), voice numbers by `textstats.py profile`, the guide and Things you've said written by us from those transcripts |
| `script-*/mocks/vamos/get_workspace` | **assembled from real reads**: demo1's Vamos-built voice guide (free read, 2026-11-11) for the RIP cases; for the @opusjake cases the guide's text is ours and the Voice examples are his public transcripts. Answered by a `type: agent` mock from the sections |

Re-save any of these from a new session with `scripts/mock-from-transcript.py`; the derived ones should be replaced the first time a live fresh-workspace run is saved.

## Cases

| Case | What it proves |
| --- | --- |
| `setup-already-done` | Smoke: the suite's set-up workspace; setup must not call `set_up_workspace`. |
| `setup-fresh-getripping` | A fresh Free workspace (real demo1 reads): get_workspace first, `set_up_workspace` once with the named competitor in `competitors` (free), one research turn in setup's own chat with rows and transcripts, credits as the poll billed them, files never saved through a Vamos message, and no save reported when every `save_brain_file` fails. |
| `setup-elsewhere-notion` | Set up elsewhere, a B2B brand (state derived from the real demo2 setup answer; the real research answer): no second setup, the research turn carries @clickup and neither rebuilds the voice nor unfollows; the usual from the real @notionhq rows (29,028 over the 12 posts at least 7 days old; the student Campus Leader repost is 6.6 days old, so it is out either way); no invented account; says what it kept; the Brain files saved with `save_brain_file` (free), never through a Vamos message, and no voice guide save claimed. |
| `setup-home-notion` | Set up here before (the real demo2 state after its save turn): the second run is free, never sets up again, says where to edit and what to run next. |
| `setup-home-getripping` | Set up here before (derived state with Vamos settings): the home visit bills nothing, reads Vamos settings free, says where to edit and what to run next. |
| `setup-whats-next-board` | "what's next?" alone, on a workspace whose Vamos board Brain file holds one idea at Approved and two at To review (the first-run case's mocks): setup reads the board free, says what waits and offers the approved idea's script as a question. |
| `setup-asks-once` | An empty ask on a fresh workspace: one numbered message of at most 6 questions, nothing set up or billed first. |
| `analyze-video-instagram-getripping` | A reel at about 9× beside a same-format miss at about 1.1× from the same account; the usual by the rule (32,507.5 over 32 posts at least 7 days old: a repost is the same caption within 2 s, so DfFoUcNjUPY is out and the re-cut De49HQvgUbF counts). |
| `analyze-video-tiktok-chloejp` | A thin answer (Vamos's own usual, no rows, no linked miss): no invented pair, median or link. |
| `analyze-video-youtube-erikcupsa` | A Short beside its same-way comparison (82,566; Vamos's second, 32,223, is under 7 days old and above the usual, so never the miss); the five partner-tagged posts, Adobe's 820,813 among them, kept out of the usual (23,477.5 over 32). |
| `analyze-profile-opusjake` | A profile's hits against same-rig misses; the studying-winners study is the answer key. |
| `analyze-profile-duolingo-tiktok` | The usual computed from rows by the rule (823,638.5 over 32 posts at least 7 days old), not Vamos's 1,172,308; the 8 posts under 7 days never judged a miss, so Vamos's dance pair (its miss is under a day old) is set aside. |
| `content-log-week-opusjake` | No setup, no board: the usual by the rule (37,629.5 over 30, posts at least 7 days old), the 16.3× hit (so far, at 4.4 days) on Repeat with 3 to 5 versions on its own sentence, five posts too early to judge. |
| `content-log-week-opusjake-link` | The opusjake case with the rows behind the poll's link (run with `--scaffold --allow-tools Bash Write Edit`): `count.py` downloads them, so the same answer key (37,629.5, 16.3× so far) tests the path real runs take. `counts-on-the-link` checks that step; the answer key also needs count.py run from the run's folder, since the link is relative (a run that cds into the skill folder first can't open it). That miss is the test's, not the skill's: real links are absolute https (review 2, approved by the build lead 11-11), and `evals/scripts/test_count.py` covers the https download. |
| `content-log-quiet-week-vamos` | Nothing posted in the window: no invented winners, Vamos's usual named as Vamos's, credits 16 from the poll. |
| `content-log-board-getripping` | A scaffolded `vamos/board.md` (run with `--scaffold --allow-tools Bash Write Edit`): predictions checked, the ad list by Levi's rule, lessons moved only by the rule, one Reviews row, the hook's Result, and 3 to 5 versions of the "Claude can now … for you" hit on its own sentence: one clause ending at "for you", each job as big as "run your Instagram" (Levi's line). The mock carries the live answer's narrow detail, so this case reproduces the live misses: before the fix, 2 of 4 Sonnet runs swapped in narrow jobs ("copy your competitors' best reels", "turn your customers' complaints into hooks"). `repeat-the-hit` has the judge write one line per version (good or bad, and why) before its verdict, since a verdict-only Haiku judge failed correct versions: replayed on two saved correct replies and two broken copies of one (a run-on and narrow jobs), 3 votes each, the verdict-only wording passed 3 of 6 correct and the reasons-first wording 6 of 6, and both failed all 6 broken. Its pass and fail conditions are unchanged. `board-lessons-by-the-rule` failed review 3's run for a real reason: it reached 3 posts for a Stop by counting a post it called "my judgment call". |
| `content-log-two-platforms-live` | The live run's answer (see the mock table): a TikTok that came back empty, the posts behind a file link. Graded on the ask: one research turn for Instagram and TikTok with `data_scope: "turn"`, and on every post read. |
| `ideas-niche-coffee` | A home coffee creator's "what should I post": the bar on real finds (a language-app joke and a health-claim list out), numbers from the rows, the straight swap, the board duplicate, their call, the thin stage. `straight-swap-first` reworded 11-11 (round 3, the lead's call, as ideas.md's "keep its picture when the picture carried it"): on a no-talking montage the first idea keeps the picture by describing its shots, and that description is no longer counted as a clause added after the swap. |
| `ideas-own-ideas-coffee` | Their own three ideas on the same rows: a plain verdict each, against their call and the board. Since 11-11 round 3 the skill asks for lookalikes and "too few to judge" under three; this answer holds one lookalike for the miso latte, so `says-which-and-why` takes "too few to judge" as well as "worth making" there. |
| `ideas-rival-comments-gymshark` | A rival's comment asks: ideas in the askers' words, buy asks as buy-stage ideas, no generic-question idea, no invented counts. |
| `ideas-ad-find-gymshark` | Ad finds become ads in the ad's own format, backed by days running. |
| `ideas-live-getripping` | The live answer for an app-growth brand with no setup: tracked accounts' strongest posts, untracked discovery and the brand's own comment asks; setup skipped by the user; links come from the answer; the straight swap and three to five ideas per find. `straight-swap-first` reworded 11-11 (round 3): a comment-ask find is judged on answering the ask in the askers' words (the lead's call, as ideas.md "From comments"), the swap may put in what RIP gives where the find's want was (ideas.md "Adapt it"), and a Hindi hook is judged on its meaning; the old wording failed all three correct answers (review-2 §5). |
| `ideas-followers-asks-getripping` | "What do my followers keep asking for that I haven't made?" on the real demo1 answer: only the comments part is sent, each ask is marked made (their post linked) or not made yet, ideas answer the not-made ones in the askers' words. `made-or-not-made` reworded 11-11 (review 3): the broken done-for-you link is a site fix that Vamos's own answer says to check, so a reply that flags it to fix is as right as one that marks it "not made yet"; the old line failed that correct reply. |
| `ideas-worth-making-getripping` | Their own two ideas on the real demo1 "worth posting" answer: one ask, then a verdict from both sides per idea: "N of M beat their usual", the best 3 and worst 3 linked, "too few to judge" under three. |

Every ideas case carries `proposes-three-ideas` (11-11 round 3), so a run that stops without ideas no longer passes on vacuous graders. The ideas cases need `Bash` and `Write` for `scripts/filter.py`: run them with `--allow-tools Bash Write`. The filter itself is tested free with `python3 evals/ideas/test_filter.py` from the repo root.

The analyze cases need `Read` (the skill reads `references/structure.md`), so their `allowed_tools` is `[Skill, Read, Glob]`. The structures are listed from `get_workspace`'s `skills` and saved with `save_brain_file`, both free: `asks-to-save-structure` checks a `save_brain_file` call titled "Structure: …", and `no-unconfirmed-save` reads the trace and fails a reply that claims a save no call made. The four cases with rows carry their own `save_brain_file` mock answering `kind: skill`, as prod does for a save with `when_to_use`. The ideas cases with a Brain-file board and content-log's quiet week grade saves the same way. Content-log's board case checks the What works for me call itself (`saves-what-works`): on that long run the judge sees a cut trace, so a trace-read grader there failed a save it couldn't see. Loop's `saves-settings` checks the Vamos settings save.

| Playbook case | What it proves |
| --- | --- |
| `playbook-duolingo-tiktok` | A brand's playbook, organic only: counted traits, our usual (823,638.5 over 32) not Vamos's, plays for the user's app, no ads turn (the Brain save is left out of that check: a correct save ending "No Meta ads read." failed it in review 2), first lines written out (no "[funny line]" templates: Duolingo's hits are visual, so a first line is the opening shot and its on-screen text), and the same `plays-have-paste` and `page-built` as Grüns (run with `--allow-tools Bash Write`). Mock: a copy of the duolingo analyze mock. |
| `playbook-opusjake` | A creator's playbook: the comment-keyword path counted (38 of 40), the hits separated from the rig. `plays-have-paste` and `page-built` as Grüns (run with `--allow-tools Bash Write`). Mock: a copy of the opusjake analyze mock. |
| `playbook-unindexed-getripping` | An account Vamos hasn't indexed (no labels): asks to watch before naming hooks; usual 32,507.5. Mock: a copy of the getripping analyze mock. |
| `playbook-ads-gruns` | Ads only when asked: "checked N of M" (114), the rows ranked by `days_running` in code (16 days, two ads), no spend claims, the site in the ask, a Paste on every play (`plays-have-paste`: eval-3's replies scored 1.00 with none), and the page made as `playbook.html` (`page-built`; run with `--allow-tools Bash Write`, since without the grant the sandbox has neither and the skill rightly skips the page). Mock: **real**, Grüns' partnership ads, 2026-10-31 (15 credits, 22 ad rows; `mock-from-transcript.py write`, 2 ids remapped). |
| `playbook-unhappy-customers` | A competitor's complaints. **No mock yet** (`needs-live-mock`): the live run saves it; until then only the step graders count. |
| `playbook-notion-tiktok-instagram` | A brand on two platforms in one ask: one research ask names TikTok and Instagram, counted traits, our usual (TikTok 11,011.5 over 32, Instagram 30,702 over 26) not Vamos's, no keyword mechanic invented for a brand that has none, plays for RIP with first lines written out, and the same `plays-have-paste` and `page-built` as Grüns (added 11-12: a run cut the plays to the page and no grader saw it; run with `--allow-tools Bash Write`). Mock: **real**, the live demo1 run of 2026-11-11 (60 credits, the turn cap); the 80 cited rows are inlined because the live run read them from the file link, which a mocked run cannot fetch. |

## formats cases (2026-11-11)

| Case | Mock source | What it proves |
| --- | --- | --- |
| `formats-coach-new-over-crowded` | **assembled from a real Vamos run**: the 11-10 format-asks harness (Chat `run-asks.ts`, prod library, the pt-coach fixture "Baseline Strength", ask fit5). The answer text is the agent's own, with its process tags removed and its script canvas flattened to text; `data.formats` is built from the `sort_by: "plan"` result it read, one row per example in the FormatRow schema (views rounded as the plan printed them, `video_url` and `role` null, `cited` when the answer names the format) | Rising and white space rank above the crowded staples; Not for me, done and off-limits calls hold; angles rest on real proof |
| `formats-skincare-no-face` | **assembled**, the same way (fixture "Plain Barrier", ask fit5). Its "best example" links a profile | Face and claims limits gate; white space over staples; nothing rising said; numbers from answer and rows; no profile link |
| `formats-b2b-no-invented-stats` | **assembled**, the same way (fixture "Fieldnote", ask fit5). The answer invents "a third of the calls" and "60 seconds before retention drops" | Invented claims stay out; content rules hold in every angle; white space gets its slot |
| `formats-thin-answer-no-setup` | **real**, unchanged: `mock-library/poll-formats-skincare` (kit round 2, 2026-11-05, 1 credit), five ideas with no posts or numbers; the fresh-workspace mocks | Setup suggested, not run; nothing invented from a thin answer |
| `formats-live-getripping` | **real, live**: demo1 run on 2026-11-11 after Chat #1502 (`claude -p` via vamos-demo, Sonnet), one research ask with `include_data` and `data_scope: "turn"`, 19 credits. Format rows carry `status`, `niche_examples` and a playable `video_url` (cdn.lazylines.ai). 34 of 105 format rows and the 8 cited video rows, kept under the host's inline size | The real connector path |

Brand names in these cases are test fixtures; the tracked handles in their `get_workspace` mocks are placeholders. Each case's `get_workspace` is a `type: agent` mock that answers both the summary and the `file` reads.

The `hooks-live-getripping` case holds real Vamos data from `vamos-demo` (a Free workspace set up as the test brand @getripping). Its `chat_completion_poll` is the answer to the round-3 ask of 2026-11-11, by views over 90 days and across the niches that sell to app founders (60 credits, 15 rows); the first live run's 60-day niche pool (37 credits) was tips and sponsored posts, and its lines read as advice (Levi: "low not viral"). `get_workspace` is the same workspace read before that run (voice guide, settings, an empty board; no "Things you've said" file).

The hooks cases' `kept-hooks-shape` also accepts a proven hook from the skill's own `references/hooks.md`, named by its @handle and the numbers given there: when fewer than three of a niche's rows can be borrowed (tips, advice, a story only that creator lived), the skill takes a Shape's sentence, and those carry a handle and views in the reference, not a link. The user needs to know what each hook is built from (bar: every hook names its source). A kept hook with no source still fails.

`numbers-from-the-answer` accepts those reference numbers too, so the two graders agree. `no-unconfirmed-save` counts a Brain file save as confirmed when `save_brain_file` comes back with an action: the shared mock answers `"created"`, and the shared Saves rule reports a save on its action. Before 2026-11-12 its premise said no answer in the run confirms a save, which stopped being true when saves moved to `save_brain_file`: on origin/main `4ee0299`, unchanged, the coffee case saved that way, reported it, and failed 3 of 3.
