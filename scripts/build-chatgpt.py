"""Build the ChatGPT plugin package from the Claude plugin's skills, so both stay one source.

  python3 scripts/build-chatgpt.py   ->  dist/chatgpt/vamos/ and dist/vamos-chatgpt.zip

Only the "no connector" line differs per host. Listing text lives in chatgpt/listing.json.
"""
import json, os, re, shutil, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'plugins', 'vamos', 'skills')
EXTRA = os.path.join(ROOT, 'chatgpt', 'skills')
OUT = os.path.join(ROOT, 'dist', 'chatgpt', 'vamos')
CLAUDE_LINE = re.compile(r"If no Vamos tool is connected, say this needs the Vamos connector:.*$", re.M)
CHATGPT_LINE = "If no Vamos tool is connected, say this needs the Vamos plugin: open chatgpt.com/plugins, find Vamos and select Connect."

listing = json.load(open(os.path.join(ROOT, 'chatgpt', 'listing.json')))
claude_manifest = json.load(open(os.path.join(ROOT, 'plugins', 'vamos', '.claude-plugin', 'plugin.json')))

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(os.path.join(OUT, 'skills'))
for src in (SRC, EXTRA):
    for name in sorted(os.listdir(src)):
        body = open(os.path.join(src, name, 'SKILL.md')).read()
        body, n = CLAUDE_LINE.subn(CHATGPT_LINE, body)
        body = body.replace('as a Claude scheduled task on a paid plan', 'as a scheduled task where their plan has them')
        os.makedirs(os.path.join(OUT, 'skills', name))
        open(os.path.join(OUT, 'skills', name, 'SKILL.md'), 'w').write(body)

ASSETS = os.path.join(ROOT, 'chatgpt', 'assets')
if os.path.isdir(ASSETS):
    shutil.copytree(ASSETS, os.path.join(OUT, 'assets'))

manifest = {
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": "vamos",
    "version": claude_manifest["version"],
    "description": claude_manifest["description"],
    "author": {"name": "Vamos", "url": "https://getvamos.ai"},
    "homepage": "https://getvamos.ai",
    "license": claude_manifest.get("license", "MIT"),
    "keywords": ["content research", "tiktok", "instagram", "youtube", "meta ads", "creators", "scripts"],
    "extensions": {"com.openai": {
        "onboardingSkill": "./skills/get-started/SKILL.md",
        "auth": {"vamos": {"type": "oauth"}},
        "interface": listing,
    }},
}
for k, cap in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000)):
    assert len(listing[k]) <= cap, (k, len(listing[k]))
assert len(listing["defaultPrompt"]) <= 3 and all(len(p) <= 128 for p in listing["defaultPrompt"])
json.dump(manifest, open(os.path.join(OUT, 'plugin.json'), 'w'), indent=2, ensure_ascii=False)
json.dump({"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
           "mcpServers": {"vamos": {"type": "streamable-http", "url": "https://mcp.getvamos.ai/mcp"}}},
          open(os.path.join(OUT, 'mcp.json'), 'w'), indent=2)
z = os.path.join(ROOT, 'dist', 'vamos-chatgpt.zip')
with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
    for d, _, files in os.walk(OUT):
        for fn in files:
            p = os.path.join(d, fn)
            f.write(p, os.path.relpath(p, OUT))
print(z, sorted(os.listdir(os.path.join(OUT, 'skills'))))
