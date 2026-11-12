"""Copy the shared sources into each skill, so every skill folder stands alone on every host.

  python3 scripts/build-skills.py           writes the copies
  python3 scripts/build-skills.py --check   fails if a copy is stale, a link is broken or a skill lost its last line

One source each: src/shared/working-with-vamos.md (injected between the markers in SKILL.md),
src/shared/board.md, src/shared/textstats.py, and the page kit in src/page-kit/.
The skills both plugins hold have one source too, plugins/vamos/skills/<name>: they are copied whole
into plugins/cracked-marketer/skills/<name> (CM_SHARED). Edit them only in plugins/vamos.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, 'plugins', 'vamos', 'skills')
SHARED = os.path.join(ROOT, 'src', 'shared')
KIT = os.path.join(ROOT, 'src', 'page-kit')

BLOCK = '<!-- shared: working-with-vamos -->'
END = '<!-- /shared -->'
LAST_LINE = re.compile(r"If no Vamos tool is connected, say this needs the Vamos connector:.*\n?\Z")
PAGES = ['setup', 'playbook', 'formats', 'ideas', 'content-log', 'analyze']
COPIES = {
    'references/board.md': (os.path.join(SHARED, 'board.md'), ['setup', 'formats', 'hooks', 'ideas', 'script', 'content-log']),
    'scripts/textstats.py': (os.path.join(SHARED, 'textstats.py'), ['setup', 'script']),
    'assets/page.html': (os.path.join(KIT, 'page.html'), PAGES),
    'assets/PAGE.md': (os.path.join(KIT, 'README.md'), PAGES),
    'scripts/fill.py': (os.path.join(KIT, 'fill.py'), PAGES),
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
CM_SHARED = ['setup', 'playbook', 'formats', 'hooks', 'ideas', 'script', 'content-log', 'loop', 'analyze']
CM_REWRITE = [('/vamos:', '/cracked-marketer:'),
              ('the Connectors tab of the Vamos plugin', 'the Connectors tab of the Cracked marketer plugin')]
# Setup's home page lists the skills in run order; Cracked marketer's order holds its own skills too (its README).
CM_SETUP_ORDER = ('the skills in run order: playbook, formats, hooks, ideas, script, content-log, loop, and analyze any time.',
                  'the skills in run order: find-creators, creator-program, playbook, formats, hooks, ideas, winning-ad-ideas, '
                  'brief, script, make-video, review-draft, content-log, loop, and analyze any time.')
# Loop's description names the creators' week only where there is a creator program to run (Cracked marketer).
CM_LOOP_DESC = [('a weekly content log, stopping', "a weekly content log with your paid creators' results, stopping"),
                ('to automate your content, keep research running', "to automate your content, run a creator program's week by itself, keep research running")]
SKIP = {'__pycache__', '.DS_Store'}

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
    for rel in sorted(have):
        data = open(os.path.join(src, rel), 'rb').read()
        try:
            text = data.decode('utf-8')
            for old, new in CM_REWRITE:
                text = text.replace(old, new)
            if (name, rel) == ('setup', 'SKILL.md'):
                if CM_SETUP_ORDER[0] not in text:
                    problems.append("setup/SKILL.md lost its run-order line: update CM_SETUP_ORDER in build-skills.py")
                text = text.replace(*CM_SETUP_ORDER)
            if (name, rel) == ('loop', 'SKILL.md'):
                for pair in CM_LOOP_DESC:
                    if pair[0] not in text:
                        problems.append("loop/SKILL.md's description changed: update CM_LOOP_DESC in build-skills.py")
                    text = text.replace(*pair)
            data = text.encode('utf-8')
        except UnicodeDecodeError:
            pass
        want_bytes(os.path.join(dst, rel), data)
    for rel in sorted(files(dst) - have) if os.path.isdir(dst) else []:
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
