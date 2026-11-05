"""Build the ChatGPT plugin package: the reviewed base (chatgpt/base/plugin.json, chatgpt/assets, chatgpt/skills)
plus the Claude plugin's job skills, so the skills stay one source.

  python3 scripts/build-chatgpt.py   ->  dist/chatgpt/vamos/ and dist/vamos-chatgpt.zip

Only the "no connector" line differs per host. Bump `version` in chatgpt/base/plugin.json for each upload.
"""
import json, os, re, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOB_SKILLS = os.path.join(ROOT, 'plugins', 'vamos', 'skills')
OWN_SKILLS = os.path.join(ROOT, 'chatgpt', 'skills')
OUT = os.path.join(ROOT, 'dist', 'chatgpt', 'vamos')
CLAUDE_LINE = re.compile(r"If no Vamos tool is connected, say this needs the Vamos connector:.*$", re.M)
CHATGPT_LINE = "If no Vamos tool is connected, say this needs the Vamos plugin: open chatgpt.com/plugins, find Vamos and select Connect."

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'skills'))
for src in (JOB_SKILLS, OWN_SKILLS):
    for name in sorted(os.listdir(src)):
        body = open(os.path.join(src, name, 'SKILL.md')).read()
        body = CLAUDE_LINE.sub(CHATGPT_LINE, body)
        body = body.replace('as a Claude scheduled task on a paid plan', 'as a scheduled task where their plan has them')
        os.makedirs(os.path.join(OUT, 'skills', name), exist_ok=True)
        open(os.path.join(OUT, 'skills', name, 'SKILL.md'), 'w').write(body)
shutil.copytree(os.path.join(ROOT, 'chatgpt', 'assets'), os.path.join(OUT, 'assets'))

manifest = json.load(open(os.path.join(ROOT, 'chatgpt', 'base', 'plugin.json')))
ui = manifest['extensions']['com.openai']['interface']
for k, cap in (('displayName', 30), ('shortDescription', 30), ('longDescription', 4000)):
    assert len(ui[k]) <= cap, (k, len(ui[k]))
assert len(ui['defaultPrompt']) <= 3 and all(len(p) <= 128 for p in ui['defaultPrompt'])
for key in ('composerIcon', 'logo'):
    assert os.path.exists(os.path.join(OUT, ui[key])), ui[key]
assert os.path.exists(os.path.join(OUT, manifest['extensions']['com.openai']['onboardingSkill']))
json.dump(manifest, open(os.path.join(OUT, 'plugin.json'), 'w'), indent=2, ensure_ascii=False)
json.dump({"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
           "mcpServers": {"vamos": {"type": "streamable-http", "url": "https://mcp.getvamos.ai/mcp"}}},
          open(os.path.join(OUT, 'mcp.json'), 'w'), indent=2)
z = os.path.join(ROOT, 'dist', f"vamos-chatgpt-{manifest['version']}.zip")
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
    for d, _, files in os.walk(OUT):
        for fn in sorted(files):
            p = os.path.join(d, fn)
            f.write(p, os.path.relpath(p, OUT))
print(z, sorted(os.listdir(os.path.join(OUT, 'skills'))))
