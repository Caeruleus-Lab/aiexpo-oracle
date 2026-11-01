# Audit B: yim-3d deck.html (web-design-guidelines + osaa-design-system)

File audited: `ψ/writing/slides/yim-3d/deck.html` (646 lines). Screenshots b1..b6 viewed (b3, b4 inspected closely; layout reads clean).
No file edited. Constraints in the brief were respected (CDN pin, `[[PERSONAL_AGENT]]`, `.notes`, no-emoji, no-dash, Thai >= 30px, transitions <= 900 ms are all left alone).

Method note, audit 1: the skill says to fetch
`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.
The fetch succeeded but the tool returned only a category digest (a11y, focus, animation, typography, content, nav/state, touch, dark mode, i18n, anti-patterns), not the verbatim rule list. I applied those categories plus the Vercel WIG rules as I know them. Output format is `file:line - issue`.
Rule source below: "WIG" = `osaa-maker/skills/web-design-guidelines/SKILL.md` (fetched list); "DS" = `osaa-maker/skills/osaa-design-system/SKILL.md`.

Verified OK (no finding): reduced-motion handled (line 159 and JS `reduce`); animations use transform/opacity only (92-94); no `transition: all`; no `outline:none`; canvas is `aria-hidden`; SVG has `role=img` + `aria-label`; viewport meta present; `lang="th"`; ring SVG Thai text lands at 30.8 px on screen (32 units x 0.962).

---

## Audit 1: web-design-guidelines

1. **SHOULD** `deck.html:311` - keydown handler fires on any modifier combo: Alt+Left / Cmd+Left (browser Back) become "previous slide", Cmd+N-style chords toggle notes, and Left/PageUp/Home/End/N never call `preventDefault`. Rule: WIG Navigation and state, keyboard handlers (do not hijack browser shortcuts). Fix: first line of handler `if(e.metaKey||e.ctrlKey||e.altKey)return;`.

2. **SHOULD** `deck.html:299, 306-310` - slide change is silent to assistive tech: `#count` has no live region, sections have no label. Rule: WIG Accessibility, live regions for async/state updates. Fix: `<div id="count" role="status" aria-live="polite" aria-atomic="true">` and optionally `aria-label` per `<section>` from its heading.

3. **SHOULD** `deck.html:172-173, 187, 288` - heading structure: slide 1 has no heading at all (`<p class="name">`), `<h1>` appears only on slide 6, slides 2-5 are `<h2>`. Rule: WIG Accessibility, semantic HTML / hierarchical headings. Fix: make slide 1 `.name` an `<h1 class="name">` (class already sets size/weight; add `margin:0` is already global) and downgrade slide 6 `.display` to `<h1>` only if slide 1 stays `<h2>`; one consistent level per slide is enough.

4. **NICE** `deck.html:229` - straight quotes `"เสร็จแล้ว"` in on-screen text (also line 242 is fine). Rule: WIG Typography, curly quotes. Fix: replace with curly quotes (U+201C / U+201D), not a dash, so the no-dash rule holds.

5. **NICE** `deck.html:154` - `#prog` animates `width` (layout property), not compositor-only. Rule: WIG Animation, animate transform/opacity only. Fix: `width:100%;transform-origin:left;transform:scaleX(0)` and set `transform:scaleX(n)` in `go()` (line 308); transition `transform`.

6. **NICE** `deck.html:4-5, 20` - head hygiene: no `<meta name="color-scheme" content="dark">` / `theme-color` (dark UI, white flash and light scrollbars outside stage), and no `<link rel="preconnect">` for `fonts.googleapis.com` / `fonts.gstatic.com`. Rule: WIG Dark mode, Performance. Fix: add the two metas and two preconnect links before line 20.

---

## Audit 2: osaa-design-system (zero-drift / token audit)

Zero-drift grep result: `grep -nE '#[0-9a-fA-F]{3,6}'` hits at 67 (`#000`) and 339 (`'#000'`); equivalent raw colours also at 333 and 369-371 (`0x...`) plus ~30 raw `oklch(...)` outside `:root` (below). Component CSS (lines 66-159) references no primitive directly (no `--graphite-*` / `--amber-*` / `--ivory-*` outside `:root`), so tier-skipping in component rules: none found. There is no Component tier (single deck, Tier 1 maturity, acceptable).

7. **MUST** `deck.html:369-371` (and 333) - WebGL uses colours that do not come from a token: `AmbientLight(0xffffff)`, `DirectionalLight(0xffe7c2)`, `DirectionalLight(0xdfe4ee)`, `setClearColor(0x000000,0)`. Every mote colour and BG/fog do come from tokens (`PAL`, `BG`, lines 343-347, all via `--mote-*` / `--color-*`); the three light tints are the gap. Rule: DS Step 5 "ทุกค่าสี trace ไป Semantic/Component token ได้" + brief constraint (all WebGL colour from tokens). Fix: add `--light-fill:oklch(100% 0 0); --light-key:oklch(93% 0.05 80); --light-rim:oklch(90% 0.01 260);` in `:root` and `new THREE.AmbientLight(tok('--light-fill'),1.05)` etc.; clear colour is alpha 0, leave it or use `tok('--color-paper')`.

8. **MUST** `deck.html:67, 156, 158, 245-260` - raw colour values outside the token block. Details: `#000` at 67; `oklch(10% .01 260/.94)` at 156 (near-duplicate of `--color-vignette`); `oklch(55% .014 260)` at 158; inline SVG presentation attributes in the ring: `oklch(60% 0.014 260)` x5 (245, 247-250, arrows/marker), `oklch(36% 0.016 260 / .6)` (246), `oklch(26% 0.016 260)` (251), `oklch(80% 0.15 75)` x4 (251, 254, 258, 260 = `--amber-500`), `oklch(23% 0.014 260)` x4 (254, 256, 258, 260 = `--graphite-850`), `oklch(36% 0.016 260)` (256 = `--graphite-700`). Rule: DS Step 5 zero-drift grep must be empty outside token def. Fix: add semantic tokens (`--color-arrow`, `--color-node`, `--color-node-core`, `--color-notes-bg`, `--color-count`, `--color-stage-bg`) and move SVG paint to CSS classes (`.ring .arrow{stroke:var(--color-arrow);fill:none}`, `.ring .node{fill:var(--color-paper-2)}`, `.ring .node.on{stroke:var(--color-accent)}`, marker `fill` via CSS). `var()` does not work reliably in SVG presentation attributes, so use classes. `#count` colour is also ~3.9:1 on the stage: pick `--color-ink-3` (62% L, about 5:1).

9. **SHOULD** `deck.html:40, 48, 52, 54-56` - semantic tokens defined from raw `oklch()` instead of a primitive (tier skip upward): `--color-paper-2` (duplicates graphite-850 + alpha), `--color-vignette`, `--mote-wait`, `--mote-key-on-amber`, `--mote-wait-on-amber`, `--mote-agent-on-amber`. Rule: DS Step 2 / token architecture Primitive -> Semantic. Fix: add primitives (`--graphite-600`, `--ivory-50`, `--amber-300`, `--bronze-900`...) in the primitive block and reference them; use `color-mix(in oklch, var(--graphite-850) 82%, transparent)` for alpha variants.

10. **SHOULD** `deck.html:338-342` - `tok()` is fail-silent: a missing or misspelled token (or an unparsable colour) leaves `fillStyle` at `'#000'` and returns black without any error, so a drifted `--mote-*` name would render near-invisible motes while the deck looks "fine". Rule: DS Step 5 zero-drift is only as good as the detector (global rule: detectors must be fatal on error). Fix: `const v=rootStyle.getPropertyValue(name).trim(); if(!v) throw new Error('missing token '+name);` (the existing try/catch at 321 already disables 3D visibly via `window.__world=false`).

11. **SHOULD** `deck.html:242, 289` (inline `style="margin-top:var(--space-*)"`); 176-178, 190-193, 197, 244, 264, 274-278 (inline `style="--d:N"`) - inline style attributes. The margin ones are tokenised but still inline; the `--d` stagger index is data, not styling. Rule: DS Step 5 / zero-drift (no inline styling). Fix: `.lead.after-title{margin-top:var(--space-md)}` and `.close .lead{margin-top:var(--space-lg)}`; for `--d` either keep (NICE-level, documented as stagger index) or use `data-d` + `.rv[data-d="1"]{--d:1}`.

12. **SHOULD** `deck.html:116, 117, 131, 156, 327-328` - magic numbers that should be tokens. Type sizes off the scale: `.row .t 48px` (116), `.row .m 32px` (117), `.todo 34px` (131); add `--text-row:48px; --text-row-sub:32px` (or snap to `--text-md`/`--text-sm`; note `.row .m` at 32 sits between sm 30 and md 40). `.notes` uses `3px`, `28px 100px`, `30px` (156) next to existing `--rule-w:4px` and `--text-sm:30px`. JS duplicates CSS values: `DUR = 0.85` (327) vs `--dur-move:850ms`, `PAD = 40` (328) vs `--space-md`; these can drift silently. Fix: in the module, `const DUR = parseFloat(rootStyle.getPropertyValue('--dur-move'))/1000; const PAD = parseFloat(rootStyle.getPropertyValue('--space-md'));`. Lower priority (NICE): layout widths/heights 1080/600/1060/270/200/230/760 (lines 102, 111, 123, 142, 149, 151) could become `--anc-h-*` / `--col-*` tokens, and the ease at line 389 is a cubic smoothstep, not `cubic-bezier(.65,0,.35,1)`, so the "matches" comment is only approximately true.

---

## Priority order

MUST: 7, 8. SHOULD: 1, 2, 3, 9, 10, 11, 12. NICE: 4, 5, 6.
Not flagged on purpose: `--mote-*` definitions themselves (intended), CDN import map, `[[PERSONAL_AGENT]]`, `.notes` text.
