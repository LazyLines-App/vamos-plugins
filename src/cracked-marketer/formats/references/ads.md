# Ad formats

## The ad ask

One more turn in the same chat, up to 60 credits; say so first. With `include_data: true` and `data_scope: "turn"`:

> For [brand], [what they sell] to [who], in [market]: find the Meta ads still running in [category] that have run 30 days or more, from [competitors] and the category's other advertisers, statics included. Group them by format, meaning what the ad is: a static's layout (a notes screenshot, a before and after, an offer card), a video's kind (a creator talking to camera, a demo, a testimonial, an unboxing), a carousel's. For each format: how many ads and advertisers, the longest days running, and its 3 longest-running ads with their Ad Library link, advertiser, days running, copies, and the image words or the first line said and the words on screen. Say how many ads you read and how many you opened, and set aside catalog and product-feed ads.

Vamos reads every ad's days running, copies, media and copy, and opens only some to see what they show and say. An ad it didn't open keeps its numbers and joins a format only when the answer puts it there.

## Ad format cards

- **The gate:** a format ranks when the days running show 2 or more advertisers at 30+ days; one brand's habit goes under More with its reason.
- **The order:** advertisers, then the longest days running, then copies.
- **The numbers** come from the rows (`days_running`, `versions`, `media_type`, where IMAGE is a static) and the answer, dated.
- **Call a format long-running,** since its proof is its days running, and say what that means on the page and in the reply: someone keeps paying, not that it sells, since nobody outside sees spend; stopped ads outside the EU and UK are hidden, never zero.
- **The card:** `where_label` "[job] · Meta ads", `stage` Static, Video or Carousel, `stat` "[N] ads from [M] advertisers among the [K] opened, the longest [D] days", `beats` what the ad shows in order, `film` who makes it (formats.md), `yours` the angles, written from the longest runner's line the formats.md way. `examples` are the ads: `url` the Ad Library link, `handle` the advertiser, `hook` the image words or first line, `meta` "[N] days running", `platform` "FACEBOOK_AD", and no `views`.

## The page

Up to four ad formats lead, then the video formats, ten cards in all.
