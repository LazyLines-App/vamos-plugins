# Skill routing check

Does a plain ask load the right Vamos skill? Each row of `cases.tsv` is the expected skill and an ask taken from a planned video. `route.py` runs each ask headless in Claude Code with only this plugin loaded (`--setting-sources project`, no other MCP servers, only the Skill tool allowed) and records which skill Claude loads.

    python3 evals/routing/route.py evals/routing/cases.tsv

About $0.06 per case. 2026-11-05: 17 of 17 (`last-run-2026-11-05.txt`). Run it after any description change.
