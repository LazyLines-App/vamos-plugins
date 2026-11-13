# formats: Cracked marketer's words

Each edit below is Content System's words in `plugins/vamos/skills/formats`, then the words Cracked marketer's copy has instead. `python3 scripts/build-skills.py` applies them and fails when the old words are gone. `references/ads.md` here is added to Cracked marketer's copy only.

A brand asks which formats to make for its ads as well as its posts, and its creators film what the team can't, so the page adds the ad formats its category keeps running and says who makes each format.

~~~old SKILL.md
description: "Ranks the video formats to make next for your brand: new ones taking off outside your niche, rising ones, and proven ones you haven't made, each with playable examples, how crowded it is near you, what it takes to film, and angles written for you. Use when you ask what format to try, what's trending, or how to make a format yours."
~~~

~~~new
description: "Ranks the formats to make next for your brand: the Meta ad formats your category keeps running 30+ days, statics included, and the video formats taking off near you, each with the job it does, real examples, how crowded it is, whether your creators can film it, and angles written for you. Use when you ask what format to try, which ad formats work in your category, what's trending, or how to make a format yours."
~~~

~~~old SKILL.md
Vamos's answer is research for the next steps, not the reply:
~~~

~~~new
**The ads:** read [references/ads.md](references/ads.md) and send its ad ask in the same chat, unless Vamos settings has Ads off. When they asked about ad formats only, it is the only ask, and steps 3 to 8 run on its answer.

Vamos's answer is research for the next steps, not the reply:
~~~

~~~old SKILL.md
the ranking lives in that file, and steps 4 to 7 add to it and read from it.
~~~

~~~new
the ranking lives in that file, and steps 4 to 7 add to it and read from it. The ad format cards follow [references/ads.md](references/ads.md).
~~~

~~~old SKILL.md
at To review, or hand it to `/vamos:script`.
~~~

~~~new
at To review, or hand it on: `/cracked-marketer:brief` when a creator films it, `/cracked-marketer:script` or `/cracked-marketer:make-video` when the team makes it.
~~~

~~~old SKILL.md
Next is `/vamos:hooks` for the format they picked, or `/vamos:ideas`.
~~~

~~~new
Next is `/cracked-marketer:brief` for a format their creators will film, `/cracked-marketer:make-video` for one the team makes, or `/cracked-marketer:hooks` for its opening line.
~~~

~~~old SKILL.md
its rank, name, badge, uses in their niche,
~~~

~~~new
its rank and name, its job and who makes it as its card says ("Trust · your creators can film it"), its badge, uses in their niche (an ad format: its ads, advertisers and longest days running),
~~~

~~~old references/formats.md
- **No hard clash with their limits:** a format filmed on a face for someone who never shows one, before-and-after for someone who rules it out.
~~~

~~~new
- **No hard clash with their limits:** before-and-after for a brand that rules it out. A face limit in Vamos settings is the team's: their creators show their own faces, so a face format ranks as one their creators film.
~~~

~~~old references/formats.md
Add the stage, the beats, the range or a risk when it helps them choose.
~~~

~~~new
Add the stage, the beats, the range or a risk when it helps them choose.

Every card, ad or video, names its job and who makes it. Its badge starts with the job its beats do ("Trust · Next door", "Buy · Meta ads"):
- **Reach:** stops a stranger.
- **Trust:** proof, a demo, a how-to, a customer.
- **Buy:** the product working, an objection answered, the offer.

How they'd film it opens with who makes it:
- **"Your creators can film it":** one person with a phone, the product and their own place, face included. Name the creators a "Creator program: [brand]" lists.
- **"Your team makes it":** a static, a carousel, a screen recording, animation, anything built rather than filmed.
~~~

~~~old SKILL.md
We film [their limits].
~~~

~~~new
Our team films [their limits]; our creators film themselves.
~~~

~~~old SKILL.md
sees only the brand's profile, its off-limits list,
~~~

~~~new
sees only the brand's profile, its off-limits list (the team's; its creators film themselves),
~~~

~~~old SKILL.md
Read the rows first, from `json_url` (curl) or inline, because the stage and the niche counts are only there.
~~~

~~~new
Read the rows first, from `json_url` (curl) or inline, because the stage and the niche counts are only there; when the ad ask's answer came without rows, its numbers fill the ad cards and every later step runs.
~~~
