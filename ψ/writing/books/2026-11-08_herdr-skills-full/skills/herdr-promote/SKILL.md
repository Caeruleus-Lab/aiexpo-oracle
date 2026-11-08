---
name: herdr-promote
description: "Give a team, a repo or one space a herdr session of its own on this machine: every live agent of it is ended where it runs and resumed in the target with its exact session id. A team (<x>-team) brings its desk and every wt/<oracle> body; a workspace id (wAA) brings only the agents in that space. Use when Nat says 'promote rd-team', 'give the team its own session', 'promote this space', 'move wAA to its own session', 'herdr-promote'. Its pair is /herdr-unpromote (bring it back). Do NOT use to bring a promoted team back (/herdr-unpromote), to arrange panes inside one session (/herdr-room), to open an oracle that is not running (/herdr-bring), or to start a team from its charter (/herdr-team-ctl)."
argument-hint: "<team|repo|workspace-id> [--to <session>] [--from <session>] [--dry]"
---

# /herdr-promote

The pair: **promote** gives a team, repo or space its own session; **/herdr-unpromote** brings it back.

Nat, 2026-10-29: *"neo fix herdr-move and add herdr-promote"*.

```bash
herdr-promote rd-team --dry               # who moves (desk + wt/* bodies), from which sessions
herdr-promote rd                          # same team; target session rd-team
herdr-promote wAA --from laris-co --dry   # only the agents in space wAA; target = its label minus -oracle
herdr-promote neo --to neo                # an oracle repo: main checkout and its worktrees
```

What it picks, then hands to `herdr-move` (which ends each agent, waits until every id is gone, closes the spaces
left holding only idle shells, starts the target and resumes each conversation with
`maw herdr ticket open … --session <to> --session-id <id>`):

- **team**: `rd-team` or `rd` resolves to the repo `<x>-team` under `$(ghq root)`: its main checkout (the desk agent)
  and everything under it (`wt/<oracle>` bodies). Default target: the repo name (`rd-team`).
- **repo**: an oracle or repo name or path, as `herdr-move` resolves it. Default target: the name minus `-oracle`.
- **workspace id**: `w…` that exists as a space in `--from` (default: the session it runs in). Only that space's
  agents, any repo. Default target: the space's label minus `-oracle`. A name like `white` is a space only if such a space exists.

Rules:

- `--dry` first. It lists every member and marks the pane running it (`← this pane: it would be skipped`).
- The default target may already run (a `neo-oracle` space → session `neo`, where neo's other agents live). Then
  the agents JOIN that session, beside what runs there; that is intended (an oracle's own session). The `--dry`
  header names the target: give `--to` when you want a fresh one.
- Run the real move from a pane outside the move set: it refuses otherwise, after listing.
- Test only on throwaway agents in scratch sessions, never on live team bodies (desk, 2026-10-29).
- The resumed agents come back with their conversations, but `maw` starts them on the default model (an agent
  started with `--model haiku` comes back on the default).
- `maw herdr ticket open` needs the repo to have an `origin` remote.

## Before a real move

- **Who runs it:** a pane outside the team. For a team, the host desk (laris-team) or Nat in a plain shell of
  another space. `!` in a member's pane counts as that pane (its process tree), so it is refused.
- **All idle, nothing dirty:** `just check <team>` (laris-team) shows state and uncommitted files per body.
- **Discord bots:** the resume does NOT pass `--channels`. A body running with `--channels` (check
  `ps -o args= -p <pid>`) comes back without its bot. Relaunch it with its channel flags after, or do not move it.

## After a real move

1. **Names:** the resumed panes come back without herdr names. `herdr --session <to> agent rename <pane> <name>`
   each (desk = the team name, members = their oracle).
2. **Room:** room state is saved per session, so the old room does not follow. Let the team's OWN desk rebuild it,
   with the charter's seat order (`room:` / `seat:`; manager-team: Athena left). Trap: when the desk's space carries
   the room's label, `herdr-room in` keeps the desk on the left whatever the saved order says.
3. **Charter:** set `session:` in `laris-team/teams/<team>.yaml` (and `sessions/<session>.yaml`). `just check
   <team>` notes a mismatch until then.
4. **Open it:** `herdr --session <to>`. A bare `<team>` command exists only as a link to `herdr-by-name`:
   `ln -s herdr-by-name ~/.local/bin/<session>` (laris-co, neo and nsm already have one).

## Back again

The same tool with `--to` the old session, from a pane outside the team:

```bash
herdr-promote manager-team --to laris-co --dry
herdr-promote manager-team --to laris-co
```

Then names, room and charter as above, and clean up what is left of the promoted session:

```bash
herdr --session <team> pane list             # only a plain shell left (often Nat's attached window)
herdr session stop <team> && herdr session delete <team>
rm ~/.local/bin/<team>                         # the link, if one was made
rm ~/.local/state/herdr-room/<team>__<room>.json
```

Tools: `~/.local/bin/herdr-promote` and `~/.local/bin/herdr-move`, source `Soul-Brews-Studio/herdr-orca-oracle`
`scripts/`. Skill source: the same repo, `skills/herdr-promote/SKILL.md`.

Tested 2026-10-29 on scratch sessions only (repo `promo-team` with `wt/alpha`, two haiku agents):

- **team**: `neo-promo-src` → `neo-promo-dst`, both ids came back the same (50c40516, dda928db).
- **space**: `w2` of `neo-promo-dst` → `neo-promo-ws`, only dda928db moved.
- **team gathered from two sessions**: `neo-promo-dst` + `neo-promo-ws` → `neo-promo-src`, both resumed with their
  history.

First live use 2026-10-29, run by the rd-team desk (outside the team): manager-team (desk 803f799e, Athena
f41b88e8, Pulse 8d732eeb, all idle, no `--channels`) `laris-co` → `manager-team`, same ids; then back with
`--to laris-co`, same ids again. Names, room and charter had to be redone by hand both ways (the steps above), and
the first room rebuild put the desk on the left instead of Athena. rd-team was dry-run only: Nexus runs the nexus
bot with `--channels`, which the resume would drop.
