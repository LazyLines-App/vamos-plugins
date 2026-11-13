# The content log

## The numbers

`scripts/count.py` does all of these from the rows. By hand, the rules are:
- **Usual:** the median views of their posts at least 7 days old, per account and platform, since views still climb before then. Set aside, each with a line: boosts (likes under 0.5% of views, or tagged paid) and reposts (the same caption within 2 s of the same length as an earlier post). A re-cut counts. A creator's posts are against that creator's usual.
- **× usual** for each post, with its age when read. A post under 7 days that already beats the usual is "N× so far" and can go on Repeat or the ad list; one that doesn't is "too early". Neither counts toward the hit rate, a pattern or a lesson until it's 7 days old.
- **Hit rate:** the share of their last 20 judged posts above 1× and above 2×, and the median ×. One row a week on the Reviews tab, so it shows as a line over time.
- **Private numbers** (saves, reach, watch time, profile visits, link clicks): only what an Insights screenshot shows, marked "from your screenshot" with its date.

## Each post on its job

Each post's stage (reach, trust, buy) comes from the Marketing plan, and it's judged on that stage's number against posts of the same stage: reach on × usual; trust on saves and shares per 1,000 views; buy on profile visits, link clicks and buying-intent comments per 1,000 views. Without a screenshot, trust posts are judged on shares and buy posts on comments; say so in one line.

## The patterns

Tag every post on its hook shape ("Claude just killed [X]", a number first, a question), format, angle (the idea underneath, in four words), first frame (a face, text, the product, a result), stage and creator; `count.py` adds length. Each pattern reads "N of M above usual, median ×, against N of M under it", over posts at least 7 days old; a younger one is named beside it as pending, never as a miss. Under 3 posts is a Hunch.

## The report, in order

1. **The finding** (SKILL.md step 4).
2. **Last review's predictions, checked:** what it said would happen, and what did. One that rests on a post too early to judge stays open: say so, and it goes in this review's predictions to check next time.
3. **The three lists** (SKILL.md step 4).
4. **Each post:** thumbnail, ×, views with its age when read, its job's number, then **Seen** (the hook, first frame, length, format, what the comments asked) beside **Guess** (why, marked as a guess). Posts too early to judge are listed as such.
5. **Competitors:** their posts at 2× or more in the period, and what they share.
6. **Ads** (when ads are on): with an export, their account's week first, from `ads.py`: spend, CPA and ROAS against last week, the top ads, risers and fallers, the words in their ad names that win on spend and CPA, and each concept that ran with its CPA against the median. Then what tracked brands started, kept and stopped in the Meta Ad Library.
7. **Lessons:** new and changed, each with its status.
8. **Next:** what the next ideas run makes more of, stops and tests, and the predictions for next time.

A quiet period is reported as one: no post is a winner or a flop when nothing was posted. Views with no profile visits is a profile or call-to-action problem, not a content one.

## Lessons

One row per lesson on the board's Lessons tab: the lesson with its numbers, the evidence (links, views, ×, date read), how many posts, its status, its action.
- **Hunch:** under 3 posts. **Testing:** being tried on purpose. **Confirmed:** 3 or more posts from different weeks. **Dropped:** a test that failed twice.
- A post counts toward a lesson only when it plainly fits; one you'd call a judgment call is named beside the lesson and left out of the count.
- A lesson moves only when a new post old enough to judge backs it.

## What works for me

After each review, rewrite the Brain file from the Confirmed and Testing lessons, under about 400 words: their usual and hit rate with dates, what to make more of, what to stop, what's being tested.
