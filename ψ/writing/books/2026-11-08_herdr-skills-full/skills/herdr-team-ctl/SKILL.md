---
name: herdr-team-ctl
description: Start, stop or check a whole team by its charter name on a herdr session and machine — "start media team on white", "stop the manager team", "status rd". Reads laris-co/laris-team/teams/<team>.yaml, resumes each member on its OWN conversation (session id) in its own folder, rebuilds the team's herdr room, or exits every member cleanly and closes the room. Use when the user says "start <team>", "stop <team>", "shut down <team>", "bring <team> back", "team status", or names a team and a session (laris-co) / machine (m5, white). Part of the /herdr-link package. Do NOT use to create a team's bodies the first time (use /herdr-link-remote, /herdr-link-local) or to remove worktrees (use /herdr-link-teardown).
---

# /herdr-team-ctl — start / stop a team by name

```bash
herdr-team-ctl status <team> [--machine m5|<label>] [--session <herdr session>]
herdr-team-ctl start  <team> [--machine m5|<label>] [--session <s>] [--fresh] [--dry]
herdr-team-ctl stop   <team> [--machine m5|<label>] [--session <s>] [--force] [--dry]
```

- `<team>` = a charter name in `laris-co/laris-team/teams/` (rd-team, manager-team, media-team, …). Charters moved
  there from `pulse-oracle/teams/` (2026-10-27); that folder is history now.
- `--machine m5` (default) uses the charter's `members:`; a machine label (`white-laris-co`) uses the charter's
  `remote:` entries for that machine. `--session` defaults to the charter's `session:` (`laris-co`).
- Built 2026-10-12 after the white mirror: manager, media and rd started and stopped by hand on white
  (guide: `athena-oracle/ψ/writing/2026-10-12_howto-start-white-manager-team.md`).

## What status does (2026-10-29)

`status` is `/team-check`: run `just -f <laris-team>/justfile check <team>` (or `--all`), shipped by
laris-team `skills/team-check` (`just skills-install`). It reads the same charter and every running herdr
session, and reports per member: pane, state, herdr name, sidebar nesting, uncommitted files, and
one soul = one body across sessions. Read-only. For a remote machine, run it there (white has the skill after
`just skills-install`).

## What start does

1. `git pull --ff-only` the laris-team checkout; read the charter.
2. Make sure the herdr session runs on that machine (start the server headless if it is stopped — it restores
   its own panes and agents from `session.json`).
3. For each member that is NOT live (match by **name**, then by cwd):
   - find its conversation: charter `session_id` / `conversation` (8-char prefix → the full id from the
     transcript file name in `~/.claude/projects/<encoded cwd>/`), else the latest m5 snapshot
     (`~/.local/state/m5-sessions/latest.json`), else none → `--fresh` needed;
   - `workspace create --cwd <path> --label <name>`; `pane run` the claude launch line with `-r <full id>`
     (or none with `--fresh`) — **never `--continue`, never `--channels`**, with `PATH=$HOME/.local/bin:$PATH`,
     via `direnv exec .` so the worktree's `.envrc` token loads;
   - trust prompt: wait for `trust this folder` (plain substring — `wait-output --match` is NOT a regex);
     if seen, `Down`, read the screen, `Enter` only when `❯ Yes, I trust this folder` is selected;
   - wait for `bypass permissions on`, then `agent rename <pane> <name>`.
4. `herdr-room in <room> <members…> --session <s>` on that machine (left seat first).
5. Verify: every member live, its session id = the expected one and different from every other body
   (on white read `~/.claude/sessions/<pid>.json`; white's herdr reports no ids).

## What stop does

1. For each member live in the session: skip it (report) if it is `working`/`blocked` unless `--force`.
2. `/exit` + Enter in its pane; wait until its claude process is gone (process files, not `agent list` —
   herdr keeps the name on the leftover shell).
3. Close the room's space (only that space). Worktrees, branches, `.envrc` and conversations stay.
   Then sweep this team's leftovers: `herdr-blank --session <s> --under <team repo> --close` (on a remote
   machine `--machine <label>`). `/exit` leaves each member's shell, and its own space, behind; herdr-blank
   closes only spaces whose every pane is a bare idle shell under the team's repo (2026-10-29, manager-team wAY).
4. Never stop the herdr session itself, never `machine disable`, never remove a worktree or branch.

## Report

One line per member: `name · pane · status · session id · started|stopped|already|skipped (why)`, then the room line.

## Traps (met for real)

| trap | avoid |
|---|---|
| a body comes up on another body's conversation (zsh auto `--continue`, removed 2026-10-12) | always `-r <id>` or `--fresh`; check the id after |
| `wait-output --match 'a\|b'` hangs | one plain substring per wait |
| trust prompt defaults to "No, exit" | Down → read → Enter on Yes only |
| non-interactive ssh has no `~/.local/bin` | `PATH=$HOME/.local/bin:$PATH` first |
| pane ids change after a room in/out or reboot | re-list, address by pane id |
| names prefix-match in `agent prompt` | use pane ids |
| white's herdr shows no session ids | `~/.claude/sessions/<pid>.json` |
