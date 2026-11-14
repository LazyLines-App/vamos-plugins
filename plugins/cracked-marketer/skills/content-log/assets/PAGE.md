# The page

The page is what the user keeps from this run: what you found, laid out so they can come back to it. [page.html](page.html) holds the look, light and dark, and a few pieces at the top of `<main>` that you can use or skip.

## Write it

1. Copy `page.html` to the page's file, set its `<title>`, and write the body in `<main>`.
2. Open with the answer: one sentence on what this run found, then a line on what it means for them.
3. Then what they'll read or act on, in sections you name and order for this run. Give each section something real from the rows or your counts, and leave out any that came back empty.
4. Give numbers as the rows give them, with the date they were read. Link every post, ad and account you name.
5. End with the recap as the footer.

Write it in plain words, the way you'd explain it to them, and say how sure you are as a reason ("from 3 posts, so a guess").

Keep it quiet: one typeface, plenty of room, the orange only for what wins. Put a wide table in `<div class="scroll">`, so the page reads on a phone. Keep contact details off the page, and name a customer only with their OK.

## Pictures

Artifacts block remote images. Use a thumbnail where seeing the post helps, with the row's `cdn.lazylines.ai` link, then run `python3 <this skill's folder>/scripts/embed.py <page>.html`. It puts each picture in the page, takes out any that won't load, and prints the page's size (an Artifact holds 16 MB) and any `cloudfront.net` link left; swap those for the post's own link, since they die in about 102 minutes. With no shell, let the post's hook and link carry it, with no picture.

Publish it as an Artifact; where the host can't, give the file's path.
