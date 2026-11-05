# End-to-end skill runs

Each row of `cases.tsv` is a skill and a plain ask with every input given. `e2e.py` runs each one headless in Claude Code with only this plugin and the Vamos connector (`vamos-mcp`, signed in) loaded, then records:
- the skill that loaded;
- the exact request sent to Vamos;
- the credits it used;
- the final answer.

The results are in `result-<skill>.md`.

    python3 evals/e2e/e2e.py evals/e2e/cases.tsv

It spends real Vamos credits in the signed-in workspace, so run only the read-only skills here. `write-like-me` saves a voice, and `content-system` sets up a workspace and a routine; test those in a demo workspace.

**2026-11-05, prod connector, `Levi` workspace:** 5 of 5 loaded the right skill and sent one plain, fully scoped request.

| Skill | Credits |
|---|---:|
| viral-research | 20 |
| competitor-research | 44 |
| creator-research | 60 |
| video-breakdown | 9 |
| content-strategy | 8 |

Total: 141 credits and $1.38 of Claude.
