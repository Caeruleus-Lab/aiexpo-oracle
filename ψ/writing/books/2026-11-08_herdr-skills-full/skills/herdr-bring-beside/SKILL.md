---
name: herdr-bring-beside
description: Move another herdr pane (an agent or a shell) into MY tab as a split right of me or below me — the agent keeps running, same conversation, only its pane id changes. Matches by pane id, Claude session id prefix, space label, terminal title or cwd folder name. Use when the user says "bring X beside me", "bring it to the right", "put that agent next to me", "split X in here", "herdr-bring-beside". Do NOT use to gather several agents into one room with a layout and send them back later (use /herdr-room), to give an oracle its own herdr session (use /herdr-move), to open a repo as a new space (use /herdr-bring), or to just list who is around (use /herdr-neighbors).
argument-hint: "<who> [right|down] [--ratio F] [--dry-run]"
---

# /herdr-bring-beside — pull a pane next to me

```bash
python3 -I ~/.claude/skills/herdr-bring-beside/bring_beside.py <who> [right|down] [--ratio 0.5] [--dry-run]
```

- `<who>`: `w2:p1` (pane id) · `0bec504c` (Claude session id, ≥ 4 chars) · `neo-oracle-main`
  (space label) · terminal title · cwd folder name. Case-insensitive; my own pane is never a match.
- Direction defaults to `right`. herdr only splits `right` or `down`.
- `--ratio` is passed to herdr as the split ratio.

Print the output. Exit codes: `0` moved / already here / dry-run, `1` not found or in another
session, `2` ambiguous (each candidate printed with its exact command — run the one the user means,
or ask if unclear).

## What it does

`herdr pane move <pane> --tab $HERDR_TAB_ID --target-pane $HERDR_PANE_ID --split <dir>`.
The process and conversation keep running; the pane gets a new id (`w2:p1 → w1:p2`), and herdr closes
the tab/space it left if it is now empty. The output ends with the undo command
(`herdr pane move <new> --new-workspace`).

## Limits

- **Same herdr session only.** One herdr server per session; `pane move` cannot cross. When the match
  lives in another session the script says where and prints the manual path: close it there, split
  here, `claude --resume <id>`. Closing stops the agent mid-work — confirm with the user first.
- The status line's session chain is keyed by session+pane, so a moved agent's `⛓` count restarts.

Tested 2026-10-11 on m5 session `neo`: already-here, cross-session (`nexus-oracle` in laris-co),
not-found, bad direction, and a real move of a scratch shell (`w3:p1 → w1:p3`, empty space closed,
undo command worked).
