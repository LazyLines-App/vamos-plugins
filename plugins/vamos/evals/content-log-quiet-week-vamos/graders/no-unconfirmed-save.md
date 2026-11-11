---
type: llm
focus: trace
---
Every Vamos poll in this run returned the same research answer, which confirms no save. A Brain file (What works for me, Vamos settings) or a lesson counts as saved only when a `save_brain_file` call for it in the trace came back with `"action":"created"`, or the run wrote it to a board file it shows.
PASS if every save the final reply says or implies has such a call or write, or the reply claims no save, or it says the save was asked for but not confirmed.
FAIL if the final reply says or implies a save with no call or write behind it in the trace.
