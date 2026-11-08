---
name: herdr-link-remote
description: Provision a worker oracle on another machine (white, black) end to end — check the box, find a token it really has, cut a worktree from origin/main, copy and allow .envrc, add an autostart roster row + enable the systemd user unit, first start without --continue, name and brief the agent, then make it talk to m5. Use when the user says "put neo on white", "white nexus", "provision a worker", "remote session with an agent", "survive reboot". Part of the /herdr-link package.
---

# /herdr-link-remote — a worker on another machine

Proven 2026-10-11 on white: neo-white (session neo, 4af6d877), nexus-white (session nexus, 43ac825c),
and the demo neo-demo that the proof book *ส่ง worker ไปอีกเครื่อง* captured step by step (restart →
same conversation 7b100254 came back).

## Script (dry first, then --go)

```bash
herdr-link remote nat@white.follow-rankine.ts.net /opt/Code/github.com/laris-co/nexus-oracle nexus nexus-white
herdr-link remote nat@white.follow-rankine.ts.net /opt/Code/github.com/laris-co/nexus-oracle nexus nexus-white --go
herdr-link remote … --token rb      # when the repo's .envrc names a token that box does not have
```

## The steps (what the script does, and what to check by eye)

| # | step | the check that matters |
|---|---|---|
| 0 | check the box: `herdr --version`, `Linger=yes`, `herdr-session@.service`, repo owner, `git status -sb` | repo owned by the login user (`nat`), not `nm` |
| 1 | token: the script greps `claude/token-…` from `.envrc` (white may lack `rg`) vs `ls ~/.password-store/claude/` | the named token exists on THAT box |
| 2 | `git worktree add -b agents/<worker> <repo>/wt/<worker>-athena-<date> origin/main`, `cp -p .envrc`, `direnv allow` | `direnv exec . sh -c 'printf %s "$CLAUDE_CODE_OAUTH_TOKEN" \| wc -c'` > 0 |
| 3 | roster row (TABs via printf, backup first) + `systemctl --user enable --now herdr-session@<s>` — enable ONLY when the session already runs (Trap A) | `awk -F'\t' '$1=="<s>"'` shows 4 fields |
| 4 | first start WITHOUT `--continue` + `agent rename <pane> <worker>` (script); **the brief is yours** — send it after | the agent answers its brief |
| 5 | `/herdr-link-talk` | the worker's one-line reply arrives over `m5-laris-co` |

Brief template — the script does NOT send it; send it yourself with `herdr --session <s> agent prompt <pane>` on the box:
"You are <worker>, a NEW <role> worker on <box> (session <s>, pane <pane>). Not a copy of <origin>. No Discord.
Branches + PRs, never main. .envrc is local — never commit it. Reply to Athena: herdr --machine m5-laris-co
agent prompt w31:p1 '<msg>'. First: read CLAUDE.md, /recap --quick, reply ONE line: name, model, session id."

## Traps (all met for real)

| trap | avoid |
|---|---|
| `.envrc` asks for `claude/token-nh`, the box has none → empty token | `--token <name>`: local edit in the worktree only |
| `git pull` blocked by local `.envrc` changes (main checkout) | worktree from origin/main instead; or back up + `git stash push -- .envrc` |
| main checkout holds someone's WIP (droidread branch on white's nexus) | worktree — never touch the main checkout |
| `.envrc` is TRACKED in neo-oracle: `git check-ignore` exits 1 and an `&&` chain stops before `direnv allow` | check with `git status --short .envrc`, not check-ignore |
| hook: `direnv: error … .envrc is blocked` | `direnv allow` inside the worktree |
| hook: `No conversation found to continue` (fresh folder) | first start by hand without `--continue` |
| session already running from a `herdr --remote` attach | `enable` only; systemd takes over at the next boot |
| roster cwd ≠ pane cwd | the hook creates a new space — cwd must be the worktree path |
| two agents in one folder | the next boot's `--continue` may resume the other one's conversation |
| model differs between workers (neo-white Sonnet, neo-demo Opus) | not investigated — say which you want in the brief / launch line |

Black is different: phd runs from a SYSTEM unit `/etc/systemd/system/herdr-phd-oracle.service`
(`oracle-herdr-up phd <repo> <name> … --channels`); find it with `systemctl list-units --type=service --all | rg herdr`.
