# REPORT: yim-3d deck, round 2 (2026-11-01)

โอซ่าเขียนเองนะคะ

What's in this folder:
- `deck.html`: still one file, now with **6 slides**. The new slide 3 is "ฝูงของยิ้มทำงานกันยังไง".
- `DESIGN-NOTES.md`: 8 moves from what we studied, each with its source file.
- `b1.png`..`b6.png`: the resting frames.
- `checks/`: the check scripts, the negative-control copies, and the screenshots from those runs.

Nothing was written outside this folder. Round 1's architecture is kept (one world, formations anchored beside the text).
This round is about craft.

## DESIGN-NOTES in short
1. **One world, one mesh, one draw call.** 1000 motes for all 6 slides, no post-processing.
2. **The camera tells the story.** The poses run wide → push in on the team → down into the house → up over the day →
   pull back over everything made → close on the node that lights the room. Each slide change is a single 850 ms move
   (cubic ease in out), and camera, formation, colour and fog move together.
3. **Ma as code.** Every mote is projected to the screen each frame and fades out within 40 px of any word. No geometry
   passes under text, even mid-move.
4. **Contrast is measured, not eyeballed.** We take the worst WCAG ratio behind every text box at 7 points in every slide
   change.
5. **Motion has a job.** Text enters once (870 ms total). Nothing loops behind text. Reduced-motion stops the loop.
6. **Colour is meaning.** Amber = Yim and work in motion · ivory = agents · graphite = waiting work and outsiders.
7. **One token source.** The 3D reads the same CSS variables as the HTML (`--mote-*`), so the two cannot drift apart.
8. **Orientation is always visible.** A progress bar runs along the bottom edge.

## Slide 3 (new)
- **Facts:** we used only the "Stage-safe wording" section of `~/hello-oracle/ψ/writing/expo-2026-10/2026-11-01_fleet-facts-for-talk.md`
  (all VERIFIED). The wording is trimmed to fit, but no claim was added.
- **Three rows**, as Dobby's addendum asked: how the buds work together · agents of other people · Yim's personal agent.
- **Bud count:** the slide says "สิบกว่าตัว". There is no number on screen, and the 3D shows no number either.
- **Personal agent:** it shows `[[PERSONAL_AGENT]]` in a dashed amber box (`span.todo`). There is an HTML comment next to it
  for Dobby. We checked the layout with the placeholder because it is longer than "Grok Bot" or "Muse", so either name fits.
- **Left out on purpose:**
  - "Messages to another house are signed": the facts file marks it UNCLEAR.
  - Whose agent it is: the facts file says not to name the person.
  - Both points are in the speaker notes as warnings.

## Acceptance (verbatim)
`uv run -q --with playwright python /private/tmp/claude-502/-Users-yim/5aabf861-4d65-4575-9c86-30c641119993/scratchpad/shot.py deck.html .`
```
1 []
2 []
3 []
4 []
5 []
6 []
```
We opened all 6 PNGs and looked at each one ourselves.

More checks: `uv run -q --with playwright --with pillow python checks/verify.py deck.html <mode>`

**`text`** (on-screen text only, notes excluded):
```
slide 1: dashes=0 emoji=0 min_font=30px placeholder=0
slide 2: dashes=0 emoji=0 min_font=30px placeholder=0
slide 3: dashes=0 emoji=0 min_font=32px placeholder=1
slide 4: dashes=0 emoji=0 min_font=30px placeholder=0
slide 5: dashes=0 emoji=0 min_font=30px placeholder=0
slide 6: dashes=0 emoji=0 min_font=52px placeholder=0
PASS
```
- `min_font` also counts the SVG labels on slide 4 at the size they actually render (viewBox scaled). That check found
  "งานจริง" at 28.9 px, and we raised it to 32.

**`contrast`** (text hidden, screenshot what is behind each box, live mode, sampled at 0/150/300/450/600/900/1500 ms of
every move):
```
slide 1: worst text contrast 6.02:1 (ขั้น 1 @300ms) · at rest 6.02:1
slide 2: worst text contrast 6.07:1 (สามข้อล่าง จากหลัก 5 ข้อ @300ms) · at rest 6.07:1
slide 3: worst text contrast 9.34:1 (ข้อความที่ส่งไปบ้านอื่นต @300ms) · at rest 9.34:1
slide 4: worst text contrast 6.11:1 (พิธีทั้งสามเป็นของ Oracl @300ms) · at rest 6.11:1
slide 5: worst text contrast 9.34:1 (จากคนเรียน กลายเป็นคนสอน @300ms) · at rest 9.34:1
slide 6: worst text contrast 9.0:1 (คุณนัทพาทำ 6 บทเรียนทำตา @300ms) · at rest 9.32:1
MIN 6.02:1  -> PASS (>= 4.5:1)
```
- A text box only counts in a sample once it is at least half visible (effective opacity >= 0.5), because during its
  entrance the text is fading in.

## Negative controls (every check was made to go red at least once)
1. **CDN broken** (`checks/neg-deck.html`):
   - **Decoy:** we copied the deck and pointed the import map at `three@0.0.0-broken`. `grep` found the decoy URL 1 time and
     the real URL 0 times, so we know the decoy landed.
   - **Result:** jsdelivr returned **404** and `window.__world = undefined`, so the 3D module never ran. It failed at the
     layer we intended.
   - All 6 slides still show their full text: the character count per slide is 251 / 270 / 606 / 234 / 226 / 81, and every
     heading has opacity 1.
   - We looked at neg3 (the fleet slide): every line is there, and the left half is plain background.
2. **Clearance off** (`checks/verify.py deck.html contrast-nomask`): every slide drops to 1.0 to 1.7:1 → `MIN 1.0:1 -> FAIL`. So the
   contrast check really can see geometry under text, and the clearance is what keeps it out.
3. **Text check decoy** (`checks/decoy-text.html`): we added an em dash and a 22 px line → `slide 3: dashes=1 ... min_font=22px`
   · `FAIL (2)`.
4. **The instrument went wrong twice before it was right.** We are writing this down because each failure looked exactly
   like a real problem:
   - The first version read the text colours **after** hiding them, so everything came back `[0,0,0,0]` and every slide
     scored 1.06:1, including the run with masking off. A check that cannot tell the two runs apart is broken. It now
     asserts that every colour it reads is opaque.
   - The second version counted the bullet dots as background, and read the boxes while the entrance animation still had
     them offset by 18 px.
   - The same 18 px offset was **a real bug in the deck**: live anchors were measured mid-animation, so the formations sat
     18 px low. Fixed: anchors are now measured with the animation paused.

## Reduced motion
- `verify.py reduced`: `world: True loop frames after 1.5 s: 0`. The world is there, but there is no render loop: one still
  frame per slide.
- CSS animations and transitions are off. Screenshot: `checks/rm3.png`.

## FPS (headless, 1920x1080, pixel ratio cap 1.5, rAF count over 3 s, live mode)
- **Mac GPU** (`ANGLE Metal, Apple M4`): 182 frames / 3 s = **60.7 fps** on every slide. That is the display cap.
- **Weak-GPU stand-in**: we forced software rendering (`--use-angle=swiftshader`, all on the CPU) and got **38.0 to 47.3 fps**
  (slide 2 is the slowest at 38.0, slide 6 the fastest at 47.3).
- **Venue projector laptop:** not tested yet. Software GL is the worst case we could stage here.

## Critique and audit passes
- **How:** we ran two independent reviewers who had not seen DESIGN-NOTES. Their full findings are in `checks/critique-A.md`
  (impeccable + praneet-front) and `checks/audit-B.md` (web-design-guidelines + osaa-design-system).
- **Applied:**
  - Every raw colour outside the token block is now a token: the ring SVG, the letterbox, the notes panel and the counter.
  - The three Three.js lights read tokens (`--light-*`) too.
  - `tok()` now throws on a missing token instead of painting black.
  - A Thai font fallback chain (Noto Sans Thai, Sukhumvit Set, Thonburi), and `nowrap` on the stage titles, so slide 1
    does not wrap offline.
  - Letter-spacing 0 on Thai headings.
  - Slide 3 bullets went from 30 to 32 px, with the same dot colour in all three rows.
  - Dim text raised (graphite 62% to 66%). That is why contrast on slides 1, 2 and 4 went from about 5.1 to about 6.0.
  - The "waiting work" motes are lighter, so the bottleneck pile reads.
  - Alt/Cmd/Ctrl + arrow no longer changes slide.
  - The counter is a live region, and `color-scheme: dark` is set.
- **After these changes:** we re-ran everything (acceptance, text, contrast, nomask, reduced, neg, fps). The numbers above
  are from that run.
- **Not applied, and why:**
  - Bigger 3D formations on slides 1, 2 and 5: it would cost the negative space between scene and text. We would rather
    test this on the real projector first.
  - Making the URL the loudest line on slide 6: the content order is fixed by the brief.
  - Raising line-height to the skill floor: slide 3 has no vertical room left at 32 px.
  - Heading-level semantics (h1 to h2): a stage deck is not read by a screen reader as one page.
  - Animating `#prog` with transform instead of width: it is a 6 px bar.
  - The JS `DUR`/`PAD` values that duplicate CSS values: noted, left as is.

## Two things we would still improve with more time
1. **A still picture for each scene when 3D is not available.** If WebGL or the CDN fails, the text is all there, but the
   left half of slide 3 (and the scene areas on slides 1, 5 and 6) is just plain background. We would put a small inline
   SVG drawing of each scene behind the `.anc` boxes and hide it once the 3D comes up, so the composition still holds
   offline.
2. **Offline fonts and a run on the real machine.** Bai Jamjuree and Sarabun still load from Google Fonts. We would put
   the fonts and three.js inside the file (or next to it), then do one run on the venue laptop and projector to measure
   real FPS and contrast under a washed-out projector.

— Osaa (Oracle AI)
