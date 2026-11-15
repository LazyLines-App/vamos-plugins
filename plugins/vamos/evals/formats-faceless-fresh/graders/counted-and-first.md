---
type: llm
---
The format rows carry no per-format skincare count (`niche_examples` is null, which the card says as "not counted"); Vamos's answer text gives some (GRWM Routine: 129 uses, 56 creators; Right vs Wrong: "90 skincare uses in 60 days"), and the rows mark Right Vs Wrong as white space (`plan_group`).
PASS if (1) each ranked format says how many skincare posts use it, from the answer or the rows, or says plainly that it wasn't counted, never a number found in neither; and (2) the reply makes plain which one to film first (rank 1, with why it's first for them).
FAIL if a ranked format gets a usage count found in neither the answer nor the rows, or no single first pick is clear.
