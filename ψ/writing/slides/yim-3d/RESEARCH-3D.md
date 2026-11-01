# RESEARCH-3D: richer 3D directions for the Yim stage deck

Date: 2026-11-01. Research only; deck.html untouched.
Constraints: one offline HTML, 1920x1080, three r169 bundled, all text in HTML, 3D degrades to stills, weak projector laptop, at most one post pass.

## 0. How to read this (limits of the research)

- My fetch tool returns page text, not rendered pixels. I could not SEE any site. Where I say "what makes it beautiful", the source is stated in the Evidence column: a case study, a repo README, a forum post, or only the page's own text/credits. Osaa should open the links in a real browser before copying any look.
- Codrops (tympanus.net) returned HTTP 403 (Cloudflare "Just a moment") to both the fetch tool and curl. I know the article titles only from search snippets. They are listed as "not opened".
- Feasibility notes marked (mine) are my own engineering judgment, not taken from a source.

## 1. References

Evidence key: OPENED-FULL = page content read with technical substance. OPENED-THIN = page opened but gave only title/credits/text. NOT-OPENED = blocked or snippet only.

| # | Reference | URL | What makes it beautiful | Core technique | Evidence | Feasibility for us |
|---|---|---|---|---|---|---|
| 1 | Igloo Inc (abeto for Bureaux), Awwwards Site of the Year 2024 | https://awwwards.com/igloo-inc-case-study.html (case study); site https://igloo.inc | Everything is real-time light and material: procedural ice blocks, particle "links" that swirl into shapes, chromatic aberration, frost transitions, sound synced to motion. | Custom shaders; particles whose target shapes come from baked VDB volume data compressed to under a typical image; UI/text drawn in WebGL with SDF text; procedural crystal-growth ice. | OPENED-FULL (case study). The site itself returned only its title. | Partly. Steal the idea "precompute shapes offline, ship tiny point clouds as embedded data, morph between them." Do not copy the fluid sim or the SDF UI (our text must stay HTML). |
| 2 | Maxime Heckel, "The magical world of particles with React Three Fiber and shaders" | https://blog.maximeheckel.com/posts/the-magical-world-of-particles-with-react-three-fiber-and-shaders/ | Soft glowing points, curl-noise swirl, warm-to-cool colour shifts, clean box-to-sphere morph. | FBO/GPGPU: positions in a data texture, simulation shader renders to a render target each frame; additive soft sprites; `mix()` between two position textures for morph. States 128x128 = 16,384 particles, and over 1M on an M1. | OPENED-FULL | High. It is the pattern for our "motes morph into formations" with real flow instead of a CPU lerp. (mine) Vanilla three has GPUComputationRenderer in `examples/jsm/misc`; it must be added to the offline bundle. |
| 3 | three.js forum, "Particles Transition Bloom" (Tibi, 2026-01-22) | https://discourse.threejs.org/t/particles-transition-bloom/89382 ; demo https://fwdapps.net/l/particles-transition-2/ | An image dissolves into a curl-noise particle cloud and back; bloom peaks mid-transition and is quiet at rest. | GPGPU + curl noise; bloom strength remapped by transition progress; Vite + GLSL. | OPENED-FULL (forum post). Demo page opened but gave title only. | High. "Bloom only during the move, crisp at rest" is exactly right for slide changes and keeps rest frames sharp for the still-frame fallback. |
| 4 | three.js forum, "GPU Particles" and "Particles swarm" (Tibi, 2026) | https://discourse.threejs.org/t/gpgpu-particles/90558 ; https://discourse.threejs.org/t/particles-swarm/90609 | Soft, smoke-like layered streams; particles sampled from a 3D mesh. | Ping-pong FBOs, curl-noise flow, initial positions in a texture, speed and fade-out logic. | OPENED-FULL (posts); demos at https://fwdapps.net/l/gpu-particles/ and /particle-swarm/ opened with title only. No particle counts or benchmarks were given. | High technique, unknown cost. Treat as a recipe, not a benchmark. |
| 5 | three.js example `webgl_gpgpu_birds` | https://threejs.org/examples/webgl_gpgpu_birds.html | Reference for a flock that reacts to a pointer. | `GPUComputationRenderer`, float textures for position and velocity, 32x32 = 1,024 birds. | OPENED (header only; the code details came from the fetch summary of the example source, so re-verify). | High. Official, MIT, matches r169 file layout. |
| 6 | Niccolo Fanton, Real-time Bayer dithering | https://github.com/niccolofanton/dithering-shader ; demo https://dithering.niccolofanton.dev | A smooth 3D object turns into two-tone dots, like a risograph or newspaper print; the pattern is fixed to the screen. | One full-screen pass: pixelate, luminance, compare against a 4x4 Bayer matrix, grayscale or colour out; optional bloom before or after. MIT. | OPENED-FULL (README) + demo page text | High. (mine) A bare 4x4 Bayer pass is about 30 lines of GLSL and needs no library, so it counts as our one post pass. |
| 7 | Codrops: "Building a Real-Time Dithering Shader", "Animating 160,000 Cubes...Dithering", "Efecto: ASCII and dithering with WebGL shaders" (2026-01-04) | https://tympanus.net/codrops/2026/01/04/efecto-building-real-time-ascii-and-dithering-effects-with-webgl-shaders ; https://tympanus.net/codrops/tag/dithering/ | Same print-like look, plus 160k instanced cubes animated by a threshold map. | Post-processing library + custom shader; instanced cubes with threshold texture and uniforms. | NOT-OPENED (403). Titles and one-line summaries from search snippets only. | Medium-high; read in a browser first. |
| 8 | Codrops: "Crafting a Dreamy Particle Effect with Three.js and GPGPU" (Dominik Fojcik, 2024-12-19) | https://tympanus.net/codrops/2024/12/19/crafting-a-dreamy-particle-effect-with-three-js-and-gpgpu/ | Dreamy, mouse-reactive particle shine. | GPUComputationRenderer with position and velocity textures, velocity shader, post-processing glow. | NOT-OPENED (403); snippet only. | High technique; same family as #2 and #3. |
| 9 | pmndrs/postprocessing | https://github.com/pmndrs/postprocessing | n/a (tool) | Effects list includes Bloom, Depth of Field, God Rays, Dot-Screen pattern, Pixelation, Vignette, LUT. `EffectPass` merges any combination of effects into one pass. | OPENED-FULL (README). three version range not stated on the page. | Medium. Merging effects into one pass fits our budget. Check the peer-dependency range against r169 and the bundle size before adopting. A hand-written single pass is the safer offline option. (mine) |
| 10 | Paper Shaders (paper-design/shaders) | https://github.com/paper-design/shaders ; Codrops interview https://tympanus.net/codrops/?p=124152 (NOT-OPENED, 403) | Soft gradient and dot-pattern canvases made by designers; the interview snippet names a LiquidMetal effect. | Zero-dependency canvas shaders (vanilla JS package `@paper-design/shaders`), Apache-2.0. README names MeshGradient and DotOrbit only. | OPENED-FULL (README). Bundle size not stated. | Medium. Good for a paper-grain or soft-gradient backdrop layer behind the 3D. Check size and whether it runs without network once bundled. |
| 11 | 4C's AD "Brush to Digital" | https://branding.4cs-ad.co.jp | Calm, text-forward Japanese site: ink-wash moon, a three-legged crow, ukiyo-e prints, brush-wipe, "burning" and ripple (uneri) transitions, Tokyo clock in traditional hour names. Copy says the design should never overpower the work. | Not confirmed. The page text shows SVG/WebP assets and named transitions only; I cannot say whether the brush effects are shader, video or CSS. | OPENED-THIN | Mood reference only for Direction A. Do not claim a technique. |
| 12 | Bruno Simon portfolio | https://bruno-simon.com | Handmade, toy-like drivable world with real physics and personality. | three.js (WebGL and WebGPU via TSL), Rapier physics, Blender models; MIT. | OPENED-FULL (page text) | Low for a deck (interactive, heavy). Reference for "charm over polish" only. |
| 13 | Awwwards three.js listing (current winners) | https://www.awwwards.com/websites/three-js/ | Shows what is winning right now. Site of the Day entries seen: Guillaume Colombel portfolio (Oct 28, 2026, also Developer Award), MECHA by widelab (Oct 31, 2026, also Developer Award), Unbelievably Crap (Oct 29), Don't Look Up game (Nov 1). | n/a | OPENED-FULL (listing). Individual sites: Don't Look Up and Unbelievably Crap opened and are flat/typographic, not 3D showpieces; MECHA, Colombel, tesseract.postminimal.agency, 100yearsmonet.com ("3D gallery") returned only titles or text with no visual detail. | Leads only. I could not see their visuals. |

Also opened but not useful as references: ondocollective.jp (static, no WebGL evident), layersoftime.studio (stage-lighting studio, tech not stated), lusion.co and activetheory.net (only titles/nav text came back; Lusion's text lists Oryzo AI, Devin AI, Porsche: Dream Machine, Synthetic Human among its work, with no technique detail).

troika-three-text (SDF text, https://github.com/protectwise/troika/tree/main/packages/troika-three-text) was read and is NOT recommended: it does not mention Thai, does not accept woff2, and defaults to CDN fonts. Our text stays HTML anyway.

## 2. Findings that shape every direction

1. The three "wow" mechanisms that recur across the sources are (a) GPU-simulated particles with curl noise (#2, #3, #4), (b) shapes precomputed offline and morphed (#1, #2), (c) a restrained post effect that is strong only in motion (#3). All three fit one InstancedMesh or one Points draw call plus one small simulation.
2. The current deck is one dark world of 1,000 motes with no post pass and formation anchors beside the text. That is "1 > 20" done correctly, but 1,000 low-poly motes read as sparse confetti. The reference work gets its beauty from density (16k to 100k+ soft points), continuity (flow, not lerp) and light (additive glow), not from more objects.
3. Our deck data is literal and countable: 211 topics, 17 decisions, 135 articles, 5 apps, 3 course parts. A direction that draws those numbers as that many marks is more creative than abstract formations, and it needs no new assets.
4. Palette tension to resolve with Yim: DESIGN-NOTES.md says round 2 deliberately kept graphite plus amber (hand-off to Nat's stage deck) and Bai Jamjuree/Sarabun, not Rikyu Labs. The Rikyu tokens (`rikyu-labs/slide-kit/tokens/tokens.css`) are kuro #1A1A1A, shiro #F7F5F2, sabi #C9B89E, moss #6B7A6B, stone #D9D6CF, with Satoshi + IBM Plex Sans Thai. The tokens note that sabi is not text on shiro (contrast 1.78) and moss is not body text (4.18), so on a light ground both are 3D/ornament colours only. Dark mode is an open decision in the Rikyu README.

## 3. Three concept directions

### A. "Sumi" (calm, Japanese minimal: ma, ink, paper, light)

Visual idea. A sheet of washi-grain paper (shiro) seen in slight perspective, with a very slow parallax. Everything that happens is ink: points rendered as soft ink blots (normal blending, not additive, kuro with a little size and alpha variation by depth for a shallow depth-of-field feel). One single sabi-gold dot is Yim. Moss dots are agents. Empty paper is the content: the deck is mostly ma, and the ink appears only where a sentence needs a picture. Movement is brushed, slow and eased, never bouncy. The sole bright moment is light: a warm sabi glow that crosses the paper.

Story map:
1. AI had no memory. Chats are ink drops that land on the paper, spread, then dry and fade to nothing, while Yim's gold dot stays. Empty paper = forgetting.
2. Yim is the bottleneck. Every faded drop leaves a thread that runs back to the gold dot; the threads pinch into one narrow neck over her.
3. A team of agents plus a way of working. The neck opens: the dot splits and moss dots appear around it, connected by brushed strokes, with space left between them (ma).
4. Fleet architecture. An enso ring is the Discord hub; one still stone at the bottom is the always-on machine; thin horizontal file lines are the shared memory (psi/); personal agents are small dots inside the ring; outside agents are grey dots outside the gap in the ring.
5. Run like a company. Three horizontal rules in stone colour = the tiers by cost of being wrong; dots settle into bands like sediment. 211 small dots (learned) beside 17 larger dots (decided), drawn literally. A failure is a splash that leaves a permanent small stroke: "rules born from failures."
6. Working in shifts. The ring is a clock face. A sabi light sweeps once around it; one paper page is re-inked at each shift, same page each time (the shared notebook).
7. Results. 135 tiny leaf marks in a grid (articles), 5 stones (apps), 3 long strokes (course parts).
8. "If Yim can do it, you can." The paper empties; one gold dot remains, then a second, empty ring appears beside it, left unfilled: the audience's place.

Techniques. Instanced soft sprites or Points with a blot texture, normal blending; the current CPU morph is enough for 3k to 6k points, or GPGPU (ref #2) for flowing strokes; one tileable paper-grain texture on a background plane (or Paper Shaders MeshGradient, ref #10); the existing "ma mask" that fades points near text; an optional faint dust layer. No post pass needed.

Risk and cost. Lowest cost and lowest GPU load. Risks: (1) it can read as flat or as a template if the slow parallax and the ink-drop physics are not done well, so budget polish time there; (2) light-ground projection in a bright room can wash out thin strokes, so keep marks heavier than they look on a laptop and test on the real projector; (3) it departs from the current graphite/amber hand-off to Nat's deck, so Yim must agree to a light deck or a light section; (4) dark mode is an open Rikyu decision, so a kuro ground version (shiro ink on kuro) should be kept as an option.
Inspired by: #11 (mood), #10 (paper/gradient layer), #2 (flow for strokes), Rikyu tokens.

### B. "Fleet Aurora" (bolder: luminous GPU flow in the dark)

Visual idea. A deep kuro room filled with 16k to 65k additive glowing points moving as one continuous curl-noise river. The river is the work. Yim is one steady warm-gold star; ivory points are agents; cool grey dust is waiting work. A single bloom pass is strong only during slide changes and drops to a faint halo at rest (ref #3), so rest frames stay crisp. The camera moves once per slide through the river.

Story map:
1. No memory. Sparse dust; each chat is a flare that flickers and dies; only the gold star holds.
2. Bottleneck. The whole river tries to pass through one gap at the star and jams: a visible funnel, a traffic jam of grey points.
3. Team and way of working. The star splits into several sub-streams; the river fans into a delta.
4. Architecture. A ring attractor is the hub; a steady dense core is the always-on machine; persistent ribbon trails are the shared memory (the trail buffer keeps its path); personal agents orbit; outside agents orbit beyond a visible membrane.
5. Company. The flow separates into lanes by speed: tiers by cost of being wrong (fast lane cheap, slow lane gated). 211 faint nodes and 17 bright crystalline nodes; a failure spawns a bright particle that freezes into a permanent node (a rule).
6. Shifts. The ring rotates like a clock; trails persist through the cycle and are never wiped (the shared notebook).
7. Results. The flow condenses into 135 + 5 + 3 distinct clusters.
8. Close. All streams collapse into one bright point; then it radiates outward toward the audience as the camera pushes through.

Techniques. GPUComputationRenderer 128x128 (16k, default) with a 256x256 (65k) tier behind a quality switch; curl-noise velocity; ping-pong FBOs; soft additive sprites; shapes precomputed offline as small embedded point clouds (ref #1); one bloom pass (hand-written or ref #9) with strength driven by transition progress (ref #3).

Risk and cost. Highest wow and highest risk. Needs float/half-float render targets (some weak or old laptops lack full float, so a half-float fallback and a CPU-morph fallback are required); needs the GPUComputationRenderer addon added to the offline bundle; bloom plus 65k additive points can hurt on integrated graphics, so default to 16k and test on the actual laptop; additive glow behind Thai text threatens the contrast gate (keep the ma mask and the contrast verifier). Closest to the current deck's palette, so least friction with Nat's hand-off.
Inspired by: #1, #2, #3, #4, #5, #9.

### C. "Riso" (mid-bold: dithered print, isometric blocks)

Visual idea. A graphic, risograph-print look on shiro paper: a scene of simple instanced blocks (cubes, slabs, a ring) lit by one directional light and viewed through an orthographic camera, then passed through one Bayer-dither pass (ref #6) that turns shading into two or three ink colours (kuro, sabi, moss) as screen-fixed dots. Shadow bands become visible stripes of dots, so a moving light looks like time passing. It is bold and recognisably "designed", still inside Rikyu colours, and the text stays crisp HTML above the dithered canvas.

Story map:
1. No memory. One block (Yim); small blocks fall, flash and vanish.
2. Bottleneck. Blocks pile into a tower on top of Yim's block; the shadow of the tower is long and dense.
3. Team. The tower unstacks into a small grid of equal blocks.
4. Architecture. An isometric diagram of blocks: ring = hub, large slab = always-on machine, thin file tiles = shared memory, small blocks = personal agents, separate blocks apart = outside agents.
5. Company. Three floors (tiers) of an isometric building; 211 tiny cubes and 17 large ones, literal; a failure cracks a block into a permanent rule tile.
6. Shifts. The light rotates around one cluster and the dither shadow sweeps like a clock hand; the same cluster is re-lit each shift.
7. Results. 135 cubes as a city skyline, 5 towers, 3 slabs.
8. Close. One block lit; the light jumps cube to cube across a grid (a cascade): "you can too."

Techniques. InstancedMesh with MeshLambertMaterial, one directional light, orthographic camera, a custom single full-screen Bayer pass (about 30 lines; ref #6 for the algorithm; also ref #7 for variants), dither pixel size fixed at 3 to 4 px at 1920x1080.

Risk and cost. Low to medium cost; the single pass is cheap. Risks: dither moire or shimmer if the projector or the capture rescales the image (fix by rendering at the native 1920x1080 and using an integer dither cell); isometric blocks may feel like a different brand from "MA x SYSTEMS" if over-played, so keep ma and few blocks; it is a new look to design from zero (more Osaa time than A).
Inspired by: #6, #7, #9.

## 4. Recommendation

Recommend A "Sumi" as the base, with two borrowed set pieces from B (a short curl-noise flow used only for the "bottleneck" jam on slide 2 and the "one dot to light" ending), drawn as ink so they stay on-brand.

Reasons:
1. Brand fit. It is the only direction that is Rikyu Labs by construction (ma, shiro/kuro/sabi/moss, "MA x SYSTEMS"); B is a generic "glowing particles" look that many 2024-2026 sites share.
2. It makes the numbers visible. 211 vs 17, 135 leaves, 5 stones, 3 strokes are each a literal drawing; the audience sees the "company" instead of reading it. This is the creative step the current abstract formations lack.
3. Lowest risk on a weak projector: a few thousand normal-blended sprites, no mandatory post pass, no float-texture dependency, and it degrades to a still frame cleanly.
4. Text legibility is easiest: dark ink on a plain paper ground is the strongest contrast case, and the ma mask already exists.
5. The story's emotional spine (forgetting, the narrow neck, the unfilled ring for the audience) fits quiet imagery better than spectacle; a non-engineer PM speaker is better served by clarity than by shader fireworks.

Conditions: (a) Yim must accept a light ground, or at least a light mode for the deck (this reverses DESIGN-NOTES decision 6), and keep a kuro-ground variant ready; (b) test a printed or projected mock on the real projector early; (c) if Yim wants an unmistakable "wow", pick B at 16k particles, and plan the half-float and CPU fallbacks first.

## 5. Could not verify

- All Codrops URLs: HTTP 403 (Cloudflare challenge) via fetch tool and curl. Their content is from search snippets only (refs #7, #8, #10's interview).
- igloo.inc, lusion.co, activetheory.net, tesseract.postminimal.agency, 100yearsmonet.com, layersoftime.studio, fwdapps.net demos: opened but returned only titles or minimal text (client-rendered). I could not see or describe their visuals.
- Awwwards inspiration pages (Blit Studio logo particles, Plasmatic Isosurface): opened, only tags and credits (WebGL, particles, GLSL); no technique detail.
- Maxime Heckel's volumetric lighting article: page returned only "Loading..." (404 on one guessed URL; the other did not render). Volumetric light is therefore not among the recommended techniques.
- `brunosimonthree/folio-2025` GitHub guess: 404; bruno-simon.com itself opened.
- three.js example list at threejs.org/examples returned no index; slugs other than `webgl_gpgpu_birds` were not checked.
- No frame-rate or particle-count benchmarks exist in any source for a weak laptop. Counts like 16k default and 65k tier are my proposal, not a measured result. Nothing was run on the target hardware.
- Whether pmndrs/postprocessing supports three r169, and its bundle size, were not stated on the page.
- I did not check whether `GPUComputationRenderer` is already inside `vendor/three.module.js` (it is an addon, so probably not).
