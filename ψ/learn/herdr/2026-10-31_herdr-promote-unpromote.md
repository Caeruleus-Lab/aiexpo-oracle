# herdr-promote and herdr-unpromote, and the skills around them (learned 2026-10-31)

Written by AIExpo Oracle (Oracle AI), session `bfe79650`, for Nat ("learn and dig deep about promote and
unpromote and more related skills"). Sources: the scripts in `~/.local/bin` (each identical to
`Soul-Brews-Studio/herdr-orca-oracle` `scripts/`), the two SKILL.md files, the repo's PRs, relic5 trace
`a7407beaa2`, and a `--dry` run on our own space wBZ.

## What they are

| Tool | One line |
|---|---|
| `herdr-move` | The engine. Moves every live agent of one repo (or of one space, `--workspace`) into another herdr session: end each agent, wait until its id is gone, close spaces left with only idle shells, start the target session, resume each conversation there with its exact id. |
| `herdr-promote` | The picker in front of herdr-move. Takes a team (`rd-team` / `rd`: desk + every `wt/<oracle>` body), a repo, or a space id (`wAA`), works out the set, then hands it to herdr-move. Default target: the team name, or the repo / space label minus `-oracle`. |
| `herdr-unpromote` | The way back. Moves a promoted team, oracle or whole session into the caller's session (or `--to`), same ids, names the panes (desk = team name, members = their oracle), then stops and deletes the emptied source session, its `herdr-by-name` link and its room state (unless `--keep`). |

herdr panes cannot cross sessions, so every move is "end here, resume there". Transcripts stay, so the
conversation survives; the process does not.

## How the move works (herdr-move, 181 lines of bash 3.2)

1. List every member (session, pane, conversation id, cwd). `--dry` stops here: `plan only: nothing changed`.
   Everything before that line only reads (`workspace list`, `agent list`, `session list`, `pane process-info`).
2. Refuse when the pane running it is in the set (it lists the set first, then refuses).
3. End each agent with `pane close`; where herdr refuses (the last pane of a space holding worktrees), send
   SIGHUP to the pane's foreground group, only when claude or codex leads it.
4. Wait up to 10 s until none of the ids is live anywhere; if any is, stop and resume nothing.
5. Close the spaces left with only idle shells (worktree spaces first).
6. Start the target session if it is stopped or new (`herdr --session <to> server`).
7. Resume each: `maw herdr ticket open <checkout> --repo <repo> --session <to> --session-id <id>`. A body that
   was never prompted has no transcript, so it gets a fresh `claude` instead.

## Traps (from the SKILL.md files, PR #15 and the first live use)

- Run it from a pane outside the set. `!` typed in a member's pane counts as that pane.
- Every member idle, nothing uncommitted (`just check <team>` in laris-team).
- `--channels` is not passed on resume: a body that owns a Discord bot comes back without it. `team-wake` holds
  the real launch lines that put the bot back.
- `--model` is not kept: an agent started on haiku comes back on the default model.
- After a move: panes come back unnamed; room state is per session, so the team's own desk rebuilds its room
  in the charter's seat order; set `session:` in `laris-team/teams/<team>.yaml`; add a `herdr-by-name` link
  if the session should open by name.
- The repo needs an `origin` remote (`maw herdr ticket open`).
- Right after a promote, wait a few seconds before an unpromote: an agent resumed but not yet detected makes
  the source look empty, so nothing moves.

## History (relic5 and git)

| When (Bangkok) | What |
|---|---|
| 9 Oct | `herdr-move` written on m5 (imported verbatim into herdr-orca-oracle on 29 Oct, commit `82caa07`). |
| 29 Oct 07:47 | Nat to Neo: "neo fix herdr-move and add herdr-promote". herdr-orca-oracle #13 (fix + promote), verified by Nexus. |
| 29 Oct 08:17 | Nat asked "who should call herdr promote for our team rd-team?". Neo and Nexus: nobody inside rd-team (all three are in the set); the caller is LarisCo, the laris-team host. |
| 29 Oct 08:18 | First live use: manager-team promoted (desk `803f799e`, athena `f41b88e8`, pulse `8d732eeb`) into session `manager-team`, same ids, room rebuilt; later brought back to laris-co (PR #15 records the round trip). Session `manager-team` no longer exists on m5. |
| 29 Oct 08:30 | Nat: "promote and unpromote". Neo renamed `herdr-demote` to `herdr-unpromote` (#16, then #17 nits). Tested only on throwaway haiku agents in scratch sessions. |
| 31 Oct 10:55 | Nat chose the opposite direction for laris-co: every oracle nests as `wt/<oracle>` under its team, inside session laris-co. LarisCo moved POS, People, Nongbua, AIExpo and God's Eyes OS by stopping each body and starting a fresh one (new conversation ids, not herdr-move). Config in laris-co/laris-team#8. AIExpo's new body is `course-team/wt/aiexpo-oracle` (wBZ:p1, `89a694ad`); this session (wBZ:p2) is "its lessons-site worker beside it". |

Neither skill has been typed as a slash command in m5's transcripts; both are run as commands.

## Dry run on our space (31 Oct)

```
$ herdr-promote wBZ --from laris-co --dry
space laris-co:wBZ (wt/aiexpo-oracle) · target session wt/aiexpo
  laris-co:wBZ:p1 89a694ad /opt/Code/github.com/laris-co/course-team/wt/aiexpo-oracle
  laris-co:wBZ:p2 bfe79650 …/aiexpo-oracle/wt/workshop-for-ai-aiexpo-issue3-30oct-fri2026   ← this pane: it would be skipped, run from another pane
plan only: nothing changed
```

What it shows:

1. **The default target has a slash.** The space label `wt/aiexpo-oracle` minus `-oracle` gives session name
   `wt/aiexpo`. Session folders live at `~/.config/herdr/sessions/<name>/`, so a slash is at best a nested
   folder. herdr-move does not clean the label. Name the target (`--to aiexpo`); the label rule may need a fix
   now that LarisCo's nested layout labels spaces `wt/<oracle>`.
2. **wBZ:p2 runs with `--channels=plugin:discord@claude-plugins-official`.** A move would bring it back
   without the Discord channel.
3. **wBZ:p2 is in the set**, so the real move has to run from another space.
4. **It would undo Nat's 31 Oct layout**, which puts course-team inside session laris-co.

## State of the sessions now (read only, 31 Oct evening)

| Session | Agents | Note |
|---|---|---|
| laris-co | 18 | the nested layout |
| neo | 10 | neo's own session |
| people | 1 (`4d710123`, people-oracle main checkout) | People also has a new body in laris-co (`07d89a29`): two bodies of one soul |
| oracle-gods-eys-os | 1 (`b4036ea1`) | God's Eyes OS also has a new body in laris-co (`b088f805`): two bodies |
| phd | 0 | one bare shell in `~`, left after DustBoy PhD moved to ccdc-team today |
| satellite, maw-atlas, messenger-archive | 1 each | single-oracle sessions |
| default | 1 | nexus-lead |
| nexus | stopped | the session `herdr-promote wAX` made in testing |

`team-check` and `herdr-info` flag a soul in two bodies; `herdr-unpromote --session phd` or `herdr-blank`
would clear the empty `phd` session. Nothing here was changed.

## The skills around them

Across sessions (end and resume, same id):

- `herdr-move` — the engine, one repo or one space.
- `herdr-promote` / `herdr-unpromote` — team, repo or space out to its own session, and back.
- `herdr-bring` (section "Moving a body to ANOTHER herdr session") — the same move done by hand: arm a pane
  with `while kill -0 PID; do sleep 1; done; claude … --resume ID`, then `/exit` the old body.
- `herdr-team-ctl` — start, stop or check a whole team from its charter on a session and machine, each member
  on its own conversation id.

Inside one session (no restart, real panes move):

- `herdr-room` — pull agents into one room tab and send them back, as often as needed.
- `herdr-bring-beside` — one pane into my tab, beside me.

Park and wake:

- `herdr-sleep` — wake card per space (cwd, session id, argv, channel on or off, dev-server commands), then quit.
- `herdr-vacation` — park agents idle more than N hours.
- `team-wake` — after a reboot, relaunch the bodies that own a Discord bot with their real launch line: the
  answer to the `--channels` trap.

Look before and after:

- `team-check` — one read-only look at a `<name>-team`: bodies, panes, names, nesting, uncommitted work, souls in
  more than one body, charter `session:` mismatch.
- `herdr-info` — every body of one oracle and the one-soul-many-bodies rules.
- `herdr-structure`, `herdr-tree`, `herdr-twin`, `herdr-machine-labels` — views of sessions, worktrees, machines.
- `herdr-blank` — close spaces whose every pane is a bare idle shell.
- `herdr-handover` — hand a live surface to a peer pane and watch.
