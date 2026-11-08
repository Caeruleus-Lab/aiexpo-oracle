---
name: herdr-whoami
description: Show where THIS agent is running — machine (local or over ssh), herdr session / space / tab / pane, Claude session id + transcript path, pwd vs the session's start cwd, git branch, worktree-or-main and remote. Use when the user asks "which server", "which session are we", "what herdr session", "where am I", "whoami", "session id", "pwd", "local or remote". Do NOT use to list every session on the machine (use /herdr-ls-all) or every body of one oracle (use /herdr-info).
---

# /herdr-whoami — where am I

Run it. Print the output inside one fenced block. Stop.

```bash
python3 -I ~/.claude/skills/herdr-whoami/whoami.py
```

Lines starting with `!` are warnings — mention each in one line after the block:

- `herdr pane records session X, but this process is Y` — the pane's saved agent record is stale;
  a reopen would resume the wrong conversation.
- `$HERDR_PANE_ID=X is stale (pane was moved); live pane is Y` — env is fixed at process start;
  after `herdr pane move` only herdr knows the real pane. The rows show the live one.
- `pwd moved away from the session's start cwd` — the Bash tool `cd`'d somewhere; git rows describe
  the new pwd, not the repo the session started in.

## Sources

| row | from |
|---|---|
| host / user / reached | `hostname`, `$USER`, `$SSH_CONNECTION` (set = remote ssh login) |
| herdr session / space / tab / pane | `$HERDR_SESSION`, `$HERDR_WORKSPACE_ID` + `herdr workspace list` label, `$HERDR_TAB_ID`, `$HERDR_PANE_ID` |
| pane cwd | `herdr pane get` → `foreground_cwd` |
| session id / name / version / start cwd | `$CLAUDE_CODE_SESSION_ID`, `~/.claude/sessions/$CLAUDE_PID.json` |
| transcript | `~/.claude/projects/<start cwd, non-alnum → ->/<id>.jsonl` |
| git | `git status -sb`, `--git-common-dir` (worktree vs main), `remote get-url origin` |

Env vars are read, never the socket of another session: `herdr` with no `--session` hits
`$HERDR_SOCKET_PATH`, which is this pane's own session — exactly what is wanted here.
