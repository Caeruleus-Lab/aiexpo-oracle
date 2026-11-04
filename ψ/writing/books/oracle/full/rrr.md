# Oracle skill `rrr`: the full skill

> For the AI: this is the WHOLE skill, not a summary. Part 1 says how to run it in a chat with no terminal. Part 2 is every file of the real skill (rrr: 4 files) from github.com/Soul-Brews-Studio/arra-oracle-skills-cli (branch alpha, commit 9feea09). Read all of it before you start, follow Part 1 for what to do in this chat, and use Part 2 for the full detail (steps, templates, rules, why). Where Part 2 needs a terminal, git or a script, do the same thing in the chat (show the file content for the person to save) and say so.

## Part 1 · run it in this chat

# /rrr in chat: the session report

> For the AI reading this page. The person wants a retrospective of THIS chat. Write it from what really happened in the conversation above; never invent times or facts. If you do not know the current time, ask the person "ตอนนี้กี่โมงครับ" once before writing. Answer in the person's language (Thai by default). If an Oracle was awakened earlier in this chat, write as that Oracle and sign with its name.
> ถึง AI ที่อ่านหน้านี้: เขียนรายงานสรุปแชทนี้จากสิ่งที่เกิดขึ้นจริงเท่านั้น

## Output: ONE document (artifact / canvas / code block) named
`ψ/memory/retrospectives/<YYYY-MM>/<DD>/<HH.MM>_<short-slug>.md` (use today's date; if you do not know the time, write `unknown` instead of guessing)

```
# Session Retrospective: <title>

**Date**: <date> · **Oracle**: <name> · **Human**: <person>

## Summary
<2-3 sentences: what we set out to do, what got done>

## Timeline
| เวลา | เกิดอะไร | ใครพูดอะไร |
|---|---|---|
| HH:MM | <step> | <one line, quote the person when it matters> |
(times only from the person's messages or a real clock tool; if a time is unknown write "ไม่ทราบเวลา" and keep the order. If a time log exists in this chat, copy it here.)

## What went well
- …
## What could be better
- …
## Lessons learned
- <a pattern that will help next time, one line each>

## Next steps
- [ ] …

## AI diary
<3-5 honest sentences in the Oracle's own voice: what was hard, what it learned about working with this person>

## Honest feedback
<1-2 sentences to the human, kind and direct>

— <Oracle name> (Oracle AI)
```

## Then make a second, short document: the lesson
`ψ/memory/learnings/<YYYY-MM-DD>_<slug>.md` with the one most reusable lesson (3-5 lines).

## Finally tell the person, in 2 bullets
- Save both files (claude.ai: add them to the Project files) so the next chat can remember
- Before closing, paste https://aiexpo.buildwithoracle.com/oracle/forward.md for a handoff; next time attach that handoff to a new chat (`/recap` itself runs only in Claude Code)

— AIExpo Oracle (Oracle AI), 2026-11-04

## Part 2 · skill `rrr`

<!-- file: skills/rrr/SKILL.md -->
### File: `skills/rrr/SKILL.md`

---
name: rrr
description: Create a session retrospective with an AI diary and reusable lessons. Supports foreground, background, and combined execution across compatible agent hosts.
argument-hint: "[--fg | --bg | --combo]"
---

# /rrr

> "Reflect to grow, document to remember."

Create a truthful session retrospective, record reusable learning, and append the
session-metrics row. Never invent timestamps or claim evidence that the active host
cannot provide.

## Mode router

Choose one execution mode:

```text
/rrr                              # default: foreground + session-clock timestamps
/rrr --light                      # fastest: timeline + summary + lesson only
/rrr --combo                      # foreground draft, then background evidence enrichment
/rrr --bg                         # full retrospective in the background
/rrr --fg                         # foreground, no session clock at all
```

`--fg`, `--bg`, and `--combo` are mutually exclusive. If more than one is supplied,
stop and report the valid syntax. **When none is supplied, use the default foreground
path** — synchronous, no background agent, but with real timestamps from the session
clock. `--light` composes with the foreground path.

| Mode | Required behavior |
|---|---|
| *(none)* | **Default.** Synchronous. Real times from the host's session clock (see [HOSTS.md](HOSTS.md)) plus git commit times. No background agent; timestamps only, never conversation content. |
| `--light` | The default path with only Timeline, Summary, Lesson, and Metrics. For quick checkpoints; skips Diary, Feedback, Blockers, Self-Audit. |
| `--combo` | Foreground artifact now, then background mining that enriches the same file with fuller evidence. Mark enrichment pending until it completes. |
| `--bg` | Mine the persisted host session and write asynchronously. Announce the destination and return without waiting. |
| `--fg` | Strict: current conversation context and repository evidence only. Do not run the session clock. Do not inspect persisted session transcripts, JSONL, rollout files, or session databases. Do not launch a hidden mining agent. |

### Why the default reads a session clock

A retrospective without a timeline cannot be audited. Git commit times alone leave a
research or browsing session with `Duration: unknown`.

The historical fix was worse: pre-2026-08-20 retros filled the gap with **estimated** times
marked `~`, back-filled from the known end time. They are recognisable by their impossible
regularity — `~04:11 ~04:12 ~04:13 …`, or neat five-minute steps — because real session
timestamps cluster unevenly (four events inside one minute, then nothing for twenty).

A **session clock** closes the gap without either cost. The contract asks only for
observed times — read timestamps, not content — so it stays cheap on any host. Claude
Code's reference implementation scans a 16MB transcript in ~50ms for a few hundred bytes of
context. That is why this is the default rather than `--combo`: no background agent, no
token burn, real times.

Each harness resolves the contract its own way. The skill states what it needs; it does not
dictate a mechanism that only one host could satisfy.

The ban stands: never emit an estimated timestamp, with or without a tilde. If the clock
reports `evidence: none` and no commits exist, say `unknown` — do not decorate the gap.

## Host capability contract

Before mining or delegation, read [HOSTS.md](HOSTS.md). Detect capabilities rather
than assuming Claude Code paths, Claude JSONL, a particular agent API, or a model name.

Public output should say **session mining**, not **JSONL mining**. A host adapter may
internally read JSONL, rollout files, or another supported source, but it must normalize
the result and preserve source attribution.

If background execution is unavailable:

- `--fg` is unaffected.
- `--bg` falls back to `--fg` and clearly reports that persisted mining was unavailable.
- `--combo` keeps the foreground artifact, marks session enrichment unavailable, and
  does not fabricate a completion notification.

## Oracle root detection

Run this before every `ψ/` write. Do not assume the current directory is the Oracle repo.

```bash
ORACLE_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -n "$ORACLE_ROOT" ] && { [ -f "$ORACLE_ROOT/CLAUDE.md" ] || [ -f "$ORACLE_ROOT/AGENTS.md" ]; } \
   && { [ -d "$ORACLE_ROOT/ψ" ] || [ -L "$ORACLE_ROOT/ψ" ]; }; then
  PSI="$ORACLE_ROOT/ψ"
elif { [ -f "$(pwd)/CLAUDE.md" ] || [ -f "$(pwd)/AGENTS.md" ]; } \
   && { [ -d "$(pwd)/ψ" ] || [ -L "$(pwd)/ψ" ]; }; then
  ORACLE_ROOT="$(pwd)"
  PSI="$ORACLE_ROOT/ψ"
else
  echo "⚠️ Not in an Oracle repo. Writing under the current repository."
  ORACLE_ROOT="${ORACLE_ROOT:-$(pwd)}"
  PSI="$ORACLE_ROOT/ψ"
fi

PSI_RESOLVED=$(readlink -f "$PSI" 2>/dev/null || printf '%s' "$PSI")
```

## Shared workflow

### 1. Gather repository evidence

All retro times and date-stamped paths use **GMT+7 (Asia/Bangkok)**. Pin it once so
every `date` call and git timestamp below renders in GMT+7 regardless of the host's
local zone:

```bash
export TZ='Asia/Bangkok'   # GMT+7 — retro timeline, header, and path stamps
```

Use the smallest commands that accurately describe this session:

```bash
date "+%H:%M %Z (%A %d %B %Y)"
git -C "$ORACLE_ROOT" status --short
git -C "$ORACLE_ROOT" log --oneline -10
git -C "$ORACLE_ROOT" diff --stat HEAD~5 2>/dev/null || true

# Verified commit timestamps in GMT+7. --date=format-local honors the TZ above.
git -C "$ORACLE_ROOT" log --since='18 hours ago' \
  --date=format-local:'%H:%M' --format='%ad — %s (%h)' --reverse
```

**Session clock — the default path's primary time source.** Ask the host for observed
times. *How* is the adapter's business; **what** is fixed by the SessionClock contract in
[HOSTS.md](HOSTS.md):

- [ ] times **observed**, never estimated or interpolated
- [ ] attributable to this session and repository, or `evidence: none`
- [ ] gap-aware, so an idle overnight is not counted as session time
- [ ] **beats** — the minutes that actually had activity — not a start/end span
- [ ] cheap: read timestamps, not content; if it would load the conversation into
      context, return `none` instead
- [ ] degrades honestly: no source → `evidence: none`, and that is a correct answer

Resolve it the way your harness allows — Claude Code has a reference implementation
(`scripts/session-clock.py`, ~50ms on a 16MB transcript); Codex should use its own rollout
or session metadata; an unknown host returns `none`. Do not run one host's implementation
against another host's layout on the assumption that it matches.

Place rows on beats. Never interpolate a time between two beats. On `evidence: none`, fall
back to commit times, then to untimed ordered bullets.

Skip the session clock entirely under `--fg`.

Repository evidence is allowed in every mode. Persisted **agent-session** evidence is
for `--bg` and `--combo` only. Commit timestamps are repository evidence, not session
mining — a `--fg` retro may and should use them to build a real timeline.

### 2. Resolve artifact paths

```bash
# TZ='Asia/Bangkok' (GMT+7) was exported in step 1, so these stamps are Bangkok-local.
DATE_PATH=$(date +%Y-%m/%d)
TODAY=$(date +%Y-%m-%d)
HHMM=$(date +%H.%M)
mkdir -p "$PSI/memory/retrospectives/$DATE_PATH" "$PSI/memory/learnings"
```

Write:

- retrospective: `$PSI/memory/retrospectives/$DATE_PATH/${HHMM}_${SLUG}.md`
- lesson: `$PSI/memory/learnings/${TODAY}_${SLUG}.md`
- metrics: `$PSI/memory/learnings/session-metrics.md`

### 3. Execute the selected mode

#### Background (`--bg`)

Resolve every path and capability before delegation. Give one background writer the
current context summary, repository evidence, normalized session evidence when
available, destination paths, template requirements, and the anti-rationalization
rules. Use the active host's model routing; never require a named vendor model.

Return immediately with the resolved absolute destination. If the host cannot keep work
alive after returning, use the documented foreground fallback instead of pretending the
task remains active.

#### Light (`--light`)

The default path with the reflective sections dropped — for a quick checkpoint mid-work
where a full retro is not worth the tokens. Write **only**:

- header metadata (with real `Start / End` and `Duration` from the session clock)
- `## Timeline`
- `## Session Summary` (2–3 sentences)
- `## Lessons Learned` (or an evidence-backed `none`)
- the metrics row

Skip Diary, What Went Well / Could Improve, Blockers, Honest Feedback, Next Steps, Related
Resources, and Self-Audit. Note `mode: light` in the evidence line so a reader knows the
reflection was intentionally omitted rather than forgotten. The silent validation gate still
applies to what *is* written.

#### Foreground (`--fg`)

Write the artifact synchronously using current conversation context and repository
evidence only. Build the Timeline from the **verified GMT+7 commit timestamps** gathered
in step 1 — real `HH:MM` rows, not `unknown`. Set the header `Start / End` to the first
and last commit time (or the current clock when there are no commits this session), and
`Duration` to their span. Only events with no timestamped evidence at all fall back to
ordered untimed bullets. State `Persisted session mining: disabled by --fg` in the
evidence note.

#### Combined (`--combo`)

First write a complete, useful context-based retrospective synchronously. Its Timeline
may contain ordered untimed entries and must include `Session enrichment: pending`.
Then launch one background miner/writer using the host adapter. It updates the same file
atomically: merge verified timestamps/evidence, replace the pending marker with the
source and completion status, and preserve user edits made after the initial write.

Use `--combo` when you want more than times — full transcript evidence, quoted decisions,
tool-level detail. For times alone the default path is faster and cheaper. If the host
cannot mine, replace the pending marker with `session enrichment unavailable` and leave the
timeline as the session clock produced it — never fill it with estimates.

### 4. Retrospective content

Use [TEMPLATE.md](TEMPLATE.md) for every mode. It preserves the detailed retrospective
shape: session metadata, summary, timeline, technical details, key changes, architecture
decisions, AI Diary, wins, improvements, blockers, Honest Feedback, lessons, next steps,
related resources, and Self-Audit — the written retro ends at Self-Audit.

Before saving, silently verify the retro against TEMPLATE.md's **validation gate**. It is
an internal quality check — run it, fix what fails, and **never write the checklist into
the retrospective file**.

Small sessions may have short sections or an evidence-backed `none`; they must not drop
required reflection sections, and must still pass the silent validation gate.

### 5. Timeline rules

1. Never invent timestamps. A tilde does not license a guess — `~04:12` is a fabricated
   timestamp wearing a disclaimer. Evenly spaced rows (every 1 or 5 minutes) are the
   signature of back-filling from the end time; real ones cluster unevenly.
2. All times render in **GMT+7 (Asia/Bangkok)** — the `TZ` exported in step 1 covers
   `date` and `git --date=format-local` alike. Label rows plainly as `HH:MM` (GMT+7).
3. Prefer verified times from these sources, in order: **session clock beats**
   (host adapter, default path) → normalized session evidence
   (`--bg`/`--combo`) → git commit timestamps (any mode) → the current clock for the
   closing entry. Never interpolate a row time between two beats.
4. Same-day sessions show the date once and `HH:MM` in rows.
5. Multi-day sessions group rows under `### YYYY-MM-DD`.
6. Only fall back to ordered untimed bullets when NO timestamped evidence exists at all —
   not merely because session mining is off. If any commit landed this session, the
   timeline has real times.
7. Record the evidence source: session-clock, Claude adapter, Codex adapter,
   git-commit-times, context-only, or unknown.

### 6. Lesson and metrics

Write a lesson only when it transfers to another project:

```yaml
---
pattern: <generalizable lesson in one line>
date: <today>
source: rrr: <repo>
concepts: [<tags>]
---
```

Create the metrics file when absent:

```markdown
# Oracle Session Metrics

| when | session | done | stuck | win | friction | error |
|---|---|---|---|---|---|---|
```

Append exactly one row for every run. Use `unknown` when the host cannot provide a
session ID. Never skip a trivial session; record `trivial` where appropriate.

Review the last seven metrics rows. If a theme appears at least three times in either
`friction` or `error`, surface a recurring-pattern section in the retrospective. Do not
open an issue automatically.


### 7. Save and announce

Do not `git add ψ/`; it may resolve to a shared vault.

Announce absolute paths only:

```text
📝 Retrospective:  <absolute path>
💡 Lesson learned: <absolute path, or "not created — no generalizable lesson">
📊 Metrics row:    <absolute path>
```

## Rules

- Default execution mode is `--fg`.
- `--fg` never mines persisted session data and never launches a hidden miner.
- `--bg` and `--combo` are the only modes allowed to mine persisted session data.
- `--combo` is the only foreground-plus-background-enrichment mode.
- Never hard-code Claude storage, JSONL schema, agent APIs, team APIs, or model names in
  the shared flow; isolate host details in [HOSTS.md](HOSTS.md).
- Never invent timestamps, session IDs, commits, files, or completed background work.
- Do not create coordinated teams or multi-agent analysis trees for `/rrr`.
- Keep vault writes outside git staging.

<!-- file: skills/rrr/HOSTS.md -->
### File: `skills/rrr/HOSTS.md`

# RRR Host Capability Guide

Use this guide only for `/rrr --bg` or `/rrr --combo`. `/rrr --fg` deliberately does
not inspect persisted session data.

## Capability detection

Detect behavior from available host tools and readable sources; do not infer it only
from which installation directory contains the skill.

Record these capabilities:

```text
HostCapabilities {
  host: claude | codex | other
  background_agents: supported | unavailable
  persisted_session: supported | unavailable
  session_source?: absolute path or host-native handle
}
```

Do not expose raw conversation contents, credentials, secrets, or unrelated sessions in
the retrospective.

## Normalized evidence

Every adapter returns the same conceptual record:

```text
SessionEvidence {
  session_id?: string
  started_at?: timestamp
  ended_at?: timestamp
  events: [{ timestamp?: timestamp, role, summary }]
  source: claude | codex | context-only | unknown
}
```

Only retain events attributable to the current repository/session. Summaries should be
short and must not reproduce secrets. Preserve timestamps exactly, converting only for
display in the configured timezone.

## Session clock — the contract every host must satisfy

`/rrr` needs times, not a transcript. Any host that can attribute *when* things happened
should return a **SessionClock**; how it does so is that adapter's business.

```text
SessionClock {
  evidence: <adapter name> | none      # 'none' is a valid, honest answer
  segments: [{ start, end, minutes, beats: [HH:MM, ...] }]
}
```

Checklist an adapter must meet — satisfy these however the host allows:

- [ ] **Times are observed, never derived.** No estimating, no interpolating between known
      points, no tilde-hedged guesses.
- [ ] **Attributable.** Only this session, in this repository. If attribution is ambiguous,
      return `none` rather than the wrong conversation.
- [ ] **Gap-aware.** Split on idle gaps (60 min is a sane default) so an overnight pause is
      not reported as a nineteen-hour session.
- [ ] **Beats, not spans.** Report the minutes that actually had activity, so the retro can
      place rows on real events instead of spreading them evenly.
- [ ] **Cheap.** Read timestamps, not content. If obtaining times means loading the whole
      conversation into context, the adapter is too expensive — return `none` instead.
- [ ] **Degrades honestly.** No source → `evidence: none`, exit success. `/rrr` then falls
      back to git commit times, then to untimed ordered bullets.

`none` is not a failure. A retro that says `Duration: unknown` is correct; one that invents
`~04:12` is not.

## Claude Code adapter

When Claude Code's project-session JSONL is present and attributable to the current
repository, parse it as an internal adapter detail. Verify each record before reading
fields; malformed lines are skipped and reported. Do not copy the Claude path or schema
into the shared `/rrr` workflow.

Use Claude's available background-agent or team facility without requiring a fixed model
tier. If the facility is unavailable, follow the shared fallback contract.

**Session clock reference implementation.** `scripts/session-clock.py` satisfies the
contract above for this host: it substring-scans the project-session JSONL for timestamp
fields only — bodies are never parsed — so a 16MB transcript costs ~50ms and a few hundred
bytes. It is *an* implementation, not the mechanism: the Claude paths and `.jsonl` schema
live inside it precisely so they stay out of the shared flow.

Other hosts may reuse it by passing `--file <transcript>` if their artifact is
newline-delimited with ISO `"timestamp":"..."` fields — otherwise write your own; the
contract is what matters.

## Codex adapter

Prefer a host-provided session handle or native session context. If Codex exposes a
persisted rollout/session artifact, use it only after confirming that it belongs to the
current session and repository.

For the session clock: derive times from whatever Codex actually exposes — rollout file
mtimes, a session API, native turn metadata. Do not invoke the Claude reference script
against a Codex layout on the assumption that it matches. If no attributable time source
exists, return `evidence: none`; that is the correct answer, not a shortfall. Treat its location and schema as version-dependent; do
not assume Claude's directory layout or message schema.

Use Codex native role routing for delegated work when available. Do not imitate Claude
tool syntax in Codex instructions. If asynchronous work cannot survive the parent turn,
report background execution as unavailable and use the documented fallback.

## Unknown hosts

Use current context and repository evidence. Set the evidence source to `context-only`
or `unknown`, session ID to `unknown`, and disclose that persisted-session enrichment was
unavailable. Never search arbitrary home-directory logs hoping to find a transcript.

Session clock: `evidence: none`. Git commit times remain available in every mode and are
often enough on their own.

## Failure behavior

- Missing or unreadable session source: continue without it and disclose the limitation.
- Ambiguous repository/session attribution: reject the source rather than mining the
  wrong conversation.
- Malformed event: skip it, count it, and do not invent replacement data.
- Background launch failure: do the documented foreground fallback.
- Partial `--combo` enrichment: preserve the foreground artifact and change its marker
  from `pending` to `unavailable` or `partial`, including the reason.

All fallbacks are explicit. A missing capability must never look like successful mining
or a still-running background job.

<!-- file: skills/rrr/TEMPLATE.md -->
### File: `skills/rrr/TEMPLATE.md`

# RRR Retrospective Template

Use this complete structure for every `/rrr` mode. Keep sections concise for small
sessions, but do not omit required reflection or verification sections.

```markdown
# Session Retrospective

**Session Date**: YYYY-MM-DD
**Start / End**: HH:MM–HH:MM GMT+7
**Duration**: ~X minutes
**Primary Focus**: <brief description>
**Session Type**: Feature Development | Bug Fix | Research | Refactoring | Maintenance
**Repository / Branch**: <repo> / <branch>
**Current Issue**: #N or none
**Current PR**: #N or none
**Session**: <host session ID or unknown>
**Evidence Source**: live-session | Claude adapter | Codex adapter | git-commit-times | unknown

## Session Summary

<Two or three sentences describing the goal, outcome, and current state.>

## Timeline

<Real `HH:MM` (GMT+7) rows. Times come from session mining (`--bg`/`--combo`) or, in
any mode including `--fg`, from verified git commit timestamps. Only fall back to ordered
untimed bullets when no timestamped evidence exists at all. Never estimate times.>

- HH:MM — <event> (`<commit>`)

## Technical Details

### Files Modified

<Files grouped by purpose, including uncommitted changes.>

### Key Code Changes

<What changed and why. Name important symbols or modules.>

### Architecture Decisions

<Decision, alternatives considered, rationale, and consequence. Write `none` when the
session made no architectural decision.>

## 📝 AI Diary

<At least 150 words in first person. Cover the initial understanding, assumptions, how
the approach evolved, confusion or clarity, surprises, and important decisions. Include
one `[→ AGENT DECISION]` line naming a decision the agent made wrong.>

## What Went Well

<Concrete successes with evidence. Do not use vague progress claims.>

## What Could Improve

<Specific changes that would make a similar session more effective.>

## Blockers & Resolutions

<For each blocker: symptom, evidence, attempts, resolution, and remaining risk. Write
`none` only when genuinely absent.>

## 💭 Honest Feedback

<At least 100 words. Give exactly three session-specific friction points covering process,
tools, communication, or scope. Keep generalizable rules for Lessons Learned.>

## Lessons Learned

- **Pattern**: <transferable rule and why it matters>
- **Mistake**: <what to avoid on another project>
- **Discovery**: <new reusable knowledge>

<Use only applicable categories; do not manufacture a lesson.>

## Next Steps

- [ ] <specific action with enough context to execute>

## Related Resources

- Issue: <URL or none>
- PR: <URL or none>
- Commits: <hashes or none>
- Retrospective: <absolute path>
- Lesson: <absolute path or none>

## 🔍 Self-Audit

- shipped: <N items — commit hash or file path for each, or "none shipped">
- blocked: <N items — specific reason for each, or "none blocked">
- uncomfortable truth: [→ AGENT DECISION] <one decision the agent made wrong>
- friction: <N points> (operational: <list> | strategic: <list>)
- next steps: <N — each actionable without a follow-up question>
- rationalizations caught: <N — name them, or "none">
```

## Validation gate — verify silently, never write it into the retro

Before saving, confirm every item below holds. This is an **internal quality gate**:
check it in your reasoning, fix whatever fails, then write the file. **Do NOT copy this
checklist into the retrospective** — the saved retro ends at Self-Audit and contains no
checklist section.

- [ ] Metadata reflects the actual session and repository.
- [ ] Summary distinguishes shipped, unfinished, and blocked work.
- [ ] Timeline uses verified times or clearly untimed ordered events.
- [ ] Technical details match git and file evidence.
- [ ] AI Diary is first-person, substantive, and includes `[→ AGENT DECISION]`.
- [ ] Honest Feedback is substantive and contains exactly three friction points.
- [ ] Lessons are transferable rather than session-only observations.
- [ ] Next steps are concrete and executable.
- [ ] Links and paths resolve, or are explicitly marked unavailable.

If an item fails, revise the retro before writing — do not record the failure in the file.

## Repository integration boundaries

The gist-inspired structure is the content contract, not permission to mutate unrelated
project files or GitHub state.

- Write under the detected Oracle vault paths from `SKILL.md`.
- Do not append lessons to `CLAUDE.md` or `AGENTS.md`; use the dedicated lesson artifact.
- Do not stage or commit `ψ/`.
- Do not comment on issues or PRs unless the user separately requests that external action.

<!-- file: skills/rrr/scripts/session-clock.py -->
### File: `skills/rrr/scripts/session-clock.py`

```python
#!/usr/bin/env python3
"""Session clock — the Claude Code adapter. One implementation, not the mechanism.

Satisfies the SessionClock contract in ../HOSTS.md for hosts that store
newline-delimited transcripts with ISO `"timestamp":"..."` fields. Codex and other
harnesses should resolve the same contract from whatever they actually expose
(rollout metadata, a session API) rather than running this against a layout it was
not written for. `evidence: none` is always a valid answer.

Reads ONLY the `timestamp` field out of the host's session transcript. Message
bodies are never parsed or returned, so a 3MB transcript costs a few hundred
bytes of context instead of blowing the window. No background agent needed.

Segments on idle gaps so an overnight pause is not reported as a 19-hour
session, and emits activity beats (minutes that actually had events) rather
than evenly spaced guesses.

    session-clock.py [--gap MIN] [--beats N] [--tz OFFSET] [--all]

Exit 0 with `evidence: none` when no transcript is found — /rrr must degrade to
untimed bullets, never to invented times.
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys

TS_KEY = '"timestamp":"'


def find_transcript(cwd: str) -> str | None:
    """Locate the newest transcript for this working directory."""
    encoded = "-" + cwd.lstrip("/").replace("/", "-").replace(".", "-")
    base = os.path.join(os.path.expanduser("~/.claude/projects"), encoded)
    files = sorted(glob.glob(os.path.join(base, "*.jsonl")), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


def read_timestamps(path: str) -> list[str]:
    """Substring-scan for timestamps. Never json.loads a whole line: the bodies
    are the expensive part and we do not want them."""
    out = []
    with open(path, "r", errors="replace") as fh:
        for line in fh:
            i = line.find(TS_KEY)
            if i >= 0:
                out.append(line[i + len(TS_KEY): i + len(TS_KEY) + 24])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=int, default=60, help="idle minutes that split a segment")
    ap.add_argument("--beats", type=int, default=12, help="max activity beats to print")
    ap.add_argument("--tz", type=float, default=7.0, help="display offset, default GMT+7")
    ap.add_argument("--all", action="store_true", help="report every segment, not just the current one")
    ap.add_argument("--file", help="explicit transcript path")
    args = ap.parse_args()

    path = args.file or find_transcript(os.getcwd())
    if not path or not os.path.exists(path):
        print("evidence: none")
        return 0

    zone = dt.timezone(dt.timedelta(hours=args.tz))
    stamps = []
    for raw in read_timestamps(path):
        try:
            stamps.append(dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(zone))
        except ValueError:
            continue
    if not stamps:
        print("evidence: none")
        return 0
    stamps.sort()

    # split on idle gaps so an overnight pause is not counted as session time
    segments, current = [], [stamps[0]]
    for prev, now in zip(stamps, stamps[1:]):
        if (now - prev).total_seconds() > args.gap * 60:
            segments.append(current)
            current = []
        current.append(now)
    segments.append(current)

    label = f"GMT{args.tz:+g}".replace(".0", "")
    chosen = segments if args.all else segments[-1:]

    print(f"evidence: session-clock ({os.path.basename(path)[:8]})")
    print(f"events: {len(stamps)}  segments: {len(segments)}  gap-threshold: {args.gap}m")
    for seg in chosen:
        start, end = seg[0], seg[-1]
        mins = int((end - start).total_seconds() // 60)
        print(f"\nsegment {start:%Y-%m-%d} {start:%H:%M}–{end:%H:%M} {label}  ({mins} min, {len(seg)} events)")
        beats = sorted({s.strftime("%H:%M") for s in seg})
        shown = beats[: args.beats]
        print("  beats: " + " ".join(shown) + (f"  …+{len(beats) - len(shown)} more" if len(beats) > len(shown) else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
