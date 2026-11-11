# End-to-end skill runs

Each row of `cases.tsv` is a skill and a plain ask with every input given. `e2e.py` runs each one headless in Claude Code with only this plugin and a demo Vamos connector loaded, then records:
- the skill that loaded;
- the exact request sent to Vamos;
- the credits it used;
- the final answer.

The results are in `result-<skill>.md`.

    VAMOS_CONNECTOR=vamos-demo python3 evals/e2e/e2e.py evals/e2e/cases.tsv

The connector name comes from `VAMOS_CONNECTOR` (default `vamos-demo`; `vamos-demo2` is the fresh account), and any name that isn't a demo connector is refused. Each run starts in `~/vamos-demo-test` (`VAMOS_DEMO_DIR`), where the demo sign-ins live, so a live run never reaches a real workspace. Results land in the folder you run it from.

It spends real Vamos credits in the signed-in workspace. Since 0.2.0 every skill but creator-research writes to the workspace (Brain files, tracked accounts, the voice) or to a board, so run these only in a demo workspace, never one with a real brand in it. The table below is from 0.1.0's skills.

**2026-11-05, prod connector, `Levi` workspace:** 5 of 5 loaded the right skill and sent one plain, fully scoped request.

| Skill | Credits |
|---|---:|
| viral-research | 20 |
| competitor-research | 44 |
| creator-research | 60 |
| video-breakdown | 9 |
| content-strategy | 8 |

Total: 141 credits and $1.38 of Claude.
