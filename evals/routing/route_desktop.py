# Routing as the Claude app sees it: the plugin, a signed-in demo Vamos connector, and no SessionStart hook (the app runs it
# only after the first tool call). Records the first tool of any kind. Only Skill and ToolSearch run, so no credits.
# Point it at a copy of the plugin without hooks/:  route_desktop.py <plugin dir> <prefix> <cases.tsv> <model> <reps>
import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
plugin, prefix, cases_file, model, reps = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
cases=[l.rstrip('\n').split('\t',1) for l in open(cases_file) if l.strip()]*reps
NAME=os.environ.get('CONNECTOR_NAME','vamos-demo2')
MCP=json.dumps({"mcpServers":{NAME:{"type":"http","url":"https://mcp.getvamos.ai/mcp"}}})
def run(c):
    exp,q=c
    p=subprocess.run(['claude','-p',q,'--model',model,'--plugin-dir',plugin,'--setting-sources','project,local',
        '--mcp-config',MCP,'--strict-mcp-config','--allowedTools','Skill,ToolSearch','--max-turns','3',
        '--output-format','stream-json','--verbose'],stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=400,
        cwd=os.environ.get('CONNECTOR_DIR', os.getcwd()))
    seq=[]; cost=0; hook=False
    for line in p.stdout.splitlines():
        try: e=json.loads(line)
        except: continue
        if e.get('type')=='system' and 'hook' in json.dumps(e).lower() and 'vamos plugin is installed' in json.dumps(e): hook=True
        if e.get('type')=='assistant':
            for x in e['message'].get('content',[]):
                if x.get('type')=='tool_use':
                    n=x['name']
                    if n=='Skill': seq.append('skill:'+x['input'].get('skill','?'))
                    elif n=='ToolSearch': seq.append('search:'+str(x['input'].get('query',''))[:30])
                    elif n.startswith('mcp__'): seq.append('vamos:'+n.split('__')[-1])
                    else: seq.append(n)
        if e.get('type')=='result': cost=e.get('total_cost_usd') or 0
    return exp,seq,q,cost,hook
with ThreadPoolExecutor(6) as ex: res=list(ex.map(run,cases))
tot=0
for exp,seq,q,cost,hook in res:
    tot+=cost
    first=next((s for s in seq if not s.startswith('search:')), '-')
    ok = first==('skill:'+prefix+exp)
    print(('OK ' if ok else 'XX ')+exp.ljust(17)+' -> '+' > '.join(seq)[:80].ljust(80)+' | '+q[:50])
print('cost $%.2f'%tot)
