---
name: herdr-tree
description: List this repo's main checkout and every git worktree as a tree, with the herdr space, agent status (working/idle/blocked/closed) and git status (ahead/behind, changed, untracked, locked) per row. Use when the user says "herdr-tree", "list our worktrees", "tree status", "what worktrees do we have here", or wants the herdr sidebar view in the conversation. Do NOT use to create a worktree (use /herdr-wt) or to move an oracle into herdr (use /herdr-bring).
---

# /herdr-tree

The herdr sidebar tree, in the conversation. Reads `git worktree list` (so worktrees closed in herdr still appear), joins it with `herdr workspace list` and `herdr pane list`, and asks git about every checkout in parallel. About 0.15 s.

## Run

```bash
python3 ~/.claude/skills/herdr-tree/herdr-tree.py            # repo of the current directory
python3 ~/.claude/skills/herdr-tree/herdr-tree.py <path>     # any repo
python3 ~/.claude/skills/herdr-tree/herdr-tree.py --json     # raw rows
python3 ~/.claude/skills/herdr-tree/herdr-tree.py --no-layout  # tree only
python3 ~/.claude/skills/herdr-tree/herdr-tree.py --session nsm  # another herdr session: one tree + layout per repo in it
```

With `--session`, `open`/`closed` is relative to that session: a worktree open in `default` shows as
`closed` in an `nsm` tree.

## Layout (after the tree)

Every open space of the repo, tab by tab, drawn from herdr's own pane rectangles (`herdr api snapshot`
→ `layouts[].panes[].rect`), scaled to 70 columns. Each box shows the pane id, the agent name and status
(or `shell`), and the pane's folder relative to the repo. A tab with one pane prints as one line instead
of a box. Panes too small for text still get their borders. Only the default herdr session is read, the
same as the tree; another session's layout needs `herdr --session <name> api snapshot`.

Print the output as-is in a fenced block, then add one line per thing that needs attention (a PRUNABLE row, a `no-upstream` branch with unpushed work, a row that is `closed` but dirty).

## Columns

| column | meaning |
|---|---|
| glyph + label | `*` working, `o` idle, `!` blocked, `?` unknown, `-` not open in herdr |
| status, space | herdr agent status and space id (`closed` if no space) |
| agent | agent kinds running in that space |
| branch | checked-out branch |
| flags | `upN` ahead, `dnN` behind, `~N` changed, `?N` untracked, `locked`, `PRUNABLE`, `no-upstream`, `clean` |
| last | short sha and age of the newest commit |

`<-- here` marks the checkout the command ran in.

## Traps

- `no-upstream` on a worktree branch is normal until the first push. It is not an error.
- A row with `closed` still has files on disk. Removing the herdr space does not remove the worktree.
- Needs `herdr` on PATH. Without a running herdr server the tree still prints, with every row `closed`.
