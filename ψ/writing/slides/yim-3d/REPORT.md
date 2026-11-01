# REPORT: yim-3d deck, round 6 (Riso ทั้งเด็ค + ชุด Riso ใน slide kit ของ Rikyu Labs)

2026-11-01 · Osaa (Oracle AI) · ตาม `BRIEF-R6.md` · ยังไม่ได้ commit (ฝั่ง deck)

ฉบับรอบ 5 ยังอยู่ใน git ที่ `c7fc050` ถ้าจะย้อนกลับก็ทำได้ค่ะ

## สิ่งที่เปลี่ยน (Part A · `deck.html`)
- **ทั้ง 8 หน้าใช้ Riso** พื้นเป็นกระดาษชิโระ ใช้หมึก Rikyu สามสี และทั้งเด็คอยู่ในโลก 3D เดียวกัน เป็นบล็อก isometric หนึ่ง InstancedMesh (1 draw call) ที่พิมพ์ผ่าน `vendor/riso.js` ไฟล์นี้คือสำเนาตรงตัวของโมดูลใน kit (Part B) เด็คนี้จึงเป็นตัวพิสูจน์ว่าโมดูลใช้งานได้จริง
- **ความหมายของหมึกเหมือนกันทุกหน้า:** คุโระคืองานและข้อเท็จจริง · ซาบิคือคุณยิ้ม (บล็อกเดียวที่เป็น "คน") · มอสคือ agent
- **กล้องและภาพในแต่ละหน้า**
  1. stages: งานตกลงข้างคุณยิ้มแล้วหายไป · หอคอยงานบนกล่องคุณยิ้ม · agent 5 ตัวส่งงานต่อกันโดยไม่ผ่านคุณยิ้ม
  2. unlock: agent 5 ตัว แต่ละตัวมีกองบันทึกที่มีแต่เพิ่มขึ้น · มีคำถามวิ่งไปหาคุณยิ้มแล้ววิ่งกลับ
  3. fleet: บ้านที่มี 12 ตัวล้อมคุณยิ้ม · ประตูที่ให้คำพูดผ่านได้ แต่การลงมือหยุดอยู่ที่ประตู · ทางส่งงานไปผู้ช่วยส่วนตัวสามตัว แล้วงานวิ่งกลับมา
  4. architecture: งานวิ่งไปตามลูกศร · 12 ตัวอยู่ใต้เครื่องที่เปิดตลอด · ความจำร่วมกองเป็นแผ่นที่มีแต่สูงขึ้น
  5. บริษัท: การตัดสินใจไต่บันได และน้อยตัวที่ไปถึงคุณยิ้ม · ลูกบาศก์ 211 ลูกเด้งขึ้น จากนั้น 17 ลูกตั้งเป็นเสาแล้วเดินไปยืนบนชั้นทะเบียน 17 ช่อง ที่เหลือแบนลงเป็นแผ่นมอส · งานผ่านประตูตรวจ บางชิ้นไม่ผ่าน
  6. วงกะ: กล้องมองจากด้านบนเหมือนดูนาฬิกา งานไหลตามเข็ม แต่ละกะหย่อนบันทึกลง ψ/ และดวงอาทิตย์หมุนจนเงากวาดเหมือนเข็มนาฬิกา (หน้าเดียวที่แดดหมุนเร็ว)
  7. ผลงาน: ลูกบาศก์ **135 ลูกจริง** (9x5x3) · แอป 5 ก้อนที่มีคนใช้วนรอบ · บันได 3 ขั้น ขั้นบนเป็นซาบิ (จากคนเรียนกลายเป็นคนสอน)
  8. ปิด: ทั้งแผ่นเปลี่ยนเป็นหมึกซาบิด้วยการ dither ระหว่างเปลี่ยนหน้า บล็อกเดียวตรงกลางส่งคลื่นออกไปทั้งห้อง
- **เปลี่ยนหน้าภายใน 850 ms** กล้อง formation และสีขยับไปพร้อมกัน และหมึกซาบิกับมอสจะพิมพ์คลาดเล็กน้อยระหว่างทาง
- **ตัวอักษรเปลี่ยนเป็นหมึกบนกระดาษ:** ink คือคุโระ (15.99:1) · ink-2 ได้ 9.98:1 · ink-3 ได้ 7.08:1 · ไฮไลต์เป็นแถบซาบิด้านหลังตัวอักษรคุโระ เพราะซาบิเป็นสีตัวอักษรบนชิโระไม่ได้ (1.78:1) · หน้า 8 ไฮไลต์เป็นเส้นใต้คุโระ
- **สิ่งที่คงไว้ทุกตัวอักษร:** ทุก `<section>` (คำบนจอ ป้ายใน SVG และ notes) เหมือน `c7fc050` ทุกไบต์ จึงยังเป็นเวลา 9 นาทีเท่าเดิม ปุ่ม S สำหรับภาพนิ่ง ไฟล์ทุกอย่างอยู่ใน vendor แบบ offline และคำทุกคำเป็น HTML

## ขนาด dither cell ที่เลือก: 4 px ที่ 1920 และเป็นจำนวนเต็มของ device pixel เสมอ
`cell = max(2, round(4 × device px ต่อ stage px))` ได้ 4 ที่ 1920x1080 ได้ 3 ที่ 1280x720 และ 1366x768 ได้ 8 ที่ 4K จอ 2x
ค่า 4 ใหญ่กว่า proto (3) เพื่อเผื่อไว้ถ้าโปรเจกเตอร์ย่อภาพลง จุดก็ยังใหญ่พอ

**เจอบั๊กจริงค่ะ:** รอบแรก canvas อยู่ใน stage ที่ใช้ CSS scale และถึงขนาดจะตรงกัน 1:1 พอดี Chrome ก็ยัง filter ภาพ ที่ 1280 จุดจึงออกมากว้าง 2 px บวกขอบเทาอีก 1 px ตัววัดจับได้ (61%) แก้โดยย้าย canvas ออกมาเป็นชั้น fixed ใต้ stage และวาง stage บน device pixel เต็ม (ความกว้างหาร 16 ลงตัว)

## Acceptance (รันจริง ผลจริง)
**1. shot.py ทั้งสองขนาด** (`checks/r6/shot.py` คือตัวของ r5 ที่เพิ่ม argument viewport · ภาพอยู่ที่ `b1.png`…`b8.png` และ `checks/r6/shots1920/contact.png`, `checks/r6/shots1280/contact.png`)
```
$ uv run -q --with playwright python checks/r6/shot.py deck.html checks/r6/shots1920 1920x1080
1 [] 2 [] 3 [] 4 [] 5 [] 6 [] 7 [] 8 []
$ uv run -q --with playwright python checks/r6/shot.py deck.html checks/r6/shots1280 1280x720
1 [] 2 [] 3 [] 4 [] 5 [] 6 [] 7 [] 8 []
```
⚠️ รอบนี้ตัวจับ overflow ไม่ได้ทดสอบด้วย decoy ใหม่ ใช้ผลที่พิสูจน์ไว้ตั้งแต่ r3 ถึง r5 โดยแก้แค่ให้ขอบเขตตามขนาด viewport

**2. Moire** (`checks/r6/moire.py`: พิมพ์แบบ `?flat` ไม่มี grain ซ่อนคำทั้งหมด แล้วนับ run ของพิกเซลหมึกคุโระว่ายาวเป็นจำนวนเต็มเท่าของ cell หรือไม่ ทั้งแนวนอนและแนวตั้ง ครบทั้ง 8 หน้า)
```
1920x1080  canvas 1920x1080 cell 4  runs_whole_cells 0.9914
1280x720   canvas 1280x720  cell 3  runs_whole_cells 0.9906
1366x768   canvas 1360x765  cell 3  runs_whole_cells 0.9914
negative control 1280x720 &fixed1920 (canvas 1920 ถูกย่อเหลือ 1280)  0.5841
```
ส่วนที่ยังขาดอีกราว 1% อยู่ที่หน้า 7 และ 8 เป็นจุดที่หมึกคุโระพิมพ์ทับมอส ซึ่งตั้งใจให้คลาดกันอยู่แล้ว ไม่ได้เกิดจากการย่อภาพ
ดูด้วยตา: ภาพ 1280 ใน `checks/r6/shots1280/` ไม่มีลายคลื่น ⚠️ โปรเจกเตอร์จริงยังไม่ได้ลอง (ดูข้อที่ต้องตัดสิน)

**3. Offline** (`checks/r5/check.py` ตัด request http(s) ทุกตัว · ผลอยู่ที่ `checks/r6/offline.txt`)
```
ทุกหน้า: loadedFaces 7 (หน้า 8 = 9), errorFaces 0, world true, framesAdvancing true · ตัวอักษรเล็กสุด 30/30/30/30/30/30/36/48
aborted http(s) requests: 0 · local: ฟอนต์ 9 ไฟล์ + fonts.css, riso.css, riso.js, three.iife.js
nav: go ซ้ำไม่ยิง event ซ้ำ · กดค้างไม่ข้ามหน้า · S หยุดครบ (framesWhileStill 0) และเดินต่อได้
dashes ใน slide text รวม notes: 0
```
console มี warning หนึ่งตัวเรื่อง `willReadFrequently` ซึ่งมาจาก canvas วัด contrast ของ check.py เอง ส่วน `riso.js` ตั้งค่านี้ไว้แล้ว
FPS (`checks/r6/fps.py`, M4, ANGLE Metal): `60.0, 60.0, 60.0, 60.0, 59.3, 60.0, 60.0, 60.0`

**4. Negative control** (`mv vendor vendor.off` → รัน → `mv` กลับ · ผลอยู่ที่ `checks/r6/novendor.txt`)
```
1..8: "loadedFaces": 0, "world": false · ตัวอักษรเล็กสุดยังเป็น 30..48 · ls หลังรัน: มี vendor ไม่มี vendor.off
```
ภาพ `checks/r6/novendor/o1.png` ยังเป็นกระดาษชิโระที่มีข้อความครบ (stage กลับมาใช้พื้นสีกระดาษเองเมื่อไม่มีโลก 3D)

**5. คำบนจอไม่ทับภาพ** (`checks/r6/knockout.py` ซ่อนคำ แล้วนับพิกเซลหมึกภายในกรอบคำ · ผลอยู่ที่ `checks/r6/knockout.txt`)
```
ปกติ              [0, 0, 0, 0, 0, 0, 0, 3]
?decoy            [0, 0, 0, 0, 0, 0, 0, 3]        บล็อกคุโระใหญ่ใต้หัวเรื่องทุกหน้า แต่หมึกโดนตัดออกหมด
?decoy&nomask     [14059, 9390, 9710, 8851, 9459, 17654, 9964, 20727]   ปิด knockout แล้ว decoy โผล่ = decoy ลงจริง และชั้นที่ตัดคือ knockout
```
หน้า 8 มี 3 px มาจากเม็ดหมึกบนพื้นซาบิที่ห่างจากค่ากลางเกินเกณฑ์ ไม่ใช่บล็อก

**6. คำไม่เปลี่ยน** `python3 checks/r6/words.py` → `sections 8 8 identical True` · decoy: แก้คำเดียวใน `/tmp` ผลออก `identical False differing [2, 3]` (หน้า 3 มีคำเดียวกันอยู่ด้วย)

**7. ห้ามใช้:** `grep -c '[—–]' deck.html vendor/riso.js` → `0` `0` · `grep -c 'ด่าน' deck.html` → `0`

## Part B · ชุด Riso ใน kit: `hello-oracle/ψ/design-systems/rikyu-labs/slide-kit/riso/`
- `riso.js` เขียนด้วย vanilla three r169 ไม่ต้อง build มี print pass, กระดาษ, threshold และ lattice แยกตามหมึก, การพิมพ์คลาด, flood ink, knockout, พื้นกับดวงอาทิตย์, instanced blocks และ helper `field`/`pick`, `stack`, `ring`
- `riso.css` แปลง `--riso-*` มาจาก `tokens.css` และมีคลาส `.riso-hl` กับ `.riso-still` · ไฟล์อื่นได้แก่ `example.html`, `example.png`, `check.py`, `README.md` และ `vendor/three.iife.js` (+ LICENSE)
- **Acceptance:** `RISO_CHROME=… python3 check.py example.html example.png` → `"overflow": []`, `"aborted_requests": []`, `"errors": []`, cell 4, `fps_live_approx` 61 · ฟอนต์มาจากเครื่องตามแบบของ kit (`Satoshi=true, IBM Plex Sans Thai=true`) และเปิดดู `example.png` แล้ว
- **บรรทัดที่เพิ่มใน kit:** เพิ่มบรรทัดชี้ไปที่ `../riso/` ไฟล์ละหนึ่งบรรทัดใน `th/README.md` และ `en/README.md` (kit ไม่มี README ที่ราก) ⚠️ ทั้งสองไฟล์ถูกสร้างใหม่โดย `slides/build/kit.py` ทุกครั้งที่ build บรรทัดนี้จะหาย ถ้าต้องการให้อยู่ถาวรต้องแก้ใน kit.py (บรรทัด ~995 และ ~1028) ส่วนโฟลเดอร์ `riso/` เองไม่โดนลบ เพราะ build ไม่ได้ล้างโฟลเดอร์
- **บรรทัดที่เสนอให้ Dobby ใส่ในสกิล `rikyu-slides`:**
  > For a presented talk deck that needs a 3D layer, use `slide-kit/riso/` (read `riso/README.md` first: canvas outside the scaled stage, cell a whole number of device pixels, kuro = work, sabi = the human, moss = agents); never for consult, proposal or printed PDFs.

## ต้องให้คุณยิ้มหรือ Dobby ตัดสิน
- **ลองกับโปรเจกเตอร์จริงหรือจอที่ไม่ใช่ 1080p** ตั้งโน้ตบุ๊กให้ตรงกับ native resolution ของโปรเจกเตอร์ แล้วยืนดูจากกลางห้อง ถ้าเห็นลายคลื่นเฉียงบนพื้นหมึก ให้แก้ `cell: 4` ในเด็คเป็น 5
- **hello-oracle มี auto-sync** (`510234bcd brain: auto-sync 15:20`) ที่ commit `riso.js` ฉบับร่างแรกไปแล้ว และตอนนี้ `riso.css` ถูก stage อยู่ โอซ่าไม่ได้ commit เองค่ะ ไฟล์ที่เหลือจะตามไปในรอบ sync ถัดไป
- ความลื่นบนเครื่องที่ใช้ในงานยังไม่ได้วัด ถ้ากระตุก ให้ลด `shadowSize` เป็น 1024 ก่อน
- หน้า 4: บล็อกอยู่แค่ในช่องว่างระหว่างกล่อง ส่วนใต้แผนภาพเว้นเป็นกระดาษเปล่าโดยตั้งใจ (ma) ถ้าอยากให้หน้านี้เต็มกว่านี้ บอกได้เลยค่ะ
