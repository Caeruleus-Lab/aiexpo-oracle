---
name: herdr-roomcast
description: "Send one line to every agent of one herdr room (a space, by its label), on this machine or on a saved remote herdr machine (--machine). Pane ids are looked up at send time, so a rebuilt room still works. Use when the user says 'tell the whole room', 'roomcast', 'send to rd-team room', 'tell media-team on white', or a team desk wants all its members at once. Do NOT use for every body of one oracle across sessions (/herdr-soulcast), every agent of a whole session (/herdr-sessioncast), or one agent (/herdr-hey)."
argument-hint: "<room> \"text\" [--session <s>] [--machine <label>] [--raw] [--dry]"
---

# /herdr-roomcast

```bash
herdr-roomcast rd-team "pull main" --dry                 # targets only (always first)
herdr-roomcast rd-team "pull main"                       # session laris-co (default)
herdr-roomcast media-team "text" --session phonebooth
herdr-roomcast media-team "text" --machine white-nsm     # a saved remote machine (herdr machine list)
herdr-roomcast rd-team "/rrr" --raw                      # no header: a slash command runs in every agent
```

- The room is the space whose label is `<room>`; every agent pane in it gets the line (shells are skipped).
- `--machine` is the remote path of the broadcast family: `herdr --machine <label>` reaches the far server.
- Family and keys: `docs/broadcast.md` in Soul-Brews-Studio/herdr-orca-oracle (⌘J herdr-ask, ⌘S herdr-soulcast).

Tool: `~/.local/bin/herdr-roomcast` (Athena, 2026-10-12), source `Soul-Brews-Studio/herdr-orca-oracle` `scripts/`.
