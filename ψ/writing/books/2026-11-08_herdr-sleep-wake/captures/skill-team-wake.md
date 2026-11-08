# team-wake SKILL.md (laris-co/laris-team skills/team-wake/SKILL.md, read 2026-11-08; newer than ~/.claude copy)
---
name: team-wake
description: After a reboot or a herdr server restart, put every laris-co oracle back the way it should run. herdr has already resumed each pane's conversation (resume_agents_on_restore = true) but as a plain `claude --resume` with no bot; this skill relaunches the ones that own a Discord bot on this machine with their real launch line plus --resume on the same conversation, stops the ones marked asleep, and leaves the rest. Use when Nat says "wake", "team wake", "after reboot", "bring all back", "bots are offline after restart", or when the orchestrator (LarisCo host) itself has just been resumed by herdr. Do NOT use to start a whole team that is on vacation (use `just up <team>`), or to move an oracle between machines.
---

# /team-wake — the orchestrator brings everyone back

Nat 2026-10-28: no system-level waker. herdr resumes every open pane; the orchestrator (LarisCo host,
`laris-co/laris-team` main) runs this once afterwards and fixes what a plain resume gets wrong.

## Why a plain resume is not enough

herdr keeps each pane's `cwd` and conversation id (`~/.config/herdr/sessions/<session>/session.json`) and runs
`claude --resume <id>`. It cannot keep the environment: no `DISCORD_BOT_TOKEN`, no `DISCORD_STATE_DIR`, no
per-oracle Claude account. So every bot comes back offline.

## Run it

```bash
python3 "$(ghq root)/github.com/laris-co/laris-team/skills/team-wake/wake.py"          # plan
python3 "$(ghq root)/github.com/laris-co/laris-team/skills/team-wake/wake.py" go       # do it
```
(`just wake` / `just wake go` in laris-team do the same.)

**Automatic:** `.claude/settings.json` in laris-team has a `SessionStart` hook (matcher `resume`). When herdr
resumes the orchestrator (laris-team MAIN checkout only, never a worktree body) it runs `wake.py spawn`: a
pane splits under the host (never a new space), waits 60 s for the other panes, runs `go`, prompts the host pane with the result and closes.

**After a member machine reboots (white), #98:** the hook above runs only when m5's host session starts, so a reboot
of white alone woke nothing (2026-11-02 22:38: every laris-co bot on white stayed deaf). `just wake-unit white`
installs `team-wake.service` there, a systemd **user** unit (`tools/systemd/team-wake.service`, rendered by
`tools/wake-unit.sh`, needs linger). It runs after that machine's `herdr-session@*` units, waits 60 s, then runs
`wake.py boot`: `go` on every herdr session there, then a one-line `WAKE <machine> after boot: …` to the host pane on
m5 (found by cwd through the saved herdr machine for session `laris-co`). If m5 cannot be reached, the report is in
`~/.local/state/laris-team/wake-boot.log`. The install is idempotent: it enables the unit and never starts it.

```bash
just wake-unit white --test   # render, systemd-analyze --user verify, run the unit's ExecStart once with
                              # WAKE_BOOT_DRY=1 (plan only, no go): installs nothing, reboots nothing
just wake-unit white          # install + enable (runs at the next boot)
```
macOS (m5) has no unit: the host's SessionStart hook is its waker.
A lock (`~/.local/state/laris-team/wake.lock`, 10 min) keeps it to one run; log in `wake.log` beside it.

1. Read the plan. Each row is `ok`, `bot` (relaunch with its bot) or `stop` (asleep).
2. `go`. A `working` agent is skipped unless `go force`: never cut a turn without being asked.
3. Run the plan again ~20 s later. Every oracle that owns a bot here must say `bot on`.
   `bot on` means `--channels`, a live discord plugin child AND the bot token in that claude (`DISCORD_BOT_TOKEN` in
   its env or in `<DISCORD_STATE_DIR>/.env`): a herdr resume keeps `--channels` but drops the token (#93).
4. Report to Nat: who was relaunched, who was stopped, who was skipped and why.

## Other machines (white)

- `python3 wake.py --machine white [go]` (or `just wake --machine white`) runs it on white over ssh: white's own herdr,
  pass and claude processes. m5's `auto` does this for every machine named in a member's `machine:`.
- After a restart of white alone: the team desks that live there (media-team, manager-team) carry the same
  `SessionStart resume` hook, so the first desk herdr resumes spawns team-wake on white. Worktree bodies never do.
- white needs `[session] resume_agents_on_restore = true` in `~/.config/herdr/config.toml` (set 2026-10-29).
- Every machine also needs herdr's claude integration (`herdr integration install claude`; `herdr integration status`
  must say `claude: current`). Without it herdr saves no conversation ids and resumes nothing: white had none until
  2026-10-29, so its reboot test brought back no laris-co or drdo-session agent.
- Prove it with `just reboot-test <machine>` (dry) and `--go` (reboots, waits, compares, report).

## Rules it keeps

- **One bot = one body.** A bot already online in another pane of the session is never started again; an oracle whose
  `machine:` is another box stays without Discord here.
- **The conversation is kept.** The relaunch uses `--resume <the same id>` herdr saved.
- Teams on vacation have no open panes, so herdr resumes nothing for them; this skill does not wake them either.
- Never run it on another agent's pane that is mid-turn. `go` never touches the orchestrator's own pane; the `auto`
  helper pane does, last: if the host came back without its bot, it quits the host and relaunches it with its launch
  line and `--resume` on the same conversation, then sends the report (2026-10-31: the LarisCo bot stayed offline
  after two resumes because nothing relaunched the host).

## Setup (once per machine)

```toml
# ~/.config/herdr/config.toml
[session]
resume_agents_on_restore = true
```
`just skills-install` copies this skill to `~/.claude/skills`.
