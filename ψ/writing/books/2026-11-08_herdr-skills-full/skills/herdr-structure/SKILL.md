---
name: herdr-structure
description: Draw a whole herdr session as a tree: every space, which spaces are rooms (2+ agents), each pane's agent name, status and conversation id, the team lead (from the pulse-oracle team charters) and "me". Works for m5 sessions and saved remote machines (white-nsm, white-phonebooth, ...), or all at once. Use when the user says "herdr-structure", "show the structure", "nsm see structure on white", "what is in session X", "draw the session", or wants the team layout of a session in the conversation. Do NOT use for one repo's worktrees and git status (use /herdr-tree) or for every body of one oracle (use /herdr-info).
---

# /herdr-structure

One session, one tree. Reads `herdr workspace list`, `pane list` and `agent list` for the target
(local session or `--machine`), so it is live, not a saved state file. About 1 s per target.

## Run

```bash
herdr-structure                          # m5, session laris-co (or $HERDR_SESSION)
herdr-structure --session phonebooth     # another m5 session
herdr-structure --machine white-nsm      # a saved remote machine = that machine's session
herdr-structure --all                    # every running m5 session + every enabled saved machine
herdr-structure --json                   # raw rows
```

## Reading it

```
white-nsm  ·  7 spaces, 8 agents
├─ w7   nonsense-matters-oracle        w7:p1   idle       <- lead
├─ wG   media-team  (room, 2)
│    ├─ wG:p1   dakanda-oracle             idle
│    └─ wG:p2   pigment-nsm                idle
└─ wH   xiaoer-oracle                  wH:p1   idle
```

- A space with 2+ agents is drawn as a room, with its panes under it.
- `<- lead` = the `lead:` of a charter in `laris-co/pulse-oracle/teams/*.yaml` (local main; an unmerged charter is not seen).
- `<- me` = the pane this runs from (local sessions only).
- `(shell, no agent)` = a space with no running agent (after a reboot, or a job pane).
- Conversation ids are empty for remote machines without herdr's claude integration (white).

After drawing, say in one or two lines what stands out: an agent missing from its room, a space with no
agent, a lead not running.
