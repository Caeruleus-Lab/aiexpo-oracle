---
name: herdr-ask
description: "⌘J in herdr: a popup input box that types one line into every agent pane of the current tab (a broadcast), or ←/→ narrows it to one pane; the tab's layout is drawn so you see where it goes. Also works in a `herdr --remote` tab through herdr-ask-remote over ssh. Use when the user asks how ⌘J works, wants to set it up on a machine, or says 'send to all panes of this tab', 'herdr-ask'. Do NOT use for every body of one oracle (/herdr-soulcast, ⌘S), a whole session (/herdr-sessioncast) or a room by name (/herdr-roomcast)."
---

# /herdr-ask (⌘J)

Nat, 2026-10-29: *"yes it herdr-ask"*: ⌘J is the tab broadcast.

- ⌘J → WezTerm sends F11 → herdr `[[keys.command]] key = "f11"` popup → `herdr-ask --layout`.
- The box draws the tab (`herdr-layout --mini`). Target starts at **all**: Enter sends to every agent pane
  (shells skipped, a refusing pane reported as `:FAIL`, the others still get it). → / ← picks one pane. Esc quits.
- Remote tab (`herdr --remote <target> --session <s>`): herdr runs no popups for remote clients, so WezTerm opens a
  12-row split running `ssh -t <target> ~/.local/bin/herdr-ask-remote <s>`, which finds that session's focused pane
  and hands over to `herdr-ask --layout`.
- Other modes: `herdr-ask` prints what you typed; `--to-focused` sends to the focused pane only;
  `herdr-ask <cmd...>` runs `<cmd> "<text>"`.

Setup (WezTerm + config.toml snippets) and the rest of the family: `docs/broadcast.md` in
Soul-Brews-Studio/herdr-orca-oracle. Tools: `~/.local/bin/herdr-ask`, `herdr-ask-remote`, `herdr-layout`.
