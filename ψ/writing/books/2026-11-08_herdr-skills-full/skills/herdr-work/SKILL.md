---
name: herdr-work
description: One command from a repo name to a working body — create-or-find a GitHub repo, clone it into the ghq tree, open it as its own herdr space, and start a Claude agent in it. Use when the user says "herdr-work <owner/repo>", "work on <name> (make the repo)", "spin up a repo and start on it", "create and incubate <repo>", or gives a repo that may not exist yet. Do NOT use to cut a worktree of an existing repo (use /herdr-wt), to move a session into herdr (use /herdr-bring), or to set up the ψ dev symlink flow (use /incubate).
argument-hint: "<owner/repo | name> [--public] [--desc \"...\"] [--here [--down]] [--no-agent] [--kind claude|codex] [--dry-run]"
---

# /herdr-work — name in, body out

```bash
python3 -I ~/.claude/skills/herdr-work/work.py <owner/repo | name> [options]
```

Print the output. Then handle the **trust prompt** (see below). Exit `0` on success, non-zero with
`✗ <problem>` and the exact fix command otherwise.

## What it does, in order

1. **Resolve the repo.** `<owner/repo>` is exact; a bare `<name>` defaults the owner to **laris-co**.
   - already cloned in the ghq tree → used as is
   - exists on GitHub, not cloned → `ghq get`
   - missing → `gh repo create <slug> --private --add-readme` (then `ghq get`). `--public` makes it public.
2. **Open a herdr space** at the repo (`herdr workspace create --cwd <path> --label <repo>`), or with
   `--here` a split in the current tab (`--down` for a horizontal split).
3. **Start an agent** (`command claude --dangerously-skip-permissions`, or `--kind codex`) and name it
   after the repo. `--no-agent` stops after the clone and prints how to open the space yourself.

## Options

| flag | effect |
|---|---|
| `--public` | create the repo public (default private) |
| `--desc "…"` | repo description on create |
| `--here` / `--here --down` | split beside/below the current pane instead of a new space |
| `--no-agent` | clone only; do not open a space or start an agent |
| `--kind codex` | start codex instead of claude |
| `--dry-run` | print what it would create/clone/open, change nothing |

## After it runs: the trust prompt

A **brand-new folder** always makes Claude Code ask *"Is this a project you created or you trust?"*.
The skill cannot answer it (it is a safety gate) — the agent sits `blocked` until someone accepts:

```bash
herdr --session <s> pane send-keys <pane> Down     # highlight "Yes, I trust this folder"
herdr --session <s> pane send-keys <pane> Enter
```

Then brief it (`/awaken`, a task, whatever the work is) with
`herdr --session <s> agent prompt <pane> "…"`.

## Notes and limits

- **Addressing:** the output prints the pane id and session; talk to the agent by pane id, never by name.
- **Deleting a test repo** needs the `delete_repo` gh scope, which this account's token does not carry by
  default: `gh auth refresh -h github.com -s delete_repo` first (ask the human — it changes auth scope).
- This does NOT symlink the repo into a caretaker's `ψ/incubate/` — that is `/incubate`'s job, and it has
  a known symlink-loop trap. `/herdr-work` only creates, clones, and opens a body.
- For an existing repo you want a parallel worktree of, use `/herdr-wt` (own branch + body), not this.

Tested 2026-10-13 on m5 session `neo`: dry-run for a new repo, an existing repo, a bare name and a
rejected URL; one real end-to-end run (created `laris-co/herdr-work-smoke-6c8c`, cloned it, opened
space `wD`, started the agent — which parked on the trust prompt as expected), then torn down.
