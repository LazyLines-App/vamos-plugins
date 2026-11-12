# Cracked marketer's own words in the shared skills

Where a brand's job differs, Cracked marketer's copy of a shared skill has its own words (`src/cracked-marketer/<skill>/`). These cases test those words; Content System's cases in `plugins/vamos/evals/` test the rest. Run from this folder, one `--case` glob at a time:

    claude plugin eval . --case 'formats-ads-*' --model sonnet --runs 1 --ablation none --judge-model opus --allow-tools Bash Write --no-publish --trust-plugin --json /tmp/cm-shared/formats.json

| Case | Ask | What it turns on |
|---|---|---|
| `formats-ads-supplements` | which Meta ad formats work, creatine gummies | the ad read alone; formats run by 2+ advertisers, catalog ads set aside; who makes each; long-running is not proof |
| `formats-ads-skincare-both` | which formats to make, a skincare brand with ads on and two creators | the formats ask then the ad read in one chat; one advertiser's ads rank no format; each video format's job and maker; a face limit is the team's |
| `hooks-ads-skincare` | hooks for an approved idea a creator will film | the one ask includes the ads; an ad's line with its link and days running, never views; the 28-day ad isn't called 30+; Next is brief |
| `setup-brand-no-talking` | set up a brand nobody talks for on camera | the research turn reads the site, captions and Meta ads, rebuilds the voice from how they write, and Vamos settings says the voice is written |
| `ideas-next-brief-getripping` | what to post, when UGC creators film most videos | the approve line and Next name brief |

A mock gives the same saved answer to every poll, so where a run reads posts and ads (the formats asks, the hooks ask) the mock joins two real answers in one; each prompt's description names its sources.
