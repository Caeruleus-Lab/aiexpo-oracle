# REPORT: yim-3d deck, round 3 (tidy typography and elements)

1 พฤศจิกายน 2026 · งานตาม `BRIEF-R3.md`

> **ใครทำรอบนี้:** รอบนี้ไม่ใช่โอซ่าทำนะคะ เป็น Claude Code (Opus 5.5) ที่รันอยู่ใน workspace ของ AIExpo Oracle คุณยิ้มวาง brief ลงในเซสชันนี้โดยตรง เราเลยลงมือเองและเขียนรายงานในนามตัวเอง ไม่ได้เขียนแทนเสียงโอซ่า (Rule 6) ส่วนรอบ 1 กับ 2 ยังเป็นงานของโอซ่าตามเดิม

## สิ่งที่เปลี่ยน

### 1. ขัดเกลา (งานหลัก)
- **ใช้ type scale เดียวทั้ง deck** เขียนไว้บนสุดของ CSS มี 5 ขั้น แต่ละขั้นมีหน้าที่เดียว:
  display 156 (ประโยคส่งไมค์ และเลขใหญ่สามตัว) · heading 72 (สไลด์ละหนึ่ง และชื่อผู้พูด) · lead 48 (ใช้สองแบบ: ชื่อหัวข้อย่อยเป็น Bai Jamjuree 700 และประโยคปิดของสไลด์เป็น Sarabun 500) · body 36 · caption 30
  ขนาดเล็กที่สุดบนจอตอนนี้คือ 30px (วัดจาก DOM จริงทุกสไลด์ ดูตารางด้านล่าง) `.fnote` 24px บนสไลด์ 3 เปลี่ยนเป็น `.foot` 30px แล้ว
- **ใช้ grid เดียว:** ขอบซ้ายขวา 140 · เส้นบนของ heading อยู่ที่ 128 ทุกสไลด์ · เส้น lamp สีอำพันอยู่ที่ 88 ทุกสไลด์ (เดิมมีแค่สไลด์ 1) · จาก heading ถึงเนื้อหาห่าง 64 · จากเนื้อหาถึงประโยคปิดห่าง 64 · footnote ตรึงไว้ที่ขอบล่าง 72 ทุกสไลด์ · เลิกจัดกึ่งกลางแนวตั้ง เพราะทำให้ heading แต่ละสไลด์ขยับขึ้นลงไม่เท่ากัน
- **ภาษาของ element:** ทุกหัวข้อใช้เส้นบน 4px เหมือนกัน (สีอำพันคือหัวข้อที่สไลด์นั้นพูดถึง สีเทาคือหัวข้ออื่น) · ป้ายกำกับ (ขั้น 1, + 1 2 3) ใช้ caption Bai Jamjuree 600 แบบเดียว · สีเน้นอำพันใช้ในหัวเรื่องเท่านั้น · ไม่มีการ์ดแล้ว (สไลด์ 2 เลิกใช้กล่องพื้นหลัง เปลี่ยนเป็นเส้นบนแบบเดียวกับสไลด์ 1 และ 5) · ไม่มี bullet · กล่องจะเห็นเฉพาะในแผนภาพ (สไลด์ 3 กับ 4) และใช้ token สีพื้น/เส้นชุดเดียวกัน
- **ตัดบรรทัดภาษาไทยด้วยมือทุกจุดที่ขึ้นบรรทัดใหม่:** สไลด์ 1 ตัดที่ "คุยในแชตทีละงาน / ทุกครั้งต้องเล่าใหม่", "AI ทำได้มากขึ้น แต่ทุกงาน / รอยิ้มสั่ง รอยิ้มตรวจ", "ทีม AI หลายตัว / กับวิธีทำงานของ ARRA" · สไลด์ 3 "…เป็นคนละตัว / คนเป็นคนอนุมัติ" · สไลด์ 4 "ใครเคยดูแลทีมคน / รู้วิธีนี้อยู่แล้ว" · สไลด์ 5 "เช่น วิเคราะห์สต็อกและ SKU / ในหนึ่งนาที" และ "จากคนเรียน / กลายเป็นคนสอน" ดูทุก PNG แล้ว ไม่มีคำค้างท้ายบรรทัด
- **คอนทราสต์:** ปรับสีเทารองให้สว่างขึ้น ตอนนี้ ink-2 = 10.05:1 และ ink-3 = 7.87:1 บนพื้น (เดิม ink-3 ราว 6:1) ถ้าเป็นเนื้อความเกิน 7:1 ทุกตัว
- **สไลด์ 6:** ไม้โทบนบรรทัด display 156px ไปชนเส้น lamp เลยดันลงมา 36px แล้ว

### 2. แก้ตามรีวิวของ Codex
- **สไลด์ 3 เป็นแผนภาพสถาปัตยกรรมแผนภาพเดียว** (SVG ทุกคำเป็นข้อความจริง): ยิ้ม (Mac · มือถือ) → Discord ศูนย์กลาง → เครื่องที่เปิดตลอด (ฝูงสิบกว่าตัว, กรอบอำพัน) → ความจำร่วม เป็นไฟล์ · มีเส้นทึบสองทางจากเครื่องที่เปิดตลอดไปหาผู้ช่วยส่วนตัว Grok · Dots · Muse · มีเส้นประสองทางจาก Discord ไปหา agent ของคนอื่น พร้อมคำว่า "คุยได้ ลงมือในระบบเราไม่ได้ · คนกดอนุมัติ" · ประโยค "ตัวที่วางแผน ตัวที่ลงมือ และตัวที่ตรวจ เป็นคนละตัว คนเป็นคนอนุมัติ" กับ footnote เครื่องมือยังอยู่ครบ
  ส่วน 3D เป็นของเสริม: แสงวิ่งตามลูกศร · agent 12 ตัววนรอบเครื่องที่เปิดตลอด · ฝั่งคนอื่นมีสองแบบ คำพูดวิ่งข้ามไปถึง Discord ได้ แต่การลงมือหยุดกลางทางแล้วจางหายไป
- **ทำงาน offline ได้:** ฟอนต์อยู่ใน `vendor/fonts.css` + `vendor/fonts/*.woff2` (Bai Jamjuree 600/700, Sarabun 400/500/700, subset thai + latin, OFL) · Three.js อยู่ใน `vendor/three.iife.js` ซึ่ง build จาก three@0.169.0 ด้วย esbuild ให้เป็น classic script
  **ทำไมไม่ใช้ three.module.js ตรงๆ:** Chrome ไม่ยอมโหลด ES module จาก `file://` เราทดสอบแล้วได้ `fail Failed to fetch dynamically imported module: file:///…/vendor/three.module.js` ถ้าเปิด deck จากโฟลเดอร์ธรรมดา โมดูลจะไม่โหลด เราเลยเก็บ `vendor/three.module.js` ไว้ให้ตรงตาม brief และไว้ใช้อ้างอิง แต่ตัว deck โหลดจาก IIFE · vendor/ ทั้งโฟลเดอร์ขนาด 2.0 MB · ลบลิงก์ Google Fonts กับ import map ของ jsDelivr ออกแล้ว
- **`.num` อยู่ในการวัดเขตกันข้อความแล้ว** (สไลด์ 5) และเพิ่ม `.label` ด้วย
- **`go()` ไม่ทำอะไรถ้าสั่งไปสไลด์ที่เปิดอยู่แล้ว** · ปุ่มที่กดค้าง (`e.repeat`) จะไม่พาข้ามสไลด์
- **โหมดภาพนิ่ง:** กดปุ่ม `S` หรือคลิกปุ่ม "S ภาพนิ่ง" มุมขวาล่าง (ตอนเปิดจะขึ้นว่า "S ภาพนิ่ง: เปิด" เป็นสีอำพัน) แล้ว loop จะหยุด CSS จะไม่เคลื่อนไหว และ 3D แสดงภาพนิ่งหนึ่งภาพต่อสไลด์ · เปิดด้วย `?still` ใน URL ได้ · ถ้าเปลี่ยนค่า reduced-motion ของ OS ระหว่างพูด ระบบก็ตามด้วย

## Acceptance (รันจริง ผลจริง)

**1. shot.py**
```
$ uv run -q --with playwright python /private/tmp/claude-502/-Users-yim/5aabf861-4d65-4575-9c86-30c641119993/scratchpad/shot.py deck.html .
1 []
2 []
3 []
4 []
5 []
6 []
```
เปิดดู b1.png ถึง b6.png ครบทุกภาพแล้ว

**2. Offline:** เปิดจาก `file://` และ abort ทุก request http/https (`checks/r3/check.py`, ผลเต็มอยู่ใน `checks/r3/offline.txt`, ภาพอยู่ใน `checks/r3/offline/o1-6.png`)
```
1 {"min": 30, "minWho": "ขั้น 1", "fontsCheck": true, "loadedFaces": 8, "errorFaces": 0, "world": true, "frames": 173, "framesAdvancing": true}
2 {"min": 30, "minWho": "+", "fontsCheck": true, "loadedFaces": 8, "errorFaces": 0, "world": true, "frames": 284, "framesAdvancing": true}
3 {"min": 30, "minWho": "Mac · มือถือ", "fontsCheck": true, "loadedFaces": 8, "errorFaces": 0, "world": true, "frames": 395, "framesAdvancing": true}
4 {"min": 30, "minWho": "พิธีทั้งสามเป็นของ Oracl", "fontsCheck": true, "loadedFaces": 8, "errorFaces": 0, "world": true, "frames": 507, "framesAdvancing": true}
5 {"min": 36, "minWho": "เล่าจากงานจริงบน product", "fontsCheck": true, "loadedFaces": 8, "errorFaces": 0, "world": true, "frames": 617, "framesAdvancing": true}
6 {"min": 48, "minWho": "คุณนัทพาทำ 6 บทเรียนทำตา", "fontsCheck": true, "loadedFaces": 9, "errorFaces": 0, "world": true, "frames": 727, "framesAdvancing": true}
contrast {'ink': 16.76, 'ink2': 10.05, 'ink3': 7.87, 'accent': 9.84, 'amberInk': 9.32}
dashes in all slide text incl. notes: 0
nav {"eventsFirstGo": 1, "eventsAfterTwoSameGo": 0, "slideAfterRepeatKey": 2, "slideAfterRealKey": 3, "stillOn": true, "button": "S ภาพนิ่ง: เปิด", "framesWhileStill": 0, "framesAfterResume": 30}
aborted http(s) requests: 0 []
local files loaded: [BaiJamjuree-600/700 thai+latin, Sarabun-400/500 thai+latin, Sarabun-700-latin, deck.html, fonts.css, three.iife.js]
```
`min` คือขนาดตัวอักษรเล็กที่สุดบนสไลด์ (px ที่ stage 1920 และคิด scale ของ SVG แล้ว) · `aborted 0` หมายถึง deck ไม่ได้ขอไฟล์จาก network เลยสักไฟล์

**ระวัง `fonts.check()`:** ค่านี้ใช้เป็นหลักฐานเดี่ยวๆ ไม่ได้ ใน decoy ด้านล่างกับใน negative control มันตอบ `true` ทั้งที่โหลดฟอนต์ได้ **0 face** เพราะถ้าไม่มี `@font-face` ชื่อนั้นเลย check ก็ตอบ true ไปเอง หลักฐานจริงจึงเป็น `loadedFaces` (นับ face ที่ status = loaded) และรายชื่อไฟล์ woff2 ที่โหลดจากดิสก์จริง
อีกเรื่องหนึ่ง: ตอนแรก check ตอบ `false` เพราะ `40px "Bai Jamjuree"` (weight 400) ไปจับ face 500 ซึ่งไม่มีที่ไหนใช้และไม่เคยโหลด เราเลยลบ face 500 ของ Bai Jamjuree ออก (ย้ายไฟล์ไปไว้ที่ /tmp ไม่ได้ลบทิ้ง)

**Decoy ของตัว router:** เอา deck รอบ 2 (ที่ใช้ Google Fonts + jsDelivr) มารันผ่านสคริปต์เดียวกัน ได้ `aborted http(s) requests: 2` (fonts.googleapis.com, cdn.jsdelivr.net) และ `world: false, loadedFaces: 0` แปลว่า router ตัด network ได้จริง ดังนั้นเลข 0 ของ deck ใหม่หมายถึงไม่ได้ใช้ network จริงๆ ไม่ใช่ router ไม่ทำงาน (`checks/r3/decoy.txt`)

**3. Negative control:** เปลี่ยนชื่อ `vendor/` เป็น `vendor.off` แล้วรันสคริปต์เดียวกัน จากนั้นเปลี่ยนชื่อกลับ (`checks/r3/novendor.txt`, ภาพอยู่ใน `checks/r3/novendor/`)
```
1..6: "loadedFaces": 0, "world": false   (ทุกสไลด์ยังมีข้อความ ขนาดเล็กสุด 30/30/30/30/36/48 เท่าเดิม)
console: 3D world disabled, deck content stays fully visible Error: vendor/three.iife.js did not load
ls หลังรัน: vendor อยู่ · vendor.off ไม่มีแล้ว
```
ดู `novendor/o3.png` แล้ว แผนภาพสไลด์ 3 ยังครบทุกคำ ใช้ฟอนต์ไทยของระบบแทน

**4. ขีดยาว:** `grep -c '[—–]' deck.html` → `0` (ทั้งไฟล์ รวม notes) · ใน notes สไลด์ 4 เดิมเขียน "หน้า 3–5" ตอนนี้เปลี่ยนเป็น "หน้า 3 ถึง 5"

## สิ่งที่ไม่ได้ทำ หรือต้องให้คุณยิ้ม/Dobby ตัดสิน
- **ไม่ได้เรียก skill impeccable critique/polish และ osaa-design-system เป็นรอบแยก** เราตรวจและแก้เอง (type scale, grid, element, คอนทราสต์, ตัดบรรทัด) แล้ววัดผลด้วยสคริปต์ด้านบน ถ้าอยากได้มุมมองอิสระ ควรส่งให้คนอื่นรีวิวต่อ
- **ข้อความสไลด์ 3 ที่ตัดออกจากจอ** เพราะแผนภาพใช้คำตาม brief: "ศูนย์กลางคือ Discord ยิ้มสั่งงานและเห็นงานทุกตัวในที่เดียว" · "แขกแต่ละคนได้กุญแจของตัวเอง เปิดได้แค่ไม่กี่อย่าง" · "ไปขอให้ agent ในฝูงทำงานให้ได้เอง" ทั้งสามประโยคยังอยู่ใน notes/ที่มา ถ้าคุณยิ้มอยากเอาประโยคไหนกลับขึ้นจอ บอกได้เลยค่ะ
- **ไม่ได้แตะเรื่องที่ Codex ยกมาแต่ไม่อยู่ใน brief นี้:** หลักฐานตัวเลขสไลด์ 5 · คำที่ฟังเหมือนสัญญาเด็ดขาด (ไม่มีอะไรหาย / AI ไม่ตัดสินแทน) · notes ที่ขึ้นบนจอเวที · เวลารวม 10:30 · ทั้งหมดยังเปิดอยู่
- **ความลื่นบนเครื่องที่ใช้จริงในงาน** ยังไม่ได้วัด ถ้ากระตุกให้กด `S`
- `BRIEF-R4.md` (สไลด์ "ฝูงบริหารแบบบริษัท") โผล่ขึ้นมาระหว่างที่เราทำรอบนี้ เรายังไม่ได้แตะนะคะ
- ยังไม่ได้ commit ไฟล์ไหนเลย

— AIExpo Oracle workspace · Claude Code (Oracle AI)
