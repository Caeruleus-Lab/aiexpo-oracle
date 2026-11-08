#!/usr/bin/env python3
"""herdr-info: every body of one oracle on this machine.

One soul, many bodies: an oracle can run in several herdr sessions, spaces and panes at once,
in its main checkout or in worktrees. This finds all of them, checks the two rules that break
when bodies share things, and draws each tab that holds one.

  herdr-info.py pulse            # every repo named pulse / pulse-oracle (any org)
  herdr-info.py pulse --no-layout
  herdr-info.py pulse --json

Rules checked:
  one conversation id per body   two live agents on one id write one transcript (interleaved)
  one Discord connection per bot two plugins with the same state dir get every message twice
"""
import json, os, re, subprocess, sys, textwrap

def run(cmd, timeout=10):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout.strip()
    except Exception:
        return ""

def hj(session, *args):
    try:
        return json.loads(run(["herdr", "--session", session, *args]))["result"]
    except Exception:
        return {}

def repos_for(name):
    """Every ghq checkout whose folder is <name> or <name>-oracle, any org."""
    want = {name, f"{name}-oracle"} if not name.endswith("-oracle") else {name, name[:-7]}
    # <ghq root>/<host>/<org>/<repo>: match names directly. `ghq list` walks the whole tree (seconds).
    import glob
    root = run(["ghq", "root"]) or os.path.expanduser("~/Code")
    hits = {p for w in want for p in glob.glob(os.path.join(root, "*", "*", w))}
    return sorted(os.path.realpath(p) for p in hits if os.path.exists(os.path.join(p, ".git")))

# linked worktrees that live OUTSIDE their repo folder (herdr's ~/.herdr/worktrees, orca, incubate):
# real path -> repo root. Filled by linked_outside() in main. Nat, 2026-10-05: herdr-info missed neo's
# worktree-green-meadow-782b agent, which sat in ~/.herdr/worktrees/neo-oracle/, outside the checkout.
EXTRA = {}

def linked_outside(roots):
    """Every linked worktree of these repos whose folder is not inside the repo: path -> repo root."""
    out = {}
    for r in roots:
        for line in run(["git", "-C", r, "worktree", "list", "--porcelain"]).split("\n"):
            if line.startswith("worktree "):
                w = os.path.realpath(line[len("worktree "):])
                if w != r and not w.startswith(r + "/"):
                    out[w] = r
    return out

def under(path, roots):
    path = os.path.realpath(path) if path else ""          # /tmp vs /private/tmp: git prints the real path
    for r in roots:
        if path == r or path.startswith(r + "/"):
            return r
    for w, r in EXTRA.items():
        if r in roots and (path == w or path.startswith(w + "/")):
            return r
    return None

def cwds(pids):
    """pid -> working folder, for many pids in ONE lsof call (one call per pid took 14 s)."""
    pids = [str(p) for p in pids if str(p).isdigit()]
    if not pids: return {}
    res, cur = {}, None
    for line in run(["lsof", "-a", "-d", "cwd", "-p", ",".join(pids), "-Fpn"], timeout=30).split("\n"):
        if line.startswith("p"): cur = int(line[1:])
        elif line.startswith("n") and cur is not None: res[cur] = line[1:]
    return res

def where(cwd, root):
    cwd = os.path.realpath(cwd) if cwd else cwd
    for w, r in EXTRA.items():                             # a worktree outside the repo folder
        if r == root and (cwd == w or cwd.startswith(w + "/")):
            home = os.path.realpath(os.path.expanduser("~"))
            return "wt " + ("~" + w[len(home):] if w.startswith(home + "/") else w) + cwd[len(w):]
    rel = os.path.relpath(cwd, root)
    if rel == ".": return "main"
    parts = rel.split("/")
    return f"wt/{parts[1]}" if parts[0] == "wt" and len(parts) > 1 else rel

# ── layout card ────────────────────────────────────────────────────────────────

CH = {(0,0,1,1):"─",(1,1,0,0):"│",(0,1,0,1):"┌",(0,1,1,0):"┐",(1,0,0,1):"└",(1,0,1,0):"┘",
      (1,1,0,1):"├",(1,1,1,0):"┤",(0,1,1,1):"┬",(1,0,1,1):"┴",(1,1,1,1):"┼",
      (0,0,0,1):"─",(0,0,1,0):"─",(1,0,0,0):"│",(0,1,0,0):"│"}

def axis(bounds, total, target, least):
    """Map herdr cell boundaries to card positions: proportional, but never thinner than `least`."""
    bs = sorted(set(bounds)); pos = {bs[0]: 0}; acc = 0
    for a, b in zip(bs, bs[1:]):
        acc += max(least, round((b - a) / max(1, total) * target)); pos[b] = acc
    return pos

def card(layout, label_of, width=36, height=9):
    a = layout.get("area") or {}
    ps = [p for p in layout.get("panes", []) if p.get("rect")]
    xs = axis([v for p in ps for v in (p["rect"]["x"], p["rect"]["x"] + p["rect"]["width"])], a.get("width", 1), width, 14)
    ys = axis([v for p in ps for v in (p["rect"]["y"], p["rect"]["y"] + p["rect"]["height"])], a.get("height", 1), height, 3)
    W, H = max(xs.values()) + 1, max(ys.values()) + 1
    hz, vt, boxes = set(), set(), []
    for p in ps:
        r = p["rect"]
        x0, x1 = xs[r["x"]], xs[r["x"] + r["width"]]
        y0, y1 = ys[r["y"]], ys[r["y"] + r["height"]]
        hz.update((x, y) for x in range(x0, x1 + 1) for y in (y0, y1))
        vt.update((x, y) for y in range(y0, y1 + 1) for x in (x0, x1))
        boxes.append((x0, y0, x1, y1, p))
    grid = [[" "] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if (x, y) in hz or (x, y) in vt:
                k = (int((x, y) in vt and (x, y - 1) in vt), int((x, y) in vt and (x, y + 1) in vt),
                     int((x, y) in hz and (x - 1, y) in hz), int((x, y) in hz and (x + 1, y) in hz))
                grid[y][x] = CH.get(k, "┼")
    for x0, y0, x1, y1, p in boxes:
        room = x1 - x0 - 2
        for i, text in enumerate(label_of(p)):
            if y0 + 1 + i >= y1 or room < 3: break
            t = text if len(text) <= room else text[:room - 1] + "~"
            for j, c in enumerate(t): grid[y0 + 1 + i][x0 + 2 + j] = c
    return ["".join(r) for r in grid]

def side_by_side(cards, gap=3):
    """Two cards per row, each with its title line above."""
    out = []
    for i in range(0, len(cards), 2):
        pair = cards[i:i + 2]
        wds = [max(len(t), max(len(l) for l in body)) for t, body in pair]
        h = max(len(body) for _, body in pair)
        out.append((" " * gap).join(t.ljust(w) for (t, _), w in zip(pair, wds)).rstrip())
        for k in range(h):
            out.append((" " * gap).join((body[k] if k < len(body) else "").ljust(w)
                                        for (_, body), w in zip(pair, wds)).rstrip())
        out.append("")
    return out


def box_table(head, rows):
    """Bordered table whose cells hold several lines; each row is as tall as its tallest cell."""
    n = len(head)
    w = [max([len(head[i])] + [len(x) for r in rows for x in r[i]]) for i in range(n)]
    sep = lambda l, m, r: l + m.join("─" * (x + 2) for x in w) + r
    line = lambda cells: "│" + "│".join(" " + c.ljust(w[i]) + " " for i, c in enumerate(cells)) + "│"
    out = [sep("┌", "┬", "┐"), line(head), sep("├", "┼", "┤")]
    for k, r in enumerate(rows):
        for j in range(max(len(c) for c in r)):
            out.append(line([c[j] if j < len(c) else "" for c in r]))
        out.append(sep("├", "┼", "┤") if k < len(rows) - 1 else sep("└", "┴", "┘"))
    return out

# ── main ───────────────────────────────────────────────────────────────────────

# a desktop app's own helpers are not bodies: ChatGPT.app runs `codex sandbox` and `codex app-server`
# from inside its bundle, with the folder it last used as cwd (Nat, 2026-10-05: herdr-info counted six
# of them as "neo outside herdr"). An executable inside an .app bundle, or those two subcommands.
APP_HELPER = re.compile(r"^\S*\.app/Contents/\S*(\s|$)|^\S*codex (sandbox|app-server)(\s|$)")

def main():
    argv = sys.argv[1:]
    width = None   # --width N: cap the table at N columns by shortening the Where column
    if "--width" in argv:
        i = argv.index("--width")
        if i + 1 >= len(argv) or not argv[i + 1].isdigit():
            print("--width needs a number of columns"); sys.exit(2)
        width = int(argv[i + 1]); del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print("usage: herdr-info.py <oracle> [--no-layout] [--json] [--width N]"); sys.exit(2)
    name = args[0].lower()
    roots = repos_for(name)
    EXTRA.update(linked_outside(roots))
    space = None   # no oracle by that name: try it as a herdr space label (Nat, 2026-10-05)
    if not roots:
        space = name

    sessions = [s["name"] for s in (json.loads(run(["herdr", "session", "list", "--json"]) or "{}").get("sessions") or [])
                if s.get("running")]
    bodies, shells, tabs, conv_pids = [], [], [], {}
    for s in sessions:
        snap = hj(s, "api", "snapshot").get("snapshot") or {}
        labels = {w["workspace_id"]: w.get("label") for w in snap.get("workspaces", [])}
        agents = {a["pane_id"]: a for a in snap.get("agents", [])}
        hit_tabs = set()
        for p in snap.get("panes", []):
            if space:
                if (labels.get(p["workspace_id"]) or "").lower() != space: continue
                m = re.match(r"(.*?/github\.com/[^/]+/[^/]+)", p.get("cwd") or "")
                root = m.group(1) if m else (p.get("cwd") or "")
                if root and root not in roots: roots.append(root)
            else:
                root = under(p.get("cwd"), roots)
            if not root: continue
            row = dict(session=s, pane=p["pane_id"], space=labels.get(p["workspace_id"]) or "", tab=p.get("tab_id"),
                       agent=p.get("agent"), status=p.get("agent_status"), name=(agents.get(p["pane_id"]) or {}).get("name"),
                       conv=((p.get("agent_session") or {}).get("value") or ""), repo=root.replace("/opt/Code/github.com/", ""),
                       where=where(p["cwd"], root))
            if p.get("agent"):
                bodies.append(row); hit_tabs.add(p.get("tab_id"))
                info = hj(s, "pane", "process-info", "--pane", p["pane_id"]).get("process_info") or {}
                fps = info.get("foreground_processes", [])
                for fp in fps:
                    conv_pids.setdefault(fp.get("pid"), row)
                # the agent's own process (not its MCP children): name matches the agent kind
                kind = (p.get("agent") or "").lower()
                own = [fp for fp in fps if kind and kind in os.path.basename(str(fp.get("argv0") or fp.get("name") or "")).lower()]
                row["pid"] = (own or fps or [{}])[0].get("pid")
            else:
                shells.append(row)
        for l in snap.get("layouts", []):
            if l.get("tab_id") in hit_tabs:
                tabs.append((s, labels.get(l.get("workspace_id")) or "", l, snap, agents))

    # bodies outside herdr: claude / codex processes in these repos that no herdr pane owns
    # one `ps` sweep answers both process questions (each pgrep -f is its own full sweep)
    table = {}
    for line in run(["ps", "-axo", "pid=,ppid=,etime=,command="], timeout=20).split("\n"):
        f = line.split(None, 3)
        if len(f) == 4 and f[0].isdigit(): table[int(f[0])] = (int(f[1]), f[2], f[3])
    procs = [pid for pid, (_, _, cmd) in table.items()
             if re.search(r"(^|/)(claude|codex)( |$)", cmd) and pid not in conv_pids
             and not APP_HELPER.search(cmd)]
    plugins = [pid for pid, (_, _, cmd) in table.items() if re.search(r"bun.*discord", cmd)]
    folder = cwds(set(procs) | {table[p][0] for p in plugins})   # one lsof for both questions

    outside = []   # claude / codex processes in these repos that no herdr pane owns
    for pid in procs:
        cwd = folder.get(pid, "")
        root = under(cwd, roots)
        if not root: continue
        _, up, cmd = table[pid]
        m = re.search(r"--resume ([0-9a-f-]{36})", cmd)
        outside.append(dict(pid=pid, up=up, repo=root.replace("/opt/Code/github.com/", ""), where=where(cwd, root),
                            conv=(m.group(1) if m else ""), cmd=cmd.split()[0]))

    discord = []   # Discord plugins whose claude runs in these repos
    for pid in plugins:
        cwd = folder.get(table[pid][0], "")
        if under(cwd, roots):
            env = run(["ps", "-Eww", "-p", str(pid)])
            m = re.search(r"DISCORD_STATE_DIR=(\S+)", env)
            discord.append(dict(pid=int(pid), where=where(cwd, under(cwd, roots)), state=(m.group(1) if m else "(default dir)")))

    warn = []
    convs = {}
    for b in bodies + outside:
        if b.get("conv"): convs.setdefault(b["conv"], []).append(b.get("pane") or f"pid {b['pid']}")
    for c, who in convs.items():
        if len(who) > 1: warn.append(f"conversation {c[:8]} is live in {len(who)} bodies ({', '.join(who)}): one transcript, interleaved")
    states = {}
    for d in discord: states.setdefault(d["state"], []).append(d["pid"])
    for st, pids in states.items():
        if len(pids) > 1: warn.append(f"{len(pids)} Discord connections share {st.replace('/opt/Code/github.com/', '')}: every message arrives {len(pids)}x")
        if st == "(default dir)": warn.append("a Discord plugin runs with no DISCORD_STATE_DIR: check which state folder it reads (the official plugin falls back to ~/.claude/channels/discord)")

    if space and not bodies and not shells:
        print(f"no oracle checkout named {name} or {name}-oracle in ghq, and no herdr space labelled {name}"); sys.exit(1)

    if "--json" in sys.argv:
        print(json.dumps(dict(oracle=name, repos=roots, worktrees_outside=sorted(EXTRA), bodies=bodies,
                              shells=shells, outside=outside, discord=discord, warnings=warn), indent=2)); return

    print(f"{('space ' + name) if space else name} - {len(bodies)} agent(s) in herdr · {len(outside)} outside herdr · {len(shells)} shell pane(s)")
    print(textwrap.fill("repos: " + " · ".join(r.replace("/opt/Code/github.com/", "") for r in roots), width, subsequent_indent="  ") + "\n"
          if width else "repos: " + " · ".join(r.replace("/opt/Code/github.com/", "") for r in roots) + "\n")

    # layout first (where they sit), list after (the details) — Nat, 2026-10-05
    if "--no-layout" not in sys.argv and tabs:
        cards = []
        for s, label, l, snap, agents in tabs:
            panes = {p["pane_id"]: p for p in snap.get("panes", [])}
            def label_of(p, panes=panes):
                info = panes.get(p["pane_id"], {})
                kind = info.get("agent") or "shell"
                conv = ((info.get("agent_session") or {}).get("value") or "")[:8]
                first = f"{p['pane_id'].split(':')[-1]} {kind}" + (f" · {info.get('agent_status')}" if info.get("agent") else "")
                return [first, conv] if conv else [first]
            cards.append((f"{s} · {label[:24]} ({l['tab_id']})", card(l, label_of)))
        for line in side_by_side(cards): print(line)

    # the list: a markdown table, so Claude Code renders it with borders (Nat, 2026-10-05: "love this")
    me = set(); cur = os.getpid()
    while cur and cur in table and cur not in me:          # this process's ancestors: whoever ran us
        me.add(cur); cur = table[cur][0]
    def up(b):
        if b.get("pid") in me: return "this conversation"
        e = (table.get(b.get("pid")) or (0, "", ""))[1]
        if not e: return "-"
        d, _, hms = e.rpartition("-"); parts = [int(x) for x in hms.split(":")]
        while len(parts) < 3: parts.insert(0, 0)
        h, m, _s = parts; d = int(d or 0)
        return f"{d}d {h}h" if d else (f"{h}h {m}m" if h else (f"{m} min" if m else "<1 min"))
    def place(b):
        if b["where"] == "main": return f"main checkout ({b['repo']})"
        return b["where"]
    if bodies:
        # one row per window = one herdr session (a terminal window shows one session; its spaces are
        # pages in the sidebar). Nat, 2026-10-05: "if same windows can we one row?"
        groups = {}
        for b in bodies: groups.setdefault(b["session"], []).append(b)
        def order(item):
            sess, bs = item
            return (not any(b.get("pid") in me for b in bs), sess)
        uniq = lambda xs: list(dict.fromkeys(xs))
        # box-drawn table: one row per session window, one line per agent inside each cell, so every
        # column lines up per agent (Nat, 2026-10-05: "make 1 cell multilines"; markdown cells can't break)
        rows = []
        for sess, bs in sorted(groups.items(), key=order):
            bs.sort(key=lambda b: (b.get("pid") not in me, b["pane"]))
            rows.append([[sess], [b["pane"] for b in bs], [b["agent"] for b in bs],
                         [b["status"] or "-" for b in bs], [place(b) for b in bs], [up(b) for b in bs]])
        if width:   # shorten Where so the whole table fits: 7 borders + 2 spaces of padding per column
            head = ["Session", "Pane", "Agent", "State", "Where", "Up"]
            fixed = sum(max([len(head[i])] + [len(x) for r in rows for x in r[i]]) for i in (0, 1, 2, 3, 5))
            room = max(12, width - fixed - 7 - 12)
            for r in rows:
                r[4] = [x if len(x) <= room else x[:room - 1] + "~" for x in r[4]]
        for line in box_table(["Session", "Pane", "Agent", "State", "Where", "Up"], rows): print(line)
    for o in outside:
        print(f"  outside herdr: pid {o['pid']} up {o['up']} · {o['repo']} {o['where']} · conv {o['conv'][:8] or '-'}")
    wrap = (lambda t, ind="": textwrap.fill(t, width, subsequent_indent=ind)) if width else (lambda t, ind="": t)
    if shells:
        print("\n" + wrap("shell panes (no agent): " + " · ".join(f"{s['session']} {s['pane']}" for s in shells), "  "))
    if discord:
        print(wrap("discord: " + " · ".join(f"pid {d['pid']} ({d['where']})" for d in discord), "  "))
    print("\nwarnings: " + ("none" if not warn else ""))
    for x in warn: print(wrap("  ! " + x, "    "))

main()
