---
type: regex
target: trace
pattern: '"(file_path|command)":\s*"(?:[^"\\]|\\.)*-playbook\.md'
match: not_contains
# A question about what they run is answered in the reply (step 8): no "Plays to steal" page nobody asked for.
---
