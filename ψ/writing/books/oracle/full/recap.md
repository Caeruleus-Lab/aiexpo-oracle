# Oracle skill `recap`: the full skill

> For the AI: this is the WHOLE skill, not a summary. Part 1 says how to run it in a chat with no terminal. Part 2 is every file of the real skill (recap: 5 files) from github.com/Soul-Brews-Studio/arra-oracle-skills-cli (branch alpha, commit 9feea09). Read all of it before you start, follow Part 1 for what to do in this chat, and use Part 2 for the full detail (steps, templates, rules, why). Where Part 2 needs a terminal, git or a script, do the same thing in the chat (show the file content for the person to save) and say so.

## Part 1 · run it in this chat

# /recap in chat: pick up where we left off

> For the AI reading this page. Look for the person's earlier files: a handoff `ψ/inbox/handoff/...md` (from `/forward`), reports `ψ/memory/retrospectives/...md` (from `/rrr`), `ψ/memory/learnings/...md`, and `CLAUDE.md`, as Project files, attachments, or text pasted in this chat. If none are available, say so in one line and ask the person to attach the last handoff or `/rrr` report.
> ถึง AI ที่อ่านหน้านี้: อ่านไฟล์ส่งต่องาน (handoff) และรายงานรอบก่อน แล้วบอกว่าค้างอะไร

The newest handoff wins: its **Next Session** list is where today starts. The retrospective adds what happened and what was learned.

Answer in the person's language, in this shape:
- **รอบก่อนทำอะไร**: 1-2 lines from the latest handoff or retrospective (cite its file name)
- **ค้างอะไร**: the unchecked `- [ ]` items from Pending and Next Session
- **บทเรียนที่ต้องจำ**: 1-2 learnings, if there are any
- **วันนี้เริ่มตรงไหนดี**: 2-3 options, the first one from the handoff's Next Session; the person decides

If CLAUDE.md is there, speak as that Oracle (its name, its principles). End with: "พร้อมแล้ว เลือกข้อไหนครับ/คะ" (match the Oracle's voice) and sign as the Oracle (Oracle AI).

— AIExpo Oracle (Oracle AI), 2026-11-04

## Part 2 · skill `recap`

<!-- file: skills/recap/SKILL.md -->
### File: `skills/recap/SKILL.md`

---
name: recap
description: Session orientation and awareness — retro summaries, handoffs, git state, focus. Use when starting a session, after /jump, lost your place, switching context, or when user asks "now", "where are we", "what are we doing", "status", "recap". Do NOT trigger for "standup" or "morning check" (use /standup), or session mining "dig", "past sessions" (use /dig).
argument-hint: "[--now | --deep]"
trigger: /recap
---

# /recap — Session Orientation & Awareness

**Goal**: Orient yourself fast. Rich context by default. Mid-session awareness with `--now`.

## Usage

```
/recap           # Rich: retro summary, handoff, tracks, git
/recap --quick   # Minimal: git + focus only, no file reads
/recap --now     # Mid-session: timeline + jumps from AI memory
/recap --now deep # Mid-session: + handoff + tracks + connections
```

---

## DEFAULT MODE (Rich)

**Run the rich script, then add suggestions:**

```bash
bun ~/.claude/skills/recap/recap-rich.ts
```

Script reads retro summaries, handoff content, tracks, git state. Then LLM adds:
- **What's next?** (2-3 options based on context)

### Step 1.5: Detect INCUBATED_BY (#229)

The recap-rich.ts script auto-detects `.claude/INCUBATED_BY` breadcrumbs. If present, shows:

```
## ⚠️ INCUBATED REPO
oracle: mawui-oracle
date: 2026-04-13
source: https://github.com/...
```

This tells the oracle: "You are in a repo tracked by another oracle. Check the breadcrumb for context."

### Step 2: Git context

```bash
git status --short
git log --oneline -1
```

Check what's appropriate from git status:
- **Uncommitted changes?** → show them, suggest commit or stash
- **On a branch (not main)?** → `git log main..HEAD --oneline` to see branch work
- **Branch ahead of remote?** → suggest push or PR
- **Clean on main?** → just show last commit, move on

Only read what matters — don't dump 10 commits if status is clean.

### Step 2.5: Skill shelf staleness

Skills are **copied** into `~/.claude/skills/` (fork model), so fixes never
propagate on their own — an oracle can run a superseded skill indefinitely with
nothing to signal it. This surfaces it during orientation, where you'd notice.

```bash
bun "$(dirname "$0")/skills-staleness.ts" 2>/dev/null || true
```

Silent when the shelf is current. Prints only when you are behind, the install is
30+ days old, the manifest can't be reconciled against disk, or `--verbose`.
Never blocks — any failure exits 0 and prints nothing, because orientation must
not break on a diagnostic.

If it reports **BEHIND**, offer the update command it prints; don't run it
unprompted — an install can change the behaviour of skills mid-session.

> Origin: written by neo (`laris-co/neo-oracle`) 2026-08-16 after a `/learn`
> contamination bug was diagnosed in a shelf version that had been superseded
> for two months. Adopted into the shelf so every oracle gets it.

### Step 3: Read latest ψ/ brain files

Sort all ψ/ files by modification time, read the most recent:

```bash
find ψ/ -name '*.md' -not -name 'CLAUDE.md' -not -name 'README.md' -not -name '.gitkeep' 2>/dev/null | xargs ls -t 2>/dev/null | head -5
```

Read those top 5 files. This recovers the same context `/compact` restores — handoffs, retros, learnings, drafts, whatever was touched last.

### Step 4: Dig last session

```bash
ORACLE_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
ENCODED_PWD=$(echo "$ORACLE_ROOT" | sed 's|^/|-|; s|[/.]|-|g')
PROJECT_BASE=$(ls -d "$HOME/.claude/projects/${ENCODED_PWD}" 2>/dev/null | head -1)
export PROJECT_DIRS="$PROJECT_BASE"

# Strip -wt* suffix to find parent project dir
PARENT_ENCODED=$(echo "$ENCODED_PWD" | sed 's/-wt-[^/]*$//')
if [ "$PARENT_ENCODED" != "$ENCODED_PWD" ]; then
  PARENT_BASE=$(ls -d "$HOME/.claude/projects/${PARENT_ENCODED}" 2>/dev/null | head -1)
  [ -n "$PARENT_BASE" ] && export PROJECT_DIRS="$PROJECT_DIRS:$PARENT_BASE"
fi

# nullglob-safe worktree scan (both parent and self)
for base in "$PROJECT_BASE" "$PARENT_BASE"; do
  [ -z "$base" ] && continue
  for wt in "$base"-wt-*(N); do  # (N) = zsh nullglob qualifier
    [ -d "$wt" ] && export PROJECT_DIRS="$PROJECT_DIRS:$wt"
  done
done

python3 ~/.claude/skills/dig/scripts/dig.py 1
```

Include in recap:
```
📡 Last session: HH:MM–HH:MM (Xm, N msgs) — [topic]
```

Need more? `/dig 5` or `/dig --timeline`.

**Total**: 1 bash call + LLM analysis

---

## QUICK MODE (`/recap --quick`)

**Minimal, no content reads:**

```bash
bun ~/.claude/skills/recap/recap.ts
```

Script outputs git status + focus state (~0.1s). Then LLM adds:
- **What's next?** (2-3 options based on git state)

---

## "What's next?" Rules

| If you see... | Suggest... |
|---------------|------------|
| Handoff exists | Continue from handoff |
| Untracked files | Commit them |
| Focus = completed | Pick from tracks or start fresh |
| Branch ahead | Push or create PR |
| Streak active | Keep momentum going |

---

## Hard Rules

1. **ONE bash call** — never multiple parallel calls (adds latency)
2. **No subagents** — everything in main agent
3. **Ask, don't suggest** — "What next?" not "You should..."
4. **Verify pending before reporting** — see "Verify Before Reporting" section below. This is NON-NEGOTIABLE.
5. **Print absolute paths** — when referencing vault files, render the resolved `$ROOT/ψ/...` path (starts with `/`). Bare `ψ/...` is not clickable. See CONVENTIONS.md.

---

## Verify Before Reporting (MANDATORY)

Handoffs, retros, and memory files are **point-in-time claims**, not live state. Between the previous session ending and this one starting, work may have been done, PRs may have merged, files may have been copied. **Echoing a stale pending list as if it were current is a lie by omission** — the human ends up chasing items that are already done.

### The rule

Before outputting any "Pending" table or "Next action" suggestion, you MUST verify each claimed pending item against current reality:

| Claim type | How to verify |
|---|---|
| "Copy file X to path Y" | `ls path/Y` — is it already there? |
| "PR #N open/merged" | `gh pr view N --json state` |
| "Branch X needs push" | `git log origin/X..X` — any commits? |
| "Apply pattern P to file F" | `grep` for the pattern in F |
| "Issue #N pending" | `gh issue view N --json state` |
| "Migration ready to run" | check migrations table or list |

### What to do with each verified item

- **Already done** → drop from pending, note in "Actually done since handoff"
- **Still pending** → keep, show in table
- **Partially done** → split into remaining sub-items
- **Can't verify** (offline/ambiguous) → mark `⚠️ unverified` in the table, do not assert state

### The correction pattern

If the handoff pending list and reality diverge (>1 item stale), show the correction explicitly so the human sees the drift:

```
| Item | Handoff said | Reality |
|------|--------------|---------|
| Copy cache/ to maw-ui | pending | DONE (Apr 20 04:16) |
| PR #4 merge | open | MERGED |
```

### Why this is non-negotiable

- Handoffs are written before work stops, but work often continues between sessions (other Oracles, scheduled tasks, user actions).
- Memory files age — an older memory claiming "feature X is broken" may be stale if a fix shipped.
- Humans trust recap output as ground truth. An unverified echo breaks that trust fast.

**Patterns over intentions** — the code is the truth, the handoff is an intention. Always verify.

---

---

## NOW MODE (`/recap --now`)

**Mid-session awareness from AI memory** — no file reading needed. Use when user asks "where are we", "now", "status", "what are we doing".

AI reconstructs session timeline from conversation memory:

```markdown
## This Session

| Time | Duration | Topic | Jump |
|------|----------|-------|------|
| HH:MM | ~Xm | First topic | - |
| HH:MM | ~Xm | Second topic | spark |
| HH:MM | ongoing | **Now**: Current | complete |

**Noticed**:
- [Pattern - energy/mode]
- [Jump pattern: sparks vs escapes vs completions]

**Status**:
- Energy: [level]
- Loose ends: [unfinished]
- Parked: [topics we'll return to]

**My Read**: [1-2 sentences]

---
**Next?**
```

### Jump Types

| Icon | Type | Meaning |
|------|------|---------|
| spark | New idea, exciting |
| complete | Finished, moving on |
| return | Coming back to parked |
| park | Intentional pause |
| escape | Avoiding difficulty |

**Healthy session**: Mostly sparks and completes
**Warning sign**: Too many escapes = avoidance pattern

---

## NOW DEEP MODE (`/recap --now deep`)

Same as `--now` but adds bigger picture context.

### Step 1: Gather (parallel)

```
1. Current session from AI memory
2. Read latest handoff: ls -t ψ/inbox/handoff/*.md | head -1
3. Git status: git status --short
4. Tracks: cat ψ/inbox/tracks/INDEX.md 2>/dev/null
```

### Step 1.5: VERIFY pending from handoff

Before outputting, run verification checks against each pending item (see "Verify Before Reporting" above). Batch checks in parallel:
- `gh pr list --state all` for PR claims
- `ls path/to/file` for "copy X" claims
- `grep` for "apply pattern" claims

If any diverge from the handoff, show the correction table.

### Step 2: Output

Everything from `--now`, plus:

```markdown
### Bigger Picture

**Came from**: [Last session/handoff summary - 1 line]
**Working on**: [Current thread/goal]
**Thread**: [Larger pattern this connects to]

### Pending

| Priority | Item | Source |
|----------|------|--------|
| Now | [Current task] | This session |
| Soon | [Next up] | Tracks/discussion |
| Later | [Backlog] | GitHub/tracks |

### Connections

**Pattern**: [What pattern emerged]
**Learning**: [Key insight from session]
**Oracle**: [Related past pattern, if any]

**My Read**: [2-3 sentences - deeper reflection]

**Next action?**
```

---

## Session Context

The recap scripts (`recap.ts` and `recap-rich.ts`) auto-detect and display the current session:

```
📡 Session: 74c32f34 | arra-oracle-skills-cli | 2h 15m
```

Detection: scans `~/.claude/projects/[encoded-pwd]/*.jsonl` for the most recent session file, extracts short ID and elapsed time from first timestamp.

If session detection fails, skip silently — it's informational only.

---

## Demographics Context

If CLAUDE.md contains demographics from `/awaken` wizard v2, include in recap output:

```markdown
**Oracle**: [name] ([pronouns]) | **Human**: [name] ([pronouns]) | **Language**: [pref]
```

Add this as one line after the timestamp in any mode. If demographics not present, skip silently.

Look for fields in CLAUDE.md: `Human Pronouns`, `Oracle Pronouns`, `Language`, `Team`, `Experience`.

---

**Philosophy**: Detect reality. Surface blockers. Offer direction. *"Not just the clock. The map."*

**Version**: 8.0 (Merged where-we-are into --now mode)
**Updated**: 2026-02-10

<!-- file: skills/recap/references/rich-paths.md -->
### File: `skills/recap/references/rich-paths.md`

# RICH MODE — 18-Path Detection

Full detection for edge cases. Use when:
- Something feels wrong
- Need detailed diagnosis
- Session is confused

## Data Gathering

```bash
ROOT=$(git rev-parse --show-toplevel)

# Git state
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
MODIFIED=$(git status --short 2>/dev/null | wc -l)
CONFLICTS=$(git diff --name-only --diff-filter=U 2>/dev/null | wc -l)

# Focus file
FOCUS_FILE="$ROOT/ψ/inbox/focus-agent-main.md"
if [ -f "$FOCUS_FILE" ]; then
  FOCUS_STATE=$(head -1 "$FOCUS_FILE" | sed 's/STATE: //')
  FOCUS_MTIME=$(stat -f%m "$FOCUS_FILE" 2>/dev/null)
  NOW=$(date +%s)
  FOCUS_HOURS=$(( (NOW - FOCUS_MTIME) / 3600 ))
  grep -q "^STATE:" "$FOCUS_FILE" || FOCUS_STATE="corrupted"
else
  FOCUS_STATE="missing"
fi

# Activity log
ACTIVITY_LOG="$ROOT/ψ/memory/logs/activity.log"
[ -f "$ACTIVITY_LOG" ] && LAST_ACTIVITY=$(tail -1 "$ACTIVITY_LOG" | cut -d'|' -f3 | xargs)

# Latest retro
LATEST_RETRO=$(find "$ROOT/ψ/memory/retrospectives" -name "*.md" -type f 2>/dev/null | grep -v CLAUDE | sort -r | head -1)
```

## Detection Precedence (In Order)

**Priority matters. Check conditions in this exact order, stop at first match.**

| Order | Condition | Return Path | Why |
|-------|-----------|-------------|-----|
| 1 | Git in merge/rebase state | GIT_CONFLICT_STATE | Prevents accidental commands |
| 2 | CONFLICTS > 0 | BLOCKER | Technical blocker—must resolve |
| 3 | FOCUS_STATE == "corrupted" | CORRUPTED_FOCUS | Can't parse, must fix |
| 4 | FOCUS_STATE == "pending" + has reason | BLOCKER | User explicitly waiting |
| 5 | FOCUS_STATE == "pending" + no reason | PENDING_NO_REASON | Incomplete state—clarify |
| 6 | FOCUS focusing + age < 4h | DEEP_WORK | Continue uninterrupted |
| 7 | FOCUS hours > 24 + recent commits | ASYNC_WORK | Work continued off-book |
| 8 | Both focus files exist | MULTI_FOCUS | Pattern collision—consolidate |
| 9 | Branch 100+ commits ahead | BRANCH_DIVERGED | Strategy needed before sync |
| 10 | "completed" in activity + files modified | INCOMPLETE_AFTER_MARKED_DONE | State inconsistency |
| 11 | MODIFIED > 5 + not focusing | UNCLEAN | Need attention |
| 12 | FOCUS_STATE == "completed" | TRANSITION | Clear finish line |
| 13 | FOCUS age >= 4h | STALE_FOCUS | Verify still current |
| 14 | No focus + clean git + gap | FRESH_START | Complete blank slate |
| 15 | No activity.log | NO_ACTIVITY_LOG | First session or reset |
| 16 | Tracks untouched 7+ days | TRACKS_DORMANT | Momentum loss |
| 17 | Retro corrupted (missing sections) | CORRUPTED_RETRO | Data integrity issue |
| 18 | (else) | CONFUSED | Doesn't fit patterns |

---

## Output Paths

### Path: BLOCKER (Conflicts or Pending)

```markdown
# RECAP — BLOCKED

[TIME]

**Blocker**: [reason from focus or conflict list]

---

What's needed to unblock?
```

**When**: Conflicts exist OR `STATE: pending` with reason

---

### Path: GIT_CONFLICT_STATE

```markdown
# RECAP — 🚩 Git In Merge/Rebase

[TIME]

Git is active in merge/rebase. All commands will fail.

**Steps**:
1. Resolve: `git status`
2. Continue: `git merge --continue` or `git rebase --continue`
3. Or abort: `git merge --abort` or `git rebase --abort`

Ready?
```

---

### Path: DEEP_WORK

```markdown
# RECAP

[TIME]

## On It

**Task**: [from focus file]
**Working**: [FOCUS_HOURS] min

**Git**: [MODIFIED] modified, last commit [time ago]

What's next?
```

**When**: `STATE: focusing` AND FOCUS_HOURS < 4

---

### Path: STALE_FOCUS

```markdown
# RECAP

[TIME]

## Focus File Stale

Last recorded: **[task]** ([FOCUS_HOURS] hours ago)

Git: [MODIFIED] modified

Recent: [last 2 activity entries]

---

Still current? Or reset?
```

**When**: FOCUS_HOURS >= 4 (and not other categories)

---

### Path: ASYNC_WORK

```markdown
# RECAP — Async Work Detected

[TIME]

Focus last updated: [FOCUS_HOURS] hours ago

But commits found: [last 2 commits]

---

Did work continue without updating focus?

Recent: `git log -3 --oneline`

Update focus or continue?
```

**When**: FOCUS_HOURS > 24 AND last_commit < 2 hours

---

### Path: CORRUPTED_FOCUS

```markdown
# RECAP — Focus File Broken

[TIME]

Can't parse: [filename]

Content:
[first 3 lines]

---

Recreate? Pattern:
STATE: [state]
TASK: [task]
SINCE: [HH:MM]
```

---

### Path: PENDING_NO_REASON

```markdown
# RECAP — Pending But Unclear

[TIME]

Marked as pending, no reason given.

Recent activity:
[last 5 log entries]

---

What were you waiting on?
```

---

### Path: MULTI_FOCUS

```markdown
# RECAP — Two Focus Files

[TIME]

**focus-agent-main.md**: [STATE + TASK]

**focus.md**: [STATE + TASK]

---

Which is current? Delete the other.
```

---

### Path: BRANCH_DIVERGED

```markdown
# RECAP — Branch Heavily Diverged

[TIME]

**Branch**: [name], [count] commits ahead of main

Last sync: [when]

---

Choose:
1. Prepare PR: `git log origin/main..[branch]`
2. Rebase: `git rebase origin/main`
3. Start over: `git checkout main`
```

---

### Path: INCOMPLETE_AFTER_MARKED_DONE

```markdown
# RECAP — Incomplete After Done

[TIME]

Activity log says: completed

Git shows: [N] modified files

---

What needs resolving?
```

---

### Path: UNCLEAN

```markdown
# RECAP

[TIME]

**Git State**: [MODIFIED] modified

[git status --short | head -5]

---

Commit first? Or reset?
```

**When**: MODIFIED > 5 + not focusing

---

### Path: TRANSITION

```markdown
# RECAP

[TIME]

## Complete

**Task**: [from focus] ✓

**Session did**: [from handoff or last retro—2 bullet points max]

**Last commit**: [git log -1 --oneline]

---

## Board

Hot tracks: [from ψ/inbox/tracks/ or "None"]

---

What's next?
```

**When**: FOCUS_STATE == "completed"

**Data gathering for TRANSITION**:
```bash
# Get session summary from handoff (if exists)
HANDOFF=$(ls -t "$ROOT/ψ/inbox/handoff/"*.md 2>/dev/null | head -1)
[ -f "$HANDOFF" ] && grep -A5 "## What We Did" "$HANDOFF" | head -6

# Get last commit
git -C "$ROOT" log -1 --oneline

# Get hot tracks
ls "$ROOT/ψ/inbox/tracks/"*.md 2>/dev/null | head -3
```

---

### Path: FRESH_START

```markdown
# RECAP

[TIME]

## Context

Last work: [from retro AI Diary—exact, 2 sentences]

**Learning**: [from retro Honest Feedback—one point]

---

## Board

Hot tracks: [list or "None"]

---

What to tackle?
```

**When**: No focus + clean + gap

---

### Path: NO_ACTIVITY_LOG

```markdown
# RECAP — No Activity History

[TIME]

First session? Log was deleted?

**State**: [branch] | [git status] | [focus exists?]

---

What to work on?
```

---

### Path: TRACKS_DORMANT

```markdown
# RECAP — Tracks Cold

[TIME]

No touches for 7+ days.

Last: [X days ago]

---

Restart a cold track? Consolidate? Fresh work?
```

---

### Path: CORRUPTED_RETRO

```markdown
# RECAP — Retro Corrupted

[TIME]

File: **[filename]**

Missing expected sections.

---

1. View: `cat [path]`
2. New: `rrr`
3. Ignore: continue

?
```

---

### Path: CONFUSED

```markdown
# RECAP — Let Me Check

[TIME]

**Focus**: [state] ([hours] old)
**Git**: [modified] modified, [conflicts] conflicts
**Activity**: [last entry]
**Branch**: [branch]

---

What's the situation?
```

<!-- file: skills/recap/recap-rich.ts -->
### File: `skills/recap/recap-rich.ts`

```ts
#!/usr/bin/env bun
// recap-rich.ts - Full context recap
import { $ } from "bun";
import { existsSync, readdirSync, realpathSync } from "fs";
import { join } from "path";

const ROOT = process.env.ROOT || (await $`git rev-parse --show-toplevel`.text().catch(() => process.cwd())).trim();
const isGit = (await $`git -C ${ROOT} rev-parse --is-inside-work-tree`.quiet().text().catch(() => "false")).trim() === "true";
if (isGit) await $`git -C ${ROOT} config core.quotePath false`.quiet().catch(() => {});

const now = new Date();
const date = now.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
const time = now.toTimeString().slice(0, 5);
const month = now.toISOString().slice(0, 7);

// Session detection
let sessionLine = "";
try {
  const encodedPwd = ROOT.replace(/^\//, '-').replace(/[\/.]/g, '-');
  const claudeHome = process.env.CLAUDE_CONFIG_DIR || `${process.env.HOME}/.claude`;
  const projectDir = `${claudeHome}/projects/${encodedPwd}`;
  if (existsSync(projectDir)) {
    const jsonls = (await $`ls -t ${projectDir}/*.jsonl 2>/dev/null`.text()).trim().split('\n').filter(Boolean);
    if (jsonls.length) {
      const envSessionId = process.env.CLAUDE_CODE_SESSION_ID;
      const envJsonl = envSessionId ? `${projectDir}/${envSessionId}.jsonl` : "";
      const chosenJsonl = envJsonl && existsSync(envJsonl) ? envJsonl : jsonls[0];
      const sessionId = chosenJsonl.split('/').pop()!.replace('.jsonl', '');
      const shortId = sessionId.slice(0, 8);
      const firstLine = (await $`head -1 ${chosenJsonl}`.text()).trim();
      let startStr = "";
      try {
        const ts = JSON.parse(firstLine).timestamp;
        if (ts) {
          const start = new Date(ts);
          const elapsed = Math.round((Date.now() - start.getTime()) / 60000);
          const h = Math.floor(elapsed / 60);
          const m = elapsed % 60;
          startStr = h > 0 ? `${h}h ${String(m).padStart(2, '0')}m` : `${m}m`;
        }
      } catch {}
      const repoName = ROOT.split('/').pop() || '';
      sessionLine = `${shortId} | ${repoName}${startStr ? ` | ${startStr}` : ''}`;
    }
  }
} catch {}

console.log("# RECAP (Rich)");
if (sessionLine) console.log(`📡 Session: ${sessionLine}`);
console.log(`\n${time} | ${date}\n\n---\n`);

// Resolve ψ symlink (used for focus + schedule)
const psiPath = join(ROOT, "ψ");
const psi = existsSync(psiPath) ? realpathSync(psiPath) : psiPath;

// INCUBATED_BY detection (#229)
const incubatedByPath = join(ROOT, ".claude", "INCUBATED_BY");
if (existsSync(incubatedByPath)) {
  const breadcrumb = await Bun.file(incubatedByPath).text();
  console.log("## ⚠️ INCUBATED REPO");
  console.log(breadcrumb.trim());
  console.log("");
}

// Focus
console.log("## FOCUS");
const focusFile = join(psi, "inbox", "focus-agent-main.md");
if (existsSync(focusFile)) {
  const content = await Bun.file(focusFile).text();
  const state = content.match(/^STATE:(.*)$/m)?.[1]?.trim() || "none";
  const task = content.match(/^TASK:(.*)$/m)?.[1]?.trim() || "No active focus";
  console.log(`\`${state}\` ${task}`);
} else {
  console.log("No focus file");
}

// Schedule
console.log("\n## UPCOMING");
const scheduleFile = join(psi, "inbox", "schedule.md");
if (existsSync(scheduleFile)) {
  const lines = (await Bun.file(scheduleFile).text()).split("\n");
  const rows = lines.filter((l) => l.startsWith("| ") && !l.includes("---") && !l.includes("Date")).slice(0, 5);
  console.log(rows.join("\n") || "No events");
} else {
  console.log("No schedule file");
}

// Git
console.log("\n## GIT");
if (isGit) {
  console.log(await $`git -C ${ROOT} status -sb`.text());
  console.log("**Last 3 commits:**");
  console.log(await $`git -C ${ROOT} log --oneline -3`.text());
} else {
  console.log("Not a git repository");
}

// Tracks
console.log("## TRACKS");
const tracksDir = join(ROOT, "ψ/inbox/tracks");
if (existsSync(tracksDir)) {
  const tracks = readdirSync(tracksDir)
    .filter((f) => f.endsWith(".md") && !f.includes("INDEX") && !f.includes("CLAUDE"))
    .slice(0, 6);
  for (const t of tracks) {
    const content = await Bun.file(join(tracksDir, t)).text();
    const id = t.match(/^(\d+)/)?.[1] || "-";
    const name = content.split("\n")[0]?.replace(/^# Track[^:]*: /, "") || t;
    console.log(`- ${id}: ${name}`);
  }
}

// Latest retro
console.log("\n---\n\n## LAST SESSION");
const retroDir = join(ROOT, `ψ/memory/retrospectives/${month}`);
if (existsSync(retroDir)) {
  const days = readdirSync(retroDir).filter((d) => !d.startsWith(".")).sort().reverse();
  for (const day of days) {
    const files = readdirSync(join(retroDir, day)).filter((f) => f.endsWith(".md") && !f.includes("CLAUDE"));
    if (files.length) {
      const retro = await Bun.file(join(retroDir, day, files[0])).text();
      console.log(`**From**: ${files[0]}\n`);
      const summary = retro.match(/## Session Summary\n([\s\S]*?)(?=\n## |$)/)?.[1]?.trim();
      if (summary) console.log(`**Summary**:\n${summary.split("\n").slice(0, 8).join("\n")}`);
      break;
    }
  }
}

// Handoff
const handoffDir = join(ROOT, "ψ/inbox/handoff");
if (existsSync(handoffDir)) {
  const handoffs = readdirSync(handoffDir).filter((f) => f.endsWith(".md") && !f.includes("CLAUDE")).sort().reverse();
  if (handoffs.length) {
    const content = await Bun.file(join(handoffDir, handoffs[0])).text();
    console.log(`\n**Handoff**: ${handoffs[0]}`);
    console.log(content.split("\n").slice(2, 20).join("\n"));
  }
}

// Context
console.log("\n---\n\n## CONTEXT\n");
if (isGit) {
  const status = await $`git -C ${ROOT} status --porcelain`.text();
  const modified = status.split("\n").filter((l) => l.startsWith(" M")).map((l) => l.slice(3));
  const untracked = status.split("\n").filter((l) => l.startsWith("??")).map((l) => l.slice(3));

  if (modified.length) console.log("**Modified**:\n" + modified.map((f) => `  ${f}`).join("\n"));
  if (untracked.length) console.log("\n**Untracked**:\n" + untracked.map((f) => `  ${f}`).join("\n"));
} else {
  console.log("Not a git repository — skipping file status");
}
```

<!-- file: skills/recap/recap.ts -->
### File: `skills/recap/recap.ts`

```ts
#!/usr/bin/env bun
// Fast recap - no AI, just git status
// Usage: bun recap.ts

import { $ } from "bun";
import { existsSync, realpathSync } from "fs";
import { join } from "path";

// Get repo root
const root = (await $`git rev-parse --show-toplevel 2>/dev/null`.text()).trim() || process.cwd();
process.chdir(root);

// Gather git data
const branch = (await $`git branch --show-current`.text()).trim();
let ahead = "0";
try {
  ahead = (await $`git rev-list --count @{u}..HEAD 2>/dev/null`.text()).trim() || "0";
} catch {}
const lastCommit = (await $`git log --oneline -1`.text()).trim().slice(8, 68);

// Resolve ψ symlink (used for focus + schedule)
const psi = existsSync("ψ") ? realpathSync("ψ") : "ψ";

// Focus state
let focusState = "none";
let focusTask = "No active focus";
const focusFile = join(psi, "inbox", "focus-agent-main.md");
if (existsSync(focusFile)) {
  const focusContent = await Bun.file(focusFile).text();
  const stateMatch = focusContent.match(/^STATE:\s*(.+)/m);
  const taskMatch = focusContent.match(/^TASK:\s*(.+)/m);
  if (stateMatch) focusState = stateMatch[1].trim();
  if (taskMatch) focusTask = taskMatch[1].trim().slice(0, 80);
}

// Schedule
let schedule = "No schedule";
const scheduleFile = join(psi, "inbox", "schedule.md");
if (existsSync(scheduleFile)) {
  const match = (await Bun.file(scheduleFile).text()).split('\n')
    .find(l => l.startsWith('| ') && !l.includes('---') && !l.includes('Date'));
  if (match) schedule = match.replace(/\|/g, '').trim().slice(0, 120);
}

// Latest retro and handoff
const monthDir = `ψ/memory/retrospectives/${new Date().toISOString().slice(0, 7)}`;
let latestRetro = "none";
let latestHandoff = "none";

try {
  const retros = (await $`ls -t ${monthDir}/*/*.md 2>/dev/null`.text()).trim().split('\n');
  const retro = retros.find(f => !f.includes('CLAUDE'));
  if (retro) latestRetro = retro.split('/').pop() || "none";
} catch {}

try {
  const handoffs = (await $`ls -t ψ/inbox/handoff/*.md 2>/dev/null`.text()).trim().split('\n');
  const handoff = handoffs.find(f => !f.includes('CLAUDE'));
  if (handoff) latestHandoff = handoff.split('/').pop() || "none";
} catch {}

// Git status
await $`git config core.quotePath false`.quiet();
const status = (await $`git status --porcelain`.text()).trim();
const lines = status ? status.split('\n') : [];

const modified = lines.filter(l => l.startsWith(' M'));
const untracked = lines.filter(l => l.startsWith('??'));

// Session detection
let sessionLine = "";
try {
  const encodedPwd = root.replace(/^\//, '-').replace(/[\/.]/g, '-');
  const claudeHome = process.env.CLAUDE_CONFIG_DIR || `${process.env.HOME}/.claude`;
  const projectDir = `${claudeHome}/projects/${encodedPwd}`;
  if (existsSync(projectDir)) {
    const jsonls = (await $`ls -t ${projectDir}/*.jsonl 2>/dev/null`.text()).trim().split('\n').filter(Boolean);
    if (jsonls.length) {
      const envSessionId = process.env.CLAUDE_CODE_SESSION_ID;
      const envJsonl = envSessionId ? `${projectDir}/${envSessionId}.jsonl` : "";
      const chosenJsonl = envJsonl && existsSync(envJsonl) ? envJsonl : jsonls[0];
      const sessionId = chosenJsonl.split('/').pop()!.replace('.jsonl', '');
      const shortId = sessionId.slice(0, 8);
      const firstLine = (await $`head -1 ${chosenJsonl}`.text()).trim();
      let startStr = "";
      try {
        const ts = JSON.parse(firstLine).timestamp;
        if (ts) {
          const start = new Date(ts);
          const elapsed = Math.round((Date.now() - start.getTime()) / 60000);
          const h = Math.floor(elapsed / 60);
          const m = elapsed % 60;
          startStr = h > 0 ? `${h}h ${String(m).padStart(2, '0')}m` : `${m}m`;
        }
      } catch {}
      const repoName = root.split('/').pop() || '';
      sessionLine = `${shortId} | ${repoName}${startStr ? ` | ${startStr}` : ''}`;
    }
  }
} catch {}

// Output
const now = new Date();
const time = now.toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit', hour12: false });
const date = now.toLocaleDateString('en', { day: '2-digit', month: 'short', year: 'numeric' });

console.log("# RECAP");
console.log("");
if (sessionLine) console.log(`📡 Session: ${sessionLine}`);
console.log(`🕐 ${time} | ${date}`);
console.log("");
console.log("---");
console.log("");
console.log("## 🚧 FOCUS");
console.log(`\`${focusState}\` ${focusTask}`);
console.log("");
console.log("## 📅 TODAY");
console.log(schedule);
console.log("");
console.log(`## 📊 GIT: ${branch} (+${ahead} ahead)`);
console.log(`Last: ${lastCommit}`);
console.log("");

if (modified.length) {
  console.log(`**Modified** (${modified.length}):`);
  modified.forEach(l => console.log(`  ${l.slice(3)}`));
  console.log("");
}

if (untracked.length) {
  console.log(`**Untracked** (${untracked.length}):`);
  untracked.forEach(l => console.log(`  ${l.slice(3)}`));
  console.log("");
}

console.log("---");
console.log("");
console.log("## 📝 LAST SESSION");
console.log(`Retro: ${latestRetro}`);
console.log(`Handoff: ${latestHandoff}`);
```

<!-- file: skills/recap/skills-staleness.ts -->
### File: `skills/recap/skills-staleness.ts`

```ts
#!/usr/bin/env bun
// skills-staleness.ts — is your installed Oracle skill shelf behind the source?
//
// Originally written by neo (laris-co/neo-oracle) on 2026-08-16; adopted into the
// shelf so every oracle gets it, not just neo. Two corrections on adoption are
// marked [ADOPTED] below.
//
// WHY THIS EXISTS (2026-08-16): staleness discovery was circular — the only way to
// learn you were behind was to run an install, which required already knowing you
// needed one. Result: a /learn contamination bug was diagnosed in a shelf version
// that had been superseded for two months, and nobody noticed. The fork install
// model (files copied into ~/.claude/skills) means fixes never propagate on their
// own; a managed/subscribe route would, which is the real argument for offering one.
//
// The data was always on disk. Nothing read it. This reads it.
//
// DESIGN RULES (each earned the hard way):
//  - Never block. Any failure prints nothing and exits 0. Orientation must not break.
//  - No network by default. `git ls-remote` on session start is a latency tax.
//  - NEVER claim "up to date" from a source you haven't verified is current. A local
//    ghq clone can itself be stale — so report the clone's own fetch age alongside its
//    version, rather than presenting it as upstream truth.
//
// Usage:  bun skills-staleness.ts            # quiet unless something's off
//         bun skills-staleness.ts --verbose  # always print what it found

import { existsSync } from 'fs';
import { readdirSync } from 'fs';
import { join } from 'path';
import { $ } from 'bun';

const VERBOSE = process.argv.includes('--verbose');
const HOME = process.env.HOME ?? '';
const SKILLS_DIR = join(HOME, '.claude/skills');
const MANIFEST = join(SKILLS_DIR, '.arra-oracle-skills.json');
const SOURCE_REPO = 'Soul-Brews-Studio/arra-oracle-skills-cli';

type Manifest = { version?: string; installedAt?: string; skills?: string[]; agent?: string };

function daysSince(iso: string): number | null {
  const t = Date.parse(iso);
  return Number.isFinite(t) ? Math.floor((Date.now() - t) / 86_400_000) : null;
}

/**
 * [ADOPTED — fix 1] Prerelease-aware comparison. The original dropped the
 * prerelease tag as NaN, so `26.7.27-alpha.947` parsed to [26,7,27,947] and
 * compared as AHEAD of the release [26,7,27]. Everyone sitting on a prerelease
 * was told they were current the moment it shipped as a release.
 *
 * Mirrors compareVersions() in src/cli/installer.ts (#500), which is locked down
 * by tests — keep the two in step.
 */
function compareVersions(a: string, b: string): number {
  const split = (v: string) => {
    const [core, pre = ''] = v.split('-', 2);
    return {
      nums: core.split('.').map((n) => parseInt(n, 10) || 0),
      pre: pre ? pre.split('.').map((p) => (/^\d+$/.test(p) ? parseInt(p, 10) : p)) : null,
    };
  };
  const [x, y] = [split(a), split(b)];
  for (let i = 0; i < Math.max(x.nums.length, y.nums.length); i++) {
    const d = (x.nums[i] ?? 0) - (y.nums[i] ?? 0);
    if (d !== 0) return d;
  }
  if (!x.pre && y.pre) return 1; // a release outranks a prerelease of the same core
  if (x.pre && !y.pre) return -1;
  if (!x.pre || !y.pre) return 0;
  for (let i = 0; i < Math.max(x.pre.length, y.pre.length); i++) {
    const [p, q] = [x.pre[i], y.pre[i]];
    if (p === undefined) return -1;
    if (q === undefined) return 1;
    if (p === q) continue;
    if (typeof p === 'number' && typeof q === 'number') return p - q;
    return String(p) < String(q) ? -1 : 1;
  }
  return 0;
}

const isBehind = (installed: string, source: string) => compareVersions(installed, source) < 0;

async function main() {
  if (!existsSync(MANIFEST)) return; // shelf not installed — nothing to say

  let m: Manifest;
  try {
    m = JSON.parse(await Bun.file(MANIFEST).text());
  } catch {
    return; // unreadable manifest is not our problem to report here
  }
  if (!m.version) return;

  const age = m.installedAt ? daysSince(m.installedAt) : null;

  // Find a local source clone WITHOUT a network call.
  //
  // `ghq root` is the accurate answer when ghq is installed, but it is a BINARY
  // DEPENDENCY and swallowing its absence made the whole BEHIND branch silently
  // unreachable: no ghq → no root → no srcDir → `behind` permanently false. The
  // tool then reports a healthy shelf forever, on every machine without ghq,
  // which is most machines that install a published skill. Caught by CI, which
  // has no ghq — three BEHIND tests failed there while passing locally, because
  // the fixture and the author's machine both happened to have it.
  //
  // So fall back to ghq's own documented default root ($HOME/ghq) when the
  // binary is missing. A user who keeps clones there still gets detection; one
  // who does not is no worse off than before.
  let ghqRoot = '';
  try {
    ghqRoot = (await $`ghq root`.quiet().text()).trim();
  } catch {
    /* ghq not installed — fall through to the conventional default */
  }
  if (!ghqRoot) ghqRoot = join(HOME, 'ghq');
  const srcDir = ghqRoot ? join(ghqRoot, 'github.com', SOURCE_REPO) : '';
  const hasSrc = srcDir && existsSync(join(srcDir, 'package.json'));

  let srcVersion = '';
  let fetchAgeDays: number | null = null;
  if (hasSrc) {
    try {
      srcVersion = JSON.parse(await Bun.file(join(srcDir, 'package.json')).text()).version ?? '';
    } catch {}
    // How stale is the CLONE itself? Never present an unfetched clone as upstream truth.
    try {
      const t =
        (await $`git -C ${srcDir} log -1 --format=%ct FETCH_HEAD`.quiet().text()).trim() ||
        (await $`git -C ${srcDir} log -1 --format=%ct`.quiet().text()).trim();
      const secs = Number.parseInt(t, 10);
      if (Number.isFinite(secs)) fetchAgeDays = Math.floor((Date.now() / 1000 - secs) / 86_400);
    } catch {}
  }

  const behind = srcVersion ? isBehind(m.version, srcVersion) : false;
  const oldInstall = age !== null && age >= 30;

  // ── MANIFEST-vs-DISK RECONCILIATION ────────────────────────────────────────
  // Don't trust the manifest on its own — count the disk and refuse to be reassured.
  //
  // Note isDirectory() deliberately does NOT follow symlinks: externally-linked
  // skills (e.g. ego-browser → ~/.local/share/ego) are not shelf-managed and must
  // not count as "unrecorded", or this fires on a healthy install.
  //
  // [ADOPTED — fix 3, found by neo] The predicate MUST match the one the installer
  // uses to build the manifest (src/cli/installer.ts:770-774), which additionally
  // requires a SKILL.md:
  //
  //     .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
  //     .filter((name) => existsSync(join(targetDir, name, 'SKILL.md')))
  //
  // Reconciling against a WIDER population than the manifest is built from makes
  // any SKILL.md-less directory permanently unrecorded: unrecorded > 0 forever,
  // MANIFEST UNRELIABLE forever, and no reinstall can ever clear it — while the
  // message tells you to reinstall. A sticky false positive on a healthy shelf is
  // the fastest way to make people stop reading the tool.
  let onDisk = 0;
  let diskReadFailed = false;
  try {
    onDisk = readdirSync(SKILLS_DIR, { withFileTypes: true })
      .filter((d) => d.isDirectory() && !d.name.startsWith('.'))
      .filter((d) => existsSync(join(SKILLS_DIR, d.name, 'SKILL.md'))).length;
  } catch {
    diskReadFailed = true; // [ADOPTED — fix 2] see below
  }
  const recorded = m.skills?.length ?? 0;
  const unrecorded = onDisk - recorded;
  const manifestUntrustworthy = onDisk > 0 && recorded > 0 && unrecorded > 0;

  // [neo, #25] Reconciliation ran in ONE DIRECTION ONLY. `unrecorded > 0` sees
  // disk exceeding the manifest; the opposite drift went entirely unreported,
  // because the subtraction simply goes negative and the guard is false.
  //
  // Measured before fixing: manifest recording 36 skills against a disk holding
  // 1 printed NOTHING in quiet mode and exit 0, and in --verbose cheerfully said
  // "36 skills recorded" while 35 were gone. A shelf that had lost 35 of 36
  // skills read as healthy, from a tool whose entire premise is reconciling two
  // sources against each other.
  //
  // This direction is the more urgent of the two: unrecorded skills are an
  // inventory gap, missing skills are LOST WORK.
  const missing = recorded - onDisk;
  const skillsMissing = recorded > 0 && !diskReadFailed && missing > 0;

  if (
    !behind &&
    !oldInstall &&
    !manifestUntrustworthy &&
    !skillsMissing &&
    !diskReadFailed &&
    !VERBOSE
  )
    return;

  console.log('\n## 🧩 SKILL SHELF');
  console.log(
    `installed: v${m.version}${age !== null ? `  (${age}d ago)` : ''}  ·  ${recorded} skills recorded`,
  );

  // [ADOPTED — fix 2] Fail closed, not open. If the disk read throws, the
  // reconciliation guard silently evaluates false and the tool reports a
  // confident "all clear" it cannot justify — the exact fail-open shape
  // /verification-gate-fail-closed exists to prevent. Say so instead.
  if (diskReadFailed) {
    console.log(`⚠️  Could not read ${SKILLS_DIR} — manifest could NOT be reconciled against disk.`);
    console.log(`   Treat everything below as UNVERIFIED.`);
  }

  if (skillsMissing) {
    console.log(`⚠️  SKILLS MISSING — manifest records ${recorded}, only ${onDisk} on disk.`);
    console.log(`   ${missing} skill(s) the manifest claims are NOT present. This is lost work,`);
    console.log(`   not an inventory gap — a shelf can silently lose skills to a failed install,`);
    console.log(`   an interrupted profile alignment, or manual deletion.`);
    console.log(`   Recover: reinstall from a current tree, then check the orphan trash dir.`);
  }

  if (manifestUntrustworthy) {
    console.log(`⚠️  MANIFEST UNRELIABLE — ${onDisk} skill dirs on disk, only ${recorded} recorded.`);
    console.log(`   ${unrecorded} skill(s) have NO version record; the v${m.version} stamp covers`);
    console.log(`   only the ${recorded} listed. Treat "not behind" below as unproven.`);
    // [ADOPTED — fix 1b] The original named installer.ts:704 as the root cause.
    // That was fixed on alpha by #458 (the manifest now derives from disk), so
    // naming it would send people to fix an already-fixed bug. The drift that
    // remains is real but its cause depends on which version installed last.
    console.log(`   Likely cause: a skill installed by an older CLI (pre-#458) or by hand.`);
    console.log(`   Fix: reinstall from a current tree so the manifest is rebuilt from disk.`);
  }

  if (behind) {
    console.log(`⚠️  BEHIND — local source says v${srcVersion}`);
    console.log(`   update: bunx --bun github:${SOURCE_REPO}#alpha install -g -y --agent claude-code`);
  } else if (srcVersion && VERBOSE) {
    console.log(`local source: v${srcVersion} (not behind)`);
  } else if (!hasSrc && VERBOSE) {
    console.log('local source clone not found — cannot compare (no network check by design)');
  }

  // Honesty about the comparison basis.
  if (srcVersion && fetchAgeDays !== null && fetchAgeDays >= 7) {
    console.log(`   ⓘ compared against a LOCAL clone last updated ${fetchAgeDays}d ago —`);
    console.log(`     it may itself be behind. \`git -C ${srcDir} fetch\` to be sure.`);
  }

  if (oldInstall && !behind) {
    console.log(`ⓘ install is ${age}d old; no newer local source found — worth a fetch.`);
  }
}

main().catch(() => {}); // never break the caller
```
