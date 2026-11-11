#!/usr/bin/env python3
"""Turn a real saved Vamos answer into a `claude plugin eval` mock file.

Why: a mocked eval run spends no Vamos credits and replays the same data every time, so a change in
score is the skill, not the data. The answers come from Claude Code transcripts, where every
connector call and its result are saved.

  list   show the Vamos tool calls in a transcript, with size, time and what each was asked
  use    copy a spare answer from mock-library/ into one case's own mocks/
  write  write one call's real result as plugins/vamos/evals/mocks/vamos/<tool>.md (or into a case)

A transcript is a path to a .jsonl file, a session id (its main transcript and its subagents'), or a
project folder. Session ids are looked up under ~/.claude/projects/*/.

Examples
  scripts/mock-from-transcript.py list 04a289d3-ec9f-4dad-b0c1-de2e3e24fb54
  scripts/mock-from-transcript.py list ~/.claude/projects/-Users-me-proj/abc.jsonl --tool chat_completion_poll --min-chars 3000
  scripts/mock-from-transcript.py write abc.jsonl --id toolu_01ABC --name poll-done-analyze
  scripts/mock-from-transcript.py write abc.jsonl --tool get_credit_usage --nth -1
  scripts/mock-from-transcript.py write abc.jsonl --tool get_messages --nth 0 --case my-case --max-chars 6000

What `write` does to the answer
  - scrubs emails, phone numbers, bearer tokens, API keys, signed-URL signatures and the values of
    workspace, user and owner id fields; maps every other UUID (chat, run) to a stable made-up one, the
    same input giving the same output, so a saved chain (create_chat, start, poll) still lines up
  - optionally drops array items that match --drop-match, swaps strings with --replace, and trims it (--max-chars cuts a long text field at a paragraph; --max-rows keeps the first N
    items of each long array), keeping the JSON shape valid
  - turns `{{` in the answer into `{ {` because the runner reads `{{input.x}}` as a substitution
  - never takes a result that is an error unless --allow-error is given
  - with --expect, adds an `expect:` guard from the call's real input (type names only), so a case
    can also assert what the skill asked the server

It does not call any server. Read the output before you commit it: this repo is public.
"""
import argparse
import hashlib
import json
import os
import re
import sys
import uuid
from pathlib import Path

PROJECTS = Path(os.environ.get("CLAUDE_PROJECTS_DIR", "~/.claude/projects")).expanduser()
DEFAULT_MOCKS = Path(__file__).resolve().parent.parent / "plugins" / "vamos" / "evals"
SERVER = "vamos"
VAMOS_TOOL = re.compile(r"^mcp__(vamos-mcp|vamos-new|vamos-demo\d*|claude_ai_Vamos_AI|plugin_vamos_vamos|vamos)__(.+)$")

KNOWN_TOOLS = {"auth_status", "get_workspace", "create_chat", "chat_completion_start", "chat_completion_poll", "chat_completion_cancel", "get_messages", "get_credit_usage", "list_chats", "set_up_workspace", "save_brain_file"}
# Fields whose values are private to a workspace or a person. Dropped to a placeholder whatever they hold.
PRIVATE_KEYS = {"workspaceid", "workspace_id", "userid", "user_id", "ownerid", "owner_id", "teamid", "orgid", "accountid"}
EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9\-]+(?:\.[A-Za-z0-9\-]+)*\.[A-Za-z]{2,}")
PHONE = re.compile(r"(?<![\w.])(?:\+?\d{1,3}[\s.\-]?)?\(?\d{3}\)?[\s.\-]\d{3}[\s.\-]\d{4}(?!\d)")
SECRETS = [
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{16,}"),
    re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}"),  # JWT
    re.compile(r"\b(?:sk|pk|rk|xai|gsk|key|tok|ghp|gho|ghs)[-_][A-Za-z0-9_\-]{16,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
]
SIGNED_PARAM = re.compile(r"([?&](?:s|sig|signature|token|access_token|key|e|expires|X-Amz-[A-Za-z\-]+|Signature|Expires)=)[^&\s\"')]+", re.I)
UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)
# Emails that are public by design (the product's own) stay.
KEEP_EMAILS = {"support@getvamos.ai", "hello@getvamos.ai"}


def fake_uuid(value: str) -> str:
    return str(uuid.UUID(hashlib.sha256(("mock-salt:" + value.lower()).encode()).hexdigest()[:32]))


def scrub_text(text: str, report: dict) -> str:
    def email(m):
        if m.group(0).lower() in KEEP_EMAILS:
            return m.group(0)
        report["emails"] += 1
        return "person@example.com"

    text = EMAIL.sub(email, text)

    def phone(m):
        report["phones"] += 1
        return "+1 555 010 0100"

    text = PHONE.sub(phone, text)
    for pat in SECRETS:
        def sec(m):
            report["secrets"] += 1
            return "REDACTED"
        text = pat.sub(sec, text)

    def signed(m):
        report["signed_params"] += 1
        return m.group(1) + "REDACTED"

    text = SIGNED_PARAM.sub(signed, text)

    def uid(m):
        report["uuids"] += 1
        return fake_uuid(m.group(0))

    return UUID.sub(uid, text)


def scrub_value(v, report):
    if isinstance(v, str):
        return scrub_text(v, report)
    if isinstance(v, list):
        return [scrub_value(x, report) for x in v]
    if isinstance(v, dict):
        out = {}
        for k, x in v.items():
            if k.lower() in PRIVATE_KEYS and isinstance(x, str):
                report["private_fields"] += 1
                out[k] = "workspace-id-redacted"
            elif k == "cursor" and isinstance(x, str):
                report["cursors"] += 1  # a page cursor encodes real chat ids; null means "no more pages"
                out[k] = None
            else:
                out[k] = scrub_value(x, report)
        return out
    return v


def drop_value(v, pats):
    """Remove array items whose JSON text matches any pattern (private rows an answer carries)."""
    if isinstance(v, list):
        return [drop_value(x, pats) for x in v if not any(p.search(json.dumps(x, ensure_ascii=False)) for p in pats)]
    if isinstance(v, dict):
        return {k: drop_value(x, pats) for k, x in v.items()}
    return v


def trim_value(v, max_chars, max_rows):
    if isinstance(v, str):
        if max_chars and len(v) > max_chars:
            cut = v[:max_chars]
            para = cut.rfind("\n\n")
            if para > max_chars * 0.5:
                cut = cut[:para]
            return cut.rstrip() + "\n\n[trimmed for the mock]"
        return v
    if isinstance(v, list):
        items = v[:max_rows] if max_rows else v
        return [trim_value(x, max_chars, max_rows) for x in items]
    if isinstance(v, dict):
        return {k: trim_value(x, max_chars, max_rows) for k, x in v.items()}
    return v


# ---------------------------------------------------------------- transcripts

def resolve(target: str):
    p = Path(target).expanduser()
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(p.rglob("*.jsonl"))
    out = []
    for proj in PROJECTS.glob("*"):
        f = proj / f"{target}.jsonl"
        if f.is_file():
            out.append(f)
        sub = proj / target
        if sub.is_dir():
            out += sorted(sub.rglob("*.jsonl"))  # subagents, and workflow agents below them
    if not out:
        sys.exit(f"no transcript found for {target!r} (path, session id or folder)")
    return out


def result_text(content):
    if isinstance(content, list):
        return "".join(x.get("text", "") for x in content if isinstance(x, dict))
    return content if isinstance(content, str) else ""


def calls(files):
    """Every Vamos tool call paired with its result, deduped by tool_use id, in file order."""
    seen, out = {}, []
    for f in files:
        uses = {}
        with open(f, errors="replace") as fh:
            for line in fh:
                if "tool_use" not in line and "tool_result" not in line:
                    continue
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                msg = d.get("message")
                if not isinstance(msg, dict) or not isinstance(msg.get("content"), list):
                    continue
                for b in msg["content"]:
                    if b.get("type") == "tool_use":
                        m = VAMOS_TOOL.match(b.get("name", ""))
                        if m:
                            uses[b["id"]] = {"id": b["id"], "tool": m.group(2), "input": b.get("input", {}), "ts": d.get("timestamp", ""), "file": str(f)}
                    elif b.get("type") == "tool_result" and b.get("tool_use_id") in uses:
                        rec = dict(uses[b["tool_use_id"]])
                        rec["text"] = result_text(b.get("content"))
                        rec["is_error"] = bool(b.get("is_error"))
                        if rec["id"] not in seen:
                            seen[rec["id"]] = rec
                            out.append(rec)
    return out


def status_of(text):
    try:
        d = json.loads(text)
        if isinstance(d, dict):
            return d.get("status") or ("ok" if "chats" in d or "plan" in d else "")
    except ValueError:
        pass
    return "text"


def ask_of(rec, by_run):
    i = rec["input"]
    if rec["tool"] == "chat_completion_start":
        return str(i.get("content", ""))[:90]
    if rec["tool"] == "chat_completion_poll":
        s = by_run.get(i.get("runId"))
        return ("<- " + str(s["input"].get("content", ""))[:85]) if s else ""
    return json.dumps(i)[:90] if i else ""


def cmd_list(a):
    cs = calls(resolve(a.transcript))
    by_run = {}
    for c in cs:
        if c["tool"] == "chat_completion_start":
            try:
                by_run[json.loads(c["text"]).get("runId")] = c
            except ValueError:
                pass
    shown = [c for c in cs if (not a.tool or c["tool"] == a.tool) and len(c["text"]) >= a.min_chars]
    if a.done_only:
        shown = [c for c in shown if status_of(c["text"]) == "done"]
    for n, c in enumerate(shown):
        print(f"{n:>3} {c['ts'][:16]} {c['tool']:<22} {len(c['text']):>7} {status_of(c['text']):<8} {c['id']} {ask_of(c, by_run)}")
    print(f"{len(shown)} of {len(cs)} Vamos calls", file=sys.stderr)


def cmd_write(a):
    files = resolve(a.transcript)
    cs = [c for c in calls(files) if (not a.tool or c["tool"] == a.tool)]
    if a.done_only:
        cs = [c for c in cs if status_of(c["text"]) == "done"]
    if a.id:
        cs = [c for c in cs if c["id"] == a.id]
    if not cs:
        sys.exit("no matching call; run `list` first")
    rec = cs[a.nth]
    if rec["is_error"] and not a.allow_error:
        sys.exit("that result is an error; pass --allow-error to mock it (and it is written with error: true)")
    tool = rec["tool"]
    name = a.name or tool
    report = dict.fromkeys(["emails", "phones", "secrets", "signed_params", "uuids", "private_fields", "cursors"], 0)

    text = rec["text"]
    try:
        body = json.loads(text)
        body = scrub_value(body, report)
        if a.drop_match:
            body = drop_value(body, [re.compile(p, re.I) for p in a.drop_match])
        body = trim_value(body, a.max_chars, a.max_rows)
        out = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
    except ValueError:
        out = trim_value(scrub_text(text, report), a.max_chars, a.max_rows)
    for pair in a.replace or []:
        old, _, new = pair.partition("=")
        out = out.replace(old, new)
    if "{{" in out:
        out = out.replace("{{", "{ {")

    front = []
    if a.expect:
        exp = {}
        for k, v in rec["input"].items():
            exp[k] = ("number" if isinstance(v, (int, float)) and not isinstance(v, bool) else "boolean" if isinstance(v, bool) else "array" if isinstance(v, list) else "object" if isinstance(v, dict) else "string")
        if exp:
            front += ["expect:"] + [f"  {k}: {t}" for k, t in exp.items()]
    if rec["is_error"]:
        front.append("error: true")
    head = ("---\n" + "\n".join(front) + "\n---\n\n") if front else ""

    base = Path(a.out).expanduser() if a.out else DEFAULT_MOCKS
    root = (base / a.case / "mocks") if a.case else (base / "mocks")
    dest = (Path(a.dir).expanduser() / f"{name}.md") if a.dir else root / SERVER / f"{name}.md"
    if a.dry_run:
        print(head + out[:2000])
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(head + out + "\n")
    src = Path(rec["file"])
    print(f"{'would write' if a.dry_run else 'wrote'} {dest}  ({len(out)} chars)")
    print(f"  from {src.parent.name}/{src.name} tool_use {rec['id']} at {rec['ts'][:10]}")
    print("  scrubbed " + ", ".join(f"{k}={v}" for k, v in report.items() if v) if any(report.values()) else "  nothing needed scrubbing")
    if name != tool and name not in KNOWN_TOOLS:
        print(f"  NOTE: the runner answers the tool `{tool}` from {tool}.md only; `{name}.md` is a spare. Copy it over {tool}.md in a case's own mocks/ to use it.")


def cmd_use(a):
    """Copy a spare answer from mock-library/ into one case's own mocks/, named for the tool it answers."""
    lib = DEFAULT_MOCKS / "mock-library" / SERVER
    src = lib / (a.name if a.name.endswith(".md") else a.name + ".md")
    if not src.is_file():
        sys.exit(f"no {src}; ls {lib}")
    stem = src.stem.replace("-", "_")
    tool = a.tool or next((t for t in sorted(KNOWN_TOOLS, key=len, reverse=True) if stem == t or stem.startswith(t + "_")), None) or (
        "chat_completion_poll" if stem.startswith("poll_") else None)
    if not tool:
        sys.exit("cannot tell which tool this answers; pass --tool")
    dest = DEFAULT_MOCKS / a.case / "mocks" / SERVER / f"{tool}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(src.read_text())
    print(f"copied {src.name} -> {dest.relative_to(DEFAULT_MOCKS.parent.parent.parent)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list", help="list Vamos calls in a transcript")
    l.add_argument("transcript")
    l.add_argument("--tool", help="short tool name, e.g. chat_completion_poll")
    l.add_argument("--min-chars", type=int, default=0)
    l.add_argument("--done-only", action="store_true", help="only polls that finished (status done)")
    l.set_defaults(fn=cmd_list)
    w = sub.add_parser("write", help="write one call's result as a mock file")
    w.add_argument("transcript")
    w.add_argument("--tool", help="short tool name; with --nth picks among that tool's calls")
    w.add_argument("--id", help="a tool_use id from `list`")
    w.add_argument("--nth", type=int, default=-1, help="which match (default -1, the last)")
    w.add_argument("--name", help="mock file name without .md (default: the tool name)")
    w.add_argument("--case", help="write into evals/<case>/mocks/ so only that case sees it")
    w.add_argument("--dir", help="write <dir>/<name>.md exactly (for a library of spare answers), ignoring --out and --case")
    w.add_argument("--out", help="the plugin's evals dir (default plugins/vamos/evals in this repo)")
    w.add_argument("--max-chars", type=int, default=0, help="cut each text field at a paragraph near this length")
    w.add_argument("--max-rows", type=int, default=0, help="keep the first N items of every array")
    w.add_argument("--done-only", action="store_true")
    w.add_argument("--drop-match", action="append", metavar="REGEX", help="drop array items whose text matches (repeatable); use for private rows")
    w.add_argument("--replace", action="append", metavar="OLD=NEW", help="swap a string after scrubbing (repeatable), e.g. a private workspace name")
    w.add_argument("--expect", action="store_true", help="add an expect: guard built from the call's input")
    w.add_argument("--allow-error", action="store_true")
    w.add_argument("--dry-run", action="store_true")
    w.set_defaults(fn=cmd_write)
    u = sub.add_parser("use", help="copy a spare answer from mock-library/ into a case's own mocks/")
    u.add_argument("name", help="a file in plugins/vamos/evals/mock-library/vamos/, e.g. poll-analyze-reel")
    u.add_argument("--case", required=True)
    u.add_argument("--tool", help="the tool it answers (default: worked out from the name)")
    u.set_defaults(fn=cmd_use)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
