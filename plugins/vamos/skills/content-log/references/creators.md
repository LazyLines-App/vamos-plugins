# Creators' results

For a brand that pays creators. The user's question is which creator and which hook won, what each view cost, and who gets the next videos.

## What to read first (free)

- **"Creator program: [brand]"** (`get_workspace` with `file`): each creator, their deal per video (base and bonus thresholds), the videos due and by when, and whose account each posts on.
- **The briefs doc** (as the brief skill keeps it): the hooks each creator was given, and the draft reviews under each brief, which are the revision rounds.
- **The board's Hooks rows** for the earlier tries of each hook.

## Which posts are the brand's

A post is "ours" when the user links it, or the row is a paid partnership with the brand, or its caption tags the brand. Ask about any you can't place rather than guess, and tag every post the user linked, whatever the period. Each one is tagged in `tags.json` as `{"ours": true, "creator": "@handle", "hook": "<the brief's hook it used, or its own opening>"}`, on the creator's account or the brand's.

Write `pay.json` from the program file: `{"@handle": {"base": 60, "bonus": [[12600, 60], [42000, 120]], "due": 4}, "pool": 500}`, the bonus as views reached and dollars added, and `"pool"` when the program caps the bonuses. Add `"sales"` or `"signups"` only from a number the user gave (their code or link's count). A deal that isn't base-plus-thresholds gets `"paid"` on each post's tag instead.

## The numbers

`count.py <rows> --since [start] --tags tags.json --pay pay.json` does them all:
- **Each post** against the usual of the account it went up on: the creator's own posts for their account, the brand's for the brand's. Posts made for the brand never count toward a usual. Under 3 days old, it's too early.
- **Where a miss broke**: under 1,000 views the opening failed; 1,000 to 10,000, people left before the product; past 100,000, only sales or signups say whether the product moment worked.
- **Cost per 1,000 views** from what the deal pays for that post, and per creator: posted against due, how many beat their usual, paid against views.
- **Hooks across creators**: tries, how many beat the usual, the best, and dead at 5 or more tries with none past 10,000 views.
- **The label**: a post for the brand with no paid-partnership label and no #ad is flagged.

Sales, signups and revenue come only from the user's own numbers, with where they came from. Without them, say the read is on views.

## The Creators section, in order

1. **The call, one sentence:** who to double down on and who to drop, with the number behind each. "Dana: 2 of 3 above her usual at $4.10 per 1,000, so she gets 4 next week; Lee: 0 of 3, all under 1,000 views, so his last video waits on a new opening or he stops."
2. **Each creator:** each post's views against the usual with its age when read, where a miss broke, what it cost per 1,000 views; then posted against due, revision rounds from the briefs doc, and paid against views.
3. **Hooks:** the top three across creators with their numbers, the dead ones, and the rest still being tried.
4. **Next brief, per creator kept:** the one thing it changes, and why in a line. A winner (5× its account's usual, or comments asking where to get it) goes to every kept creator, with only its subject swapped, as on the Repeat list. A miss changes only the part its band names: a new opening under 1,000, the product earlier at 1,000 to 10,000.
5. **Labels to fix**, if any: the creator and the post, for the user to ask them.

Drop or keep is the user's call: give the number behind it. One post never drops a creator; the program reads reliability and drafts at day 14.

## Record

Each hook's tries go on its Hooks row (creator, views, ×, age when read). Add a dated "Results" part to "Creator program: [brand]" with the call, each creator's line and each kept creator's next-brief change, saved whole with `save_brain_file`, so the next brief starts from it.
