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
- **Each post** against the usual of the account it went up on: the creator's own posts for their account, the brand's for the brand's. Posts made for the brand never count toward a usual. Under 7 days old, a post that already beats it is "so far" and one that doesn't is too early.
- **Where a miss broke**: under 1,000 views the opening failed; 1,000 to 10,000, people left before the product; past 100,000, only sales or signups say whether the product moment worked.
- **Cost per 1,000 views** from what the deal pays for that post, and per creator: posted against due, how many beat their usual, paid against views.
- **Hooks across creators**: tries, how many beat the usual, the best, and dead at 5 or more tries with none past 10,000 views.
- **The label**: a post for the brand with no paid-partnership label and no #ad is flagged.

Sales, signups and revenue come only from the user's own numbers, with where they came from. Without them, say the read is on views.

## The Creators section, in order

1. **The call, one sentence:** each creator's call (more, wait or drop) with the number behind it. A creator whose posts are still too early waits, with what has settled so far. "Dana: 2 of 3 above her usual at $4.10 per 1,000, so she gets 4 next week; Lee: 0 of 3, all under 1,000 views, so his last video waits on a new opening or he stops; Sam: 1 of 1 judged above his usual so far at $9.80 per 1,000, his second too early, so he waits until it's 7 days old."
2. **Each creator:** each post's views against the usual with its age when read, where a miss broke, what it cost per 1,000 views; then posted against due, revision rounds from the briefs doc, and paid against views.
3. **Hooks:** the top three across creators with their numbers, the dead ones, and the rest still being tried.
4. **Next brief, per creator kept:** the one thing it changes, and why in a line. A winner (5× its account's usual, or comments asking where to get it) goes to every kept creator, with only its subject swapped, as on the Repeat list. A miss changes only the part its band names: a new opening under 1,000, the product earlier at 1,000 to 10,000.
5. **The code ask, written out in full,** for each winner on a creator's own account, whether or not ads are on in Vamos settings (that setting is for the Meta Ad Library read and the Turn into an ad list; this message is part of paying creators): the message the user sends so it runs as a Spark ad (TikTok) or a partnership ad (Instagram) from the creator's handle, with the steps and why it's safe, for the window and fee the program agreed. When it agreed none, write it anyway with a `[$ for 60 days]` slot and say ad use isn't in their terms yet. They paste the code in their own Ads Manager.
   > Hi Dana, your paycheck video is our best yet, so we'd like to run it as a Spark ad from your account for 60 days, for the $22.50 we agreed. On that video: tap ⋯, then Ad settings, agree to the terms, turn on Ad authorization, choose 60 days, tap Generate and send me the code. It covers that one video only. We get no login and can't post, edit or message from your account, the ad shows your handle and TikTok marks it Sponsored, and it ends by itself after 60 days.

   On Instagram the steps are: on that reel, tap ⋯, then Partnership label & ads, turn on Get partnership ad code, tap Copy and send it. Its code has no end date, so the line becomes "we'll stop it on day 60". A window TikTok doesn't offer (90 days, say) asks for 365 days and says "we'll stop it on day 90". A winner on the brand's own account needs no code.
6. **Labels to fix**, if any: the creator and the post, for the user to ask them.

Drop or keep is the user's call: give the number behind it. One post never drops a creator; the program reads reliability and drafts at day 14.

## Record

Each hook's tries go on its Hooks row (creator, views, ×, age when read). Add a dated "Results" part to "Creator program: [brand]" with the call, its cohort grid (when it has one) brought up to date on posted, best video and stage, each creator's line, each kept creator's next-brief change and each code asked (the creator, the video, Spark or partnership, the window, the day asked), saved whole with `save_brain_file`, so the next brief starts from it.
