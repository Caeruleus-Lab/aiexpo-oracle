#!/usr/bin/env python3
"""herdr-bring-beside: move another pane into MY tab as a split next to me.

  bring_beside.py <who> [right|down] [--ratio F] [--dry-run]

<who> matches, in this herdr session only:
  pane id (w2:p1) | Claude session id prefix (0bec504c, >= 4 chars)
  | space label | terminal title | cwd folder name   (case-insensitive)

Uses `herdr pane move`: the process and conversation keep running, only the
pane id changes. herdr cannot move a pane between sessions (one server per
session); for that case this prints where the match lives and the commands.
Run with `python3 -I`.
"""
import json
import os
import subprocess
import sys

HERDR = os.environ.get("HERDR_BIN_PATH", "herdr")


def call(*args, session=None):
    cmd = [HERDR] + (["--session", session] if session else []) + list(args)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if p.returncode != 0:
        raise SystemExit(f"✗ {' '.join(cmd)} failed: {(p.stderr or p.stdout).strip()}")
    return json.loads(p.stdout)["result"]


def sid(p):
    return (p.get("agent_session") or {}).get("value", "")


def describe(p, labels):
    return (f"{p['pane_id']:7} {p.get('agent') or 'shell':6} {p.get('agent_status') or '-':8} "
            f"{sid(p)[:8] or '-':8}  space={labels.get(p['workspace_id'], '?')}  {p.get('cwd', '')}")


def matches(p, who, labels):
    w = who.lower()
    if p["pane_id"].lower() == w:
        return True
    s = sid(p).lower()
    if len(w) >= 4 and s.startswith(w):
        return True
    names = [labels.get(p["workspace_id"], ""), p.get("terminal_title_stripped", ""),
             os.path.basename(p.get("cwd", "").rstrip("/"))]
    return any(n and n.lower() == w for n in names)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    dry = "--dry-run" in argv
    ratio = None
    if "--ratio" in argv:
        i = argv.index("--ratio")
        ratio = argv[i + 1]
        args.remove(ratio)
    if not args:
        raise SystemExit(__doc__)
    who = args[0]
    direction = args[1] if len(args) > 1 else "right"
    if direction not in ("right", "down"):
        raise SystemExit(f"✗ direction must be right or down, got {direction!r}\n"
                         f"  python3 -I {sys.argv[0]} {who} right")

    me, tab, session = (os.environ.get(k, "") for k in ("HERDR_PANE_ID", "HERDR_TAB_ID", "HERDR_SESSION"))
    if not (me and tab):
        raise SystemExit("✗ not inside a herdr pane (HERDR_PANE_ID unset); run this from the pane to bring things beside\n"
                         "  herdr pane current")

    labels = {w["workspace_id"]: w.get("label", "") for w in call("workspace", "list")["workspaces"]}
    panes = call("pane", "list")["panes"]
    # env pane/tab ids are fixed at process start and go stale after a move:
    # use the pane that holds this Claude session now.
    my_sid = os.environ.get("CLAUDE_CODE_SESSION_ID", "")
    live = next((p for p in panes if my_sid and sid(p) == my_sid), None)
    if live:
        me, tab = live["pane_id"], live["tab_id"]
    hits = [p for p in panes if p["pane_id"] != me and matches(p, who, labels)]

    if not hits:
        # look in the other running sessions, so the error says where it is
        elsewhere = []
        out = subprocess.run([HERDR, "session", "list", "--json"], capture_output=True, text=True, timeout=15).stdout
        for s in json.loads(out or "{}").get("sessions", []):
            if not s.get("running") or s["name"] == session:
                continue
            try:
                ol = {w["workspace_id"]: w.get("label", "") for w in call("workspace", "list", session=s["name"])["workspaces"]}
                elsewhere += [(s["name"], p, ol) for p in call("pane", "list", session=s["name"])["panes"] if matches(p, who, ol)]
            except SystemExit:
                continue
        if not elsewhere:
            print(f"✗ no pane matches {who!r} in herdr session {session or 'default'} or any other running session")
            print("  herdr pane list")
            return 1
        print(f"✗ {who!r} is in another herdr session; `herdr pane move` only works inside one session:")
        for name, p, ol in elsewhere:
            print(f"  [{name}] {describe(p, ol)}")
        name, p, _ = elsewhere[0]
        if sid(p):
            print("  To bring it here, stop it there, then resume the same conversation beside you:")
            print(f"  herdr --session {name} pane close {p['pane_id']}")
            print(f"  herdr pane split {me} --direction {direction} --cwd {p['cwd']}   # note the new pane id")
            print(f"  herdr pane run <NEW_PANE> 'claude --resume {sid(p)}'")
        return 1

    if len(hits) > 1:
        print(f"✗ {who!r} matches {len(hits)} panes; pass a pane id or a longer session id:")
        for p in hits:
            print(f"  {describe(p, labels)}")
            print(f"    python3 -I {sys.argv[0]} {p['pane_id']} {direction}")
        return 2

    p = hits[0]
    if p["tab_id"] == tab:
        print(f"= {p['pane_id']} is already in this tab ({tab}); nothing to move")
        print(f"  {describe(p, labels)}")
        return 0

    cmd = ["pane", "move", p["pane_id"], "--tab", tab, "--target-pane", me, "--split", direction]
    if ratio:
        cmd += ["--ratio", ratio]
    print(f"bring  {describe(p, labels)}")
    print(f"beside {me} ({direction})  in tab {tab}, session {session or 'default'}")
    if dry:
        print(f"dry-run: {HERDR} {' '.join(cmd)}")
        return 0
    r = call(*cmd)["move_result"]
    new = r["pane"]["pane_id"]
    closed = [x for x in (r.get("closed_tab_id"), r.get("closed_workspace_id")) if x]
    print(f"✓ {r.get('previous_pane_id')} → {new}" + (f"  (closed empty {', '.join(closed)})" if closed else ""))
    print(f"  undo: {HERDR} pane move {new} --new-workspace")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
