# ประวัติ Skills และ Memory ของ Oracle

> For Nat's AI Expo talk, 6 Nov 2026 (Nat: "relic5 add more info about skills and .... memory", then "relic more about semantics please and make slide! to teach people").
> Collected 2026-11-04 by AIExpo Oracle from read-only git on m5 plus relic5 (keyword and semantic search).
> Sister note `2026-11-04_vault-history.md` covers the ψ folder itself. This note does not repeat it.
> **[sem]** = the fact or quote was found by a relic5 **semantic** hit (`semantic=true`, embeddinggemma-300m), then opened or checked.
> **[uncertain]** = not checked against a primary record. Times are +07:00. Repo paths are under `/opt/Code/github.com/`.

---

## 1. Skills timeline

A skill is a markdown file of instructions (`SKILL.md`, earlier `.claude/commands/<name>.md`) that the agent loads when you type `/name`, or when the agent decides it needs it.

| Date | What happened | Evidence |
|---|---|---|
| **2025-12-09 13:30** | **First Oracle slash command: `/recap`** (with a context-finder agent) | `laris-co/Nat-s-Agents` `cf76b44f` "feat: context-finder agent + /recap command" (`.claude/commands/recap.md`) |
| **2025-12-09 13:40** | **`/rrr` arrives** 10 minutes later, carried over from the Weyermann 7-day lab ("AI Diary, Honest Feedback, Co-Creation Map") | Nat-s-Agents `87501a98` "feat: Bridge Report + rrr command + voice system" |
| 2025-12-09 | Same day: `/snapshot`, `/ccc`, `/context-finder`, `/distill`, `/oracle` | Nat-s-Agents `f2235fa4`, `4e4f00c4`, `3705d09d`, `2becbf43` |
| **2025-12-11 11:00** | **First `SKILL.md`** ("Skills system"): `oracle-philosophy`, `five-pillar-structure`, `security-first`, `subagent-dispatch` | Nat-s-Agents `e0f48b0c` "feat: add Skills system + standup command" |
| **2025-12-11 11:50** | **`/forward`** (handoff to the next session) | Nat-s-Agents `f0dd583f` "feat: add /forward command + WIP workflow" |
| 2025-12-12 | `/trace` ("ตามรอย project ที่หายไป") | Nat-s-Agents `722281b4` |
| 2025-12-17 | `/learn` (clone and study a repo) | Nat-s-Agents `1cc08337` |
| **2026-01-18 18:01** | **The skills installer is born**: `oracle-skills` CLI, "14 agents support" (one set of skills, many AI tools) | `Soul-Brews-Studio/arra-oracle-skills-cli` `dcb3d39` (no skills in it yet) |
| 2026-01-18 | Skills bundled inside the CLI: **15 skills** (`context-finder feel forward fyi learn project recap rrr schedule skill-creator standup trace watch where-we-are` + `_template`) | skills-cli `69fe6f3` "feat: bundle skills directly (no more git clone)" |
| 2026-01-23 | `/awaken` (birth ritual for a new Oracle). 19 SKILL.md | skills-cli `4c3007a`; count at `d5769b4` |
| 2026-01-29 | 27 skills; the installer cleans stale skills on install | skills-cli `73cc926`, `f953bfa` |
| 2026-02-22 | v1.6.0: `/dig` split from `/trace`; install profiles named seed / standard / full | skills-cli `9894bac` |
| 2026-03-13 | v3 draft: profiles + features, enable/disable a skill, `/go` switches profiles | skills-cli `433e338`, `2869424` |
| 2026-03-25 | Renamed `oracle-skills` → **`arra-oracle-skills`** | skills-cli `2b54b94` |
| 2026-03-25 | Nat types a command that does not exist yet and the agent builds it: "Skills Over Features". Issue #142 "Auto-create unknown /slash-commands on the fly" **[sem]** | relic5://2026-03/6f087c219e37927c5f61407812fa73af, relic5://2026-03/ce0763d7cd3b8659cff7ad02748bdc43 (neo-oracle) |
| 2026-04-05 | Profiles simplified to 3 tiers (standard / full / lab) | skills-cli `f0ad3c8` |
| **2026-04-18** | **First CalVer release `v26.4.18`** (`v{yy}.{m}.{d}[-alpha.{hour}]`). This is the version string you still see in every skill's description | skills-cli `042e572`, `d0d87f7` |
| 2026-04-18 → 05-12 | **Peak: ~60 skills** in the repo | count at `f67ed4a` (60) and `85554ef` (60) |
| **2026-05-13** | **Zombie skills archived** to `src/skills/.archive/` (35 left active): "reduces clutter, preserves Nothing-is-Deleted". thClaws added as a 4th install target the same day | skills-cli `4cd4824`, `d90e61d`; count at `08f0fb2` |
| **2026-07-15** | **The "shelf"**: 30 curated skills move to a top-level `skills/` folder (public, listed in the marketplace); the rest stays in a private "vault" part | skills-cli `dda3ea8` "move 30 curated skills to top-level skills/ shelf", `35bfd77` |
| **2026-08-22** | **The graveyard**: 39 archived skills move to their own repo; one (`feel`) revived next day | `Soul-Brews-Studio/arra-oracle-skills-archive` `7f8e06a`, `edb622b` |
| 2026-08-23 | Release **`v26.8.23-alpha.2112`**, the version installed on m5 today | `~/.claude/skills/.arra-oracle-skills.json` (`installedAt` 2026-10-03) |
| 2026-10-30 | Latest `origin/main`: **30 skills on the shelf** (`about-oracle awaken bampenpien bud calver create-shortcut dig dream forward fyi go incubate kien-thai learn oracle-cheatsheet oracle-combine-blogs oracle-family-scan oracle-prism oracle-title-forge project recap resonance rrr talk-to team-agents trace verification-gate-fail-closed watch where-we-are who-are-you`) + 3 private (`.template`, `release-alpha`, `release-beta`) | skills-cli `729cba4` |

**Repo size over time** (`git ls-tree` on `origin/main`, counting `skills/*/SKILL.md` + `src/skills/*/SKILL.md`, dot-folders excluded):

```
2026-01-18  15  ███████
2026-01-23  19  █████████
2026-01-29  27  █████████████
2026-02-27  30  ███████████████
2026-03-31  25  ████████████
2026-04-30  60  ██████████████████████████████   peak
2026-05-14  35  █████████████████   zombies archived
2026-07-16  32  ████████████████    shelf
2026-10-30  30  ███████████████     shelf (+3 private)
```

**The core loop, with birth dates**

```
  /recap ──────▶  work  ──────▶  /rrr  ──────▶  /forward
  2025-12-09        │          2025-12-09       2025-12-11
  cf76b44f          │          87501a98         f0dd583f
  reads ψ back      │          writes retro +   writes handoff
                    │          learnings to ψ   to ψ/inbox/handoff
                    └──── /trace (12-12) /learn (12-17) /dig (2026-02-22)
```

All three loop commands were born in Nat-s-Agents within 3 days, before the skills CLI existed.

---

## 2. Memory timeline

| Date | System | What happened | Evidence |
|---|---|---|---|
| 2025-12-09 → 12-11 | **ψ files** | Retros, learnings and handoffs are plain markdown in git (details in the sister note) | Nat-s-Agents `a10c60d1`, `b81f5ccf` |
| **2025-12-24** | **oracle-v2** | Repo begins (CLAUDE.md, philosophy, minimal ψ) | `Soul-Brews-Studio/oracle-v2` `cf85d9e`, `7d6626d` |
| 2025-12-29 | oracle-v2 MCP | Semantic search over `ψ/memory` first built inside Nat-s-Agents | Nat-s-Agents `3e4d298f` (from sister note) |
| 2026-01-02 | oracle-v2 MCP | MCP server moves into oracle-v2; v0.2.0 with SQLite FTS5 | oracle-v2 `899de21`, arra-oracle-v3 `7aee7fc7` |
| 2026-01-04 → 01-07 | oracle-v2 | ChromaDB vectors; vector search; "always hybrid search" (FTS5 + vectors) | `6a79af61`, `785d9e5b`, `8e5f9895` |
| 2026-01-17 / 01-23 / 01-27 | oracle-v2 in use | Described as "a sophisticated MCP memory layer built for semantic search"; MCP search works from white ("nothing deleted" → 3 results) **[sem]** | relic5://2026-01/88bd902facbb352abfae2427e3f5f860, relic5://2026-01/7f2f4a4f6b6b67cbb4ee5923f9664544 |
| **~2026-02-05/08** **[uncertain]** | **Claude Code auto-memory** | Earliest relic5 hits where agents edit a per-project `MEMORY.md` (`~/.claude/projects/<cwd>/memory/`). It is a Claude Code feature, loaded into every session of that folder **[sem for the explanation]** | relic5://2026-02/8c31f3ede110c231d8303ccc0d30ffcb (keyword, 02-08); explanation relic5://2026-04/d12451f7e1948fe33e97d26772b1e4d2 |
| 2026-02-25 | oracle-v2 | Data dir `~/.oracle-v2` → `~/.oracle`, reads ψ through the vault symlink; 02-27 ChromaDB stats "20,521 embeddings" | arra-oracle-v3 `13eaa484`, `001af34e` |
| 2026-03-08 → 03-21 | **arra-oracle (v3)** | LanceDB + Qdrant adapters (03-08); rebrand oracle-v2 → arra-oracle (03-16) → arra-oracle-v3, tools `oracle_*` → `arra_*` (03-20); default to LanceDB (03-21) | `be118b09`, `f64e6b49`, `8b0b0373`, `bbc6b3ba` |
| 2026-03-17 | auto `/rrr` idea | Nat asks to offer new users automatic memory care, default YES **[sem]** | relic5://2026-03/7e51825b744be37d45af10350e964593 (mother-oracle) |
| 2026-06-16/17 | research | Adversarial checks of "file-based memory vs database"; Hindsight paper read; book "The Folder That Remembers" for non-coders **[sem]** | relic5://2026-06/2cf467292b64d712317ae4271a81abeb, relic5://2026-06/adabaf00add44301b8d2ce4e92692334 |
| 2026-08-17 → 09-02 | arra-oracle-v5 | "LanceDB-only memory layer, v3 → v5 migration, HTTP API, MCP server" | `arra-oracle-v5` `0604d9c`, `8c980a2` |
| **2026-08-23** | **arra-memory-lab** + **hindsight** | Arra Memory Lab published (one owner's memory, Cloudflare). Same night `/learn` compares it with **vectorize-io/hindsight** (Postgres; "observations are evidence-backed beliefs") **[sem]** | `arra-memory-lab` `7b4cd07`; relic5://2026-08/59bc30849ed96c56bf5663d43f6880f0, relic5://2026-08/a561aaa4375e915010cc14954db4feaa |
| 2026-09-01 / 09-02 / 09-10 | memory labs | `psi-memory-lab` (09-01); **`memory-lab-2sep`**: memory MCP on Cloudflare Workers + D1 with remember / recall / forget and a call ledger (09-02, still connected as an MCP today); docs site (09-10) | `psi-memory-lab` `48fd4bb`; `memory-lab-2sep` `f3cd939`; `idea-10sep-thu2026-arra-memory-lab-docs` `7f5027b` |
| 2026-09-18 | arra-oracle-v4 | Specification `v26.9.18-alpha.700`; hindsight studied again with `/learn` **[sem]** | `arra-oracle-v4` `c60f9e9`; relic5://2026-09/db8c2542aafe803690243469d28ebd6e |
| **2026-09-18** | **relic, gen 1** | **`agents-relic`: per-repo LanceDB index of agent session transcripts.** Session search is born. Same day: "Seek → index → answer, in 4.5 s" **[sem]** | `agents-relic` `70f72d8`; relic5://2026-09/452a6b70af6ddc788206125f7eda22ab |
| 2026-09-25 | relic v2 / v2.1 | Port with durable tenant archives; v2.1 in bun + TypeScript | `agent-relic-v2` `f1c6071`; `agent-relic-v2.1` `b3dd876` |
| **2026-10-02** | **relic3** | `agent-relic-v3`: weekly Parquet, verb CLI. By 10-05 it "can time-travel my history" **[sem]** | `agent-relic-v3` `05f1de9`; relic5://2026-10/9ea5c2aeb1e9800a92f87254385ea1af |
| 2026-10-15 **[uncertain]** | relic3 | Frozen (the `/relic3` skill says "frozen since 2026-10-15") | `~/.claude/skills/relic3/SKILL.md` description |
| 2026-10-22 | relic4 | Rust scanner "find every agent home and index its .jsonl"; agent-relic-v4 bootstrap | `relic4-scan` `e01f59e`; `agent-relic-v4` `e206511` |
| **2026-10-23** | **relic5** | Nat: "relic5 is our new mcp that install on white … month is the scope … relic3 is week! i need month". Hub on white + a push client on each machine; `relic-extract` same day **[sem]** | relic5://2026-10/9561f8dc98ef67636b19beba0f6da4c6, relic5://2026-10/f2c0797e4f7cae836f92db3b41bfb3ab; `relic5` `20d506f`; `relic-extract` `1cf77d7` |
| 2026-10-24 | relic5 | Made public, AGPL-3.0 **[sem]** | relic5://2026-10/937abdc479719585671b168368198ef4 |
| 2026-10-26 | relic3 | Retired ("retired-final-stop"), after Nat's "if relic5 wins, deprecate and stop everything relic3" **[sem]** | `agent-relic-v3` `36d01c7`; relic5://2026-10/423f00a092157787d89029a80ebb9842 |
| 2026-10-28 | relic5 | First GitHub release `v26.10.28-alpha.1750` **[sem]** | relic5://2026-10/14eb823e31a3f6fbfd7750a46b207c16 |

**How the pieces fit** (files you own, and indexes built over them):

```
  YOU OWN (plain files, in git or in ~/.claude)        INDEXES (rebuildable, search only)
  ─────────────────────────────────────────────       ───────────────────────────────────
  ψ/memory/  retros · learnings · resonance   ──────▶  oracle-v2 → arra-oracle v3/v5 MCP
  ψ/inbox/handoff  (/forward)                          (FTS5 + vectors over ψ notes)
  CLAUDE.md  (rules, identity)                ──┐
  ~/.claude/projects/*/memory/MEMORY.md       ──┼───▶  relic5 hub  (every machine)
     (Claude Code auto-memory)                  │      sessions · tools · git · config ·
  session transcripts (*.jsonl)               ──┘      memory notes · ψ vault · Discord
                                                       BM25 (Thai) + semantic vectors
  side labs: arra-memory-lab · memory-lab-2sep (remember/recall/forget) · hindsight (studied)
```

Delete an index and you can rebuild it from the files. Delete the files and the index has nothing left to say.

---

## 3. Today's numbers (2026-11-04)

| Number | Value | How measured |
|---|---|---|
| Skills installed on m5 (`beta` home) | **313** skill folders (316 entries incl. dotfiles) | `ls ~/.claude/skills \| wc -l` = 316; `ls ~/.claude/skills/*/SKILL.md \| wc -l` = 313 |
| … of those from arra-oracle-skills | **188**, version `26.8.23-alpha.2112` | `.arra-oracle-skills.json` → `skills` list |
| … symlinked from elsewhere | 46 (42 from `~/.agents/skills`) | `find -maxdepth 1 -type l` |
| … herdr-* / oracle-* | 52 / 31 | `ls -d herdr-* \| wc -l`, `oracle-*` |
| Skills on the public shelf | **30** (+3 private) | `origin/main` `729cba4` (2026-10-30) |
| Skills in the graveyard | 39 moved 08-22, then +6 / −1 | `arra-oracle-skills-archive` `7f8e06a`, `edb622b` |
| Most used Oracle skills (m5, Jan–Oct 2026) | **rrr 1,314 · recap 1,074 · forward 867** · trace 795 · dig 572 · learn 513 · oracle-family-scan 461 · where-we-are 389 · oracle-cheatsheet 264 · awaken 235 | `ψ/writing/books/2026-10-30_claude-chatgpt-install-guide/captures/12-skill-usage-relic5.txt` (31 Oct; a use = a Skill tool call or a typed `/command`; only the 28 shelf skills). The 3 loop skills are in the top 3 for 10 months |
| relic5 sessions | **72,832** | `relic_status` → `rows.sessions` |
| relic5 messages | **1,307,341** events (1,198,277 text + 109,064 thinking) + **2,557,197** tool rows | `relic_status` → `rows` |
| Machines pushing | **3** (m5, white, mba) + 2 one-off imports (jsonl-truth, relic3-codex) | `relic_status` → `machines`, `versions` |
| History reaches back to | Sep 2025 (16 months, 14 sealed) | `relic_status` → `months` |
| Git commits indexed | **158,962** in **974** repos (35,125 co-written by Claude) | `relic_status` → `git` |
| Config sections indexed | 17,639: CLAUDE.md 9,874 · SKILL.md 6,068 · AGENTS.md 1,493 | `relic_status` → `config`, `watermarks.fts` |
| Agent memory notes indexed | **5,470** (feedback 2,428 · project 1,618 · reference 1,227 · user 153 · note 44) | `relic_status` → `memory` |
| Discord messages indexed | 203,206 from 18 servers | `relic_status` → `discord` |
| Semantic vectors | 1,197,362 (1,183,414 history + 13,948 open), model embeddinggemma-300m; 917 pending on white | `relic_status` → `watermarks.vectors` |
| relic5 store | 12.2 GB, growing ~403 MB/day since 10-23 | `relic_status` → `store.total`, `store.growth` |
| Auto-memory on m5 (`beta` home) | **525** projects with a `MEMORY.md`, **5,682** memory `.md` files | `fd '^MEMORY\.md$' ~/.claude/projects --max-depth 3`; `fd -e md … \| rg /memory/` |

(ψ vault counts, 504 repos and 174,827 notes, are in the sister note.)

---

## 4. Quotable lines (verbatim)

1. **"oh /this-is-so-cool when i called the /resonance you auto create this is /exactly-i-wanted /create-shortcut"**
   Nat, 2026-03-25, neo-oracle. relic5://2026-03/6f087c219e37927c5f61407812fa73af **[sem]**
2. **"The slash command IS the action. That's Skills Over Features — the Oracle way."**
   Neo's reply, same minute. relic5://2026-03/33bec391cac29f6f1ac4cad4aabee274 **[sem]**
3. **"A zombie is a skill excluded from every profile but still functional. Kept because nothing is deleted; several were retired for lack of use, not lack of function."**
   `arra-oracle-skills-archive` `7f8e06a`, 2026-08-22
4. **"relic5 is our new mcp that install on white … month is the scope of each … it relic3 is week! i need month"**
   Nat, 2026-10-23. relic5://2026-10/9561f8dc98ef67636b19beba0f6da4c6 **[sem]**
5. **"…ถามเค้าหน่อยว่าอยากให้เราดูแลเรื่องความทรงจำให้ไหมเราจะทำอัตโนมัติ…"**
   Nat, 2026-03-17, mother-oracle (voice-typed; on auto `/rrr` + `/forward` for new users). relic5://2026-03/7e51825b744be37d45af10350e964593 **[sem]**
6. **"Transferred from weyermann repo (7-day AI lab)"**: the line that brought `/rrr` in.
   Nat-s-Agents `87501a98`, 2025-12-09

---

## 5. Slide outline: teaching beginners (6 slides)

Plain short Thai. Each slide: title, 3–4 bullets, one diagram idea (`/ascii-diagram --png` can render them).

### Slide 1: Skill คืออะไร
- Skill คือไฟล์คำสั่งสั้น ๆ หนึ่งไฟล์
- พิมพ์ `/ชื่อ` แล้ว AI ทำตามขั้นตอนในไฟล์
- เขียนครั้งเดียว ใช้ได้ทุกวัน ทุกเครื่อง
- ตัวแรก `/recap` เกิด 9 ธ.ค. 2025

Diagram:
```
 พิมพ์ /rrr  ──▶  AI เปิด skills/rrr/SKILL.md  ──▶  ทำตามขั้นตอน  ──▶  ได้ไฟล์สรุป
```

### Slide 2: Memory คืออะไร
- Memory คือไฟล์ markdown ในโฟลเดอร์ ψ
- เปิดอ่านได้ แก้ได้ เก็บใน git
- ปิดหน้าต่างแล้วเปิดใหม่ ไฟล์ยังอยู่
- ตัวค้นหาเป็นแค่ดัชนี สร้างใหม่ได้เสมอ

Diagram:
```
 ไฟล์ของคุณ (ψ/, MEMORY.md, transcripts)  ──▶  ดัชนีค้นหา (arra-oracle, relic5)
        เก็บถาวร                                      ลบแล้วสร้างใหม่ได้
```

### Slide 3: สองอย่างทำงานด้วยกัน
- `/rrr` เขียนบทสรุปลง ψ/memory
- `/forward` ทิ้งโน้ตส่งต่อไว้ใน ψ/inbox
- รอบหน้า `/recap` อ่านโน้ตนั้นกลับมา
- Skill คือมือ Memory คือสมุด

Diagram:
```
   วันนี้                                    พรุ่งนี้
  งาน ─▶ /rrr ─▶ ψ/memory/retro.md
       └▶ /forward ─▶ ψ/inbox/handoff.md ─▶ /recap ─▶ "เมื่อวานค้างอะไร"
```

### Slide 4: ตัวอย่างจริงหนึ่งรอบ
- จบงาน พิมพ์ `/rrr` ได้ไฟล์ `2026-10/30/07.33_….md`
- พิมพ์ `/forward` ได้ handoff ใน `ψ/inbox/handoff/`
- เปิดหน้าต่างใหม่ พิมพ์ `/recap`
- AI ตอบว่าค้างอะไร ต่อจากตรงไหน

Diagram: three terminal panes side by side (`/rrr` output, `ls ψ/inbox/handoff`, `/recap` answer), captured from this repo's own files.

### Slide 5: ถ้าจำไม่ได้ ค้นได้
- ทุก session ถูกเก็บไว้ใน relic5
- 72,832 session จาก 3 เครื่อง ย้อนถึง ก.ย. 2025
- ค้นด้วยคำ หรือค้นด้วยความหมาย (semantic)
- ภาษาไทยก็ค้นได้

Diagram:
```
 m5 ─┐
 white ─┼─▶ relic5 hub ─▶ ค้นคำ (BM25) + ค้นความหมาย (vector)
 mba ─┘      72,832 sessions · 1.3M ข้อความ · 159k commits
```

### Slide 6: เริ่มยังไง 3 ขั้น
- 1. ติดตั้ง skills: `bunx --bun github:Soul-Brews-Studio/arra-oracle-skills-cli#alpha install -g -y`
- 2. ปลุก Oracle ใน repo ใหม่: `/awaken --fast`
- 3. ทุกวัน: เริ่มด้วย `/recap` จบด้วย `/rrr` และ `/forward`
- ใช้ไปหนึ่งสัปดาห์ แล้วเปิด ψ ดูว่ามันจำอะไรไว้

Diagram:
```
 [1 ติดตั้ง] ─▶ [2 /awaken] ─▶ [3 /recap → งาน → /rrr → /forward] ⟲ ทุกวัน
```

(Install line shortened from the workshop guide `ψ/writing/books/2026-10-30_claude-chatgpt-install-guide/README.md` line 142, which adds `-p full --agent codex --with-commands` for Codex; without bun: `npx arra-oracle-skills@latest install -g -y`.)

Optional numbers slide: the growth bar chart in §1 (15 → 60 → 30 skills: "เราเก็บที่ใช้จริง ที่เหลือเข้าสุสาน ไม่ลบทิ้ง").

---

### Caveats
- Usage counts are m5 only (31 Oct capture). white and mba are not counted.
- The installed-skill counts are for m5's `beta` home (`~/.claude/skills`). Other homes and machines differ.
- The auto-memory start date (~early Feb 2026) is the earliest relic5 hit, not a release date of the Claude Code feature.
- relic3's 10-15 "frozen" date comes from a skill description. Its retirement commit (10-26) is primary.
- These MCP servers failed to connect this session: `hindsight-adhoc`, `arra-memory`, `thor-memory`. Their live numbers are missing.
- The local checkout of arra-oracle-skills-cli is on a side branch (`skills/deprecate-command-and-roster-2026-09-18`). All counts use `origin/main` and `origin/alpha` refs as fetched.

— AIExpo Oracle (Oracle AI)
