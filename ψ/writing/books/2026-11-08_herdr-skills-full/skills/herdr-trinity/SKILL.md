---
name: herdr-trinity
description: "One pass that winds down EVERY worktree of the current repo under Nat's trinity rule (arise · stand · cease, เกิดขึ้น ตั้งอยู่ ดับไป): table, peek every agent, brief them all to commit + push + signed PR + report, collect the reports, merge on Nat's go, pull main safely, move big ignored data to tombstones, delete only what is rebuildable (with a RETIRED ledger row), repoint anything that still runs from a worktree, then fleet clean. Use when Nat says \"trinity\", \"trinity unload all\", \"dissolve all\", \"clean fleet all\", \"merge all and clean all\", \"retire all worktrees\", or /herdr-trinity. Do NOT use for one worktree (use /herdr-dissolve) or to create one (/herdr-wt)."
argument-hint: "[--plan] [--only <wt,...>] [--skip <wt,...>]"
---

# /herdr-trinity — wind down every worktree in one pass

Built 2026-10-26 from the night neo dissolved 10 worktrees by hand with 6 skills
(/herdr-wt-ship, /herdr-dissolve, /herdr-pr, fleet clean, /return, relic5). This chains
them. The rule is Nat's trinity (relic5 `docs/RETIRED.md`):

> Everything arises, stands, ceases. "Nothing is deleted" covers only the middle.
> A retirement is three written steps: **stop** using it · **record** where it went and
> how to bring it back · name the **successor** (or "nothing" and why).
> Rebuildable things may simply cease (Nat 10-15). Once uploaded, redundant copies go (10-25).

Nat's go words already given for this flow: "merge all and clean all", "yes if rebuildable
go delete". Without them, stop at the step that needs them.

## 0. Table (always first)

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
python3 -I ~/.claude/skills/herdr-wt-ship/wt_table.py --no-size
gh auth status 2>&1 | head -3   # 401 = stop: print `! gh auth login -h github.com -p ssh -w`, or run it in a pane
```

`gh` dies silently mid-flow (token invalid, 2026-10-26). Check it before briefing anyone:
every brief ends in a PR.

## 1. Peek every agent

```bash
herdr --session <s> pane read <pane> --source recent-unwrapped --lines 60 | rg -v '^\s*$' | tail -14
```

- `blocked` is often a **codex update prompt**, not real work: `herdr pane send-keys <pane> Escape`.
- `/goal active`: its brief must say what is left on the goal.
- A space whose folder is gone (tombstone exists): `herdr --session <s> workspace close <ws>`.
- A worktree with no agent: do its PR yourself (`gh pr create … --head <branch>`, then
  `herdr-sign.sh <model> <me> --work <wt> | gh pr comment <N> --body-file -`).

## 2. Brief all, in parallel (fleet_send, never `herdr agent prompt`)

Parent = this pane (`<me>@<session>`). One brief per agent, specialised by what the table
says (big data, a running service, an existing PR):

```
/herdr-dissolve brief from your parent <me> (<pane>@<session>), for Nat. Wind this worktree down:
1. Commit everything that is work on this branch. Never .envrc, .codex/, .env*, keys, phone data.
   Hooks off: git -c core.hooksPath=/dev/null commit. List files and secret-scan first.
2. Push. Open a PR (or push to the existing #N) and sign it with /herdr-pr.
3. Gitignored data over 50 MB: do NOT delete. Say what it is, rebuildable or not, the rebuild command,
   and which part is the only copy.
4. Anything still running from this path (MCP, maw plugin, launchd, app, panes): list it and give the
   exact commands to repoint it at the main checkout. Do not move it yourself.
5. Report to me with fleet_send to <pane>@<session>, max 6 lines: PR, done, verified, open, data, pick-up.
6. Last line: DISSOLVE-READY <pr-url|no-changes>  or  NOT-READY <reason>
Do not merge. Do not remove the worktree yourself.
```

Then **stop and wait**. Reports arrive as messages; never sleep-poll.
A worktree whose PR is already merged and signed needs no brief: go straight to step 8.

## 3. Collect → one table for Nat

Per worktree: PR · READY / NOT-READY · big data (size, rebuildable?, rebuild command) ·
what still runs from it · pick-ups. Things committed nowhere (site code living only in
`.tmp/`) are the dangerous row: copy them into their home repo before step 6.

## 4. Merge (Nat's go only)

```bash
gh pr list -R <slug> --state open --json number,mergeable,headRefName,title
for n in <smallest/vault first ... biggest last>; do gh pr merge $n -R <slug> --merge; done
```

Never `--admin`, never squash a branch another worktree still builds on, never delete the
remote branch.

## 5. Pull main without losing local notes

`git pull --ff-only` aborts when untracked files sit where merged files land (vault notes
other agents wrote straight into the main checkout). For each blocking path:

```bash
B=.tmp/pre-pull-untracked-$(date +%d%b); mkdir -p $B
# identical to origin/main → move aside (safe); different → keep the LOCAL copy, pull, put it back as a modification
[ "$(git hash-object "$f")" = "$(git rev-parse origin/main:"$f")" ] && mv "$f" "$B/$f"
```

## 6. Big data: stop · record · successor

```bash
T=~/.herdr/tombstones/<repo>; mkdir -p $T
mv <wt>/.tmp $T/<slug>.tmp          # same APFS volume: instant, frees nothing yet
```

On "yes if rebuildable go delete": delete only parts with a named rebuild command, keep any
only-copy (paid TTS caches, raw test frames, uncommitted code), and append a row per deletion
to `$T/RETIRED.md`: what · size · record (PR) · successor / rebuild command.

## 7. Repoint what still runs from a worktree

Use the agent's own commands from its report. The usual set:

```bash
claude mcp remove <name> -s user && claude mcp add <name> -s user -- <bin> <main-checkout path>
ln -sfn <main-checkout path> ~/.maw/plugins/<name>
```

Running sessions keep the old process until they restart; say so.

## 8. Remove — fast path when the PR is already merged AND signed (Nat, 2026-10-26)

Nat: "if clean, check the PR; if already /herdr-pr we can go directly from here." So do NOT
wait for agents to dissolve themselves and do NOT run bare `fleet clean --pick`. Use:

```bash
~/.claude/skills/herdr-trinity/fast-remove.sh <worktree-path>...   # in a pane (herdr-pane-run pattern)
```

Per worktree it checks, in order, and stops at the first failure with the fixing command:
clean (a modified `.envrc` is saved as a patch and restored) → PR merged → `/herdr-pr`
signature in the PR **body or a comment** → no ignored data over 50 MB → tombstone →
**closes the herdr space(s)** of the worktree (ctrl-c to every agent in them, transcripts stay on disk, then
`workspace close`; leftover shell panes die with it) → `fleet clean --repo <slug> --pick <wt> --go` →
`git branch -d`. Space first because `fleet clean` answers `skipped 1` (no reason) when an omp/codex agent is
still alive in the worktree (rapid-harbor). Remote branch stays.

A worktree already removed but whose space is still in the sidebar (fleet leaves extra shell panes):
`~/.claude/skills/herdr-trinity/fast-remove.sh --close-spaces <old-worktree-path>`.
Before closing a space, `herdr pane process-info --pane <p>`: a pane that is NOT an idle shell
(a server, an install retry loop) dies with the space; say so in the report.

Why this and not `ship.sh` / bare `fleet clean` (all measured 2026-10-26):

| trap | effect | fix in fast-remove.sh |
|---|---|---|
| `fleet clean --pick` without `--repo` scans all 1,321 repos | ~7 min per worktree, 3 in parallel looked frozen | `--repo <slug>`: eight worktrees planned in 68 s |
| `fleet clean` skips a worktree with >50 MB ignored data | prints `removed 0 · kept 0 · skipped 0`: no reason given | refuses up front, prints the `mv` to the tombstone dir |
| `ship.sh` reads signatures from PR comments only | agents sign in the PR body → "no signature" | body or comment counts |
| `.envrc` is tracked and `maw token use` rewrites its label | worktree "dirty" forever | patch saved, `git checkout -- .envrc` |
| agent blocked on a codex update prompt / usage limit | tier K "agent working" | `Escape` it first (step 1); a limited agent is still removable once its PR is merged |

Open PRs for work nobody committed (agent at its limit, no agent left) are made by you in
step 1/2; then they are merged in step 4 and removed here. Afterwards:
`python3 -I ~/.claude/skills/herdr-wt-ship/wt_table.py --no-size`.

## 9. Report

One table: worktree · PR merged · data freed / kept (where) · removed yes/no and why · what Nat
still owns. Then the freed-disk number (`df -h`) and the `RETIRED.md` path.

## Traps (all hit on 2026-10-26)

- **Never edit `fast-remove.sh` while a pane is running it.** bash reads a script as it goes; an in-place edit
  made the live run die with `syntax error near unexpected token` after six good removals. Wait for the pane's
  report, then edit.
- A branch with no PR and nothing main lacks (`HEAD` already in `origin/main`) needs no PR: `fast-remove.sh`
  accepts it (rapid-harbor's cheatsheet had gone out on another branch).
- A hand-written 'Built by' line is not the `/herdr-pr` block (no `herdr:` address): sign it with
  `HERDR_SESSION=<s> herdr-sign.sh <model> <pane> --work <wt> --ref <head> | gh pr comment <N> --body-file -`
  (the `pane@session` form is rejected; set `HERDR_SESSION`).
- `pkill -f <pattern>` over ssh kills the ssh itself (its argv matches): use `[b]racket` patterns.
- zsh `$C:r…` in `git push origin $C:refs/...` eats `:r`: write `"${C}:refs/heads/…"`.
- A heavy MCP at user scope = one copy per session (sate-rag 15 GB × 4 filled swap). Check
  `ps -Ao rss,args -m | head` before blaming anything else for a hot fan.
- Bare `fleet clean --pick` scans every repo (minutes, silent). Always `--repo <slug>`; `fast-remove.sh` does.
- Putting `| grep | tail` after a long command hides its progress until it exits: in a pane, let it print.
