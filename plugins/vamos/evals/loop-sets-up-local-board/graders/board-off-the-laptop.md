---
type: llm
focus: trace
---
The user's board is a local file, vamos/board.md, and they want runs to happen with the laptop closed. A cloud scheduled run starts from a fresh copy and cannot read files on the laptop. No Notion or Google tool is connected in this session.
PASS if the assistant moves the board somewhere a cloud run can read before scheduling (for example it saves the board as the Brain file Vamos board with `save_brain_file`, or tells the user to connect Notion or Google Sheets first and holds the schedule until then), or it clearly tells the user that a cloud run can't see the local file and offers only a run that can.
FAIL if it sets up or tells the user to set up a cloud scheduled task that reads vamos/board.md from the laptop.
