---
name: herdr-machine-labels
description: Name every saved herdr machine "<host> · <session>" (machine first) so the sidebar reads the same session on two machines as a pair — Local (nsm on m5) next to "white · nsm" — and explain what herdr's machine sidebar can and cannot do (expand per machine, prefix+w across machines, no grouping by session name). Use when the user says "rename the machine label", "white first", "make the sidebar match", "same session on both machines", "expand white", or sees labels like white-nsm. Do NOT use to add or remove machines (herdr machine add/remove) or to list sessions on both machines (use /claude-twins).
argument-hint: "[--go]"
---

# /herdr-machine-labels — machine first, session second

```bash
herdr-machine-labels          # dry run: what each saved machine would be called
herdr-machine-labels --go     # rename (label only — nothing reconnects)
herdr machine list            # id · label · ssh target · session · state
```

Rule (Nat, 2026-10-10: "white first"): label = `<host> · <session>`; a machine on the `default` session is
just `<host>`. Host = the ssh target without `user@` and without the domain
(`nat@white.follow-rankine.ts.net` → `white`).

First run 2026-10-10: `white-nsm` → `white · nsm`, `white-laris-co` → `white · laris-co` (black · phd left for Nat).

## What the machine sidebar does (herdr 0.9.3, docs "Connecting machines")

| want | herdr | how |
|---|---|---|
| see m5's nsm and white's nsm in one window | yes | Local = the session herdr was opened with (`herdr --session nsm`); white = a saved machine |
| expand white's spaces | yes, per machine, in the client | click the `▸` beside the machine row — no CLI for it; it does not switch you away |
| jump between machines by keyboard | yes | `prefix+w`, Up/Down (reaches spaces under collapsed rows), Enter |
| agent list across machines | yes | each row carries a `machine` token when >1 machine is connected |
| one node for "nsm" on both machines / auto-expand when names match | **no** | "A machine profile targets one remote session; it does not combine every session on the host." — a herdr feature request (public: ask Nat first) |

## Rules
- Labels only. Never `machine remove`/`disable` to tidy names — that disconnects the machine.
- Read ids from `herdr machine list`; never derive them from labels.
- An agent cannot click the sidebar arrow: tell the human, or use `prefix+w`.
- Script: `~/.local/bin/herdr-machine-labels`.

## Show only the matching session
See `/herdr-twin` (`herdr-twin`, `herdr-twin all`) — hide machines whose session differs from the local one.
