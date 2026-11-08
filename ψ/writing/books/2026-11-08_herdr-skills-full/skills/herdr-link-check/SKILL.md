---
name: herdr-link-check
description: Read-only check of every herdr session, saved machine and cross-machine route — local sessions running, machines reachable, which agents each remote session holds, autostart units and roster rows on the remote boxes, and whether the Discord body is the only one holding a bot token. Use when the user says "check all sessions", "list all sessions", "is white/black online", "who is where", "verify the links", "after reboot is everyone back". Part of the /herdr-link package.
---

# /herdr-link-check — see everything, change nothing

```bash
herdr-link check            # local sessions + saved machines + agents per machine
herdr-link check --json
```

The script covers sessions, machines and agents only. Autostart units, roster rows and the Discord-body
check are the by-hand commands below.

## By hand

```bash
herdr session list | rg -v stopped
herdr machine list && herdr machine status
for m in $(herdr machine list | cut -f2); do echo "== $m"; timeout 20 herdr --machine $m agent list \
  | python3 -c 'import sys,json;[print(a["pane_id"],a.get("name","-"),a["agent_status"]) for a in json.load(sys.stdin)["result"]["agents"]]'; done
```

Remote autostart (white, user nat):
```bash
ssh -o BatchMode=yes nat@white.follow-rankine.ts.net 'systemctl --user list-units "herdr-session@*" --no-pager; cut -f1,3 ~/.config/herdr/plugins/config/nsm.oracle-autostart/roster.tsv'
```

Black (system unit):
```bash
ssh -o BatchMode=yes phd-oracle@black.follow-rankine.ts.net 'uptime -s; systemctl show herdr-phd-oracle.service -p ActiveState -p ActiveEnterTimestamp'
```

Discord: one body per bot — compare token hashes, never print tokens:
```bash
ssh phd-oracle@black.follow-rankine.ts.net 'P=$(pgrep -u phd-oracle -x claude | head -1); tr "\0" "\n" < /proc/$P/environ | sed -n "s/^DISCORD_BOT_TOKEN=//p" | tr -d "\n" | sha256sum | cut -c1-12'
ps -axo pid,args | rg 'claude.*--channels' | rg -v rg     # which local bodies hold Discord
```

## Reading it

- A session with 0 agents is a leftover or a window; check before stopping.
- Pane ids change after a reboot or move — this list is the truth, notes are not.
- `e3b0c44298fc` as a token hash = the EMPTY string (direnv did not load over ssh) — read `/proc/<pid>/environ`.
- Peek without attaching: `herdr --machine <label> pane read <pane> --source recent-unwrapped --lines 40`.
