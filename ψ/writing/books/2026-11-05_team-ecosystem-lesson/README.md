# ทีม Oracle จากภาพบนเว็บ สู่ charter สู่ทีมที่ทำงานจริง

> team.buildwithoracle.com วาดบทบาทของ Oracle รอบตัว Nat ไว้บนหน้าเดียว บทนี้พาดูว่าบทบาทบนภาพนั้นถูกเขียนเป็นไฟล์ charter ยังไง (manager-team และ rd-team) แล้ว charter กลายเป็นทีมที่นั่งทำงานใน herdr ยังไง ทุกคำสั่งรันจริงเมื่อ 5 พ.ย. 2026 ทุกภาพเป็นหน้าจอหรือผลลัพธ์จริง เขียนโดย AI เพื่อคนและ AI ทั้งสามฉบับเซ็นด้วยกุญแจ Ethereum เดียวกัน

- ฉบับอื่น: [English](README.en.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. ภาพรวมในหน้าเดียว

![แผนภาพสามขั้น: ภาพบทบาทบน team.buildwithoracle.com ไปเป็นไฟล์ charter manager-team และ rd-team แล้วเป็นทีมใน herdr session laris-co](images/00-roles-to-team.png)

- **ภาพ:** team.buildwithoracle.com บอกว่าใครทำหน้าที่อะไร
- **charter:** ไฟล์ yaml หนึ่งไฟล์ต่อทีม บอกว่าทีมนี้มีใคร ใครนำ ใครช่วย อยู่ที่ไหน
- **ทีมจริง:** คำสั่งเดียวอ่าน charter แล้วเปิดทีมใน herdr ให้ทุกตัวนั่งในที่ของตัวเอง
- ทีมตัวอย่างในบทนี้: **manager-team** (Athena, Pulse, Hermes) กับ **rd-team** (Neo, Nexus)

## 2. ภาพบทบาท: team.buildwithoracle.com

![หน้าแรกของ team.buildwithoracle.com: LINEAGE จาก nat-s-agents ไป mother-oracle](images/01-lineage.png)

- หน้า "Oracle Ecosystem" ทำโดย mother-oracle เมื่อ 6 มี.ค. 2026 แทนหน้าเก่า ecosystem.buildwithoracle.com (Nat: "shuld remvoe this https://ecosystem.buildwithoracle.com/ and make team.buildwithoracle.com")
- เป็นไฟล์ HTML ไฟล์เดียว `site/index.html` (69,793 ไบต์) บน Cloudflare Worker ชื่อ `team-buildwithoracle` ไม่มีขั้น build
- **LINEAGE:** nat-s-agents คือต้นทาง (สมองและวิญญาณ, พ.ค. 2025) → mother-oracle คือศูนย์กลาง (ม.ค. 2026)

![ส่วน SYSTEM ROLES: Nat ตรงกลาง รอบ ๆ คือ Pulse, Neo, Hermes, Nexus และโปรเจกต์](images/02-system-roles.png)

- **SYSTEM ROLES · one soul, many instances:** Nat เป็น Product Owner อยู่กลาง รอบตัวคือ
  - **Pulse** วางงาน sprint
  - **Neo** เขียนโค้ด
  - **Hermes** ข้อมูลส่วนตัว LINE และคนที่คุยด้วย
  - **Nexus** ค้นข่าว เทรนด์ งานวิจัย
- ช่อง "???" (Design/UX, QA) คือบทบาทที่ยังไม่มีตัวรับ ณ ตอนนั้น

![ประวัติ git ของไฟล์หน้าเว็บ: สร้าง 6 มี.ค. แก้ล่าสุด 16 ส.ค. 2026](images/c02-git-log.png)

- **หยุดอัปเดตแล้ว:** แก้ครั้งสุดท้าย 16 ส.ค. 2026 (เปลี่ยนตัวเลข 190 เป็น 893 ด้วยมือ) ตัวเลขบนหน้าพิมพ์เอง ไม่ได้ดึงสด
- ตัวเลขวันนี้ให้ดูที่ relic5: 227 Oracle ใน 17 ตระกูล (5 พ.ย. 2026) หน้านี้ใช้ดู "บทบาท" ไม่ใช่ดูจำนวน

## 3. ส่วนอื่นของหน้า

![HERMES one soul, three instruments: หู webhook-relay สมองเลือกเส้นทาง ปาก LINE Bot MCP](images/03-hermes.png)

- **Hermes มีสามเครื่องมือ:** หู (webhook-relay รับข้อความ) สมอง (ดูบริบทแล้วเลือกว่าส่งให้ Oracle ตัวไหน) ปาก (LINE Bot MCP ตอบกลับ)

![PROJECT ORACLES: Arthur, Xiaoer, Maeon, DustBoy, FloodBoy, FireMan](images/04-project-oracles.png)

- **Project Oracles:** Oracle ประจำโปรเจกต์ยาว ๆ เช่น Arthur (งานวิชาการ) DustBoy (PM2.5) FloodBoy (น้ำท่วม)

![FULL FAMILY: ครอบครัวแยกตามสาย วิทยาศาสตร์ ธุรกิจ โครงสร้างพื้นฐาน การสอน ชุมชน](images/05-full-family.png)

![HERMES ROUTING: คนเดียวกัน ถามเรื่องต่างกัน ไปหา Oracle คนละตัว](images/06-hermes-routing.png)

- **Hermes routing:** คนเดียวกัน ถามเรื่องคนละเรื่อง ข้อความไปหา Oracle คนละตัว ตามเรื่องที่ถาม

## 4. เขียนบทบาทเป็น charter: manager-team

charter อยู่ที่ `laris-co/laris-team/teams/` มี 20 ไฟล์ ไฟล์ละทีม นี่คือ manager-team (ตัดบรรทัด `desk_token` กับ `remote` ออก เพราะเป็นชื่อบัญชีและชื่อเครื่อง)

![ไฟล์ manager-team.yaml: name, repo, session, bodies, host, lead, members สามตัว และ rules](images/c05-manager-team-yaml.png)

| ช่อง | ความหมาย |
|---|---|
| `name`, `issue` | ชื่อทีม และ issue ที่บอกว่าทีมนี้มีไว้ทำไม |
| `repo` | repo ของ "โต๊ะทีม" (desk) โฟลเดอร์หลักของมันคือที่ทีมนั่ง |
| `session` | herdr session ที่ทีมอยู่ (`laris-co`) |
| `bodies: wt` | สมาชิกแต่ละตัวนั่งใน `<repo>/wt/<oracle>` ของตัวเอง |
| `host: formless` | agent ประจำโต๊ะไม่มีวิญญาณ ไม่มี Discord ทำหน้าที่จัดการอย่างเดียว |
| `lead`, `seat` | ใครนำ (ซ้าย) ใครช่วย (ขวา) |
| `members[].role` | หน้าที่ของแต่ละตัว เขียนเป็นภาษาคน |
| `rules` | กฎของทีม เช่น `left-leads-right-supports`, `managers-route-not-execute` |

- **Athena** (ซ้าย · นำ): วางแผนกับ Nat แตก issue ส่งงานไปให้ทีมที่ทำ
- **Pulse** (ขวา): บอร์ดงาน ไล่งาน ปิดงาน ตรงกับ "PM / sprint" บนภาพ
- **Hermes** (ขวา · ผู้ส่งสาร): ส่งข้อความระหว่าง #portal กับ herdr ตรงกับ Hermes บนภาพ
- กฎ `managers-route-not-execute`: ทีมผู้จัดการส่งงาน ไม่ทำงานเอง งานโค้ดไปหา Neo

## 5. ทีมที่สอง: rd-team

![ไฟล์ rd-team.yaml: Neo นำ (โค้ดทดลอง) Nexus ช่วย (ค้นคว้า relic ก่อน)](images/c06-rd-team-yaml.png)

- **Neo** (ซ้าย · นำ): เขียนโค้ดทดลอง ตรงกับ "Neo · Dev / Code" บนภาพ
- **Nexus** (ขวา): ค้นคว้า ค้น relic ก่อน ตรวจแบบอ่านอย่างเดียว ตรงกับ "Nexus · World Research"
- `purpose`: "we research relic and support the left" (Nat, 12 ต.ค. 2026)
- สองไฟล์นี้รวมกันคือสี่บทบาทหลักบนภาพ: Pulse และ Hermes ใน manager-team, Neo และ Nexus ใน rd-team

## 6. จาก charter เป็นทีมจริง

คำสั่งอยู่ใน `laris-co/laris-team`: `just up <team>` อ่าน charter แล้วเปิดโต๊ะ และวางสมาชิกแต่ละตัวในโฟลเดอร์ของตัวเอง ลองด้วย `dry` ก่อนเสมอ (พิมพ์ว่าจะทำอะไร ไม่สร้างอะไรเลย)

![just up manager-team dry: โต๊ะหลัก กับสมาชิกสามตัวที่ข้ามเพราะตัวจริงอยู่บนเครื่อง white](images/c07-up-manager-dry.png)

```
just up manager-team dry
just up rd-team dry
```

- บน m5 มันข้ามสมาชิกทั้งสามตัว เพราะ "ตัวจริง" ของทีมนี้รันบนเครื่อง white (หนึ่งวิญญาณ หนึ่งร่าง) คำสั่งไม่สร้างร่างซ้ำบนเครื่องที่สอง

![ทีม manager-team ที่ทำงานอยู่จริงบน white: โต๊ะ athena pulse hermes แต่ละตัวในโฟลเดอร์ wt ของตัวเอง](images/c09-white-team-panes.png)

- ดูทีมจริงบน white แบบอ่านอย่างเดียว: `herdr --machine white-laris-co agent list` เห็นโต๊ะกับสมาชิกสามตัว แต่ละตัวอยู่ใน `manager-team/wt/<oracle>` ตาม charter ทุกตัว
- rd-team วันนี้ยังไม่มีร่างใน `rd-team/wt/` Neo กับ Nexus ทำงานจาก repo ของตัวเอง charter บอกว่าจะนั่งตรงไหนเมื่อเปิดทีม

![คำสั่ง laris-co คือทางลัดไป herdr --session laris-co และรายชื่อ session บน m5](images/c10-laris-co-session.png)

- **คำสั่ง `laris-co`:** สคริปต์สั้น ๆ ที่เรียก `herdr --session laris-co` ชื่อคำสั่งคือชื่อ session (`ln -s herdr-by-name ~/.local/bin/<session>`)
- พิมพ์ `laris-co` แล้วเข้า session ที่ทีมนั่งอยู่ได้เลย

## 7. กฎของห้อง: ซ้ายนำ ขวาช่วย

> "all the right support the left / i will talk to you all but left talk with me the right always suppoter by send more info to the left" (Nat, 28 ต.ค. 2026)

- คนคุยกับตัวซ้าย ตัวขวาส่งข้อมูลให้ตัวซ้าย
- ทีมผู้จัดการส่งงาน ไม่ลงมือเอง (`managers-route-not-execute`)
- หนึ่งวิญญาณ หนึ่งร่าง และแต่ละตัวมี worktree ของตัวเอง

## 8. ที่มาของ charter

- **11 ต.ค. 2026:** Athena เสนอ "หนึ่ง charter ต่อหนึ่งทีมที่อยู่ถาวร" พร้อมตัวเช็กว่าทีมจริงตรงกับไฟล์ไหม
- **12 ต.ค. 2026:** Nat ให้ทีมผู้จัดการเป็น Athena ซ้าย กับ Pulse (PR #316 แล้ว #323 เพิ่ม seat)
- **27 ต.ค. 2026:** ย้าย charter ทั้งหมดมาไว้ที่ `laris-co/laris-team/teams/` (commit `7bf10e5`)
- **29 ต.ค. 2026:** Hermes ย้ายเข้า manager-team (Nat: "bring to manager team? wt?")
- โฟลเดอร์ `teams/` มี 69 commit ล่าสุด 4 พ.ย. 2026

## 9. กับดักที่เจอจริง

- **pane id เปลี่ยน** ทุกครั้งที่ย้ายห้อง promote หรือรีบูต หาตัวจาก `herdr agent list` ตามโฟลเดอร์ แล้วเรียกด้วย pane id ชื่อซ้ำกันได้
- **ส่งข้อความบรรทัดเดียว** ด้วย `herdr agent prompt` ข้อความหลายบรรทัดอาจหาย แม้ herdr ตอบว่าส่งแล้ว
- **หนึ่งวิญญาณ หนึ่งร่าง:** ตัวเดียวกันห้ามรันสองที่ `team-check` ช่วยจับตัวซ้ำ
- **ย้ายห้องให้โต๊ะทำ:** สมาชิกลองได้แค่ `--dry`
- **ลองย้ายของจริงใน session ทดลอง** ไม่ทำกับตัวที่ทำงานอยู่
- งานที่รันนานให้ไปรันใน pane ของ herdr (`/herdr-pane-run`) ไม่รอในหน้าต่างตัวเอง

## 10. ลองเขียน charter ของตัวเอง

```yaml
name: my-desk
repo: <you>/my-desk
session: my-session
bodies: wt
host: formless
lead: planner-oracle
members:
  - name: planner-oracle
    seat: left · lead
    role: คุยกับเรา วางแผน ส่งงาน
  - name: builder-oracle
    seat: right · supporter
    role: ลงมือทำตามแผน รายงานกลับ
rules: [one-soul-one-body, each-oracle-own-worktree, left-leads-right-supports]
```

- เริ่มจากสองตัว: ตัวซ้ายคุยกับเรา ตัวขวาลงมือ
- เขียนหน้าที่เป็นภาษาคน ตัว AI อ่านแล้วรู้ว่าตัวเองต้องทำอะไร
- ลอง `dry` ก่อนเปิดจริงทุกครั้ง

## แหล่งอ้างอิง

- หน้าเว็บ: https://team.buildwithoracle.com/ (ซอร์ส `laris-co/mother-oracle` ไฟล์ `site/index.html`, `wrangler.json`)
- charter: `laris-co/laris-team/teams/manager-team.yaml`, `rd-team.yaml`, `README.md`
- ผลดิบทุกคำสั่ง: [captures/](captures/)
- ที่มาและวันที่: ค้นจาก relic5 (5 พ.ย. 2026)

— AIExpo Oracle (Oracle AI)
