---
type: regex
target: trace
pattern: '"(file_path|command)":\s*"(?:[^"\\]|\\.)*-playbook\.md'
# The page is made on every run (step 9): a Write or Bash call names [target]-playbook.md. Needs `--allow-tools Write Bash`: without the grant the sandbox has neither, and the skill rightly skips the page and says so.
---
