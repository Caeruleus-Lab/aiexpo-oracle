#!/usr/bin/env python3
"""herdr-work: create-or-find a repo, clone it into the ghq tree, open it as its
own herdr space, and start a Claude agent in it — one command from a name to a
body you can work in.

  work.py <owner/repo | name> [--public] [--private] [--desc "..."]
          [--here] [--no-agent] [--kind claude|codex] [--down] [--dry-run]

- <owner/repo>: exact. A bare <name> defaults the owner to laris-co.
- repo missing on GitHub  -> gh repo create (private by default) --add-readme
- repo exists, not cloned -> ghq get
- already cloned          -> used as is
Then: a new herdr space at the repo (or --here = a split in this tab), an agent
named after the repo, started in it (unless --no-agent).

Run with `python3 -I`.  gh + ghq + herdr must be on PATH.
"""
import json
import os
import subprocess
import sys

HERDR = os.environ.get("HERDR_BIN_PATH", "herdr")
DEFAULT_OWNER = "laris-co"


def sh(*args, check=True):
    p = subprocess.run(args, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise SystemExit(f"✗ {' '.join(args)}\n  {(p.stderr or p.stdout).strip()}")
    return p


def herdr(*args):
    p = sh(HERDR, *args, check=False)
    if p.returncode != 0:
        raise SystemExit(f"✗ {HERDR} {' '.join(args)}: {(p.stderr or p.stdout).strip()}\n"
                         f"  {HERDR} {args[0]} --help")
    try:
        return json.loads(p.stdout)["result"]
    except (ValueError, KeyError):
        return {}


def main(argv):
    flags = {a for a in argv if a.startswith("--")}
    pos = [a for a in argv if not a.startswith("--")]
    desc = ""
    if "--desc" in argv:
        i = argv.index("--desc")
        if i + 1 < len(argv):
            desc = argv[i + 1]
            pos = [a for a in pos if a != desc]
    kind = "claude"
    if "--kind" in argv:
        i = argv.index("--kind")
        kind = argv[i + 1] if i + 1 < len(argv) else kind
        pos = [a for a in pos if a != kind]
    if not pos:
        raise SystemExit(__doc__)
    target = pos[0].rstrip("/")
    if target.startswith(("http://", "https://", "git@", "ssh://")):
        raise SystemExit("✗ pass owner/repo or a name, not a URL\n  "
                         f"python3 -I {sys.argv[0]} laris-co/{target.rstrip('/').split('/')[-1].replace('.git','')}")
    owner, _, repo = target.partition("/")
    if not repo:
        owner, repo = DEFAULT_OWNER, owner
    slug = f"{owner}/{repo}"
    dry = "--dry-run" in flags
    public = "--public" in flags
    visibility = "--public" if public else "--private"

    root = sh("ghq", "root").stdout.strip()
    path = f"{root}/github.com/{owner}/{repo}"

    # 1. resolve the repo
    if os.path.isdir(os.path.join(path, ".git")):
        state = "already cloned"
    else:
        exists = sh("gh", "repo", "view", slug, "--json", "name", check=False).returncode == 0
        if not exists:
            if dry:
                state = f"WOULD create {visibility} + clone"
            else:
                sh("gh", "repo", "create", slug, visibility, "--add-readme",
                   *(["--description", desc] if desc else []))
                sh("ghq", "get", slug)
                state = f"created {visibility.lstrip('-')} + cloned"
        else:
            if dry:
                state = "WOULD clone (repo exists on GitHub)"
            else:
                sh("ghq", "get", slug)
                state = "cloned (existed on GitHub)"

    print(f"repo   {slug}  ({state})")
    print(f"path   {path}")
    if dry and not os.path.isdir(os.path.join(path, ".git")):
        print(f"dry-run: gh repo create {slug} {visibility} --add-readme; ghq get {slug}")
        return 0
    if not os.path.isdir(os.path.join(path, ".git")):
        raise SystemExit(f"✗ clone did not land at {path}\n  ghq get {slug}")

    if "--no-agent" in flags:
        print("space  (skipped, --no-agent)")
        print(f"  open it yourself: {HERDR} workspace create --cwd {path} --label {repo}")
        return 0

    # 2. open a herdr space (or split here)
    if "--here" in flags:
        me = os.environ.get("HERDR_PANE_ID")
        if not me:
            raise SystemExit("✗ --here needs to run inside a herdr pane (HERDR_PANE_ID unset)")
        direction = "down" if "--down" in flags else "right"
        if dry:
            print(f"dry-run: {HERDR} pane split {me} --direction {direction} --cwd {path}")
            return 0
        r = herdr("pane", "split", me, "--direction", direction, "--cwd", path)
        pane = (r.get("pane") or r).get("pane_id")
        where = f"split {direction} of {me}"
    else:
        if dry:
            print(f"dry-run: {HERDR} workspace create --cwd {path} --label {repo}")
            return 0
        ws = herdr("workspace", "create", "--cwd", path, "--label", repo, "--no-focus")
        ws_id = (ws.get("workspace") or ws).get("workspace_id")
        pane = next((p["pane_id"] for p in herdr("pane", "list").get("panes", [])
                     if p.get("workspace_id") == ws_id), None)
        where = f"space {ws_id}"
    if not pane:
        raise SystemExit("✗ could not find the new pane; open it by hand")

    # 3. start the agent and name it
    cmd = "command codex" if kind == "codex" else "command claude --dangerously-skip-permissions"
    herdr("pane", "run", pane, cmd)
    sh(HERDR, "agent", "rename", pane, repo, check=False)
    sess = os.environ.get("HERDR_SESSION", "default")
    print(f"agent  {kind} '{repo}' in {where}  (pane {pane}, session {sess})")
    print(f"  brief it: {HERDR} --session {sess} agent prompt {pane} \"...\"")
    print(f"  close it: {HERDR} --session {sess} pane close {pane}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
