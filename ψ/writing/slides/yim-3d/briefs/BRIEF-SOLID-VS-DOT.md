# Brief for Osaa: solid vs dot screen rule for flat (2D) Rikyu Riso elements

From Dobby, 2026-11-01, relaying the SME 101 deck session. Yim, verbatim: "บางอย่างก็ควรทำเป็นสีทึบนะ เช่นป้าย หรือ label"
Problem: the SME 101 deck turns every stone (#D9D6CF) and sabi (#C9B89E) fill into a 3px dot screen, including chips, labels and table cells.
Draft rule from that session, for you to correct and make precise:
- SOLID for anything read as one unit: labels, chips/tags, buttons, part tracker, table header, QR plate, progress bar, the marker band (.riso-hl), error fills.
- DOTS for surfaces that carry an amount or a shape: big slabs, panels behind several lines, chart bars, 3D blocks.
- Never dots behind body text under 30px.

Do:
1. Read /Users/yim/hello-oracle/ψ/design-systems/rikyu-labs/riso/README.md and riso.css, and the brand tokens (slide-kit/tokens/tokens.css, th/guideline.html).
2. Add a section "Solid or dot screen (flat elements)" to riso/README.md: the decision rule (with your corrections and reasons from real risograph practice: ink coverage, legibility, registration), a short element list, minimum sizes (e.g. smallest dot-screened area, smallest text over a screen, contrast numbers), and how to express it in CSS (class names, e.g. `.riso-solid` vs `.riso-screen`, added to riso.css if missing; keep existing classes working).
3. One small visual check: add `example-solid-vs-dot.html` + screenshot showing a chip, a label, a table header, a panel and a chart bar done right; look at it.
Commit in /Users/yim/hello-oracle with explicit pathspec: `git commit -F <msgfile> -- ψ/design-systems/rikyu-labs/riso` (wait while `.git/brain-sync.lock` exists). English message. Don't push. Reply text: the README section name + the class names.

## Addendum (supersedes the draft rule above)
Yim narrowed the rule (2026-11-01, verbatim): "ส่วนใหญ่ใน slide มันควรเป็นสีทึบนะ ยกเว้นอันที่เราทำเป็น motion ทำเป็น graphic". Flat elements (boxes, labels, chips, table rows, panels, tags) = SOLID ink. Dot screens ONLY for graphics and motion: the Riso 3D print and illustrative figures. Paper texture stays.
