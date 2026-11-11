# Page kit

One HTML file that every page-making skill fills with data. No build step, no external scripts, fonts from Google Fonts only.

| File | What it is |
|---|---|
| `page.html` | The template. Its `<script type="application/json" id="data">` block is the only part a skill changes |
| `fill.py` | In a skill it's `scripts/fill.py`, and `page.html` is `assets/page.html`. `python3 scripts/fill.py data.json out.html [--embed]` puts the data in and, with `--embed`, inlines every image |
| `samples/*.json` | Local test data, one per page, kept out of git |
| `shots/` | Each sample at 1280 and 390 px, light and dark; the gap matrix; four motion frames per page (t = 0, 0.8, 1.8, 3.5 s) |

## How a skill fills it

1. Map the Vamos rows into the JSON below. Keep the numbers as they came: views, `outlier_score` and dates from the same row, never rounded or invented. Date everything with `as_of`.
2. Write the JSON to a file and run `python3 scripts/fill.py data.json out.html --embed` from the skill's folder. Without Python, copy `page.html` and replace only the text inside the data block, escaping `</` as `<\/`.
3. Publish the result as an Artifact. Run the checks first.

## Media

- In the data, keep the `cdn.lazylines.ai` links (`prod/instagram/THUMBNAIL/<id>.jpg`, `prod/tiktok/AUTHOR/<handle>.jpg`, and so on). Never a signed CloudFront link: it dies in about 102 minutes.
- Artifacts block remote images and video. In Claude Code, run `fill.py --embed` before publishing: it turns every `thumbnail`, `avatar` and `poster` into a `data:` URI and drops the field when a download fails (some thumbnails answer 403), so the card falls back to its image-free version.
- `video` (the first example on a format card) is kept as a link. It plays when the page is opened from disk. In an Artifact it shows its poster and "Watch on Instagram ↗" unless you publish the MP4 beside the page through `files` and set `video` to that relative path. MP4s run 2 to 3 MB, so publish only the top three.
- In claude.ai, where there's no shell, leave the links in: images fail, and every card falls back to its text version.

## Data

Every page takes the common fields. `?` means optional.

| Field | Type | Notes |
|---|---|---|
| `page` | `setup` · `playbook` · `formats` · `ideas` · `content-log` · `analyze` | Picks the layout |
| `title`, `title_pixel?` | string | Line one in Inter; line two in the orange pixel font |
| `lede?` | string | One or two sentences under the headline |
| `as_of` | `YYYY-MM-DD` | The date the data was read; printed in the receipt |
| `counters` | `[{value, label, decimals?, suffix?, prefix?, accent?}]` | Up to four. `suffix: "×"` for multiples. One `accent` (orange); the last one if none is set |
| `receipt` | `[string]` | Printed as "Read from Vamos on 10 Nov 2026 · …". Real counts only |
| `next` | `{command, says}` | The footer: "Next: `/cracked-marketer:formats` ranks the formats…" with a Copy button that copies `command` |
| `sample?` | string | A line under the receipt, for sample data |
| `titles?` | `{key: string}` | Renames a section (keys below) |
| `doc_title?` | string | The tab title; defaults to the two title lines |

**Post** (used everywhere): `{url, handle, views, x?, date?, thumbnail?, avatar?, hook?, caption?, platform?}`. `x` is `outlier_score`, the post against its creator's usual: 5 and up is an orange "win" badge, 2 to 5 a white "kept" one, under 2 no badge. With no `thumbnail`, the card shows `hook` (or the caption's first line) instead.

**Format**: `{name, about, where: niche|next_door, where_label?, stage?, niche_uses?, creators_5x, examples_total?, median_x?, beats[3-5], film?, yours?, examples[post + video?]}`. Ranked as given. `stage` is the row's `status` (early and trending show in orange). `niche_uses` is how many posts in their niche use it (the row's `niche_examples`), the card's big number; `null` prints "not counted", and without the field the big number is `creators_5x`. `creators_5x` counts unrelated creators at 5× or more among the examples read; `median_x` and `examples_total` are the library's. The card shows three examples and the formats header up to five; the first plays when it has `video`.

**Hook**: `{hook, shape, yours, post}`. `shape` is plain words (Contrarian, POV, Problem callout…).

**Next post**: `{title, why?, hook?, steps?[], post?}`.

| Page | Its fields (section keys in brackets) |
|---|---|
| setup | `set[{title, value?, detail?, accounts?[{handle, avatar?, followers?, url?}], lines?[], link?{url, label}, change?}]` [set], where `change` is only the words to say (the page adds "To change it, say:" and the quotes), `set_sub?`, `skills[{command, does, status: done\|next\|later}]` in run order [skills], `skills_sub?` |
| playbook | `who[{line, proof, post}]` [who], `formats` (the first three show) [formats], `hooks` [hooks], `plays[{title, seen, work, watch, line, paste, post?}]` (five, each with a Copy button for `paste`) and `skip?[{line, why?}]` [plays], `next_post?` [next], `week[{day, task, command?}]` [week]; each with an optional `<key>_sub`. A section with no data is left out |
| formats | `formats` [formats], `formats_sub?`, `matrix{columns[2], rows[{format, detail?, cells[{count, thumbnail?, url?, label?} \| null] x2}], empty?, note?}`. A `null` or zero cell is a gap, outlined in dotted orange. `#matrix` in the URL opens the matrix |
| ideas | `wall[{thumbnail, url, x?}]` (up to 30, trimmed to full rows of 10; 15 show on phones, so put the finds early), `finds[{title, nav?, why?, post, angles[{line, stage?}], status?, board_url?, board_label?}]`, where `line` is the idea's sentence alone, `stage` (Reach, Trust or Buy) prints as a tag after it, and up to five show. Finds whose `post.url` is on the wall lift out of it |
| content-log | `lists?[{status: Repeat\|Stop\|Ad, line, evidence?}]` (the three lists, first) [lists], `median` (the usual views every × is against), `median_label?`, `posts[]` in date order, `chart_sub?`, `chart_note?`, `next_post`, `lessons[{status: Confirmed\|Testing, line, evidence?}]`, `lessons_sub?` |
| analyze | `usual{views, posts, rule?, aside?[string]}` (printed under the first pair; `x` is views ÷ `usual.views` when a post has none), `pairs[{title?, verdict?, hit: post, miss: post\|null, beats[{role, differs?, hit, miss}], layers?[{layer, differs?, hit, miss}]}]` [pair, pair2…], where a beat side is `{t?, said?, screen?, shown?}` or `null` and a layer side is a string; `structures[{name, status: unproven\|holds, format?, length?, signature?, slots[{role, slot, why?}], never_change[], what_fails[]}]` [structure]. A profile adds `patterns[{status: Holds\|Unproven, line, evidence?}]` [patterns] and `kinds[{name, about?, posts, median}]` [kinds], strongest first. A `null` miss shows "No post made the same way did a third as well" |

## Motion

It starts when the header is first on screen and the tab is visible, runs from `seek(t)` and holds still after 3.4 s. `prefers-reduced-motion` or `#still` in the URL shows the end state. `window.seek(t)` is exposed for capture. "Replay" in the footer runs it again.

## Checks before handing the page over

1. `fill.py` printed no error and the page is under 16 MB. Embedded pages run 0.1 to 4 MB.
2. Every number is in the source rows with its date, and every card links to its post.
3. No emails, phone numbers or other contact details; no customer names unless the customer agreed.
4. No `cloudfront.net` links: `grep -c cloudfront out.html` prints 0.
5. Open it at 390 px wide: no sideways scroll, and the nav scrolls inside its own strip.
6. Screenshot it with `#still` and look at it full size before you send the link.
