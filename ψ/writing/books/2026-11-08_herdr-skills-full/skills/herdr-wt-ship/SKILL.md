---
name: herdr-wt-ship
description: "Show every worktree of the current repo as one measured table FIRST, then finish the ones that are done: the merged PR is signed, a tombstone is written, the worktree is removed and the local branch deleted. Use when the user says list worktrees, our worktrees, cleanup worktrees, pr all and cleanup, finish worktrees, ship worktrees. Do NOT use for a machine-wide sweep (use /herdr-clean-up-sync), to cut a worktree (use /herdr-wt) or to sign one PR (use /herdr-pr)."
---

# /herdr-wt-ship — table first, then finish what is done

Nat (2026-10-09): "i want to see like above first". The table comes before any plan, question or action.

## Step 0

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

## 1. The table, always first

```bash
python3 -I ~/.claude/skills/herdr-wt-ship/wt_table.py            # this repo, every worktree, measured now
python3 -I ~/.claude/skills/herdr-wt-ship/wt_table.py --no-size  # fast: skips du (a 700 GB folder takes ~40 s)
```

Print its output to the user as it is: header line, the main-checkout line, the boxed table, the tier legend.
Do not replace it with a summary. Columns: `#`, worktree, branch (`same` = equals the folder), size, herdr space,
state = fleet tier + why + the agent living there (the main checkout is a path prefix of `wt/` and `.tmp/`, so an
agent is attributed to the longest matching worktree).

Tiers: A folder gone · B merged, clean · C pushed, not merged · D uncommitted or local-only work · K keep
(agent working, or gitignored data over fleet's 50 MB cap).

The last line is the rule (Nat, 2026-10-09; also neo-oracle Golden Rule 11): **at most 10 linked worktrees, none
created more than 15 days ago.** The `age` column is days since the worktree's git admin dir was created, and `!`
marks one past 15. When the `Rule:` line says OVER, or any row is marked `!`, offer those rows first in step 4.
Limits can be tried with `WT_MAX=3 WT_MAX_DAYS=7 python3 -I wt_table.py`.

## 2. Read before you offer

`✓`/idle means the agent finished a turn, not the task. For every row with an agent:

```bash
herdr --session <s> pane read <pane> --source recent-unwrapped --lines 40 | tail -12
```

A standing watch (the Kong migration until 10-14), a question waiting on Nat, or a fresh session with no task is
not "done". Never pass `--idle-agents` for those.

## 3. Plan (changes nothing)

```bash
bash ~/.claude/skills/herdr-ticket/ship.sh done <worktree>...            # add --idle-agents only for rows you read
```

Per row it stops at the first thing that is not true: clean → PR merged (or HEAD already in the default branch,
and nothing landed after the merge) → no working agent → PR signed citing a commit that is on main → fleet would
remove it. Every stop prints the command that fixes it.

## 4. Ask, then act on exactly what was picked

AskUserQuestion (multiSelect) with the rows whose plan ended in `PLAN`, each with its repo, branch and agent. Then:

```bash
bash ~/.claude/skills/herdr-ticket/ship.sh done <worktree> [--idle-agents] --go
```

Order: tombstone → `fleet clean --pick` (goes through `herdr worktree remove`, so the sidebar agrees with git) →
`git branch -d`. Never: `git branch -D`, push, merge, force, `rm -rf`. The remote branch is always kept.

- **Unsigned merged PR:** `--go` asks the worktree's OWN session to run /herdr-pr (`ticket.sh continue`: prompts
  the live agent, or resumes the session headless on sonnet). It is asynchronous: the row stops at "signing
  requested". When the reply arrives, run the same command again. No sleep, no polling.
- **Over 50 MB of ignored data** (`.tmp/` clones): move it, never delete it:
  `mkdir -p ~/.herdr/tombstones/<repo> && mv <wt>/.tmp ~/.herdr/tombstones/<repo>/<slug>.tmp`
- **Local branch kept** ("not merged into its upstream", typical after a squash): `git branch -D` only after
  checking `git rev-parse origin/<branch>` equals the recorded head.

## Not this skill

- **D rows (uncommitted work):** rescue is `/herdr-clean-up-sync` step 4. List the files first
  (`git -C <wt> status --porcelain -uall | head -40`); a bulk rescue once pushed `.codex` homes to public repos.
- **C rows with no PR, or commits after a merged PR:** a human opens the PR first
  (`gh pr create -R <slug> --head <branch>`); merging is always Nat's.
- **The main checkout** is never a target.

## Traps (measured 2026-10-09)

- `fleet clean` with `--pick` lists nothing for a row it will keep; `ship.sh` therefore refuses before it writes a
  tombstone, with the `fleet audit … --pick` command to see why.
- A signature made before a merge cites a SHA the merge may have rewritten (herdr-pr trap 6). `ship.sh` accepts
  the landed merge sha, or the PR head sha when that commit is on main.
- `du` on a 700 GB worktree dominates the table's run time; it times out at 90 s per row and prints `>90s`.
