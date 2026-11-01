# Language and clarity review: yim-3d deck (8 slides)

Reviewed: COPY-FOR-REVIEW.md plus screenshots b1..b8. Rules applied: kien-thai (frames, clarity pass, 3 hard rules), Yim house rules. Rewrites are Thai, explanations English. Rewrites keep on-screen lines about as short as now.

## Mechanical checks (run, not remembered)

- `thai-lint.py lint` on the copy file: 4 hits, all `Numerals`: "สามข้อล่าง" (slide 2 screen), "หนึ่งนาที" (slide 7 screen, see note there), "สี่บรรทัด" and "สองข้อ" (notes). Also "พิธีทั้งสาม" (slide 6) is a count spelled out that the linter did not catch.
- grep `—` `–`: 0 hits. grep `ด่าน`: 0 hits. No `เธอ`, no `ครับ/ค่ะ` on slides. Clean.
- Still open: `·` is used as a separator on screen (`Mac · มือถือ`, `Grok · Dots · Muse`, the slide 3 footnote, slide 4 `คุยได้ ลงมือในระบบเราไม่ได้ · คนกดอนุมัติ`). Your memory rule says to check `[—–·]` in Thai prose. In name lists it reads as a list mark, so optional. In the slide 4 sentence it hides a relationship, so fix it (slide 4).

## Cross-deck problems (read first)

1. **Slide 2 vs slide 5 contradict.** Slide 2: "AI ไม่ตัดสินแทน". Slide 5: "Dobby ตัดสินเองแล้วรายงาน". A sharp listener catches this in 3 minutes. Fix the slide 2 wording (below) so it says "เรื่องใหญ่ คนตัดสิน".
2. **ฝูง / ทีม AI / fleet / agent are four names for one thing.** Slides 1-2 say "ทีม AI", slide 3 suddenly says "ฝูง" with no definition, slide 5 says "Fleet registry", slide 7 says "ฝูง agent". See the term list at the end.
3. **Overclaim repeated 3 times.** "ไม่มีอะไรหาย" (slide 2 headline, slide 3 body) plus "ย้อนดูได้เสมอ". Your own rule on slide 5 says "เสร็จแล้ว ไม่นับ ต้องเปิดของจริงดู", so a guarantee on slide 2 undercuts the credibility of slide 5. Use "ย้อนดูได้" (checkable) not "ไม่หาย" (absolute).
4. **Speaker notes are mixed documents, not speakable scripts.** Each note blends: what to say, what NOT to say (ห้าม...), provenance paths, source dates, and ⚠️ to-dos. On stage the speaker needs 2 to 3 lines to say. Recommendation: split every note into `SAY` (max 3 short lines) / `DON'T` / `CHECK BEFORE STAGE`. Provenance paths and "(คุณยิ้ม 2026-11-01)" go to CHECK or out.
5. **Notes contradict the screen in 3 places** (slide 3 "ห้ามบอกเลขเป๊ะ" vs slide 5 shows 15/160/393/22; slide 5 "ไม่ต้องเอ่ยชื่อ registry" vs screen headline "Registry ..."; slide 5 notes quote 211/17 while screen shows 393/22). Details per slide.
6. **Who is "เรา".** Slide 2 `ของเรา`, `เราถาม` (= any user), slide 3-4 `ระบบเรา` (= Yim's system), slides 1,3,5,7 use `ยิ้ม` in the third person. Pick one rule: `ยิ้ม` for what Yim built, `เรา`/`คุณ` only in generic principles (slide 2). Change `ระบบเรา` to `ระบบของยิ้ม` (slides 3, 4).
7. **Slide 5 carries 3 ideas and 7 numbers.** For a non-technical audience in 75 seconds, only one column will land. Suggest cutting the numbers block or the rules block (see slide 5).

---

## Slide 1: intro and 3 steps

**Should fix**
- Step 3 body is the weakest line and ARRA is unexplained. Current: `ทีม AI หลายตัว / กับวิธีทำงานของ ARRA`. Step 3 is the payoff, but the body says what exists, not what changed. Rewrite: `AI หลายตัวช่วยกันทำ / ตามวิธีทำงานแบบ ARRA` (same length). The audience learns ARRA properly on slide 2; a one-word gloss is not needed if the order "AI หลายตัว + วิธีทำงาน" is kept.
- Step 2 headline is right, but `คอขวด` is an idiom some owners will not map to themselves. Body already explains it, so keep, but speaker should say it as "ทุกอย่างต้องผ่านยิ้มคนเดียว". Optional gloss on screen: `AI ทำได้มากขึ้น แต่ทุกงานต้องรอยิ้มสั่ง รอยิ้มตรวจ` (adds `ต้อง`, reads more naturally).

**Optional**
- Subtitle `product manager ไม่ใช่วิศวกร`: natural, keep. It is the whole reason the audience can trust "if I can, you can".
- Name line: a mid-talk viewer sees a name only. Fine for an intro slide.

**Notes**
- Speakable except `ห้ามอธิบายเทคนิค...` (a DON'T). 1.5 min for 3 steps is right.
- `เมื่อปีที่แล้ว` is a factual claim about Yim's own timeline. Check it is true before saying it.
- Good line to keep: "เมื่อกี้ที่เห็น AI ลืม นั่นคือชีวิตยิ้มทุกวัน". Say "ชีวิตของยิ้มทุกวัน" (natural Thai needs `ของ`).

---

## Slide 2: what unlocked it

**Must fix**
- **Headline is not a sentence the audience can parse.** Current: `สิ่งที่ปลดล็อก ทีม AI กับวิธีทำงาน`. Unlock what? And the 4 rows below are not all "unlocks": row `+` is the team, rows 1-3 are principles. Rewrite: `ทีม AI ทำงานได้ เพราะมี 3 หลักนี้` (the `+` row becomes the thing being explained, rows 1-3 the reasons).
- **Row 2 contradicts slide 5.** Current: `AI ไม่ตัดสินแทน / คนตัดสิน ความรู้ของงานยังเป็นของเรา`. Rewrite: `เรื่องใหญ่ คนตัดสิน / AI ช่วยคิดและเตรียมให้ ความรู้ของงานยังเป็นของเรา`. If space is tight: `AI ช่วยคิด คนตัดสิน` / `เรื่องใหญ่คนเป็นคนเลือก ความรู้ยังเป็นของเรา`.
- **Row 1 overclaim.** Current: `ไม่มีอะไรหาย / งานทุกชิ้นถูกจดไว้ ย้อนดูได้เสมอ`. Rewrite: `ทุกอย่างมีบันทึก / งานแต่ละชิ้นถูกจดไว้ ย้อนกลับไปดูได้`. Note: on a stage with live demos, "ไม่มีอะไรหาย" is also the sentence a skeptical engineer will test.

**Should fix**
- `+` row has an orphan symbol on screen (a plus in a column of numbers). Replace with no marker or a team icon, and drop `+`. Subject missing: `หลายตัว ทำพร้อมกัน` reads as a fragment. Rewrite: `AI หลายตัว ทำพร้อมกัน / แต่ละตัวมีหน้าที่ และตรวจงานกันเอง`.
- Row 3: `เราถาม มันจำ`. `มัน` for AI is the calque kien-thai bans (`dummy-man`). Rewrite: `เราถาม AI จำไว้ / ครั้งหน้าก็ง่ายขึ้นกว่าเดิม` (uses `ก็` pacing, frame 6; `จึง` is stiff).
- Footnote: `สามข้อล่าง จากหลัก 5 ข้อของชุมชน ARRA Oracle`. Numeral lint hit, and a mid-talk viewer asks "5 ข้อ มีอะไรบ้าง". Rewrite: `3 ข้อล่าง มาจากหลักของชุมชน ARRA Oracle`.

**Notes**
- 45 s for 4 rows plus a story is tight. Change instruction to: read the headline, say one row, tell one story. Say it that way.
- The English principle names in parentheses are provenance, not speech. Move to CHECK.
- `สี่บรรทัด` numeral lint hit: `4 บรรทัด`.

---

## Slide 3: how the fleet works

**Must fix**
- **`ฝูง` appears here for the first time, undefined.** Title: `ฝูงของยิ้ม ทำงานกันยังไง`. A mid-talk viewer has no idea what ฝูง is. Rewrite: `ทีม AI ของยิ้ม ทำงานกันยังไง`, and say once aloud "เราเรียกทีมนี้ว่าฝูง". Then use one term to the end (term list below). If you keep ฝูง on screen, the first row must define it: `ฝูงคือทีม AI สิบกว่าตัวของยิ้ม`.
- **Row 1 headline is broken Thai.** Current: `ในฝูง สิบกว่าตัว อยู่บนเครื่องที่เปิดตลอด`. "ตัว" of what? Rewrite: `agent สิบกว่าตัว ทำงานบนเครื่องที่เปิดไว้ตลอด`.
- **Row 1 body repeats the overclaim and has jargon.** Current: `ศูนย์กลางคือ Discord ยิ้มสั่งงานและเห็นงานทุกตัวในที่เดียว / ความจำร่วมเป็นไฟล์ ไม่มีอะไรหาย`. Rewrite: `Discord คือห้องกลาง ยิ้มสั่งงานและดูงานทุกตัวจากที่เดียว / ความจำร่วมจดเป็นไฟล์ ย้อนดูได้`. `เครื่องที่เปิดตลอด` is acceptable for owners ("คอมที่เปิดทิ้งไว้"); keep, and the speaker says "เหมือนเซิร์ฟเวอร์ของร้าน" once.
- **Row 2 is ambiguous about what "approve" unlocks.** `คุยได้ แต่ลงมือในระบบเราไม่ได้ / คนต้องเป็นคนกดอนุมัติ`. Can they act after approval? Rewrite: `agent ของคนอื่น คุยได้ แต่ลงมือเองไม่ได้ / ต้องให้คนกดอนุมัติก่อน`. Also `ระบบเรา` becomes `ระบบของยิ้ม` (see cross-deck 6).

**Should fix**
- **`แขก` is a new noun** for what the headline calls `agent ของคนอื่น`. Current: `แขกแต่ละคนได้กุญแจของตัวเอง เปิดได้แค่ไม่กี่อย่าง`. Rewrite: `agent ของคนอื่นแต่ละตัวได้กุญแจของตัวเอง เปิดได้เฉพาะบางอย่าง`. Keep the key image (one metaphor, good), drop `แขก`. Notes say do not say whose agents these are, so do not say "แขกของใคร" either.
- Row 3: `ผู้ช่วยส่วนตัว Grok · Dots · Muse` has 3 names with no meaning on screen. Whose personal assistants? Rewrite: `ผู้ช่วยส่วนตัวของแต่ละคน เช่น Grok · Dots · Muse / ต่อเข้ากับทีมได้ และขอให้ agent ในทีมทำงานให้ได้เอง`. Only do this if "ของแต่ละคน" is true; verify against the fleet facts file.
- Row 1 third line: `ตัวที่วางแผน ตัวที่ลงมือ และตัวที่ตรวจ เป็นคนละตัว คนเป็นคนอนุมัติ`. Best idea on the slide, buried at the bottom of the longest block, and the longest line is 1 line wider than the others. Rewrite: `คนวางแผน คนลงมือ คนตรวจ เป็นคนละคน` is wrong (they are AIs). Use: `agent ที่วางแผน ที่ลงมือ และที่ตรวจ เป็นคนละตัวกัน แล้วคนค่อยอนุมัติ`.
- Footnote `T3 · Pi (Claude วางแผน, Codex ลงมือและตรวจแยก) · Linear` is an orphan jargon line. T3, Pi, Linear mean nothing to owners and notes say "ไม่ต้องอธิบาย". Either label it `เครื่องมือที่ใช้: T3 · Pi · Linear` or delete. Also `ตรวจแยก` is ambiguous. Rewrite if kept: `เครื่องมือที่ใช้ เช่น Claude วางแผน Codex ลงมือและตรวจแยกกัน`.

**Optional**
- `สิบกว่าตัว` is fine and honest, but see below: the notes ban exact numbers while slide 5 shows `15`.

**Notes**
- Contradiction: notes say `พูดว่า "สิบกว่าตัว" ห้ามบอกเลขเป๊ะ` but slide 5 prints `Fleet registry 15 yaml`. Pick: either drop "ห้ามบอกเลขเป๊ะ" or drop the 15 on slide 5.
- `หลักคนละตัว:` is a label with no meaning. It should be `จุดที่ 3: วางแผน ลงมือ ตรวจ เป็นคนละตัว`.
- `(คุณยิ้ม 2026-11-01)` and the `ที่มา:` path are provenance, not speech.
- `box` and `ห้องคนขับ` appear only in notes. `Mac ของยิ้มคือห้องคนขับ` is a good image, but the screen never shows the Mac on this slide (it is on slide 4). Say it on slide 4 instead.
- 1.5 min for 3 rows is fine; the slide is dense, so say only the bold line of each row.

---

## Slide 4: architecture picture

**Must fix**
- **Title uses `สถาปัตยกรรม`.** An owner hears an engineering word at slide 4. Rewrite: `ภาพรวม ฝูงต่อกันอย่างไร` (or `ใครสั่ง ใครทำ ความจำอยู่ตรงไหน`, the speakable version, 29 chars of Thai).
- **Bottom-left box hides a rule behind `·`.** Current: `คุยได้ ลงมือในระบบเราไม่ได้ · คนกดอนุมัติ`. Rewrite: `คุยได้ ลงมือเองไม่ได้ ต้องรอคนอนุมัติ`.

**Should fix**
- Slide 3 and slide 4 say the same things twice (center = Discord, machine always on, agent ของคนอื่น, ผู้ช่วยส่วนตัว). Because slide 4 adds only arrows, make the 45 s count: say "ตามลูกศรไปได้เลย: ยิ้มสั่งจากมือถือ ไปถึงทีม และทีมจดความจำลงไฟล์". Optional: delete slide 3's repeated third row and let slide 4 carry it.
- Box 3 `เครื่องที่เปิดตลอด / ฝูงสิบกว่าตัว` and box 4 `ความจำร่วม / เป็นไฟล์`: the arrow from machine to memory reads as "machine sends data to a file box". Fine. Use `จดลงไฟล์` as the sub-line to make the arrow a verb: `ความจำร่วม / จดลงไฟล์`.
- Layout (not copy): bottom 35% of the slide is empty while text boxes are small. Raise font size of box sub-lines for the back row.

**Notes**
- Speakable. Good and short. `ไม่ต้องอ่านทุกกล่อง` is exactly right.
- `ที่มา: hello-oracle ψ/...` path: move out of speech.

---

## Slide 5: run it like a company

**Must fix**
- **Middle column heading is ungrammatical.** Current: `Registry ว่าใครทำอะไรได้ / และเรียนอะไรมาแล้ว`. "Registry ว่า..." is a calque of a definition. Rewrite: `Registry คือทะเบียนว่า ใครทำอะไรได้ และเรียนอะไรมาแล้ว` (keep `Registry` in English per house rule; the gloss `ทะเบียน` makes it self-explaining).
- **Numbers have no meaning without a unit.** Current: `เรียน 393 เรื่อง ตัดสินใจแล้ว 22`. Decided what? Rewrite: `เรียนมาแล้ว 393 เรื่อง / เลือกเอามาใช้จริง 22 เรื่อง`. Also decide what the audience should feel: 22 of 393 sounds like failure unless the speaker says "แค่ 22 ที่ผ่านการตัดสินใจ ที่เหลือยังเป็นแค่ความรู้". Make the point explicit in the notes.
- **`yaml` to a business audience.** Current: `Fleet registry 15 yaml / Skill registry 160 skills`. A non-technical viewer reads "15 yaml" as noise. Keep yaml in English (house rule) but pair it with the thing it counts: `Fleet registry: 15 agent (15 ไฟล์ yaml)` / `Skill registry: 160 skill`. Verify that the 15 files = 15 agents before putting "15 agent" on a stage.
- **Right column's first line is cryptic.** Current: `เสร็จแล้ว ไม่นับ ต้องเปิดของจริงดู`. Rewrite: `AI บอกว่าเสร็จ ยังไม่นับ ต้องเปิดของจริงดูก่อน`. Second line: `กฎที่เป็นตัวหนังสือจะถูกลืม / ทำให้เป็นกลไกที่บังคับเอง` has vague `กลไก`. Rewrite: `กฎที่แค่เขียนไว้ คนก็ลืม / เลยให้ระบบบังคับแทน`.
- **Notes contradict the screen on registry.** Notes: `ไม่ต้องเอ่ยชื่อ registry หรือ hook`. Screen headline of the middle column is `Registry`. Pick one. Recommended: say it ("ทะเบียน", the Thai word, aloud) and keep the English word on screen only.
- **Notes quote different numbers than the screen.** Notes: `ตอนนั้น (ส.ค. 2026) ฝูงเรียนไป 211 เรื่อง แต่มีแค่ 17 เรื่อง`. Screen: `393 ... 22` as of 1 Nov. A speaker who reads the notes states the old numbers over the new ones. Rewrite notes: "ตอนเริ่มเรียน 211 เรื่อง มีแค่ 17 ที่จดว่าเอามาใช้ ตอนนี้ 393 กับ 22 สัดส่วนยังเล็ก เพราะเราเลือกเอามาใช้จริงเท่านั้น". Or drop 211/17 entirely (fewer numbers).

**Should fix**
- Left column has orphan one-word labels: `กลาง`, `เล็ก`. Mid-talk viewer cannot read them. Rewrite: `เรื่องใหญ่ หรือย้อนไม่ได้ / ยิ้มตัดสิน`, `เรื่องกลาง / คิดด้วยกัน`, `เรื่องเล็ก / Dobby ตัดสินเองแล้วรายงาน`.
- `Dobby` is unexplained. Add: `ผู้ช่วยหลัก Dobby ตัดสินเองแล้วรายงาน`.
- Column heading `แบ่งงาน ตามราคาของการผิด`: `ราคาของการผิด` is a calque of "cost of error". Rewrite: `แบ่งงานตามว่า ถ้าพลาดแล้วเสียหายแค่ไหน` (longer by one line; OK because the left column is otherwise sparse). Shorter: `แบ่งงาน ตามความเสียหายถ้าพลาด`.
- Slide is overloaded (3 columns, 7 numbers). If you cut one thing, cut the numbers block (`15 yaml / 160 skills / 393 / 22`): the left and right columns are the real story, "run like a company" = approval limits plus checking the real thing. Keep `ทะเบียน` as one line: `Registry คือทะเบียน ว่าใครทำอะไรได้`.

**Notes**
- Too long: about 190 words for 75 s of speech. Cut to the 3 columns: one sentence each, plus the "เหมือนวงเงินอนุมัติ" analogy (excellent, keep) and the "ลูกทีมบอกว่าเสร็จ เราก็ยังเปิดดู" line (excellent, keep). Drop the dates `31 ก.ค.` and `8 ส.ค.` from speech.
- `สองข้อ` numeral lint hit: `2 ข้อ`.
- `ไม่ต้องเอ่ยชื่อ registry หรือ hook` conflicts with the screen (above).

---

## Slide 6: shift work

**Must fix**
- **Commands are on screen with no meaning.** `/recap`, `/forward`, `/rrr` appear as bare strings in the circles. Title and notes explain them, but the screen does not. Rewrite the circles (keep the command, add a verb): `เข้ากะ / อ่านบันทึกก่อนเริ่ม /recap`, `ออกกะ / เขียนส่งต่อ /forward`, `ทบทวน / เก็บบทเรียน /rrr`. If a circle cannot take 2 lines, put the verb in the circle and the command small below.
- **`ψ/` is an unreadable symbol for most of the room.** Current: `ψ/ บันทึกส่งกะ`. Rewrite: `สมุดส่งกะ` as main and `โฟลเดอร์ ψ/` as small caption, or `ψ/ (โฟลเดอร์ของบันทึกส่งกะ)`. The nice metaphor is `บันทึกส่งกะ`, so make that the readable part.

**Should fix**
- Footnote `พิธีทั้งสามเป็นของ Oracle Protocol ของคุณนัท`: `พิธี` (ritual) is odd Thai here, `Oracle Protocol` is a new proper name, `ทั้งสาม` numeral. Rewrite: `3 คำสั่งนี้ มาจากวิธีทำงานของคุณนัท (ARRA Oracle)`.
- Circle `ทำงาน / งานจริง` is redundant. Rewrite: `ทำงาน / ลงมือจริง`.
- `ใครเคยดูแลทีมคน รู้วิธีนี้อยู่แล้ว`: good, speakable. Optional: `ใครเคยดูแลทีมที่เป็นคน ก็รู้วิธีนี้อยู่แล้ว` (adds `ก็`, frame 6).

**Notes**
- Opening line `โรงพยาบาลกับโรงงานไม่ได้ใช้คู่มือส่งงานกัน เขาใช้บันทึกส่งกะ` is awkward (`ส่งงานกัน`) and an absolute claim. Rewrite: "โรงพยาบาลกับโรงงานส่งงานต่อกันด้วยบันทึกส่งกะ ไม่ได้ส่งต่อกันด้วยความจำ".
- The timing `1.5 นาที` sits mid-note. Put at the start for all slides.
- `⚠️ เช็กกับคุณนัท...` is an open to-do, not speech. Resolve before stage; if `/forward` is not in the 6 lessons, the screen circle must say `handoff` too. Today the screen says `/forward`, so the check is blocking, not optional.
- Best line in the deck: "คนที่เคยบริหารทีมคนมาแล้ว รู้วิธีทำงานกับ AI อยู่แล้ว แค่ยังไม่มีใครบอก". Put it on the screen instead of the current left-bottom line. It is the slide's real main line.

---

## Slide 7: results

**Must fix**
- **Headline does not match the body.** Current: `งานที่เคยอยากทำ แต่ทำไม่ได้`. Body shows things now done (135, 5, 3). A viewer reads "things I could not do" over three achievements. Rewrite: `งานที่เคยอยากทำ ตอนนี้ทำได้แล้ว`. Keeps the highlighted second half.
- **`3 Part ของคอร์ส / จากคนเรียนกลายเป็นคนสอน` is ambiguous.** Who changed from learner to teacher? Rewrite: `3 Part ของคอร์ส / จากคนเรียน กลายเป็นคนสอนเอง`. Optional: name the course `From Prompting to Your Own AI Agent` in the small line if space allows (it is on the notes, not the screen).

**Should fix**
- `5 แอปที่คนอื่นใช้ได้ / เช่น วิเคราะห์สต็อกและ SKU ในหนึ่งนาที`: `SKU` is a retail term the SME audience knows, keep. `ในหนึ่งนาที` reads as a promise and is a numeral lint hit (time unit, check `lek-nap-khong` before changing to digits). Rewrite: `เช่น แอปวิเคราะห์สต็อกและ SKU ที่ได้ผลใน 1 นาที`, or soften: `เช่น วิเคราะห์สต็อกและ SKU ได้ในไม่กี่นาที` if 1 นาที is not measured.
- Closing line: `ทั้งหมดมาจากความรู้งานเดิมของยิ้ม ฝูง agent แค่ขยายมันออกไป`. `มัน` again, `แค่` downplays the team, `ฝูง agent` mixes terms. Rewrite: `ทั้งหมดมาจากความรู้งานเดิมของยิ้ม ทีม AI ช่วยขยายให้ไปได้ไกลขึ้น`. This is the slide's true main line; it should be spoken last and slowly.

**Notes**
- `เวิร์กช็อป 11:00 ก็ทำกับฝูงนี้` conflicts with the event facts (this talk is 15:05 to 16:10 in the repo CLAUDE.md). If an 11:00 workshop exists it should be named, otherwise cut.
- `Kensa ตรวจงานตัวอื่น ไม่มีตัวไหนตรวจงานตัวเอง` is a claim of a guarantee ("no agent checks its own work"). Say "โดยหลักการ" or verify it is enforced.
- Names `Fude Osaa Koe Kensa` are not on screen; fine as a spoken aside if each is glossed in 3 words.
- ⛔ and ⚠️ lines are CHECK items (count again on the morning), not speech.

---

## Slide 8: close

**Should fix**
- Headline `ถ้ายิ้มทำได้ คุณก็ทำได้`: strong, keep. `ยิ้ม` in the third person is the whole point here.
- `คุณนัทพาทำ 6 บทเรียน / ทำตามได้ที่ aiexpo.buildwithoracle.com`: `พาทำ` is fine, but `ทำตามได้ที่` is ambiguous (the lessons, or the 6 steps?). Rewrite: `คุณนัทจะพาทำทีละขั้นใน 6 บทเรียน / ลองทำตามได้ที่ aiexpo.buildwithoracle.com`.

**Notes**
- Not speakable: has no spoken line, only a stage direction and a ⚠️. Add a SAY line: "ที่เหลือ คุณนัทจะพาทำให้ดูทีละขั้น ใครอยากลองตาม สแกนหรือเข้าลิงก์ได้เลย". `⚠️ ถามคุณนัท...` is a to-do to resolve before stage.
- Time total checks out at 9 minutes: 1.5 + 0.75 + 1.5 + 0.75 + 1.25 + 1.5 + 1.25 + 0.5.

---

## Term choices to use consistently

| Concept | Use | Do not use |
|---|---|---|
| The AI team as a whole | `ทีม AI` on slides 1-4 and 7 (say "เราเรียกว่าฝูง" once on slide 3). If you keep `ฝูง`, define it at first use and use it everywhere | mixing `ทีม AI`, `ฝูง`, `ฝูง agent`, `fleet` |
| One member | `agent` (ทับศัพท์) | `ตัว` alone, `เอเจนต์`, `ผู้ช่วย` for fleet agents |
| Others' agents | `agent ของคนอื่น` | `แขก` |
| Personal helpers | `ผู้ช่วยส่วนตัว` (people's own tools, not fleet agents) | `agent` for Grok, Dots, Muse |
| The always-on computer | `เครื่องที่เปิดตลอด` (spoken once: "เหมือนเซิร์ฟเวอร์ของร้าน") | `box` (notes only, never on screen) |
| Discord | `Discord คือห้องกลาง` | `ศูนย์กลาง`, `hub` |
| Memory file store | `ความจำร่วม` (จดเป็นไฟล์) | `ความจำ` alone, `ψ/` unless glossed |
| Handoff doc | `บันทึกส่งกะ` (ψ/ as a caption only) | `คู่มือส่งงาน` |
| The 3 commands | `/recap` `/forward` `/rrr` always with a verb: อ่านบันทึก, เขียนส่งต่อ, เก็บบทเรียน | bare commands |
| The registry | `Registry` (English) with `ทะเบียน` gloss at first use; `yaml` only beside the thing it counts | `Registry ว่า...` |
| Approval | `คนอนุมัติ`, `คนตัดสิน` for big matters; `Dobby ตัดสินเอง` for small ones. Never `AI ไม่ตัดสิน` as an absolute | `AI ไม่ตัดสินแทน` |
| History | `ย้อนดูได้` | `ไม่มีอะไรหาย`, `เสมอ` |
| Self-reference | `ยิ้ม` for Yim's work and system (`ระบบของยิ้ม`); `เรา`/`คุณ` only in generic principles | `ระบบเรา` for Yim's system |
| Counts | digits: `3 ข้อ`, `4 บรรทัด`, `2 ข้อ`, `3 คำสั่ง` | `สามข้อ`, `สี่บรรทัด`, `สองข้อ`, `ทั้งสาม` |
| Punctuation | spaces and `:`; no `—` `–`; `·` only inside name lists | `·` between clauses |
| AI as subject | `AI` | `มัน` |
