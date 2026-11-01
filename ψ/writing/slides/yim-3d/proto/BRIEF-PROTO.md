# Brief for Osaa: 3 direction prototypes, one slide each

From Dobby, 2026-11-01. Yim, verbatim: "ทำหน้าทดลองแนวละ 1 หน้าได้ -> go".
Purpose: let Yim choose the 3D direction by seeing it on OUR content, not on reference sites.
Read `../RESEARCH-3D.md` first (directions A Sumi, B Fleet Aurora, C Riso, with references and techniques).
Another Osaa run is editing `../deck.html` right now: **do not touch anything outside this `proto/` folder.**

## Make 3 files in this folder: `sumi.html`, `aurora.html`, `riso.html`
- Each = ONE slide, 1920x1080 stage scaled to the window, the SAME content: slide 1 of the deck (the 3 stages:
  ขั้น 1 ยิ้มเป็นความจำให้ AI · ขั้น 2 ยิ้มกลายเป็นคอขวด · ขั้น 3 งานเดินได้โดยไม่รอยิ้ม, with the sub-lines and the name line, copy them from `../deck.html`).
- Bonus if cheap: a second state reached with → (e.g. the "211 → 17" registry moment) so motion between states can be judged. Optional.
- Fonts: Rikyu Labs type (Satoshi + IBM Plex Sans Thai; tokens `~/hello-oracle/ψ/design-systems/rikyu-labs/slide-kit/tokens/tokens.css`). Reuse `../vendor/` for three.js and put any new font files in `proto/vendor/`.
- Text is HTML, content-first, works offline, WebGL failure shows text. No emoji, no `[—–]` on screen, never the word "ด่าน".
- Make each one the best version of its direction, not a sketch: this is what Yim will judge.

## Acceptance
For each file: Playwright screenshot at 1920x1080 → `sumi.png`, `aurora.png`, `riso.png` (+ `-2.png` if you built a second state);
no text overflow; measure FPS over 3 s and write it down. Look at every PNG.
Write `PROTO-REPORT.md` (your voice, เรา/โอซ่า ค่ะ): one paragraph per direction, what you did, FPS, and your own pick with why.
