# แผนที่ skill ของ herdr: 52 ตัว และมันโตมายังไง

> herdr คือ tmux ที่ทำใหม่ให้ AI agent อยู่ ปิดฝาโน้ตบุ๊กแล้วงานยังรันต่อบนเครื่อง บนเครื่อง m5 ของ Nat มี skill ชื่อ `/herdr-*` อยู่ 52 ตัว บทนี้จัดทั้ง 52 ตัวเป็น 7 กลุ่มตามงานที่ทำ บอกหน้าที่ตัวละหนึ่งบรรทัด (สรุปจาก description ใน SKILL.md ของมันเอง อ่านเมื่อ 8 พ.ย. 2026) ย้อนดูว่าแต่ละกลุ่มเกิดเมื่อไหร่ด้วย relic5 แล้วจบด้วยรายการสั้น ๆ ว่างานไหนใช้ตัวไหน บทนี้เป็นบทที่ 1 ของชุด herdr 6 บท ภาพมาจากวิดีโอ "Herdr part 1" และ "Herdr part 2" ที่ Nat อัดไว้เมื่อ 3 พ.ย. 2026

- ฉบับอื่น: [English](README.en.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. herdr คืออะไร

- herdr เป็น terminal multiplexer แบบ tmux แต่รู้จัก coding agent ที่รันอยู่ในแต่ละ pane (`herdr --help`: "terminal workspace manager for AI coding agents")
- โครงสร้าง: session → workspace (ใน sidebar เรียก space) → tab → pane
- เพิ่มเครื่องอื่นเข้ามาเป็น **machine** ได้ sidebar แสดงหลายเครื่องพร้อมกัน
- Nat อธิบายในวิดีโอ part 1 นาที 05:45 ว่า herdr "ก็คือ tmux นั่นแหละ แต่ทำในรูปแบบที่เป็น AI"
- รุ่นที่ใช้วันนี้: `herdr 0.9.5`

![sidebar ของ herdr บน m5: Local มี laris-team, aiexpo-oracle, ccdc-team และ worktree ย่อย ด้านล่างเป็นเครื่อง white-laris-co ที่มี media-team, rd-team, manager-team](images/00-sidebar-machines.png)

ภาพจาก part 2 นาที 24:30 (22:04 น. 3 พ.ย.) ทางซ้ายคือ sidebar: เครื่อง `Local` (m5) อยู่บน เครื่อง `white-laris-co` อยู่ล่าง แต่ละทีมมี `main` กับ worktree ของสมาชิก ทางขวายังเห็นผลของ `/herdr-dissolve` ที่ agent รันไปเมื่อ 21:36 น. (PR #130)

## 2. ทำไมถึงมี skill เยอะ

- คำสั่ง `herdr` เองมีแค่ของพื้นฐาน: `workspace`, `tab`, `pane`, `agent`, `worktree`, `machine`, `session`
- งานจริงของทีมเป็นขั้นตอนหลายคำสั่งต่อกัน เช่น เปิด issue → ตัด worktree → เปิด space → สตาร์ท agent → brief
- แต่ละขั้นตอนที่ทำซ้ำได้ ถูกเขียนเป็น skill หนึ่งตัว agent อ่าน SKILL.md แล้วทำตาม
- skill ทั้งหมดอยู่ที่ `~/.claude/skills/herdr*/` นับได้ 52 โฟลเดอร์ (ไฟล์ `.zip` สองไฟล์ในที่เดียวกันไม่นับ)

![แผนภาพ 52 skill แบ่ง 7 กลุ่ม: where am I 7, one worktree 14, talk to agents 9, rooms & teams 6, move agents 6, machines 7, sleep & clean up 3](images/03-seven-groups.png)

## 3. กลุ่ม 1: ฉันอยู่ไหน ใครอยู่รอบ ๆ (7)

| skill | ทำอะไร |
|---|---|
| `herdr` | skill ฐาน คุม herdr ผ่าน CLI ใช้ได้เฉพาะตอน `HERDR_ENV=1` คืออยู่ใน pane ของ herdr จริง |
| `/herdr-whoami` | บอกว่า agent ตัวนี้รันอยู่ที่ไหน: เครื่อง, session/space/tab/pane, session id, branch, worktree หรือ main |
| `/herdr-info` | แสดงทุกร่างของ oracle หนึ่งตัวบนเครื่องนี้ ทุก session ทุก pane และเช็คกฎหนึ่งวิญญาณหลายร่าง |
| `/herdr-tree` | ต้นไม้ของ main checkout กับทุก worktree ของ repo นี้ พร้อมสถานะ agent และ git |
| `/herdr-structure` | วาดทั้ง session เป็นต้นไม้: space ไหนเป็น room, agent ชื่ออะไร, หัวหน้าทีมคือใคร |
| `/herdr-neighbors` | สำรวจทุก pane รอบตัวก่อนแตะอะไร อ่านอย่างเดียว |
| `/herdr-twin` | หาเครื่องอื่นที่รัน session ชื่อเดียวกัน แล้วให้ sidebar แสดงเฉพาะเครื่องคู่นั้น |

## 4. กลุ่ม 2: worktree หนึ่งงาน ตั้งแต่เริ่มจนจบ (14)

เริ่มงาน:

| skill | ทำอะไร |
|---|---|
| `/herdr-wt` | เปิด issue พร้อมบริบทเต็ม → ตัด worktree ที่ `<repo>/wt/<slug>-<oracle>-<date>` → เปิด space → สตาร์ท agent แล้ว brief จาก issue |
| `/herdr-fib-wt` | ตัด worktree หลายอันพร้อมกัน วางเป็น pane ในแท็บนี้แบบเกลียว Fibonacci |
| `/herdr-idea` | เริ่ม lab ที่มีเลขลำดับ `ψ/lab/NN-slug` พร้อม worktree และ space ของมัน |
| `/herdr-issue` | เปิด issue ใน repo ของ oracle ที่ถูกตัว แล้วตัด worktree + agent ทำ issue นั้นจนเป็น PR ทำทีละหลายงานได้ |
| `/herdr-ticket` | รับ issue ที่มีอยู่แล้ว ทำใน space และ worktree แยก ชื่อ `wt/<slug>-<oracle>-issue<N>-<date>` |
| `/herdr-work` | จากชื่อ repo เดียว: สร้างหรือหา repo บน GitHub → clone → เปิด space → สตาร์ท Claude |

ระหว่างทำ:

| skill | ทำอะไร |
|---|---|
| `/herdr-rename` | เปลี่ยนชื่อ branch (ป้ายใน sidebar) เป็นชื่อที่มีความหมาย AI เลือกจากงานจริง |
| `/herdr-pr` | เซ็น PR / issue / comment ด้วยบล็อก "Built by": oracle, model, worktree, branch, transcript และที่อยู่ herdr สำหรับคุยกลับ |

ปิดงาน:

| skill | ทำอะไร |
|---|---|
| `/herdr-done` | ตรวจว่าปิด session นี้ได้ไหม: มีของค้างไหม (ยังไม่ commit, ยังไม่ push, ไม่มี upstream) |
| `/herdr-finished` | ปิดจบในรอบเดียวไม่มี popup: done → `/rrr` → `/herdr-pr` → ลบ worktree ถ้า PR merge แล้ว |
| `/herdr-wt-ship` | ตารางทุก worktree ของ repo แล้วปิดตัวที่ PR merge แล้ว: เขียน tombstone, ลบ worktree, ลบ branch |
| `/herdr-dissolve` | ด้านกลับของ `/herdr-wt` ปิดตั้งแต่ worktree เดียวจนถึงทั้งเครื่อง (`--all-but-me`, `--sweep`, `--sync`, `self`) ถามก่อนปิดเสมอ |
| `/herdr-clean-up-sync` | ชื่อเก่า รวมเข้า `/herdr-dissolve` แล้วเมื่อ 29 ต.ค. 2026 เหลือไว้แค่ชี้ทาง |
| `/herdr-trinity` | ปิดทุก worktree ของ repo ในรอบเดียวตามกฎ "เกิดขึ้น ตั้งอยู่ ดับไป": brief ทุกตัวให้ commit, push, PR, รายงาน แล้วรอ Nat สั่ง merge |

ลำดับเต็ม wt → rename → pr → dissolve อยู่ในบทที่ 2 ของชุด: [herdr-wt-lifecycle](../2026-11-08_herdr-wt-lifecycle/)

## 5. กลุ่ม 3: คุยกับ agent (9)

| skill | ทำอะไร |
|---|---|
| `/herdr-hey` | ส่งข้อความถึง agent ใน pane ข้าง ๆ แล้วอ่านคำตอบ |
| `/herdr-peek` | ดูว่า agent ข้าง ๆ ทำอะไรอยู่ อ่าน scrollback โดยไม่ขัดจังหวะ |
| `/herdr-ask` | ⌘J: กล่อง popup ส่งหนึ่งบรรทัดถึงทุก agent ในแท็บ หรือเลือกทีละตัว |
| `/herdr-roomcast` | ส่งหนึ่งบรรทัดถึงทุก agent ใน room เดียว (ตามชื่อ space) เครื่องนี้หรือเครื่องอื่น |
| `/herdr-sessioncast` | ส่งหนึ่งบรรทัดถึงทุก agent ใน session เดียว ประทับต้นทางและทางตอบกลับ |
| `/herdr-soulcast` | ส่งหนึ่งบรรทัดถึงทุกร่างของ oracle ตัวเดียว ทุก session ทุก worktree (⌘S) |
| `/herdr-send` | ส่งงานให้ oracle ตัวอื่น: เปิด issue ใน repo ของมัน ตัด worktree เลือก engine (claude, codex, omx) แล้ว brief |
| `/herdr-handover` | ยกความเป็นเจ้าของของที่รันอยู่ (repo, server, extension) ให้ agent อีกตัว แล้วดูอยู่ห่าง ๆ |
| `/herdr-pane-run` | รันคำสั่งยาวใน pane ให้คนดูสด แล้ว pane ส่งผลกับ exit code กลับมาให้ agent |

⌘J กับ ⌘L มีบทของมันเอง: [herdr ⌘J ⌘L](../2026-11-05_herdr-cmd-j-lesson/)

## 6. กลุ่ม 4: room และทีม (6)

| skill | ทำอะไร |
|---|---|
| `/herdr-room` | ดึง agent ที่รันอยู่มารวมใน space เดียว (fib/cols/rows/main) แล้วส่งกลับได้ ไม่ต้อง restart |
| `/herdr-team` | เปิด team charter (`ψ/teams/*.yaml`) เป็น agent ใน space เดียว แต่ละตัวใช้ engine ของมันและได้ brief จาก charter |
| `/herdr-team-ctl` | start / stop / status ทั้งทีมตามชื่อ charter บน session และเครื่องที่เลือก แต่ละตัวกลับมาใน conversation เดิม |
| `/herdr-lead-scouts` | หัวหน้าหนึ่ง pane ทางซ้าย scout สองตัวทางขวา แบ่งงานกัน แล้วรายงานกลับมาทางซ้าย |
| `/herdr-buddy` | แบ่ง pane แล้ววาง buddy agent ที่ไม่ถามสิทธิ์ (omx, omp, claude) ไว้ข้าง ๆ ไม่ยอมรันใน main checkout |
| `/herdr-bring-beside` | ย้าย pane อื่นมาไว้ข้างเราในแท็บนี้ agent รันต่อ conversation เดิม |

room มีบทของมัน: [herdr room](../2026-10-31_herdr-room-lesson/) ส่วน team charter: [team ecosystem](../2026-11-05_team-ecosystem-lesson/)

## 7. กลุ่ม 5: ย้าย agent (6)

| skill | ทำอะไร |
|---|---|
| `/herdr-bring` | เอา handle ของ maw มาเปิดเป็น space ใน herdr และ resume ประวัติ Claude ถ้ามี |
| `/herdr-move` | ย้าย oracle หนึ่งตัวทั้ง main และ worktree ไป session ของมันเองบนเครื่องนี้ resume ด้วย id เดิม |
| `/herdr-promote` | ให้ทีม, repo หรือ space หนึ่งได้ session ของตัวเอง: จบ agent ที่เดิม แล้ว resume ที่ใหม่ด้วย session id เดิม |
| `/herdr-unpromote` | คู่ของ promote: ดึงกลับมา session เดิม (ค่าเริ่มต้นคือ session ของคนสั่ง) แล้วลบ session ที่ว่าง |
| `/herdr-incubate` | ทำงานเรื่องของ oracle ตัวอื่นจาก repo ปัจจุบัน ตัด worktree แล้ววาง breadcrumb `.claude/INCUBATED_BY` |
| `/herdr-soul` | เอาวิญญาณของ oracle ไปทำงานใน repo อื่น มี verb `list`, `ls`, `check`, `in`, `out` |

![sidebar มีเครื่อง black-phd, white-laris-co, white-nsm, white-phonebooth, gb300, white-humanist-art และพิมพ์ /herdr-promote neo รอ Enter](images/02-promote-typed.png)

ภาพจาก part 2 นาที 32:00 (22:11 น.) Nat พิมพ์ `/herdr-promote neo` sidebar ทางซ้ายมีเครื่องที่เพิ่มไว้ 6 เครื่อง รายละเอียดอยู่ในบทที่ 4: [herdr-bring-promote](../2026-11-08_herdr-bring-promote/)

## 8. กลุ่ม 6: หลายเครื่อง (7)

| skill | ทำอะไร |
|---|---|
| `/herdr-link` | ดัชนีของชุด link: session ต่อ oracle, worker บนเครื่องอื่น, คุยกันไม่ต้องพิมพ์ ssh, ตรวจ, รื้อ |
| `/herdr-link-local` | ให้ oracle หนึ่งตัวมี session ของมันเองบน m5 ย้ายออกจาก session รวมอย่าง `laris-co` |
| `/herdr-link-remote` | ตั้ง worker oracle บนเครื่องอื่นตั้งแต่ต้นจนจบ: worktree, `.envrc`, autostart, brief |
| `/herdr-link-talk` | ให้สอง session บนสองเครื่องคุยกันได้ทั้งสองทาง ด้วย `herdr machine` แล้วทดสอบไปกลับ |
| `/herdr-link-teardown` | รื้อ worker ออกจากเครื่องอื่นอย่างสะอาด สำรองก่อนลบ ลบ branch ด้วย `-d` |
| `/herdr-link-check` | ตรวจอย่างเดียว: ทุก session, ทุกเครื่องที่บันทึกไว้, ทุกเส้นทางข้ามเครื่อง |
| `/herdr-machine-labels` | ตั้งชื่อเครื่องเป็น "<host> · <session>" ให้ sidebar อ่านเป็นคู่ |

![หน้าต่าง herdr สองบาน: m5 ทางซ้าย white ทางขวา แต่ละบานมี sidebar machines ของมัน](images/01-two-machines.png)

ภาพจาก part 2 นาที 28:00 (22:07 น.) herdr บน m5 (ซ้าย) กับบน white (ขวา) เปิดคู่กัน white ก็เห็น m5 เป็น machine (`m5-nsm`, `m5-laris-co`, `m5-phonebooth`) รายละเอียดอยู่ในบทที่ 5: [herdr-machines](../2026-11-08_herdr-machines/)

## 9. กลุ่ม 7: หลับและเก็บกวาด (3)

| skill | ทำอะไร |
|---|---|
| `/herdr-sleep` | พัก space ให้ตื่นมาที่เดิม: ขอ bookmark จาก agent, เขียน wake card (cwd, session id, คำสั่งของ pane อื่น) แล้วค่อยปิด |
| `/herdr-vacation` | ก่อนคนไปพัก: ปิด agent ที่ idle เกิน N ชั่วโมง (ค่าเริ่มต้น 3) เก็บ transcript ไว้ resume ไม่ลบ worktree |
| `/herdr-blank` | หา space ที่ทุก pane เป็น shell ว่าง ปิดได้ด้วย `--close` |

ในวิดีโอ (15:05Z) Nat สั่ง "now put media team to sleep" แล้ว "wake just pigment" รายละเอียดอยู่ในบทที่ 3: [herdr-sleep-wake](../2026-11-08_herdr-sleep-wake/)

## 10. มันโตมายังไง (ย้อนดูด้วย relic5)

วันที่มาจาก relic5 (ประวัติทุก session ทุกเครื่อง) กับวันที่ใน SKILL.md และ git ของแต่ละ skill

| วันที่ (2026) | เกิดอะไร |
|---|---|
| 31 ก.ค. | โน้ตแรก "Herdr Quick Reference" ใน vault ของ oracle: "a terminal workspace manager and runtime for AI coding agents, built in Rust" |
| 13 ก.ย. | cheat sheet ของ herdr 0.9.0 |
| 14 ก.ย. | ใน worktree `neo-herdr-14sep` ของ neo-oracle: `herdr`, `herdr-wt`, `herdr-incubate` กลายเป็น skill กลาง (`herdr-bring` ยังอยู่ในโปรเจกต์เดียว) |
| 19 ก.ย. | กลุ่มคุยข้าง ๆ: peek, hey, neighbors, handover |
| 24-29 ก.ย. | sleep, vacation, team, send |
| 3-13 ต.ค. | room (ตัวแรก), fib-wt, info, issue, move, sessioncast, roomcast, work, machine-labels, twin, ชุด link-* (11 ต.ค.) |
| 26 ต.ค. | trinity |
| 29 ต.ค. | dissolve (กิน clean-up-sync), promote, unpromote, ask (⌘J), blank |
| 30-31 ต.ค. | herdr-wt กับ herdr-room รุ่นปัจจุบัน |
| 3 พ.ย. | Nat อัดวิดีโอ Herdr part 1 + part 2 ใช้จริงหลายตัว |
| 7 พ.ย. | herdr-soul (commit แรกใน `laris-co/soul-in-repo` 10:43 น.) |

สิ่งที่เห็นจากลำดับนี้:

- เริ่มจากตัวเดียวคือ worktree (`herdr-wt`) แล้วงอกออกไปตามงานที่ทำซ้ำ
- ก.ย. เป็นเรื่อง pane ข้าง ๆ ต.ค. เป็นเรื่องทีม ห้อง และหลายเครื่อง ปลาย ต.ค. เป็นเรื่องย้ายทั้ง session และเก็บกวาด
- ชื่อเก่าไม่ลบ: `herdr-clean-up-sync` ยังอยู่ ชี้ไปที่ `/herdr-dissolve`

## 11. งานไหนใช้ตัวไหน

- **ไม่รู้ว่าตัวเองอยู่ไหน** → `/herdr-whoami` แล้ว `/herdr-structure`
- **จะเริ่มงานใหม่ที่ต้องมี branch** → `/herdr-wt` (มี issue อยู่แล้วใช้ `/herdr-ticket`)
- **อยากลองไอเดียหลายทางพร้อมกัน** → `/herdr-fib-wt`
- **งานเสร็จ อยากส่ง** → `/herdr-rename` → `/herdr-pr` → `/herdr-dissolve`
- **อยากถาม agent ข้าง ๆ** → `/herdr-peek` ดูก่อน แล้ว `/herdr-hey`
- **อยากบอกทุกคนในแท็บ** → ⌘J (`/herdr-ask`) ทั้งห้อง `/herdr-roomcast` ทั้ง session `/herdr-sessioncast`
- **อยากให้ oracle ตัวอื่นทำงานให้** → `/herdr-send`
- **อยากเห็นหลาย agent ในจอเดียว** → `/herdr-room`
- **ทีมหนึ่งกิน RAM เครื่องนี้** → ย้ายไปเครื่องอื่น (บทที่ 5) หรือ `/herdr-sleep`
- **ทีมโตจนควรมี session ของตัวเอง** → `/herdr-promote` (เอากลับด้วย `/herdr-unpromote`)
- **ก่อนออกจากคอม** → `/herdr-vacation`
- **sidebar รก** → `/herdr-blank` แล้ว `/herdr-dissolve --sweep`

## 12. ชุด herdr 6 บท

1. แผนที่ skill (บทนี้)
2. [worktree ตั้งแต่เกิดจนดับ: wt → rename → pr → dissolve](../2026-11-08_herdr-wt-lifecycle/)
3. [หลับและตื่น: sleep / wake](../2026-11-08_herdr-sleep-wake/)
4. [ย้าย agent: bring / promote](../2026-11-08_herdr-bring-promote/)
5. [หลายเครื่อง: machines](../2026-11-08_herdr-machines/)
6. [ทุกสกิล ฉบับเต็ม: อ่านหรือคัดลอกได้ทั้ง 52 ตัว](../2026-11-08_herdr-skills-full/)

บทที่เกี่ยวข้อง: [herdr room](../2026-10-31_herdr-room-lesson/), [herdr ⌘J ⌘L](../2026-11-05_herdr-cmd-j-lesson/), [team ecosystem](../2026-11-05_team-ecosystem-lesson/)

## 13. ที่มา

- `~/.claude/skills/herdr*/SKILL.md` บน m5 อ่านเมื่อ 8 พ.ย. 2026: description ทั้ง 52 ตัวอยู่ใน [captures/skill-descriptions.txt](captures/skill-descriptions.txt)
- `herdr --help` (herdr 0.9.5): [captures/herdr-help.txt](captures/herdr-help.txt)
- วิดีโอของ Nat 3 พ.ย. 2026: part 1 เริ่ม 21:07:28, part 2 เริ่ม 21:39:58 จุดที่ใช้อยู่ใน [captures/video-moments.txt](captures/video-moments.txt)
- relic5: [captures/relic5-hits.txt](captures/relic5-hits.txt)
- ข้อความแผนภาพ: [captures/diagram.txt](captures/diagram.txt)

## 14. กับดักที่เจอจริง

- **นับ skill ผิด:** ในโฟลเดอร์มี `herdr-skills.zip` กับ `herdr-skills-internal.zip` ด้วย `ls herdr*` ได้ 54 รายการ นับเฉพาะโฟลเดอร์ (`ls -d herdr*/`) ได้ 52
- **เรียกชื่อเก่า:** `/herdr-clean-up-sync` ไม่ทำงานเองแล้ว ต้องใช้ `/herdr-dissolve --sweep` หรือ `--sync`
- **รัน skill นอก herdr:** skill ฐาน `herdr` เช็ค `HERDR_ENV=1` ก่อน ถ้าไม่ใช่ pane ของ herdr ให้หยุด ไม่ไปคุม session ที่เปิดอยู่จากข้างนอก
- **agent ลบ worktree ที่ตัวเองยืนอยู่ไม่ได้:** ในภาพแรก agent รัน `/herdr-dissolve` แบบ self แล้วบอกว่า "An agent can't remove the worktree it is running in" มันเลยส่งต่อให้ pane เจ้าของ (`wDW:p1`) ลบแทน
- **space ผิดที่:** `/herdr-wt` เขียนไว้ว่า space ต้องเป็นของ repo ที่สั่ง แม้โค้ดจะอยู่อีก repo กฎนี้ "missed five times before it became a guard"
- **buddy ใน main:** `/herdr-buddy` ไม่ยอมรันใน main checkout เพราะ buddy ที่ไม่ถามสิทธิ์รันอะไรก็ได้ตรงที่ agent อื่นทำงานอยู่
