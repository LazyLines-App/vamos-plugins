# Weekly format measurements

These rows describe the approved format-library sample, not every post on a platform. They add context beside the existing picks; they do not replace the format gate or choose the recommendation order.

After ranking and checking the angles, use the complete saved JSON export once. Keep both `formats` and `format_weeks`; do not reconstruct rows by hand or drop the named-format list:

```sh
python3 [this skill's folder]/scripts/price.py rows.json --compact --format-id [first pick's format_id] --format-id [next pick's format_id]
```

Repeat `--format-id` for the picks you are presenting. The default command emits the full weekly tables; save that output as a Markdown artifact when the user wants the detail. `--json` returns the same validated rows with their format ids for a host that needs structured data. The script makes no network or model call. Download a signed export once with the existing file link; do not spend another research turn to reprint it.

Run one command with all picked ids before drafting any measurement block. Insert each matching block in full under that format, after its example link. Keep its numerical values, supporting Ns and age wording; translate labels if needed, without shortening the block. The pooled line carries the actual number of readable weeks, counts and median values. The `N` after views and after the multiple can differ. The small charts show publication weeks in order, each scaled from zero to its own maximum; a dot is missing, not zero. Missing weeks and too-new view counts stay gaps. A measured zero is still zero.

Say "latest stored views", and keep how old the posts were when those counts were recorded. A post age of 4.8 days does not mean the data was fetched 4.8 days ago, nor establish views at seven days. A pooled row covering six readable weeks must not become an eight-week median. Do not average the weekly medians yourself.

Keep the user's niche and next-door niches separate. The numerator/denominator and share refer to library posts, not all content in that niche. Keep existing lifetime `niche_examples` separate from these publication-window counts.

When `format_weeks` is absent or the parser rejects rows, keep the current useful formats reply. Leave those measurements out. Inline data prices at most five formats; a missing section is not a zero or proof that a format failed. Use the already supplied file when available; do not add a paid ask for this field. Ad-only rows and older exports need no weekly section.
