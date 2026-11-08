---
name: herdr-lead-scouts
description: Lay out one lead pane on the left and two scout agents on the right (top and bottom) in the current herdr tab, brief each scout with its own half of a task, and have both report back into the lead pane. Use when Nat says "1 left 2 right", "two scouts", "split the research to the right", "all report to the left", or wants a question answered by two parallel agents he can watch. Do NOT use for a single buddy (use /herdr-buddy), for a whole team from a charter (use /herdr-team), or for agents in other spaces (use /herdr-room).
---

# /herdr-lead-scouts — 1 left, 2 right, all reporting left

Born 2026-10-07 (neo-oracle): Nat asked "how many Mac apps and widgets did we create", then
"1 left 2 right all reported in 1 left", then "how you did that? create skill".

```
┌──────────────┬──────────────────┐
│              │ scout A (top)    │  e.g. relic5 / session history
│  lead (you)  ├──────────────────┤
│              │ scout B (bottom) │  e.g. files on disk, one repo at a time
└──────────────┴──────────────────┘
        ▲ both: herdr agent prompt <lead-pane> "[scout X] <result>"
```

## Run

```bash
zsh ~/.claude/skills/herdr-lead-scouts/scouts.sh "<task for A>" "<task for B>"            # new panes, claude --model sonnet
zsh ~/.claude/skills/herdr-lead-scouts/scouts.sh "<A>" "<B>" --reuse                       # brief 2 agents already in this tab
zsh ~/.claude/skills/herdr-lead-scouts/scouts.sh "<A>" "<B>" --kind codex                  # other agent kinds
```

What it does: reads `$HERDR_PANE_ID` (the lead), splits right, splits that pane down, starts an agent
in each with `herdr agent start <name> --kind claude --pane <id> -- --model sonnet`, then sends each
scout its task plus a fixed tail: report only via `herdr agent prompt <lead> "[scout A|B] …"`,
read-only, stop at 40 tool calls. Results land in the lead as mid-turn messages — never sleep-poll.

## Split the task so the halves don't overlap

| Scout A | Scout B |
|---|---|
| history: relic5 / transcripts — what was built, when, where it was discussed | disk: confirm each claim in the repo (`fd`, `rg` one repo at a time) |
| upstream docs / web | local code and config |
| one half of a repo list | the other half |

The lead merges both reports, de-duplicates, and answers Nat. The lead never re-does a scout's search.

## Traps (met for real)

| trap | avoid |
|---|---|
| Nat had already forked the lead into two right panes; the lead opened two MORE, giving 5 panes and duplicates | the script lists agents already in the tab and warns; pass `--reuse` to brief those instead |
| a background subagent was already doing the same search | stop it (TaskStop) before briefing scouts — one search, one owner |
| reporting to the lead by agent NAME failed (`agent_not_found`) after the lead moved sessions | report to the lead's **pane id** (`$HERDR_PANE_ID`), and re-read it after any session move |
| scouts run `rg`/`fd` over the whole ghq root | the brief says "one repo at a time, never /opt/Code or ~ wholesale" (fleet search rule) |
| scout inherits Opus | `-- --model sonnet` on `herdr agent start` (claude kind); judgement stays in the lead |

## Close

When both reports are in: `herdr pane close <scout-pane>` for each (their conversations stay
resumable via `claude --resume <session>` from `herdr agent list`).
