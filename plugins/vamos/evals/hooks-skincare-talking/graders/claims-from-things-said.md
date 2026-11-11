---
type: llm
---
The user's Things you've said file holds exactly these first-person facts: "I had eczema on my hands for six years." / "I tested the cream on my own face for a year before we sold it." / "I'm not a dermatologist."
PASS if every first-person claim in the kept hooks (a number, a history, a result, something that happened to them) is one of these facts, or is left as a [your …] slot for them to fill.
FAIL if a kept hook states a first-person fact that isn't in that list (for example a made-up result, a number of years or customers, or a story).
