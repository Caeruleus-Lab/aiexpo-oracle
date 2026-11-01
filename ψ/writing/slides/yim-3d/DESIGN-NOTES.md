# DESIGN-NOTES: yim-3d deck, round 2

Osaa, 2026-11-01. Eight moves I took from my studies, with the source of each and where it lands in `deck.html`.
I wrote these before the build and corrected them after the checks ran, so each "lands as" line describes what the file does now.

## 1. One signature world, not six effects
- **Source:** `~/hello-oracle/fleet/osaa.yaml` → `knowledge.web3d_award_playbook` rule 1 ("1 > 20"). Also
  `~/hello-oracle/ψ/learn/somtor/somtor-3d-playbook/2026-06-27/0201_ARCHITECTURE.md` (the playbook page is one InstancedMesh
  of 820 bodies morphing through 8 formations).
- **Lands as:** one `InstancedMesh` of 1000 motes, 1 draw call, one renderer for all 6 slides. Every slide is a formation
  of the same motes, so the audience watches the same "material" change shape. There is no post-processing and no second mesh.

## 2. The camera tells the story, and moves once per slide
- **Source:** `web3d_award_playbook` rule 2 ("กล้องคือทุกอย่าง"). Also `somtor/.../0201_CODE-SNIPPETS.md` §8: the camera moves,
  the object doesn't.
- **Lands as:** six camera poses that follow the story. Wide establishing shot (memory and bottleneck), push in to the team,
  drop down into the house (fleet), rise over the day (shift ring), pull back to see everything made, then close in on the
  one node that lights the room. Each change is a single timed move: **850 ms**, cubic ease in out. Camera, formation,
  colour and fog all move on the same curve. This replaces round 1's exponential damping, which took about 2 s to settle.

## 3. Ma (間) as code: the 3D knows where the words are
- **Source:** `web3d_award_playbook` rule 6 (restraint and negative space). Also `somtor/.../0201_CODE-SNIPPETS.md`, where the
  `fSparse` "間" formation codes negative space directly.
- **Lands as:** every frame, each mote is projected to the screen. If it comes within 40 px of any heading, line, card or
  list item (30 px around SVG labels), it fades out. So no geometry passes under a word, even in mid-flight. Formations are
  still anchored to empty HTML boxes (`.anc`) at the slide's own camera pose, as in round 1.
- **Proof it works:** `checks/verify.py contrast` gives a worst case of 5.09:1. Turning the clearance off (`?nomask`) drops
  it to 1.0:1. See REPORT.md.

## 4. Contrast is measured, not eyeballed
- **Source:** `~/hello-oracle/ψ/learn/nextlevelbuilder/ui-ux-pro-max-skill/origin/.claude/skills/ui-ux-pro-max/data/ux-guidelines.csv`
  row 36 (Color Contrast, 4.5:1 minimum) and row 76 (Contrast Readability). Also `somtor/.../0201_ARCHITECTURE.md` layer
  `.vignette`: radial darkening at the edges.
- **Lands as:**
  - A soft vignette that darkens the edges and pushes the eye to the centre. It is off on the amber close.
  - A check that hides the text and screenshots what lies behind each text box. It runs at 0, 150, 300, 450, 600, 900 and
    1500 ms of every slide move, then takes the worst WCAG ratio per box.
  - Two design fixes the check forced:
    - The background now turns in 250 ms, and text enters only after 200 ms. Before this, dark text showed on a dark
      background going into the amber close.
    - Anchors are now measured with the entrance animation paused. Before this, formations sat 18 px low in live mode.

## 5. Motion with a job, and nothing that loops behind text
- **Source:** `ux-guidelines.csv` row 8 (Duration Timing), row 9 (Reduced Motion), row 12 (Continuous Animation: decorative
  infinite loops distract), row 99 (Motion Sensitivity).
- **Lands as:**
  - Text enters once per slide, staggered: 200 ms delay, then up to 210 ms stagger, then 460 ms, for 870 ms in all.
  - Idle motion stays inside the formation areas and is slow (dust drift amplitude 0.5 units).
  - `prefers-reduced-motion` stops the render loop completely: 0 loop frames, one still frame per slide, no CSS animation.

## 6. Colour is meaning, and the accent is spent on purpose
- **Source:** `~/hello-oracle/ψ/learn/nazt/relay-decks/2026-06-27/1214_PRINCIPLES.md` A.3 ("Color is meaning, not
  decoration": one entity = one colour on every slide). Also `osaa.yaml` → `knowledge.productize_brand_guideline`: the accent
  is used sparingly, one point per frame.
- **Lands as:** three mote roles, kept the same on every slide.
  - **Amber** (`--mote-key`) = Yim, her knowledge, work in motion: the stage 1/2 node, envelopes, callbacks, the ψ/ drip.
  - **Ivory** (`--mote-agent`) = agents.
  - **Graphite** (`--mote-wait`) = work waiting, outsiders, dust: the bottleneck pile, the other person's agent, actions
    stopped at the gate.
  - On the amber close the roles flip: the key colour becomes light itself, so "one node lights many" reads as light.
- **Kept on purpose:** I did not apply the rest of the productize brand (light paper, Anuphan, no 3D). This deck hands off to
  Nat's graphite and amber stage deck, so I kept Bai Jamjuree, Sarabun and graphite with amber.

## 7. One token source for HTML and WebGL (zero drift)
- **Source:** `osaa-design-system` skill (Primitive → Semantic → Component, no raw hex in components). Also
  `~/hello-oracle/ψ/learn/designil/from-figma-to-code-with-ai/from-figma-to-code-with-ai.md` key insight 5 ("Zero-UI Drift").
- **Lands as:** the CSS now has a primitive tier (`--graphite-*`, `--amber-*`, `--ivory-*`) and a semantic tier
  (`--color-*`, `--mote-*`). The 3D reads `--mote-*` and `--color-paper` / `--color-accent` at runtime, by painting each
  token on a 1 px canvas and reading the pixel back. Change a token, and the HTML and the 3D change together. No colour
  is typed twice.

## 8. Orientation always visible, one idea per slide
- **Source:** `relay-decks/2026-06-27/1214_PRINCIPLES.md` A.2 (one idea per slide) and A.7 (persistent progress bar and
  counter).
- **Lands as:** a 6 px amber progress bar along the bottom edge (ink-coloured on the amber close), next to the existing
  counter. The new fleet slide holds one idea in three rows: a scene on the left, its words on the right, and the eye
  reads scene then line, row by row.

## Slide 3 (new): how the 3D carries the three facts
Each row has its own scene, anchored beside its words.
1. **In the fleet:** about twelve ivory buds on a tilted ring. Flat amber "envelopes" hop between them. Some of the
   hops go through the amber node in the middle (Yim), the picture of "things that cannot be undone wait for Yim". The heading says "สิบกว่าตัว"; the
   scene shows no number.
2. **Other people's agents:**
   - Our house is on the left, a ring-shaped gate stands across the path, and the outside agent is on the right in graphite.
   - Ivory "talk" motes pass through the gate.
   - Graphite "action" chips stop at the gate and fade.
   - Our checked replies (amber) go out.
3. **The personal agent:**
   - One relay line runs between our house and `[[PERSONAL_AGENT]]`.
   - A short ivory train carries the task out. Half a beat later an amber train brings the callback home.
   - A small ledger under the line gains one entry per trip.
   - The design fits either "Grok Bot" or "Muse": the placeholder is longer than both names.

## Audit passes
I ran the critique and audit passes (impeccable + praneet-front, web-design-guidelines + osaa-design-system) as two
independent reviewers who had not seen these notes. Their findings and what I applied are in REPORT.md and
`checks/critique-A.md`, `checks/audit-B.md`.
