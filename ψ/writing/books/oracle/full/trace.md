# Oracle skill `trace`: the full skill

> For the AI: /trace = find where something was done before. In a chat it works partly in a chat: run what the chat can do; files it would write are shown for the person to save, and they are gone in the next chat unless saved. The full version needs Claude Code or Codex.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 2 files.

<!-- file: trace/SKILL.md -->
### File: `trace/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: trace
description: '[standard] v26.8.23-alpha.2112 G-SKLL | Find projects, code, and knowledge across git history, repos, docs, and Oracle. Use when user asks "trace", "find project", "where is [project]", "search history", or needs to locate something across the codebase. Supports --oracle (fast), --smart (default), --deep (wave execution), --deep --dig (combo). Do NOT trigger for session mining or "past sessions" (use /dig), or codebase exploration "learn repo" (use /learn).'
argument-hint: "<query> [--oracle | --smart | --deep] [--dig]"
---

# /trace - Unified Discovery System

Find + Measure + Log + Distill

## Usage

```
/trace [query]                    # Current repo (default --smart)
/trace [query] --oracle           # Oracle only (fastest)
/trace [query] --deep             # Wave execution (thorough)
/trace [query] --deep --dig       # Combo: trace deep + dig session mining (parallel)
/trace [query] --repo [path]      # Search specific local repo
/trace [query] --repo [url]       # Clone to ghq, then search
```

> `/dig` alone mines sessions. `--dig` flag on `/trace` runs both together.

## Directory Structure

```
ψ/memory/traces/
└── YYYY-MM-DD/              # Date folder
    └── HHMM_[query-slug].md # Time-prefixed trace log
```

**Trace logs are committed** - they become Oracle memory for future searches.

---

## Step 0: Timestamp + Calculate Paths

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
ROOT="$(pwd)"
TODAY=$(date +%Y-%m-%d)
TIME=$(date +%H%M)
```

---

## Step 1: Detect Target Repo

### Default: Current repo
```bash
TARGET_REPO="$ROOT"
TARGET_NAME="$(basename $ROOT)"
```

### With --repo [path]: Local path
```bash
TARGET_REPO="[path]"
TARGET_NAME="$(basename [path])"
```

### With --repo [url]: Clone to ghq first
```bash
URL="[url]"
ghq get -u "$URL"
GHQ_ROOT=$(ghq root)
OWNER=$(echo "$URL" | sed -E 's|.*github.com/([^/]+)/.*|\1|')
REPO=$(echo "$URL" | sed -E 's|.*/([^/]+)(\.git)?$|\1|')
TARGET_REPO="$GHQ_ROOT/github.com/$OWNER/$REPO"
TARGET_NAME="$OWNER/$REPO"
echo "✓ Cloned to ghq: $TARGET_REPO"
```

**Note**: `/trace` only clones to ghq. Use `/learn` to create docs in ψ/learn/.

---

## Step 2: Create Trace Log Directory

```bash
mkdir -p "$ROOT/ψ/memory/traces/$TODAY"
TRACE_FILE="$ROOT/ψ/memory/traces/$TODAY/${TIME}_[query-slug].md"
```

---

## Mode 1: --oracle (Oracle Only)

**Fastest. Just Oracle MCP, no subagents.**

```
arra_search("[query]", limit=15)
```

Display results and done. Even if empty.

---

## Mode 2: --smart (Default)

**Oracle first → auto-escalate if results < 3**

**Step 1**: Query Oracle first
```
arra_search("[query]", limit=10)
```

**Step 2**: Check result count
- If Oracle results >= 3 → Display and done
- If Oracle results < 3 → Auto-escalate to --deep mode

---

## Mode 3: --deep (Wave Execution + Session Mining)

**Two waves of parallel search + dig session mining. Each wave has fresh context (no rot).**
`--deep --dig` is now the same as `--deep` (dig is always included).

### Wave 1 — Fast surface search + session mining (run in parallel)

**Agent A: Current/Target Repo Files**
```
You are searching for: [query]
TARGET REPO: [TARGET_REPO]

Search for:
- Files matching query (names, paths)
- Code/docs containing query
- Config files mentioning query

Return findings as text. Main agent compiles.
```

**Agent B: Oracle Memory**
```
You are searching for: [query]
PSI DIR: [ROOT]/ψ/

Search ψ/memory/ for:
- Learnings mentioning query
- Retrospectives mentioning query
- Previous trace logs for same query

Return findings as text. Main agent compiles.
```

**Agent F: Session History (dig)**
```
You are mining session history for: [query]

Run the dig script to get all sessions:
ENCODED_PWD=$(pwd | sed 's|^/|-|; s|[/.]|-|g')
PROJECT_BASE=$(ls -d "$HOME/.claude/projects/${ENCODED_PWD}" 2>/dev/null | head -1)
export PROJECT_DIRS="$PROJECT_BASE"

PARENT_ENCODED=$(echo "$ENCODED_PWD" | sed 's/-wt-[^/]*$//')
if [ "$PARENT_ENCODED" != "$ENCODED_PWD" ]; then
  PARENT_BASE=$(ls -d "$HOME/.claude/projects/${PARENT_ENCODED}" 2>/dev/null | head -1)
  [ -n "$PARENT_BASE" ] && export PROJECT_DIRS="$PROJECT_DIRS:$PARENT_BASE"
fi

for base in "$PROJECT_BASE" "$PARENT_BASE"; do
  [ -z "$base" ] && continue
  for wt in "$base"-wt-*(N); do
    [ -d "$wt" ] && export PROJECT_DIRS="$PROJECT_DIRS:$wt"
  done
done

python3 ~/.claude/skills/dig/scripts/dig.py 0 --deep

Then search the session data for mentions of: [query]
Look for:
- Sessions where this topic was worked on
- Timeline of when it was touched
- Which repos it appeared in
- How much time was spent

Return findings as text. Max 500 words.
```

After Wave 1: check if answer is sufficient.
- Sufficient (clear answer found) → skip Wave 2, go to Step 3
- Insufficient (< 3 results or answer unclear) → run Wave 2

### Wave 2 — Deep search (run in parallel, only if Wave 1 insufficient)

**Agent C: Git History**
```
You are searching for: [query]
TARGET REPO: [TARGET_REPO]

Search git history:
- Commits mentioning query
- Files created/deleted matching query
- Branch names matching query
Run: git log --all --oneline --grep="[query]"

Return findings as text. Main agent compiles.
```

**Agent D: Cross-Repo (ghq + ~/Code)**
```
You are searching for: [query]

Search other repos:
- find $(ghq root) -maxdepth 3 -name "*[query]*" 2>/dev/null | head -20
- grep -r "[query]" ~/Code --include="*.md" -l 2>/dev/null | head -10

Return findings as text. Main agent compiles.
```

**Agent E: GitHub Issues/PRs**
```
You are searching for: [query]
TARGET REPO: [TARGET_REPO]

If repo has GitHub remote, run:
- gh issue list --search "[query]" --limit 10
- gh pr list --search "[query]" --limit 10

Return findings as text. Main agent compiles.
```

**After both waves**, main agent compiles all results → Step 3.

---

## Mode 4: --deep --dig (Alias)

**Same as `--deep`** — dig is now always included in `--deep` mode (Agent F in Wave 1).
This flag is kept for backward compatibility but has no additional effect.

The trace log includes a **Session History** section from the dig agent:

```markdown
## Session History (from /dig)
[Sessions where query appeared, timeline, time spent]
```

This goes between "Oracle Memory" and "Friction Analysis" in the trace log.

---

## Step 3: Calculate Friction Score (Volt-inspired)

After search completes, calculate `friction_score` using the v2 formula:

```
friction_score = S + C_offset    (clamped to [0.0, 1.0])
```

**S — Source Score** (highest-tier source with relevant result):

| Where found | S | Meaning |
|-------------|---|---------|
| Oracle | 1.0 | Frictionless — well-indexed, visible |
| Repo files | 0.7 | Present but not indexed |
| Git history | 0.5 | Buried — existed, hard to surface |
| Cross-repo | 0.3 | Hidden — lives elsewhere |
| Not found | 0.0 | Invisible — doesn't exist yet |

**C_offset — Completeness** (from goal-backward check in Step 4):

| Confidence | C_offset |
|------------|----------|
| high | +0.00 |
| medium | −0.10 |
| low | −0.20 |

**Score table**:

| Situation | Score |
|-----------|-------|
| Oracle + high | 1.0 |
| Oracle + medium | 0.9 |
| Files + high | 0.7 |
| Files + medium | 0.6 |
| Git + high | 0.5 |
| Git + medium | 0.4 |
| Cross-repo + high | 0.3 |
| Not found | 0.0 |

**Rule**: S = highest-tier source that contained relevant result. Not found → 0.0 regardless of C_offset.

Also calculate `coverage`: how many of 5 dimensions were searched.
- `oracle`, `files`, `git`, `cross-repo`, `github` — list which were checked.

---

## Step 4: Goal-Backward Check (GSD verifier-inspired)

Before writing the trace log, ask:

> "Did this trace actually answer the original question?"

- **Yes** → confidence: high
- **Partial** (found related but not exact) → confidence: medium — note what's missing
- **No** → confidence: low — note what next step is needed

This prevents "found something → assume done". Omar stops here. Never crosses into deciding for jeera-p.

---

## Step 5: Write Trace Log

```markdown
---
query: "[query]"
target: "[TARGET_NAME]"
mode: [oracle|smart|deep]
timestamp: YYYY-MM-DD HH:MM
friction_score: [0.0–1.0]
coverage: [oracle, files, git, cross-repo, github]
confidence: [high|medium|low]
---

# Trace: [query]

**Target**: [TARGET_NAME]
**Mode**: [mode] | **Friction**: [score] | **Confidence**: [level]
**Time**: [timestamp]

## Oracle Results
[list results or "None"]

## Files Found
[list files or "None"]

## Git History
[list commits or "None"]

## GitHub Issues/PRs
[list or "None"]

## Cross-Repo Matches
[list or "None"]

## Oracle Memory
[list or "None"]

## Friction Analysis
**Score**: [0.0–1.0] — [interpretation]
**Coverage**: [dimensions searched]
**Goal check**: [Did this answer the question? What's missing?]

## Summary
[Key findings, next steps]
```

---

## Step 6: Log to Oracle MCP

```
arra_trace({
  query: "[query]",
  project: "[TARGET_NAME]",
  foundFiles: [...],
  foundCommits: [...],
  foundIssues: [...],
  friction_score: [0.0–1.0],
  confidence: "[high|medium|low]"
})
```

---

## Step 7: Confirm trace log path (announce-mode — absolute paths required)

# announce-mode → absolute path (no ψ/, no ~/, no $VAR, no ...).
# Use:  echo "marker: $RESOLVED_PATH"  — bash substitutes. See CONVENTIONS.md.

```bash
echo "🔍 Trace logged: $TRACE_FILE"
```

---

## Friction Score Reference

```
friction_score = S + C_offset    (clamped to [0.0, 1.0])

1.0 ████████████  Frictionless   — Oracle + high confidence
0.9 ███████████░  Near-perfect   — Oracle + medium confidence
0.7 ████████░░░░  Visible        — Files + high confidence
0.6 ███████░░░░░  Slightly buried — Files + medium confidence
0.5 ██████░░░░░░  Buried         — Git + high confidence
0.4 █████░░░░░░░  Buried-medium  — Git + medium confidence
0.3 ████░░░░░░░░  Hidden         — Cross-repo + high confidence
0.2 ███░░░░░░░░░  Very hidden    — Cross-repo + medium confidence
0.0 ░░░░░░░░░░░░  Invisible      — Not found anywhere
```

**Actionable zones**:
| Range | Action |
|-------|--------|
| 0.9–1.0 | No action needed |
| 0.6–0.89 | Consider `oracle_learn` indexing |
| 0.4–0.59 | Distill + index this session |
| 0.1–0.39 | Cross-repo consolidation needed |
| 0.0 | Create / document |

**Low score = signal**: this topic needs better indexing, documentation, or creation.
Omar surfaces this. jeera-p decides what to do about it.

---

## Philosophy

> Trace → Measure → Distill → Awakening

### The Seeking Signal

| User Action | Meaning | AI Response |
|-------------|---------|-------------|
| `/trace X` | First search | --smart (Oracle first) |
| `/trace X` again | Still seeking | Oracle knows |
| `/trace X --deep` | Really need it | Wave execution |
| Found! | **RESONANCE** | Log + score |

### Skill Separation

| Skill | Purpose | Writes to |
|-------|---------|-----------|
| `/trace` | Find + measure | ψ/memory/traces/ (logs) |
| `/trace --dig` | Find + measure + mine sessions | ψ/memory/traces/ (logs) |
| `/dig` | Mine sessions (standalone) | Screen only (read-only) |
| `/learn` | Study repos | ψ/learn/ (docs) |
| `/project` | Develop repos | ψ/incubate/ or active/ |

**Workflow**: `/trace` finds + measures → `/learn` studies → `/project` develops
**Combo**: `/trace --deep --dig` = find + mine in one shot

---

## Summary

| Mode | Speed | Scope | Waves |
|------|-------|-------|-------|
| `--oracle` | Fast | Oracle only | — |
| `--smart` | Medium | Oracle → maybe deep | Auto |
| `--deep` | Thorough | Wave 1 (+ dig) + Wave 2 if needed | 2 + dig |
| `--deep --dig` | (alias) | Same as --deep | — |

| Output field | Description |
|-------------|-------------|
| `friction_score` | 0.0–1.0 how hard to find |
| `coverage` | dimensions searched |
| `confidence` | did trace answer the question |

---

ARGUMENTS: $ARGUMENTS

<!-- file: trace/scripts/dig.py -->
### File: `trace/scripts/dig.py`

```python
#!/usr/bin/env python3
"""Session goldminer — scan Claude Code .jsonl files for session timeline."""
import json, os, glob, sys, subprocess, re, time
from datetime import datetime, timedelta, timezone

project_dirs = [d for d in os.environ.get('PROJECT_DIRS', '').split(':') if d]
count = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# Auto-detect local timezone offset (works on any machine)
local_offset = timedelta(seconds=-time.timezone if time.daylight == 0 else -time.altzone)
local_tz = timezone(local_offset)

def build_repo_map():
    mapping = {}
    try:
        r = subprocess.run(['ghq', 'list', '-p'], capture_output=True, text=True, timeout=5)
        for path in r.stdout.strip().split('\n'):
            if path:
                mapping[path.replace('/', '-')] = path.split('/')[-1]
    except: pass
    return mapping

def get_repo_name(project_dir, repo_map):
    base = os.path.basename(project_dir.rstrip('/'))
    clean = re.sub(r'-wt-\d+$', '', base)   # strip -wt-1, -wt-8 etc
    return repo_map.get(clean) or clean.split('-')[-1] or clean

repo_map = build_repo_map()

# Get .jsonl files across all project dirs, deduplicate by basename, take N most recent
seen = {}
for d in project_dirs:
    for f in glob.glob(os.path.join(d, '*.jsonl')):
        base = os.path.basename(f)
        if base not in seen or os.path.getmtime(f) > os.path.getmtime(seen[base][0]):
            seen[base] = (f, d)   # store (filepath, project_dir) tuple
all_files = [(fp, d) for fp, d in seen.values()]
files = sorted(all_files, key=lambda x: os.path.getmtime(x[0]), reverse=True)[:count]

# Load sessions-index from all dirs
index_map = {}
for d in project_dirs:
    try:
        with open(os.path.join(d, 'sessions-index.json')) as f:
            for e in json.load(f).get('entries', []):
                index_map[e['sessionId']] = e
    except: pass

sessions = []
for fp, source_dir in files:
    sid = os.path.basename(fp).replace('.jsonl', '')
    first_ts = last_ts = None
    branch = summary_text = None
    is_sidechain = False
    real_human = []
    assistant_count = 0

    with open(fp) as fh:
        for line in fh:
            try: obj = json.loads(line)
            except: continue
            ts = obj.get('timestamp')
            if ts:
                if not first_ts or ts < first_ts: first_ts = ts
                if not last_ts or ts > last_ts: last_ts = ts
            t = obj.get('type', '')
            if t == 'summary':
                summary_text = obj.get('summary', '')
                branch = obj.get('gitBranch', '')
                is_sidechain = obj.get('isSidechain', False)
            elif t == 'assistant':
                assistant_count += 1
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
                if text and len(text) > 5 and not text.startswith('[Request interrupted'):
                    real_human.append(text[:80])

    if not first_ts: continue

    # Convert timestamps to local timezone
    def to_local(iso):
        try:
            dt = datetime.fromisoformat(iso.replace('Z', '+00:00'))
            return dt.astimezone(local_tz).strftime('%Y-%m-%d %H:%M')
        except: return iso

    dur_min = 0
    if first_ts and last_ts:
        try:
            t1 = datetime.fromisoformat(first_ts.replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
            dur_min = int((t2 - t1).total_seconds() / 60)
        except: pass

    # Prefer index summary over first prompt
    idx = index_map.get(sid, {})
    final_summary = idx.get('summary') or summary_text or (real_human[0] if real_human else 'No summary')
    final_branch = branch or idx.get('gitBranch') or 'unknown'

    sessions.append({
        'sessionId': sid[:12],
        'repoName': get_repo_name(source_dir, repo_map),
        'startLocal': to_local(first_ts),
        'endLocal': to_local(last_ts),
        'durationMin': dur_min,
        'realHumanMessages': len(real_human),
        'assistantMessages': assistant_count,
        'firstPrompt': real_human[0] if real_human else None,
        'gitBranch': final_branch,
        'summary': final_summary[:80],
        'isSidechain': is_sidechain,
    })

sessions.sort(key=lambda s: s['startLocal'])  # chronological (oldest first)

GAP_THRESHOLD = 30  # minutes

def parse_local(s):
    try: return datetime.strptime(s, '%Y-%m-%d %H:%M')
    except: return None

with_gaps = []
for i, s in enumerate(sessions):
    if i == 0:
        with_gaps.append({"type": "gap", "label": "sleeping / offline"})
    else:
        prev_end = parse_local(sessions[i-1]['endLocal'])
        curr_start = parse_local(s['startLocal'])
        if prev_end and curr_start:
            gap_min = int((curr_start - prev_end).total_seconds() / 60)
            if gap_min > GAP_THRESHOLD:
                with_gaps.append({"type": "gap", "gapMin": gap_min, "label": f"{gap_min}m gap"})
    with_gaps.append(s)
with_gaps.append({"type": "gap", "label": "no session yet"})

print(json.dumps(with_gaps, indent=2))
```
