---
name: herdr-link-teardown
description: Remove a worker oracle from another machine cleanly — drop the saved machine here, disable its systemd user unit, remove only its roster row (backup first), restore and remove its worktree, delete its branch with -d. Use when the user says "remove the worker", "tear down", "clean up the demo", "undo provision". Part of the /herdr-link package.
---

# /herdr-link-teardown — leave the box as it was

Proven 2026-10-11 (proof book run 2, captures 30–33): neo-demo removed; only the stopped `demo`
session folder stayed on white.

```bash
herdr-link teardown nat@white.follow-rankine.ts.net demo neo-demo          # dry plan
herdr-link teardown nat@white.follow-rankine.ts.net demo neo-demo --go
```

## By hand, in this order

```bash
# 1. here: forget the remote session
herdr machine remove $(herdr machine list | awk '$2=="white-demo"{print $1}')

# 2. there: stop it booting
systemctl --user disable --now herdr-session@demo

# 3. there: remove ONLY this worker's roster row (backup first)
R=~/.config/herdr/plugins/config/nsm.oracle-autostart/roster.tsv
cp -p "$R" "$R.bak-$(date +%Y%m%d-%H%M)"
awk -F'\t' '!($1=="demo" && $3=="neo-demo")' "$R" > "$R.new" && mv "$R.new" "$R"

# 4. there: restore the tracked .envrc, then remove the worktree and its branch
cd /opt/Code/github.com/laris-co/neo-oracle
git -C wt/neo-demo-athena-11oct-sun2026 checkout -- .envrc
git worktree remove wt/neo-demo-athena-11oct-sun2026
git branch -d agents/neo-demo
```

## Traps

| trap | avoid |
|---|---|
| `git worktree remove` → "contains modified or untracked files" | the copied `.envrc` modifies a tracked file — `checkout -- .envrc` first; never `--force` blindly (look at `git status` first: real work may be there) |
| `git branch -d` refuses (unmerged commits) | the worker made commits — push them / open a PR, ask the human; never `-D` |
| restoring the roster from an old `.bak` | rows added since then are lost — filter out the one row instead |
| the session folder `~/.config/herdr/sessions/<s>` is left | fine: stopped, harmless; it keeps the layout if the worker comes back |
| teardown of a REAL worker (neo-white, nexus-white) | ask the human first — those carry conversations and work |
