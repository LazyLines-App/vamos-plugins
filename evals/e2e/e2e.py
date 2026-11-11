"""Live end-to-end runs on a demo Vamos workspace. Spends real credits.

  VAMOS_CONNECTOR=vamos-demo python3 evals/e2e/e2e.py evals/e2e/cases.tsv

The connector name comes from VAMOS_CONNECTOR (default vamos-demo; vamos-demo2 is the fresh account), and any
name that isn't a demo connector is refused. Each run starts in ~/vamos-demo-test (VAMOS_DEMO_DIR), where the demo
connectors' sign-ins live, so a live run never reaches a real workspace. Results land in the folder you ran it from,
one pair of files per row (the row number keeps two rows for the same skill apart).
"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

plugin = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'plugins', 'vamos'))
server = os.environ.get('VAMOS_CONNECTOR', 'vamos-demo')
demo_dir = os.path.expanduser(os.environ.get('VAMOS_DEMO_DIR', '~/vamos-demo-test'))
if not re.fullmatch(r'vamos-demo\d*', server):
    sys.exit(f'VAMOS_CONNECTOR={server}: live runs go only through a demo connector (vamos-demo, vamos-demo2, ...)')
if not os.path.isdir(demo_dir):
    sys.exit(f'{demo_dir} not found: the demo connectors are signed in there')
out = os.getcwd()
mcp = json.dumps({'mcpServers': {server: {'type': 'http', 'url': 'https://mcp.getvamos.ai/mcp'}}})
tools = ','.join(['Skill', 'ToolSearch', 'Read', 'Write'] + [f'mcp__{server}__{t}' for t in [
    'chat_completion_start', 'chat_completion_poll', 'create_chat', 'get_messages', 'list_chats',
    'get_credit_usage', 'auth_status', 'get_workspace', 'set_up_workspace']])
cases = [l.rstrip('\n').split('\t', 1) for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]


def run(ic):
    i, (exp, q) = ic
    name = f'{i + 1:02d}-{exp}'
    p = subprocess.run(['claude', '-p', q, '--plugin-dir', plugin, '--setting-sources', 'project', '--mcp-config', mcp,
                        '--strict-mcp-config', '--allowedTools', tools, '--max-turns', '40', '--output-format',
                        'stream-json', '--verbose'], stdin=subprocess.DEVNULL, capture_output=True, text=True,
                       timeout=1500, cwd=demo_dir)
    open(os.path.join(out, f'out-{name}.jsonl'), 'w').write(p.stdout)
    skill = '-'; asks = []; result = ''; cost = 0; credits = []
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get('type') == 'assistant':
            for x in e['message'].get('content', []):
                if x.get('type') == 'tool_use':
                    if x['name'] == 'Skill' and skill == '-':
                        skill = x['input'].get('skill')
                    if x['name'].endswith('chat_completion_start'):
                        asks.append(x['input'])
        if e.get('type') == 'user' and isinstance(e['message'].get('content'), list):
            for x in e['message']['content']:
                if x.get('type') == 'tool_result':
                    t = x.get('content')
                    t = t if isinstance(t, str) else json.dumps(t)
                    credits += [int(m) for m in re.findall(r'creditsCharged\\?":\s*(\d+)', t)]
        if e.get('type') == 'result':
            result = e.get('result', ''); cost = e.get('total_cost_usd') or 0
    open(os.path.join(out, f'result-{name}.md'), 'w').write(
        f"# {exp}\n\nConnector: {server}\n\nAsk: {q}\n\nSkill loaded: {skill}\n\nVamos asks sent:\n```json\n"
        f"{json.dumps(asks, indent=1, ensure_ascii=False)}\n```\n\nVamos credits: {credits}\nClaude cost: ${cost:.2f}\n\n"
        f"## Final answer\n\n{result}\n")
    return name, skill, len(asks), credits, cost


with ThreadPoolExecutor(5) as ex:
    for r in ex.map(run, enumerate(cases)):
        print(r)
