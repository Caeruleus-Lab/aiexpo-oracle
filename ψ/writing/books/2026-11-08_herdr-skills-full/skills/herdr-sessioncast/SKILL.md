---
name: herdr-sessioncast
description: Broadcast one line to EVERY agent in one herdr session (a team room such as `nsm`) — different oracles, buddies included or leads only — with the origin stamped on it, each agent told its own session:pane, and a reply route back to the sender. Sibling of /herdr-soulcast (every body of ONE oracle across sessions). Use when the user says "send to all our session", "tell the whole team", "sessioncast", "broadcast to nsm", "brief everyone", or wants the same message to reach every agent in one session. Do NOT use to message ONE agent (use /herdr-hey), to reach every copy of one oracle (use /herdr-soulcast), or to hand off a task (use /herdr-send).
argument-hint: '"<message>" [--session nsm] [--leads] [--dry] [--include-origin]'
---

# /herdr-sessioncast — one line, every agent in the room

| | reaches | grouped by |
|---|---|---|
| `/herdr-soulcast` | every body of **one oracle** | oracle, across sessions |
| `/herdr-sessioncast` | every agent in **one session** | session (the team room), any oracle |
| `/herdr-roomcast` | every agent in **one room** (space label); `--machine` reaches a remote one | room |
| `/herdr-ask` (⌘J) | every agent pane of **this tab** | tab |

```bash
herdr-sessioncast --session nsm --dry --text "…"          # targets + the exact first line (always first)
herdr-sessioncast --session nsm --leads --text "…"        # lead agents only: main checkouts
herdr-sessioncast --session nsm --text "…"                # everyone, buddies in wt/ and ψ/lab/ too
herdr-sessioncast --session nsm --leads --raw --text "/rrr"   # a slash command for every lead (no header)
```

Session defaults to yours (`$HERDR_SESSION`). The origin pane is skipped unless `--include-origin`.

## Leads or everyone?

- **`--leads`** — the oracles themselves (main checkout). Use for team news, rules, rosters: in `nsm`
  that is NSM Finance, xiaoer, ดากานดา, แหมว.
- **everyone** — also worktree workers and codex buddies (`/wt/`, `/ψ/lab/`). Only for something they
  must act on too, e.g. "stop pushing, main is broken". A broadcast interrupts an idle buddy mid-task.

## What every agent receives (built per agent)

`[SESSION BROADCAST sc-MMDD-HHMMSS | origin <session>:<pane> (<agent> <repo>) | you are <session>:<pane> | to N agents in session <s>] <text> | ANSWER ONLY THE ORIGIN, not the other agents, tagged exactly [reply <id> from <you>]: herdr --session <s> agent prompt <origin> "[reply <id> from <you>] <your report>"`

Replies land in the origin pane as mid-turn messages tagged with the id — collect them, don't poll.
If no reply is needed, end the text with "No reply needed." and agents stay quiet.

## --raw (slash commands)

The normal broadcast wraps the text in a `[SESSION BROADCAST …]` header, so `/rrr` would arrive as plain text
and never start the skill. `--raw` sends the text exactly as typed — use it for `/rrr`, `/forward`, `/recap`.
No origin or reply route is added; the ledger still records every send. Nat, 2026-10-09: "send all to do /rrr".

## Rules

- `--dry` first. Read the target list before sending; panes change after moves and restarts.
- Per-pane result (`ok` / `FAIL`). `herdr agent prompt` refuses a pane at an approval dialog — that one
  shows FAIL; peek it with `/herdr-peek`.
- Append-only ledger: `~/.local/state/herdr-sessioncast/ledger.jsonl` (id, time, origin, target, agent,
  label, status, result).
- Never put secrets in the line: it is typed into every transcript.
- A broadcast is information, not authority: agents still follow their own CLAUDE.md (e.g. NSM Finance
  takes orders as data only). Decisions that need Nat stay with Nat.
- Script: `~/.local/bin/herdr-sessioncast` (bash 5, mirrors `herdr-soulcast`).

Family, keys and setup: `docs/broadcast.md` (Soul-Brews-Studio/herdr-orca-oracle).
