# Independent review: deck.html

Reviewed 1 November 2026 for Yim's AI Expo talk on 6 November. Read-only review; only this file was written. Evidence: current `deck.html`, `BRIEF.md`, `BRIEF-R2.md`, all six supplied `b1.png`–`b6.png`, and `/Users/yim/hello-oracle/ψ/writing/expo-2026-10/2026-11-01_fleet-facts-for-talk.md` (called **Facts** below). Existing REPORT.md was treated as a prior author's report, not independent proof. The user’s read-only scope overrides the design skill's request to initialize additional project documents.

## Findings, ranked by severity

### High — S5: the strongest proof points lack an auditable evidence trail

**Evidence:** deck.html:293–299 shows 135 articles, 5 publicly usable apps, 3 course parts, and stock/SKU analysis “ในหนึ่งนาที”. BRIEF.md repeats all four, but repetition is not verification. The notes assert a 1 November count without a saved inventory, URLs per app, or benchmark. Facts mentions 123 articles in an older, limited public-memory mirror; that is neither confirmation nor disproof of 135 current published articles. No before/after result establishes the title's “couldn't do before” or the causal attribution to the fleet.

**Fix:** save a dated list/count of published articles, five app names and working public links, and the course outline; label counts “ณ 1 พ.ย. 2026” or recount on talk day. Define and reproduce the one-minute task with a sample input, or remove that duration. Keep personal transformation as Yim's testimony, illustrated with one actual before/after example. “คนอื่นใช้ได้” means available to others, not proven active users; do not upgrade it to “มีผู้ใช้จริง” without evidence.

### High — S3: missing the requested architecture makes the hardest slide difficult to decode

**Evidence:** BRIEF-R2.md's later addendum asks for one five-layer architecture: Yim/Mac/mobile → Discord → box → shared memory, with external/personal-agent edges. deck.html:230–249 and b3.png instead show three unlabeled particle scenes. Discord is a bullet, Yim's cockpit is absent on screen, and no visible connections explain the layers. The bottom illustration depicts one personal-agent endpoint although the words name three. Abstract moving dots do not tell a non-engineer which object is a person, machine, memory, or agent.

**Fix:** use a labeled HTML/SVG architecture diagram with the five requested layers and the three named personal agents grouped at its edge. Keep particles as enhancement. Explain “ฝูง = ทีมผู้ช่วย AI” once and preserve the human approval boundary. This also gives offline mode a meaningful diagram.

### High — S1–S6: text survives offline, but the complete presentation is not self-contained

**Evidence:** Google Fonts is remote (line 21), Three.js is remote (335–340), and no static substitute fills the `.anc` areas. I blocked jsDelivr and both Google font domains with cache disabled: all six slides remained selectable, `__world` was absent, and N still worked. This is a successful content fallback, not complete offline fidelity. Font fallback can change Thai widths, particularly S1's forced `nowrap` titles (124). Static import failure occurs before the module's try/catch, so it does not reach the friendly warning at 663.

**Fix:** package fonts and Three.js locally, or embed them if the single-file requirement is strict. Add static diagrams and an explicit still-mode switch independent of WebGL. Rehearse with a fresh cache and network disabled on the actual laptop; verify Thai fallback layout if remote fonts remain. Use a caught dynamic import if a controlled load-failure diagnostic is wanted.

### Medium — S1–S6: weak-laptop smoothness is not established; rendering remains expensive at small output sizes

**Evidence:** lines 349–351 always allocate a 1920×1080 drawing surface at up to DPR 1.5; I observed a 2880×1620 canvas even with a smaller viewport. There is one mesh and no postprocessing, which is good, but every frame recalculates 1,000 instances, projects each against text boxes, and uploads matrices/colors (598–640). PENTA and formation helpers allocate temporary arrays/objects repeatedly. My two foreground browser samples were 61 frames/3.0015 s (~20.3 fps) and 89/3.0014 s (~29.7 fps). These are environment-specific, not venue benchmarks; REPORT.md's M4 and software-renderer figures do not guarantee the projector laptop's performance.

**Fix:** offer a visible/rehearsable still-mode key or query parameter, size the drawing buffer to the actual display, cap DPR at 1 on weak devices, and precompute per-frame shared formation nodes. Test the entire talk on the venue machine, plugged in, including a ten-minute run. Use still mode if motion stutters.

### Medium — S3, with smaller risks on S1/S2/S4/S5: supporting text is too small for dependable hall reading

**Evidence:** b3.png is the densest image: 32px bullets and a 24px footnote (`.fnote`, line 182). The footnote violates the brief's >=30px requirement and is only 16px when scaled to 1280-wide projection. Other 30–32px secondary copy becomes 20–21px at that width. S3's planning/building/review/approval sentence is a long single line. b4.png splits the hospital sentence after “ไม่ได้ใช้”, separating the negative from its object. All six screenshots retain Thai marks without obvious clipping; S1's bottleneck subtitle breaks into sensible phrases. Main white/amber titles have strong visual contrast; the issue is small gray copy and projector washout, not an observed universal contrast failure.

**Fix:** raise essential supporting text to roughly 38–44px at design resolution and shorten it to fit. Make the S3 footnote at least 30px or move it into notes if the owner permits. Give S4 an intentional short phrasing such as “ส่งกะด้วยบันทึกงาน / กะใหม่อ่านแล้วทำต่อ”. Check at the actual back row, with lights on; desktop screenshots alone cannot certify that distance.

### Medium — S2/S3/S4: absolute wording overstates the source evidence

**Evidence:** “ไม่มีอะไรหาย”, “งานทุกชิ้น…ย้อนดูได้เสมอ”, “AI ไม่ตัดสินแทน”, and “ครั้งต่อไปจึงง่ายกว่าเดิม” (214–216,235) sound like guarantees. Facts documents file-based memory, but also a historical silent handoff failure and tiers where Dobby makes small decisions. Human approval applies especially to irreversible actions; it is not evidence that AI never decides anything. S4's “โรงพยาบาลกับโรงงานไม่ได้ใช้คู่มือส่งงานกัน” (261) is a broad industry assertion with no supporting source in the supplied material.

**Fix:** identify the three ARRA phrases explicitly as working principles, not reliability promises. Use “บันทึกงานไว้ให้ย้อนดูได้”, “เรื่องสำคัญคนตัดสิน”, and “เก็บบริบทไว้ใช้ครั้งต่อไป”. Frame S4 as an analogy: “เหมือนบันทึกส่งกะ: คนใหม่อ่านแล้วทำต่อ”. This makes the autonomy on S1 consistent with approval on S3.

### Medium — S1–S6: notes expose backstage instructions and the script exceeds ten minutes

**Evidence:** N toggles a bottom overlay on the projected stage (178–179,330), not a separate presenter window. It includes unresolved checks and private stage instructions. S1–S5 each allocate 2 minutes and S6 30 seconds: 10:30 before transitions or audience reaction. S4 still says to confirm /forward against Nat's six lessons; S6 still says to ask where Yim's segment fits.

**Fix:** resolve /forward and running-order questions before rehearsal; use separate presenter notes or a printed copy. Trim the first five slides to a combined 8:30–9:00, leaving the closing and handoff room. Rehearse one concrete bottleneck incident instead of trying to tell all the examples suggested in notes.

### Low — S5: the text-clearance selector omits the large numbers

**Evidence:** the claim “no geometry ever passes under a word” is stronger than the implementation. `measure()` selects h1,h2,p,li,.row,svg and SVG text (438), but 135/5/3 are `div.num` (293–295). They therefore receive no exclusion box. b5.png already shows background motes in the open region within/around the 3. Particle centers are masked, not their full projected radii, so the protection is also approximate at text edges.

**Fix:** include `.num` in measured text regions and account for projected mote radius if guaranteeing full exclusion. Sample transition frames in live mode, including S4→S5 and S6→S5.

### Low — S1–S6: navigation and motion have rehearsal edge cases

**Evidence:** `go()` re-emits a slide event even at the first/last boundary or when Home/End selects the current slide (325–330); this starts a redundant morph. Key repeat is not suppressed, so a held remote key can skip slides. Hash is read only at startup; external hash changes do not navigate. `reduce` is read once (344), so changing the OS preference during the session leaves the JS loop running. The module's outer try/catch cannot catch failures in later rAF/event callbacks. There is no app-level context-loss fallback or health indicator.

**Fix:** return early when the target already equals the current slide, handle unwanted key repeats, and listen for reduced-motion changes. Add a renderer health/context-loss handler that exposes the static fallback and stops unnecessary animation. Hash listening is optional unless URL navigation is part of the workflow.

## Complete on-screen claims and number ledger

“Brief-backed” means requested/approved copy, not independently measured truth. “Facts-backed” means the supplied facts memo records evidence; I did not re-audit every underlying fleet file. UI slide counters, step numerals, and decorative node counts are structural, not measured outcomes.

| Slide | Claim / number | Support and disposition |
|---|---|---|
| 1 | สุทธิณี เทพปริยะพล (ยิ้ม); product manager, not engineer | BRIEF.md and user identify the speaker/role. Backed as supplied biography. |
| 1 | Three stages, numbered 1–3 | BRIEF.md's narrative framework, not a universal maturity model. |
| 1 | Yim supplied AI's memory; each chat required retelling | Brief-backed personal testimony; no incident record here. Say “ตอนนั้น” to avoid claiming all AI always forgets. |
| 1 | AI could do more, but all work waited for Yim to order/check | Brief-backed testimony; a concrete bottleneck example is still missing from the notes. |
| 1 | Work proceeds without waiting for Yim, through multiple agents and ARRA methods | Brief-backed; Facts supports roles, handoffs and autonomy tiers. Qualify as routine/authorized work, not all actions. |
| 2 | Multiple agents work concurrently, with distinct roles and cross-review | Brief and Facts §1 support the workflow; no throughput measurement implied. |
| 2 | Nothing is lost; every work item is recorded and always retrievable | Brief-backed principle; unsupported as an absolute operational guarantee. |
| 2 | AI does not decide for us; people decide; work knowledge remains ours | Brief-backed philosophy; Facts supports human authority but expressly permits small autonomous decisions. Ownership is philosophical, not a verified legal claim. |
| 2 | We ask, it remembers; next time is easier | Brief-backed aspiration; files support memory persistence, not guaranteed ease or recall. |
| 2 | Three displayed principles drawn from five ARRA Oracle principles | BRIEF.md repeats 3-of-5; notes name the three. Full five-principle primary text is not supplied here. Attribution is brief-backed, not independently substantiated. |
| 3 | More than ten agents on an always-on machine | Facts §0 explicitly recommends “สิบกว่าตัว”; architecture addition supports the box. Exact concurrently running count remains unknown. Avoid implying measured uptime or that all chartered agents run continuously. |
| 3 | Discord is the hub; Yim orders/sees every agent's work there | Facts' final Discord addition directly supports this wording. “Every” describes the intended hub, not an audited coverage metric. |
| 3 | Shared memory is files; nothing disappears | Files are Facts-backed (§1/architecture); losslessness is only a principle. |
| 3 | Planner, implementer and reviewer are separate; human approves | Facts' final coding line explicitly approves the copy. Facts §1 supplies independent-review and approval scope. |
| 3 | Others' agents may converse but cannot act in our system themselves; human approval required | Facts §2 and stage-safe wording support the intended trust boundary. Not a security penetration-test guarantee. |
| 3 | Each guest has its own limited key | Facts §2 supports per-key allowlists and deny-by-default targets. |
| 3 | Grok, Dots, Muse connect to the fleet and request work themselves | Facts' verbatim Yim correction and final wording support all three. Do not generalize Grok's rate/reply rules to all three; deck correctly omits those. |
| 3 | T3, Pi; Claude plans, Codex builds/reviews separately; Linear | Facts' final coding line and latest BRIEF-R2 addendum explicitly support this footnote. |
| 4 | AI work resembles shifts | An analogy, not an empirical claim. |
| 4 | Hospitals/factories use handover records rather than manuals; anyone managing people knows this | Repeated in BRIEF.md, but unsupported generalization. Reword as an analogy. |
| 4 | Four phases: recap → work → forward → retrospective; shared ψ/ handover files | Brief-backed diagram. Notes cite `part2-working-with-ai.html` pp.3–5 but that underlying course was not audited here. Explain ψ/ as “แฟ้มบันทึกงาน”. |
| 4 | The three rituals belong to Nat's Oracle Protocol | Brief-backed attribution, not independently established in Facts. /forward's match to the live lessons is explicitly unresolved in notes. |
| 5 | 135 articles, drawn from real work, on productize.life | Brief-backed; dated count asserted by notes only. No saved article inventory. Older 123-item mirror in Facts has a different date/scope. Unverified current count. |
| 5 | 5 apps usable by others | Brief-backed; no five-app inventory or usability checks in supplied evidence. Unverified. |
| 5 | Stock/SKU analysis in one minute | Brief-backed; no workload definition, timing or demonstration. Unsupported performance claim. |
| 5 | 3 course parts; learner became teacher | Brief-backed; no course outline or teaching record attached. Count unverified; personal trajectory is testimony. |
| 5 | Previously impossible work; all came from Yim's existing expertise, expanded by agents | Personal/causal interpretation, not proven by output counts. Provide a specific example. |
| 6 | “ถ้ายิ้มทำได้ คุณก็ทำได้” | Motivational invitation, not a guarantee; appropriate closing for this speaker. |
| 6 | Nat will teach 6 lessons; follow at aiexpo.buildwithoracle.com | BRIEF.md supports the planned handoff and address. Current lesson count, accessibility of the site and session position were not independently verified; confirm in final rehearsal. |
| All | Counter 1/6…6/6; six total slides | Directly verified in DOM/navigation. S1 stages 1–3 and S2 items 1–3 are enumeration. |

## Runtime and JS assessment

- Opened the actual local file in Ego Chromium. Three.js initialized. After a normal reload, the filtered browser event buffer contained no console, exception or log entries. This is a short-run check, not a guarantee of an error-free ten-minute talk.
- Right, PageDown, Space, Left, PageUp, Home and End selected the expected slides; first/last bounds clamped correctly. Both n and N toggled notes. Rapid sequential navigation did not break the state.
- Blocking the CDN/fonts with cache disabled left every slide navigable and notes working. Import failure is outside try/catch; expect browser resource diagnostics even though HTML remains usable. The immediate filtered blocked-load buffer returned no entries, so I do not claim a specific observed error string.
- Forcing canvas WebGL context creation to return null produced `__world === false`; Home/End still worked. Initialization fallback passed. Mid-talk hardware context loss was not simulated.
- Reduced-motion emulation plus reload produced zero loop frames, with the world correctly on slide index 1 after navigation. This passes startup reduced-motion behavior.
- Resize settled correctly at 1024×768: stage x=0, y=96, width=1024, height=576. The fixed 16:9 scene and uniform CSS scaling preserve anchor coordinates; missing remeasurement on ordinary resize is not itself a geometry bug. The unchanged high-resolution buffer is a performance issue.
- Morph interpolation uses elapsed seconds and snapshots current position/scale/color/camera, which sensibly handles interrupted transitions. Target formations continue moving during the 850ms morph. CSS background finishes in 250ms, entrance effects in up to 870ms, and JS uses its own easing; “all together” is approximate, not exact synchronization.
- No obvious unbounded memory leak: one renderer, geometry, material and mesh; fixed typed arrays; six slots of cached anchors/text boxes; listeners registered once. Short-lived per-frame allocations create GC pressure, but are not evidence of retained-memory growth. No ten-minute heap/GPU soak was performed. Lack of dispose is not a leak by itself in this single-page lifetime.
- REPORT.md is stale for the current content: it describes a personal-agent placeholder and a 32px minimum for S3, while current code has final names and a 24px footnote. Its earlier acceptance/contrast results should not be treated as current certification.

## Screenshot readability and story

b1 gives a clear memory → bottleneck → team overview, and b2 connects it to ways of working. b3 is the weak link: it adds several systems and trust boundaries without labeled architecture. b4 restores a familiar shift metaphor; simplify the paragraph and explain the commands in human terms before saying their names. b5 makes outputs memorable but needs evidence and one actual example. b6 is an excellent, legible closing; the invitation fits a non-engineer PM.

All six supplied stills have clear primary hierarchy, visible Thai marks and no obvious text clipping. The main formations sit beside copy. Moving dust remains present across the frame; still screenshots cannot prove readability at every transition instant. Gray subtitles/footnotes and S3 density are the main back-row risks. The arc is complete in the requested order, but “งานเดินได้โดยไม่รอยิ้ม” needs one bridging sentence: routine work continues; consequential decisions still come to Yim. Explain ARRA as the community's working method, agent as an AI teammate, Discord as the team room, ψ/ as saved work notes, and SKU as product codes. Tool names can stay a quiet credit rather than becoming part of Yim's spoken explanation.

Verdict: ship after fixes
