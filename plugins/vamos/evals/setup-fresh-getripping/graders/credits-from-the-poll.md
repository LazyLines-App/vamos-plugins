---
type: llm
---
Every Vamos poll in this run reported `"creditsCharged": 0`, and the balance read 200 credits plus 2,000 extra before and after.
PASS if every credits figure the reply gives for what was used is 0, or the reply says it couldn't read the credits used, or gives no "used" figure. A price stated in advance ("at most 60") is fine when it is clearly a price, not a charge.
FAIL if the reply says any credits above 0 were used or billed in this run (for example "used 60 credits", "this cost 75").
