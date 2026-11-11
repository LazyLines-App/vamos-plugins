# startup-deals cases

Five founders, made up, because the job turns on private facts (money raised, team size, country) no public account shows. Each case's graders hold the bar it tests, and each names the founder's need behind it (MAINTAINING item 4).

The plugin has no Vamos connector, so there are no mocks. Each case checks that the skill fires, then grades the answer.

| Case | Founder | Web |
|---|---|---|
| `startup-deals-bootstrapped-us` | solo, no money raised, Delaware C-corp | none: answers from the dated list |
| `startup-deals-yc-seed-us` | YC batch, $2.5M seed, 8 people, SF | live: run with `--allow-tools WebSearch WebFetch` |
| `startup-deals-berlin-preseed` | €400K angels, 3 people, Berlin GmbH | none |
| `startup-deals-series-b-uk` | Series B, $30M, 60 people, London | none |
| `startup-deals-asks-first` | nothing given | none |

Graders, with the need each serves: `skill-fired` (the ask reaches the skill); `asks-the-five` and `no-total-yet` (a founder who gave nothing is asked, and is not handed programs or a price that don't fit them); `matches-and-traps`, `country-rules`, `outgrown-programs` (the founder applies only to programs they can get into, and is told which popular ones won't work); `total-and-freshness` (the kit's total uses official prices only, and the founder is told the list wasn't re-checked today); `rechecks-live` (with the web on, each program shown is re-read on its own page).

2026-11-11, moved from Cracked marketer. Cut: `no-vamos-research` (the plugin has no Vamos tool to call) and `no-secondhand-total` (a regex on three sums from the old Pro-plan total; `total-and-freshness` already tests the need, a total with no secondhand price, and the sums changed when the Vamos plan became an assumption). No length limit: the founder reads the list and applies, so the skill's own example sets the size and no grader counts words.

The skill is standalone (not in a plugin), and `claude plugin eval` loads plugins, so to run these cases make a temp plugin: a folder with `.claude-plugin/plugin.json` (name `startup-deals`), this skill copied to its `skills/startup-deals/`, and this `evals/` folder copied to its `evals/`. Then, from that folder, the four no-web cases without any `--allow-tools` (their freshness graders assume no web tool), the live one with it. The `--case` glob takes no brackets or braces, so name each case:

    claude plugin eval . --case startup-deals-bootstrapped-us --runs 1 --ablation none --no-publish --trust-plugin --json /tmp/sd-eval/run.json
    claude plugin eval . --case startup-deals-yc-seed-us --runs 1 --ablation none --allow-tools WebSearch WebFetch --no-publish --trust-plugin --json /tmp/sd-eval/live.json
