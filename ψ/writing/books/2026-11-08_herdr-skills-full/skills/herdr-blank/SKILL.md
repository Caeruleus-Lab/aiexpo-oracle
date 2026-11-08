---
name: herdr-blank
description: "Find herdr spaces whose every pane is a bare idle shell (no agent, nothing running but the shell) in every running session, or one session, or a saved remote machine, and close them with --close. Never closes a space where anything else runs, nor the space it runs in. Use when Nat says 'detect blank shells', 'close the empty spaces', 'clean blank workspaces', 'herdr-blank', or after stopping agents (/exit leaves the shell and its space behind). Do NOT use to stop agents (/herdr-team-ctl, just vacation) or to remove worktrees (/herdr-dissolve)."
argument-hint: "[--session <s>]... [--machine <label>] [--under <path>] [--close] [--json]"
---

# /herdr-blank

Nat, 2026-10-29: *"can we detect all blank shell? it should close workspace"*.

```bash
herdr-blank                                   # list, every running session (dry is the default)
herdr-blank --close                           # close them
herdr-blank --session laris-co --under /opt/Code/github.com/laris-co/manager-team --close   # a stop path
herdr-blank --machine white-laris-co          # a saved remote machine
herdr-blank --json                            # one object per space: session, workspace, label, shells, cwd, action
```

Blank = no pane has an agent, and in EVERY pane the shell itself holds the foreground (`pane process-info`:
`foreground_process_group_id == shell_pid`, every foreground process a shell). Kept:

- any space with an agent, a server, a build, `less`, a claude not yet detected: anything but a shell;
- the space it runs in (popup `HERDR_ACTIVE_PANE_ID`, else the pane whose shell is an ancestor);
- a parent space whose worktree spaces are not all blank (closing it would close the group). Worktree spaces
  close first, then their parent.

`--under <path>` limits it to spaces whose panes all sit in that path: what a stop path uses, so it closes only
its own team's leftovers and never a plain shell Nat keeps open elsewhere.

Stop paths that call it: `herdr-move` closes its own idle spaces already; laris-team `just vacation` and
`/herdr-team-ctl stop` run `herdr-blank --session <s> --under <team repo> --close` after the agents exit.

Tool: `~/.local/bin/herdr-blank`, source `Soul-Brews-Studio/herdr-orca-oracle` `scripts/herdr-blank`.

Tested 2026-10-29 in a scratch session only: 2-shell space closed; `sleep` space, agent space and the caller's
space kept; a parent with a busy worktree child kept, then (child idle) child and parent both closed; `--under`
closed only the team's spaces. Live m5, dry: `neo w1Q laris-meshtastic`, `phd wB access-app-lab`.
