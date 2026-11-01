# Brief round 3 for Osaa: tidy the typography and elements

From Dobby, 2026-11-01. Yim, verbatim: "ยิ้มว่า font กับ element ต่างๆ เก็บได้เรียบร้อยกว่านี้นะ"
Start from the current `deck.html` (Dobby edited slide 3 text and slide 4 lead after your round 2; keep those words).
All MUST rules from BRIEF.md still apply. Do NOT change on-screen wording except where this brief says so; Yim is still deciding wording changes.

## 1. Polish (the main job)
Run impeccable critique + polish and your osaa-design-system pass, then fix what they find. At minimum:
- One type scale for the whole deck: display / heading / lead / body / caption, each used the same way on every slide. Write the scale at the top of the CSS.
- One grid: same left edge, same top line for headings, consistent gaps between heading → content → footnote on every slide.
- Consistent element language: rule lines, labels (ขั้น 1, numerals), bullets, highlight colour, card/no-card. Pick one treatment per element type and apply it everywhere.
- Thai line breaks chosen on purpose (no orphan word, no break inside a phrase). Body text on screen >= 34px; captions/footnotes >= 30px (the 24px `.fnote` on slide 3 fails).
- Secondary grey text must stay readable from the back: contrast >= 7:1 for body copy.

## 2. Fixes from the independent Codex review (`REVIEW-CODEX.md`)
- Slide 3: replace the three particle rows with ONE labelled architecture diagram (HTML/SVG, particles as enhancement only):
  ยิ้ม (Mac / มือถือ) → Discord ศูนย์กลาง → เครื่องที่เปิดตลอด (ฝูงสิบกว่าตัว) → ความจำร่วมเป็นไฟล์,
  with edges to ผู้ช่วยส่วนตัว Grok · Dots · Muse and to agent ของคนอื่น (คุยได้ ลงมือในระบบเราไม่ได้ · คนกดอนุมัติ).
  Keep the line "ตัวที่วางแผน ตัวที่ลงมือ และตัวที่ตรวจ เป็นคนละตัว คนเป็นคนอนุมัติ" and the tools footnote (now >= 30px).
- Offline: put fonts (Bai Jamjuree, Sarabun woff2) and three.module.js in `./vendor/` next to deck.html and load them locally; keep the deck working from a plain folder copy with network off.
- Include `.num` in the text-exclusion measure (slide 5). `go()` returns early when the target is the current slide; ignore key auto-repeat.
- Add a visible still-mode toggle (key `S`) that stops the loop and shows static frames.

## Acceptance (run and paste output into REPORT.md, which you must rewrite to match the current deck)
- `uv run -q --with playwright python /private/tmp/claude-502/-Users-yim/5aabf861-4d65-4575-9c86-30c641119993/scratchpad/shot.py deck.html .` → `1 []` … `6 []`; look at every PNG.
- Offline proof: serve nothing, block all network in Playwright (`route('**/*', abort)` for http/https), screenshot all 6 → fonts are the real faces (check `document.fonts.check('40px "Bai Jamjuree"')` is true) and the 3D runs (`window.__world` truthy).
- Negative control: rename `vendor/` temporarily → text still shows on all 6, `__world` false. Restore it.
- `grep -c` for `[—–]` in on-screen text = 0.
Write REPORT.md in your own voice (เรา/โอซ่า, ค่ะ/นะ).

## Addendum (Yim, verbatim, arrived after the run started): "font เอา style ของ rikyu lab มาใช้ก็ได้"
Use the Rikyu Labs type system instead of Bai Jamjuree + Sarabun. Source of truth:
`~/hello-oracle/ψ/design-systems/rikyu-labs/slide-kit/tokens/tokens.css` lines 39-41 and the kit's `th/guideline.html`:
- sans (headings + body): Satoshi (Latin) + IBM Plex Sans Thai (Thai)
- alt sans for friendly surfaces: LINE Seed Sans TH (optional)
- serif only for one editorial line (quote/manifesto), Source Serif 4 + Noto Serif Thai; don't use it elsewhere
Bundle the files you use into `./vendor/` (offline rule still applies). Note the licence of each font in REPORT.md.
Keep the dark stage palette unless the kit's guideline says otherwise for talks; report what you chose and why.

## Addendum 2 (Yim, verbatim): "เก็บความเรียบร้อยเรื่อง UI element ด้วย"
UI element pass, every slide, list each fix in REPORT.md:
- One stroke width, one corner radius, one circle size family, one arrowhead style across the deck.
- Slide 4 ring: arrows must start and end on the circle edge with equal gaps (they currently touch/overlap the nodes); node circles the same size; ψ/ centre aligned to the exact ring centre; labels optically centred in their circles.
- Dotted halos and particles must not cut through labels or arrows.
- Slide 1 stage rules, slide 5 number rules, slide 3 diagram boxes: same rule thickness and the same gap to the text below.
- Progress bar and page counter: one position, one size, same on every slide.
- Measure, don't eyeball: script the bounding boxes (gaps, alignment to the left edge, equal spacing) with Playwright and paste the numbers.
