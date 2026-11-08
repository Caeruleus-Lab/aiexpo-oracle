---
name: herdr-info
description: Show every body of ONE oracle on this machine — every herdr session, space and pane where it runs (main checkout or worktree), anything running outside herdr, its Discord connections — check the one-soul-many-bodies rules (one conversation id per body, one Discord connection per bot), and draw each tab that holds it as a layout card. Use when the user says "herdr-info <oracle>", "where is <oracle> running", "list all <oracle>", "list all working pulse", "draw <oracle> layout", or "how many <oracle> bodies". Also takes a herdr SPACE name ("herdr-info office") when no oracle has that name: lists every pane in that space. Do NOT use for one repo's worktree and git status (use /herdr-tree), or to move an oracle (use /herdr-bring).
argument-hint: "<oracle|space> [--no-layout] [--json] [--width N]"
---

# /herdr-info — one soul, every body

An oracle can run in several herdr sessions, spaces and panes at once, in its main checkout or in
worktrees. This finds all of them on this machine and draws where they sit.

## Run

```bash
python3 ~/.claude/skills/herdr-info/herdr-info.py <oracle>              # e.g. pulse
python3 ~/.claude/skills/herdr-info/herdr-info.py <space>               # e.g. office (when no oracle has that name)
python3 ~/.claude/skills/herdr-info/herdr-info.py <oracle> --no-layout  # table only
python3 ~/.claude/skills/herdr-info/herdr-info.py <oracle> --json       # raw
python3 ~/.claude/skills/herdr-info/herdr-info.py <oracle> --width 96   # fit N columns: shortens Where, wraps long lines
```

How to show it (Nat, 2026-10-05):
1. Everything the script prints goes **inside one fenced block**: header, layout cards, agents table,
   shell panes, warnings. All of it is box drawing, which only lines up in monospace.
2. The agents table (`Session | Pane | Agent | State | Where | Up`) has one row per window, i.e. per
   herdr session (a terminal window shows one session; its spaces are pages in the sidebar). Each cell
   holds one line per agent, so a row reads across: line 2 of every column is the same agent. The
   script draws it itself: markdown table cells cannot hold line breaks. `Up` is the agent process's
   age; the agent that ran the command shows `this conversation`, and its line comes first.
3. After the block: one line per warning and per body worth acting on (an idle agent whose worktree
   is merged, a body outside herdr).

## Name lookup: oracle first, then space

`<name>` is tried as an oracle first: any ghq checkout named `<name>` or `<name>-oracle`. If none
exists, it is tried as a herdr space label (case-insensitive) in every running session, and every
pane in that space is listed, whatever repo it runs in. The header then reads `space <name> - ...`.
Neither found: exit 1. (Nat, 2026-10-05: "first track oracle name if not found go these space name")

## What it reads

| source | for |
|---|---|
| `ghq list -p` | the oracle's repos: every checkout named `<oracle>` or `<oracle>-oracle`, any org |
| `git -C <repo> worktree list --porcelain` | linked worktrees that live OUTSIDE the repo folder (`~/.herdr/worktrees/…`, orca, incubate); panes there count too, shown as `wt ~/.herdr/worktrees/<repo>/<name>` |
| `herdr session list --json`, then `herdr --session <s> api snapshot` per running session | panes whose folder is in those repos or their worktrees: agent, status, conversation id, space, tab layout |
| `herdr --session <s> pane process-info --pane <p>` | which processes each agent pane owns |
| `ps` + `lsof` cwd | claude / codex processes in those repos that no herdr pane owns (tmux, plain terminals). A desktop app's own helpers are skipped: an executable inside an `.app` bundle, or `codex sandbox` / `codex app-server` (ChatGPT.app runs these with whatever folder it last used) |

Fixed 2026-10-05 (Nat: "fix herdr-info"): before, an agent in `~/.herdr/worktrees/neo-oracle/…` was
missing from the table, and ChatGPT.app's codex helpers showed up as "6 outside herdr" for neo.
Checked on the-oracle-voice: shell `wAT:p1` in `~/.herdr/worktrees/the-oracle-voice/worktree-brave-forest-2d98` is now listed.
| `bun … discord` plugin processes + their parent's cwd | Discord connections, by `DISCORD_STATE_DIR` |

Always passes `--session <name>` explicitly: inside a herdr pane, `HERDR_SOCKET_PATH` would otherwise
silently point every call at the caller's own session.

## Warnings

| warning | why it matters |
|---|---|
| one conversation id live in 2+ bodies | both write one transcript; it branches and a later resume can come back as the other body |
| 2+ Discord connections on one state dir | every message reaches every connection (seen 2026-10-03 on atlas, twice) |
| Discord plugin with no `DISCORD_STATE_DIR` | the official plugin then falls back to `~/.claude/channels/discord` (mawjs's folder); a repo's own plugin (e.g. `bun .discord/mcp.ts`) may read its own `.discord` — check `ps -o command=` |

## Layout card

Printed FIRST, right after the two header lines; the table, shells, Discord and warnings follow
(Nat, 2026-10-05: "layout first list later"). Each tab that holds at least one body is drawn from
herdr's own pane rectangles, two cards per row.
Proportions are kept but compressed so every pane gets room for its label: pane id, agent and
status, and the first 8 characters of the conversation id. Other panes in the same tab (shells,
other agents) are drawn too, so the card shows what the body sits next to.

## Related

- `/herdr-tree` — one repo: checkouts, git state, phase, and the layout of its open spaces
- `/herdr-bring` — move a body into this herdr server (kill before resume)
- `herdr-layout --pane <id>` (`~/.local/bin`) — one tab in full detail
