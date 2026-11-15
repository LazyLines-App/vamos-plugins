---
type: regex
target: trace
pattern: '(?:"file_path":\s*"[^"]*-playbook\.md",\s*"content":\s*"|"command":\s*"(?:[^"\\]|\\.)*-playbook\.md)(?:[^"\\]|\\.)*?\\n\s*[-*] \*\*Seen'
# The page itself (the Write or Bash call that makes [target]-playbook.md) lists each play's parts on their own lines, as step 8's example does. Written as one paragraph, Claude Desktop's page ran them together ("history. - Seen: … - Your first line: …", 11-15, Wispr Flow).
---
