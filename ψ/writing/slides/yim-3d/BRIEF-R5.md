# Brief round 5 for Osaa: restore the fleet slide, architecture on its own, Rikyu type

From Dobby, 2026-11-01. Yim, verbatim: "ไม่เอา เอาไสลด์เดิมกลับมาและหน้าสถาปัตยกรรมแยกหน้า"

1. **Restore the fleet slide** ("ฝูงของยิ้ม ทำงานกันยังไง") exactly as it was at commit `86e2829`
   (`git show 86e2829:"ψ/writing/slides/yim-3d/deck.html"`): the three rows with their particle scenes and the same words, including the
   tools footnote. Only restyle it to your round-3 type scale/grid (footnote >= 30px). Do not drop or rewrite any sentence.
2. **Architecture = its own slide, right after the fleet slide.** Keep the labelled diagram you built in round 3, move it there, with
   the heading "สถาปัตยกรรมของฝูง" (or shorter). The slide order becomes: stages · unlock · fleet · architecture · ฝูงบริหารแบบบริษัท · shift ring · results · close (8 slides).
   Timing must stay near 9 min: architecture slide ~45 s; shave the rest from notes, put a timing table in REPORT.md.
3. **Fonts: Rikyu Labs type system (Yim asked earlier, not done in round 3).** `~/hello-oracle/ψ/design-systems/rikyu-labs/slide-kit/tokens/tokens.css` L39-41:
   Satoshi + IBM Plex Sans Thai for everything; Source Serif 4 + Noto Serif Thai for at most one editorial line. Bundle woff2 into `vendor/fonts/`, note licences.
4. Run impeccable critique + polish as a separate pass this time and list what it changed.

Acceptance: shot.py prints `1 []` to `8 []`; offline proof with `document.fonts.check('40px Satoshi')` and `('40px "IBM Plex Sans Thai"')` both true and `__world` truthy;
negative control (rename vendor/) shows all text; no `[—–]` on screen; restored fleet slide text diffs clean against 86e2829 (show the diff command and its output).

- Word rule (Yim): never use the Thai word "ด่าน". Slide 4 rule line becomes "กฎที่เป็นตัวหนังสือจะถูกลืม ทำให้เป็นกลไกที่บังคับเอง". Check all on-screen text and notes for ด่าน.
