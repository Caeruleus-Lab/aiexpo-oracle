---
name: herdr-move
description: "Move one oracle — every live agent of its repo, main checkout and worktrees — into a herdr session of its own on this machine (default name: repo minus -oracle), resuming each conversation there with its exact id. Use when Nat says 'give <oracle> its own session', 'send maeon to its session', 'move <oracle> to session X', 'bring <oracle> into this session'. Do NOT use to open an oracle that is not running (/herdr-bring) or to arrange panes inside one session (herdr-room)."
argument-hint: "<oracle|repo-path> | --workspace <id> [--from <session>] [--to <session>] [--dry]"
---

# /herdr-move

Nat, 2026-10-09: *"make maeon-craft-oracle create themself session in this m5"*.

```bash
herdr-move <oracle> --dry            # who moves, from which session
herdr-move <oracle>                  # into session <repo minus -oracle>
herdr-move <oracle> --to laris-co    # "bring": into an existing session instead
herdr-move --workspace wAA --from laris-co --to x   # only the agents in one space (any repo)
```

For a whole team or one space by a single name, use `/herdr-promote` (it calls this tool).

herdr panes cannot cross sessions, so the tool ends each agent where it runs and resumes the same conversation in
the target (`maw herdr ticket open … --session <to> --session-id <id>`). Order: end all → wait until every id is gone
(10 s) → close the oracle's spaces left holding only idle shells, worktrees first → start the target if needed →
resume. A space where something still runs (a server) stays.

It refuses to move the pane that runs it, but only after it lists every member: `--dry` marks that pane
(`← this pane: it would be skipped`) and still prints the whole plan, so run the real move from a pane outside the
set. "This pane" is matched by `HERDR_PANE_ID` and by the process tree (the pane's shell pid is an ancestor), since
`HERDR_PANE_ID` goes stale once herdr-room moves a pane. It exits 1 if any conversation was not resumed, and prints
the `maw herdr ticket open …` line to run by hand. Runs on macOS `/bin/bash` 3.2 (no `mapfile`).

Where herdr will not close a pane (the last pane of a space holding worktrees: `confirmation_required`), it sends
SIGHUP to the pane's foreground group, only when claude or codex leads it.

Tool: `~/.local/bin/herdr-move`, source `Soul-Brews-Studio/herdr-orca-oracle` `scripts/herdr-move`. Attach: `herdr --session <to>`.

Tested live 2026-10-09: maeon-craft's 3 idle agents (default:w5X:p1, laris-co:w2Z:p1, laris-co:w32:p1) → new
session `maeon-craft` w1/w2/w3 with the same ids 79da634b · 63f87317 · 0cfb9004; nothing of maeon-craft left in
default or laris-co.
