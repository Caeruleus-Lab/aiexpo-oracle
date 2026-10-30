---
name: ego-lite-install
description: Install ego(lite) from https://lite.ego.app/ and make the ego-browser skill visible to Claude Code, omx (Codex) and omp — check first, download + verify the DMG read-only, hand the GUI install and onboarding to the human, then link the skill for every agent and prove it with ego-browser --version. Use when the user says "install ego", "install ego-browser", "set up ego lite", "ego-browser not found", "/ego-browser missing in codex/omp", or wants an agent to have its own browser. Do NOT use to drive the browser for a task (that is the ego-browser skill itself) or to upgrade a working install (run `ego-browser upgrade`, with the user's approval).
---

# ego-lite-install: lite.ego.app → a browser your agent can drive

Guide with screenshots, captured 2026-10-30: `ψ/writing/books/2026-10-30_ego-lite-guide/README.md` (Thai, plus `README.en.md`).

## Where this skill lives (repo-local, not global)

It lives in this repo only. Each agent finds it when started inside the repo:

| Path in the repo | Read by |
|---|---|
| `.claude/skills/ego-lite-install/` (the real files) | Claude Code, omp |
| `.agents/skills/ego-lite-install` → symlink to the above | Codex / omx, omp |
| `.codex/skills/ego-lite-install` → symlink to the above | Codex / omx (older path) |

The steps are shell scripts beside this file. From the repo root run `.claude/skills/ego-lite-install/scripts/<name>.sh`
(`<skill-dir>` below means that folder).

## Step 1: check (read-only, always first)

```bash
bash <skill-dir>/scripts/check.sh
```

Prints the app version, the `ego-browser` CLI version, whether `ego-browser/SKILL.md` is in
`~/.claude/skills`, `~/.agents/skills` and `~/.codex/skills`, which agents exist, and a VERDICT line.
`VERDICT: ready` means stop here and tell the user to type `/ego-browser <task>`.

## Step 2: download and verify (only if the app is missing)

```bash
bash <skill-dir>/scripts/fetch-verify.sh            # → ~/Downloads/ego-lite-<date>/egolite.dmg
```

- Apple Silicon only (`https://cdn.ego.app/setup/macos/arm64/egolite.dmg`, verified 2026-10-30). On Intel or
  Windows, the script prints the download page instead. Do not guess another URL.
- It mounts the image **read-only**, prints the version, `codesign` and `spctl`, and ends with
  `VERIFIED` only if Gatekeeper says `accepted` and the team is `JGQLC6YQYJ` (CITRO LABS). Anything else means
  stop and show the user the output.
- It never runs the app from the image. Long download (~143 MB): in herdr, run it in a pane (`/herdr-pane-run`).

## Step 3: install and onboard (the human does this)

The installer is a GUI step that also asks for the macOS keychain password. Never type a password for the user.

```bash
open ~/Downloads/ego-lite-<date>/egolite.dmg
```

Tell the user, in order:
1. Quit ego(lite) first if it is running (the installer says so).
2. Double-click the **ego lite** icon in the window that opens.
3. Open ego(lite) and finish onboarding: let it scan for agents, choose whether to import Chrome
   data, and enter the keychain password each time macOS asks (it can ask more than once).
4. If Claude Code / Codex / omp was open during onboarding, restart it so the skill list reloads.

Wait for the user to say done.

## Step 4: link the skill for every agent

```bash
bash <skill-dir>/scripts/link-skill.sh
```

Onboarding writes `~/.local/share/ego/ego-skills` and links it into `~/.claude/skills` and `~/.agents/skills`.
This script adds only the **missing** links (also `~/.codex/skills` for older Codex/omx) and never overwrites.

| Agent | Reads skills from |
|---|---|
| Claude Code | `~/.claude/skills` |
| omx (oh-my-codex → Codex) | `~/.agents/skills`, `~/.codex/skills` |
| omp (oh-my-pi) | `~/.agents/skills`, `~/.claude/skills`, `~/.codex/skills` |

## Step 5: prove it

```bash
bash <skill-dir>/scripts/check.sh      # expect VERDICT: ready
ego-browser skill | tail -1            # expect: [ego-browser:skill] end of guide v…
```

Then the first task, in the agent's chat (permissions must allow running commands outside the sandbox:
Claude Code `Bypass permissions` / `claude --dangerously-skip-permissions`, Codex/omx Full access, omp no-approval):

```text
/ego-browser open https://example.com and tell me the page title
```

## Rules

- Check before you download; download only when the app is missing.
- Verify before you open: no `VERIFIED`, no install.
- The keychain password, the install double-click and every login belong to the human.
- Never `ego-browser upgrade` or overwrite an existing install without the user's yes.
- Redact `ref_code=` from any download URL you quote; the site adds one.
