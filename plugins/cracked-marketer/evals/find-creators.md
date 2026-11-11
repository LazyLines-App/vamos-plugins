# find-creators cases

Four cases replay a real Vamos answer: three saved on 2026-11-09 and one from the demo workspace's live run on 2026-11-11 (test brand @getripping). The fifth is a fresh workspace. Every bio email in the mocks is scrubbed to `handle@example.com`, and each prompt says so, because Sonnet won't build a sheet on placeholder emails it hasn't been told about.

| Case | Tests |
|---|---|
| `find-creators-budget-app` | a no-email creator keeps no email, an unwatched format isn't claimed, a first message per creator, nothing sent |
| `find-creators-creatine-pouch` | all 7 in the sheet, near misses kept off the main list, the rival deal asked for and flagged |
| `find-creators-getripping-live` | the shortfall said plainly (1 of 25), rival-product sellers not picked, rival-tool posters flagged before paying |
| `find-creators-not-set-up` | setup is started first, once |
| `find-creators-prayer-app` | all 24 in the sheet, no invented on-topic counts, repeats not counted, at most 3 turns |

The sheet graders read the skill's `Write` call, and `Write` is a gated tool, so run every case with `--allow-tools Write`. Without it, the reply says file writing is disabled and the run tests nothing about the sheet. Run from `plugins/cracked-marketer`:

    claude plugin eval . --case 'find-creators-*' --runs 1 --model sonnet --allow-tools Write --no-publish --trust-plugin --json /tmp/fc-eval/run.json
