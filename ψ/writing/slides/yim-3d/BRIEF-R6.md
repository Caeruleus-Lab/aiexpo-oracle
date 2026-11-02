# Brief round 6 for Osaa: Riso across the whole deck + a reusable Riso kit for Rikyu Labs

From Dobby, 2026-11-01. Yim, verbatim: "ยิ้มก็ชอบ riso ดูเข้ากับ rikyu labs มาก เก็บไว้ใช้ทำ slide ได้ยาวๆ เลยนะ"

## Part A: the AI Expo deck (`deck.html`, 8 slides) in the Riso direction
- Restyle the whole deck to match `proto/riso.html`: paper ground, Rikyu inks, dithered isometric blocks, Rikyu type. One world across all 8 slides, camera/formations per slide like before, mapped to each story beat (fleet slide, architecture, company slide, shift ring, results, close).
- Keep every word, all speaker notes, the 9-minute timing, offline vendor, still-mode key S, text exclusion, and all round-5 checks.
- Mind Riso's known risk: moire when the projector rescales. Pick a dither cell size that survives 1280x720 and 1920x1080 output, test both, and report it.
- Acceptance: shot.py → `1 []`…`8 []` at 1920x1080 AND a second run at 1280x720 viewport (look for moire); offline proof; negative control; no `[—–]`, no "ด่าน". Rewrite REPORT.md.

## Part B: a reusable Riso module in the Rikyu Labs slide kit
- Target: `/Users/yim/hello-oracle/ψ/design-systems/rikyu-labs/slide-kit/riso/` (new folder). Read the kit first (`README`, `tokens/tokens.css`, `th/guideline.html`, how layouts are chosen) so the module fits how the kit is used by the `rikyu-slides` skill.
- Contents: `riso.js` (the dither post pass + paper + per-ink thresholds + misregistration, vanilla three r169, no build step), `riso.css` (tokens it needs, from the kit's tokens), 2-3 formation helpers (block field, stack/bottleneck, ring), `example.html` (one talk slide using it), `README.md`: when to use, when not, how to add to a deck, performance budget, moire rule, still-mode, credits (dithering-shader MIT by Niccolo Fanton; Klems pattern credit as in our learn notes).
- Do not edit other kit files except adding one line/link in the kit README pointing to `riso/`. Do not edit the rikyu-slides skill; report the line you'd add to it and Dobby will do it.
- Acceptance: `example.html` renders offline (screenshot `riso/example.png`), no overflow.

Write REPORT.md (deck) and `riso/README.md` (kit). Your voice in REPORT (เรา/โอซ่า ค่ะ). Don't commit.

## Addendum (Yim, verbatim, after the run started): "อยากให้เก็บเป็นรูปแบบที่เอาใช้ทั้ง slide และ landing page ของ rikyu labs ได้"
Part B moves up one level: put the module at `/Users/yim/hello-oracle/ψ/design-systems/rikyu-labs/riso/` (shared), not inside slide-kit.
It must work for BOTH a 1920x1080 slide stage AND a responsive landing page section (hero background, section divider, scroll-driven formation):
- `riso.js` exposes a mount(canvas, options) that sizes to its container (not a fixed 1920 stage), handles DPR, reduced-motion, IntersectionObserver pause when off-screen.
- `example-slide.html` (one slide) and `example-landing.html` (hero + one scroll section, responsive to 390px mobile), screenshots of both incl. mobile.
- README: slide usage, landing usage, performance budget for mobile, moire rule, credits. Link it from both the slide-kit README and the design-system README (one line each).
