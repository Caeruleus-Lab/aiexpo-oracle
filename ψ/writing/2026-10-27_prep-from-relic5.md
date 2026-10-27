# How to prep "ARRA Oracle & Multi-Agent Workflow": everything relic5 holds

Drafted by AIExpo Oracle (AI), 2026-10-27, from relic5 (sessions, ψ notes, Discord, all machines). Each item names its source so it can be opened again.
Event: Fri 6 Nov 2026, **15:05–16:10**, Builder Stage, Challenger Hall (official poster, 27 Oct). 10 days from today.

## 1. What the organizer already expects (LINE Masterclass, summarized by Athena + Pulse on 17 Oct)

- Title TH: "ARRA Oracle และเวิร์กโฟลว์การทำงานแบบ Multi-Agent". **Subtitle: "AI ที่จำงานของคุณได้ และความจำนั้นเป็นของคุณ"** (AI that remembers your work, and the memory is yours).
- Nat leads; คุณยิ้ม (FlowAccount / Rikyu Labs) supports.
- **4 agreed talking points**: memory that carries across days · no lock-in to one AI vendor · build an Oracle hands-on in the room · grow from one agent to a team.
- **Attendees bring a laptop with Claude Code installed.**
- **Attendees hand in homework by event day to get the e-certificate.** Nat sent his signature 16 Oct (vectorized in a Codex session that day).
- Gaps Pulse flagged on 17 Oct: **no homework brief has gone to the organizer yet**; คุณยิ้ม's signature not seen in the chat.
  Sources: athena-oracle session 7160430f (17 Oct 16:07), pulse-oracle session 3a25e13e (17 Oct 16:12), pulse-oracle 923951fc (20 Oct).

## 2. Nat's own teaching method (vault note, 5 Jan 2026)

`Nat-s-Agents ψ/memory/learnings/2026-01-05_workshop-teach-necessity-not-features.md`
- **Teach through necessity, not features.** Sell the outcome ("an AI that remembers"), let people feel the problem, then the pattern appears as the answer.
- Plan the breaking point; don't rescue too early; write the emotional arc, not just "topic X at minute Y".
- Quote: *"The best teachers don't teach the answer. They engineer the question."*
- For a 65-minute slot this means: open a session, work, **close the window**, open again: it forgot (pain). Then `/awaken` + ψ/ + `/rrr`/`/recap`: it remembers (answer).

## 3. Past workshops and what they taught

| When | Workshop | Lesson for 6 Nov |
|---|---|---|
| 4–5 Jan 2026 | Thirdpint, "Build Your Oracle" | Outcome-first framing (above) |
| 28 Feb–1 Mar 2026 | PSRU, Two Rivers Oracle | 7 student Oracles born; Antigravity free worked; install retries ("tried 6 times"); Thai `gh issue` failures. Already mapped in `ψ/memory/learnings/2026-10-12_two-rivers-workshop-lessons.md` |
| 18 Mar 2026 | Mother Oracle, "Oracles Build the Oracle" | 25+ signed up but "don't know how". 3 steps: everyone `/awaken --fast` (5 min each; non-Claude users on Codex/OpenCode via oracle-skills-cli) → Oracles talk to each other → Oracles improve oracle-skills-cli. Use an experienced attendee as co-guide |
| 24 May 2026 | CCC Academy, The Quarter Ratchayothin, ~20 people, 13:30–17:10 | The Oracle answered Discord live, voice replies, `/trio` demo, Federation Map, `/dig` across 1,830 sessions. Lessons: **"prompt" means a copyable code block**, not an AI diary; preinstall deps (Pillow took 3 tries live); run demos from the repo root |
| 26 Jul 2026 | "ARRA Oracle Second Brain for Research" with AJ ฝน | Nat: "อย่าให้ขายหน้า": test the demo end to end and rehearse ~20 rounds with the partner's Oracle before the day |
| 13 Sep 2026 | neo-oracle multi-agent lesson script | `neo-oracle/ψ/writing/2026-09-13_multi-agent-workflow-lesson.md`: open with the pain, not numbers; demo = 1 agent vs 3 haiku agents in parallel → main thread compiles; prepared Q&A; checklist says **the demo was never actually run: rehearse and capture screenshots as a fallback** |

## 4. What changed in Nat's own stack since the proposal (affects the demo)

- **relic3 is frozen (15 Oct). relic5 replaced it (23 Oct)**: the hub on white, every machine's Claude Code + Codex history, Thai-aware search, semantic search, MCP. The memory concept note (`2026-10-12_memory-system-concept.md`) still says relic3: update before slides.
- **ARRA Memory** was built from scratch on 20 Oct (one Codex session, 29 issues closed, evening demo) plus a static-JSON MCP connector for claude.ai and a Thai booklet. Possible "where it grows" demo, and possibly the web-only path for free attendees.
- **Discord fleet** (laris-co-team, 17 Oct): oracles answer in threads; good live "team of agents" picture (as in May).
- `/voice-map` (27 Oct): recording → transcript → summary → map. Could record the session itself for the follow-up.

## 5. Media already made (local drafts, never posted)

- FB cover 1200×630 and square 1080 (pigment, media-team PR #2, 12 Oct), principles card, 48-s teaser storyboard (iris, `~/Downloads/iris-draft-expo-2026-teaser.mp4`).
- They still say `วันที่: TODO(Nat)` (Thor, 21 Oct). Herald won't post until the date is filled. **Now known: 6 Nov 15:05–16:10.**
- Official poster + title slide: `ψ/writing/promo/`, `ψ/writing/slides/01-title.png`.

## 6. Prep checklist (10 days)

- [ ] **Homework brief to the organizer** (needed for the e-certificate). Suggest: clone the repo + run `/awaken --fast` + one `/rrr`, submit the repo link. Matches คุณยิ้ม's prerequisite idea.
- [ ] Pre-event install guide for attendees: Claude Code (Pro) + free fallback (Codex on ChatGPT Free, Antigravity) + claude.ai web upload path. One page.
- [ ] Rehearse `/awaken --fast` → close window → `/recap` on a **clean** machine/account, Claude + Codex + Antigravity. Time each.
- [ ] Rehearse the multi-agent demo (1 agent vs 3 in parallel). Capture screenshots as a fallback.
- [ ] Decide the "special" demo: relic5 search, Oracle app (Mac only), or ARRA Memory. Update the memory concept note from relic3 to relic5.
- [ ] Timing on the new clock: 15:05–15:25 คุณยิ้ม, 15:25–16:05 Nat, 5 min Q&A/buffer (if the 20/40 split stays).
- [ ] Copyable prompts on one slide/page (the May lesson).
- [ ] Fill the date into the media drafts; Nat decides if Herald posts.
- [ ] Ask คุณยิ้ม for the certificate signature if the organizer still needs it.
