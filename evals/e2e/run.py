"""End-to-end runner: each case runs headless in Claude Code, with the plugin or with only the connector.

Cases are a TSV: id, mode (plugin|connector), server, ask. Live runs spend real credits, so they go only through a
demo connector: the server column is ignored, and every run uses VAMOS_CONNECTOR (default vamos-demo; vamos-demo2 is
the fresh account). Any other name is refused, so a run can never reach a real user's workspace.
An ask may hold follow-up turns separated by " ||| ": each later turn resumes the same session, the way a user
answers the questions Claude asked. Outputs land in <out>/<id>/: stream.jsonl per turn and result.md.

  python3 evals/e2e/run.py cases.tsv OUTDIR [--conc 4] [--model sonnet] [--only id1,id2]
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.join(HERE, '..', '..', 'plugins', 'vamos')
SERVER = os.environ.get('VAMOS_CONNECTOR', 'vamos-demo')
if not re.fullmatch(r'vamos-demo\d*', SERVER):
    sys.exit(f'VAMOS_CONNECTOR={SERVER}: live runs go only through a demo connector (vamos-demo, vamos-demo2, ...)')
URLS = {SERVER: 'https://mcp.getvamos.ai/mcp'}
VAMOS_TOOLS = ['chat_completion_start', 'chat_completion_poll', 'chat_completion_cancel', 'create_chat', 'get_messages',
               'list_chats', 'get_credit_usage', 'auth_status', 'set_up_workspace']

args = sys.argv[1:]
cases_path, outdir = args[0], args[1]
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
CONC, MODEL, ONLY = int(opt('--conc', 4)), opt('--model', 'sonnet'), opt('--only')

cases = []
for line in open(cases_path):
    if not line.strip() or line.startswith('#'):
        continue
    cid, mode, _server, ask = line.rstrip('\n').split('\t', 3)
    server = SERVER
    if ONLY and cid not in ONLY.split(','):
        continue
    cases.append((cid, mode, server, [t.strip() for t in ask.split('|||')]))


def turn(cid, mode, server, prompt, session, i, d):
    mcp = json.dumps({'mcpServers': {server: {'type': 'http', 'url': URLS[server]}}})
    # Write and Read inside the run folder, so a skill that builds a sheet or file can, as it would for a real user.
    tools = ['Skill', 'ToolSearch', 'Write', 'Read'] + [f'mcp__{server}__{t}' for t in VAMOS_TOOLS]
    cmd = ['claude', '-p', prompt, '--model', MODEL, '--setting-sources', 'project', '--mcp-config', mcp,
           '--strict-mcp-config', '--allowedTools', ','.join(tools), '--max-turns', '60',
           '--output-format', 'stream-json', '--verbose']
    if mode == 'plugin':
        cmd[3:3] = ['--plugin-dir', PLUGIN]
    if session:
        cmd += ['--resume', session]
    t0 = time.time()
    p = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3000, cwd=d)
    open(os.path.join(d, f'turn{i}.jsonl'), 'w').write(p.stdout + ('\n#STDERR\n' + p.stderr if p.stderr else ''))
    out = {'skills': [], 'calls': [], 'results': [], 'final': '', 'cost': 0.0, 'session': session, 'secs': round(time.time() - t0)}
    pending = {}
    for line in p.stdout.splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get('type') == 'system' and e.get('session_id'):
            out['session'] = e['session_id']
        if e.get('type') == 'assistant':
            for x in e['message'].get('content', []):
                if x.get('type') == 'tool_use':
                    if x['name'] == 'Skill':
                        out['skills'].append(x['input'].get('skill'))
                    if x['name'].startswith('mcp__'):
                        name = x['name'].split('__')[-1]
                        pending[x['id']] = name
                        if name != 'chat_completion_poll':
                            out['calls'].append({'tool': name, 'input': x['input']})
        if e.get('type') == 'user' and isinstance(e['message'].get('content'), list):
            for x in e['message']['content']:
                if x.get('type') == 'tool_result' and pending.get(x.get('tool_use_id')):
                    t = x.get('content')
                    t = t if isinstance(t, str) else json.dumps(t, ensure_ascii=False)
                    out['results'].append({'tool': pending[x['tool_use_id']], 'text': t})
        if e.get('type') == 'result':
            out['final'] = e.get('result', '')
            out['cost'] = e.get('total_cost_usd') or 0.0
            out['session'] = e.get('session_id') or out['session']
    return out


def run(case):
    cid, mode, server, turns = case
    d = os.path.join(outdir, cid)
    os.makedirs(d, exist_ok=True)
    if os.path.exists(os.path.join(d, 'result.md')):
        return cid, 'kept'
    session, md, total = None, [f'# {cid}\n\nMode: {mode} · server: {server} · model: {MODEL}\n'], 0.0
    answers = []
    for i, prompt in enumerate(turns):
        r = turn(cid, mode, server, prompt, session, i, d)
        session = r['session']
        total += r['cost']
        vamos = [x for x in r['results'] if x['tool'] == 'chat_completion_poll' and '"status":"done"' in x['text'].replace(' ', '')]
        credits = [int(m) for x in r['results'] for m in re.findall(r'creditsCharged\\?"\s*:\s*(\d+)', x['text'])]
        chats = sorted(set(re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
                                      json.dumps([c['input'] for c in r['calls']]) + json.dumps([x['text'][:400] for x in r['results']]))))
        md.append(f'\n## Turn {i + 1}\n\n**User:** {prompt}\n\nSkills loaded: {r["skills"] or "none"} · Vamos credits: {credits} · '
                  f'Claude ${r["cost"]:.2f} · {r["secs"]} s\n\nIds seen: {", ".join(chats) or "none"}\n')
        md.append('### Calls to Vamos\n\n```json\n' + json.dumps(r['calls'], indent=1, ensure_ascii=False) + '\n```\n')
        for j, v in enumerate(vamos):
            try:
                body = json.loads(v['text'])
                body = body.get('result', v['text']) if isinstance(body, dict) else v['text']
            except Exception:
                body = v['text']
            md.append(f'### Vamos answer {j + 1}\n\n{body}\n')
        md.append(f'### What Claude told the user\n\n{r["final"]}\n')
        answers.append((r['skills'], len(r['calls']), credits, r['cost']))
    md.insert(1, f'Total Claude cost: ${total:.2f}\n')
    open(os.path.join(d, 'result.md'), 'w').write('\n'.join(md))
    return cid, answers


with ThreadPoolExecutor(CONC) as ex:
    for res in ex.map(run, cases):
        print(json.dumps(res, ensure_ascii=False), flush=True)
