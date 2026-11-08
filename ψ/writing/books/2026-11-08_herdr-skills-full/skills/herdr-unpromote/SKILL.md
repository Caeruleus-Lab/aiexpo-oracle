---
name: herdr-unpromote
description: "Bring a promoted team, oracle or whole herdr session BACK into a session (default: the caller's own, 'bring back here'), with the same session ids, then name the panes and remove the emptied source session, its herdr-by-name link and room state. The pair of /herdr-promote. Use when Nat says 'unpromote <team>', 'bring <team> back', 'bring nongbua back to laris-co', 'undo the promote', 'herdr-unpromote'. Do NOT use to give something its own session (/herdr-promote), to arrange panes inside one session (/herdr-room), or to start a team from its charter (/herdr-team-ctl)."
argument-hint: "<team|oracle|session> | --session <name> [--to <session>] [--keep] [--dry]"
---

# /herdr-unpromote

The pair: **/herdr-promote** gives a team, repo or space its own session; **unpromote** brings it back.
Nat, 2026-10-29: *"promote and unpromote"*.

```bash
herdr-unpromote nongbua --dry             # nongbua's agents -> this session, named nongbua-oracle; session nongbua removed
herdr-unpromote manager-team --to laris-co   # a team (desk + wt/* bodies), from wherever it runs
herdr-unpromote some-session --keep       # every agent of that session; keep the emptied session
```

What moves (first match wins):

- **team**: `<x>-team` or `<x>` → the desk repo `<x>-team` under `$(ghq root)`: desk + `wt/<oracle>` bodies.
- **oracle**: an oracle or repo name or path, as `herdr-move` resolves it.
- **session**: a running herdr session that is neither: every agent in it, space by space.
- A running session of that name also wins over a team/oracle when none of its agents runs under that repo
  (`herdr-promote wAX` makes session `nexus`, which is not nexus-oracle's own bodies). `--session <name>` takes the
  name as a session, always.

Steps:

1. `herdr-move` each set to `--to` (end, wait until every id is gone, resume with the same ids). It refuses when the
   pane running it is in the set: run it from outside (the target session is fine).
2. Wait (30 s) for every id in the target and name its pane: team desk = team name, members = their oracle
   (`wt/<oracle>`), an oracle's main checkout = the repo name, anything else = the name it had (else its folder).
3. Each source session left with only plain shells and no agent is stopped and deleted, unless `--keep`; with it go
   `~/.local/bin/<session>` (only if it links to `herdr-by-name`) and `~/.local/state/herdr-room/<session>__*.json`.
   A source that still runs something (an agent not detected yet counts) is kept and said so.
4. Reminders: the team's own desk rebuilds its room in the charter's seat order
   (`herdr-room in <team> --session <to>`; room state is per session), and laris-team sets `session:` in
   `teams/<team>.yaml` (and `sessions/<to>.yaml`).

Rules:

- `--dry` first: the whole plan, names and cleanup included.
- Real tests only on throwaway agents in scratch sessions, never on live team bodies.
- Bodies running with `--channels` (a Discord bot) come back without it: `maw` does not pass the flag on resume.
- `maw herdr ticket open` needs the repo to have an `origin` remote.
- Right after a promote, wait a few seconds: an agent resumed but not yet detected makes the source look empty
  of agents and busy, so unpromote moves nothing and keeps it.

Tools: `~/.local/bin/herdr-unpromote` (uses `herdr-move`), source `Soul-Brews-Studio/herdr-orca-oracle` `scripts/`.
Lessons from the first live round trip by hand (manager-team): herdr-orca-oracle#15.

Tested 2026-10-29 in scratch sessions only (repo `upx-team` + `wt/alpha-oracle`, two haiku agents):

- **team**: `neo-up-team` → `neo-up-home`. Same ids (9b7ac118, e7d100ac), named `upx-team` / `alpha-oracle`.
  `neo-up-team` was stopped and deleted, and its link and room state were removed.
- **session, --keep**: one agent `neo-up-sess` → `neo-up-home`, named; `neo-up-sess` kept.
- **session**: `neo-up-sess2` → `neo-up-home`; `neo-up-sess2` stopped and deleted.
- **default --to**: the caller's session; outside herdr it asks for `--to`.
