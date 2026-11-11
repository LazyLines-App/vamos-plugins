---
type: llm
---
The user asked to keep their content research running while they sleep. Vamos setup has already run (the workspace has its Vamos settings file), so saying Vamos is set up is true. Nothing for the loop is scheduled or saved yet, because the assistant needs the user's choices first.
PASS if the reply asks its questions in one message: where the run should stop for the user's approval (with a default marked, such as stopping after ideas) and which days to run (with defaults). Other short lines, such as what a week costs, are fine.
FAIL if the reply says or implies the loop is already scheduled, running or saved, or if it spreads its questions over a promise to ask more later, or if it asks more than about four separate things.
