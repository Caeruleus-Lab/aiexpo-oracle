#!/usr/bin/env python3
"""herdr-whoami: where is THIS agent running?

Machine (local or reached over ssh), herdr session/space/tab/pane, Claude session id
and transcript, cwd, git branch and remote. Read-only. Run with `python3 -I`.
"""
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

E = os.environ


def run(args, cwd=None):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=8, cwd=cwd)
        return p.stdout.strip() if p.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def herdr(*args):
    out = run([E.get("HERDR_BIN_PATH", "herdr"), *args])
    try:
        return json.loads(out)["result"]
    except (ValueError, KeyError):
        return {}


rows, warns = [], []


def section(title):
    rows.append((None, title))


def row(k, v):
    rows.append((k, v if v not in (None, "") else "-"))


# machine
section("machine")
row("host", socket.gethostname().split(".")[0])
row("user", E.get("USER") or run(["whoami"]))
ssh = E.get("SSH_CONNECTION", "").split()
row("reached", f"remote: ssh from {ssh[0]}" if ssh else "local (no ssh)")

# herdr
section("herdr")
if E.get("HERDR_ENV") == "1" and E.get("HERDR_PANE_ID"):
    # HERDR_*_ID env is fixed at process start and goes stale after `herdr pane move`;
    # find the pane that holds this Claude session now, fall back to the env pane.
    my_sid = E.get("CLAUDE_CODE_SESSION_ID", "")
    pane = next((p for p in herdr("pane", "list").get("panes", [])
                 if my_sid and (p.get("agent_session") or {}).get("value") == my_sid), None)
    if pane is None:
        pane = herdr("pane", "get", E["HERDR_PANE_ID"]).get("pane", {})
    if pane.get("pane_id") and pane["pane_id"] != E["HERDR_PANE_ID"]:
        warns.append(f"$HERDR_PANE_ID={E['HERDR_PANE_ID']} is stale (pane was moved); live pane is {pane['pane_id']}")
    ws_id = pane.get("workspace_id") or E.get("HERDR_WORKSPACE_ID", "")
    label = next((w.get("label") for w in herdr("workspace", "list").get("workspaces", [])
                  if w.get("workspace_id") == ws_id), "")
    row("session", E.get("HERDR_SESSION"))
    row("space", f"{ws_id} {label}".strip())
    row("tab", pane.get("tab_id") or E.get("HERDR_TAB_ID"))
    row("pane", pane.get("pane_id") or E.get("HERDR_PANE_ID"))
    row("agent name", pane.get("name") or herdr("agent", "get", pane.get("pane_id", "")).get("agent", {}).get("name"))
    row("pane cwd", pane.get("foreground_cwd") or pane.get("cwd"))
    # the sidebar's "machines" tree: Local = this machine's server, the rest are
    # saved machines reached over ssh (`herdr machine list`)
    row("sidebar", "Local" + (" (but this shell came in over ssh)" if ssh else ""))
    try:
        saved = json.loads(run([E.get("HERDR_BIN_PATH", "herdr"), "machine", "list", "--json"]) or "[]")
    except ValueError:
        saved = []
    for m in saved:
        row("remote", f"{m.get('label')}  {m.get('target')}  session={m.get('session')}"
            + ("" if m.get("enabled", True) else "  (disabled)"))
    herdr_sid = (pane.get("agent_session") or {}).get("value", "")
else:
    row("session", "not inside a herdr pane")
    herdr_sid = ""

# claude
section("claude")
sid = E.get("CLAUDE_CODE_SESSION_ID", "")
pid = E.get("CLAUDE_PID", "")
meta = {}
if pid:
    try:
        meta = json.loads((Path.home() / ".claude/sessions" / f"{pid}.json").read_text())
    except (OSError, ValueError):
        pass
sid = sid or meta.get("sessionId", "")
row("session id", sid)
row("name", meta.get("name"))
row("pid", pid)
row("version", meta.get("version"))
start_cwd = meta.get("cwd", "")
row("start cwd", start_cwd)
if sid and start_cwd:
    slug = "".join(c if c.isalnum() else "-" for c in start_cwd)
    t = Path.home() / ".claude/projects" / slug / f"{sid}.jsonl"
    row("transcript", str(t).replace(str(Path.home()), "~", 1) + ("" if t.exists() else "  (missing)"))
if herdr_sid and sid and herdr_sid != sid:
    warns.append(f"herdr pane records session {herdr_sid}, but this process is {sid}")

# cwd + git
section("cwd")
cwd = os.getcwd()
row("pwd", cwd)
if start_cwd and os.path.realpath(cwd) != os.path.realpath(start_cwd):
    warns.append(f"pwd moved away from the session's start cwd {start_cwd}")
top = run(["git", "rev-parse", "--show-toplevel"], cwd)
if top:
    section("git")
    common = run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd)
    main = str(Path(common).parent) if common else top
    row("repo", top)
    row("checkout", "main checkout" if os.path.realpath(main) == os.path.realpath(top)
        else f"worktree of {main}")
    head = run(["git", "status", "-sb", "--porcelain"], cwd).splitlines()
    row("branch", head[0].removeprefix("## ") if head else "")
    row("dirty", f"{len(head) - 1} files" if len(head) > 1 else "clean")
    remote = run(["git", "remote", "get-url", "origin"], cwd)
    row("remote", remote or "no origin")

w = max(len(k) for k, _ in rows if k)
for k, v in rows:
    print(f"\n{v}" if k is None else f"  {k:<{w}}  {v}")
for m in warns:
    print(f"\n! {m}")
sys.exit(0)
