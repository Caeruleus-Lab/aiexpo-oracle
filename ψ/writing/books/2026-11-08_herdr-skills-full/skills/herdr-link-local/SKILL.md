---
name: herdr-link-local
description: Give an oracle its own herdr session on this machine (m5) — move all its agents out of a shared session like laris-co into session <name>, same conversations, empty spaces closed. Use when the user says "create <oracle> session", "session per oracle", "move nexus into its own session", "local session". Part of the /herdr-link package. Do NOT use for another machine (use /herdr-link-remote).
---

# /herdr-link-local — one herdr session per oracle

Proven 2026-10-11: `~/.local/bin/herdr-move nexus-oracle` moved 4 Nexus agents from `laris-co` into a new
session `nexus` (16bedad6 → w1:p1, 0243bb79 → w2:p1, 13e2c4c7 → w3:p1, cd2c4b12 → w4:p1). Nat: "that exactly cool!"

## Steps

```bash
herdr session list | rg -v stopped                 # what runs now
~/.local/bin/herdr-move nexus-oracle --dry         # who moves, from where — nothing changes
~/.local/bin/herdr-move nexus-oracle               # into session "nexus" (repo name minus -oracle)
~/.local/bin/herdr-move nexus-oracle --to laris-co # or into an existing session
herdr --session nexus agent list                   # new pane ids; names are gone
herdr --session nexus agent rename w1:p1 nexus     # give names back if you want them
```

`herdr-move` ends each agent, waits until its id is gone, closes the oracle's spaces left holding only idle
shells, starts the target session, and resumes every conversation there. It refuses to move the pane it runs in.

## After the move

- Address agents by **pane id**: names are cleared, and two sessions may hold the same name.
- A space where something still runs (a shell after claude left) stays in the old session — e.g. `laris-co`
  kept an empty `nexus-oracle` space `w28`. Close it only after looking: `herdr --session laris-co pane list`.
- Remote copies of this session open by themselves in the new window when the saved machine's
  `--remote-session` has the same name (`fold_machines_by_session = true` on m5).

## Traps

| trap | avoid |
|---|---|
| `herdr session list` shows a typo session (`laris-c`, `neo-session`) with 0 agents | check `agent list` = 0, then `herdr session stop <s>` (the folder stays) |
| sending by agent name after a move | names are gone — use pane ids, re-list first |
| `default` keeps coming back after you stop it | Neo.app hub autostart (#116) restarts sessions saved within 15 min of boot; remote attaches start sessions too |
