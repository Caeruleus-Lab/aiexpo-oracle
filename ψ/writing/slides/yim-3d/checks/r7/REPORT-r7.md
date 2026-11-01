# REPORT: round 7 — Riso เป็นโมดูลกลางของ Rikyu Labs ใช้ได้ทั้งสไลด์และ landing page

2026-11-01 · Osaa (Oracle AI) · ตาม `BRIEF-R7.md` · ฝั่ง hello-oracle commit แล้ว (`f944fe473`, ยังไม่ push) · ฝั่ง deck นี้ยังไม่ได้ commit

รายงานรอบ 6 อยู่ใน git ที่ `52ba83a` ค่ะ

## สรุปสั้น

คุณยิ้มขอว่า "อยากให้เก็บเป็นรูปแบบที่เอาใช้ทั้ง slide และ landing page ของ rikyu labs ได้" ตอนนี้ทำแล้วค่ะ
โมดูลย้ายไปอยู่ที่ `~/hello-oracle/ψ/design-systems/rikyu-labs/riso/` และเรียกใช้ทางเดียวคือ `RikyuRiso.mount(canvas, options)`
สไลด์ใช้โหมด stage (เวที 1920x1080 ที่เด็คย่อขยาย) ส่วนหน้าเว็บใช้โหมด container (ภาพพอดีกล่องของมัน ตามขนาดจอจริง)
มีหน้า landing ตัวอย่างของ Rikyu Labs ให้ดูด้วย เปิดดูได้ที่ `riso/example-landing.html` และดูภาพจอมือถือได้ที่ `riso/example-landing-390.png`

## สิ่งที่ทำ

1. **ย้ายด้วย `git mv`** จาก `slide-kit/riso/` ขึ้นมาเป็น `rikyu-labs/riso/` แล้ว `git log --follow riso.js` ยังตามประวัติได้ถึง `510234bcd`
   `slide-kit/riso/README.md` เหลือเป็นป้ายชี้ทาง 3 บรรทัด และ `example.html` เปลี่ยนชื่อเป็น `example-slide.html`
   ⚠️ ระหว่างที่ทำ daemon brain-sync เก็บไฟล์ที่ย้ายไปเป็น auto-sync commit เองแล้ว 3 อัน (`b98b7e3ec`, `2082892ff`, `ae6124a03`)
   ส่วนที่เหลือจึงอยู่ใน `f944fe473` ซึ่ง commit โดยระบุ pathspec ไว้ ฉันไม่ได้แก้ประวัติย้อนหลังค่ะ
2. **`mount()` ใน `riso.js` v1.1.0**
   - ขนาดตามกล่อง แยก backing store ตาม DPR
   - ตามการเปลี่ยนขนาดด้วย ResizeObserver, media query `(resolution)` และเช็ก `devicePixelRatio` ทุกเฟรม
   - พักเองเมื่อกล่องหลุดจอ (IntersectionObserver) หรือแท็บถูกซ่อน
   - เคารพ `prefers-reduced-motion` ด้วยการพิมพ์ภาพนิ่งภาพเดียว เป็นภาพตอนจบเรื่อง
   - มี `track` ให้ส่วน scroll ได้ค่า progress 0..1
   - กฎรอบ 6 ยังอยู่ครบ: canvas ต้องไม่อยู่ใต้ transform (ถ้าเจอ จะเตือนและบอกชื่อ element ใน `info().transformed`) และ cell ต้องเป็นจำนวนเต็มของ device pixel
   - `create()` แบบ v1.0 ยังใช้ได้
3. **ตัวอย่าง:** `example-slide.html` (ย้ายมาใช้ mount แล้ว) และ `example-landing.html` ซึ่งมี hero, ส่วน scroll แบบ sticky (งานกระจัดกระจายค่อยๆ เรียงเป็นระบบ) และเส้นคั่น section
   ข้อความหน้าเว็บเอามาจาก brand brief (§1, §3, §6, §14) ไม่ได้แต่งใหม่ ใช้ได้ตั้งแต่จอกว้าง 390 px ขึ้นไป และมีปุ่ม Pause ตาม WCAG 2.2.2
4. **README** ใหม่ทั้งฉบับ มีวิธีใช้กับสไลด์และ landing, งบประสิทธิภาพบนมือถือ, กฎ moire, still mode และเครดิต (dithering-shader MIT Niccolo Fanton, pattern ของ Klems)
   ใส่ลิงก์บรรทัดเดียวไว้ใน `rikyu-labs/README.md` และ `slide-kit/en|th/README.md` แล้ว (ไม่มีไฟล์ `slide-kit/README` ตัวเดียว จึงใส่ทั้งสองภาษา)
5. **deck.html** เปลี่ยนจาก `RR.create(...)` เป็น `RR.mount(canvas, { stage, ... })` แบบไม่ส่ง `draw` เพราะเด็คมี loop ของตัวเองอยู่แล้ว
   `vendor/riso.js` และ `vendor/riso.css` เป็นสำเนา v1.1.0 (`cmp` ตรงกับต้นฉบับ)

## Acceptance (รันจริงทุกข้อ ใช้ Chrome for Testing บน Apple M4)

- `python3 checks/r6/shot.py deck.html .` → `1 []` ถึง `8 []` ✅ และ `__world.ok = true`, `mode stage`, `cell 4`, `version 1.1.0`
- moire ของ deck: 1920x1080 → 99.06%, 1280x720 → 99.07%, negative control `&fixed1920` → 58.2% (รอบ 6 ได้ 99.1 / 99.1 / 58.4)
- FPS ของ deck: รันแรกได้ 44–48 บนสไลด์ 3–6 ฉันเลยสร้างเด็ครอบ 6 กลับมาจาก git (`checks/r7/r6deck/`) แล้ววัดคู่กัน
  ได้ 60 ทุกสไลด์ทั้งรอบ 6 และรอบ 7 รันแรกจึงน่าจะช้าเพราะวัดซ้อนกับงาน moire ที่รันอยู่ ไม่ได้มาจากโค้ด
- `check.py example-slide.html` → overflow `[]`, errors `[]`, cell 4, 61 fps
- landing shots ที่ 1920x1080, 1280x800, 390x844@3 → overflow `[]`, errors `[]` ทุกขนาด, `transformed: null` ทุกกล่อง (ภาพอยู่ใน `checks/r7/landing-*`)
- **whole-cell** (ซ่อนตัวอักษร นับช่วงของจุดหมึกคุโระว่ายาวเท่าจำนวนเต็มของ cell ไหม) ได้ **100%** ทั้ง hero / scroll / divider ที่ 390@3 (cell 12), 1280 และ 1920 (cell 4)
  negative control `?neg` (backing store 0.9 เท่า) ตกลงเหลือ 0–46% แปลว่าตัววัดแดงได้จริง (`checks/r7/cells-summary.txt`)
- knockout บน hero ของ landing: เมื่อวาง decoy ไว้ใต้หัวเรื่อง นับจุดหมึกในกรอบหัวเรื่องได้ 0 px ทั้งที่ 1280 และ 390@3
  พอปิด mask (`&nomask`) ได้ 27,200 และ 199,128 px แปลว่า decoy ลงจริง (`checks/r7/knock_landing.py`)
- พฤติกรรม: ตอนอยู่บนสุดของหน้า hero วิ่ง 61 fps ส่วนอีกสองกล่องหยุดที่ 0 fps
  เลื่อนมากลางหน้าแล้วได้ 0 / 61 / 0 คือวิ่งเฉพาะกล่องที่อยู่บนจอ กดปุ่ม Pause แล้วได้ 0 ทุกกล่อง
  เปิด reduced-motion ได้ 0 เฟรม แต่ยังพิมพ์ภาพนิ่งออกมา (67,955 จุดหมึก) และปุ่ม Pause ถูกซ่อน
  เปลี่ยน DPR 1→2 แล้ว canvas เปลี่ยนจาก 1280x800 เป็น 2560x1600 และ cell จาก 4 เป็น 8
- FPS มือถือ 390x844@3 เมื่อหน่วง CPU 1x / 4x / 6x ได้ 60 / 60 / 60 ทั้ง hero และส่วน scroll

## สิ่งที่ต้องรู้ (ข้อจำกัดที่วัดเจอ)

- **ยังไม่ได้วัดบนมือถือจริง** การหน่วง CPU ผ่าน CDP ไม่ได้ทำให้ GPU ช้าลง ส่วนงานหนักของ Riso อยู่ที่ GPU
  ผล 60 fps จึงบอกได้แค่ว่าฝั่ง JS ยังมีที่เหลือ ไม่ได้รับรองว่าโทรศัพท์จะได้ 60 ค่ะ
- **เจอบั๊กหนึ่งตัวและแก้แล้ว:** การจำลอง DPR ของ CDP ไม่ยิง event `resize` หรือ media query เลย ฉันลองใส่ listener เปล่าๆ ดูแล้วก็ไม่มี event เข้ามา
  ทางเดิมของโมดูลจึงทดสอบด้วยวิธีนี้ไม่ได้ ฉันเพิ่มการเช็ก `devicePixelRatio` ทุกเฟรมไว้เป็นทางสำรอง และผลที่ผ่านข้างบนผ่านทางนี้
  ส่วนทาง media query บนเบราว์เซอร์จริงยังไม่ได้พิสูจน์
- **`?nosnap` ไม่แดง:** ถ้าตัดการขยับ canvas ให้ลงพิกเซลเต็มออก ก็ยังได้ 100% แม้ divider จะอยู่ที่ y = 787.25 px
  แปลว่า Chrome จัดให้ลงพิกเซลเต็มให้อยู่แล้ว กฎข้อ 3 จึงยังไม่มีหลักฐานว่าจำเป็นบนหน้าเว็บ ฉันเก็บไว้เป็นตัวกันและเขียนไว้ใน README ตรงๆ
- Chromium ที่มากับ playwright เรนเดอร์ WebGL ด้วยซอฟต์แวร์และได้ราว 4 fps ต้องตั้ง `RISO_CHROME` ให้ชี้ไป Chrome ที่ใช้ GPU ก่อนอ่านตัวเลข FPS
- เส้นคั่นบางๆ มีลายเนื้อกระดาษของการพิมพ์ เมื่อวางบนพื้นหน้าเว็บสีเรียบจึงเห็นเป็นแถบกระดาษพิมพ์ ฉันตั้งใจเก็บไว้ ถ้าอยากให้กลืนไปกับพื้นใช้ `grain: false`
  ฉันเพิ่มตัวเลือก `vignette` ไว้ด้วย (ปิดเป็นค่าเริ่มต้นบนหน้าเว็บ) เพราะขอบมืดแบบสไลด์ทำให้แถบดูเป็นสีเทา

## ให้คุณยิ้มหรือ Dobby ตัดสิน

1. หน้า landing ตัวอย่างใช้ copy ภาษาอังกฤษจาก brief ล้วน ถ้าเว็บจริงจะเป็นภาษาไทย ต้องมีคนเขียน copy ไทยก่อน ฉันไม่ได้แต่งเพิ่ม
2. จะ commit ฝั่ง deck นี้ไหม (`deck.html`, `vendor/riso.*`, `checks/r7/`) ใน brief สั่งให้ commit เฉพาะ hello-oracle ฉันเลยยังไม่ได้แตะ
   `checks/r7/` มีขนาด 26 MB ส่วนใหญ่เป็นภาพหน้าจอ
3. registry ระดับบน `ψ/design-systems/README.md` อยู่นอก pathspec ที่สั่งไว้ ฉันจึงยังไม่ได้ใส่ลิงก์ ถ้าอยากให้ใส่ บอกได้เลยค่ะ

— Osaa (Oracle AI)
