---
name: herdr-twin
description: Resolve the local herdr session and list every machine running the same session, grouped like "nsm · 2 places · ● m5 ◐ 3 · ● white ✓ 6" (agent count + status per machine); toggle twin mode so the herdr sidebar shows only those machines (on the Soul-Brews build prefer ui.fold_machines_by_session / herdr machine fold-others --same-session, which folds instead of disabling); group every session the same way. Use when the user says "twin", "/herdr-twin", "herdr twin", "show my twin", "which machines run this session", "group by session", "show only matching sessions", "toggle remote machines", "hide the other machines", "show all machines again". Old names /herdr-match and /herdr-machines-match (aliases kept). Do NOT use to rename labels (use /herdr-machine-labels), to add/remove machines (herdr machine add/remove), or to list Claude conversation ids per repo (use /claude-twins).
argument-hint: "[on | off | toggle | groups | list | <session>]"
---

# /herdr-twin — this session, every place it runs

Calling `/herdr-twin` with no argument = **resolve + list, no change**:

```text
$ herdr-twin
  nsm                          2 places
    ● m5           ◐  3   local
    ● white        ✓  6   white · nsm
  twin mode: herdr-twin on · back: herdr-twin off · every session: herdr-twin groups
```

| command | does |
|---|---|
| `herdr-twin` | local session = `$HERDR_SESSION` (else the name in `$HERDR_SOCKET_PATH`, else `default`); every saved machine on that session, with its agents |
| `herdr-twin groups` | every session (running here + every saved machine), one block per session name |
| `herdr-twin on` | twin view: `herdr machine fold-others --same-session` — folds the other machines **in this session's windows only**, nothing disconnects (Soul-Brews build). Upstream herdr (white) falls back to `machine disable`, which hides them in every window — avoid on m5 |
| `herdr-twin off` | unfold every machine (fold build) / enable every machine (upstream fallback) |
| `herdr-twin toggle` | on ⇄ off |
| `herdr-twin list` | saved machines and state |
| `… --session nsm` / `herdr-twin nsm` | name the session instead of resolving it |

Icons: `◐` some agent working · `!` some blocked · `✓` all ready (idle/done) · `○` hidden (a disabled machine
cannot be queried: "machine … is disabled"). The number is the agent count from `herdr agent list` (local) and
`herdr --machine <id> agent list` (remote).

In nonsense-matters-oracle: `just twin` · `just twin groups|on|off|toggle|list` (script vendored at
`tools/herdr-twin`). Global: `~/.local/bin/herdr-twin`.

Nat, 2026-10-10: *"toggle remote machine name match local session name"* → *"resolve current session id and
list all remote match session id like this we can group"* (a mock: `nsm · 2 places · m5 ◐ 2 · white ✓ 6`).

## Fold instead of hide (Soul-Brews build, 2026-10-10)

On m5's herdr (fork `soul-brews`, herdr-orca-oracle #10) the sidebar does this by itself:
`[ui] fold_machines_by_session = true` in `~/.config/herdr/config.toml` (ON on m5 since 10:04).
On attach, each window opens Local + the saved machines whose session equals its own, and folds
the rest. An `nsm` window: `▾ Local`, `▸ black`, `▸ white-laris-co`, `▾ nsm · white`.

| want | prefer | why |
|---|---|---|
| sidebar shows only this session's twins | the config (already on) or `herdr machine fold-others --same-session` | per session, per window; nothing disconnects; folded machines stay queryable |
| really drop the others from every window | `herdr-twin on` (disable) | one list per computer: hides them in every session's window |
| text view with agent counts | `herdr-twin` / `groups` | unchanged |

Check a session's folds: `herdr --session nsm machine folds`. Manual folds last until the next attach.
Upstream herdr (and white, unless it gets our build) has no fold command: there, `herdr-twin on` is
still the only switch.

## Rules
- Disable (twin mode) is safe: profile kept, remote herdr server, sessions and agents keep running; only this
  computer's herdr clients disconnect. One saved-machine list per computer — twin mode in an `nsm` window hides
  `white · laris-co` in a `laris-co` window too.
- Upstream herdr has no grouped node and no auto-expand (docs "Connecting machines": a machine profile targets one
  remote session). Our build adds the auto-expand per session (above), still no grouped node: this skill
  stays the text view.
- Pairs with `/herdr-machine-labels` (`<host> · <session>`) and `/claude-twins` (conversation ids per repo).


2026-10-10 11:0x: herdr-orca-oracle (for Nat) — my `herdr-twin on` at 10:55 disabled black + white · laris-co in every m5 window. Fixed the same hour: on/off/toggle fold per window when `herdr machine --help` lists `fold-others`.
