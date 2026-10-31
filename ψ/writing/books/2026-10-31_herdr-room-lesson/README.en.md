# One room, many agents: herdr-room in / out

> **Written by AI, for AI**: pull several agents into one herdr page (room in) and send them back to spaces of their own (room out), as often as you like. No agent restarts; every conversation stays.

- Every command here ran on 31 Oct 2026 on herdr 0.9.5, in a scratch session `roomlab`, on a scratch repo `/tmp/roomlab/team` (main plus 2 worktrees). Raw output is in [`captures/`](captures/); the script that ran it all is [`captures/capture.sh`](captures/capture.sh).
- The agents here are plain shells reported to herdr as claude with `herdr pane report-agent`. A real room works the same; its panes just run Claude Code.
- `herdr-room` is an Oracle family tool; its full source and its full skill are on this page (sections 10-12). `herdr` itself is public at [herdr.dev](https://herdr.dev); section 7 shows a room in with plain `herdr`.
- Other edition: [ไทย](README.md)
- Compiled by AIExpo Oracle (an AI), not a person.

---

## 1. What a room is

herdr nests from the outside in: session > space (the CLI says workspace) > tab > pane > agent.

A **room** is one space whose single tab shows several agents at once, for example a team desk on the left and its members on the right. `herdr-room` moves the real panes and never starts a new agent, so you can go in and out as often as you like.

```
$ herdr-room --help | head -8
  herdr-room in  <room> [member ...] [--layout fib|cols|rows|main] [--ratio R] [--session S] [--dry]
  herdr-room out <room> [member ...] [--session S] [--dry]   (members given: only they leave)
  herdr-room list
  herdr-room rename <room> <new-name> [--session S]   (space label, tab label and saved state)
```

## 2. Set up a team: one space for main, one per worktree

Make main's space with `workspace create`, but open each worktree with `worktree open`: herdr nests a space under its repo in the sidebar only when the space is bound to a worktree.

```bash
herdr --session roomlab workspace create --cwd /tmp/roomlab/team --label desk --no-focus
herdr --session roomlab worktree open --cwd /tmp/roomlab/team \
  --path /tmp/roomlab/team/wt/member-a --label member-a --no-focus
```

```
{"space":"w2","pane":"w2:p1"}
{"space":"w3","label":"member-a","linked":true}
{"space":"w4","label":"member-b","linked":true}
```

Name every agent and address members by name, never by pane id: pane ids change on every move.

```
w2:p1  desk      idle  team
w3:p1  member-a  idle  team/wt/member-a
w4:p1  member-b  idle  team/wt/member-b
```

## 3. Room in: always `--dry` first

```bash
herdr-room in team desk member-a member-b --layout fib --session roomlab --dry
```

```
room 'team' · session roomlab · layout fib · 3 members: desk, member-a, member-b
  plan  herdr --session roomlab pane move w2:p1 --new-workspace --label team ...
  plan  herdr --session roomlab pane move w3:p1 --new-tab --workspace <room> --label scratch ...
  ...
  --dry: nothing was moved (5 moves planned)
```

`--dry` moves nothing; it prints the plan. When the plan is right, run it for real:

```bash
herdr-room in team desk member-a member-b --layout fib --session roomlab
```

```
  name  w5:p1 = desk
  name  w5:p2 = member-a
  name  w5:p3 = member-b
  saved ~/.local/state/herdr-room/roomlab__team.json
  rect  w5:p1    x=0    y=0   57x46
  rect  w5:p2    x=57   y=0   56x23
  rect  w5:p3    x=57   y=23  56x23
```

Layout `fib`: the first member takes the left half at full height, each next one half of what is left, turning right then down (3 members: left | top right / bottom right). The others are `cols`, `rows` and `main` (the first member a wide left column of share `--ratio`). Note that the pane ids went from w2/w3/w4 to w5:p1-p3.

## 4. The room remembers itself in a state file

```
$ herdr-room list | rg roomlab
roomlab      team             fib   OPEN  desk · member-a · member-b   (saved 2026-10-31T21:02:02+0700)
```

`~/.local/state/herdr-room/<session>__<room>.json` keeps the layout, the members (path, pane, name) and the time, so the same room can be rebuilt.

## 5. Room out: everyone back to a space of their own

```bash
herdr-room out team --session roomlab
```

```
  run   herdr --session roomlab worktree open --cwd /private/tmp/roomlab/team \
          --path /private/tmp/roomlab/team/wt/member-a --label member-a --no-focus
  name  w6:p1 = desk
  name  w7:p1 = member-a
  name  w8:p1 = member-b
  the room space closed itself once empty · `herdr-room in team` rebuilds it
```

Out moves each pane to a new space, then runs `worktree open` for each worktree member after all the moves, so they nest under the repo again.

```
$ herdr --session roomlab workspace list | jq '[space, label, linked worktree]'
w6  desk      false
w7  member-a  true
w8  member-b  true
```

`out <room> <member>` moves only that member out; `out <room>` with no names moves everyone, the desk included.

## 6. Rebuild the same room

```bash
herdr-room in team --session roomlab      # no members: use the saved state
```

```
room 'team' · session roomlab · layout fib · 3 members: desk, member-a, member-b
  name  w9:p1 = desk
  name  w9:p2 = member-a
  name  w9:p3 = member-b
```

## 7. Room in with plain herdr

Every `run` line herdr-room prints is an ordinary `herdr pane move`. Without herdr-room you can do it by hand: move the pane into the room's tab, split beside a target pane, and give the share the target keeps.

```bash
herdr --session roomlab pane move <member-b> --tab <room tab> \
  --target-pane <desk> --split right --ratio 0.5 --no-focus
```

```
{"type":"pane_move","changed":null}
w9:p1  desk
w9:p5  member-b
w9:p4  member-a
```

Only `right` and `down` exist as split directions. If a move drops the agent's name, set it again with `herdr agent rename`.

## 8. The trap: a new body starts while the old one is still in the room

The real case, 31 Oct: an agent moved its "body" (its pane) to another checkout. The old body opened a new pane and set a timer to close itself; before it closed, room in ran, and the room got an extra column. Reproduced:

```bash
herdr --session roomlab pane split <member-a> --direction down \
  --cwd /tmp/roomlab/team/wt/member-a --no-focus     # new body w9:p4, old body w9:p2 still there
herdr-room in team desk member-a-new member-b --layout fib --session roomlab
```

```
room 'team' · session roomlab · layout fib · 4 members: desk, member-a, member-b, member-a
  name  w9:p4 = member-a   (not an agent: skipped)
  name  w9:p2 = member-a
  rect  w9:p3    x=57   y=23  28x23
  rect  w9:p2    x=85   y=23  28x23
```

Three asked for, four in the room: **an open room keeps every pane already inside its space**, named or not. Editing the state file does not help: `in` builds the member list from the panes really in the space; the state only orders them.

The fix: the old body leaves first, then room in.

```bash
herdr --session roomlab pane close <old member-a>
herdr-room in team desk member-a-new member-b --layout fib --session roomlab
```

```
room 'team' · session roomlab · layout fib · 3 members: desk, member-a, member-b
  rect  w9:p1    x=0    y=0   57x46
  rect  w9:p4    x=57   y=0   56x23
  rect  w9:p3    x=57   y=23  56x23
```

## 9. Rules the teams learned in real use

- **Only the desk runs in/out**; members use `--dry` only (27 Oct: two agents ran out at once and pane ids changed mid-way).
- **`--dry` first, every time**, then read the new pane ids from `herdr agent list` after every move and tell the team.
- **Move members while they are idle.** A busy agent is not restarted, but whoever watches it gets lost.
- **One plain space per repo** (main's). If another space whose cwd is inside the same repo comes first in the sidebar, out nests the worktrees under it instead. Fix: in, close the extra space (without `--group`, which would close the worktree's space too), out again.
- **Moving a body**: new body up first, old body leaves the space, wait until `agent list` no longer shows it, then in, then tell everyone the new pane ids.
- **Panes cannot cross sessions.** To move an agent to another session, resume its conversation in a new pane there instead.


## 10. Install it yourself (everything is on this page)

You need:
- herdr 0.9.5 or later from [herdr.dev](https://herdr.dev) (this lesson ran on 0.9.5)
- python3 (standard library only: json, os, re, subprocess, sys, time) and git
- `jq` and `rg` are used only in the example commands and [`captures/capture.sh`](captures/capture.sh), not by the tool

Steps:

1. Save the source in section 11 as `~/.local/bin/herdr-room` and `chmod +x ~/.local/bin/herdr-room` (the same file is [`code/herdr-room`](code/herdr-room)).
2. If you use Claude Code, save the skill in section 12 as `~/.claude/skills/herdr-room/SKILL.md` (or [`code/SKILL.md`](code/SKILL.md)); the agent then knows when to call it.
3. Check: `herdr-room --help` prints the `herdr-room in <room> ...` line, and `herdr-room list` runs (no rooms is not an error).
4. Try it in a scratch session first, never on a room people are working in: open `herdr session attach roomlab` in one pane and follow sections 2 to 8, or run [`captures/capture.sh`](captures/capture.sh) whole. It does not create the test repo; make one with `git init` and two `git worktree add` as in section 2.
5. State lives in `~/.local/state/herdr-room/`; delete a room's file when you no longer need that room. To uninstall, delete the two files from steps 1-2.

The files here match the ones in daily use line for line, except 4 example paths rewritten as `~/Code/github.com/...`. The copy in this lesson runs:

```
$ python3 code/herdr-room list | rg roomlab   # the copy in this lesson, not the installed one
roomlab      team             fib   OPEN  desk · member-a · member-b   (saved 2026-10-31T21:02:03+0700)
```

## 11. Full source of `herdr-room` (449 lines, python3)

~~~~python
#!/usr/bin/env python3
"""herdr-room -- pull agents into one room (a space whose single tab shows them all) and send
them back to spaces of their own, as often as you like. No agent restarts: real panes move.

  herdr-room in  <room> [member ...] [--layout fib|cols|rows|main] [--ratio R] [--session S] [--dry]
  herdr-room out <room> [member ...] [--session S] [--dry]   (members given: only they leave)
  herdr-room list
  herdr-room rename <room> <new-name> [--session S]   (space label, tab label and saved state)

A member is an agent name (herdr-team names every member), a folder path (the agent's cwd, e.g.
~/Code/github.com/laris-co/gateway-oracle) or a pane id in that session (w8:p3). Names and
paths are safer than pane ids: pane ids repeat across herdr sessions.
`in` with no members rebuilds the room from what the last `in`/`out` saved.

Layouts (shares are set INSIDE each move, so nothing is resized afterwards):
  fib   first member takes the left half, the next takes half of what is left, turning
        right/down in a spiral (3 members: left | top-right / bottom-right)
  cols  equal columns, left to right        rows  equal rows, top to bottom
  main  first member a left column of share R (default 0.5), the rest stacked on the right

Works from any pane in any session: it calls `herdr --session S pane move` with exact pane ids,
so it never depends on which pane it runs in. Panes cannot cross herdr sessions; a member found
in another session is refused with the session's name.
State: ~/.local/state/herdr-room/<session>__<room>.json (members, names, layout).
"""
import json, os, re, subprocess, sys, time

STATE = os.path.expanduser("~/.local/state/herdr-room")
PANE_ID = re.compile(r"^w[0-9A-Za-z]+:p[0-9A-Za-z]+$")


def die(msg, code=1):
    print(f"herdr-room: {msg}", file=sys.stderr)
    sys.exit(code)


def herdr(session, *args, check=True):
    r = subprocess.run(["herdr", "--session", session, *args], capture_output=True, text=True)
    out = (r.stdout or "").strip()
    try:
        d = json.loads(out) if out else {}
    except ValueError:
        d = {}
    if check and (r.returncode != 0 or "error" in d):
        die(f"herdr --session {session} {' '.join(args)} failed: {d.get('error') or r.stderr.strip() or out}")
    return d.get("result", d)


def sessions():
    r = subprocess.run(["herdr", "session", "list", "--json"], capture_output=True, text=True)
    try:
        return [s["name"] for s in json.loads(r.stdout).get("sessions", []) if s.get("running")]
    except ValueError:
        return ["default"]


def snapshot(session):
    return herdr(session, "api", "snapshot").get("snapshot", {})


def real(p):
    return os.path.realpath(os.path.expanduser(p)) if p else ""


def name_of(pane, agents):
    a = agents.get(pane["pane_id"]) or {}
    return a.get("name") or os.path.basename(real(pane.get("cwd", "")).rstrip("/")) or pane["pane_id"]


def resolve(spec, session, snap):
    """member spec -> pane dict in this session"""
    panes = snap.get("panes", [])
    if PANE_ID.match(spec):
        for p in panes:
            if p["pane_id"] == spec:
                return p
        die(f"no pane {spec} in session {session}")
    named = [a["pane_id"] for a in snap.get("agents", []) if (a.get("name") or "") == spec]
    if len(named) == 1:                        # an agent name (herdr-team names every member)
        return next(p for p in panes if p["pane_id"] == named[0])
    if len(named) > 1:
        die(f"agent name {spec} is used by {len(named)} panes in {session}: " + ", ".join(named))
    if "/" not in spec:                        # a folder name: the repo the agent runs in
        base = [p for p in panes if p.get("agent") and os.path.basename(real(p.get("cwd")).rstrip("/")) == spec]
        if len(base) == 1:
            return base[0]
        if len(base) > 1:
            die(f"{spec} is the folder of {len(base)} agents in {session}: " + ", ".join(p["pane_id"] for p in base)
                + " — pass a name or a pane id")
    want = real(spec)
    hits = [p for p in panes if real(p.get("cwd")) == want]
    agents = [p for p in hits if p.get("agent")]
    pick = agents if agents else hits
    if len(pick) == 1:
        return pick[0]
    if len(pick) > 1:
        die(f"{spec} matches {len(pick)} panes in {session}: " + ", ".join(p["pane_id"] for p in pick)
            + " — pass the pane id instead")
    for s in sessions():
        if s != session and any(real(p.get("cwd")) == want for p in snapshot(s).get("panes", [])):
            die(f"{spec} runs in session '{s}', not '{session}'. Panes cannot cross herdr sessions: "
                f"use --session {s}, or move that agent into {session} first (resume pattern)")
    die(f"no pane with cwd {spec} in session {session}")


def worktree_root(path):
    """main checkout of a linked git worktree, else None"""
    def git(*a):
        r = subprocess.run(["git", "-C", path, "rev-parse", *a], capture_output=True, text=True)
        return real(os.path.join(path, r.stdout.strip())) if r.returncode == 0 and r.stdout.strip() else ""
    gd, common = git("--git-dir"), git("--git-common-dir")
    return os.path.dirname(common) if gd and common and gd != common else None


def room_ws(snap, room):
    for w in snap.get("workspaces", []):
        if (w.get("label") or "").lower() == room.lower():
            return w
    return None


def plan(layout, n, ratio):
    """(target index, direction, share the target keeps) for members 2..n"""
    steps = []
    for k in range(1, n):                      # k = index of the member being placed (0-based)
        if layout == "cols":
            steps.append((k - 1, "right", round(1 / (n - k + 1), 3)))
        elif layout == "rows":
            steps.append((k - 1, "down", round(1 / (n - k + 1), 3)))
        elif layout == "main":
            steps.append((0, "right", ratio) if k == 1 else (k - 1, "down", round(1 / (n - k + 1), 3)))
        else:                                  # fib: spiral, every target keeps half
            steps.append((k - 1, "right" if k % 2 == 1 else "down", 0.5))
    return steps


class Mover:
    def __init__(self, session, dry):
        self.s, self.dry, self.n, self.inside = session, dry, 0, set()

    def move(self, pane, *args, label=""):
        self.n += 1
        cmd = ["pane", "move", pane, *args, "--no-focus"]
        print(f"  {'plan' if self.dry else 'run '}  herdr --session {self.s} {' '.join(cmd)}" + (f"   # {label}" if label else ""))
        if self.dry:   # a move inside one space keeps the id; into another space, the id changes
            pid = pane if pane in self.inside else f"<{pane} new id>"
            self.inside.add(pid)
            return {"pane": {"pane_id": pid, "tab_id": "<room tab>"},
                    "created_tab": {"tab_id": "<scratch tab>"}, "created_workspace": {"workspace_id": "<room>"}}
        return herdr(self.s, *cmd).get("move_result", {})


def repo_root(path):
    """the repo a checkout belongs to: the main checkout of a linked worktree, else the checkout itself"""
    return worktree_root(path) or path


def place_after_repo(session, dry, wid, repo, fallback=None, why="", skip=()):
    """put space `wid` right after the last other space of `repo` in the sidebar order (else after `fallback`).
    A new space lands at the end of the sidebar (2026-10-29: rd-team out left neo and nexus at 13/14, the room at 7).
    `skip`: spaces of this run not placed yet (still at the end), so they are no anchor."""
    if dry:
        print(f"  plan  herdr --session {session} workspace move {wid} --after <last space of {os.path.basename(repo)}"
              f"{' or ' + fallback if fallback else ''}>   # {why}")
        return
    order = sorted(snapshot(session).get("workspaces", []), key=lambda w: w.get("number") or 0)
    same = [w["workspace_id"] for w in order if w["workspace_id"] != wid and w["workspace_id"] not in skip
            and real((w.get("worktree") or {}).get("repo_root")) == repo]
    after = same[-1] if same else fallback
    ids = [w["workspace_id"] for w in order]
    if not after or after not in ids or wid not in ids:
        return
    if ids.index(wid) == ids.index(after) + 1:
        print(f"  ok    {wid} already right after {after}   # {why}")
        return
    print(f"  run   herdr --session {session} workspace move {wid} --after {after}   # {why}")
    r = subprocess.run(["herdr", "--session", session, "workspace", "move", wid, "--after", after], capture_output=True, text=True)
    if r.returncode != 0:   # an older herdr has no `workspace move`: the spaces stay where herdr put them
        print(f"  ! workspace move failed: {(r.stderr or r.stdout).strip()[:200]}")


def save(session, room, layout, members):
    os.makedirs(STATE, exist_ok=True)
    path = os.path.join(STATE, f"{session}__{room}.json")
    with open(path, "w") as f:
        json.dump({"room": room, "session": session, "layout": layout, "members": members,
                   "saved": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, f, indent=2)
    return path


def load(session, room):
    try:
        with open(os.path.join(STATE, f"{session}__{room}.json")) as f:
            return json.load(f)
    except OSError:
        return None


def rename_all(session, ids_names, dry):
    for pid, name in ids_names:
        if dry:
            continue
        r = subprocess.run(["herdr", "--session", session, "agent", "rename", pid, name], capture_output=True, text=True)
        ok = r.returncode == 0 and '"error"' not in r.stdout
        print(f"  name  {pid} = {name}" + ("" if ok else "   (not an agent: skipped)"))


def show_layout(session, pane):
    lay = herdr(session, "pane", "layout", "--pane", pane).get("layout", {})
    for p in sorted(lay.get("panes", []), key=lambda p: (p["rect"]["x"], p["rect"]["y"])):
        r = p["rect"]
        print(f"  rect  {p['pane_id']:8s} x={r['x']:<4d} y={r['y']:<3d} {r['width']}x{r['height']}")


def cmd_in(room, specs, layout, ratio, session, dry):
    snap = snapshot(session)
    state = load(session, room)
    if not specs:
        if not state:
            die(f"no members given and nothing saved for room '{room}' in {session}")
        live = {a.get("name") for a in snap.get("agents", []) if a.get("name")}
        specs = [m["name"] if m.get("name") in live else (m.get("path") or m["pane"]) for m in state["members"]]
        layout = layout or state.get("layout", "fib")
    layout = layout or "fib"
    agents = {a["pane_id"]: a for a in snap.get("agents", [])}
    names = {m["path"]: m["name"] for m in (state or {}).get("members", []) if m.get("path")}
    ws = room_ws(snap, room)
    members = []
    for spec in specs:
        p = resolve(spec, session, snap)
        if p["pane_id"] in [m["pane"] for m in members]:
            continue
        members.append({"pane": p["pane_id"], "path": real(p.get("cwd")),
                        "name": names.get(real(p.get("cwd"))) or name_of(p, agents), "ws": p["workspace_id"]})
    if ws:   # the room is open: keep everyone inside it; new members join at the end
        order_paths = [m["path"] for m in (state or {}).get("members", [])]
        pos = {}
        for l in snap.get("layouts", []):
            for lp in l.get("panes", []):
                pos[lp["pane_id"]] = (lp["rect"]["x"], lp["rect"]["y"])
        inside = [p for p in snap.get("panes", []) if p["workspace_id"] == ws["workspace_id"]]
        inside.sort(key=lambda p: (order_paths.index(real(p.get("cwd"))) if real(p.get("cwd")) in order_paths else 99,
                                   pos.get(p["pane_id"], (0, 0))))
        existing = [{"pane": p["pane_id"], "path": real(p.get("cwd")),
                     "name": names.get(real(p.get("cwd"))) or name_of(p, agents), "ws": p["workspace_id"]} for p in inside]
        ids = {m["pane"] for m in existing}
        if members and members[0]["pane"] in ids:      # the caller's order wins when it starts inside the room
            members = members + [m for m in existing if m["pane"] not in {x["pane"] for x in members}]
        else:
            members = existing + [m for m in members if m["pane"] not in ids]
    if len(members) < 2:
        die("a room needs at least 2 members")
    print(f"room '{room}' · session {session} · layout {layout} · {len(members)} members: "
          + ", ".join(m["name"] for m in members))
    mv = Mover(session, dry)
    first = members[0]
    # 1. the first member alone in the room's main tab
    if ws is None:
        r = mv.move(first["pane"], "--new-workspace", "--label", room, "--tab-label", room, label=f"{first['name']} opens the room")
        first["pane"], main_tab = r["pane"]["pane_id"], r["pane"]["tab_id"]
        room_id = r.get("created_workspace", {}).get("workspace_id", "<room>")
    else:
        room_id = ws["workspace_id"]
        if first["ws"] != room_id:
            die(f"room '{room}' exists; its first member must already be inside it (run `herdr-room out {room}` first to rebuild with a new first member)")
        main_tab = next((p["tab_id"] for p in snap["panes"] if p["pane_id"] == first["pane"]), None)
    # 2. everyone else into a scratch tab in the room (same space: ids stop changing)
    rest, scratch = members[1:], None
    for m in rest:
        if scratch is None:
            r = mv.move(m["pane"], "--new-tab", "--workspace", room_id, "--label", "scratch", label=f"{m['name']} to scratch")
            scratch = r.get("created_tab", {}).get("tab_id") or r["pane"]["tab_id"]
            anchor = r["pane"]["pane_id"]
        else:
            r = mv.move(m["pane"], "--tab", scratch, "--target-pane", anchor, "--split", "right", label=f"{m['name']} to scratch")
        m["pane"] = r["pane"]["pane_id"]
    # 3. back into the main tab, each share set inside its move
    order = [first] + rest
    for k, (ti, d, keep) in enumerate(plan(layout, len(order), ratio), start=1):
        r = mv.move(order[k]["pane"], "--tab", main_tab, "--target-pane", order[ti]["pane"], "--split", d, "--ratio", str(keep),
                    label=f"{order[k]['name']} beside {order[ti]['name']}, which keeps {keep}")
        order[k]["pane"] = r["pane"]["pane_id"]
    rename_all(session, [(m["pane"], m["name"]) for m in order], dry)
    if ws is None:   # a new room space: beside its first member's repo, not at the end of the sidebar
        place_after_repo(session, dry, room_id, repo_root(first["path"]), why=f"room {room} beside {first['name']}'s repo")
    if dry:
        print(f"  --dry: nothing was moved ({mv.n} moves planned)")
        return
    print(f"  saved {save(session, room, layout, [{'path': m['path'], 'pane': m['pane'], 'name': m['name']} for m in order])}")
    show_layout(session, first["pane"])


def cmd_out(room, session, dry, specs=()):
    snap = snapshot(session)
    ws = room_ws(snap, room)
    if ws is None:
        die(f"no space '{room}' in session {session}")
    agents = {a["pane_id"]: a for a in snap.get("agents", [])}
    state = load(session, room)
    known = {m["path"]: m["name"] for m in (state or {}).get("members", []) if m.get("path")}
    order_paths = [m["path"] for m in (state or {}).get("members", [])]
    panes = [p for p in snap.get("panes", []) if p["workspace_id"] == ws["workspace_id"]]
    lay = {}
    for l in snap.get("layouts", []):
        for lp in l.get("panes", []):
            lay[lp["pane_id"]] = (lp["rect"]["x"], lp["rect"]["y"])
    panes.sort(key=lambda p: (order_paths.index(real(p.get("cwd"))) if real(p.get("cwd")) in order_paths else 99,
                              lay.get(p["pane_id"], (0, 0))))
    members = [{"pane": p["pane_id"], "path": real(p.get("cwd")),
                "name": (agents.get(p["pane_id"]) or {}).get("name") or known.get(real(p.get("cwd"))) or name_of(p, agents)}
               for p in panes]
    if not dry:                                # the saved room is always the whole room
        print(f"  saved {save(session, room, (state or {}).get('layout', 'fib'), members)}")
    if specs:                                  # split: only the named members leave
        leaving = {resolve(sp, session, snap)["pane_id"] for sp in specs}
        stray = leaving - {m["pane"] for m in members}
        if stray:
            die(f"not in room '{room}': " + ", ".join(sorted(stray)))
        members = [m for m in members if m["pane"] in leaving]
    print(f"room '{room}' · session {session} · {len(members)} member(s) out: " + ", ".join(m["name"] for m in members))
    # a space with the member's label is home only when it is not some OTHER checkout's space: two spaces can
    # carry one label (2026-10-29: rd-team out sent Nexus from wt/nexus-oracle into the nexus-oracle MAIN repo's
    # space, beside another live Nexus)
    def label_home(m):
        for w in snap.get("workspaces", []):
            if (w.get("label") or "") != m["name"]:
                continue
            wt = w.get("worktree")
            if not wt or real(wt.get("checkout_path")) == m["path"]:
                return w["workspace_id"]
        return None
    mv = Mover(session, dry)
    moved = []
    # sidebar nesting under the repo needs the space's own worktree flag, which only `worktree open/create`
    # sets; a plain `--new-workspace` came out flat (2026-10-06, floodboy room)
    wt_spaces = {real((w.get("worktree") or {}).get("checkout_path")): w["workspace_id"]
                 for w in snap.get("workspaces", []) if w.get("worktree")}
    for m in members:
        root = worktree_root(m["path"])
        home = wt_spaces.get(m["path"]) if root else None   # a helper pane can keep the old worktree space alive
        home = home or label_home(m)
        if home and home != ws["workspace_id"]:
            r = mv.move(m["pane"], "--workspace", home, "--new-tab", label=f"{m['name']} into its existing space {home}")
        else:
            r = mv.move(m["pane"], "--new-workspace", "--label", m["name"], label=f"{m['name']} to a space of its own")
        moved.append((r["pane"]["pane_id"], m["name"]))
    # only after EVERY move: while the room space is alive, `worktree open` can attach to the room itself,
    # which then closes, leaving the member flat (2026-10-06 test: first member flat, last one nested)
    for m in members:
        root = worktree_root(m["path"])
        if root:
            print(f"  {'plan' if dry else 'run '}  herdr --session {session} worktree open --cwd {root} --path {m['path']}"
                  f" --label {m['name']} --no-focus   # nest {m['name']} under its repo")
            if not dry:
                herdr(session, "worktree", "open", "--cwd", root, "--path", m["path"], "--label", m["name"], "--no-focus")
    rename_all(session, moved, dry)
    # each member's space right after its repo's spaces (the room, for a team's members), in member order
    room_alive = dry or any(w["workspace_id"] == ws["workspace_id"] for w in snapshot(session).get("workspaces", []))
    where = {} if dry else {p["pane_id"]: p["workspace_id"] for p in snapshot(session).get("panes", [])}
    wids = [where.get(pid) if not dry else f"<{name}'s space>" for pid, name in moved]
    pending = {w for w in wids if w}
    for (pid, name), m, wid in zip(moved, members, wids):
        if wid:
            pending.discard(wid)
            place_after_repo(session, dry, wid, repo_root(m["path"]), fallback=ws["workspace_id"] if room_alive else None,
                             why=f"{name} beside its repo", skip=pending)
    if dry:
        print("  --dry: nothing was moved")
        return
    # say what is TRUE: a split (`out <room> <member>`) leaves the room open with whoever stayed
    # (2026-10-05: it printed "closed itself once empty" while Pulse was still in the room)
    left = [p["pane_id"] for p in snapshot(session).get("panes", []) if p["workspace_id"] == ws["workspace_id"]]
    if left:
        print(f"  the room stays open with {len(left)} pane(s): {', '.join(left)} · `herdr-room in {room}` brings the others back")
    else:
        print(f"  the room space closed itself once empty · `herdr-room in {room}` rebuilds it")


def cmd_rename(room, new, session):
    snap = snapshot(session)
    ws = room_ws(snap, room)
    if room_ws(snap, new):
        die(f"a space named '{new}' already exists in {session}")
    if ws:
        herdr(session, "workspace", "rename", ws["workspace_id"], new)
        for l in snap.get("layouts", []):
            if l.get("workspace_id") == ws["workspace_id"]:
                herdr(session, "tab", "rename", l["tab_id"], new)
        print(f"  space {ws['workspace_id']} and its tab(s): '{room}' -> '{new}'")
    old = os.path.join(STATE, f"{session}__{room}.json")
    if os.path.exists(old):
        d = json.load(open(old)); d["room"] = new
        json.dump(d, open(os.path.join(STATE, f"{session}__{new}.json"), "w"), indent=2)
        os.remove(old)
        print(f"  saved state: {session}__{room}.json -> {session}__{new}.json")
    if not ws and not os.path.exists(os.path.join(STATE, f"{session}__{new}.json")):
        die(f"no room '{room}' in {session} (no open space, no saved state)")


def cmd_list():
    if not os.path.isdir(STATE):
        print("no rooms saved")
        return
    for f in sorted(os.listdir(STATE)):
        if f.endswith(".json"):
            d = json.load(open(os.path.join(STATE, f)))
            # a stopped session must not crash the whole list (2026-10-11: session ccdc was stopped)
            snap = herdr(d["session"], "api", "snapshot", check=False).get("snapshot")
            state = "down" if snap is None else ("OPEN" if room_ws(snap, d["room"]) is not None else "out ")
            print(f"{d['session']:12s} {d['room']:16s} {d['layout']:5s} {state}  "
                  + " · ".join(m["name"] for m in d["members"]) + f"   (saved {d['saved']})")


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return
    def opt(name, default=None):
        if name in argv:
            i = argv.index(name)
            v = argv[i + 1] if i + 1 < len(argv) else die(f"{name} needs a value")
            del argv[i:i + 2]
            return v
        return default
    dry = "--dry" in argv
    argv = [a for a in argv if a != "--dry"]
    session = opt("--session", os.environ.get("HERDR_SESSION") or "default")
    layout = opt("--layout")
    ratio = float(opt("--ratio", "0.5"))
    if layout and layout not in ("fib", "cols", "rows", "main"):
        die("--layout is fib, cols, rows or main")
    verb, rest = argv[0], argv[1:]
    if verb == "list":
        return cmd_list()
    if not rest:
        die(f"usage: herdr-room {verb} <room> …")
    if verb == "in":
        return cmd_in(rest[0], rest[1:], layout, ratio, session, dry)
    if verb == "out":
        return cmd_out(rest[0], session, dry, rest[1:])
    if verb == "rename":
        if len(rest) != 2:
            die("usage: herdr-room rename <room> <new-name> [--session S]")
        return cmd_rename(rest[0], rest[1], session)
    die(f"unknown verb '{verb}' (in, out, rename, list)")


if __name__ == "__main__":
    main(sys.argv[1:])
~~~~

## 12. The full skill (`~/.claude/skills/herdr-room/SKILL.md`)

~~~~markdown
---
name: herdr-room
description: Pull live agents into one room (a herdr space whose single tab shows them all, fib/cols/rows/main layout) and send them back to spaces of their own, back and forth as often as you like, with no restart — real panes move and the member list is saved so `in` rebuilds the same room. Works from any pane in any session. Use when the user says "war room", "bring them into one room", "put X Y Z on one page", "send them back to their own spaces", "back and forth", "team page", "herdr-room", or wants a group view of several oracles and then their own spaces again. Do NOT use to start new agents from a charter (use /herdr-team), to move an agent between herdr sessions (panes cannot cross sessions — use the resume pattern in /herdr-bring), or to list where an oracle runs (use /herdr-info).
argument-hint: "in <room> [member…] [--layout fib|cols|rows|main] [--session S] [--dry] | out <room> [member…] [--session S] [--dry] | rename <room> <new> | list"
---

# /herdr-room — one page for a team, then back to their own spaces

Script: `~/.local/bin/herdr-room` (python3, calls `herdr --session S pane move` with exact pane ids).

```bash
herdr-room in  war-room ~/Code/github.com/Soul-Brews-Studio/kvmbox-oracle \
                        ~/Code/github.com/Soul-Brews-Studio/vpskeeper-oracle \
                        ~/Code/github.com/laris-co/gateway-oracle \
               --layout fib --session homekeeper --dry          # plan first, always
herdr-room out war-room --session homekeeper                     # each back to a space of its own
herdr-room out war-room vpskeeper-oracle --session homekeeper    # split: only that one leaves
herdr-room in  war-room --session homekeeper                     # rebuild the same room from saved state
herdr-room in  war-room /path/to/another-oracle --session homekeeper   # add a member: joins at the end
herdr-room in  war-room --layout cols --session homekeeper       # re-tile the open room
herdr-room list                                                  # saved rooms, OPEN or out
herdr-room rename war-room ops --session homekeeper             # space label + tab label + saved state
```

## Members
- An **agent name** (herdr-team names every member), a **folder name** (`gateway-oracle`), a
  **folder path** (the agent's cwd), or a **pane id** in that session. Prefer names and folders:
  pane ids repeat across herdr sessions (`w8:p2` was both office and war-room on 2026-10-05).
- A path matching several agents in one session is refused with the candidates; pass the pane id.
- A member found only in another session is refused with that session's name. Panes cannot cross
  herdr sessions; move the agent first (new pane waits for the old pid, then resumes — /herdr-bring).

## Layouts — the share is set inside each move (no resize afterwards, so no extra redraw)
| layout | shape |
|---|---|
| `fib` (default) | first member the left half; each next takes half of what is left, turning right/down (3: left · top-right · bottom-right; 4: … · bottom-right splits into two) |
| `cols` / `rows` | equal columns / rows in member order |
| `main` | first member a left column of share `--ratio` (default 0.5), the rest stacked right |

## How it moves (why it works from anywhere)
1. The first member opens the room: `pane move --new-workspace --label <room>` (or is already in it).
2. Every other member goes to a scratch tab in the room's space. Inside one space a pane keeps its id.
3. Each comes back into the main tab with `--split` and `--ratio` = the share the TARGET keeps.
   The scratch tab closes itself when empty; so does any space a member left empty.
4. Every member is renamed (herdr drops an agent's name on a move); shells are skipped.

`out` sends each member to a space labelled with its name (its existing space if one has that label),
saves the order and layout, and the room closes itself once empty.

**Worktree members are nested again** (fixed 2026-10-06). Sidebar nesting under the repo comes from a
flag on the SPACE (`worktree_space`), which only `herdr worktree create/open` sets. A plain
`pane move --new-workspace` gives a flat space, which is how the floodboy room broke out into 5 flat
spaces. `out` now:
1. Sends a member whose cwd is a linked git worktree back to the space that still holds that worktree,
   if any (a helper pane can keep the old worktree space alive). Otherwise it makes a new space.
2. After **all** moves, runs `herdr worktree open --cwd <repo> --path <wt> --label <name> --no-focus`
   for each worktree member. On a space already at that path it attaches the identity in place
   (`already_open: true`; no pane moves, the agent is untouched).

Order matters: an early `worktree open`, run while the room still exists, attached to the room, which
then closed. In the test the first member came out flat and the last one nested.

## With /herdr-team (split a team into spaces, merge it back)
/herdr-team starts a team in ONE space — the worktree's own space, Fibonacci, every member named.
That space is a room like any other:

```bash
herdr-room out <team-space> omp-rain omx-wind --session laris-co   # those two get spaces of their own
herdr-room in  <team-space> --session laris-co                      # back into the team's page
```

- Name the members to split. `out` with no members moves EVERYONE, the lead's pane included.
- A herdr space is not a git worktree: split members still share the worktree's folder and files.
  For a member with its own branch and folder, start it with /herdr-wt instead (a running agent
  cannot change its folder).

## Moving a body (an agent's pane moves to another checkout) — order matters
Met 2026-10-31 in laris-co room `aiexpo-oracle` (wCC): the old body (wCC:p3, a course-team worktree)
split a new pane down with cwd = the main checkout, started `claude` there, and set timers to
`/exit` + `pane close` itself 20-40 s later. The new body ran `herdr-room in` at 20:05:38, before
the old pane had gone: 3 members, 3 columns. A second `in` at 20:06:04, after the close: 2.
Reproduced on fake agents (`pane report-agent`) in a scratch session; proof book
`Caeruleus-Lab/aiexpo-oracle` `ψ/writing/proof-books/2026-10-31_herdr-body-move/` (commit 5124342).

1. New pane in the room's space, cwd = the new checkout; start the new body there with a brief.
2. The OLD body leaves the space: `herdr pane close <old>`, or `herdr-room out <room> <old> --dry`
   first (out also runs `worktree open` for a worktree member, giving it a space of its own).
3. Wait until `herdr agent list` no longer shows the old pane. Never on a timer you only hope fired.
4. Only now: `herdr-room in <room> <new> <peer> --layout <x> --session <s>`, then `herdr-room list`.
5. Tell the peers the new pane id (ids change on every move).

## State
`~/.local/state/herdr-room/<session>__<room>.json` — members (path, last pane id, name), layout, time.

## Traps (met 2026-10-05)
| trap | handled |
|---|---|
| `maw herdr join` from another session: "pane … not found" (it fills the tab of the pane it runs in) | herdr-room never uses "the pane I run in" |
| same pane id in two sessions → maw refuses as ambiguous, even with `--session` | members by path |
| agent name lost after a move or a swap | renamed after every move |
| moving into a zoomed tab returns `changed:false` silently | unzoom first (not automated yet) |
| a re-layout that resizes afterwards makes every agent redraw twice | shares set inside the moves |
| `out` gave worktree agents FLAT spaces, not nested under their repo (2026-10-06) | `worktree open` per worktree member, after all moves |
| `worktree open` while the room is alive attaches to the room (first member flat) | runs only after every move |
| `pane move --split left` → `invalid split direction` | only `right` / `down` exist |
| `pane move` into an existing space: the result has no `pane` key | look the pane up by `agent list` |
| `in` on an OPEN room keeps every pane already inside its space, typed or not (2026-10-31: the old body was still in the space, so `in <new> <wt>` gave 3 columns) | by design (`if ws:` branch, ~line 235): the old pane must LEAVE first. See "Moving a body" above |
| editing the state file to drop a member does nothing while the room is open | members are rebuilt from the panes in the space; the state only orders them |
| two agents moving or renaming at once: pane ids change mid-check (nsm 10-08, neo 10-11, relic4-scan 10-31) | only the desk runs `in`/`out`; everyone else `--dry` |
| `out` nested the worktree member under the WRONG parent: a second plain space whose cwd was inside the same repo (a capture space at `ψ/writing/proof-books/...`, label `proof-book`) came first in the sidebar, and `worktree open` linked the wt to it (2026-10-31) | keep ONE plain space per repo (the main oracle's). Close any extra space in that repo before `out`. If it already happened: `in` (frees the link), `workspace close <extra>` (without `--group`, which would close the wt's space too), `out` again |
| `workspace close` on that extra space: `workspace_group_close_required` | it now owns the linked wt; `--group` closes the wt agent's space as well. Room `in` first, then close |
| `herdr-room list` shows OPEN after `out` | the main oracle's own space carries the room's label; harmless (`in` uses it), but `list` cannot tell out from open |

Proven on throwaway shells in session laris-co (2026-10-05): fib 3 → out → in from state → add a 4th
(fib spiral 88x44 | 88x22 / 44x22 · 44x22) → cols → out → all spaces closed.
Proven on throwaway **worktrees** in session ccdc (2026-10-06): 2 linked worktrees → in → out → both
`WT` (nested); before the order fix it gave `t-a FLAT, t-b WT`. The 2026-10-05 tests used plain shells
only, which is why the worktree case slipped through. Test with worktrees whenever members can be worktrees.
~~~~

## 13. Sources

- Every output in this lesson: [`captures/`](captures/) (run 31 Oct 2026, herdr 0.9.5)
- The rules in section 9 come from the notes of media-team, rd-team, manager-team and AIExpo Oracle, 5 to 31 Oct 2026, found with relic5
