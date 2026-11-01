# Brief round 8 for Osaa: space, composition, and review fixes

From Dobby, 2026-11-01. Yim, verbatim: "ยิ้มว่าต้องดูเรื่องการใช้ space ด้วย"

## 1. Space and composition (main job)
Every slide must use the 1920x1080 frame on purpose: content block balanced in the frame, no large accidental empty zone, no crowding at an edge, consistent margins. Measure it, don't eyeball:
- Script per slide with Playwright: bounding box union of all text + the 3D formation's projected box; report % of frame used, empty bands > 25% of height or width, distance of the visual centre of mass from the frame centre (or from the intended grid position), margin consistency (left/right/top/bottom).
- Seen by Dobby on the current b*.png:
  - Slide 4 (architecture): bottom ~40% empty; the diagram sits high. Re-compose to fill (bigger boxes, or diagram centred vertically, or the 3D fleet given real space). Riso arrows look messy: make arrows clean (solid strokes) and keep dots for the 3D only.
  - Slide 6 (shift ring): left column has a big gap between the headline and "ใครเคยดูแลทีมคน รู้วิธีนี้อยู่แล้ว"; group them.
  - Slide 2: the 3D cluster floats in the right half with the beige cube far below; tighten the composition.
  - Slide 5: the shelf still shows 17 slots and a 211-dot field; numbers on screen are now 393 learned, 22 decided. Make the 3D match (or make it unlabelled-abstract without countable slots).
  - Slide 8: the sand flood shows horizontal streaks that read as blur; make the flood clean or a proper riso texture.
- Write the before/after measurements in REPORT.md.

## 2. Review fixes
Apply what Dobby forwards from REVIEW-CODEX-2.md and REVIEW-LANGUAGE.md in this folder (read both if they exist when you start; Dobby will list which language fixes Yim accepted in an addendum below; do NOT change on-screen wording unless listed).

## Acceptance
checks/r5/shot.py → `1 []`…`8 []` at 1920x1080 and 1280x720; offline proof; negative control; no `[—–]`, no "ด่าน"; timing table still ~9:00; space measurements before/after. Look at every PNG. REPORT.md in your voice (เรา/โอซ่า ค่ะ). Don't commit.

## Addendum: approved language fixes (Yim "ok" to Dobby's recommendations, 2026-11-01)
Apply exactly the items marked "Recommend yes" / "Recommend define" in LANGUAGE-DECISIONS.md, using the rewrites in REVIEW-LANGUAGE.md:
1 (slide 2 "เรื่องใหญ่ คนตัดสิน") · 2 (ทุกอย่างมีบันทึก ย้อนกลับไปดูได้, slides 2 and 3) · 3 (define ฝูง once on slide 3 as ทีม AI ของยิ้ม; keep ฝูง after) · 4 (registry units, heading Thai, update stale notes) · 5 (short verb under each command; ψ/ = สมุดส่งกะ; keep /forward until Nat confirms) · 6 (slide 7 headline "งานที่เคยอยากทำ ตอนนี้ทำได้แล้ว") · 7 (slide 3 wording except keep the T3 · Pi · Linear footnote) · notes split into SAY / DON'T / CHECK, add a spoken line on slide 8.
Keep "สถาปัตยกรรม" (optional subtitle "ฝูงต่อกันยังไง"). Keep the 11:00 workshop reference (it is Yim's own morning workshop).
Also apply the High/Medium items of REVIEW-CODEX-2.md that are not wording changes.

## Addendum 2 (Yim ok, 2026-11-01): on screen use "Fleet" instead of "ฝูง" everywhere; define once on slide 3 as "Fleet = ทีม AI ของยิ้ม". Notes may keep ฝูง. (If this arrives after you finished, Dobby applies it.)

## Addendum 3
Yim narrowed the rule (2026-11-01, verbatim): "ส่วนใหญ่ใน slide มันควรเป็นสีทึบนะ ยกเว้นอันที่เราทำเป็น motion ทำเป็น graphic". Flat elements (boxes, labels, chips, table rows, panels, tags) = SOLID ink. Dot screens ONLY for graphics and motion: the Riso 3D print and illustrative figures. Paper texture stays. Apply this to this deck too.
