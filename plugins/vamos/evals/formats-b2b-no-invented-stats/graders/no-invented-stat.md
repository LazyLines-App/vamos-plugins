---
type: regex
target: last_message
pattern: '(?<![Dd]ropp[^\n]{0,200}|[Ll]eft (?:it |them )?out[^\n]{0,200}|[Nn]othing[^\n]{0,30}backs?[^\n]{0,200}|[Uu]nsourced[^\n]{0,200})(?:[Tt]hird of (?:the |recorded |our )?(?:discovery )?calls|60 seconds before retention|60-second retention)(?![^\n]{0,200}(?:[Ll]eft (?:it |them )?out|[Dd]ropped|[Nn]othing[^\n]{0,30}backs|[Dd]on.t use|unsourced|isn.t in anything you|not in anything you))'
match: not_contains
---
# Vamos's answer invented two claims ("about a third of the calls we record" / "a third of recorded discovery calls include this line", and "caps at about 60 seconds before retention drops"); neither is in Things you've said, and the brand never opens on an unsourced statistic. The claim may be named on a line that says it was dropped (the bar: nothing invented reaches the user as fact); anywhere else it fails. 11-11 eval-3: a reply listed "About a third of calls", which isn't in anything you've told us" under a "Left out from Vamos's answer" heading, which the same-line lookbehind couldn't see, so "isn't in anything you…" after the claim also counts as dropped.
