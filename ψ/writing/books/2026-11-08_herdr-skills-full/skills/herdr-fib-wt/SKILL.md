---
name: herdr-fib-wt
description: "Cut one git worktree per slug and open each as a pane in the CURRENT herdr tab, laid out as a Fibonacci spiral around your own pane (you left half, then top-right / bottom-right, turning). Optional --claude starts an agent in each. Use when Nat says 'fibonacci with worktrees', 'split panes with worktrees', 'open N worktrees here', 'I need this layout with worktrees'. Do NOT use for one worktree in its own space (/herdr-wt), or to arrange agents that already run (herdr-room in <room> --layout fib)."
argument-hint: "<slug> [slug ...] [--claude] [--dry]"
---

# /herdr-fib-wt

Nat, 2026-10-09: *"i need this with worktree"* — the Fibonacci split (me left, the rest spiralling right/down),
but each new pane sitting in its own fresh worktree.

```bash
herdr-fib-wt <slug> [slug ...] --dry      # the plan: paths, branches, which pane splits which way
herdr-fib-wt <slug> [slug ...]            # do it (shells)
herdr-fib-wt <slug> [slug ...] --claude   # and start claude in each (direnv exec . claude)
```

Run it from inside the repo, from the pane that should keep the left half.

| piece | what |
|---|---|
| worktree | `<main checkout>/wt/<slug>-<oracle>-<day>`, branch of the same name, cut from `origin/<default>` (the /herdr-wt naming) |
| pane | split from the newest pane, alternating right / down at 0.5, `--cwd` the worktree, label = slug |
| spiral | 1 slug: left \| right · 2: left \| top-right / bottom-right · 3: … bottom-right splits right again |
| limit | refuses past 10 linked worktrees (Rule 11); prints the table command and the `WT_MAX=` override |

Tool: `~/.local/bin/herdr-fib-wt`.

## Rules

- **Start from a tab where you are alone.** Every split halves the pane it splits; extra panes already in the tab
  squeeze you (tested 2026-10-09: two existing shells left the agent pane at 25% width).
- Name the agents after they start: `herdr agent rename <pane> <slug>` (pane ids change across restarts).
- Retire each worktree with `/herdr-wt-ship` when its work merges.
- Tested live 2026-10-09 in neo-oracle: `fibtest-a` → right of wAT:p1, `fibtest-b` → below it; both removed after.

## See also

- Agents already running? `herdr-room in <room> --layout fib|cols|rows|main` moves their real panes (no 2×2 grid).
- 1/3 | 2/3 by hand: Pulse's cheatsheet `ψ/writing/cheatsheets/2026-10-03_herdr-pane-move-layout.md` (laris-co/pulse).
