#!/usr/bin/env python3
"""wt_table.py — every worktree of this repo as one boxed table, measured now.

  python3 -I wt_table.py [--repo <path>] [--no-size] [--no-fleet]

Columns: #, worktree (relative to the repo, ~ for herdr's own), branch ("same" when it equals the folder name),
size (du -sh), space (herdr workspace id), state (fleet tier + why + the agent living there).
Tiers (fleet audit): A folder gone · B merged, clean · C pushed, not merged · D uncommitted/local-only work · K keep
(agent working, or gitignored data over the cap). Read-only: it never changes a worktree, a space or a branch.
"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor


def sh(*a, cwd=None):
    r = subprocess.run(a, capture_output=True, text=True, cwd=cwd)
    return r.stdout if r.returncode == 0 else ""


def js(*a, cwd=None):
    try:
        return json.loads(sh(*a, cwd=cwd) or "null")
    except ValueError:
        return None


args = sys.argv[1:]
base = os.getcwd()
if "--repo" in args:
    base = args[args.index("--repo") + 1]
no_size, no_fleet = "--no-size" in args, "--no-fleet" in args
# Nat's rule (2026-10-09): at most 10 linked worktrees per repo, none created more than 15 days ago.
MAX_WT, MAX_DAYS = int(os.environ.get("WT_MAX", "10")), int(os.environ.get("WT_MAX_DAYS", "15"))   # env override for tests

gcd = sh("git", "-C", base, "rev-parse", "--path-format=absolute", "--git-common-dir").strip()
if not gcd:
    sys.exit(f"✗ {base} is not inside a git repo\n  cd <repo> && python3 -I {sys.argv[0]}")
repo = os.path.dirname(gcd)
origin = sh("git", "-C", repo, "remote", "get-url", "origin").strip()
slug = re.sub(r"\.git$", "", re.sub(r"^.*github\.com[:/]", "", origin))
home = os.path.expanduser("~")

# worktrees, main first
wts, cur = [], {}
for line in sh("git", "-C", repo, "worktree", "list", "--porcelain").split("\n") + [""]:
    if line.startswith("worktree "):
        cur = {"path": line[9:], "branch": ""}
    elif line.startswith("branch "):
        cur["branch"] = line[7:].replace("refs/heads/", "")
    elif line == "" and cur:
        wts.append(cur); cur = {}
real = os.path.realpath
for w in wts:
    w["real"] = real(w["path"])
    w["main"] = w["real"] == real(repo)

# herdr: workspace id per path, agents per path (longest matching worktree path wins, the main checkout is a prefix of wt/)
sessions = [l.split()[0] for l in sh("herdr", "session", "list").split("\n")[1:] if len(l.split()) > 1 and l.split()[1] == "running"]
space, agents = {}, {w["real"]: [] for w in wts}
for s in sessions:
    d = js("herdr", "--session", s, "worktree", "list") or {}
    for x in (d.get("result") or {}).get("worktrees", []):
        if x.get("open_workspace_id"):
            space[real(x["path"])] = (s, x["open_workspace_id"])
    d = js("herdr", "--session", s, "agent", "list") or {}
    for a in (d.get("result") or {}).get("agents", []):
        c = real(a.get("cwd") or "/nonexistent")
        best = max((w["real"] for w in wts if c == w["real"] or c.startswith(w["real"] + "/")), key=len, default=None)
        if best:
            agents[best].append((s, a.get("pane_id"), a.get("agent_status") or "?"))
multi = len({v[0] for v in space.values()}) > 1

# size, in parallel (a 700 GB folder takes a while)
def du(w):
    try:
        r = subprocess.run(["du", "-sh", w["path"]], capture_output=True, text=True, timeout=90)
        return r.stdout.split("\t")[0].strip() or "?"
    except subprocess.TimeoutExpired:
        return ">90s"
if no_size:
    sizes = ["-"] * len(wts)
else:
    with ThreadPoolExecutor(8) as ex:
        sizes = list(ex.map(du, wts))

# fleet's tiers
tier = {}
if not no_fleet and slug:
    d = js("fleet", "audit", "--repo", slug, "--idle-agents", "--idle-shells", "--min-age", "0", "--json", cwd=repo)
    rows = d if isinstance(d, list) else ((d or {}).get("rows") or (d or {}).get("worktrees") or [])
    for r in rows:
        tier[real(r["path"])] = r


def age_days(w):
    """Days since the worktree was created: birth time of its git admin dir (the folder's own as a fallback)."""
    import time
    gd = ""
    try:
        t = open(os.path.join(w["path"], ".git"), encoding="utf-8").read().strip()
        if t.startswith("gitdir:"):
            gd = t[7:].strip()
    except OSError:
        pass
    for p in (gd, w["path"]):
        try:
            return int((time.time() - os.stat(p).st_birthtime) // 86400)
        except (OSError, AttributeError):
            continue
    return None


def disp(w):
    p = w["path"]
    if p == repo:
        return "(main checkout)"
    if p.startswith(repo + "/"):
        return p[len(repo) + 1:]
    return "~" + p[len(home):] if p.startswith(home + "/") else p


def state(w):
    r = tier.get(w["real"])
    parts = []
    if w["main"]:
        n = len([l for l in sh("git", "-C", w["path"], "status", "--porcelain").split("\n") if l])
        parts.append(f"{n} dirty" if n else "clean")
    elif r:
        why = r.get("why") or ""
        t = r.get("tier") or "?"
        pr = r.get("pr") or "-"
        pr = re.sub(r"^#(\d+):MERGED$", r"PR #\1 merged", pr)
        txt = why if pr == "-" or "PR" in why else f"{why} · {pr}"
        txt = re.sub(r"holds ([\d.]+ [KMG]B) gitignored data \(([^)]*)\); move it first", r"\1 data in \2", txt)
        d = r.get("dirty") or 0
        if d and "changed" not in why:
            txt += f" · {d} dirty"
        parts.append(f"{t}: {txt}")
    else:
        parts.append("?")
    for s, p, st in agents.get(w["real"], []):
        parts.append(f"agent {st} {p}")
    return " · ".join(parts)


def group(w):
    p = w["path"]
    return (0 if w["main"] else 1 if p.startswith(repo + "/wt/") else 2 if p.startswith(repo + "/.tmp/") else 3, p)


order = sorted(range(len(wts)), key=lambda i: group(wts[i]))
linked = [i for i in order if not wts[i]["main"]]
mi = next(i for i in order if wts[i]["main"])
m = wts[mi]

import datetime
print(f"{slug}: {len(linked)} worktrees plus the main checkout, measured {datetime.datetime.now():%H:%M} (m5)")
ms = space.get(m["real"])
print(f"Main checkout: {repo}, branch {m['branch'] or '(detached)'}, {state(m)}"
      + (f", space {ms[1]}" if ms else "") + (f", agents {', '.join(a[1] for a in agents[m['real']])}" if agents[m["real"]] else ""))
print()

hdr = ["#", "worktree", "branch", "size", "age", "space", "state"]
body = []
too_old = []
for k, i in enumerate(linked, 1):
    w = wts[i]
    folder = os.path.basename(w["path"])
    br = "same" if w["branch"] == folder else (w["branch"] or "(detached)")
    sp = space.get(w["real"])
    spc = "–" if not sp else (f"{sp[1]}" + (f" ({sp[0]})" if multi else ""))
    ad = age_days(w)
    if ad is not None and ad > MAX_DAYS:
        too_old.append(k)
    agetxt = "?" if ad is None else f"{ad}d" + (" !" if ad > MAX_DAYS else "")
    body.append([str(k), disp(w), br, sizes[i], agetxt, spc, state(w)])
cols = list(zip(*([hdr] + body))) if body else [[h] for h in hdr]
wid = [max(len(c) for c in col) for col in cols]


def line(l, mid, r):
    return l + mid.join("─" * (x + 2) for x in wid) + r


def cells(row):
    return "│" + "│".join(" " + c.ljust(wid[j]) + " " for j, c in enumerate(row)) + "│"


out = [line("┌", "┬", "┐"), cells(hdr), line("├", "┼", "┤")]
for k, row in enumerate(body):
    out.append(cells(row))
    out.append(line("├", "┼", "┤") if k < len(body) - 1 else line("└", "┴", "┘"))
print("\n".join(out))
print()
over = len(linked) > MAX_WT
print(f"Rule: {len(linked)} of {MAX_WT} worktrees" + (" — OVER, retire before cutting a new one" if over else " — ok")
      + f" · {len(too_old)} older than {MAX_DAYS} days" + (f" (rows {', '.join(map(str, too_old))} marked !)" if too_old else " — ok"))
print("Tiers: A folder gone · B merged, clean · C pushed, not merged · D uncommitted or local-only work · K keep (agent working, or data over the cap)")
