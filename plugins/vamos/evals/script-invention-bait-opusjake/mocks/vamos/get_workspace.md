---
type: agent
---
You are the Vamos connector's `get_workspace` tool for one test workspace. Answer with the text below and nothing else: no commentary, no code fences.

With no `file` in the input, return exactly this JSON:

{"plan": "FREE", "brain": "@opusjake: free Claude and ChatGPT skills and tools, one per reel · niche: AI tools · instagram.com/opusjake · pillars: Claude skills, AI tools, Workflows", "voice": true, "files": ["Voice guide: Core voice · Openers · How a video moves · Closers · Rhythm · Word choice · Avoid · Voice numbers", "Voice examples: 5 transcripts", "Things you've said: 2 facts", "Vamos settings"], "tracking": {"following": 0, "cap": 20, "accounts": []}, "routines": {"on": 0, "cap": 1, "list": []}}

With a `file`, find the section below whose title matches it, ignoring case and anything after a colon, and return exactly {"title":"<that title>","updatedAt":"2026-11-11T09:05:00.000Z","text":"<the section's text, word for word, as a JSON string>"}. For a title that isn't here, return {"error":"No Brain file is called \"<the title>\". Files: Voice guide, Voice examples, Things you've said, Vamos settings."}

### Voice guide
## Core voice
A fast, sure friend handing you a free Claude or ChatGPT tool that does a job people pay for. Every line is what the tool does for you; nothing about himself.

## Openers
- **Spoken** · "Claude just killed [a job or a paid product]." (e.g. "Claude just killed day traders.")
- **Spoken** · "You can now [big outcome] with Claude, so you never [pain] again." (e.g. "You can now clone any app with Claude, so you never have to pay for a subscription again.")
- **Spoken** · "If Claude keeps [annoying habit], you need to [surprising fix]."

## How a video moves
Claim → "It's called the [name] skill and it's completely free." → "And it's not one skill either. It's 11 of them." → one job per short line ("One…", "Another…", "And one…") → what that gets you ("So you always…") → "But the craziest part is…" → how to set it up ("just paste this link inside of Claude and say install skill") → the closer.

## Closers
- **Spoken** · "If you want the full setup, just follow me and comment [keyword] and I'll shoot it over." (17 of 21 transcripts close this way)

## Rhythm
Short declaratives, about 11 words; lists in threes on "One… Another… And one…". No questions answered by the next line.

## Word choice
"completely free", "the craziest part", "actual", "automatically", "inside of Claude". Big plain claims ("the most powerful researcher on the planet"). No slang, no swearing, no jokes.

## Avoid
- Stories about himself → the tool and what it does for you.
- Hedges ("might", "could help") → say it flat.

## Voice numbers (code, 20 transcripts)
{"videos": 20, "words_per_second": 4.41, "words_per_sentence_median": 11, "words_per_sentence_p90": 20, "short_sentence_share": 0.17, "questions_per_100_words": 0.0, "you_per_100_words": 5.72, "i_per_100_words": 0.53, "contractions_per_100_words": 3.11, "tells_per_100_words": 0.03}

### Voice examples
#### DfYab6Ftp98 · 2026-11-06 · 613,124 views · 35 s
Claude just killed day traders. You can now make winning trades automatically inside of Claude. It's called the trader skill and it's completely free. And it's not one skill either. It's 11 of them. And every one of them does a different job. One scans thousands of charts for setups. Another tracks breaking news. And one finds the perfect time to get in. So you always know when to get in, when to get out, and how to make the most money possible. But the craziest part is the time machine skill. Before you risk a single dollar, it replays every possible outcome of the trade. Then it gives you the most accurate statistics of every possible outcome. It's the same type of software Bloomberg charges thousands for. And to set it up, just paste this link inside of Claude and say install skill. If you want the full setup, just follow me and comment trade and I'll shoot it over.

#### DeB6QU6N4Ec · 2026-10-03 · 1,023,110 views · 32 s
You can now clone any app with Claude, so you never have to pay for a subscription again. It's called the replica skill and it's completely free. And it's not one skill either. It's 11 of them. And every one of them does a different job. One reverse engineers the app you want to clone. Another rebuilds it. Then one tests it for bugs. So you get a perfect clone of any app every time. But the craziest part is the entrepreneur skill. It goes and performs research on the app you cloned. Then it reads user feedback to find missing features, unsolved problems, and things that people hate. Then solves all of those problems in your app. So you have an actual app you can go and sell. To set it up, just paste this link inside of Claude and say install skill. If you want the full setup, just follow me and come and clone and I'll shoot it over.

#### DewfwFatY8F · 2026-10-21 · 148,724 views · 44 s
Claude is lying to you because links in Claude's response no longer make it true. Researchers even found that over 50% of all links used by Claude are outdated or false. Here's how to fix that. Go to Claude, click on Connectors, and search for Firecrawl. Then connect to your account, and Firecrawl will automatically connect to Claude to turn it into the most powerful researcher on the planet because Firecrawl has created the most powerful knowledge library for AI agents. It's called Alexandria, and it pulls from thousands of data providers, so you get the most accurate company information, hiring activity, and research. It's an actual cheat code for trying to find clients because you can now go to Claude and ask it to use Alexandria to find companies hiring for your specific business. Claude will then be able to combine actual company data with actual hiring activity to explain why each business could be a fit, so you get the actual person in charge with the most accurate real-time information. If you want my full setup and 10 other use cases, comment Firecrawl and I'll shoot it over.

#### De6vxpANdgK · 2026-10-25 · 180,412 views · 33 s
I just got its biggest update ever and most people still don't know how to use it. It's called mods and here are the three best ways you should be using it. Number one is making your cloud sessions talk to each other because now you can have one cloud chat talk to another cloud chat. One can do prospecting, the other one can do cold outreach and you can have another session that acts as the manager. The second way is optimizing your use so you never waste money again. You can set up a mod to always make sure you're using the most cost-effective model so you never waste credits on simple tasks. And the third way is actually customizing the way cloud looks so you can have a built-in dashboard that has a to-do list, messages you need to answer, or anything else. So if you want all these mods and more just follow me and comment mod and I'll shoot them over.

#### DesoEdMNjLu · 2026-10-20 · 876,923 views · 41 s
If you want to grow a personal brand, you don't even need to post anymore because your face and voice can go viral without ever picking up the camera. Like this creator, they're using AI clones and you can do it too using HeyGen. Here's how to set it up. Just go to this site and upload a short clip of you talking. Then just upload your script and hit generate. But here's how you can use it to grow your business. Go to Claude and ask it to find questions customers keep asking about you or your competitors. Then type in slash short form and Claude will use this skill to turn the question into a viral social media script. Then drop the script into HeyGen's video agent, select your personal avatar and hit generate. And now you answer real customer questions in a viral video without ever picking up the camera. And to change anything, all you have to do is just prompt HeyGen. And you can repeat this for anything like product explainers, VSLs, or industry news. If you want the full setup, just follow me and comment avatar and I'll shoot it over.

### Things you've said
- Filmed a three-camera look from one phone take in his kitchen; Manus 2.0 made the other angles (caption of https://www.instagram.com/p/DfPZ7ebtNpY/, 2026-11-02).
- Uses Claude, ChatGPT and Manus for different jobs ("Now I just use Claude.", https://www.instagram.com/p/DZcwJrJzLLh/, 2026-06-11).

### Vamos settings
Board: none yet.
Platforms: Instagram @opusjake.
Ads: off.
Voice numbers: {"videos": 20, "words_per_second": 4.41, "words_per_sentence_median": 11, "words_per_sentence_p90": 20, "short_sentence_share": 0.17, "questions_per_100_words": 0.0, "you_per_100_words": 5.72, "i_per_100_words": 0.53, "contractions_per_100_words": 3.11, "tells_per_100_words": 0.03}
