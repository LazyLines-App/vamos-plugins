import json, subprocess, sys, os
from concurrent.futures import ThreadPoolExecutor
plugin=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','plugins','vamos')
mcp='{"mcpServers":{"vamos-mcp":{"type":"http","url":"https://mcp.getvamos.ai/mcp"}}}'
tools=",".join(["Skill","ToolSearch"]+["mcp__vamos-mcp__"+t for t in ["chat_completion_start","chat_completion_poll","create_chat","get_messages","list_chats","get_credit_usage","auth_status"]])
cases=[l.rstrip('\n').split('\t',1) for l in open(sys.argv[1]) if l.strip()]
def run(c):
    exp,q=c
    p=subprocess.run(['claude','-p',q,'--plugin-dir',plugin,'--setting-sources','project','--mcp-config',mcp,'--strict-mcp-config','--allowedTools',tools,'--max-turns','40','--output-format','stream-json','--verbose'],stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=1500)
    open(f'out-{exp}.jsonl','w').write(p.stdout)
    skill='-'; asks=[]; result=''; cost=0; credits=[]
    for line in p.stdout.splitlines():
        try: e=json.loads(line)
        except: continue
        if e.get('type')=='assistant':
            for x in e['message'].get('content',[]):
                if x.get('type')=='tool_use':
                    if x['name']=='Skill' and skill=='-': skill=x['input'].get('skill')
                    if x['name'].endswith('chat_completion_start'): asks.append(x['input'])
        if e.get('type')=='user':
            for x in e['message'].get('content',[]) if isinstance(e['message'].get('content'),list) else []:
                if x.get('type')=='tool_result':
                    t=x.get('content'); t=t if isinstance(t,str) else json.dumps(t)
                    if '"creditsCharged"' in t:
                        try:
                            import re; m=re.search(r'creditsCharged\\?":\s*(\d+)',t); credits.append(int(m.group(1)))
                        except: pass
        if e.get('type')=='result': result=e.get('result',''); cost=e.get('total_cost_usd') or 0
    open(f'result-{exp}.md','w').write(f"# {exp}\n\nAsk: {q}\n\nSkill loaded: {skill}\n\nVamos asks sent:\n```json\n{json.dumps(asks,indent=1,ensure_ascii=False)}\n```\n\nVamos credits: {credits}\nClaude cost: ${cost:.2f}\n\n## Final answer\n\n{result}\n")
    return exp,skill,len(asks),credits,cost
with ThreadPoolExecutor(5) as ex:
    for r in ex.map(run,cases): print(r)
