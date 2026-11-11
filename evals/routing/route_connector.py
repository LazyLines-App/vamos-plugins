# Routing with the Vamos connector loaded beside the skills, as a real install has it.
# Run from (or set CONNECTOR_DIR to) a folder where that connector is signed in. Only Skill and ToolSearch are allowed, so any connector call is denied: no credits.
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
plugin, prefix, cases_file = sys.argv[1], sys.argv[2], sys.argv[3]
cases=[l.rstrip('\n').split('\t',1) for l in open(cases_file) if l.strip()]
NAME=os.environ.get('CONNECTOR_NAME','vamos')  # the name your signed-in Vamos connector has in that folder
MCP=json.dumps({"mcpServers":{NAME:{"type":"http","url":"https://mcp.getvamos.ai/mcp"}}})
def run(c):
    exp,q=c
    p=subprocess.run(['claude','-p',q,'--model','sonnet','--plugin-dir',plugin,'--setting-sources','project,local',
        '--mcp-config',MCP,'--strict-mcp-config','--allowedTools','Skill,ToolSearch','--max-turns','3',
        '--output-format','stream-json','--verbose'],stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=400,
        cwd=os.environ.get('CONNECTOR_DIR', os.getcwd()))
    got='-'; cost=0
    for line in p.stdout.splitlines():
        try: e=json.loads(line)
        except: continue
        if e.get('type')=='assistant' and got=='-':
            for x in e['message'].get('content',[]):
                if x.get('type')=='tool_use':
                    if x['name']=='Skill': got=x['input'].get('skill','?'); break
                    if x['name'].startswith('mcp__'): got='CONNECTOR:'+x['name'].split('__')[-1]; break
        if e.get('type')=='result': cost=e.get('total_cost_usd') or 0
    return exp,got,q,cost
with ThreadPoolExecutor(6) as ex: res=list(ex.map(run,cases))
tot=0
for exp,got,q,cost in res:
    tot+=cost
    print(('OK ' if got==prefix+exp else 'XX ')+exp.ljust(18)+' -> '+got.ljust(34)+' | '+q[:70])
print('ok',sum(1 for e,g,q,c in res if g==prefix+e),'/',len(res),'connector-first',sum(1 for e,g,q,c in res if g.startswith('CONNECTOR')),'cost $%.2f'%tot)
