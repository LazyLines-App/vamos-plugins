import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
plugin=os.environ.get('PLUGIN') or os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','plugins','vamos')
prefix=os.environ.get('PREFIX','vamos')+':'  # PLUGIN=plugins/cracked-marketer PREFIX=cracked-marketer for its rows
cases=[l.rstrip('\n').split('\t',1) for l in open(sys.argv[1]) if l.strip()]
def run(c):
    exp,q=c
    p=subprocess.run(['claude','-p',q,'--model',os.environ.get('MODEL','sonnet'),'--plugin-dir',plugin,'--setting-sources','project','--strict-mcp-config','--allowedTools','Skill','--max-turns','2','--output-format','stream-json','--verbose'],stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=400)
    got='-'; cost=0
    for line in p.stdout.splitlines():
        try: e=json.loads(line)
        except: continue
        if e.get('type')=='assistant' and got=='-':
            for x in e['message'].get('content',[]):
                if x.get('type')=='tool_use' and x['name']=='Skill': got=x['input'].get('skill','?'); break
        if e.get('type')=='result': cost=e.get('total_cost_usd') or 0
    return exp,got,q,cost
with ThreadPoolExecutor(7) as ex:
    res=list(ex.map(run,cases))
tot=0
for exp,got,q,cost in res:
    tot+=cost
    print(('OK ' if got==prefix+exp else 'XX ')+exp.ljust(20)+' -> '+got.ljust(28)+' | '+q[:80])
print('ok',sum(1 for e,g,q,c in res if g==prefix+e),'/',len(res),'cost $%.2f'%tot)
