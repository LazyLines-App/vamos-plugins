#!/usr/bin/env python3
"""Copy a plugin with extra MCP servers in its .mcp.json, for a replay that mocks a server the user connects
themselves (Zernio), since `claude plugin eval` mocks only servers the plugin declares.

    python3 scripts/with-server.py plugins/vamos /tmp/vamos-zernio zernio=https://mcp.zernio.com/mcp
    cd /tmp/vamos-zernio && claude plugin eval . --case content-log-zernio-numbers ...

The copy is for the replay only: the shipped plugin never declares the user's own Zernio. Standard library only.
"""
import json, os, shutil, sys

if len(sys.argv) < 4 or any('=' not in a for a in sys.argv[3:]):
    sys.exit(__doc__)
src, dst = sys.argv[1], sys.argv[2]
if os.path.exists(dst):
    sys.exit(f'{dst} exists: give a new folder')
shutil.copytree(src, dst, ignore=shutil.ignore_patterns('results'))
path = os.path.join(dst, '.mcp.json')
cfg = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {'mcpServers': {}}
for arg in sys.argv[3:]:
    name, url = arg.split('=', 1)
    cfg['mcpServers'][name] = {'type': 'http', 'url': url}
with open(path, 'w', encoding='utf-8') as f:
    json.dump(cfg, f, indent=2)
    f.write('\n')
print(f'{dst}: servers ' + ', '.join(cfg['mcpServers']))
