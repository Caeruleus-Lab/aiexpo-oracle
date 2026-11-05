# Oracle skill `dig`: the full skill

> For the AI: /dig = mine past sessions: what was done, when. In a chat it needs Claude Code or Codex on the person's own machine (terminal, git, files on disk). In a chat, do NOT run or imitate it: explain what it does, and give the download link and install line below.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 3 files.

<!-- file: dig/SKILL.md -->
### File: `dig/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: dig
description: '[standard] v26.8.23-alpha.2112 G-SKLL | Mine Claude Code sessions — timeline, gaps, repo attribution, session history. Use when user says "dig", "sessions", "past sessions", "timeline", "what did I work on", or wants to see session history. Do NOT trigger for finding code/projects (use /trace), exploring repos (use /learn), or current session status (use /recap).'
argument-hint: "[N] | --all | --timeline | --deep"
---

# /dig - Session Goldminer v2

Mine Claude Code session data for timelines, gaps, and repo attribution. No query needed.

## Usage

```
/dig                    # Current repo, 10 most recent
/dig [N]                # Current repo, N most recent
/dig --all              # All repos, ALL sessions (auto-detect count)
/dig --all [N]          # All repos, N most recent
/dig --deep             # Deep scan — ALL .jsonl files (not just most-recent per project)
/dig --deep [N]         # Deep scan, N most recent
/dig --all --deep       # All repos, deep scan — full coverage
/dig --timeline         # Day-by-day grouped (current repo)
/dig --all --timeline   # Day-by-day grouped (all repos, ALL sessions)
```

### Deep Mode (#216)

Standard `/dig` deduplicates by session basename — only showing the most recent file per session. This misses historical sessions, subagent sessions, and worktree sessions.

`--deep` scans ALL `.jsonl` files across all project directories. Output includes extra fields:
- `toolCalls` — number of tool invocations in the session
- `fileSizeKB` — session file size in KB
- Coverage metadata: `"X of Y sessions"` showing how many were returned vs found

### Timezone (#214)

dig.py v2 auto-detects timezone instead of hardcoding GMT+7:
1. `MAW_DISPLAY_TZ` env var (e.g., `Asia/Bangkok`, `7`, `America/New_York`)
2. `TZ` env var
3. System timezone
4. Fallback: UTC

Output metadata includes detected timezone name and offset.

## Step 0: Timestamp

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
ENCODED_PWD=$(pwd | sed 's|^/|-|; s|[/.]|-|g')
PARENT_ENCODED=$(echo "$ENCODED_PWD" | sed 's/-wt-[^/]*$//')
export PROJECT_DIRS=""

# EVERY corpus root, not just the live one (#dig-corpus-2026-09-17).
# Archived roots are siblings named projects-<something>; see "Corpus roots" below.
# `find -maxdepth 1 -name`, NOT a bare glob. zsh aborts the whole command with
# "no matches found" when a pattern matches nothing, and its `(N)` nullglob
# qualifier is not parsed in every non-interactive shell — measured 2026-09-17,
# the old `"$base"-wt-*(N)` line errored outright and took the scan with it.
# (This is depth-1 inside ONE named directory, not a filesystem sweep — the
# fleet ban is on `find` rooted at `/`, `~`, or the ghq root.)
for ROOT in $(find "$HOME/.claude" -maxdepth 1 -type d -name 'projects*' 2>/dev/null); do
  for enc in "$ENCODED_PWD" "$PARENT_ENCODED"; do
    [ -d "$ROOT/$enc" ] && PROJECT_DIRS="$PROJECT_DIRS:$ROOT/$enc"
    for wt in $(find "$ROOT" -maxdepth 1 -type d -name "${enc}-wt-*" 2>/dev/null); do
      PROJECT_DIRS="$PROJECT_DIRS:$wt"
    done
  done
done
export PROJECT_DIRS="${PROJECT_DIRS#:}"
echo "corpus roots: $(find "$HOME/.claude" -maxdepth 1 -type d -name 'projects*' | tr '\n' ' ')"
```

Encodes `pwd` the same way Claude does (replace `/` and `.` with `-`, prepend `-`) to match the `.claude/projects/` directory naming (e.g. `github.com` → `github-com`). Detects parent project from worktree dirs (strips `-wt-*` suffix) and includes both parent and self worktrees. The `(N)` qualifier prevents zsh crashes when no worktrees exist.

**With `--all`** (all repos, EVERY corpus root):
```bash
export PROJECT_DIRS=$(ls -d "$HOME/.claude/"projects*/*/ | tr '\n' ':')
```

### Corpus roots — why the glob is `projects*`, not `projects`

`~/.claude/projects/` is the **live** root only. Claude Code (and manual archiving)
leaves older roots as siblings — `projects-archive/`, `projects-<date>/` — and they
hold most of the history. Measured on m5, 2026-09-17:

| root | project dirs | `.jsonl` |
|---|---|---|
| `projects` | 163 | 6,315 |
| `projects-1sep-tue2026` | 903 | 25,397 |
| `projects-archive` | 455 | 7,052 |
| | | **38,764** |

Globbing `projects/` alone reaches **16%** of the corpus and says nothing about the
rest — `/dig --all --deep` reported "1,257 sessions" while every session containing
the searched term sat in `projects-1sep-tue2026/`. A dig that silently covers a sixth
of the history is worse than one that refuses: it answers confidently.

**Always echo the roots that were scanned** so the coverage is on the record.

## Step 2: Extract Session Data

Run the dig script. Pass `0` for `--all` (no limit), or N if user specified a count, default 10:

```bash
python3 ~/.claude/skills/dig/scripts/dig.py [N] [--deep]
# N=10 (default), N=0 (scan all sessions), N=50 (50 most recent)
# --deep: scan ALL .jsonl files (not just most-recent per basename)
```

### Deep Mode Display

When `--deep` is used, add extra columns to the table:

```markdown
| # | Date | Session | Min | Repo | Msgs | Tools | Size | Focus |
```

And show coverage in the footer:

```markdown
**Coverage**: [returned]/[found] sessions | **Timezone**: [tz_name] (GMT+[offset])
```

## Step 3: Display Timeline

Read the JSON output and display as a table. Sessions are chronological (oldest first). Gap rows (`type: "gap"`) span the session column with `· · ·` prefix:

```markdown
## Session Timeline

| # | Date | Session | Min | Repo | Msgs | Focus |
|---|------|---------|-----|------|------|-------|
|   |      | · · · sleeping / offline | | | | |
| 1 | 02-21 | 08:40–09:08 | 28m | oracle-skills-cli | 5 | Wire /rrr to read pulse data |
|   |      | · · · 45m gap | | | | |
| 2 | 02-21 | 09:55–10:23 | 28m | homelab | 3 | oracle-pulse birth + CLI flag |
|   |      | · · · no session yet | | | | |

**Dirs scanned**: [list PROJECT_DIRS]
**Total sessions found**: [count]
```

Column rendering rules:
- **Gap rows**: `|   |      | · · · [label] | | | | |` — number + date empty, label in Session col
- **Date**: `MM-DD` short format (strip year)
- **Session**: `HH:MM–HH:MM` using `startGMT7` and `endGMT7` (strip date, keep time only)
- **Min**: `[durationMin]m` — ACTIVE time: idle gaps over 30 min are left out, so a session
  resumed across days shows its work, not the wall clock. `spanMin` is first→last; when it
  is far larger, the `Session` HH:MM–HH:MM range crosses days — say so (e.g. `09-22→09-26`).
- **Repo**: use `repoName` field from dig.py output (resolved via ghq)
- **Msgs**: `realHumanMessages` count

"Msgs" = real typed human messages (not tool approvals).

---

## With --timeline: Group by Date

When `--timeline` flag is present, group sessions by date instead of a flat table. Use `--all` to see all repos (recommended for timeline).

**Step 1**: Run dig.py with `0` for `--all` (scans all sessions), or user-specified count

**Step 2**: Group sessions by date from `startGMT7`. Render each day as:

```markdown
## Feb 22 (Sun) — [vibe label]

                  · · ·   sleeping / offline
08:48–09:11    23m   homelab        Update Fleet Runbook + Explore black.local
09:11–11:30   139m   homelab        Set Up KVM OpenClaw Node on black.local
09:37–12:51   194m   Nat-s-Agents   /recap → supergateway → CF ZT → arra-oracle-v3 dig
                  · · ·   45m gap
12:51–13:03    12m   Nat-s-Agents   Dig All + Design arra-oracle-v3 ← current
                  · · ·   no session yet

## Feb 21 (Sat) — Long day: Fleet + Brewing + Skills

06:19–08:38   139m   homelab        Moltworker Gateway + MBP Node
08:40           (bg)  openclaw       ClawHub Build Script (idle long)
09:23–16:08   405m   homelab        Debug MBP Node 401 — Gateway Token Auth
```

**Rendering rules**:
- **Day header**: `## MMM DD (Day) — [vibe label]` — infer vibe from session summaries (e.g. "Infrastructure Day", "Brewing + Skills")
- **Session rows**: `HH:MM–HH:MM  [N]m  REPO  Summary` — use `repoName` for repo, `summary` for focus
- **Gap rows**: `· · ·  [label]` between sessions when gap > 30 min
- **Sidechain**: prefix `(bg)` for sessions with `isSidechain: true`
- **Current**: append `← current` marker on the last session of the current day (today only)
- **Sort**: days newest-first, sessions within each day oldest-first (chronological)
- **Date format**: `startGMT7` time portion only (HH:MM), `endGMT7` time portion (HH:MM)
- **Repo width**: pad repo names to align columns

**Step 3**: Show summary footer:
```markdown
**Days**: [count] | **Sessions**: [count] | **Total time**: [sum of durationMin]m
```

---

## Trace Connection

After displaying the timeline, log the discovery to Oracle so it's searchable later:

```
arra_trace({
  query: "dig session [N]",
  project: "[repo-name]",
  foundFiles: [],
  foundCommits: [list of commit hashes from timeline],
  foundIssues: []
})
```

This connects `/dig` discoveries to `/trace` — "When did we first work on X?" becomes answerable.

---

ARGUMENTS: $ARGUMENTS

<!-- file: dig/DEEP.md -->
### File: `dig/DEEP.md`

# /dig — Deep Knowledge

Companion to SKILL.md. Teaches the Oracle (and future siblings) how /dig timeline works under the hood, when to reach for it, and where it breaks.

## Real Timeline Output

### Flat mode: `/dig --all 20`

```markdown
## Session Timeline

| # | Date | Session | Min | Repo | Msgs | Focus |
|---|------|---------|-----|------|------|-------|
|   |      | · · · sleeping / offline | | | | |
| 1 | 05-19 | 06:19–08:38 | 139m | homelab | 8 | Moltworker Gateway + MBP Node |
|   |      | · · · 45m gap | | | | |
| 2 | 05-19 | 09:23–16:08 | 405m | homelab | 22 | Debug MBP Node 401 — Gateway Token Auth |
|   |      | · · · sleeping / offline | | | | |
| 3 | 05-20 | 08:40–09:08 | 28m | oracle-skills-cli | 5 | Wire /rrr to read pulse data |
|   |      | · · · no session yet | | | | |

**Dirs scanned**: 3
**Total sessions found**: 3
```

### Grouped mode: `/dig --all --timeline`

```markdown
## May 20 (Tue) — Skills Day

                  · · ·   sleeping / offline
08:40–09:08    28m   oracle-skills-cli   Wire /rrr to read pulse data
09:55–10:23    28m   homelab             oracle-pulse birth + CLI flag
                  · · ·   no session yet

## May 19 (Mon) — Long Infrastructure Day

06:19–08:38   139m   homelab        Moltworker Gateway + MBP Node
08:40           (bg)  openclaw       ClawHub Build Script (idle long)
09:23–16:08   405m   homelab        Debug MBP Node 401 — Gateway Token Auth

**Days**: 2 | **Sessions**: 5 | **Total time**: 600m
```

### Deep mode: `/dig --deep --all`

Adds columns for tool calls, file size, and subagent identification:

```markdown
| # | Date | Session | Min | Repo | Msgs | Tools | Size | Focus |
|---|------|---------|-----|------|------|-------|------|-------|
| 1 | 05-19 | 06:19–08:38 | 139m | homelab | 8 | 47 | 312KB | Moltworker Gateway |
| 2 | 05-19 | 06:25–06:31 | 6m | homelab | 0 | 12 | 45KB | (subagent: Explore) |

**Coverage**: 14/14 sessions | **Timezone**: GMT+07:00
```

## Date/Time Extraction Logic

dig.py does NOT extract dates from filenames. The pipeline:

1. **Primary**: Parse `timestamp` field from each JSON line in the `.jsonl` session file. Track `first_ts` (earliest) and `last_ts` (latest).
2. **Format**: ISO 8601 with Z suffix (e.g., `2026-05-19T06:19:00Z`). Converted to local time via detected timezone offset.
3. **Duration**: `(last_ts - first_ts)` in minutes.
4. **Timezone detection priority**: `MAW_DISPLAY_TZ` env > `TZ` env > `date +%z` system call > UTC fallback.

There is no filename-based date extraction or mtime fallback — if a session has no `timestamp` fields, it's skipped entirely (`if not first_ts: continue`).

### Session identity

- **Session ID**: derived from the `.jsonl` filename (e.g., `a0a0531d-77ea-...jsonl` → `a0a0531d-77ea`).
- **Standard mode**: deduplicates by basename — keeps the most recently modified file when the same session ID appears in multiple project dirs.
- **Deep mode**: deduplicates by full path — shows every `.jsonl` file including subagent sessions in `<uuid>/subagents/`.

### Summary resolution

Cascading fallback: `sessions-index.json` summary → in-file `type: "summary"` entry → first human message text → `"No summary"`.

## When to Use /dig vs Alternatives

| Need | Tool | Why |
|------|------|-----|
| "What did I work on this week?" | `/dig --all --timeline` | Groups sessions by day, shows time spent per repo |
| "When did I first touch repo X?" | `/dig --all` then scan for repo | Flat list makes it easy to spot first appearance |
| "Find the code/commit where X was built" | `/trace --deep` | Searches git history, file content — /dig only shows session metadata |
| "What's happening right now?" | `/recap --now` or `/where-we-are` | Current session awareness, not historical |
| "Show me yesterday's standup data" | `/standup` | Pulls recent sessions + calendar, formatted for standup |
| "How many sessions hit repo X?" | `/dig --deep --all` | Deep mode shows coverage counts and subagent sessions |
| "Find a specific conversation" | `/dig --deep --all 50` | Then scan summaries for keywords — no text search, but summaries are searchable |

### /dig timeline vs /trace --deep

- **/dig** answers **when** — temporal questions about sessions, duration, gaps, patterns.
- **/trace** answers **where** — locating code, commits, files, projects across the codebase.

They complement each other: `/dig` finds the session, `/trace` finds the artifact. The `Trace Connection` section in SKILL.md bridges them — dig results get logged so `/trace` can answer "when did we first work on X?"

## Limits and Performance

### Scale

- **Session count**: no hard limit in deep mode (`--deep --all` with `count=0` scans everything). Practically, 200+ sessions per project dir is where you'll notice latency.
- **File parsing**: every `.jsonl` is fully line-scanned. A 500KB session file with 2000 lines takes ~50ms. A 5MB session (long Opus conversation) can take 500ms+.
- **Subagent explosion**: `--deep` scans `<uuid>/subagents/*.jsonl` — a single session with 10 subagents adds 10 entries. Heavy `team-agents` usage can produce 50+ subagent files per session.

### Known limits

- **No full-text search**: dig doesn't search message content. It reads summaries and first prompts only. For "find the conversation where I discussed X", you need to grep `.jsonl` files directly.
- **Gap detection is naive**: gaps > 30 min are shown. Overlapping sessions (e.g., background sidechain running alongside main session) can produce negative or zero gaps — these render correctly but look odd.
- **Repo name resolution depends on ghq**: if `ghq list -p` fails or isn't installed, repo names fall back to the last segment of the project dir path, which can be ambiguous.
- **Worktree dirs**: the Step 0 shell setup handles `-wt-*` suffixed dirs, but if worktrees are created with non-standard naming, they'll be missed.

## Enrichment Checklist (for future siblings)

When budding a new Oracle that needs /dig:
1. Verify `ghq` is installed (for repo name resolution)
2. Check timezone: `echo $MAW_DISPLAY_TZ` or `date +%z`
3. Test with `/dig 3` first (small, fast) before `/dig --deep --all`
4. If sessions seem missing, check `PROJECT_DIRS` — the Step 0 shell encoding must match Claude's internal project dir naming

<!-- file: dig/scripts/dig.py -->
### File: `dig/scripts/dig.py`

```python
#!/usr/bin/env python3
"""Session goldminer v3 — scan Claude Code .jsonl files for session timeline.

Fixes (ported from home-comming-oracle/dig-deep.py):
- --deep now scans subagent dirs: <project>/<uuid>/subagents/*.jsonl
- --subagents alias for explicit subagent inclusion
- Proper timezone detection (MAW_DISPLAY_TZ > TZ > system > UTC)
- Coverage metadata entry appended to output when --deep is used
- toolCalls, fileSizeKB, isSubagent fields added in --deep mode
"""
import json, os, glob, sys, subprocess, re
from datetime import datetime, timedelta
from pathlib import Path

project_dirs = [d for d in os.environ.get('PROJECT_DIRS', '').split(':') if d]

# Parse flags and positional args
_raw_args = sys.argv[1:]
deep = '--deep' in _raw_args
include_subagents = '--subagents' in _raw_args
skip_current = '--skip-current' in _raw_args
_positional = [a for a in _raw_args if not a.startswith('--')]
count = int(_positional[0]) if _positional else 10  # 0 = no limit

# The session running this script is always the newest file, because it is
# being written right now. /recap asks for "the last session" with `dig.py 1`,
# so without --skip-current it gets itself back: measured 2026-09-26 on a
# resumed session, "last session" was the current one, 4,709 min long.
# The host names its own session in the env (same keys and shape check as
# agents-relic's sessionIdFromEnv); with no id, the youngest file is treated
# as the current one (the same rule relic's `tail` uses).
current_sid = ''
for _k in ('CLAUDE_CODE_SESSION_ID', 'CODEX_THREAD_ID', 'CODEX_COMPANION_SESSION_ID'):
    _v = os.environ.get(_k, '').strip()
    if re.match(r'^[0-9a-fA-F][0-9a-fA-F-]{7,}$', _v):
        current_sid = _v
        break


# Turns in the user channel that the HOST wrote, not the human. Measured on the
# session that prompted this: the first "prompt" was a <local-command-caveat>,
# and skill bodies, task notifications and teammate messages were counted as
# human messages. Same shapes as agents-relic's isHarnessTurn (src/recap.ts).
HARNESS_PREFIXES = (
    '<local-command-caveat>', '<local-command-stdout>', 'Caveat: The messages below',
    '<command-name>', '<command-message>', '<command-args>',
    'Base directory for this skill:', '<system-reminder>',
    '<bash-stdout>', '<bash-stderr>', '<task-notification>',
    'Another Claude session sent a message:', '<teammate-message',
    'This session is being continued from a previous conversation',
    '[Request interrupted',
)


def is_harness_turn(obj, text):
    if obj.get('isMeta') or obj.get('isCompactSummary'):
        return True
    return text.startswith(HARNESS_PREFIXES)


def detect_tz():
    """Detect local timezone offset. Priority: MAW_DISPLAY_TZ > TZ > system > UTC."""
    for var in ('MAW_DISPLAY_TZ', 'TZ'):
        val = os.environ.get(var, '')
        if val:
            try:
                return timedelta(hours=int(val)), f"GMT+{val}"
            except ValueError:
                pass
    try:
        r = subprocess.run(['date', '+%z'], capture_output=True, text=True, timeout=3)
        offset_str = r.stdout.strip()
        if offset_str and len(offset_str) >= 5:
            sign = 1 if offset_str[0] == '+' else -1
            hours = int(offset_str[1:3])
            mins = int(offset_str[3:5])
            total = sign * (hours * 60 + mins)
            label = f"GMT{offset_str[0]}{hours:02d}:{mins:02d}"
            return timedelta(minutes=total), label
    except:
        pass
    return timedelta(hours=0), "UTC"


tz_offset, tz_name = detect_tz()


def build_repo_map():
    # `ghq list -p` maps encoded project-dir names → real repo names, but it can
    # take several seconds on machines with a large ghq root — and it runs on
    # every dig/recap/rrr invocation. DIG_SKIP_REPO_MAP=1 skips the subprocess
    # entirely: repo names then fall back to get_repo_name()'s own parsing. The
    # e2e test sets it so it stays hermetic (no ghq dependency) and fast.
    if os.environ.get('DIG_SKIP_REPO_MAP', '').lower() in ('1', 'true', 'yes', 'on'):
        return {}
    mapping = {}
    try:
        r = subprocess.run(['ghq', 'list', '-p'], capture_output=True, text=True, timeout=5)
        for path in r.stdout.strip().split('\n'):
            if path:
                mapping[path.replace('/', '-').replace('.', '-')] = path.split('/')[-1]
    except:
        pass
    return mapping


def get_repo_name(project_dir, repo_map):
    base = os.path.basename(project_dir.rstrip('/'))
    clean = re.sub(r'-(wt|agents)-.*$', '', base)   # strip -wt-1, -wt-herdr-…, -agents-1-gpu
    return repo_map.get(clean) or clean.split('-')[-1] or clean


repo_map = build_repo_map()

# ── Collect .jsonl files ──────────────────────────────────────────────────────
all_files = []   # list of (filepath, project_dir, is_subagent)
total_found = 0

skipped_unreadable = 0  # dangling symlinks / files pruned mid-scan
for d in project_dirs:
    # Top-level sessions (always included)
    for f in glob.glob(os.path.join(d, '*.jsonl')):
        all_files.append((f, d, False))
        total_found += 1

    # Deep scan: subagent sessions inside <uuid>/subagents/
    if deep or include_subagents:
        for uuid_dir in glob.glob(os.path.join(d, '*')):
            if not os.path.isdir(uuid_dir):
                continue
            sub_dir = os.path.join(uuid_dir, 'subagents')
            if os.path.isdir(sub_dir):
                # Direct subagents, PLUS the workflow tier one level deeper.
                # Until 2026-09-18 this globbed only sub_dir, so every agent
                # spawned inside a workflow run was invisible: measured on one
                # project dir, 13 transcripts found vs 118 actually present —
                # 105 workflow agents missing, i.e. the whole of any fan-out.
                candidates = list(glob.glob(os.path.join(sub_dir, '*.jsonl')))
                for wf_dir in glob.glob(os.path.join(sub_dir, 'workflows', 'wf_*')):
                    for wf_f in glob.glob(os.path.join(wf_dir, '*.jsonl')):
                        # journal.jsonl is run bookkeeping, not a transcript
                        if os.path.basename(wf_f) != 'journal.jsonl':
                            candidates.append(wf_f)
                for f in candidates:
                    # getsize() follows symlinks and raises on a dangling one.
                    # Archived roots are full of links into the LIVE root, and
                    # those break as soon as a session is pruned there — one
                    # dangling link used to abort the entire scan and emit zero
                    # sessions, which reads as "no history" (measured 2026-09-17:
                    # 38,764 files, 1 bad link, 0 output).
                    try:
                        if os.path.getsize(f) > 0:
                            all_files.append((f, d, True))
                            total_found += 1
                    except OSError:
                        skipped_unreadable += 1
                        continue

# Prune anything that cannot be stat'd BEFORE any getmtime/getsize below.
# Archived roots link into the live root; those links break when a session is
# pruned there. Doing this once here covers the dedup (getmtime), the sort
# (getmtime) and fileSizeKB — each of which used to abort the whole run on a
# single bad path, emitting zero sessions, which reads as "no history".
_kept = []
for _entry in all_files:
    if os.path.exists(_entry[0]):
        _kept.append(_entry)
    else:
        skipped_unreadable += 1
all_files = _kept

# Deduplicate
if deep or include_subagents:
    # Deep mode: deduplicate by full path
    seen_paths = {}
    for fp, d, is_sub in all_files:
        if fp not in seen_paths:
            seen_paths[fp] = (fp, d, is_sub)
    all_unique = list(seen_paths.values())
else:
    # Standard mode: deduplicate by basename (original behaviour)
    seen_base = {}
    for f, d, is_sub in all_files:
        base = os.path.basename(f)
        if base not in seen_base or os.path.getmtime(f) > os.path.getmtime(seen_base[base][0]):
            seen_base[base] = (f, d, is_sub)
    all_unique = list(seen_base.values())

files_sorted = sorted(all_unique, key=lambda x: os.path.getmtime(x[0]), reverse=True)
if skip_current and files_sorted:
    if current_sid:
        # the transcript itself, plus its subagents under <sid>/subagents/
        files_sorted = [e for e in files_sorted
                        if os.path.basename(e[0]) != current_sid + '.jsonl'
                        and f'/{current_sid}/' not in e[0]]
    else:
        files_sorted = files_sorted[1:]
if count > 0:
    files_sorted = files_sorted[:count]

# ── Load sessions-index from all dirs ─────────────────────────────────────────
index_map = {}
for d in project_dirs:
    try:
        with open(os.path.join(d, 'sessions-index.json')) as f:
            for e in json.load(f).get('entries', []):
                index_map[e['sessionId']] = e
    except:
        pass


def to_local(iso):
    try:
        dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return (dt + tz_offset).strftime('%Y-%m-%d %H:%M')
    except:
        return iso


GAP_THRESHOLD = 30  # minutes — a silence longer than this is not session time


def active_minutes(stamps):
    """Minutes with activity: sum the steps between consecutive events, skipping
    any step longer than GAP_THRESHOLD. First→last alone counts every night a
    session sat idle before being resumed — measured 2026-09-26: 9c77f5f5 read
    5,619 min (four days) as one span."""
    times = []
    for s in stamps:
        try:
            times.append(datetime.fromisoformat(s.replace('Z', '+00:00')))
        except:
            pass
    times.sort()
    total = 0.0
    for a, b in zip(times, times[1:]):
        step = (b - a).total_seconds()
        if step <= GAP_THRESHOLD * 60:
            total += step
    return int(total / 60)


# ── Parse sessions ─────────────────────────────────────────────────────────────
sessions = []
for fp, source_dir, is_subagent in files_sorted:
    sid = os.path.basename(fp).replace('.jsonl', '')
    stamps = []
    first_ts = last_ts = None
    branch = summary_text = None
    is_sidechain = False
    real_human = []
    assistant_count = 0
    tool_calls = 0

    try:
        with open(fp) as fh:
            for line in fh:
                try:
                    obj = json.loads(line)
                except:
                    continue
                ts = obj.get('timestamp')
                if ts:
                    stamps.append(ts)
                    if not first_ts or ts < first_ts:
                        first_ts = ts
                    if not last_ts or ts > last_ts:
                        last_ts = ts
                # Claude Code stamps gitBranch on EVERY record. Reading it only
                # from a type=='summary' record made this 'unknown' for every
                # modern session: sampled over the 120 newest transcripts across
                # both roots, summary records 0/120, gitBranch present 120/120.
                if not branch:
                    branch = obj.get('gitBranch') or None

                t = obj.get('type', '')
                if t == 'summary':
                    summary_text = obj.get('summary', '')
                    branch = obj.get('gitBranch', '') or branch
                    is_sidechain = obj.get('isSidechain', False)
                elif t == 'assistant':
                    assistant_count += 1
                    if deep or include_subagents:
                        msg = obj.get('message', {})
                        content = msg.get('content', [])
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and c.get('type') == 'tool_use':
                                    tool_calls += 1
                elif t == 'user':
                    msg = obj.get('message', {})
                    content = msg.get('content', [])
                    text = ''
                    if isinstance(content, list):
                        for c in content:
                            if isinstance(c, dict) and c.get('type') == 'text':
                                text = c.get('text', '').strip()
                                break
                    elif isinstance(content, str):
                        text = content.strip()
                    if text and len(text) > 5 and not is_harness_turn(obj, text):
                        real_human.append(text[:80])
    except:
        continue

    if not first_ts:
        continue

    span_min = 0
    if first_ts and last_ts:
        try:
            t1 = datetime.fromisoformat(first_ts.replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
            span_min = int((t2 - t1).total_seconds() / 60)
        except:
            pass

    idx = index_map.get(sid, {})
    final_summary = idx.get('summary') or summary_text or (real_human[0] if real_human else 'No summary')
    final_branch = branch or idx.get('gitBranch') or 'unknown'

    entry = {
        'sessionId': sid[:12],
        'repoName': get_repo_name(source_dir, repo_map),
        'startGMT7': to_local(first_ts),
        'endGMT7': to_local(last_ts),
        # durationMin is ACTIVE time (idle gaps > GAP_THRESHOLD removed), so
        # /dig's "Min" column and its "Total time" sum mean work, not wall clock.
        # spanMin keeps the old first→last value.
        'durationMin': active_minutes(stamps),
        'spanMin': span_min,
        'realHumanMessages': len(real_human),
        'assistantMessages': assistant_count,
        'firstPrompt': real_human[0] if real_human else None,
        'gitBranch': final_branch,
        'summary': final_summary[:80],
        'isSidechain': is_sidechain,
    }

    # Extra fields only in deep/subagents mode
    if deep or include_subagents:
        entry['toolCalls'] = tool_calls
        entry['fileSizeKB'] = os.path.getsize(fp) // 1024
        entry['isSubagent'] = is_subagent
        # Which of the THREE tiers, not a yes/no — and the run id, which is the
        # only thing that groups a fan-out's agents back together.
        wf_m = re.search(r'/subagents/workflows/(wf_[^/]+)/', fp)
        entry['tier'] = ('workflow_agent' if wf_m else
                         'subagent' if is_subagent else 'session')
        entry['workflowRunId'] = wf_m.group(1) if wf_m else None

    sessions.append(entry)

sessions.sort(key=lambda s: s['startGMT7'])


def parse_local(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M')
    except:
        return None


with_gaps = []
for i, s in enumerate(sessions):
    if i == 0:
        with_gaps.append({"type": "gap", "label": "sleeping / offline"})
    else:
        prev_end = parse_local(sessions[i - 1]['endGMT7'])
        curr_start = parse_local(s['startGMT7'])
        if prev_end and curr_start:
            gap_min = int((curr_start - prev_end).total_seconds() / 60)
            if gap_min > GAP_THRESHOLD:
                with_gaps.append({"type": "gap", "gapMin": gap_min, "label": f"{gap_min}m gap"})
    with_gaps.append(s)
with_gaps.append({"type": "gap", "label": "no session yet"})

# Append coverage metadata when in deep/subagents mode (as a trailing sentinel entry)
_tier_counts = {}
for _s in sessions:
    _t = _s.get('tier', 'session')
    _tier_counts[_t] = _tier_counts.get(_t, 0) + 1

if deep or include_subagents:
    with_gaps.append({
        "type": "coverage",
        "totalFound": total_found,
        "skippedUnreadable": skipped_unreadable,
        "corpusRoots": sorted({os.path.dirname(d.rstrip('/')) for d in project_dirs}),
        "returned": len(sessions),
        "deep": deep,
        "includeSubagents": include_subagents,
        "timezone": tz_name,
        "projectDirs": len(project_dirs),
        "tiers": _tier_counts,
    })

print(json.dumps(with_gaps, indent=2))
```
