# Maintaining the plugins

This repo is one marketplace, `vamos-plugins`, with two plugins:
- `vamos` (Content System): for creators, coaches and service providers who film their own content. It is the one in Claude's plugin directory.
- `cracked-marketer` (Cracked marketer by Vamos): the marketing hire for a brand or startup. It holds the nine shared Content System skills plus its own, and installs from this marketplace only.

## Making a change

1. **Start from the root cause.** Trace the bad output to the line that caused it and fix it there. Often the fix is a deletion.
2. **Edit shared parts once.**
   - `src/` holds the Vamos block, the board, `textstats.py` and the page kit.
   - `plugins/vamos/skills/<name>` is the one source for the nine shared skills: setup, playbook, formats, hooks, ideas, script, content-log, loop, analyze.
   - Run `python3 scripts/build-skills.py`. It copies `src/` into each skill and each shared skill into `plugins/cracked-marketer/skills/`, with `/vamos:` turned into `/cracked-marketer:`.
   - Where a shared skill's job differs for a brand, Cracked marketer's copy differs only through `src/cracked-marketer/<skill>/`: `EDITS.md` holds each edit as Content System's exact words (`~~~old SKILL.md`) and Cracked marketer's (`~~~new`), and any other file there is added to Cracked marketer's copy only. The build fails when an edit's old words are gone.
   - Cracked marketer's own skills live only in `plugins/cracked-marketer/skills/`. The build refreshes only the Vamos block between its markers in each, and checks their last line and links.
3. **Run what the change needs.**
   - Always: `python3 scripts/build-skills.py --check` prints `ok`. It fails if any copy drifts from its source.
   - A changed skill script: its test in `evals/scripts/` (`python3 evals/scripts/test_count.py` for content-log's `count.py`; free, no network).
   - A changed description: rerun the routing test (`python3 evals/routing/route.py evals/routing/cases.tsv`, about $0.05 a case).
   - A changed skill: replay its saved cases with `claude plugin eval` on mocks, with the old version as the control. Mocks are written from real saved Vamos answers, so a replay spends no credits and a change in score is the skill, not the data. Cases and mocks live in `plugins/vamos/evals/` (the routing test stays in the root `evals/routing/`). Run `claude plugin eval .` from inside the plugin's folder, with the `--allow-tools` its eval note names: run from the repo root, a case's saved files aren't found and every file grader fails.
   - A new skill: a cold review by a fresh Opus agent, then one fix round.
   - Both plugins: `claude plugin validate .` and `claude plugin validate ./plugins/<name>`.
4. **Every check traces to the skill's core check.** Each grader names the bar item it tests: what the user needs at that step. A check no need asks for goes. Length, language and format limits come from what the user does with the answer (a brief read on a phone, a line said in 3 s), with the reason in the case's README line.
5. **A bug a user hits becomes a saved case,** so the replay catches it next time.
6. **Commit** with the root cause in the message.

## Releasing

1. Bump `version` in the plugin's `.claude-plugin/plugin.json`. Without a bump, installed copies don't update. A change to a shared skill bumps both plugins.
2. Add a line per change to `CHANGELOG.md`, under the new version.
3. A renamed command keeps working under its old name for one release: keep a short skill under the old name that runs the new one, and remove it the release after.
4. `claude plugin tag plugins/<name>` makes the release tag and checks plugin.json against the marketplace entry.
5. Push only on Levi's word.
6. Content System only: resubmit it to Claude's plugin directory after the push. Cracked marketer is not in the directory.

## Who says yes

- After launch, a bug fix that passes every check above can go out on Levi's standing OK. Send him one line afterwards: what broke, the fix, the checks.
- New or changed skills always wait for Levi's look.
- Pushes, PRs and directory submissions wait for his word.
