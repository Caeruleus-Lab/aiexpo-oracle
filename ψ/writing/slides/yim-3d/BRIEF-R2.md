# Brief round 2 for Osaa: make it your best work

From Dobby, 2026-11-01. Yim, verbatim: "ยิ้มอยากให้ osaa ทำ slide นี้อย่างสุดความสามารถ จากทั้งหมดที่ได้เรียนมา จากเว็บไซต์ UI สวยๆ เอามาจัดในหน้า 3d นี้ให้ลงตัว"

Start from your round-1 `deck.html` and `REPORT.md` in this folder. All MUST rules from `BRIEF.md` still apply
(content-first, WebGL/CDN failure still shows all text, no emoji, no dashes, Thai >= 30px, acceptance command, negative control).

## What changes
1. **Quality bar = award-site level, not "nice slides".** Before touching code, read what you have learned and write
   `DESIGN-NOTES.md` here: 5-8 concrete moves you are taking from your studies, each with its source file, and how it lands in this deck. Sources:
   - your charter knowledge `web3d_award_playbook`, `slide_decks`, `productize_brand_guideline` (`~/hello-oracle/fleet/osaa.yaml` → `knowledge:`)
   - `~/hello-oracle/ψ/learn/somtor/` (3D playbook) · `~/hello-oracle/ψ/learn/nazt/relay-decks/` · `~/hello-oracle/ψ/learn/designil/` · `~/hello-oracle/ψ/learn/nextlevelbuilder/ui-ux-pro-max-skill/`
   - your skills: impeccable, praneet-front, osaa-design-system, web-design-guidelines (run the critique/audit passes, not just read)
2. **The 3D and the layout are one composition.** Type, grid and the 3D scene should be designed together per slide
   (where the eye lands, negative space for text, depth that points at the key line). No text floating over busy geometry; check contrast on every frame.
3. **Motion with purpose.** Camera move between slides tells the story (memory → bottleneck → team → shift ring → many results → you).
   Transitions <= 900 ms, nothing loops distractingly behind text, reduced-motion = still frames.
4. **New slide (6 slides total), inserted after slide 2:** "ฝูงของยิ้มทำงานกันยังไง". Content will be in
   `~/hello-oracle/ψ/writing/expo-2026-10/2026-11-01_fleet-facts-for-talk.md` section "Stage-safe wording". Use only VERIFIED items from that file.
   If the file is not there yet, build the slide shell with the 3D treatment and leave the text block clearly marked for Dobby to fill.
5. **Stage reality:** venue projector at 1920x1080, possibly a weak laptop GPU. Keep it smooth: cap pixel ratio at 1.5, one renderer, instancing, no post-processing heavier than one pass. Report the FPS you measured in headless (requestAnimationFrame count over 3 s).

## Report
Update `REPORT.md`: DESIGN-NOTES summary, acceptance output verbatim for all 6 slides, negative control, FPS, and the 2 things you would still improve with more time.

## Addendum (Dobby, after round 1)
- Round 1 is good: one world, formations anchored beside text, negative control passed. Keep that architecture; raise the craft.
- The fleet slide must cover 3 things from the facts file: how the buds work together · the protocol for talking to agents outside the fleet · Yim's personal agent connected to the fleet.
  **Which personal agent is still unconfirmed by Yim** (candidates in the facts file: Grok Bot, Muse). Leave its name as a clearly marked placeholder `[[PERSONAL_AGENT]]` and design so either name fits.
  Say "สิบกว่าตัว" for the bud count, never a precise number.
- Speaker notes may keep their original text; on-screen text must stay free of `[—–]`.
- Write REPORT.md in your own voice as Osaa (เรา/โอซ่า, ค่ะ/นะ), not ผม/ครับ.

- Personal-agent block on the fleet slide: names only (Grok Bot, Dots, Muse) + one line "ไปขอให้ agent ในฝูงทำงานให้ได้เอง". No rate caps or reply rules on screen.
- Fleet slide also shows Discord as the central hub of the fleet (Yim + buds meet there; personal agents and outside agents connect around it). One line on screen: "ศูนย์กลางของฝูงคือ Discord".
- Fleet slide = one architecture diagram, 5 layers: ยิ้ม (Mac/มือถือ, ห้องคนขับ) · Discord (ศูนย์กลาง) · box (บ้านของฝูง เปิดตลอด) · ψ/ (ความจำร่วมเป็นไฟล์) · edges to personal agents (Grok, Dots, Muse) and outside agents. Optional one line: "ตัวหนึ่งวางแผน อีกเจ้าหนึ่งลงมือ อีกเจ้าตรวจ". No tool names beyond these.
- Coding line on the fleet slide (Yim OK 2026-11-01): main line "ตัวที่วางแผน ตัวที่ลงมือ และตัวที่ตรวจ เป็นคนละตัว คนเป็นคนอนุมัติ" · small footnote: "T3 · Pi (Claude วางแผน, Codex ลงมือและตรวจแยก) · Linear". Beads not on screen. This replaces the earlier optional coding line.
