# post: Cracked marketer's words

Each edit below is Content System's words in `plugins/vamos/skills/post`, then the words Cracked marketer's copy has instead. `python3 scripts/build-skills.py` applies them and fails when the old words are gone.

In Cracked marketer the videos come from make-video, which writes each one's post sheet.

~~~old SKILL.md
The videos are their own edits of `/vamos:script`'s scripts.
~~~

~~~new
The videos are `/vamos:make-video`'s, each with its post sheet, or the user's own edits.
~~~
