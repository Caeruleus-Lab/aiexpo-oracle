# Brief for Osaa: Yim's 3D talk deck, AI Expo 2026 (Fri 6 Nov, Builder Stage)

From Dobby, 2026-11-01. Yim wants her own beautiful deck, not Nat's template, with a 3D signature
in the spirit of the torii-gate hero Osaa built for jizo-landing (commit 59f23a5).

## MUST (acceptance)
- Output: one self-contained file `deck.html` in this folder (`ψ/writing/slides/yim-3d/`). Write nothing outside this folder.
- 5 slides, 1920x1080 stage scaled to the window, keys: → / Space next, ← prev, Home/End, N toggles speaker notes.
  Content and notes below are fixed; you may cut words for layout but not change claims or numbers.
- 3D: Three.js via import map pinned `https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js` (same as the reference).
  **Content-first:** all text is HTML, never drawn in WebGL; wrap 3D in try/catch so the deck works if WebGL or the CDN fails
  (venue projector laptop, maybe offline). Respect `prefers-reduced-motion`.
- Thai body text. No emoji, no em-dash or en-dash on screen (check `[—–]`). Text must read from the back of a hall: body >= 30px at 1920 wide.
- Acceptance, run it and report the output:
  `uv run -q --with playwright python /private/tmp/claude-502/-Users-yim/5aabf861-4d65-4575-9c86-30c641119993/scratchpad/shot.py deck.html <this folder>`
  → prints `1 []` … `5 []` (no overflow) and writes b1.png..b5.png here. Look at every PNG yourself before you say done.
  Negative control: also screenshot with the import map URL broken (temp copy) and confirm all 5 slides still show their text.

## HINT (advisory)
- Reference source: `ref/jizo-gate-index.astro` (InstancedMesh torii + drifting motes, camera dolly, ~1 draw call). 3D playbook: `~/hello-oracle/ψ/learn/somtor/`.
- One 3D world across the whole talk, with the camera moving per slide, beats five separate effects. Idea that fits the story:
  a single glowing node (Yim) that the work piles onto (stage 2: bottleneck), then splits into a small constellation of
  agents passing light between them (stage 3), which becomes the 4-node shift ring on slide 3. Your call.
- Palette is yours. Nat's stage deck is graphite + amber (Bai Jamjuree + Sarabun); staying near it keeps the hand-off smooth, but not required.

## Content (from yim-bridge.html in the parent folder; open it for the exact text and notes)
1. Name line: สุทธิณี เทพปริยะพล (ยิ้ม) · product manager ไม่ใช่วิศวกร. Three stages:
   ขั้น 1 ยิ้มเป็นความจำให้ AI (คุยในแชตทีละงาน ทุกครั้งต้องเล่าใหม่) · ขั้น 2 ยิ้มกลายเป็นคอขวด (AI ทำได้มากขึ้น แต่ทุกงานรอยิ้มสั่ง รอยิ้มตรวจ) · ขั้น 3 งานเดินได้โดยไม่รอยิ้ม (ทีม AI หลายตัว กับวิธีทำงานของ ARRA)
2. สิ่งที่ปลดล็อก: ทีม AI กับวิธีทำงาน · + หลายตัว ทำพร้อมกัน (แต่ละตัวมีหน้าที่ และตรวจงานกันเอง) · 1 ไม่มีอะไรหาย · 2 AI ไม่ตัดสินแทน · 3 เราถาม มันจำ · footnote: สามข้อล่าง จากหลัก 5 ข้อของชุมชน ARRA Oracle
3. ทำงานกับ AI เหมือนทำงานเป็นกะ · ring: เข้ากะ /recap → ทำงาน → ออกกะ /forward → ทบทวน /rrr, centre ψ/ บันทึกส่งกะ · line: โรงพยาบาลกับโรงงานไม่ได้ใช้คู่มือส่งงานกัน เขาใช้บันทึกส่งกะ ใครเคยดูแลทีมคน รู้วิธีนี้อยู่แล้ว · footnote: พิธีทั้งสามเป็นของ Oracle Protocol ของคุณนัท
4. งานที่เคยอยากทำ แต่ทำไม่ได้ · 135 บทความ (เล่าจากงานจริงบน productize.life) · 5 แอปที่คนอื่นใช้ได้ (เช่น วิเคราะห์สต็อกและ SKU ในหนึ่งนาที) · 3 Part ของคอร์ส (จากคนเรียน กลายเป็นคนสอน) · line: ทั้งหมดมาจากความรู้งานเดิมของยิ้ม ฝูง agent แค่ขยายมันออกไป
5. ถ้ายิ้มทำได้ คุณก็ทำได้ · คุณนัทพาทำ 6 บทเรียน · ทำตามได้ที่ aiexpo.buildwithoracle.com
Copy every slide's speaker notes from yim-bridge.html.

## Report
Write `REPORT.md` here: what the 3D does per slide, the acceptance output verbatim, negative-control result, anything you could not do.
