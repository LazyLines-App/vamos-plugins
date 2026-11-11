# Where creator-program's eval mocks came from

| Mock | Source |
| --- | --- |
| `mocks/vamos/*` (suite defaults) | Byte copies of `plugins/vamos/evals/mocks/vamos/` (see that README for each one's source) |
| `creator-program-app-no-winner/mocks/vamos/chat_completion_poll.md` | **Real**: a connector answer, 2026-11-09, to "Who already wins with UGC in this category?" for a client's Christian iPhone app that locks the phone until you pray (59 credits, 381 s). Two creator emails removed; run and chat ids made up |
| `creator-program-dtc-shop/mocks/vamos/chat_completion_poll.md` | **Real**: the same ask, 2026-11-09, for a client's liposomal creatine pouch (31 credits, 253 s); ids made up |
| `creator-program-price-a-creator/mocks/vamos/chat_completion_poll.md` | **Assembled from real reads**: the same file as `plugins/vamos/evals/analyze-profile-opusjake` (@opusjake's 40 posts, vamos-research `fetch_link`, 2026-11-10 11:16 UTC) |
| `*/mocks/vamos/get_workspace.md`, `get_credit_usage.md`, `create_chat.md` (the other four cases) | **Derived** from the connector code: the vamos mock library's fresh workspace, Free 200 credits and fresh chat |
| `creator-program-rip-live/mocks/vamos/*` | **Real**: the step-4 live run on the demo workspace (test brand @getripping), 2026-11-11: the one category turn (33 credits, 200 rows), `create_chat`, `chat_completion_start`, and the real `get_workspace` and `get_credit_usage` reads. Signed file-link parameters scrubbed. The rows file it fetched is not mocked |
