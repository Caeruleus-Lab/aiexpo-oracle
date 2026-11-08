---
name: herdr-link-talk
description: Make two herdr sessions on two machines talk to each other both ways with no ssh typed — save the remote session as a herdr machine here, give the remote user a way back (host key, key check, machine add), and verify with a round trip. Use when the user says "make them talk", "talk without ssh", "add machine", "they can't reply to m5", "white can't reach laris-co". Part of the /herdr-link package.
---

# /herdr-link-talk — both ways, no ssh typed

`herdr --machine <label> <command>` runs the command on a saved machine's session. ssh runs underneath;
nobody types it. **One saved machine = one remote session** — `--machine X --session Y` is refused, and
`herdr --remote …` only attaches the screen (it cannot `agent list` or `agent prompt`).

## Script

```bash
herdr-link talk nat@white.follow-rankine.ts.net neo            # dry plan
herdr-link talk nat@white.follow-rankine.ts.net neo --go       # do it
```

## By hand (what the script does)

```bash
# 1. here (m5): save the remote session
herdr machine add nat@white.follow-rankine.ts.net --label white-neo --remote-session neo
herdr --machine white-neo agent list

# 2. there: can the remote user reach m5 at all?
ssh -o BatchMode=yes beta@m5.follow-rankine.ts.net hostname
#    "Host key verification failed"  -> ssh-keyscan -t ed25519 m5.follow-rankine.ts.net >> ~/.ssh/known_hosts
#    "Permission denied (publickey)" -> STOP. Ask the human to add the remote user's ~/.ssh/id_ed25519.pub
#                                       to ~beta/.ssh/authorized_keys on m5 (back it up first)

# 3. there: save m5's session as a machine (as the user the agent runs as)
herdr machine add beta@m5.follow-rankine.ts.net --label m5-laris-co --remote-session laris-co
herdr --machine m5-laris-co agent prompt w31:p1 "[white:neo-white] route ok"
```

Tell the remote agent its reply route in its brief:
`herdr --machine m5-laris-co agent prompt w31:p1 "<msg>"`.

## What exists (2026-10-11)

| from | label | id | to |
|---|---|---|---|
| m5 | white-nsm / white-neo / white-nexus / white-laris-co | 58f05059 / 64957122 / d59f7577 / 83ef54c5 | white sessions |
| m5 | black-phd | efe95d03 | black phd |
| white (nat) | m5-laris-co | e4fc00fc | m5 laris-co |
| black (phd-oracle) | m5-laris-co | 8788d179 | m5 laris-co |

## Traps

| trap | avoid |
|---|---|
| `unknown machine 'efe95d03'` | full id or label |
| `--machine cannot be combined with other launch options` | add another saved machine for the other session |
| `machine add` on the remote ran as the wrong user (old herdr, `unknown option: --machine`) | run as the user the agent runs as (`phd-oracle`, `nat`) |
| m5's machine list is ONE list for every session | relabel/disable affects every window; hide with `herdr machine fold`, never `disable` |
| adding a machine on m5 that points at m5 | not needed: local sessions use `herdr --session <s>` |
