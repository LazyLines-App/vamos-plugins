---
type: regex
target: trace
pattern: '"(file_path|command)":\s*"(?:[^"\\]|\\.)*playbook\.html'
# The page is made on every run (step 9): a Write or Bash call names playbook.html. Needs `--allow-tools Write Bash`: without the grant the sandbox has neither, and the skill rightly skips the page and says so.
---
