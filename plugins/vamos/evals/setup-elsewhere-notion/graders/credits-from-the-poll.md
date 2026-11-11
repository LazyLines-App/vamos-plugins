---
type: llm
---
In this run the research poll reported `"creditsCharged": 32` and the balance read 200 credits.
PASS if every credits figure the reply gives for what was used is 32 (or 0 for setup steps that were not run), or the reply says it couldn't read the credits used, or gives no "used" figure. A price stated in advance ("at most 60") is fine when it is clearly a price, not a charge.
FAIL if the reply states a used or billed figure that no poll showed (for example 60, 47, 75, 120).
