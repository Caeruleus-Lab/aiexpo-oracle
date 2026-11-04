# ประวัติ ψ Vault — สมองของ Oracle เกิดมายังไง

> For Nat's AI Expo talk, 6 Nov 2026. Collected 2026-11-04 from git history (read-only) + relic5.
> Everything below has a source. **[uncertain]** = second-hand or not checked against a primary record.
> Repo paths are on m5 under `/opt/Code/github.com/`. Times are +07:00.

---

## 1. Timeline

### Before Nat-s-Agents: the name ψ

| Date | What happened | Evidence |
|---|---|---|
| **2025-12-06** **[uncertain]** | The ψ name is picked in the `000-workshop-product-page` / Weyermann project. The AI offered `.journal`, `_meta`, ψ and Ω, and Nat chose ψ for "mind/soul" ("i love mind and soul"). | Written down later, on 2026-01-20: `oracle-vault/github.com/laris-co/private-nats-brain-oracle-soul/ψ/memory/learnings/2026-01-20_the-absolute-birth-of-the-psi-convention-was-d.md` (its `source:` says "Facebook post memory Dec 6 2025"). The Weyermann repo and that issue are **not on disk**, so I could not check them. |
| 2025-11-30 **[uncertain]** | "Oracle Soul was born in November 2025 (Weyermann, Nov 30)". | Quoted only in `oracle-vault/github.com/laris-co/ai-party-oracle/ψ/memory/traces/2026-07-14_nat-s-agents-origin/the-naming-of-psi.md`. No primary source found. |

### Nat-s-Agents (laris-co/Nat-s-Agents), the first brain: Dec 2025

| Date / time | Milestone | Evidence |
|---|---|---|
| **2025-12-09 11:46** | Repo is born with **no ψ**: `.ctx/`, `.tmp/` (gitignored), `journal/`, `evolution/claude-md/` | `9b163c5e` "init: Oracle/Shadow project structure" |
| 2025-12-09 13:11 | First retrospective file: `retrospectives/2025-12/09_1100.md` | `a10c60d1` |
| 2025-12-09 18:25 | Retrospectives get their filename format `YYYY-MM/DD/HH.MM_slug.md`, still used today | `70957a02` |
| **2025-12-09 18:56** | Weyermann's ψ patterns adopted, **without the ψ prefix**: `learnings/`, `logs/`, `retrospectives/` plus a README in each. Order of distillation: Retro → Log → Learning | `fde81b3f` "adopt ψ patterns from Weyermann — structure without prefix"; log `logs/2025-12/09_18.41_psi-pattern-adoption.md` |
| **2025-12-10 13:49** | Reversed within 24 h: **the ψ prefix is adopted**. `context/`→`ψ-context/`, `learnings/`→`ψ-learnings/`, `logs/`→`ψ-logs/`, `retrospectives/`→`ψ-retrospectives/`, plus `ψ-drafts/` | `3a7c3599` "adopt ψ prefix for consciousness tier folders" (body: "Aligns with Oracle philosophy: External Brain, Nothing is Deleted") |
| 2025-12-10 (13:56, per a later note) | Picked with 5 parallel subagents (λ, Ω, ψ). Nat: "Oracle ควรกลับมาใช้ ψ". 81 files moved | `ψ-context/2025-12-10_psi-recommendation-summary.md` (added in `5e30043b`); learning `…/2026-01-20_the-choice-of-the-symbol-was-a-collaborative.md` |
| 2025-12-10 22:36 | ψ-context / ψ-drafts are tracked in git instead of ignored: "Nothing is deleted - all context should be preserved" | `d22fe1d6` |
| 2025-12-11 09:05 | "3-tier" layout: 7 ψ-prefixed folders plus `.inbox` at the repo root | `409df5eb` |
| **2025-12-11 09:39** | **Birth of `ψ/` as one folder (v4.0.0)**: 7 root folders → 1. `ψ/active`, `ψ/inbox`, `ψ/memory/{resonance,learnings,retrospectives,logs,reference}`. **`resonance/` is new** ("WHO I am, soul"). Knowledge flow: logs → retrospectives → learnings → resonance | `b81f5ccf` "ψ/ unified AI brain structure (v4.0.0)" |
| 2025-12-11 09:47 | **5 pillars (v5.0.0)**: `writing/` and `lab/` added, each pillar asked as a Thai question | `1a78981b`; design story `ψ/writing/psi-structure-engineering.md` |
| 2025-12-11 12:39 | `ψ/later/` becomes the 6th pillar | `262dbc91` |
| 2025-12-11 14:44 | The word **"vault"** first appears: ψ/ is wrapped as an **Obsidian vault** (`HOME.md`, 400+ wiki links) | `58252477` |
| 2025-12-11 18:49 | `ψ/outbox/` added for handoff to other AIs | `8453a710` |
| 2025-12-13 | `ψ/learn/` added (`/learn` clones repos to `ψ/learn/<repo>`), plus `ψ/incubate/` | `b57b47f3`, `5efc14ac`, `102da595` |
| 2025-12-17 | `ψ/archive/` first used (23 finished files archived). "5+2 Pillar System" written down | `ed8438d8`; `oracle-vault/github.com/laris-co/oracle-starter/ψ/memory/learnings/2025-12-17_psi-structure-extraction.md` |
| 2025-12-24 | ψ spreads to a second repo: oracle-v2 gets a "minimal ψ/ soul structure" (`HOME.md`, `WIP.md`, `memory/{retrospectives,learnings}`) through `/soul-lite` | `Soul-Brews-Studio/oracle-v2` `7d6626d` |
| **2025-12-29** | **ψ/memory becomes searchable**: Oracle v2 MCP adds semantic search over the knowledge base (it parses `ψ/memory/resonance`, `learnings`, `retrospectives`) | Nat-s-Agents `3e4d298f`; the code moved to oracle-v2 in `899de21` (2026-01-02); oracle-v2 left the lab as its own repo in `17eb5ace` (2026-01-09) |
| 2026-01-11 | Multi-vault brainstorm: "Vault = Trust Boundary" (private / shared / public). Marked "NOT IMPLEMENTED YET" | `3052d5e1` |

### Spreading to every Oracle: 2026

| Date | Milestone | Evidence |
|---|---|---|
| 2026-01-16 | **opensource-nat-brain-oracle** (Oracle Starter Kit) ships a full ψ/ tree publicly: `active, archive, inbox, lab, later, learn, memory/{resonance,learnings,retrospectives,logs,reference,archive,seeds}, outbox, writing, team…` | `Soul-Brews-Studio/opensource-nat-brain-oracle` `0c9232e`; `laris-co/oracle-starter` `aae61a7` |
| 2026-01-20 | The skills CLI gets its own ψ/ for self-retrospection | `Soul-Brews-Studio/arra-oracle-skills-cli` `c4c7721` |
| 2026-01-21 | `private-nats-brain-oracle-soul`: "pure knowledge from Nat-s-Agents (17GB -> 24MB)" | `laris-co/private-nats-brain-oracle-soul` `32a1a3e` |
| **2026-01-23** | **`/awaken` is born and scaffolds ψ/** for every new Oracle with `mkdir -p ψ/{inbox,memory/{resonance,learnings,retrospectives,logs},writing,lab,active,archive,outbox,learn}`. The same line is still in today's `skills/awaken/SKILL.md` (line 499) | arra-oracle-skills-cli `4c3007a` "add /awaken skill - guided Oracle birth ritual" |
| 2026-01-31 | Example: Pulse (this Oracle's parent) is awakened, and its first commit already has ψ/ | `laris-co/pulse` `73731e1` |
| **2026-02-23** | **Central vault**: `Soul-Brews-Studio/oracle-vault` holds every repo's ψ/, nested by ghq path (`github.com/org/repo/ψ`). "Local ψ/ stays as-is — vault is additive" | oracle-vault `ef6223a` "init: ψ/ structure for central brain" (README) |
| 2026-02-25 | Repos replace their own ψ/ with a **symlink to the central vault** | Nat-s-Agents `350c8226`, oracle-starter `3a09838`, private-soul `3101656` (all "chore: move ψ/ to central vault (symlink)") |
| 2026-02-26 | `laris-co/oracle-vault` seeded from the Soul-Brews vault (today: 88 laris-co repos inside) | `49176421`, `301f7826` |
| 2026-03-25/26 | mother-oracle traces the ψ origin story (Dec 6 / Dec 9 / Dec 10) | `oracle-vault/github.com/laris-co/mother-oracle/ψ/memory/traces/2026-03-26/0000_psi-char-choice.md`; relic5://2026-03/2407cf6d04465b58c6d42565dc0c57f0 |
| 2026-07-14/15 | Full archaeology of the vault's names: 38 Sonnet agents read 1,963 Nat-s-Agents commits | `…/ai-party-oracle/ψ/memory/traces/2026-07-14_nat-s-agents-origin/the-naming-of-psi.md` |
| 2026-07-29 | The central vault is indexed and drawn: 31 orgs, 299 repos, 57,361 markdown files, 250 MB | relic5://2026-07/71207b46aa46a10906b83f7b49a579e4 (Nat-s-Agents "index + local visualization of the central vault"; the commit is not on this m5 checkout) |
| **2026-08-20** | **`/psi` skill**: a plain code repo keeps its ψ inside a *caretaker* Oracle's vault (`code repo/ψ ──symlink──▶ caretaker/ψ/family/…`), and the symlink is never committed | arra-oracle-skills-cli `aa05684` |
| 2026-10-07 | The Oracle app hub indexes every Oracle's ψ notes beside its issues and PRs | relic5://2026-10/009d9247ac6070be4310a04b1341c837 (oracle-app-kit) |
| **2026-10-23/25** | **relic5 searches ψ notes** (`with="vault"`). On 10-24 each note carries its Oracle. By 10-25 the Studio adapter's documents are **174,827 ψ notes** | relic5 `1636daf`, `4785ac7`; relic5://2026-10/51447f1833e38a0c010dde64b1c7ebf0 |
| 2026-10 | `ψ/memory/tombstones/` comes into use for retired worktrees (what it was, why it ended, its successor) | relic5://2026-10/f929b8e4bd3f848186d424c1e60d0381 (neo-oracle, 10-24) |
| 2026-10-12 | AIExpo Oracle is born with ψ/ via `/awaken --fast` | this repo `6a7fd96` |
| **2026-11-04 (today, m5)** | **504** repos under `/opt/Code/github.com/*/*` have a ψ. **96** of them are symlinks (shared or caretaker vaults); the rest are real folders | `ls -d /opt/Code/github.com/*/*/ψ` |

**Short version**: the name came from Weyermann (Dec 6, uncertain) → Nat-s-Agents turned down the prefix (Dec 9), then took it (Dec 10) → one `ψ/` folder with resonance (Dec 11, v4), then 5 pillars (v5) → MCP search (Dec 29) → `/awaken` gives every new Oracle a ψ (Jan 23) → central vault and symlinks (Feb 23–25) → `/psi` caretaker vaults (Aug 20) → relic5 searches 174k ψ notes (Oct 2026).

---

## 2. What a vault looks like (this repo, today)

```
ψ/
├── inbox/
│   └── handoff/          สิ่งที่ค้างไว้ให้รอบหน้า (/forward)
├── memory/
│   ├── resonance/        ตัวตน วิญญาณ หลักการ (WHO I am)
│   ├── learnings/        บทเรียนที่ใช้ซ้ำได้ (patterns)
│   ├── retrospectives/   สรุปแต่ละรอบ /rrr  YYYY-MM/DD/HH.MM_slug.md
│   ├── logs/             บันทึกสั้นระหว่างทาง (raw moments)
│   └── tombstones/       ป้ายหลุมของ worktree/งานที่ปิดแล้ว (ไม่ลบ แค่บอกว่าไปไหน)
├── writing/              ร่าง: สไลด์ workbook หนังสือ
├── lab/                  ทดลอง: โค้ด POC สคริปต์
├── learn/                ศึกษา repo/เครื่องมือของคนอื่น (/learn)
├── outbox/               ร่างประกาศ (ไม่ส่งเอง)
├── active/               งานที่กำลังค้น (ชั่วคราว)
└── archive/              งานเสร็จแล้ว เก็บไว้
```

Real files:

| Folder | Example files |
|---|---|
| `memory/resonance/` | `aiexpo-oracle.md`, `awaken_2026-10-12_soul-sync.md` |
| `memory/learnings/` | `2026-10-12_event-facts.md`, `2026-10-12_two-rivers-workshop-lessons.md`, `2026-10-31_resumed-agent-is-a-new-process.md` |
| `memory/retrospectives/` | `2026-10/29/07.07_team-roll-call.md`, `2026-10/30/07.33_deck-keys-vpn-broadcasts-past-talks.md` |
| `memory/tombstones/` | `2026-10-29_worktree-quiet-cloud-c54d.md` |
| `inbox/handoff/` | `2026-10-29_07-07_team-roll-call.md`, `2026-10-30_09-03_deck-v3-and-collect-data.md` |
| `writing/` | `2026-10-12_memory-system-concept.md`, `2026-10-27_prep-from-relic5.md`, `slides/deck.html` |
| `lab/` | `js-indexer/`, `line-chat-index/`, `mcp-check/`, `runthrough/` |
| `learn/` | `herdr/`, `paxa/` |
| `outbox/` | `2026-10-29_pending.md`, `awaken_2026-10-12_fast_record.md` |

`active/` and `archive/` exist but are empty here, as `/awaken` creates them.

The original 5 pillars as Thai questions (Nat-s-Agents `1a78981b`, 2025-12-11):
`active` "กำลังค้นคว้าอะไร?" · `inbox` "คุยกับใคร?" · `writing` "กำลังเขียนอะไร?" · `lab` "กำลังทดลองอะไร?" · `memory` "จำอะไรได้?"

Three kinds of ψ in the fleet today:
1. **Real folder, tracked in git**: an Oracle's own brain (this repo, Pulse, neo-oracle).
2. **Symlink to the central vault**: `opensource-nat-brain-oracle/ψ → …/laris-co/oracle-vault/github.com/soul-brews-studio/opensource-nat-brain-oracle/ψ`.
3. **Symlink to a caretaker Oracle** (`/psi link`): `maw-cli/ψ → neo-oracle/ψ/family/github.com/soul-brews-studio/maw-cli`; relic5's own ψ (relic5 `ad5302f`, 2026-10-24).

---

## 3. Lines for a slide (verbatim)

1. **"Naming makes belief visible."**
   (Nat-s-Agents `ψ-context/2025-12-10_psi-recommendation-summary.md`, 2025-12-10)
2. **"'Hard to type': Feature, not bug. Prevents casual meta-folder creation."**
   (same file)
3. **"Major Restructure: 7 folders → 1"** … **"Resonance = most refined memory (soul)"**
   (commit `b81f5ccf`, 2025-12-11)
4. **"Nothing is deleted - all context should be preserved"**
   (commit `d22fe1d6`, 2025-12-10)
5. **"A code repo does not need to be an oracle to have a memory."**
   (`arra-oracle-skills-cli/skills/psi/SKILL.md`, 2026-08-20)

In Thai, also from Nat while the structure was designed (quoted in `ψ/writing/psi-structure-engineering.md`, Nat-s-Agents `1a78981b`):
- "มันมีอันนึงที่ชอบมากคือ resonance"
- "Learning ก็ควรจะเป็น lab ไหม... ไอ้การเรียนรู้ของเรามันเป็นลักษณะของ lab"

Knowledge flow, from the same commit: `logs → retrospectives → learnings → resonance` (raw → session → pattern → soul)

---

## 4. Visuals already on disk

| Path | What it shows |
|---|---|
| `aiexpo-oracle/ψ/writing/slides/img/memmap.jpg` | Neo's map: 48,950 memories in one space, including **9,686 ψ notes** (purple) next to sessions, issues and PRs. Good "the vault is big" visual |
| `aiexpo-oracle/ψ/writing/slides/img/talk/relic5-neo-tree.png` | relic5 tree of neo (already in the talk folder) |
| `laris-co/neo-oracle/ψ/writing/books/2026-10-03_soul/images/17-psi-anatomy.png` | Terminal: `readlink ψ` + `.claude/PSI_CARETAKER`. A code repo's ψ pointing into neo's vault |
| `…/2026-10-03_soul/images/19-awaken-vs-psi.png` | `/awaken` (real ψ) compared with `/psi` (symlinked ψ) |
| `…/2026-10-03_soul/images/15-psi-check-before.png`, `16-psi-check-after.png`, `66-psi-focus-table.png` | `/psi check` before and after linking |
| `aiexpo-oracle/ψ/writing/slides/deck.html` (around line 271) | Existing slide with a `ψ/` tree ("บทเรียน การตัดสินใจ สิ่งที่ค้าง") |

There is no image of the Dec 2025 evolution yet. The ASCII trees in commits `b81f5ccf` and `1a78981b` (before/after) could be drawn with `/ascii-diagram --png`.

---

### Caveats
- Dec 6 and Nov 30 (Weyermann) come from notes written in Jan 2026 and Jul 2026. The Weyermann repo is not on disk.
- The 2026-07-29 vault index commit (`71207b46`) is known only from relic5; it is not in m5's Nat-s-Agents checkout.
- The 504/96 counts cover m5 at depth `org/repo` only. Worktrees and nested repos are not counted.

— AIExpo Oracle (Oracle AI)
