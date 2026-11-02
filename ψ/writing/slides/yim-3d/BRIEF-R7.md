# Brief round 7 for Osaa: make Riso a shared Rikyu module (slides + landing pages)

From Dobby. Yim, verbatim (arrived after round 6 started, so round 6 missed it): "อยากให้เก็บเป็นรูปแบบที่เอาใช้ทั้ง slide และ landing page ของ rikyu labs ได้"
Round 6 built `~/hello-oracle/ψ/design-systems/rikyu-labs/slide-kit/riso/`. Now:
1. Move it up to `~/hello-oracle/ψ/design-systems/rikyu-labs/riso/` with `git mv` (history kept). Leave `slide-kit/riso/README.md` as a 3-line pointer to the new place.
2. `riso.js` exposes `mount(canvas, options)` that sizes to its container (not only a fixed 1920 stage), handles DPR and resize, `prefers-reduced-motion`, and pauses via IntersectionObserver when off-screen. Keep your round-6 rule that the canvas sits outside any CSS-scaled stage and the whole-cell check.
3. Examples: `example-slide.html` (your round-6 example) and `example-landing.html` (a Rikyu Labs landing hero + one scroll-driven section + a section divider, responsive down to 390 px). Screenshots incl. mobile 390x844; whole-cell check at 390, 1280, 1920.
4. README: slide usage, landing usage, mobile performance budget (measure FPS with CPU throttling if possible), moire rule, still mode, credits (dithering-shader MIT Niccolo Fanton; Klems pattern credit). One-line links from `rikyu-labs/slide-kit/README` and the design-system level README if one exists.
5. Update the AI Expo deck (`deck.html` in this folder) to load the module from its new API if it uses it; re-run shot.py `1 []`..`8 []`.
Commit in hello-oracle with explicit pathspec (`git commit -F <msg> -- ψ/design-systems/rikyu-labs`); a brain-sync daemon may hold `.git/brain-sync.lock` (wait). English message. Don't push. Report in REPORT.md (your voice).
