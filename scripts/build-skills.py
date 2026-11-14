"""Copy the shared sources into each skill, so every skill folder stands alone on every host.

  python3 scripts/build-skills.py           writes the copies
  python3 scripts/build-skills.py --check   fails if a copy is stale, a link is broken or a skill lost its last line

One source each: src/shared/working-with-vamos.md (injected between the markers in SKILL.md),
src/shared/board.md, src/shared/textstats.py, and the page kit in src/page-kit/.
The skills both plugins hold have one source too, plugins/vamos/skills/<name>: they are copied whole
into plugins/cracked-marketer/skills/<name> (CM_SHARED). Edit them only in plugins/vamos. Where a brand's job
differs, src/cracked-marketer/<name>/ holds Cracked marketer's own words (EDITS.md) and files.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'plugins', 'vamos', 'skills')
SHARED = os.path.join(ROOT, 'src', 'shared')
KIT = os.path.join(ROOT, 'src', 'page-kit')

BLOCK = '<!-- shared: working-with-vamos -->'
END = '<!-- /shared -->'
LAST_LINE = re.compile(r"If no Vamos tool is connected, say this needs the Vamos connector:.*\n?\Z")
PAGES = ['playbook']
COPIES = {
    'references/board.md': (os.path.join(SHARED, 'board.md'), ['setup', 'formats', 'hooks', 'ideas', 'script', 'content-log', 'post']),
    'scripts/textstats.py': (os.path.join(SHARED, 'textstats.py'), ['setup', 'script']),
    'assets/PAGE.md': (os.path.join(KIT, 'README.md'), PAGES),
}

check = '--check' in sys.argv
problems = []

def want(path, text):
    old = open(path).read() if os.path.exists(path) else None
    if old == text:
        return
    if check:
        problems.append(f'stale: {os.path.relpath(path, ROOT)}')
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w').write(text)

block = open(os.path.join(SHARED, 'working-with-vamos.md')).read().strip()
for name in sorted(os.listdir(SKILLS)):
    path = os.path.join(SKILLS, name, 'SKILL.md')
    body = open(path).read()
    if BLOCK in body:
        head, rest = body.split(BLOCK, 1)
        body = f'{head}{BLOCK}\n{block}\n{END}{rest.split(END, 1)[1]}'
        want(path, body)
    if not LAST_LINE.search(body):
        problems.append(f'{name}: SKILL.md must end with the connector line (build-chatgpt.py swaps it)')

for rel, (src, skills) in COPIES.items():
    if not os.path.exists(src):
        problems.append(f'missing source: {os.path.relpath(src, ROOT)}')
        continue
    text = open(src).read()
    for name in skills:
        want(os.path.join(SKILLS, name, rel), text)

for name in sorted(os.listdir(SKILLS)):
    path = os.path.join(SKILLS, name, 'SKILL.md')
    for link in re.findall(r'\]\(((?:references|assets|scripts)/[^)]+)\)', open(path).read()):
        if not os.path.exists(os.path.join(SKILLS, name, link)):
            problems.append(f'{name}: broken link {link}')

# Cracked marketer holds Content System's skills: each is copied whole from plugins/vamos/skills,
# with the command prefix and the plugin name rewritten. Its own skills are never touched.
CM_SKILLS = os.path.join(ROOT, 'plugins', 'cracked-marketer', 'skills')
CM_SHARED = ['setup', 'playbook', 'formats', 'hooks', 'ideas', 'script', 'content-log', 'loop', 'analyze', 'post']
CM_REWRITE = [('/vamos:', '/cracked-marketer:'),
              ('the Connectors tab of the Vamos plugin', 'the Connectors tab of the Cracked marketer plugin')]
# Where a shared skill's job differs for a brand, Cracked marketer's copy has its own words and files:
# src/cracked-marketer/<skill>/EDITS.md holds each edit (Content System's words, then Cracked marketer's),
# and every other file in that folder is added to Cracked marketer's copy only.
CM_ONLY = os.path.join(ROOT, 'src', 'cracked-marketer')
EDIT = re.compile(r'^~~~old (\S+)\n(.*?)\n~~~\n+~~~new\n(.*?)\n~~~$', re.S | re.M)
SKIP = {'__pycache__', '.DS_Store'}

def cm_edits(name):
    path = os.path.join(CM_ONLY, name, 'EDITS.md')
    edits = {}
    if os.path.exists(path):
        body = open(path).read()
        found = EDIT.findall(body)
        if len(found) != len(re.findall(r'^~~~old ', body, re.M)):
            problems.append(f'src/cracked-marketer/{name}/EDITS.md: an edit block is malformed (~~~old <file>, the words, ~~~, then ~~~new, the words, ~~~)')
        for rel, old, new in found:
            edits.setdefault(rel, []).append((old, new))
    return edits

def want_bytes(path, data):
    old = open(path, 'rb').read() if os.path.exists(path) else None
    if old == data:
        return
    if check:
        problems.append(f'stale: {os.path.relpath(path, ROOT)}')
    else:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'wb').write(data)

def files(top):
    out = set()
    for d, dirs, names in os.walk(top):
        dirs[:] = [x for x in dirs if x not in SKIP]
        out |= {os.path.relpath(os.path.join(d, n), top) for n in names if n not in SKIP}
    return out

for name in CM_SHARED:
    src, dst = os.path.join(SKILLS, name), os.path.join(CM_SKILLS, name)
    if not os.path.isdir(src):
        problems.append(f'missing shared skill: plugins/vamos/skills/{name}')
        continue
    have = files(src)
    edits = cm_edits(name)
    extra_dir = os.path.join(CM_ONLY, name)
    extra = files(extra_dir) - {'EDITS.md'} if os.path.isdir(extra_dir) else set()
    for rel in sorted(set(edits) - have):
        problems.append(f'src/cracked-marketer/{name}/EDITS.md edits {rel}, which plugins/vamos/skills/{name} lacks')
    for rel in sorted(extra & have):
        problems.append(f'src/cracked-marketer/{name}/{rel} would replace the shared file: edit it in EDITS.md instead')
    skill_md = ''
    for rel in sorted(have | extra):
        data = open(os.path.join(src if rel in have else extra_dir, rel), 'rb').read()
        try:
            text = data.decode('utf-8')
            for old, new in edits.get(rel, []):
                if text.count(old) != 1:
                    problems.append(f'src/cracked-marketer/{name}/EDITS.md: {rel} holds "{old[:60]}…" {text.count(old)} times, not once')
                text = text.replace(old, new)
            for old, new in CM_REWRITE:
                text = text.replace(old, new)
            data = text.encode('utf-8')
            if rel == 'SKILL.md':
                skill_md = text
        except UnicodeDecodeError:
            pass
        want_bytes(os.path.join(dst, rel), data)
    for link in re.findall(r'\]\(((?:references|assets|scripts)/[^)]+)\)', skill_md):
        if link not in have | extra:
            problems.append(f'cracked-marketer/{name}: broken link {link}')
    for rel in sorted(files(dst) - have - extra) if os.path.isdir(dst) else []:
        if check:
            problems.append(f'stale: {os.path.relpath(os.path.join(dst, rel), ROOT)} (not in plugins/vamos)')
        else:
            os.remove(os.path.join(dst, rel))

# Cracked marketer's own skills get the same Vamos block between the same markers, with its command prefix.
cm_block = block
for old, new in CM_REWRITE:
    cm_block = cm_block.replace(old, new)
for name in sorted(set(os.listdir(CM_SKILLS)) - set(CM_SHARED) - SKIP):
    path = os.path.join(CM_SKILLS, name, 'SKILL.md')
    if not os.path.exists(path):
        continue
    body = open(path).read()
    if BLOCK in body:
        head, rest = body.split(BLOCK, 1)
        body = f'{head}{BLOCK}\n{cm_block}\n{END}{rest.split(END, 1)[1]}'
        want(path, body)
    if not LAST_LINE.search(body):
        problems.append(f'cracked-marketer/{name}: SKILL.md must end with the connector line')
    for link in re.findall(r'\]\(((?:references|assets|scripts)/[^)]+)\)', body):
        if not os.path.exists(os.path.join(CM_SKILLS, name, link)):
            problems.append(f'cracked-marketer/{name}: broken link {link}')

print('\n'.join(problems) or ('ok' if check else 'built'))
sys.exit(1 if problems else 0)
