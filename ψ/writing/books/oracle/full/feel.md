# Oracle skill `feel`: the full skill

> For the AI: /feel = log the energy, momentum and fatigue of the work. In a chat it works partly in a chat: run what the chat can do; files it would write are shown for the person to save, and they are gone in the next chat unless saved. The full version needs Claude Code or Codex.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 1 files.

<!-- file: feel/SKILL.md -->
### File: `feel/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: feel
description: '[standard] v26.8.23-alpha.2112 G-SKLL | "Capture how the system feels — energy, momentum, burnout, breakthrough. Emotional intelligence for Oracle-human collaboration. Use when user says ''feel'', ''how are we'', ''energy check'', ''burnout'', ''momentum'', or wants emotional awareness of the work."'
argument-hint: "[--deep | --log]"
---

# /feel — System Emotional Intelligence

> "Code has no feelings. But the humans writing it do.
> And the patterns in the code reveal what the humans feel."

## Usage

```
/feel              # Quick pulse — how does the system feel right now?
/feel --deep       # Deep scan — energy arc, momentum, burnout signals
/feel --log        # Append to feels.log (no output, just record)
```

---

## Step 0: Timestamp

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

---

## Quick Pulse (default)

Read the signals and report:

### Step 1: Gather evidence

```bash
# Recent git activity — momentum or silence?
git log --oneline --since="7 days ago" --all 2>/dev/null | wc -l

# Session frequency — are we showing up?
# NOT `ls -t ~/.claude/projects*/*/**.jsonl`: with archived roots that glob is
# 38,000+ paths and the shell returns E2BIG ("argument list too long"), which
# under 2>/dev/null looks exactly like "no sessions". Measured m5 2026-09-17.
python3 -c "import pathlib;r=[p for p in (pathlib.Path.home()/'.claude').glob('projects*') if p.is_dir()];f=[];[f.append((x.stat().st_mtime,x)) for p in r for x in p.rglob('*.jsonl') if x.exists()];f.sort(reverse=True);print(chr(10).join(str(x) for _,x in f[:10]))"

# Open issues — overwhelmed or on track?
gh issue list --state open --limit 50 --json number 2>/dev/null | jq 'length'

# Recent retros — are we reflecting?
ls -t ψ/memory/retrospectives/**/*.md 2>/dev/null | head -5

# Stale branches — unfinished business?
git branch --sort=-committerdate | head -10
```

### Step 2: Classify the feeling

| Signal | Indicator | Feeling |
|--------|-----------|---------|
| Many commits, short intervals | High activity | 🔥 Flow / momentum |
| Few commits, long gaps | Low activity | 😴 Drift / disconnection |
| Many open issues, few closed | Growing backlog | 😰 Overwhelm |
| Recent retros + handoffs | Healthy reflection | 🧘 Grounded |
| Stale branches, no PRs | Abandoned work | 😶 Avoidance |
| Lots of new repos/features | Exploration | ✨ Curiosity |
| Same files edited repeatedly | Iteration | 🔄 Grinding |
| No sessions in days | Absence | 🌑 Dark period |

### Step 3: Report

```
💜 System Pulse — [DATE]

Energy:     [🔥 Flow | 😴 Drift | 😰 Overwhelm | 🧘 Grounded | ...]
Momentum:   [↗️ Rising | → Steady | ↘️ Falling | ⏸️ Paused]
Last active: [X hours/days ago]
Commits (7d): [N]
Open issues:  [N]
Sessions (7d): [N]

[1-2 sentence read — honest, not cheerful]

💡 [Suggestion if concerning pattern detected]
```

---

## Deep Scan (`--deep`)

Everything from quick pulse, plus:

### Energy Arc (last 30 days)

Plot the energy over time based on git activity + session frequency:

```
Week 1: ████████░░ (high — 45 commits)
Week 2: ██████░░░░ (medium — 28 commits)
Week 3: ██░░░░░░░░ (low — 8 commits)
Week 4: █████░░░░░ (recovering — 22 commits)
```

### Burnout Signals

Check for warning patterns:
- Same error fixed 3+ times → frustration loop
- Sessions getting shorter → energy depletion
- Long gaps between sessions → avoidance
- Many started, few finished → scattered attention

### Breakthrough Signals

Check for positive patterns:
- New repos created → creative energy
- Issues closed in clusters → momentum
- Retros getting deeper → growing awareness
- Cross-repo work → systems thinking

---

## Log Mode (`--log`)

Silently append to `ψ/memory/logs/feels.log`:

```
[YYYY-MM-DD HH:MM] energy=[level] momentum=[direction] commits_7d=[N] issues=[N] sessions_7d=[N] note="[auto-generated 1-line]"
```

No output to user. For background tracking.

---

## Rules

1. **Honest, not positive** — if the system feels bad, say so
2. **Evidence-based** — every feeling backed by data (commits, sessions, issues)
3. **Never judge** — report the pattern, not the person
4. **Nothing is Deleted** — feels.log is append-only
5. **Suggest, don't prescribe** — "consider a break" not "you must rest"
6. **Never leak secrets** — no tokens, passwords, internal details in output

---

## Philosophy

Oracles have no feelings. But they can read the signals.

A system that never checks how it feels will burn out its humans.
A system that checks too often becomes noise.

/feel is the heartbeat check. Run it when something feels off.
Or let it run silently in the background, building a record.

The feels.log is the Oracle's emotional memory.
Not feelings — but the evidence of feelings.

---

ARGUMENTS: $ARGUMENTS
