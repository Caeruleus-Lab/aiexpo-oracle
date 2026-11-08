---
name: herdr-finished
description: Finish the current herdr session in one pass, with no popups. Audit with herdr-done, write the /rrr retro, sign the PR with /herdr-pr, then remove the worktree only if its PR is merged (otherwise keep it and close just the space), print one summary line, `maw hey` that summary back to the oracle that owns this worktree (its main checkout), and close the session. Use when the user says "finished", "herdr finished", "we are done here", "wrap up and close", "rrr + pr + close", or /herdr-finished. Do NOT use to only check whether a pane is safe to close (use /herdr-done), to clean up many worktrees (use /herdr-wt-ship), or for a session that is not in a herdr worktree (use /done).
---

# /herdr-finished — retro, sign, tidy, close

One command at the end of a worktree session. It chains skills that already exist and
adds the one decision they leave open: what happens to the worktree.

```
herdr-done audit ─ blocked? ─▶ STOP, print the fixing command
      │ clean
      ▼
/rrr retro (vault write, not committed on the feature branch)
      ▼
/herdr-pr sign the PR this session produced (skip if already signed)
      ▼
PR merged? ── yes ─▶ remove worktree via herdr + delete local branch, close space
      │ no (open / draft)
      ▼
keep worktree, close the space only
      ▼
one summary line ─▶ maw hey it back to the owning oracle (main checkout)
      ▼
the session closes itself (last action)
```

**No popups anywhere** (Nat, 2026-10-09, #157). The human asked for the finish by running
this; every step either proceeds or stops with a command to run. Never AskUserQuestion here.

## Step 0 — where am I

```bash
date '+%F %T %Z'
W=$(git rev-parse --show-toplevel); B=$(git branch --show-current)
echo "pane=$HERDR_PANE_ID space=$HERDR_WORKSPACE_ID wt=$W branch=$B"
git rev-parse --git-dir | rg -q '/worktrees/' && echo linked-worktree || echo MAIN-CHECKOUT
```

In the **main checkout**, never remove anything: do steps 1-3, skip step 4's removal, and
close the space only if asked.

## Step 1 — audit (stop on blockers)

```bash
~/.claude/skills/herdr-done/herdr-done.sh; echo "rc=$?"
```

- `rc=1` (uncommitted, unpushed, no upstream, detached): **stop**. Print each blocker with
  the exact command that fixes it (`git -C <W> add <files> && git -C <W> commit …`,
  `git -C <W> push -u origin <B>`), and do not go on. Only fix it yourself if the change is
  this session's own work and the commit rules allow it.
- Warnings/notes (dir ≠ branch, PR open, locked) are not blockers; carry them into the summary.

## Step 2 — retro

Invoke the `rrr` skill (default mode; pass `--file` with your own transcript to the session
clock when agents share a cwd). It writes to the oracle's `ψ/memory/…`. **Never commit
the retro onto the feature branch** — it would ride into the feature PR.

When `ψ` is a tracked folder (neo-oracle: yes, `vault/retro-*` PRs like #155), ship it as
its own draft PR built from `origin/main` with a **temporary index**, so this worktree's
branch and checkout are untouched (first used 2026-10-09, PR #159):

```bash
git fetch -q origin main
export GIT_INDEX_FILE="$PWD/.tmp/vault.index"; rm -f "$GIT_INDEX_FILE"; git read-tree origin/main
for f in <retro.md> <lesson.md>; do
  git update-index --add --cacheinfo 100644,"$(git hash-object -w "$f")","$f"; done
# metrics: main's file + only THIS run's row, never the worktree's whole file
git show origin/main:ψ/memory/learnings/session-metrics.md > .tmp/metrics.main
tail -1 ψ/memory/learnings/session-metrics.md >> .tmp/metrics.main
git update-index --cacheinfo 100644,"$(git hash-object -w .tmp/metrics.main)",ψ/memory/learnings/session-metrics.md
C=$(git commit-tree "$(git write-tree)" -p origin/main -m "vault: retro <date> <slug>")
unset GIT_INDEX_FILE
git push origin "${C}:refs/heads/vault/retro-<d><mon>"     # ${C}, braces required — see trap
gh pr create --draft --base main --head vault/retro-<d><mon> --title "vault: retro …" --body-file <f>
```

If `vault/retro-<d><mon>` already exists on the remote, add `-<slug>`; never push over it.
The worktree keeps uncommitted copies of the retro files; they are already in that PR. If
ψ is a symlinked vault (not tracked), skip the PR: the write is already where it belongs.

## Step 3 — sign the PR

Find the PR of this branch:

```bash
gh pr list --head "$B" --state all --json number,state,isDraft,url,mergedAt -q '.[0]'
```

- No PR: say so in the summary (`gh pr create --draft --base main --head "$B"` as the fix
  line); do not create one unasked.
- PR exists and has no "Built by" signature from this session
  (`gh pr view <N> --json comments,body -q '[.body, .comments[].body]|join("\n")' | rg -c 'Built by'`):
  invoke the `herdr-pr` skill on it. Name the agent first (`herdr agent rename
  "$HERDR_PANE_ID" <short-topic>`), or the block addresses a bare pane id. Because step 6
  closes the space, the herdr address dies with it: append a resume line to the block
  before posting —
  `cd <W> && claude --resume <session-id>` (the worktree is kept whenever the PR is open).
- Already signed: skip.

## Step 4 — the worktree: remove only if merged

Re-read the PR state (it can merge while you work):

```bash
gh pr view <N> --json state,mergedAt -q '.state'
```

| PR | worktree | branch | space |
|---|---|---|---|
| `MERGED` | remove via herdr | `git branch -d` (local only) | goes with the worktree |
| `OPEN` / draft | **keep** (review may need it; the PR's Resume line points here) | keep | close |
| `CLOSED` unmerged | keep; say so | keep | close |
| none | keep | keep | close |

Merged removal goes through the existing tooling so the sidebar agrees with git:

```bash
bash ~/.claude/skills/herdr-ticket/ship.sh done "$W" --go
```

Never `git branch -D`, `rm -rf`, `git worktree remove --force`, or deleting the remote
branch. Over 50 MB of ignored data in `.tmp/`: move it to `~/.herdr/tombstones/<repo>/`
first (see /herdr-wt-ship).

## Step 5 — report back to the oracle that owns this worktree

A worktree agent is a body of its repo's oracle. Before this session disappears, tell the
oracle's main body what came back (Nat, 2026-10-09: *"check his oracle and maw hey back here
like from us"*). The owner is the **main checkout** of this repo; `maw hey` takes that path
and resolves it to the agent running there ("matched by path").

```bash
M=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")   # main checkout
[ "$M" = "$W" ] && echo "in the main checkout: no report-back" || {
  maw hey --dry "$M" "x" 2>&1 | head -2            # must show a pane id, e.g. "● <repo>/main wAM:p2 · claude"
  maw hey "$M" "finished from $(basename "$W") ($B, pane $HERDR_PANE_ID):
PR <url> (<state>) · signed <yes|already|no PR> · retro <path>
wt <removed | kept at $W — resume: cd $W && claude --resume <session-id>>
<one line: what changed, or the blocker it stopped on>"
}
```

- Stamp it as from this worktree (name + branch + pane): the message lands in the oracle's
  prompt and must say who is talking and how to reach it after the space is gone.
- `--dry` says `no agent '…'`: the oracle is not running. Do not wake it; put
  `report-back: oracle not running` in the summary instead.
- Send it once, before Step 6. Never `herdr agent prompt <name>`: it prefix-matches and
  misdelivers.
- Step 1 stopped on blockers? Still send it, with the blocker and its fix command, so the
  oracle knows this worktree is waiting.

## Step 6 — summary, then close (LAST action)

Print one block, real values, nothing after it:

```
finished  <repo>/<branch>
  PR      <url> (<state>)  signed: yes|already|no PR
  retro   <path>
  wt      removed | kept at <W> (PR open) — resume: cd <W> && claude --resume <session-id>
  hey     sent to <oracle pane> | oracle not running | main checkout
```

Then close the space as the **very last tool call** of the turn. Closing it kills this
agent's own pane, so detach it and let the turn end first:

```bash
nohup sh -c "sleep 3; herdr workspace close $HERDR_WORKSPACE_ID" >/dev/null 2>&1 &
```

Closing a herdr space destroys nothing: the worktree (if kept) and the transcript stay,
and `fleet resume` or `claude --resume` brings the session back. If the merged branch
already removed the worktree through herdr, the space is gone with it: skip this call.

## Traps

- **zsh eats `$C:r…`.** `git push origin $C:refs/heads/x` became `<sha>efs/heads/x`
  (`:r` is zsh's strip-extension modifier) and the push failed. Always `"${C}:refs/…"`.
- **Step 1 after a retro run.** The retro copies left in the worktree are uncommitted, so
  a re-run of the audit reports them. They are in the vault PR; name that PR, don't block.

- **A clean audit is not a reason to remove.** Open PR = keep the worktree. This is the
  one rule that separates this skill from a plain cleanup.
- **The space close must be last.** Anything after it never runs; a summary printed after
  it is lost.
- **Several panes in one space** (a buddy, a split): closing the space closes them too.
  If `herdr pane list` shows other live agents in `$HERDR_WORKSPACE_ID`, close only this
  pane instead (`herdr pane close $HERDR_PANE_ID`, same detach) and name the others in the
  summary.
