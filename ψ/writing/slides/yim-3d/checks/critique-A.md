# Critique A: yim-3d deck (6 slides), design review

Reviewer: Claude (Sonnet 5.5) acting as design director. Date 2026-11-01. Deck and b1..b6.png read in full; BRIEF.md and BRIEF-R2.md checked.
Skills applied:
- impeccable 3.5.0: `skills/impeccable/SKILL.md` (General rules, Color/Typography/Layout/Motion, Absolute bans) and `reference/critique.md` (Assessment A + Cognitive Load Assessment). I also ran its bundled detector as a cross-check: `node .../scripts/detect.mjs --json deck.html` returned exactly 1 hit (`layout-transition`, deck.html line 177, `#prog` transition on `width`). No slop-family hits (no gradient text, no side-stripe, no glass).
- praneet-front 1.0.0: `skills/praneet-front/SKILL.md` (Hard rules 1 to 7, Implementation checklist) and `references/cdn-quickstart.md`. Its prerequisite skill `frontend-design` is not installed here; impeccable covers that role.

Note on two impeccable rules I deliberately do NOT apply: "hero heading clamp <= 6rem" and "primary-accent <= 10%". Both are for web pages read at arm's length; 156px display and amber-heavy graphite are correct for a 1920x1080 hall projection and are the deliberate hand-off palette.

Overall: strong deck. One world, 3D beside text, clearance masking, good contrast on slide 6, consistent grid. Problems are mostly (a) Thai-typography hard rules not yet met, (b) things too small or too dim for the back of a hall, (c) 3D formations scaled for a laptop screen, not a hall.

Findings, ranked by impact on a back-of-hall audience.

---

## 1. [MUST] All slides: Thai font stack has no Thai-capable fallback, and fonts are CDN-only

- What is wrong: `--font-display:"Bai Jamjuree","Sarabun",sans-serif` and `--font-body:"Sarabun","Bai Jamjuree",sans-serif` (deck.html lines 58-59). Fonts come only from the Google Fonts `<link>` (line 20). The brief says the venue laptop may be offline. Offline, every Thai glyph falls to whatever `sans-serif` is, with different widths. Layouts were measured with Bai Jamjuree/Sarabun and are tight in places: slide 1 stage 3 title "งานเดินได้โดยไม่รอยิ้ม" is 505px wide in a 520px column (b1.png, x 1260 to 1765, column ends 1780), so any wider fallback wraps it. Slide 3 row 3 heading is about 886px of about 976px.
- Rule: praneet-front SKILL.md, Hard rule 3 ("NEVER ship a font stack without a Thai-capable fallback ... `'Noto Sans Thai', 'Sukhumvit Set', 'Thonburi', system-ui, sans-serif`") and Implementation checklist (confirm the Thai font loaded, `references/cdn-quickstart.md` width-compare probe).
- Smallest change:
  - CSS: `--font-display:"Bai Jamjuree","Sarabun","Noto Sans Thai","Sukhumvit Set","Thonburi",system-ui,sans-serif;` and `--font-body:"Sarabun","Bai Jamjuree","Noto Sans Thai","Sukhumvit Set","Thonburi",system-ui,sans-serif;`
  - Guard the tightest line: `.stages .t{white-space:nowrap}` (slide 1) so a fallback never wraps it into 2 lines.
  - Better, if time allows: ship the 5 woff2 files next to deck.html and add `@font-face` with `src:local(...), url(fonts/...)` so the stage laptop never depends on the network.
  - Drop the unused `Bai+Jamjuree:wght@500` from the link (weights used: 600, 700).

## 2. [MUST] Slides 1 to 6 headings: negative letter-spacing applied to Thai

- What is wrong: `h1,h2,.display{... letter-spacing:-.01em ...}` (line 79). At 156px that is about -1.6px, at 72px about -0.7px, on Thai combining marks (ิ ี ้ ็ ุ and SARA AM "ำ" in "ทำ", "น้ำ", "ทำงาน", "ทำได้"). It cannot be seen in the screenshots at rest, but it is exactly the case the rule exists for, and it is a one-line fix.
- Rule: praneet-front SKILL.md, Hard rule 2 ("NEVER apply `letter-spacing` to Thai ... force `letter-spacing: normal` on Thai containers"). impeccable SKILL.md Typography floor (>= -0.04em) is satisfied but the Thai rule is stricter.
- Smallest change: `h1,h2,.display,.who .name,.stages .t,.row .t,.ft{letter-spacing:0}` (replace the `-.01em`). If the Latin look matters, scope tracking with `:lang(en)` only.

## 3. [SHOULD] Slide 3: nine bullets sit exactly at the 30px floor, and the dot accent says the wrong thing

- What is wrong: all `.frow li` are 30px / 1.4 (line 127). Slide 3 carries 3 headings + 9 sentences; it is the densest slide and the least readable from the back. There is vertical room: content spans y 265 to 940 of the 888px content box (b3.png) and the right column is 976px wide while the longest bullet is 660px wide. Also `.frow:first-child li::before{background:var(--color-accent)}` (line 129) colours only row 1's dots amber; rows 2 and 3 get `--color-rule` (graphite-700 on graphite-900, about 1.7:1, nearly invisible). The three rows are parallel ideas, so accenting only row 1 reads as "row 1 is the point".
- Rule: impeccable critique.md, Cognitive Load Assessment ("Visual Noise Floor", "Visual hierarchy", chunking); impeccable SKILL.md Color ("verify contrast").
- Smallest change: `.frow li{font-size:34px;line-height:1.4;padding-left:34px}` (estimated total about 857px of 888px, still fits; the longest bullet becomes about 750px, fits). Delete line 129 and set `.frow li::before{background:var(--color-ink-3)}` so all dots match and are visible. Check with the existing screenshot script, since three rows plus the placeholder row width must still fit.

## 4. [SHOULD] Slides 1 and 5 (and 2): 3D formations are tiny for a hall, and slide 2 wastes width

- What is wrong: the formations occupy about 130px (slide 1: three clusters inside 270px boxes, b1.png), about 150px (slide 5 gems and 135-stack inside 230px boxes, b5.png). At projector distance they read as specks; the "lone node, buried node, team" story on slide 1 is the best visual in the deck and it is about 10 percent of the frame. Slide 2: `.unlock{grid-template-columns:1080px ...}` gives the row panels 1080px, but the text inside ends at about 755px, so there is about 330px of dead panel while the 3D column is squeezed to about 600px.
- Rule: impeccable critique.md "Single focus / Visual hierarchy"; impeccable SKILL.md Layout ("Vary spacing for rhythm", do not fill with dead cards).
- Smallest change: `.stages .anc{height:340px}` (slide 1; total height still about 780 of 888). `.big3 .anc{height:280px}` (slide 5; +50 only, because the slide is already about 830 tall). `.unlock{grid-template-columns:900px minmax(0,1fr)}` (slide 2; rows still hold the longest line at 755px; 3D column grows from about 596 to about 676px). No JS change needed because formations size from the `.anc` boxes.

## 5. [SHOULD] Slide 1 (stage 2) and slide 3 (row 2): the "work waiting" colour is almost invisible, and a stray stream runs out of its column

- What is wrong: `--mote-wait:oklch(42% 0.018 260)` (line 52) on graphite-900 is about 2.2:1. This colour is the whole bottleneck metaphor (the pile of work waiting on Yim) and the outsider agent on slide 3. In b1.png the gray pile reads as grit, and the diagonal "work arriving" stream at x 668 to 850, y 360 to 460 starts left of column 2 (column starts x 700) and looks like debris drifting across the gap toward stage 1. Note the same slot is used by the background dust (`dust()` calls `put(..., 1)`), so raising it also raises noise behind text.
- Rule: impeccable SKILL.md Color ("Verify contrast ... large text >= 3:1"; applied here to the key meaning-bearing graphic); impeccable critique.md "Emotional journey" (stage 2 is the emotional low and must be legible).
- Smallest change: add a fourth palette slot for dust and lift the wait colour. CSS: `--mote-wait:oklch(56% 0.018 260); --mote-dust:oklch(34% 0.016 260);` JS: add `'--mote-dust'` / its amber equivalent to `PAL.dark` / `PAL.amber`, and in `dust()` change the last `put(..., 1)` to slot 3. Optionally keep the stream inside its column by starting `sx` at `a1.x - a1.hw * 0.9` (line 460).

## 6. [SHOULD] Slides 1, 2, 4: dim text uses graphite-500, which projectors will wash out

- What is wrong: `--color-ink-3` is graphite-500 (62%). It is used for the greyed-out "ขั้น 1 / ขั้น 2" labels (40px), and for `.foot` on slides 2 and 4 (30px regular weight, b2.png and b4.png bottom-left). Nominal contrast is about 5:1, but a projector lifts black, so real contrast in the hall is much lower, and the 30px regular footnotes are the weakest text in the deck.
- Rule: impeccable SKILL.md Color ("light gray 'for elegance' is the single biggest reason AI designs feel hard to read ... bump toward the ink end").
- Smallest change: `--color-ink-3:oklch(72% 0.014 260)` (about 8:1; graphite-300 would be too close to ink-2). Stages 1 and 2 stay recessed against the amber stage 3 through colour and the grey top rule, not through near-invisible text.

## 7. [SHOULD] Slide 6: the URL is the one action and is not the loudest thing after the headline

- What is wrong: "ทำตามได้ที่ aiexpo.buildwithoracle.com" is on the same 52px line as "ทำตามได้ที่" and the same weight scale as "คุณนัทพาทำ 6 บทเรียน" (b6.png, y 780). The audience will photograph this line, and it ends at x 1032 with room to grow (column is 1060px).
- Rule: impeccable critique.md "Visual hierarchy: is it immediately clear what's most important" and Single focus.
- Smallest change (layout only, wording unchanged): `.close .lead b{display:block;font-size:68px;line-height:1.2;margin-top:var(--space-xs)}`. At 68px the URL is about 845px wide (fits 1060). The `.nw` already prevents breaking inside it. The cream "source" node in the 3D (b6.png, about 1520, 540) is cream on amber (about 1.5:1) and reads as a lumpy cloud while the dark satellites pop; NICE: raise its scale 3.2 to 4.2 in `F[5]` (`put(a.x, a.y, 0, 4.2, 0)`).

## 8. [SHOULD] Thai line-height is below the skill floor on display and body

- What is wrong: `h1,h2,.display` line-height 1.08 (line 79, so `.display` on slide 6 at 156px stays 1.08, about 20px between "ถ้ายิ้มทำได้" and the tone marks of "คุณก็ทำได้"), `.who .name` 1.1 (line 100), body at 1.35 to 1.45: `.row .m` 1.35, `.stages .s` 1.4, `.big3 .note` 1.4, `.frow li` 1.4, `.lead` 1.45. Nothing collides in the screenshots, but slide 6 line 1 to line 2 is the tightest and a line with a below-vowel above a line with tone marks would touch.
- Rule: praneet-front SKILL.md, Hard rule 1 (Thai body 1.6 to 1.8, never below 1.55; headings/display 1.2 to 1.35; test น้ำ ที่ ปั๊ม).
- Smallest change: `.display{line-height:1.2}`, `.who .name{line-height:1.2}`. For body, a stage deck cannot take 1.6 everywhere; apply 1.5 only where there is room: `.lead{line-height:1.5}`, `.stages .s,.big3 .note{line-height:1.5}`. Leave slide 3 at 1.4 after finding 3 (the height budget is spent there) and say so in REPORT.md as a deliberate exception.

## 9. [NICE] Slides 2, 3, 5: the title jumps vertically between slides

- What is wrong: `.frame` uses `align-content:center` for every slide, so the h2 sits at y about 115 on slide 2 (full stack), about 185 on slide 3 and about 165 on slide 5. During the 850ms camera move the title appears to slide up and down between neighbouring slides, which weakens the "one world" feeling.
- Rule: impeccable SKILL.md Layout ("Vary spacing for rhythm" is about content; consistent anchors are the exception); critique.md heuristic 4 (Consistency).
- Smallest change: add `class="frame top"` to slides 2, 3, 5 and `.frame.top{align-content:start;padding-top:var(--space-lg)}` (64px). Slide 2 is already full, so it will not move; slides 3 and 5 move up about 50 to 70px and leave a little more air at the bottom.

## 10. [NICE] Slides 4 and 5: the thesis sentence is the quietest text on the slide

- What is wrong: the key line of slide 4 ("ใครเคยดูแลทีมคน รู้วิธีนี้อยู่แล้ว", flagged in the notes as "จุดที่แรงที่สุดของช่วงยิ้ม") and of slide 5 ("ทั้งหมดมาจากความรู้งานเดิมของยิ้ม ...") is `.lead` in `--color-ink-2` (grey-lavender), subordinate to the numerals and the diagram. Slide 5 also repeats amber four ways (title highlight, three top rules, three numerals, 3D), which flattens the hierarchy; the same slide is the SaaS "big number, small label" template (impeccable Absolute bans, "hero-metric template"), saved here only by real content and the 3D.
- Rule: impeccable SKILL.md Absolute bans (hero-metric template) and Color; critique.md Visual hierarchy.
- Smallest change: `.ring .lead,.big3 + .lead{color:var(--color-ink)}` (use the `.lead` after `.big3`; a class `.lead.key{color:var(--color-ink)}` on both is simpler) and `.big3 .col{border-top-color:var(--color-rule)}` so amber is carried by the numerals only. Also (detector hit, trivial): replace `#prog{transition:width ...}` (line 154) with `transform:scaleX()` and `transform-origin:left`; the 6px bar gives no visible jank, so this is polish only.

---

## Slides with no significant issue

- Slide 4 (shift ring): no layout or type problem. The SVG text scales by about 0.963 (viewBox 900 into about 867px), so the smallest Thai label ("งานจริง", 32 units) renders about 30.8px, above the 30px floor with little margin; do not shrink the SVG. The grey "ทำงาน" node against three amber nodes carries the meaning "three rituals" and matches the footnote. Only findings 1, 2, 6, 8, 10 touch it.
- Slide 2: only findings 4 (column widths), 6 (footnote), 9. Row panels, the "+" row ring and numerals are clear.

## Checks against the constraints (nothing here breaks them)

- Transitions: 850ms move, entrance 200 + 210 stagger + 460 = 870ms, amber slide 300 + 460 = 760ms, all <= 900. Reduced motion handled (`animation:none`, still frame).
- No em/en dash found in on-screen text; `[[PERSONAL_AGENT]]` kept as intended; Thai >= 30px everywhere I measured (the only sub-30 text is the 14px `#count` presenter counter, not Thai).
- All fixes above are CSS or a one-line JS constant; none adds claims, emoji or WebGL text.
