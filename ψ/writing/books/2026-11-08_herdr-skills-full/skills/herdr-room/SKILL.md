---
name: herdr-room
description: Pull live agents into one room (a herdr space whose single tab shows them all, fib/cols/rows/main layout) and send them back to spaces of their own, back and forth as often as you like, with no restart — real panes move and the member list is saved so `in` rebuilds the same room. Works from any pane in any session. Use when the user says "war room", "bring them into one room", "put X Y Z on one page", "send them back to their own spaces", "back and forth", "team page", "herdr-room", or wants a group view of several oracles and then their own spaces again. Do NOT use to start new agents from a charter (use /herdr-team), to move an agent between herdr sessions (panes cannot cross sessions — use the resume pattern in /herdr-bring), or to list where an oracle runs (use /herdr-info).
argument-hint: "in <room> [member…] [--layout fib|cols|rows|main] [--session S] [--dry] | out <room> [member…] [--session S] [--dry] | rename <room> <new> | list"
---

# /herdr-room — one page for a team, then back to their own spaces

Script: `~/.local/bin/herdr-room` (python3, calls `herdr --session S pane move` with exact pane ids).

```bash
herdr-room in  war-room /opt/Code/github.com/Soul-Brews-Studio/kvmbox-oracle \
                        /opt/Code/github.com/Soul-Brews-Studio/vpskeeper-oracle \
                        /opt/Code/github.com/laris-co/gateway-oracle \
               --layout fib --session homekeeper --dry          # plan first, always
herdr-room out war-room --session homekeeper                     # each back to a space of its own
herdr-room out war-room vpskeeper-oracle --session homekeeper    # split: only that one leaves
herdr-room in  war-room --session homekeeper                     # rebuild the same room from saved state
herdr-room in  war-room /path/to/another-oracle --session homekeeper   # add a member: joins at the end
herdr-room in  war-room --layout cols --session homekeeper       # re-tile the open room
herdr-room list                                                  # saved rooms, OPEN or out
herdr-room rename war-room ops --session homekeeper             # space label + tab label + saved state
```

## Members
- An **agent name** (herdr-team names every member), a **folder name** (`gateway-oracle`), a
  **folder path** (the agent's cwd), or a **pane id** in that session. Prefer names and folders:
  pane ids repeat across herdr sessions (`w8:p2` was both office and war-room on 2026-10-05).
- A path matching several agents in one session is refused with the candidates; pass the pane id.
- A member found only in another session is refused with that session's name. Panes cannot cross
  herdr sessions; move the agent first (new pane waits for the old pid, then resumes — /herdr-bring).

## Layouts — the share is set inside each move (no resize afterwards, so no extra redraw)
| layout | shape |
|---|---|
| `fib` (default) | first member the left half; each next takes half of what is left, turning right/down (3: left · top-right · bottom-right; 4: … · bottom-right splits into two) |
| `cols` / `rows` | equal columns / rows in member order |
| `main` | first member a left column of share `--ratio` (default 0.5), the rest stacked right |

## How it moves (why it works from anywhere)
1. The first member opens the room: `pane move --new-workspace --label <room>` (or is already in it).
2. Every other member goes to a scratch tab in the room's space. Inside one space a pane keeps its id.
3. Each comes back into the main tab with `--split` and `--ratio` = the share the TARGET keeps.
   The scratch tab closes itself when empty; so does any space a member left empty.
4. Every member is renamed (herdr drops an agent's name on a move); shells are skipped.

`out` sends each member to a space labelled with its name (its existing space if one has that label),
saves the order and layout, and the room closes itself once empty.

**Worktree members are nested again** (fixed 2026-10-06). Sidebar nesting under the repo comes from a
flag on the SPACE (`worktree_space`), which only `herdr worktree create/open` sets. A plain
`pane move --new-workspace` gives a flat space, which is how the floodboy room broke out into 5 flat
spaces. `out` now:
1. Sends a member whose cwd is a linked git worktree back to the space that still holds that worktree,
   if any (a helper pane can keep the old worktree space alive). Otherwise it makes a new space.
2. After **all** moves, runs `herdr worktree open --cwd <repo> --path <wt> --label <name> --no-focus`
   for each worktree member. On a space already at that path it attaches the identity in place
   (`already_open: true`; no pane moves, the agent is untouched).

Order matters: an early `worktree open`, run while the room still exists, attached to the room, which
then closed. In the test the first member came out flat and the last one nested.

## With /herdr-team (split a team into spaces, merge it back)
/herdr-team starts a team in ONE space — the worktree's own space, Fibonacci, every member named.
That space is a room like any other:

```bash
herdr-room out <team-space> omp-rain omx-wind --session laris-co   # those two get spaces of their own
herdr-room in  <team-space> --session laris-co                      # back into the team's page
```

- Name the members to split. `out` with no members moves EVERYONE, the lead's pane included.
- A herdr space is not a git worktree: split members still share the worktree's folder and files.
  For a member with its own branch and folder, start it with /herdr-wt instead (a running agent
  cannot change its folder).

## Moving a body (an agent's pane moves to another checkout) — order matters
Met 2026-10-31 in laris-co room `aiexpo-oracle` (wCC): the old body (wCC:p3, a course-team worktree)
split a new pane down with cwd = the main checkout, started `claude` there, and set timers to
`/exit` + `pane close` itself 20-40 s later. The new body ran `herdr-room in` at 20:05:38, before
the old pane had gone: 3 members, 3 columns. A second `in` at 20:06:04, after the close: 2.
Reproduced on fake agents (`pane report-agent`) in a scratch session; proof book
`Caeruleus-Lab/aiexpo-oracle` `ψ/writing/proof-books/2026-10-31_herdr-body-move/` (commit 5124342).

1. New pane in the room's space, cwd = the new checkout; start the new body there with a brief.
2. The OLD body leaves the space: `herdr pane close <old>`, or `herdr-room out <room> <old> --dry`
   first (out also runs `worktree open` for a worktree member, giving it a space of its own).
3. Wait until `herdr agent list` no longer shows the old pane. Never on a timer you only hope fired.
4. Only now: `herdr-room in <room> <new> <peer> --layout <x> --session <s>`, then `herdr-room list`.
5. Tell the peers the new pane id (ids change on every move).

## State
`~/.local/state/herdr-room/<session>__<room>.json` — members (path, last pane id, name), layout, time.

## Traps (met 2026-10-05)
| trap | handled |
|---|---|
| `maw herdr join` from another session: "pane … not found" (it fills the tab of the pane it runs in) | herdr-room never uses "the pane I run in" |
| same pane id in two sessions → maw refuses as ambiguous, even with `--session` | members by path |
| agent name lost after a move or a swap | renamed after every move |
| moving into a zoomed tab returns `changed:false` silently | unzoom first (not automated yet) |
| a re-layout that resizes afterwards makes every agent redraw twice | shares set inside the moves |
| `out` gave worktree agents FLAT spaces, not nested under their repo (2026-10-06) | `worktree open` per worktree member, after all moves |
| `worktree open` while the room is alive attaches to the room (first member flat) | runs only after every move |
| `pane move --split left` → `invalid split direction` | only `right` / `down` exist |
| `pane move` into an existing space: the result has no `pane` key | look the pane up by `agent list` |
| `in` on an OPEN room keeps every pane already inside its space, typed or not (2026-10-31: the old body was still in the space, so `in <new> <wt>` gave 3 columns) | by design (`if ws:` branch, ~line 235): the old pane must LEAVE first. See "Moving a body" above |
| editing the state file to drop a member does nothing while the room is open | members are rebuilt from the panes in the space; the state only orders them |
| two agents moving or renaming at once: pane ids change mid-check (nsm 10-08, neo 10-11, relic4-scan 10-31) | only the desk runs `in`/`out`; everyone else `--dry` |
| `out` nested the worktree member under the WRONG parent: a second plain space whose cwd was inside the same repo (a capture space at `ψ/writing/proof-books/...`, label `proof-book`) came first in the sidebar, and `worktree open` linked the wt to it (2026-10-31) | keep ONE plain space per repo (the main oracle's). Close any extra space in that repo before `out`. If it already happened: `in` (frees the link), `workspace close <extra>` (without `--group`, which would close the wt's space too), `out` again |
| `workspace close` on that extra space: `workspace_group_close_required` | it now owns the linked wt; `--group` closes the wt agent's space as well. Room `in` first, then close |
| `herdr-room list` shows OPEN after `out` | the main oracle's own space carries the room's label; harmless (`in` uses it), but `list` cannot tell out from open |

Proven on throwaway shells in session laris-co (2026-10-05): fib 3 → out → in from state → add a 4th
(fib spiral 88x44 | 88x22 / 44x22 · 44x22) → cols → out → all spaces closed.
Proven on throwaway **worktrees** in session ccdc (2026-10-06): 2 linked worktrees → in → out → both
`WT` (nested); before the order fix it gave `t-a FLAT, t-b WT`. The 2026-10-05 tests used plain shells
only, which is why the worktree case slipped through. Test with worktrees whenever members can be worktrees.
