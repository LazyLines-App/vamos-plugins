# winning-ad-ideas cases

Five asks for Meta ad concepts. Each case's `mocks/vamos/chat_completion_poll.md` is a saved Vamos answer; `getripping-live` is the live demo1 run (the test brand RIP, 2026-11-11, 23 credits). The three LLM graders (answer-key, distinct-pictures, honest-claims) need an Opus judge: Sonnet judges failed all 15 on this suite, a correct reply included.

    claude plugin eval . --case 'winning-ad-ideas-*' --model sonnet --runs 1 --ablation none --judge-model opus --no-publish --trust-plugin --json /tmp/wai/run.json

| Case | Ask | What it turns on |
|---|---|---|
| `winning-ad-ideas-getripping-live` | RIP, from AI app builders | named brands with no ads, catalog ads, unread pictures kept from their words |
| `winning-ad-ideas-greens-gruns-ag1` | a greens powder against Grüns and AG1 | only three ads past 30 days; formats the answer doesn't state |
| `winning-ad-ideas-medicube-device` | a microcurrent device from Medicube's ads | every concept a video, copies count once, fewer than 10 sources |
| `winning-ad-ideas-skincare-ordinary` | a barrier serum against The Ordinary | retailer catalog ads, organic posts aren't sources |
| `winning-ad-ideas-supplements-category` | creatine gummies, the category | no rows and no per-brand counts in the answer |

## Grader rewordings

- 2026-11-11, `getripping-live` answer-key: the inventory left out the 32-day Replit video (1866623877660944), Devs.ai's "2 ads, 3 picture assets" and the other stated copy counts, so a reply quoting them failed for "a count not in the answer". It now lists every ad and count the answer states. "Hatchable (three, one template)" became "none catalog", as the answer says.
- 2026-11-11, `greens-gruns-ag1` answer-key, item 3: "one from a creator ad is a video" failed a static from the 18-day gift ad, whose format the answer never states. An ad with no stated format now takes any format the concept labels "format not stated"; the named videos still must stay videos.
- 2026-11-11 (round 2), `getripping-live` answer-key: it gave every Buildify ad the "WARNING" body, but the 396- and 196-day rows open "Embark on…" and the 351-day row "Ready to revolutionize…", so a reply quoting the 396-day ad's real copy failed (eval-3). Each body is now listed by days. Item 6 gains Levi's 11-11 call: an ad whose words the answer gives isn't set aside for its unread picture.
- 2026-11-11 (round 3), `getripping-live` answer-key: an Opus judge failed "116 days, static, 2 variants" as a count not in the answer, but the answer says "2 variants reported", and read item 5 as asking a reason for 10 concepts. The inventory now gives the 2 variants, and item 5 says 10 needs no reason.
- 2026-11-11 (round 3), `greens-gruns-ag1` answer-key: an Opus judge failed "runs as 9 ads" (the answer: "One creative runs as 9 ads") and the 148-day row's own body "90 Days of AG1. Lock In. Level Up." as not in the answer. The inventory now carries both, and (after eval-6) the gut ad's "11 ads" and Grüns' "100 pulled ads", which the answer also states. The format items are unchanged: "DCO" or "creator ad" given as a format still fails.
- 2026-11-11 (review 3), `getripping-live` answer-key: an Opus judge failed "Hercules, 5 records, 4 of them identified" as a count not in the answer, but the answer says Hercules' "set contains 5 catalog ads" and links four. The inventory now gives the 5. Catalog ads used as a source still fail.
