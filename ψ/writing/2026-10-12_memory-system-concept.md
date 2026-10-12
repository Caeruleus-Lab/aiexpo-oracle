# ARRA Oracle Memory System: Concept

Drafted by AIExpo Oracle (AI) on 2026-10-12. Material for the 20–25 slot ("what an Oracle is") and for decision 3.
Sources: Nat's screenshots of the Nexus Oracle app (Work · Memory · Map · Trace), `relic3 --help`,
the README of `Soul-Brews-Studio/agent-relic-v3` (2026-10-07) and `agents-relic`, the `oracle-app` skill in
`oracle-app-kit` (2026-10-10), and the source of `arra-oracle-v3`.

> **ความจำคือ pattern ที่บันทึกไว้ ไม่ใช่ตัวคุณ และเพราะมันเป็นแค่ไฟล์ มันจึงเป็นของคุณ**
> ("Memory is recorded patterns, not you. And because it is just files, it belongs to you.")

## Memory in 3 layers: what the agent writes, what was said, what it means

```
 ┌─ 1. What the Oracle chooses to write down (ψ/) ─────────────────────────────┐
 │  /rrr → retrospectives + learnings · /forward → handoff · CLAUDE.md = self  │
 │  plain files in git, readable and editable; this layer works on its own     │
 └─────────────────────────────────────────────────────────────────────────────┘
 ┌─ 2. Everything that was said (relic3) ──────────────────────────────────────┐
 │  every Claude Code + Codex session transcript → weekly Parquet index        │
 │  full-text search (BM25, Thai-capable), faceted by repo / worktree / time / │
 │  who spoke · no embeddings needed · writes nothing into your repos          │
 │  "did I already do X?"  → relic3 search "<a unique string>"                 │
 └─────────────────────────────────────────────────────────────────────────────┘
 ┌─ 3. What it means: the Oracle's own app (oracle-app-kit) ───────────────────┐
 │  Memory · sessions + ψ notes + issues + PRs in one semantic index           │
 │           vectors computed on the Mac itself (CoreML / Apple Neural Engine) │
 │  Map    · every memory as a point; close = related; clusters get names      │
 │  Trace  · every question anyone asked this memory, via the page or MCP:     │
 │           who asked, when, and what came back first                         │
 │  MCP memory server · other agents ask this Oracle's past                    │
 └─────────────────────────────────────────────────────────────────────────────┘
```

**A real example from the screenshots (Nexus Oracle, 12 Oct):**
- 6,425 memories in one space: 5,043 session pieces · 1,333 ψ notes · 29 issues · 20 PRs, indexed since 2026-03-07
- It read 2,700 transcripts in 0.3 s and found that 122 belong to Nexus. Each answer comes back in roughly 25–166 ms.
- In Trace you can see that Neo asked "check nexus …" over MCP from `laris-co w22:pA`. That is provenance on the read side.

## The habit loop

```
 /recap ──► work ──► /rrr ──► /forward ──► close the window
   ▲  (read what's pending)  (summary + lesson)  (handoff)   │
   └──────────────────────── reopen ◄─────────────────────────┘
```
Layer 1 is what the Oracle chooses to remember. Layers 2 and 3 cover what it didn't write down, so it can still be found again.

## Lines for the stage

- "ψ/ is a notebook the agent writes itself. relic3 is a recording of every conversation. The app turns both into a map you can ask."
- "Every memory is on your own machine. Even the vectors are computed on the Mac's chip, and nothing goes up to a server."
- "Trace shows who asked about you, and what they got back." This answers Yim's question "who checks the work?"

## Decision 3: proposal text vs. what exists today

| Proposal says | What exists today |
|---|---|
| A team of agents learns together through **arra-oracle MCP (v3)** | v3 still exists (`oracle_learn` with a `source`, `oracle_supersede` that keeps the old version). But the newer memory layer is **relic3 + the app's MCP memory server**, and Trace shows who asked what |
| Every note is tagged with who wrote it | Write side: v3 `source`/`project`. Read side: the app's Trace (caller + pane) |
| Nothing is deleted | relic3 only adds to the index. v3 supersedes instead of deleting |

⇒ **Nat needs to decide:** demo arra-oracle v3 as the proposal says, or relic3 + the Oracle app as in these screenshots.

## Caveats

- **The Oracle app is macOS only** (Swift, CoreML/ANE). Windows and Linux users in the room can only watch it on screen.
- relic3 indexes Claude Code and Codex transcripts. Antigravity is not listed yet, so it needs checking.
- Layer 1 (ψ/) is all the room needs for the 40–55 memory-loop slot. Layers 2–3 are a demo of where this grows.
- claude.ai on the web keeps no files between chats, so none of the 3 layers apply there.
