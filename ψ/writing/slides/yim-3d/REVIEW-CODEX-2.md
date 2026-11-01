# Independent second review: Yim's eight-slide deck

Reviewed 1 November 2026 for AI Expo, 6 November. Reviewed the current `deck.html`, `vendor/riso.js`, local font assets, all supplied `b1.png`–`b8.png`, `BRIEF.md`, `BRIEF-R2.md`, and `REVIEW-CODEX.md`. **Facts** below means `/Users/yim/hello-oracle/ψ/writing/expo-2026-10/2026-11-01_fleet-facts-for-talk.md`; **Rules** means the adjacent `2026-11-01_fleet-rules-candidates.md`. Also checked the cited Part 2 course's command text and local registry-copy references. Only this review was written. The read-only request overrides the design skill's project-initialization workflow.

This is a source and screenshot review with limited executable checks, not a live-browser certification. Ego failed to start under the sandbox (`Failed to start ego lite`, macOS XPC connection errors). No browser console, GPU benchmark, context-loss experiment, or ten-minute soak was obtained in this review. Prior reports are not independent proof of the current build. Screenshot b5 is demonstrably older than the current HTML.

## Findings ranked by severity

### High — S5: three incompatible registry stories, with unsupported new counts

**Evidence:** `deck.html` S5 displays **15 yaml / 160 skills / 400 learned / 22 decided**, dated 1 November. `b5.png` instead shows **393** learned; `COPY-FOR-REVIEW.md` also says 393. The actual S5 formation still builds `FM.field({count:211,...})`, selects `FM.pick(17,211,900)`, and uses **17 SVG shelf slots**. Notes tell the August **211 / 17** story. Rules backs that historical pair as of 18 August, not the new 400 / 22 count. Facts backs 15 charters, which is not itself a dated count of registry YAML files. No auditable inventory supporting 160, 400, or 22 was found in the reviewed sources. Repeated copy is not measurement.

**Fix:** choose one dated snapshot and save its counting method and inventory. Either restore the explicitly historical 211/17 story or substantiate the November counts. Generate text, shelf, formation and notes from the same values; alternatively make the illustration explicitly non-counting. Regenerate b5 after settling the copy. Do not silently round 393 to 400 without “ประมาณ”.

### High — S7: the results still lack an evidence trail

**Evidence:** 135 articles, five publicly usable apps, three course parts and stock/SKU analysis “ในหนึ่งนาที” remain brief-backed assertions. Notes claim a 1 November count but provide no article inventory, five app links, course outline or timed workload. Facts' older 123-article public mirror has a different scope/date and neither proves nor disproves 135. “คนอื่นใช้ได้” establishes availability as the intended claim; decorative orbiting users do not establish adoption.

**Fix:** attach a dated published-article count, the five app names/public links, and the three-part outline. Define input size and start/end conditions for the minute claim and retain a reproducible timing, or remove that duration. Add an on-screen as-of date. Support the personal transformation with one concrete before/after example rather than treating counts as proof of causality.

### High — S1–S8: mid-talk WebGL loss can remove the readable paper background

**Evidence:** `html.riso-on #stage` makes the stage transparent; the canvas supplies its light paper. The initialization catch removes `riso-on`, correctly restoring CSS paper if setup throws. There is no deck-level `webglcontextlost` handler, however, and later frame/event callbacks are outside that catch. If the canvas clears or stops rendering during context loss, dark text can be left over the dark body or a failed canvas. Pressing S still calls `stillFrame()`, so it is not a renderer-independent emergency fallback. Three.js's internal context recovery is not a guarantee of a legible interim screen.

**Fix:** on context loss or render exception, stop drawing, hide the canvas, remove `riso-on`, and retain the HTML/SVG deck on opaque CSS backgrounds. Add an explicit renderer-off fallback key. Test failure after initialization, including on S8, then recovery. This is a source-derived risk, not an observed browser failure in this review.

### Medium — S2, S3 and S5: autonomy and reliability claims contradict each other

**Evidence:** S2 says “AI ไม่ตัดสินแทน”; S5 explicitly says Dobby decides small matters. Facts supports the latter and human authority for consequential/irreversible work. “ไม่มีอะไรหาย”, “งานทุกชิ้น…ย้อนดูได้เสมอ” and “ครั้งต่อไปจึงง่ายกว่าเดิม” imply guarantees beyond file-based memory. Facts includes a real silent-handoff failure. The architecture addition repeats losslessness as stage wording, but that does not prove it operationally.

**Fix:** mark the three ARRA lines as principles and qualify their explanations: “บันทึกงานไว้ให้ย้อนดูได้”, “เรื่องสำคัญคนตัดสิน”, “เก็บบริบทไว้ใช้ครั้งต่อไป”. Bridge S1 to S5 with “งานประจำเดินต่อได้ เรื่องใหญ่ยังรอยิ้ม”. Preserve the principle's attribution while avoiding a promise of perfect recall.

### Medium — S1–S8: weak-laptop performance remains unproven; DPR is uncapped

**Evidence:** the renderer now updates 400 instances instead of the old 1,000 and uses a low-resolution separation pass, both useful improvements. But `vendor/riso.js:242` sizes output to stage size × actual DPR, without BRIEF-R2's 1.5 cap. A 1920×1080 CSS viewport at DPR 2 yields 3840×2160 output. There is a 2048² shadow map, a scene pass and a full-output print pass; “one InstancedMesh” does not mean one total draw call. Formation functions repeatedly allocate rings, arrays and objects inside the per-instance loop. No current FPS was independently measured.

**Fix:** provide a rehearsed low-power mode (lower output budget and shadows, while preserving integer dither cells), hoist common formation calculations out of the instance loop, and benchmark the actual projector laptop. S / `?still` already avoids continuous rendering and is the practical normal-operation fallback. Start in still mode if venue performance is uncertain.

### Medium — S3–S6: hall readability and jargon still need selective trimming

**Evidence:** main type is now strong: headings 72px, leads 48px, body 36px, captions 30px at 1920. At 1280-wide output those become 48/32/24/20px. S6's 36-unit SVG sublabels are additionally scaled by 800/900, yielding 32 stage pixels, about 21px at 1280. b3 remains a dense three-row explanation with a long approval sentence; b5 adds “Registry”, “yaml”, “skills” and an unexplained Dobby. These implementation terms interrupt the non-engineer story. b4 has ample unused lower space while important diagram sublabels remain 30px.

**Fix:** on S5 say “ทะเบียนทีม / ทะเบียนทักษะ” and move YAML to notes; introduce Dobby once as the coordinator. On S3 shorten the approval sentence or move its explanation to the architecture walkthrough. Enlarge S4's important labels using its available space. Explain agent = ผู้ช่วย AI, Discord = ห้องทำงานทีม, ψ/ = แฟ้มบันทึกงาน, SKU = รหัสสินค้า orally. Essential labels should be nearer 36–44 stage pixels; verify from the actual back row.

### Medium — S1–S8: N exposes unresolved backstage instructions

**Evidence:** N toggles `.shownotes` on the same projected document, not a presenter-only window. Notes still contain the /forward confirmation, running-order question, prohibitions and internal cues. S6 says to point at the hospital/factory sentence that is no longer on screen. Its broad hospital/factory claim survives in the spoken script despite being removed from the visual.

**Fix:** resolve the handoff and lesson wording, remove stale pointing instructions, and use printed or separate presenter notes. Treat N as rehearsal-only on a mirrored projector. Rewrite the hospital sentence as an analogy. Timing itself is improved: notes allocate 1.5 + .75 + 1.5 + .75 + 1.25 + 1.5 + 1.25 + .5 = **9 minutes**, leaving one minute in a ten-minute slot.

### Low — S1–S8: two rendering lifecycle edge cases remain

**Evidence:** `stillFrame()` sets `tStart = -1e9`; resuming S therefore completes an interrupted morph rather than continuing it, and time-driven formations jump to elapsed wall time. The deck also owns an unconditional rAF scheduler, bypassing mount's visibility/pause machinery. In still mode it avoids rendering but continues scheduling callbacks. Separately, mount's DPR-change handler can resize/clear the canvas, but with no `draw` callback its `redraw()` does nothing; the deck only redraws on its own resize event. A DPR-only change without a window resize can leave a stale/blank still frame.

**Fix:** separate slide-local time from morph time, pause/resume the presentation clock deliberately, and use a single loop owner. Wire mount's `onResize` to remeasure and repaint in still/capture mode, including DPR-only changes. Cancel idle rAF and resume on state changes. These are code-derived edge cases, not measured failures.

## Complete on-screen claims and number ledger

“Supported” here means the supplied source records it, not that every fleet subsystem was independently audited. “Brief-only” means approved/requested wording without an evidence artifact. Personal testimony, principles and analogies are distinguished from measurable facts. Repeated claims across slides are grouped explicitly.

| Slide | Claim or number | Evidence and disposition |
|---|---|---|
| 1 | สุทธิณี เทพปริยะพล (ยิ้ม), PM, not engineer | Brief and user's biography; supported as supplied identity. |
| 1 | Three stages, numbered 1–3 | Narrative structure in BRIEF; not a universal maturity model. |
| 1 | Yim was AI's memory; chat work required retelling | Brief-only personal testimony. Give one incident and say “ตอนนั้น”. |
| 1 | AI could do more but every task waited for Yim's orders/checks | Personal testimony, not measured queue data. The note still requests an example rather than supplying one. |
| 1 | Work continues without Yim through multiple agents and ARRA methods | Facts supports roles/handoffs/autonomy tiers; qualify to authorized routine work. |
| 2 | Several agents work concurrently, have roles and check each other | Facts §1 supports the workflow and independent review; not a throughput guarantee. |
| 2, 3 | Nothing is lost; every item is recorded and always retrievable | Brief/Facts stage wording, but unbacked as a reliability guarantee. |
| 2 | AI does not decide; people decide; work knowledge remains ours | Philosophy in BRIEF. Literal no-autonomy reading conflicts with Facts' tiers and S5. Ownership is not a verified legal conclusion. |
| 2 | We ask, it remembers; next time becomes easier | Brief-backed principle/aspiration; no recall or ease measurement. |
| 2 | Three displayed principles from five ARRA Oracle principles | BRIEF supports attribution/count; complete primary five-principle text was not established in this review. Numerals 1–3 enumerate them. |
| 3, 4 | More than ten agents, on an always-on machine | Facts §0 and architecture addition support this stage-safe scope. Not an exact concurrent-running count or uptime measurement. |
| 3, 4 | Discord is the central hub; Yim orders/sees everyone's work there | Explicit final Facts addition supports the intended workflow; “every” is not an audited coverage metric. |
| 3, 4 | Shared memory is files | Facts §1/architecture supports canonical files. |
| 3 | Planner, builder and checker are distinct; human approves | Facts' final coding line explicitly approves this statement. Approval/review scope is risk-based in the underlying memo. |
| 3, 4 | Other people's agents can talk but cannot act in our system themselves; human approval gates action | Facts stage-safe wording and guest-lane rules support the boundary, not an unconditional security guarantee. |
| 3 | Each guest has its own key with limited capabilities | Facts §2 supports allowlists and deny-by-default targets. |
| 3, 4 | Grok, Dots and Muse connect and can ask fleet agents to work | Facts' verbatim Yim correction and final wording support all three. Correctly omits generalizing Grok's rate cap to all three. |
| 3 | T3, Pi; Claude plans, Codex implements/reviews separately; Linear | Facts' final coding line and BRIEF-R2 final addendum support this footnote. |
| 4 | Yim uses Mac/mobile → Discord → always-on execution → file memory; personal/external-agent edges | Facts architecture recommendation supports this high-level diagram. Does not establish Discord as the internal file-handoff transport. |
| 5 | Fleet is managed like a company | Analogy grounded in Rules' orchestration section. |
| 5 | Three decision tiers: small Dobby decides/reports; medium together; big/irreversible Yim | Directly supported by Facts §1 and Rules. |
| 5 | Registries record who can do what and what was learned | Rules supports registries and their purpose. |
| 5 | Fleet registry 15 YAML | Facts supports 15 charters, not this exact current file-count measure. Needs inventory/scope. |
| 5 | Skill registry 160 skills | Local copy repeats it; no substantiating inventory in reviewed sources. Unverified. |
| 5 | 400 learned, 22 decided, counted 1 November 2026 | Unverified current counts/date; b5 and local copy say 393, illustration/notes say historical 211/17. See high finding. |
| 5 | Rules came from actual failures; saying done is insufficient; open the real artifact | Rules cites the 31 July unchanged-file incident. Supported as an incident-derived practice. |
| 5 | Written rules get forgotten; turn them into enforced mechanisms | Rules cites the 8–14 August rediscovery incident. Supported lesson; soften universal wording if read as all rules always fail. |
| 6 | AI work resembles shifts; previous managers already know the method | Useful analogy/rhetorical invitation, not a demonstrated universal fact. |
| 6 | Four phases: recap → work → forward → rrr; ψ/ handover notes | BRIEF and cited `part2-working-with-ai.html` command/hand-off text support the cycle. Four phases include three named rituals. |
| 6 | Three rituals belong to Nat's Oracle Protocol | Brief-backed attribution; course confirms command usage, not independent provenance. Match to the event's six lessons remains an explicit note TODO. |
| 7 | 135 articles based on real work at productize.life | Brief-only count plus personal testimony; no dated inventory located. |
| 7 | Five apps others can use | Brief-only count/availability claim; no five-link usability evidence located. |
| 7 | Stock and SKU analysis in one minute | Unsupported performance claim; workload and timing absent. |
| 7 | Three course parts; learner became teacher | Brief-only count; personal trajectory is testimony. Attach outline/example. |
| 7 | Previously impossible work, all expanded from Yim's existing knowledge by agents | Personal causal interpretation; output totals do not establish it. Supply one concrete example. |
| 8 | ถ้ายิ้มทำได้ คุณก็ทำได้ | Motivational invitation; appropriate, not a literal guarantee for every audience member. |
| 8 | Nat leads six lessons at aiexpo.buildwithoracle.com | BRIEF supports planned count/address. Current public availability and final running order not verified here. |
| All | Eight slides, counter 1/8–8/8; S still control | Direct source/mock-DOM support. Structural numbers, not outcome metrics. Decorative fleet rings are illustrative, not roster counts; S5's count-specific illustration is separately flagged. |

## What changed since REVIEW-CODEX.md

| Previous finding | Current status |
|---|---|
| Unsupported results metrics | **Remains**, now S7; S5 adds new unsupported counts. |
| Missing labeled fleet architecture | **Fixed** by S4's HTML/SVG diagram. S3's detailed prose remains dense. |
| Remote Three.js/fonts and no still switch | **Fixed for the bundled folder**: local classic scripts, local WOFF2, S button/key/query. Ship `deck.html` together with `vendor/`; the HTML alone is not self-contained. |
| Expensive fixed render surface | **Partly fixed**: follows stage output and fewer instances; uncapped DPR and new print/shadow work still need venue measurement. |
| Small text / bad hospital line break | **Improved**: body 36, captions 30, clear Thai phrase breaks. Hospital paragraph removed from screen; spoken notes still contain it. |
| Absolute claims | **Remains**; S5 now makes the autonomy contradiction explicit. |
| Projected notes / >10-minute script | **Partly fixed**: nine-minute allocation; projected backstage notes and unresolved questions remain. |
| Big numbers omitted from exclusion | **Fixed in source**: `.num` is measured and the print shader applies padded knockout regions. b7 shows clear numbers. Live transition coverage not verified. |
| Repeated boundary morphs, held keys, static reduced-motion preference | **Fixed in source**: same-index guard, repeat guard, media-query change listener. Hash changes still do not navigate; optional unless URL navigation is expected. |
| No context-loss fallback | **Remains**, with greater contrast consequences because paper now comes from WebGL. |

## Runtime, JS and offline assessment

- Syntax compilation passed for inline scripts, `vendor/riso.js` and `vendor/three.iife.js` using Node's parser. Every referenced local script, stylesheet and font exists. The deck has no runtime CDN dependency; an unavailable CDN should not affect this bundled version. Fonts/layout can still differ if the vendor folder is omitted.
- Executed the actual navigation script in a minimal mock DOM: Right, Space, PageDown, Left, PageUp, Home, End, bounds, repeat suppression, n/N and s/S passed. At a mocked 1024×768/DPR1 viewport, fit produced scale .533333, left 0, top 96. These checks do not prove browser event delivery, font metrics or GPU behavior.
- Startup failure is sensibly isolated: navigation runs before vendor scripts; missing globals or a throwing renderer setup reaches the catch, restores opaque stage backgrounds and sets `__world=false`. Local resource failures and the intentional warning can appear in the console. **No claim of a clean browser console is made.** A shader compilation failure that is logged rather than thrown also needs browser testing.
- Morphs use elapsed time and snapshot current instance/camera/color state, so interrupted transitions have a reasonable basis. The nominal duration is 850ms. Text delay/animation and background timing differ; do not call every effect exactly synchronized. Still-mode time reset is covered above.
- Normal resizing remeasures the current slide and redraws still frames. Mount also schedules resize work, but equal dimensions avoid render-target reallocation. Replaced separation targets are disposed. The DPR-only still redraw edge is separate.
- No obvious unbounded retained-memory leak: fixed 400-instance buffers, bounded per-slide caches, one renderer, and one-time listeners. Temporary per-frame arrays/objects can cause GC pauses. No ten-minute heap/GPU soak was performed; lack of teardown alone is not evidence of a leak during one talk.

## Screenshot readability and story

All eight screenshots were inspected. Black/near-black type over light paper is substantially clearer than the first deck. Nominal CSS contrast is about 16:1 for main ink on paper, 10:1 for body ink and 7:1 for caption ink; main ink on the closing sabi background is about 9:1. These are token-level estimates, not projector measurements. The light tan accent is appropriately a highlight/rule rather than essential pale text. Grain and dither can still soften or shimmer through projector rescaling; software pixel alignment cannot guarantee physical projector alignment.

- **b1:** strong three-stage overview; Thai phrases and marks are intact. Good memory → bottleneck → team framing.
- **b2:** readable hierarchy and separation from 3D; principles need the factual qualifications above.
- **b3:** weakest reading load. Text is clear in the PNG but asks listeners to read three systems and a long policy sentence while hearing the speaker.
- **b4:** labeled architecture fixes the earlier comprehension gap. Keep the walkthrough to the main path; do not read every box. Small labels could grow.
- **b5:** company metaphor is useful, but three diagrams plus registry vocabulary and four metrics crowd the explanation. Screenshot is stale at 393. The 17-slot shelf visibly conflicts with 22 decisions.
- **b6:** familiar shift cycle restores the human story. Thai line breaks are intentional; commands are secondary but small at hall scale. Explain the saved handover note before saying ψ/.
- **b7:** clear numbers, uncluttered text and sensible Thai breaks. Evidence, rather than layout, is the outstanding problem.
- **b8:** strongest closing. Large Thai serif text, intact marks, a readable invitation and address. The illustration stays beside the message.

The requested arc is present: memory/bottleneck (1) → team and ARRA practices (2) → fleet (3–4) → management method (5) → shift cycle (6) → results (7) → invitation (8). The main story risk is spending too much of nine minutes explaining the machinery in 3–5. Keep S4 to its planned 45 seconds, translate S5's registry jargon, and use one real PM bottleneck incident to connect the opening to the results. This preserves Yim's authority as the user of the system and makes the final invitation credible.

Verdict: ship after fixes
