---
name: herdr-dissolve
description: The reverse of /herdr-wt, and the one skill for winding herdr down — from a single worktree up to the whole machine. A worktree whose agent did work gets saved first (its own agent commits, pushes, opens a signed PR and reports to its PARENT, the repo's main-checkout agent); a worktree with nothing in it, a merged or pushed one, or a space on a missing folder is removed straight away through herdr so the sidebar and git agree; idle agents on the main checkout are quit and their panes closed; checkouts that are only behind are fast-forwarded. Always shows the plan and asks before anything is closed or removed, and never closes the pane running it. Modes — `<wt|pane ...>` (named), `--all-but-me` (this repo down to one pane), `--sweep` (whole machine, was /herdr-clean-up-sync), `--sync`, `self`. Use when the user says "dissolve", "wind down this worktree", "finish and close", "commit push pr and close", "done with this wt", "close all panes and wt, only me", "clean up herdr", "clean up the sidebar", "sync", "too many ✓", "close the done ones", "everything is ↓", /herdr-dissolve or /herdr-clean-up-sync. Do NOT use to check whether ONE session is safe to close (use /herdr-done), to create worktrees (/herdr-wt), or to move sessions between machines (/herdr-bring).
argument-hint: "[<wt|pane> ...] | --all-but-me | --sweep [--host <ssh>]... | --sync [--all] | self"
---

# /herdr-dissolve: wind herdr down, saving work first

`/herdr-wt` makes a branch, a locked worktree, a space and an agent. This undoes it in
the right order, at any scale. **The agent that did the work saves it and reports first.**
Only then is anything removed. Nothing is lost: work lands in a PR, the summary reaches
the parent, the transcript stays in `~/.claude/projects`, and a tombstone records what
ended and why.

Merged 2026-10-29 from `/herdr-dissolve` (save, then remove) and `/herdr-clean-up-sync`
(sweep and sync). Nat: "merge … to one". The old texts are in `SKILL.md.bak-20261029-premerge`
here and `../herdr-clean-up-sync/SKILL.md.bak-20261029-merged-into-dissolve`.

## Modes

| call | scope | typical ask |
|---|---|---|
| `/herdr-dissolve <wt\|pane> [...]` | the named worktrees | "done with this wt" |
| `/herdr-dissolve --all-but-me` | every pane and worktree of the CURRENT repo, except the pane running this | "close all panes and wt, just only 1 here" |
| `/herdr-dissolve --sweep [--host H]` | every repo on the machine (`ghq list -p`) | "clean up the sidebar", "too many ✓" |
| `/herdr-dissolve --sync [--all]` | checkouts that are only behind | "everything is ↓" |
| `/herdr-dissolve self` | the worktree you are running in | an agent finishing its own task |

`--sweep` runs sync's plan too, as the old `/herdr-clean-up-sync` did. Every mode goes
through the same four steps: **survey, plan, ask, act**.

## The engine: `fleet`

Everything runs on `fleet` (`tools/fleet-tui/worktrees.ts` in laris-co/neo-oracle,
installed as `fleet` by `just fleet-install`). Every command prints a plan until `--go`.

```
fleet audit  [--host H] [--repo X] [--pick wt1,wt2] [--idle-agents] [--idle-shells] [--min-age N] [--no-fetch] [--json]
fleet clean  [--host H] [--repo X] [--pick wt1,wt2] [--tier A,B,C,D] [--idle-agents] [--idle-shells] [--pr] [--go]
fleet sync   [--host H] [--all] [--go]
fleet send <pane> "<text>"      fleet watch <pane>      fleet tail <pane>
fleet close <pane>              fleet snapshot --commit
```

No `--host` = this machine. `--host white.local` runs the same code there over ssh; it
needs bun, git, gh and ghq, nothing from fleet.

**`fleet <cmd> --help` is not help.** Unknown flags are ignored, so `fleet clean --help`
ran a full-machine `clean` plan (2026-10-08, stopped at repo 445/1278). Without `--go` it
changes nothing, but never type a flag to "see the usage". `fleet` with no arguments
prints the usage.

## 1. Survey (read-only)

Scope it to the mode. **With no `--repo` and no `--pick`, `audit` and `clean` walk every
repo on the machine** (1278 on m5, 2026-10-08). Only `--sweep` may run unscoped.

```bash
# named / --all-but-me: this repo only
repo=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
slug=$(git -C "$repo" remote get-url origin | sed -E 's#.*[:/]([^/]+/[^/.]+)(\.git)?$#\1#')
fleet audit --repo "$slug" --idle-agents --idle-shells --min-age 0 --no-fetch --json > "$(mktemp -t dissolve).json"
# --sweep
fleet audit [--host H] --idle-agents --idle-shells --min-age 0 --json > "$(mktemp -t cleanup-<host>).json"
fleet sync [--host H] --json > "$(mktemp -t sync-<host>).json"
```

For `--all-but-me`, also list the panes on the main checkout, since `fleet audit` covers
worktrees only:

```bash
me=$HERDR_PANE_ID
herdr pane list | jq -r --arg r "$repo" --arg me "$me" '.result.panes[]
  | select(((.foreground_cwd // .cwd) == $r) and .pane_id != $me)
  | "\(.pane_id)\t\(.agent // "shell")"'
```

Rows come back in tiers:

| tier | means | removing it loses |
|---|---|---|
| A | worktree folder gone, or a herdr space on a missing folder | nothing |
| B | merged (in the default branch, or a merged PR whose head IS this HEAD), clean | nothing |
| C | pushed, clean, not merged | nothing; the branch stays |
| D | uncommitted work or local-only commits | the work, unless saved first |
| K | an agent is **working/blocked** in it, or not picked | kept, never touched |

For every row with an agent, read what it last said:

```bash
herdr pane read <pane> --source recent-unwrapped --lines 40 | tail -12
```

**✓ is not done.** ✓ means the agent finished its turn, not its task. An agent that ended
on a question ("A or B?"), a plan waiting for approval, an AskUserQuestion popup, or "want
me to merge?" is **waiting on the human**: list it, never offer it, and never type into
its pane (keystrokes answer the popup).

## 2. Decide each row

| row | action |
|---|---|
| A | prune, nothing to save |
| B / C, no agent | remove (step 4b) |
| B / C, idle ✓ agent that reads finished | quit it, remove (step 4b) |
| D with an idle agent | **save first** (step 4a): its own agent commits, PRs, reports, then remove |
| D with no agent | rescue to a draft PR (step 4c), only if asked |
| clean worktree with zero own commits | remove; nothing to save, no PR |
| idle agent on the MAIN checkout (`--all-but-me`) | `/exit`, then `fleet close <pane>` (step 4d). Never removes the checkout |
| bare shell on the main checkout | `fleet close <pane>` |
| working / blocked / waiting agent | K: report it, touch nothing |
| the pane running this skill | always kept |
| behind only (`would ff`) | `fleet sync --go` (step 4e) |

## 3. Show the plan, then ask

One table per machine, grouped:

- **Save then remove**: D rows with an agent, and what is dirty in each.
- **Safe now**: A, plus B/C and empty worktrees with no agent. Nothing is lost.
- **Done agents**: B/C with an idle ✓ agent whose last output reads finished. Quitting keeps
  the transcript; `/herdr-bring` or `claude --resume` revives it.
- **Main-checkout panes** (`--all-but-me`): pane id, agent or shell, idle.
- **Waiting on you**: listed, not offered.
- **Unsaved, no agent (D)**: listed; rescue is offered separately.
- **Behind (sync)**: `would ff` rows, and SKIP reasons (modified, diverged, no upstream).

Then AskUserQuestion (multiSelect), one option per group that has rows. Put the row
COUNT and the repos in each description (`removes 23 worktrees in 11 repos`): a label alone
hides that `--sweep` is machine-wide. For a long "Done agents" list, let the human drop
names in "Other".

## 4. Act on exactly what was picked

### 4a. Save first (D rows with an agent)

**Who is the parent:** the agent in the repo's main checkout, where `/herdr-wt` ran.

```bash
repo=$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir | xargs dirname)
herdr pane list | jq -r --arg r "$repo" '.result.panes[]
  | select((.foreground_cwd // .cwd) == $r and .agent) | .pane_id' | head -1
```

Usually that is you. If no agent runs there, the parent report becomes a file in main's
vault, `$repo/ψ/inbox/handoff/<date>_dissolve_<wt>.md`, which the lead reads to the human.

Brief each agent with `fleet send <pane> "<brief>"`, never `herdr agent prompt` (it
prefix-matches names). The brief asks it to:

- Commit everything that is work, on this worktree's branch. Never `.envrc`, `.codex/`,
  `.env*`, shell snapshots or credentials. Hooks off: `git -c core.hooksPath=/dev/null commit`.
- Push the branch and open a PR signed with `/herdr-pr`. If nothing changed, say so and skip the PR.
- Tell the parent with `fleet send <parent-pane> "…"`, at most 6 lines: PR url, what was
  done, what is verified, what is left open, anything the parent must pick up.
- Finish with the single line `DISSOLVE-READY <pr-url|no-changes>`.

Brief them all, then `fleet watch` them all. When each goes idle, `fleet tail <pane>` and
confirm the `DISSOLVE-READY` line. If one fails, don't stop the others. It is now a B/C
row: go to 4b.

### 4b. Tombstone, then remove (A/B/C, done agents, saved D)

Removing a worktree ends its function, not its record. Before any `--go` that removes a
B/C worktree, write its tombstone:

```bash
python3 ~/.claude/skills/herdr-dissolve/tombstone.py <worktree-path>             # dry run
python3 ~/.claude/skills/herdr-dissolve/tombstone.py <worktree-path> --write --reason "merged PR #12"
```

It records what the worktree was (branch, born, own commits), why it ended, the successor
(PR url or `main@sha`) and where the record lives (branch kept, session ids with transcript
paths). It writes `<main checkout>/ψ/memory/tombstones/<date>_<label>.md`, or
`~/.herdr/tombstones/<repo>/` when the repo has no ψ. It never overwrites and never removes.

Read its `BLOCKER:` lines first:

- uncommitted or untracked files: not in any commit, so removal loses them. Save them (4a) or rescue (4c).
- HEAD not in main and no merged PR: not merged, so not a ceasing worktree.
- LOCKED: `/herdr-wt` and `wtui` lock every worktree they cut. Unlock deliberately
  (`git -C <repo> worktree unlock <path>`), do not force.

`/herdr-tree` shows the phase: `cease` rows are ready, `stand!` rows (main moved on, or
commits landed after the PR merged) are not.

**Why:** a removed thing with no death date and no successor is a record that lost its
chain (2026-08-22: 33 of 39 archived skills had neither). The tombstone is the chain.

```bash
fleet clean [--host H] --repo X --pick <wt1,wt2,...> --idle-agents --tier B,C,D --go   # named
fleet clean [--host H] --idle-shells --go                                               # sweep: safe now
```

`--pick` switches off the age rule for those rows only. It still re-checks just before
acting: a working agent, new edits or new local commits turn the row into a SKIP. It quits
an idle agent with ctrl-c (transcript kept), and removes the worktree and closes the space
through `herdr worktree remove`, so the sidebar agrees with git. **The branch stays** until
its PR merges.

Run it from a pane **outside** the worktree. The **whole space** goes, every pane in every
tab.

### 4c. Rescue D with no agent (only if asked)

```bash
fleet clean [--host H] --pick <wt,...> --tier D --pr --go
```

Commits to `rescue/<wt>`, pushes, opens a signed draft PR, removes the worktree. Guards:
`.codex/`, `.env*`, shell snapshots and credentials are never committed; anything key-like
in the staged diff stops it before pushing; repo hooks never run; a file over 10 MB keeps
its worktree; a rescue over 50 MB total is refused.

### 4d. Main-checkout panes (`--all-but-me`)

```bash
herdr agent prompt <pane> '/exit'          # an idle agent; its transcript stays
fleet close <pane>                         # or: herdr pane close <pane>
```

Never the pane running this skill. Never `rm` or remove the main checkout. If a pane was
the last one in its space, the space closes with it.

### 4e. Sync

```bash
fleet sync [--host H] --go
```

It only fast-forwards. `SKIP diverged ↑N` means someone has local commits there, which is
a human's call. It never merges, rebases or resets.

## 5. Record and report

```bash
fleet snapshot --commit        # the fleet history sees the change (local machine)
```

Report: before and after counts of worktrees and panes, PRs opened (with the parent's
acknowledgement), spaces closed, agents quit (pane id and session id so they can be
revived), fast-forwards (`↓N → sha`), tombstones written, and every SKIP with its reason.
Name what is left for the human: waiting agents, D rows, diverged checkouts.

## Self mode: `/herdr-dissolve self` (inside the worktree)

Do 4a yourself: commit, push, signed PR, report to the parent. You cannot remove the
worktree you run in, so hand that step off, then stop working:

```bash
fleet send <parent-pane> "DISSOLVE-READY <pr-url> — please: /herdr-dissolve $(basename "$PWD")"
```

## Guards and traps

1. **Never dissolve a working agent, and never one waiting on the human.** Read its last message.
2. **Fresh files count.** `.envrc`, `.DS_Store` and `._*` are junk to fleet
   (`worktrees.ts:49,71`): a modified `.envrc` reads `dirty: 0` and goes with the worktree.
   Any other uncommitted file makes it `SKIP uncommitted`. Gitignored data under 50 MB
   (`IGNORED_CAP`) is deleted too, so copy anything you want out of `.tmp/` first; over
   50 MB the worktree is kept. Do not bypass that check.
3. **Public repo:** before any PR or `--pr`, list what is about to be committed
   (`git -C <wt> status --porcelain -uall | head -40`). A 2026-09-24 run by hand pushed
   Codex session logs into public PRs; closed PRs keep their commits on GitHub, and only
   GitHub Support can purge them.
4. **A space can hold an agent in a second tab or pane.** 2026-10-05: atlas had been moved
   into another space as its own tab; closing that space would have killed it. Before
   closing a space, list ALL its panes in ALL tabs (`herdr pane list --workspace W`, then
   `herdr pane process-info --pane P`): close it only when every one is a bare shell or is
   in the plan.
5. **Removing a worktree with `git` alone leaves a herdr space on a missing folder.**
   `fleet clean` goes through `herdr worktree remove`; tier A closes earlier orphans.
6. **Other owners.** On m5, `arra-oracle-v4` and `odoo-yd` belong to other agents' work.
   `--sweep` uses `--skip arra-oracle-v4,odoo-yd` unless the user names them.
7. **Idle shells on main checkouts** are not worktrees. `clean` never removes a main
   checkout. Outside `--all-but-me`, closing those spaces is a separate
   `herdr workspace close <id>` the user must ask for.
8. **"local-only commits" may be MAIN's, not the worktree's.** A worktree cut from a local
   `main` that is ahead of `origin` reports main's unpushed commits as its own, so a clean,
   empty worktree reads as D. Check `git -C <repo> log --oneline origin/main..main` first:
   if those are the same commits, push main (the human's call) or treat the worktree by
   `git -C <wt> log main..HEAD` instead. Measured 2026-10-29 in aiexpo-oracle: main
   `[ahead 5]`, and both empty worktrees showed `5 local-only commits`.
9. **Survey files go to `mktemp`, not `.tmp/`.** Not every repo ignores `.tmp/`
   (aiexpo-oracle does not), and a survey file there shows up as untracked.
10. **Nothing merges here.** PRs wait for a human. Removing a worktree neither merges nor
   deletes its branch.

## Related

- `/herdr-wt`: creates what this dissolves
- `/herdr-issue`, `/herdr-ticket`: issue first, then a worktree; dissolve when the PR is up
- `/herdr-done`: is ONE session safe to close (read-only)
- `/herdr-pr`: the signature on the PR
- `/herdr-tree`: the phase of each worktree (`cease`, `stand!`)
