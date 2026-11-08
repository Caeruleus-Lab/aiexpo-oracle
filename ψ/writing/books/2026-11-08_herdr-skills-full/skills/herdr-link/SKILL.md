---
name: herdr-link
description: Package index for herdr sessions across machines — create a local session per oracle, provision a worker oracle on another machine, make sessions talk with no ssh typed, check every route, and tear a worker down. Use when the user says "herdr link", "local session / remote session", "make them talk", "provision a worker on white/black", "session per oracle", or asks which herdr-link skill to use. Routes to /herdr-link-local, /herdr-link-remote, /herdr-link-talk, /herdr-link-check, /herdr-link-teardown.
---

# /herdr-link — the package

One package, five skills, one shared script (`~/.local/bin/herdr-link`, dry by default, `--go` to run).
Built 2026-10-11 from the real work: Nexus moved into its own m5 session, neo-white and nexus-white
provisioned on white, black and white given a way back to m5, a reboot test on black, and the proof book
*ส่ง worker ไปอีกเครื่อง* (`athena-oracle/ψ/writing/books/2026-10-11_provision-worker/`).

## Which skill

| You want to | Skill | Script verb |
|---|---|---|
| give an oracle its own herdr session on THIS machine | `/herdr-link-local` | (herdr-move) |
| put a worker oracle on ANOTHER machine, surviving reboot | `/herdr-link-remote` | `herdr-link remote` |
| make two sessions on two machines talk, both ways, no ssh typed | `/herdr-link-talk` | `herdr-link talk` |
| see every session, machine and route at once (read-only) | `/herdr-link-check` | `herdr-link check` |
| remove a worker cleanly | `/herdr-link-teardown` | `herdr-link teardown` |
| start / stop / check a whole TEAM by charter name, on a session + machine | `/herdr-team-ctl` | `herdr-team-ctl start\|stop\|status <team>` |

Typical order for a new worker: `check` → `remote` (it calls `talk` at the end) → `check`.

## The map (as of 2026-10-11)

```
 m5 (beta)  sessions: laris-co (Athena w31:p1) · neo · nexus · nsm · phd · rd · default
   saved machines: white-laris-co · white-nsm · white-neo · white-nexus · black-phd
        │ herdr --machine <label>                ▲ herdr --machine m5-laris-co
        ▼                                        │
 white (nat)  neo: neo-white · nexus: nexus-white · nsm · arkkra · laris-co
 black (phd-oracle)  phd: dustboy-phd-oracle (system unit herdr-phd-oracle.service)
```

## Five rules (every skill in the package follows them)

1. **One soul = one body.** A second machine gets a worker with a NEW name (`neo-white`), never a copy.
2. **Discord on one body only.** Workers never run `--channels` and never hold a bot token.
3. **One worker per worktree.** `--continue` resumes the newest conversation of the *folder*.
4. **Talk through herdr.** Send and read with `herdr --machine <label>`; one saved machine = one session.
5. **Back up before editing** (roster, authorized_keys, .envrc, oracles.json). Never delete history:
   `git branch -d`, never `-D`; stopped session folders stay.

Confirm with the human before anything outward: adding a key to authorized_keys, rebooting a machine,
posting anywhere. The script prints a dry plan first — show it, then `--go`.

References: `athena-oracle/ψ/writing/cheatsheets/2026-10-11_provision-worker-oracle.md` (playbook),
`…/2026-10-11_herdr-sessions-machines.md`, `…/2026-10-11_white-workers-autostart.md`.
