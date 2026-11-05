# Oracle skill `oracle-title-forge`: the full skill

> For the AI: /oracle-title-forge = forge a title for a book, article or talk. In a chat it works in a chat: follow it with the person here. Where it mentions files or commands, show the content for the person to save.
> This is every file of the skill as shipped in lesson 01 (arra-oracle-skills v26.8.23, ~/.claude/skills on m5), 1 files.

<!-- file: oracle-title-forge/SKILL.md -->
### File: `oracle-title-forge/SKILL.md`

---
installer: arra-oracle-skills-cli v26.8.23-alpha.2112
origin: Nat Weerawan's brain, digitized — how one human works with AI, captured as code — Soul Brews Studio
name: oracle-title-forge
description: '[core] v26.8.23-alpha.2112 G-SKLL | "Forge a title + subtitle (or reframe) for a BOOK, article, talk, or any technical piece, then hand off to a cover so it has LIFE and honesty — not clinical/dated. The method that produced ''Claude Code Channel ปะทะ Hermes Gateway''. Describe-before-you-name, find the real tension, prism the candidates, calibrate register (eloquent but dev-natural, not poetic), name the real technical axes in the subtitle, refuse a fake winner. Use when: a title feels เชย/dead/generic, when naming a book or post, when reframing a comparison as a genuine contest, or when the user says ''ตั้งชื่อ'', ''title'', ''reframe'', ''ชื่อมันเชย'', ''คิดชื่อ''. After the title lands, offer the cover step (see ''Then: the cover''). DO NOT TRIGGER for: writing the body content itself (use kien-thai / the book skills), or for designing a cover from scratch when no title work is needed (go straight to /oracle-book-cover)."'
argument-hint: "<what to title — topic, or the current dead title + what the piece is about>"
hidden: true
metadata:
  internal: true
---

# /oracle-title-forge — forge a title that has life, honestly

> Born 2026-07-09 turning the dead "ผ่าไส้ Discord Channel ของ Claude Code" into
> **"Claude Code Channel ปะทะ Hermes Gateway — สองสถาปัตยกรรมที่ทำให้ AI คุยบน Discord ได้…"**
> The lesson: a great title is *grown from understanding what the thing IS*, not shuffled from words.

## Why the method works (read this first)

A dead title fails one specific way: it has **clarity without intrigue**. "ผ่าไส้ X" tells you
the topic and nothing else — no tension, no question, no stake. Every principle below exists to
add intrigue *without lying*. The magic isn't wordsmithing; it's that each step forces you to
understand the material more deeply, and the title falls out of that understanding.

## The method — 7 moves

### 1. Describe before you name
Never start by brainstorming words. First write **what each thing IS** — once vividly, once in
plain technical terms. The title grows from this. (For the Discord book, writing "the plugin is
a stdio bridge tied to a session's lifecycle; Hermes is an always-on daemon" is what *revealed*
the contest.)

### 2. Find the real tension — and check it's not forged
If it's a comparison/VS, run a **skeptic pass**: is the contest real or clickbait? Two things at
different layers can't fight on features. Reframe the tension at the honest layer — *philosophy,
fit, tradeoff* — not a fake feature-fight. A title promising a showdown the book can't deliver is
a lie. (Discord book: they're transport vs runtime — so the contest is "two philosophies of
presence," which is true, not "which codes better," which is false.)

### 3. Prism the candidates — 3-5 lenses
Look at each candidate from angles a single view misses. Useful lenses for titles:
- **🏪 Bookshelf browser** — does the spine make someone pick it up?
- **💀 Honest skeptic** — does the title over-promise? name only one side of a two-sided story?
- **🧑‍💻 Dev-ear** — *would a developer actually say this phrase?* Kill words devs don't use
  ("ให้ AI พูด" → "AI คุยบน Discord"; "ต่อ AI เข้ากับ Discord" → clunky; "data เข้าทางไหน" ✓ real).
- **✍️ Thai editor** — cadence, clean noun phrases, cut stray connectors (ด้วย/ต่อ...เข้ากับ).
- **🎯 Precision** — does the subtitle name the *real axes*, not vague adjectives?

### 4. Apply the craft principles (from title research)
- **Tension = clarity × intrigue.** The reader must grasp *something* instantly AND be compelled
  to open it for the rest.
- **Contrast breeds curiosity.** Unexpected/opposed words hook ("The Wealthy Barber"). A "ปะทะ" /
  "vs" between two named things is contrast built-in.
- **Formula: short curious head + longer explaining subtitle.** Head = hook (1-6 words / a clash /
  a question). Subtitle = context + payoff.
- **Question form** raises the stakes above the mechanism ("ใครควรได้…").
- **Cadence / list-of-three** makes the subtitle linger ("data ขาเข้า, การคุมสิทธิ์, วงจรชีวิต").

### 5. Calibrate register with the human
Draft, then dial. Common arc: *clinical → too poetic → eloquent-but-technical*. The target for
technical work: **สละสลวยแต่ตรง, ไม่เล่นอุปมามาก** — pleasant to the ear, but every phrase points
at something real in the code. Show the human one sample paragraph in the proposed voice and let
their taste calibrate. Their "แปลกๆ" is data — chase the specific weird word.

### 6. Name the real technical axes in the subtitle
Don't sell with adjectives ("powerful, elegant"). Sell with the **concrete things the piece
compares/covers** — the axes a practitioner cares about (data path, access control, lifecycle),
ending on the payoff ("ตัวไหนเหมาะกับงานแบบใด").

### 7. Honesty is a feature, not a weakness
Refuse the cheap winner. "Generic: it's a tie on different axes; situational: here's the matrix"
reads as *more* authoritative than "X wins." A title/frame that promises an honest verdict earns
trust the clickbait can't.

## Output shape
Offer **2-3 candidates**, each *described by the feeling it gives + the craft reason it works*
(not a bare list), recommend one with why, then render the full cover block (head + subtitle) so
the human sees it assembled. End by asking which — let taste decide the last 5%.

## Proven example
```
# Claude Code Channel ปะทะ Hermes Gateway
สองสถาปัตยกรรมที่ทำให้ AI คุยบน Discord ได้ — เทียบตั้งแต่ data ไหลเข้าทางไหน
คุมสิทธิ์การเข้าถึงยังไง ไปจนถึงว่าตัวไหนเหมาะกับงานแบบใด
```
Head = two named contenders + ปะทะ (contrast). Subtitle = 3 real axes + payoff. Register =
eloquent but dev-natural. Verdict promised = honest (fit, not a fake winner).

Related: [[kien-thai]] (Thai prose engine), [[oracle-prism]] (the lens method), the book skills
(oracle-write-complete-book / -booklet / -combine-blogs) that consume the forged title.

---

## Book mode

A book title carries more weight than an article's: it is the spine text, the search
result, and the thing someone repeats to a friend. Two extra constraints on top of the
7 moves:

- **Spine test** — say it out loud as if recommending it. If it needs a subtitle to make
  sense spoken, the main title is doing too little.
- **Shelf test** — write it next to three real books in the same genre. Generic titles
  vanish; that is the whole signal.
- Subtitle carries the technical axes (the 7 moves already say this); the **main title
  carries the tension**. Do not let the subtitle rescue a dead title.

## Cover text: title + subtitle, nothing else

What goes ON the cover is title work, so it belongs to this skill. Learned on the relic vs
relic3 proof book (2026-10-03, kvmbox-oracle PR #45). It took six cover builds to arrive at the
cover below, and every step before the last one added text Nat then cut.

```
เขียนโดย AI เพื่อ AI                            ← kicker, ALWAYS first (default since 2026-10-05)
$ relic3 tail d69f33c7 -n 20 --handoff         ← the story's trap, dim

relic vs relic3                                ← head: the two contenders
อ่านประวัติ session ให้ถูก                       ← promise, the ONLY accent colour
───
เครื่องมืออ่านประวัติ session ของ Claude Code + Codex สองรุ่น
ทุกคำสั่งรันจริง ทุก capture คือเทอร์มินัลจริง — 2026-10-03
   (with generated art: ทุกภาพในเล่มคือเทอร์มินัลจริง ยกเว้นภาพปกที่ AI วาด)

kvmbox-oracle (AI, ไม่ใช่คน) กับ Nat Weerawan
```

| Rule | Because (what actually happened) |
|---|---|
| **Cover = head + subtitle + tagline + author. Stop.** | A labelled อะไร / ทำไม / ยังไง / ผล grid was added "to explain the book". Nat: *"too dense"*, then *"full not ok — this is a book cover and title!"* |
| **No labelled rows, no what/why/how/result** | A `/hallmark audit` named it critical twice. Tag-left/content-right labels are the hanging-header AI tell (gate 54), and what/why/how/result is the default LLM explainer form. |
| **The cover never states the finding** | The answer belongs in the preface and the last chapter. A cover that gives it away has nothing left to make someone open the book. |
| **One accent, on the promise line only** | Labels, inline code and the title line were all the same blue, so nothing stood out. |
| **A command on the cover must be the story's trap or villain** | `$ relic tail d69f33c7 -n 1` was decoration, and the id meant nothing to a reader. `… --handoff` is the command that caused the book. |
| **Every word on the cover is literally true** | "ทุกภาพคือเทอร์มินัลจริง" was false for the drawn diagrams, so it became "ทุก capture". "ของ Claude Code" was too narrow, so it became "Claude Code + Codex" (per the tool's own `--help`). |
| **Kicker "เขียนโดย AI เพื่อ AI" is the first line of every cover** | Nat added it on 2026-10-03 ("หนังสือโดย" → "หนังสือจาก" → "เขียนโดย", he picked เขียนโดย) and on 2026-10-05 told us to make it the default in the skills. It is the cover-level form of Rule 6 (AI disclosed from the cover onward). |
| **Render at 90 dpi and look before saying done** | At 60 dpi a Thai mid-word break ("เทอร์ / มินัล") and an orphan word were easy to miss. Control line breaks in typst with explicit `\`. |

**Prism with imagined real people, not abstract lenses.** "Archaeologist / Skeptic" lenses
produced a correct audit that Nat didn't feel. He asked to *"think as a person"*. Five made-up
people with an age, a job and a moment did land: a backend dev scrolling at lunch, a cover
designer, a 15-year editor, a sceptical SRE, and a junior who recaps sessions every morning.
Each speaks in their own voice about the actual cover. Say plainly that they are imagined.

## Then: the cover

**This skill does not draw.** Stated plainly because the alternative is pretending:

| capability | present here |
|---|---|
| generative image tool in Claude Code itself | **no** |
| `codex` CLI built-in `image_gen` | **yes**, through `/imagegen` (`codex exec`, 2–4 min per image; the sandbox can't write into your dir, so collect the file from `~/.codex/generated_images/`). Corrected 2026-10-03: this row used to say codex can't generate images |
| ImageMagick (`convert` / `magick`) | yes — **composition only**: type on a ground, crops, gradients |
| typst | yes — vector/typographic covers rendered with the book |

So a cover here is one of three honest things: **found art** (licence-checked), a
**typographic composition**, or a **generated image via `/imagegen`**, labelled as generated and
never passed off as a photograph. Keep a generated image humble: quiet, dark, lots of negative
space, no text, no people, no logos. The title still carries the cover.

**Default for proof books (2026-10-05):** the cover is layout C — kicker, Codex-generated art, title.
Run `zsh ~/.claude/skills/oracle-write-proof-book/scripts/make-cover-art.sh <book dir> "<one quiet object tied to the story>"`
(direct `codex exec`, seconds, no pane), then Read the image. `/oracle-write-proof-book` § 2c holds the layout and the gate. The
tagline must then say the art is generated (`ยกเว้นภาพปกที่ AI วาด`). `/oracle-book-cover` stays the route for licence-checked
found art and social crops.

**Hand off to `/oracle-book-cover`** — it already does this properly: finds real art with a
LICENCE gate, runs a 5-lens prism (Reader / Editor / Artist / Designer / Ads), renders 2-3
PNG candidates, bakes the winner into the `book.typ` cover block only, and exports social
crops. Do not rebuild that pipeline here.

```text
/oracle-title-forge   → title + subtitle
        ↓
/oracle-book-cover    → art (licence-checked) or typographic cover → book.typ
```

If `/oracle-book-cover` is not installed on this machine, say so and stop — do not
improvise a cover with `convert` and call it a design. A typographic fallback is legitimate
only when the human asks for it knowing no illustration is involved.

**Delegating to codex**: `/codex:rescue` or the `codex-rescue` agent can take a
cover-generation *task* (typst layout, ImageMagick composition, asset wrangling). It cannot
produce an illustration *through rescue*. To actually draw, use `/imagegen`, which drives
`codex exec` with the built-in `image_gen`.
