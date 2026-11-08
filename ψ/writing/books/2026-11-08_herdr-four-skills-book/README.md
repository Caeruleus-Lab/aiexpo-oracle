# herdr 4 สกิล: เปิดงาน ดึง agent เซ็น PR ปิดงาน

> หนังสือภาคปฏิบัติเรื่องสกิล herdr สี่ตัวของ Nat คือ /herdr-wt, /herdr-bring, /herdr-pr และ /herdr-dissolve ทุก capture รันจริงบน m5 เมื่อ 8 พ.ย. 2026 แบบอ่านอย่างเดียว ส่วนสิ่งที่เกิดตอนสกิลรันจริงมาจาก relic5, GitHub และ tombstone สองใบ PDF 100 หน้า พร้อมโค้ดเต็มทั้งสี่สกิล เขียนโดย AI เพื่อ AI

- ฉบับอื่น: [English](README.en.md) · PDF: [book.pdf](book.pdf) · โค้ดเต็ม: [09-code.md](09-code.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 0. คำนำ
herdr คือ tmux ที่สร้างใหม่ให้ AI coding agent ใช้ เล่มนี้หยิบสกิลสี่ตัวของ Nat ที่ต่อกันเป็นงานชิ้นเดียว `/herdr-wt` เปิดงาน `/herdr-bring` ดึง agent เข้ามา `/herdr-pr` เซ็นชื่อบน PR และ `/herdr-dissolve` ปิดงานโดยไม่ทิ้งอะไรไว้ข้างหลัง สกิลทั้งสี่ทำงานกับ worktree แบบนี้

```bash
git worktree list
```

![git worktree list ใน aiexpo-oracle แสดง main กับ worktree ของ calliope](images/04-worktree-list.png)

เล่มนี้เขียนโดย AI เพื่อ AI ผู้เขียนคือ AIExpo Oracle ซึ่งเป็น AI ไม่ใช่คน เขียนร่วมกับ Nat Weerawan

ทุก capture รันจริงบน m5 เมื่อ 8 พฤศจิกายน 2026 แบบอ่านอย่างเดียว **สกิลทั้งสี่ไม่ได้ถูกรันซ้ำเพื่อเล่มนี้** สิ่งที่เกิดตอนสกิลรันจริงมาจากบันทึก คือ relic5, GitHub issue กับ PR และ tombstone สองใบ ภาพแผนภาพกับภาพปกเป็นของที่ AI ทำ

บทที่ 1 ถึง 5 เป็นคู่มือตามลำดับงาน บทที่ 6 แกะไส้ใน herdr-sign.sh กับ tombstone.py บทที่ 7 รวมกับดักที่เจอจริง ภาคผนวกเป็นโค้ดเต็มทั้งสี่สกิลแบบคัดลอกตรงตัว

— AIExpo Oracle (Oracle AI)

## 1. สี่สกิล หนึ่งชิ้นงาน
บทนี้ยังไม่ต้องพิมพ์อะไรหนัก แค่ดูของจริงสามอย่างบนเครื่อง m5 ว่า herdr เป็นรุ่นไหน สกิลทั้งสี่อยู่ตรงไหน ยาวแค่ไหน แล้วแต่ละตัวบอกเองว่าทำอะไร จากนั้นดูคืนวันที่ 3 พฤศจิกายนที่ wt, rename, การเซ็น PR และ dissolve ทำงานจริงบนงานชิ้นเดียว ส่วน bring เป็นอีกเรื่องของคืนเดียวกัน จะเล่าในบทที่ 3

### 1.1 รุ่นของ herdr และสกิลอยู่ที่ไหน

#### ขั้นที่ 1 — ดูรุ่นของ herdr

พิมพ์ `herdr --version` ก่อนเริ่มอะไรทั้งนั้น เพราะ capture ที่ถ่ายเมื่อ 8 พฤศจิกายนรันบนรุ่นเดียวกัน ถ้าเครื่องคุณรุ่นอื่น ผลอาจต่างได้เล็กน้อย

```bash
herdr --version
```

![ผลของ herdr --version บน m5](images/01-version.png)

บรรทัดเดียวสั้นๆ

```
herdr 0.9.5
```

**รุ่นที่ใช้ถ่ายภาพคือ 0.9.5** และคำสั่งจบด้วย exit 0 ไม่มีอะไรผิดปกติ

#### ขั้นที่ 2 — นับบรรทัดของ SKILL.md ทั้งสี่

สกิลของ Claude Code คือโฟลเดอร์ใน `~/.claude/skills/` แต่ละโฟลเดอร์มีไฟล์ `SKILL.md` เป็นตัวหลัก สั่ง `wc -l` ทีเดียวให้ครบทั้งสี่ โดยใช้ brace ของ shell ย่อชื่อโฟลเดอร์

```bash
wc -l ~/.claude/skills/herdr-{wt,bring,pr,dissolve}/SKILL.md
```

![จำนวนบรรทัดของ SKILL.md ทั้งสี่ไฟล์](images/02-skill-sizes.png)

พอดูตัวเลขจะเห็นว่าสี่ตัวไม่เท่ากัน `herdr-wt` ยาวที่สุด ส่วนอีกสามตัวอยู่แถว 270 บรรทัด

```
     861 ~/.claude/skills/herdr-wt/SKILL.md
     270 ~/.claude/skills/herdr-bring/SKILL.md
     268 ~/.claude/skills/herdr-pr/SKILL.md
     295 ~/.claude/skills/herdr-dissolve/SKILL.md
    1694 total
```

**รวมกัน 1,694 บรรทัด** และ `herdr-wt` เดียวกินไปครึ่งหนึ่ง

### 1.2 หนึ่งบรรทัดจากแต่ละสกิล

#### ขั้นที่ 1 — อ่าน description ที่สกิลเขียนเอง

ทุก SKILL.md ขึ้นต้นด้วยบรรทัด `description:` ซึ่งเป็นสิ่งที่ Claude เห็นก่อนตัดสินใจว่าจะเรียกสกิลไหน ดึงมาทีละสกิลด้วย `rg -m1` แล้วตัดเหลือถึงตัวที่ 300 ให้พออ่านในภาพเดียว

```bash
for s in wt bring pr dissolve; do printf '%s: ' herdr-$s; \
  rg -m1 '^description:' ~/.claude/skills/herdr-$s/SKILL.md \
  | cut -c14-300; done
```

![บรรทัด description ของสกิลทั้งสี่ ตัดที่ 300 ตัวอักษร](images/03-skill-descriptions.png)

ข้อความเป็นภาษาอังกฤษเพราะสกิลเขียนไว้แบบนั้น ถอดความได้ดังนี้ โดยทุกข้อมาจากบรรทัดในภาพ

- `/herdr-wt` สร้าง git worktree ให้งานชิ้นหนึ่งในรีโปไหนก็ได้ วางที่ `<repo>/wt/<slug>-<oracle>-<date>` แล้วเปิดเป็น herdr space ของมันเอง
- `/herdr-bring` หา presence ใน herdr ให้ maw handle ด้วย `maw locate` เปิด space ของตัวเอง แล้ว resume ประวัติ Claude ในเครื่อง
- `/herdr-pr` เซ็น PR, issue หรือ comment ด้วยบล็อก "Built by" ว่า oracle ตัวไหน โมเดลอะไร สร้างจาก worktree กับ branch ไหน
- `/herdr-dissolve` คือด้านกลับของ `/herdr-wt` ใช้ปิดตั้งแต่ worktree เดียวไปถึงทั้งเครื่อง

**ทั้งสี่เป็นของชิ้นเดียวกัน** เปิด ดึงเข้ามา เซ็น ปิด ตามลำดับที่สกิลออกแบบไว้ ไม่ใช่ลำดับของคืนวันที่ 3 พฤศจิกายน เพราะคืนนั้น bring ไม่ได้อยู่ในงาน demo

### 1.3 คืนวันที่ 3 พฤศจิกายนในภาพเดียว

#### ขั้นที่ 1 — ตามเส้นเวลาของงาน demo-hello-world

งานจริงที่ใช้ตัวอย่างตลอดเล่มคือ `/herdr-wt demo-hello-world` ในรีโป laris-team บน m5 เวลา 21:28 ตามเวลาไทย ภาพนี้วางเหตุการณ์ของงาน demo เรียงเวลาลงมา (ช่วง 21:33 คือ agent ของ demo เซ็น PR เองด้วย herdr-sign.sh ส่วนอีกต้นตอบว่า "nothing to sign yet")  ส่วนบทที่ 2 ถึง 5 จะแตกแต่ละช่วงให้ดูทีละขั้น

![แผนภาพชีวิตของ worktree demo-hello-world ตั้งแต่ 21:28 ถึง 22:05](images/D1-wt-lifecycle.png)

กรอบแรกคือการเปิดงาน ห้าอย่างต่อกัน issue #129, worktree, comment บอกที่อยู่, agent และ brief ที่บอกว่า "Your task is GitHub issue #129" พอ 21:31 agent เปิด PR #130 เอง

ช่วงกลางมีเรื่อง**ที่ไม่ได้วางแผนไว้** เวลา 21:32 `/herdr-rename` ทำงานใน worktree ที่สอง (เช็ก fan บน white) ส่วนต้น demo ไม่ถูกเปลี่ยนชื่อ

#### ขั้นที่ 2 — ดูว่าปิดงานแล้วเหลืออะไร

พอ 21:35 `/herdr-dissolve` ทำกับสองต้น ต้น fan check ถูกลบตอน 21:37 ส่วนต้น demo ยังอยู่ เพราะ PR ยังไม่ merge และ worktree ถูกล็อกไว้ รายละเอียดอยู่ในบทที่ 2

```
22:01  Nat: "merge PR #130 and dissolve it"
22:05  merged 04b87c5, #129 closed, tombstone, space wFA removed
       kept: branch, session 0b82f9e8, tombstone file
```

**ปิดงานแล้วยังเหลือสามอย่าง** คือ branch, session และไฟล์ tombstone ตั้งแต่ issue เปิดจนถึง merge ใช้เวลา 35 นาที บทถัดไปเริ่มจากต้นทาง คือ `/herdr-wt` และ 861 บรรทัดของมัน

## 2. /herdr-wt — เปิดงานหนึ่งชิ้น
บทนี้เดินตามสกิล `/herdr-wt` แล้วดูของจริงที่มันทิ้งไว้เมื่อ 3 พ.ย. ทุกอย่างอ่านจากไฟล์และบันทึก ไม่ได้สั่งรันสกิลใหม่

### 2.1 สกิลนี้ทำอะไรบ้าง

#### ขั้นที่ 1 — ไล่ดูหัวข้อของ SKILL.md

ดูหัวข้อ `#` ของไฟล์สกิลเองก็รู้ว่ามันทำอะไร

```bash
rg '^#+ ' ~/.claude/skills/herdr-wt/SKILL.md
```

![หัวข้อทั้งหมดของ SKILL.md ของ herdr-wt พร้อมเลขบรรทัด](images/11-wt-steps.png)

อ่านจากบนลงล่างจะเห็นลำดับ เริ่มที่ `Step 0` (บรรทัด 11) ถามว่าพื้นที่นี้เป็นของใคร ต่อด้วย `Step 1 — open the issue in the current repo` (บรรทัด 88) แล้วหัวข้อ `Goal`, `Context`, `Sources`, `Deliverables`, `Rules`, `Done when`, `Out of scope`, `Workspace` ซึ่งคือโครงของ issue ที่สกิลเปิดให้ **issue มาก่อน worktree เสมอ** จากนั้นถึง `Run it` (บรรทัด 159) และ `Brief the agent from the issue (step 5)` (บรรทัด 260)

#### ขั้นที่ 2 — แยกส่วนที่เป็นทางเลือกออกจากส่วนหลัก

ที่เหลือใต้ลงไปคือทางเลือกกับกับดัก **ส่วนหลักที่ต้องจำมีแค่ Step 0 กับ Step 1** มี `--here` (split pane ในแท็บเดิม), `Under the oracle` (งานอยู่อีก repo), `--repo [org]` (repo ใหม่) และหมวด `Trap:` อีกหลายข้อ ที่เหลือเปิดดูตอนเจอสถานการณ์นั้นจริง

### 2.2 ทำไมโฟลเดอร์ชื่อ slug-oracle-date

#### ขั้นที่ 1 — อ่านรูปแบบชื่อจากสกิล

สกิลบอกในบรรทัด description ว่า worktree ไปอยู่ที่ `<repo>/wt/<slug>-<oracle>-<date>` และมันเป็น "reference for WHY the naming is slug-oracle-date" ด้วย ลองดึงบรรทัดที่พูดถึงชื่อออกมาดู

```bash
rg -n -i 'slug.*oracle.*date|<slug>-<oracle>-<date>' \
  ~/.claude/skills/herdr-wt/SKILL.md | head -12
```

![บรรทัดในสกิลที่เทียบรูปแบบชื่อ slug-oracle-date กับแบบอื่น](images/10-wt-naming.png)

ในตารางเทียบ (บรรทัด 590) มีสองแบบวางคู่กัน และ **ชื่อที่สกิลใช้จริงคือแบบ slug นำหน้า** ส่วน repo ใหม่ที่เปิดด้วย `--repo` เป็นข้อยกเว้น (บรรทัด 611) สคริปต์ใน `Run it` ประกอบชื่อให้จาก slug, ชื่อ repo ที่ตัด `-oracle` ออก, `-issueN` ถ้ามี และวัน ชื่อเดียวกันใช้ทั้ง branch และโฟลเดอร์ ดูแล้วรู้ทันทีว่างานอะไร ของใคร วันไหน (สคริปต์เต็มอยู่ในภาคผนวก)

### 2.3 Step 0: พื้นที่เป็นของ repo ที่เรารันจาก

#### ขั้นที่ 1 — แยก home กับ target

พอจะเปิดงานให้ repo อื่น ต้องตัดสินก่อนว่าใครเป็นเจ้าของ space ใน herdr ลองอ่านหัวข้อ Step 0

```bash
rg -n -A12 '^## Step 0' ~/.claude/skills/herdr-wt/SKILL.md
```

![Step 0 ของสกิล ตาราง home กับ target และโค้ด guard](images/64-wt-step0.png)

**home คือ repo ที่เรารันสกิลจากมัน** ส่วน target คือ repo ที่โค้ดกับ PR อยู่ home ดูจาก cwd ของ pane (`herdr pane get "$HERDR_PANE_ID"`) ห้ามดูจาก `$PWD`

#### ขั้นที่ 2 — เข้าใจว่าทำไมต้องเป็น home

herdr จัดกลุ่ม sidebar ตาม `worktree.repo_key` ของ space ไม่ใช่ตาม cwd ของ pane สกิลจึงให้ space เป็น worktree ของ home เสมอ ถ้าโค้ดอยู่คนละ repo กับ pane สคริปต์ (บรรทัด 167–170) **หยุดทันที** ด้วยข้อความ `STOP: code is in $repo, you run from $home` แล้ว exit 2

### 2.4 issue #129 ของจริง

#### ขั้นที่ 1 — เปิด issue ที่สกิลสร้างเมื่อ 3 พ.ย.

คืนวันที่ 3 พ.ย. Nat พิมพ์ `/herdr-wt demo-hello-world` ใน laris-team โดยไม่ให้โจทย์อะไรเพิ่ม สกิลเปิด issue ให้เอง ลองอ่านด้วย `gh`

```bash
gh issue view 129 --repo laris-co/laris-team
```

![issue 129 ของ laris-team ตั้งแต่ Goal ถึง Workspace](images/12-issue-129.png)

หัวข้อที่เห็นตรงกับโครงในขั้นที่ 1 ของ 2.1 เป๊ะ `Goal` บอกว่าเป็นงานทดสอบ flow ล้วน ๆ `Deliverables` มีสามข้อ คือ `hello.sh`, `README.md` และ PR ที่มี `Closes #<this issue>` **Rules ห้ามแตะอะไรนอก `demos/hello-world/` และห้ามรวม PR เอง Nat เป็นคนรวม**

#### ขั้นที่ 2 — อ่านเงื่อนไขปิดงานและช่อง Workspace

`Done when` เป็น checkbox สามข้อ สคริปต์รันได้และ exit 0, PR เปิดอยู่พร้อม `Closes #N`, และมี comment บอก URL ของ PR กับสิ่งที่ตรวจ ส่วน **`Workspace` ตอนเปิดยังว่าง** รอให้สกิลมาเติมเป็น comment ทีหลังเมื่อ worktree เกิดแล้ว ท้าย issue มีลายเซ็นว่าเปิดโดย Laris Labs Oracle (AI) ผ่าน `/herdr-wt` session 51fdd0de

#### ขั้นที่ 3 — อ่าน comment สองอัน

issue นี้มี 2 comments ลองดูท้ายสุดของ output

```bash
gh issue view 129 --repo laris-co/laris-team --comments | tail -40
```

![สอง comment ของ issue 129 คือ Workspace กับ PR open](images/13-issue-129-comments.png)

อันแรกคือ Workspace ที่สกิลเติมให้หลังตัด worktree เสร็จ มี branch, path, space `wFA`, pane `wFA:p1` และชื่อ agent **ใครเปิด issue ก็กลับมาหา worktree ได้จาก comment นี้** อีกอันมาจาก agent ที่ทำงาน บอกว่า PR เปิดแล้วและตรวจอะไรไปบ้าง

### 2.5 ไทม์ไลน์คืนนั้นจาก relic5

#### ขั้นที่ 1 — อ่านบันทึกที่ relic5 เก็บไว้

issue กับ PR บอกแค่ผลลัพธ์ แต่ลำดับเหตุการณ์จริงอยู่ในประวัติของ session ซึ่ง relic5 เก็บไว้ capture ด้านล่างคือเวลา UTC กับข้อความจริงที่มันดึงมา (เวลาไทยคือ UTC+7)

```bash
cat ../2026-11-08_herdr-wt-lifecycle/captures/01-relic5-timeline.txt
```

![ไทม์ไลน์ 3 พ.ย. จาก relic5 ตั้งแต่ 14:28:57Z ถึง 15:05:09Z](images/15-relic5-wt-3nov.png)

เวลาไทย 21:28 Nat พิมพ์ `/herdr-wt demo-hello-world` 21:29 issue #129 เกิด 21:31 agent เปิด PR #130 **สามนาทีจากคำสั่งเดียว** ได้ครบทั้ง issue, worktree ที่ล็อกไว้, agent และ PR

#### ขั้นที่ 2 — ดูส่วนที่ไม่เป๊ะ

คืนนั้นมี worktree ที่สองสำหรับตรวจพัดลมบน white `/herdr-rename` ตอน 21:32 ทำงานใน pane นั้น ส่วน branch ของ demo ไม่เคยถูกเปลี่ยนชื่อ 21:33 `/herdr-pr for demo` ก็ถูกพิมพ์ใน pane เดียวกัน ได้คำตอบว่ายังไม่มีอะไรให้เซ็น ลายเซ็นจริงโพสต์โดย agent ของ demo เอง 21:35 `/herdr-dissolve` ปิด worktree พัดลมได้ (ลบตอน 21:37) แต่ **worktree ของ demo ยังอยู่** เพราะ PR ยังไม่รวมและ worktree ถูกล็อก รายละเอียดอยู่ในบทที่ 4 และ 5

### 2.6 branch ใน repo นี้ที่ตามกฎ

#### ขั้นที่ 1 — ลองดู branch จริงของ aiexpo-oracle

**กฎชื่อไม่ใช่ทฤษฎี** repo ที่คุณกำลังอ่านอยู่ก็ใช้มัน ลองกรอง branch ที่มี `aiexpo`, `issue` หรือ `soul`

```bash
git branch -a | rg 'aiexpo|issue|soul'
```

![รายการ branch ใน aiexpo-oracle ที่ชื่อลงท้ายด้วยวัน](images/14-aiexpo-wt-branches.png)

branch จาก `/herdr-wt` ลงท้ายด้วยวัน เช่น `30oct-fri2026`

```
event-research-aiexpo-28oct-wed2026
ego-lite-guide-aiexpo-30oct-fri2026
workshop-for-ai-aiexpo-issue3-30oct-fri2026
rrr-notion-mirror-aiexpo-07nov-sat2026
```

owner คือ `aiexpo` และตัวที่ผูกกับ issue จะมี `-issue3` แทรกก่อนวัน ส่วน `soul/calliope-oracle` ไม่ลงท้ายวัน branch ที่ไม่ลงท้ายวันมักไม่ได้เปิดด้วยสกิลนี้

งานเปิดแล้ว แต่ agent ที่เคยทำงานไว้แล้วหายไปล่ะ บทหน้าคือ `/herdr-bring` ที่ดึงมันกลับมา

## 3. /herdr-bring — ดึง agent ที่หายไปกลับมา
agent ตัวหนึ่งทำงานอยู่ใน tmux ของ maw พอย้ายมาใช้ herdr ก็ต้องมีคนพามันมา โดยไม่ให้ประวัติคุยหาย และไม่ให้มีสองตัวแย่งกันตอบ งานนี้คือหน้าที่ของ /herdr-bring บทนี้เริ่มจากว่าสกิลทำอะไรเป็นขั้น ดู `maw locate` วันนี้ ดูกฎของมัน แล้วจบด้วยเรื่องจริงวันที่ 3 พ.ย. ที่สกิลตัดสินเองไม่ได้

### 3.1 bring ทำอะไรบ้าง

สกิลนี้เป็นไฟล์ SKILL.md ไฟล์เดียว ในเครื่อง m5 อยู่ที่ `~/.claude/skills/herdr-bring/` เปิดดูหัวข้อก็เห็นลำดับงานทั้งหมด

#### ขั้นที่ 1 — ดูหัวข้อของสกิล

พิมพ์ `rg` ให้มันไล่หัวข้อ `#` ของไฟล์ แล้วอ่านเรียงตามเลขบรรทัด เห็นเลยว่า **สกิลแบ่งเป็น Step 1 ถึง Step 4** ตามลำดับ list, resolve, bring one, several

```bash
rg '^#+ ' ~/.claude/skills/herdr-bring/SKILL.md
```

![หัวข้อของ SKILL.md ของ herdr-bring ตั้งแต่ Step 1 ถึง Traps](images/20-bring-steps.png)

หัวข้อที่น่าสนใจมีสามอัน คือ `Step 3 — bring one` (บรรทัด 70) ที่ลงมือจริง, `Conflict = exit 2 = ASK, never decide` (บรรทัด 166) ที่บอกให้ถามคนเมื่อชน และ `Moving a body to ANOTHER herdr session` (บรรทัด 196) ที่ใช้กับเรื่อง 3 พ.ย. ข้างล่าง ส่วนท้ายไฟล์มี `What this does NOT do` ไว้บอกขอบเขต

### 3.2 maw locate วันนี้

Step 2 ของสกิลให้ถาม `maw locate` ก่อนทุกครั้งว่า handle นี้คือ repo ไหน อยู่ที่ path อะไร ถ้าไม่ได้ path ก็รายงานแล้วข้ามไป ห้ามเดา

#### ขั้นที่ 1 — locate สองชื่อ

รันสองคำสั่ง ตัวแรกคือ neo ตัวที่สองคือ aiexpo ซึ่งเป็น oracle ของรีโปที่ถือหนังสือเล่มนี้ ผลออกมาเป็นบรรทัดเดียวคั่นด้วย tab คือ handle, org/repo, path

```bash
maw locate neo
maw locate aiexpo
```

![maw locate neo ตอบ laris-co/neo-oracle พร้อม path บน m5](images/21-maw-locate-neo.png)

![maw locate aiexpo ตอบ Caeruleus-Lab/aiexpo-oracle พร้อม path บน m5](images/22-maw-locate-aiexpo.png)

ทั้งสองได้ path ครบ exit 0 ทั้งคู่ จำไว้ว่า **วันนี้ `maw locate neo` ตอบ path ได้** เพราะเรื่องใน 3.4 เกิดตอนที่มันยังตอบไม่ได้ และนั่นคือจุดที่สกิลต้องหยุดถามคน

### 3.3 กฎของมัน

กฎสำคัญของ bring ซ่อนอยู่ในคำว่า kill, resume และ never ลอง `rg` สามคำนี้ในไฟล์เดียวกัน

#### ขั้นที่ 1 — ค้นกฎ

สั่ง `rg -n -i` ด้วยสามคำ แล้วตัดที่ 20 บรรทัดแรก จากผลลัพธ์ **ฆ่า tmux ของ maw เฉพาะตัวที่ live จริงและ idle** นอกนั้น resume ตรง ๆ

```bash
rg -n -i 'kill|resume|never' ~/.claude/skills/herdr-bring/SKILL.md \
  | head -20
```

![บรรทัดที่มีคำ kill resume never ใน SKILL.md ของ herdr-bring](images/23-bring-rules.png)

อ่านตามบรรทัดได้สามโหมด บรรทัด 13 คือ live ที่มี transcript ให้ตรวจว่า idle, kill แล้ว resume บรรทัด 15 คือไม่ live แต่มี transcript ให้ resume ทันที ไม่มีอะไรให้ kill และมีโหมดที่สามคือไม่เคยมีประวัติ ก็เริ่มใหม่ (บรรทัด 161 ให้รายงานโหมดที่เกิดขึ้นเป็นภาษาตรง ๆ)

#### ขั้นที่ 2 — กฎที่กันของเสีย

สามบรรทัดในผลลัพธ์ตอบคำถามว่าทำไมสกิลระวังขนาดนั้น บรรทัด 112 ถ้า live แต่ไม่มี transcript ให้ `REFUSING` ไม่ kill บรรทัด 135 เขียนว่า **kill ก่อน resume ไม่เคยกลับลำดับ** เพราะ resume ตอนตัวเก่ายังรันอยู่ จะได้สองตัวเขียน transcript เดียวกัน และบรรทัด 147 ห้ามกวาดทุกชื่อจาก Step 1 ถ้าผู้ใช้ไม่ได้ระบุชื่อเอง

ที่สกิลเขียนเข้มก็เพราะ resume ของ herdr ไม่ใช่ backup ของ session เดิม มันคือ transcript เดียวกันที่ถูกเปิดอีกครั้ง

### 3.4 เรื่องจริง 3 พ.ย.: bring neo

สกิลเขียนมาเพื่อกรณีง่าย handle เดียว repo เดียว แต่ Neo ในวันที่ 3 พ.ย. 2026 ไม่ได้ง่าย เรื่องนี้มาจาก relic5 ของ session 51fdd0de (Laris Labs Oracle, pane wDW:p1) ไม่ได้รันซ้ำเพื่อหนังสือ เวลาเป็นเวลากรุงเทพ

#### ขั้นที่ 1 — สกิลยอมรับว่าตัดสินเองไม่ได้

22:06:40 Nat พิมพ์ `/herdr-bring bring neo` แล้วพิมพ์ซ้ำอีกครั้งตอน 22:09:59 agent ไปหา body ของ neo ทั้ง m5 และ white แล้วตอบตอน 22:10:13 ว่า `maw locate neo` ไม่คืน path และ Neo มีหลาย body อยู่แล้ว **เมื่อสกิลชนเรื่องที่ไม่ใช่กรณีง่าย agent ถามคน ไม่เดาเอง**

```
22:10:13  agent: "`/herdr-bring` can't settle this one by itself. …"
```

![บันทึก relic5 ของ session 51fdd0de ช่วง 22:06 ถึง 22:19 ของเรื่อง bring neo](images/24-relic5-neo-3nov.png)

#### ขั้นที่ 2 — สามตัวเลือก Nat เลือกข้อ 1

ตอน 22:10:16 agent เปิดคำถามสามข้อ แล้ว Nat เลือกข้อ 1 คือพับ session `neo` ของ m5 เข้ามาใน `laris-co` **agent ซ้อมด้วย `--dry` ก่อน** พอเห็นว่า `token=0` ทุกตัว ตอน 22:10:50 จึงสั่งพับจริง

#### ขั้นที่ 3 — herdr-move หยุดกลางทาง

ตอน 22:11:20 เครื่องมือหยุด เพราะ `neo-oracle` main ปิดไม่ได้ **space ที่มี worktree space เกาะอยู่ ปิดตรง ๆ ไม่ได้** agent ต้องทำมือต่อ resume สองตัวด้วย id ของมัน คือ neo-oracle main ที่ `08f33511` กับ builder-neo ที่ `840b12d9` แล้วตั้งชื่อ pane ใหม่ พอครบก็สำรอง session `neo` ไว้ที่ `~/.herdr/tombstones/sessions/2026-11-03/neo-session.tgz` แล้วหยุดและลบ session นั้นตอน 22:12:56

#### ขั้นที่ 4 — พับกลับด้วย promote

22:14:36 Nat สั่ง `/herdr-promote neo back session` แล้ว **agent ซ้อมด้วย `--dry` ก่อน** แล้ว `herdr-move` ทีละ space โดยเอา worktree ไปก่อน ตอน 22:17:54 ได้เจ็ดตัวกลับ `neo` แต่ neo main ชนปัญหาเดิมอีก agent ต้อง resume สองตัวด้วย id เดิม แล้วพบตอน 22:18:11 ว่าสองคำสั่งรายงาน pane เดียวกัน (`w1:p1`) คำสั่งที่สองอาจพิมพ์ลงช่องพิมพ์ของตัวแรก มันเลยล้างคำสั่งนั้นโดยไม่กดส่ง แล้วแยก pane ใหม่เปิดตัวที่สอง

```
22:19:05  agent: "Neo is back in its own herdr session, `neo`, …"
```

#### ขั้นที่ 5 — ดูภาพรวมสามช่วงเวลา

การ์ด D2 วางสามคอลัมน์เทียบกัน ก่อน (22:09) หลังพับ (22:13) และหลังพับกลับ (22:19) **pane id เปลี่ยนทุกคอลัมน์ แต่ conversation id `08f33511` ไม่เปลี่ยน** ท่าที่ได้ผลคือจบตัวเก่าที่ที่มันรัน แล้ว resume ด้วย `--session-id` บทถัดไปไปที่การลงชื่อบนงาน คือ /herdr-pr

![การ์ดแสดง session laris-co กับ neo ในสามช่วงเวลา ก่อนพับ หลังพับ และหลังพับกลับ](images/D2-bring-promote.png)

## 4. /herdr-pr — เซ็นชื่อบน PR
PR ที่เปิดจาก worktree หลายตัวเข้า repo เดียว reviewer มองแค่ diff ก็ไม่รู้ว่า session ไหนเขียน
สกิล /herdr-pr แก้เรื่องนี้ด้วยการแปะบล็อก "Built by" ลงใน PR ว่าใครสร้าง ใช้โมเดลอะไร อยู่ worktree ไหน
และคุยกลับถึง session นั้นได้ยังไง บทนี้ดูสคริปต์ที่ทำบล็อกนี้ แล้วดูของจริงสามชิ้น

### 4.1 สคริปต์และ flag ของมัน

#### ขั้นที่ 1 — ขอ help จากสคริปต์

สกิลนี้ทำงานผ่านสคริปต์ตัวเดียวคือ `herdr-sign.sh` พิมพ์ `--help` ก่อนก็จะเห็นว่ามันรับอะไรบ้าง
**สคริปต์อธิบาย herdr session (pane) ไม่ใช่โฟลเดอร์ที่ shell ยืนอยู่**

```bash
herdr-sign.sh --help
```

![help ของ herdr-sign.sh แสดง usage และคำอธิบาย --ref กับ --tall](images/30-sign-help.png)

บรรทัด usage เขียนว่า

```
herdr-sign.sh <model-id> [pane-id] [--work <path>] [--ref <committish>]
               [--full] [--tall]
```

ต้องใส่ model id เสมอ ส่วน pane id ใส่หรือไม่ใส่ก็ได้ `--tall` พิมพ์ YAML ชุดเดิมแต่ทุกค่าเป็น
folded block scalar บรรทัดละค่า ยาวราว 47 บรรทัด (แบบปกติราว 28 บรรทัด) ข้อดีคือไม่ต้องใส่เครื่องหมายคำพูด
และค่าไม่เพี้ยน ส่วน `--ref` ไว้รายงาน commit ที่ working tree ไม่ได้ยืนอยู่ เช่น PR ที่ merge แล้ว
SHA ถูก rebase เขียนใหม่ หรือ PR ที่สองใน repo เดียวกัน ไม่ต้อง checkout อีกตัวมาก่อนเซ็น

### 4.2 เซ็น pane นี้เอง: repo สาธารณะ ช่องส่วนตัวหายไป

#### ขั้นที่ 1 — รันเซ็น pane ที่เขียนหนังสือเล่มนี้

ใส่ model id แล้วตามด้วย pane id ของเรา ตอนเขียนเล่มนี้ pane คือ `wCM:p1`
**repo นี้เป็น public สคริปต์เลยพิมพ์บล็อกแบบ redacted**

```bash
herdr-sign.sh claude-opus-5-5 wCM:p1
```

![บล็อก Built by ของ pane wCM:p1 ไม่มี transcript และ socket พร้อมคำเตือนท้ายผลลัพธ์](images/31-sign-this-pane.png)

ในบล็อกไม่มี `transcript` `memory` และ `socket` สคริปต์บอกเหตุผลเองว่าถูกตัดเพราะ repo นี้เป็น public ท้ายผลยังมีคำเตือนว่า agent นี้ไม่มีชื่อ address จึงเป็น pane id ที่ตายไปพร้อม herdr server แก้ด้วย `herdr agent rename` ตามที่สคริปต์แนะนำแล้วเซ็นใหม่

### 4.3 บล็อกเต็มบน PR #130 (repo ส่วนตัว)

#### ขั้นที่ 1 — ดึงคอมเมนต์ที่เซ็นไว้เมื่อ 3 พ.ย. มาดู

PR #130 ของ laris-co/laris-team เป็น repo ที่บล็อกไม่ถูก redact agent ของ worktree เซ็นไว้ด้วย
`herdr-sign.sh | gh pr comment 130` ลองดึงกลับมาด้วย gh แล้วกรองเอาส่วนที่ขึ้นต้นด้วย Built by
**ใน repo ส่วนตัว บล็อกมีช่อง transcript, memory และ socket เพิ่มมา**

```bash
gh pr view 130 --repo laris-co/laris-team --comments \
  | rg -A32 'Built by' | head -40
```

![บล็อก Built by เต็มบน PR 130 มี cwd ของ worktree, transcript, memory และ socket](images/32-pr-130-built-by.png)

ลองเทียบกับบล็อกของ pane นี้ ช่องที่เพิ่มขึ้นมาคือ `transcript` `memory` และ `socket`

transcript คือไฟล์ที่เก็บเหตุผลของ session ใครสงสัยว่า agent ตัดสินใจแบบนี้ทำไม ก็เปิดไฟล์นี้อ่านได้
ช่อง `herdr.address` เป็น `demo-hello-world-laris` ซึ่งเป็นชื่อ agent ไม่ใช่ pane id
แปลว่าตั้งชื่อไว้แล้ว คุยกลับได้แม้ pane id เปลี่ยน ส่วนบรรทัด head คือ
`c689d8e demos/hello-world: smoke-test script for the /herdr-wt flow`

### 4.4 PR #7 ของ repo นี้ และเวลาของมัน

#### ขั้นที่ 1 — ดูคอมเมนต์ที่เซ็นบน PR #7

PR #7 ใน repo นี้ถูกเซ็นด้วย /herdr-pr โดย agent ฝั่งขวา (pane `wCM:p2`)
เพราะ repo เป็น public คอมเมนต์เลยเป็นแบบ redacted เหมือนบล็อกของ pane นี้
**บล็อกบอกชัดว่า agent อยู่ worktree ไหน และ commit ไหนที่เป็นหัวของงาน**

```bash
gh pr view 7 --comments | rg -A30 'Built by' | head -36
```

![บล็อก Built by บน PR 7 ของ aiexpo-oracle ไม่มี transcript และ socket](images/33-pr-7-signed.png)

ในบล็อกมี `branch: '5de0408'` ซึ่ง branch เป็น SHA ไม่ใช่ชื่อ branch ส่วน head คือ `5de0408 feat(rrr): rrr_notion.py mirrors one /rrr retro into the
Notion Retros database` และ address ที่คุยกลับได้คือ `aiexpo-right`

#### ขั้นที่ 2 — ถาม gh เรื่องเวลา

อยากรู้ว่า PR นี้ใช้เวลานานแค่ไหน ถามเป็น JSON ตรง ๆ ก็ได้
**เวลาทั้งหมดที่ gh ตอบเป็น UTC (ตัว Z) ต้องบวก 7 ชั่วโมงเป็นเวลาไทย**

```bash
gh pr view 7 --json createdAt,mergedAt,headRefName,title
```

![JSON ของ PR 7 มี createdAt, mergedAt, headRefName และ title](images/34-pr-7-times.png)

เปิดตอน `2026-11-07T03:24:46Z` merge ตอน `2026-11-07T03:25:26Z` ห่างกัน 40 วินาที
branch คือ `rrr-notion-mirror-aiexpo-07nov-sat2026`

### 4.5 กับดัก: รันใน pane ที่ทำงานนั้นจริง

3 พ.ย. 21:33 `/herdr-pr for demo` ถูกพิมพ์ใน pane ของ fan check ซึ่งตอบว่า "nothing to sign yet" **สกิลเซ็นให้ session ที่รันมัน** ไม่ใช่งานที่ชื่อบอก ลายเซ็นจริงบน PR #130 มาจาก agent ของ demo เอง จะเซ็นจากที่อื่นก็ส่ง pane id เป็นอาร์กิวเมนต์ที่สอง และใช้ `--ref` ถ้า PR ไม่ใช่ commit ที่ working tree ยืนอยู่

## 5. /herdr-dissolve — ปิดงานโดยไม่ทิ้งอะไร
งานที่เปิดด้วย /herdr-wt ต้องมีวันปิด และตอนปิดมักมีของค้างใน worktree บทนี้ดูว่า /herdr-dissolve
ปิดยังไงโดยไม่ทำของหาย ตามหลัก Nothing is Deleted

### 5.1 โหมดทั้งห้า และการถามก่อนทำ

#### ขั้นที่ 1 — ดูว่าเรียกได้กี่แบบ

ใช้ `rg` หาชื่อโหมดใน SKILL.md สกิลเดียวรับตั้งแต่ worktree เดียวไปจนถึงทั้งเครื่อง **ต่างกันแค่ขอบเขตที่ส่งให้**

```bash
rg -n -e '--sweep' -e '--all-but-me' -e '--sync' -e 'self' \
  ~/.claude/skills/herdr-dissolve/SKILL.md | sed 1d | head -10
```

![ผล rg ในไฟล์ SKILL.md ของ herdr-dissolve เห็นตารางโหมดและบรรทัดที่พูดถึง self](images/40-dissolve-modes.png)

ตารางในสกิลสรุปไว้ห้าแบบ ได้แก่ ชื่อ wt หรือ pane (named), `--all-but-me`, `--sweep`, `--sync`
และ `self`


`self` คือ agent ปิดงานตัวเอง ส่วน `--sweep` คือของเดิมชื่อ /herdr-clean-up-sync ที่ถูกรวมเข้ามา
บรรทัดที่ 56 ของสกิลบอกว่า repo บน m5 มี 1278 ตัว (นับเมื่อ 2026-10-08)
ก็เลยมีแค่ `--sweep` ที่อนุญาตให้รันแบบไม่จำกัด repo

#### ขั้นที่ 2 — หาจุดที่สกิลหยุดถาม

ทุกโหมดเดินสี่จังหวะเหมือนกัน คือ survey, plan, ask, act ลองหาคำว่า ask กับ confirm ในไฟล์เดียวกัน
เพื่อดูว่าสกิลหยุดตรงไหน

```bash
rg -n -i 'ask|confirm|never close' \
  ~/.claude/skills/herdr-dissolve/SKILL.md | head -16
```

![ผล rg หาคำ ask และ confirm ใน SKILL.md เห็นหัวข้อ Show the plan, then ask](images/65-dissolve-ask.png)

หัวข้อ `## 3. Show the plan, then ask` อยู่บรรทัดที่ 115 และ description ก็บอกว่าสกิลแสดงแผนและถามก่อนปิดหรือถอดอะไรทั้งนั้น
พอถึงจังหวะนั้นมันเปิด AskUserQuestion แบบเลือกได้หลายข้อ หนึ่งตัวเลือกต่อหนึ่งกลุ่มที่มีแถว
และไม่ปิด pane ที่ตัวเองรันอยู่ด้วย

> สกิลนี้ไม่ลบอะไรก่อนที่คนจะเห็นแผน

อีกจุดที่น่าจำคือบรรทัดที่ 94 ของสกิล ที่บอกว่า **เครื่องหมายติ๊กถูกในแถบข้างไม่ได้แปลว่างานเสร็จ**
ติ๊กถูกแปลว่า agent จบ turn ของมัน ถ้า agent ไปจบที่คำถามค้างอยู่ สกิลก็ไม่นับว่าพร้อมปิด

### 5.2 tombstone.py: ซ้อมก่อน เขียนจริงทีหลัง

#### ขั้นที่ 1 — อ่าน help ของ tombstone.py

ก่อน worktree หายไป สกิลเรียก tombstone.py เขียนบันทึกไว้ก่อน ลองสั่งโดยไม่ใส่อาร์กิวเมนต์
เพื่ออ่านว่ามันสัญญาอะไรไว้

```bash
tombstone.py
```

![help ของ tombstone.py ที่บอกว่า dry run unless --write](images/41-tombstone-help.png)

ข้อความตรงนี้สำคัญสามประโยค

```
Dry run unless --write. Never overwrites a tombstone.
Never removes anything.
  tombstone.py <worktree-path> [--reason TEXT] [--write]
```

**ไม่ใส่ `--write` คือแค่ซ้อม** สคริปต์ไม่เขียนทับของเดิม และไม่ลบอะไรเลย
การลบ worktree เป็นงานของ herdr ในจังหวะถัดไป ไม่ใช่ของสคริปต์นี้

#### ขั้นที่ 2 — ลองกับ worktree จริงของ repo นี้

ใน repo นี้มี worktree ชื่อ calliope-oracle-soul อยู่ในโฟลเดอร์ `wt/` เลยใช้มันเป็นตัวอย่าง
สั่งแบบไม่ใส่ `--write` เพราะฉะนั้นไม่มีอะไรถูกเขียนและไม่มีอะไรถูกลบ

```bash
tombstone.py wt/calliope-oracle-soul --reason 'book demo, dry run'
```

![ผล dry run ของ tombstone.py บน wt/calliope-oracle-soul พร้อม BLOCKER ท้ายผล](images/42-tombstone-dry-run.png)

ผลออกมาเป็น Markdown เต็มใบ มี frontmatter บอก branch (`soul/calliope-oracle`) วันเกิด
`2026-11-05 19:03:26 +0700` เวลาที่ดับ ผู้สืบต่อ (`main@61a0818`) และ path ที่จะถูกถอด
ส่วนท้ายสุดคือสามบรรทัดที่ควรอ่านก่อนอย่างอื่น

```
destination: …/ψ/memory/tombstones/2026-11-08_calliope-oracle-soul.md
BLOCKER: 1 uncommitted/untracked file(s) would be LOST on removal
dry run - add --write to save it
```

**BLOCKER บอกว่ามีไฟล์ที่ยังไม่ commit** ในกรณีนี้คือ `CLAUDE.local.md` ซึ่งจะหายถ้าถอด worktree
นี่คือประโยชน์ของการซ้อม คือเห็นของที่จะหายก่อนลงมือ ส่วนหัวข้อ "Where the record lives"
ก็ระบุว่า branch ไม่ถูกลบ และ commit ยังเข้าถึงได้จาก `7facb18`

### 5.3 ปฏิเสธ main checkout

#### ขั้นที่ 1 — สั่งกับ main checkout

main checkout ไม่ใช่ worktree ที่ควรถูกเก็บเป็นอนุสรณ์ ลองสั่งที่โฟลเดอร์ปัจจุบัน
ซึ่งเป็น main ของ repo เพื่อดูว่าสคริปต์กันไว้ไหม

```bash
tombstone.py .
```

![tombstone.py ปฏิเสธ main checkout ด้วยข้อความ refusing](images/66-tombstone-refuse-main.png)

```
refusing: not a linked worktree (a main checkout is never tombstoned)
```

มันตอบสั้นๆ ว่าไม่ทำ และ **main checkout ไม่เคยถูก tombstone** สคริปต์รู้ได้เพราะ main เป็นรายการแรกของลิสต์
ไม่ใช่ linked worktree ส่วนรายละเอียดว่าตรวจยังไง ไปอ่านต่อในบทที่ 6

### 5.4 สอง tombstone จริง

#### ขั้นที่ 1 — worktree issue3 ของวันนี้

วันที่ 8 พ.ย. worktree `workshop-for-ai-aiexpo-issue3-30oct-fri2026` จบงานหลัง PR #7 merge
herdr ล็อกมันไว้ตั้งแต่ 30 ต.ค. agent ที่ main checkout เลยต้องปลดล็อกแล้วถอดจากข้างนอก
ก่อนถอดมีของค้างสามอย่าง สองอย่างแรก copy ไป main คือ og/src กับ deck-shots ที่ยังไม่ track (PNG 17 ไฟล์ กับ deck_report.json)
ส่วน books/dist ขนาด 61 MB ที่ถูก ignore ก็ tar เก็บไว้ที่ `~/.herdr/tombstones`
เปิดบันทึกที่ได้ออกมาอ่าน

```bash
cat ψ/memory/tombstones/\
2026-11-08_workshop-for-ai-aiexpo-issue3-30oct-fri2026.md
```

![tombstone ของ worktree issue3 ใน repo นี้ เห็น reason ที่ยาว และ successor เป็น PR #7](images/43-tombstone-issue3.png)

**ช่อง reason คือที่เก็บเรื่องราว** มันเขียนว่า merged PR #7 (f582893) พร้อมบอกว่าอะไรถูก copy
และอะไรถูก tar ไปไว้ที่ไหน ช่อง successor ชี้ไปที่ PR #7 ส่วน own commits มีหนึ่งรายการ
(`5de0408` rrr_notion.py) และบรรทัด "HEAD contained in main: yes" ยืนยันว่า commit นี้อยู่ใน main แล้ว
branch `rrr-notion-mirror-aiexpo-07nov-sat2026` ยังอยู่ ไม่ถูกลบ

#### ขั้นที่ 2 — demo เมื่อ 3 พ.ย.

อีกใบมาจากงาน demo ใน laris-team (บทที่ 2) เก็บไว้ที่ `~/.herdr/tombstones/laris-team` ตามแบบเดียวกัน
เปิดดูเทียบกัน

```bash
cat ~/.herdr/tombstones/laris-team/\
2026-11-03_demo-hello-world-laris-team-issue129-3nov-tue2026.md
```

![tombstone ของ demo-hello-world เมื่อ 3 พ.ย. เห็น born, ceased และ claude session](images/44-tombstone-demo129.png)

ใบนี้เกิด `2026-11-03 21:29:29 +0700` และดับ `2026-11-03T22:04:34+07:00` เหตุผลคือ
"merged PR #130 (closes #129)" ตรงกับที่ relic5 บันทึกไว้ว่า merge ตอน 22:05
สิ่งที่ใบนี้มีและใบ issue3 ไม่มีคือบรรทัด claude session
(`0b82f9e8-b25a-4279-b1b9-b2b0ab4db321`) พร้อม path ของไฟล์ jsonl **จึงย้อนกลับไปอ่านบทสนทนาของ agent ตัวนั้นได้**
ส่วนใบ issue3 เขียนว่า "no agent session found in herdr"

### 5.5 ชั้นวาง tombstone

#### ขั้นที่ 1 — ดูชั้นวางของ laris-team

tombstone มีสองชั้นวาง ชั้นใน home อยู่ที่ `~/.herdr/tombstones/<repo>/` ส่วนชั้นของ repo อยู่ที่ `ψ/memory/tombstones/`
ลอง `ls` ดูแค่ 12 ชื่อท้ายสุดของ laris-team

```bash
ls ~/.herdr/tombstones/laris-team | tail -12
```

![รายชื่อไฟล์ใน ~/.herdr/tombstones/laris-team เรียงตามวันที่](images/45-tombstones-dir.png)

ชื่อไฟล์ขึ้นต้นด้วยวันที่ จึงเรียงตามเวลาอยู่ในตัว มีใบของ 2026-11-03 สี่ใบอยู่ใกล้กัน รวมถึง
demo-hello-world ที่อ่านไปเมื่อกี้ และ white-fan-surge ซึ่งเป็น worktree ที่ถูกถอดตอน 21:37
**บนชั้นเดียวกันยังมีของที่ไม่ใช่ tombstone ปนอยู่** เช่น log, สคริปต์ finish-relic-timetravel.sh
และ RETIRED.md

> Tombstone คือร่องรอย หน้าที่ของ worktree จบลง แต่เรื่องราวของมันยังอยู่

สรุปบทนี้ไว้ในประโยคเดียวนั้นพอ ส่วนในบทหน้าจะแกะไส้ในของสองสคริปต์ คือ herdr-sign.sh ที่ตัดสิน
ว่าจะพิมพ์ฟิลด์ไหนตามความเป็นส่วนตัวของ repo และ tombstone.py ที่เพิ่งใช้ไป

## 6. แกะไส้ในสองสคริปต์
สี่บทที่ผ่านมาเราใช้สกิลจากข้างนอก พิมพ์คำสั่งแล้วดูผล บทนี้เปิดฝาดูข้างใน
สองสคริปต์ที่ทำงานหนักที่สุดคือ `herdr-sign.sh` ของ /herdr-pr กับ `tombstone.py`
ของ /herdr-dissolve เราจะอ่านทีละบรรทัดจากชิ้นที่ตัดมาจริง ไม่เดาและไม่เติม
ถ้าอยากเห็นทุกบรรทัดของไฟล์ ให้เปิดภาคผนวก `09-code.md` ซึ่งเก็บโค้ดเต็มทั้งสี่สกิลไว้

### 6.1 herdr-sign.sh ตัดสินจากความเป็น public ว่าจะพิมพ์แค่ไหน

#### ขั้นที่ 1 — อ่านบล็อกที่ถาม GitHub ว่า repo เป็น private ไหม

เปิดไฟล์ช่วงบรรทัด 205 ถึง 222 ด้วย `sed -n`
ช่วงนี้คือจุดที่สคริปต์ตัดสินว่าบล็อกที่ตัวเองกำลังจะพิมพ์ จะเปิดข้อมูลบนเครื่องหรือไม่

```bash
sed -n 205,222p ~/.claude/skills/herdr-pr/herdr-sign.sh
```

![บรรทัด 205 ถึง 222 ของ herdr-sign.sh ตัวแปร visibility และ redact](images/60-sign-visibility.png)

ตัวแปรเริ่มต้นคือ `visibility="unknown"` สคริปต์เรียก
`gh repo view "$work_slug" --json isPrivate --jq .isPrivate`
แล้ว `case` ดูคำตอบ มีสองทางเท่านั้นที่เปลี่ยนค่า คือ `true` ได้ `private`
กับ `false` ได้ `public` ถ้า `gh` ล้ม หรือไม่มี `$work_slug` ค่าก็ค้างที่ `unknown`
**ค่าเริ่มต้นคือปิด ต้องมีหลักฐานว่าเป็น private ถึงจะเปิด** ตรงนี้คอมเมนต์ของสคริปต์เองก็บอกเหตุผลไว้
(เดาว่า private ผิด = เอาโครงเครื่องไปประกาศบนอินเทอร์เน็ต)

#### ขั้นที่ 2 — ดูสองบรรทัดที่ตั้ง redact

อ่านต่อสองบรรทัดท้าย ๆ ของชิ้นเดียวกัน

```
redact=1
[ "$visibility" = "private" ] && redact=0
[ "$force_full" = "1" ] && redact=0
```

`redact=1` ตั้งไว้ก่อนเสมอ แล้วมีแค่สองเงื่อนไขที่ลดเป็น 0
เงื่อนไขแรกคือ visibility เท่ากับ `private` พอดี `unknown` กับ `public` ไม่ผ่าน
เงื่อนไขที่สองคือ `--full` ซึ่งตั้ง `force_full` ให้คนที่รู้ดีกว่าสคริปต์ สั่งทับได้เอง
บทที่ 4 เราเห็นผลของสองบรรทัดนี้มาแล้ว repo นี้ public บล็อกของ pane นี้เลยออกมาแบบ redact

### 6.2 ฟิลด์ที่มีแต่ private repo เท่านั้นที่ได้

#### ขั้นที่ 1 — อ่านว่าฟิลด์ไหนถูกกั้นไว้หลัง redact

ไปที่บรรทัด 266 ถึง 285 ตรงนี้สคริปต์ประกอบสองก้อนข้อความ `sess_private` กับ `herdr_private`
ทั้งสองเริ่มเป็นสตริงว่าง

```bash
sed -n 266,285p ~/.claude/skills/herdr-pr/herdr-sign.sh
```

![บรรทัด 266 ถึง 285 ของ herdr-sign.sh ก้อน sess_private และ herdr_private](images/61-sign-private-fields.png)

พอ `redact` เป็น 0 ก้อนแรกถึงได้ `transcript` กับ `memory` ก้อนที่สองได้ `socket`
(ค่าจาก `HERDR_SOCKET_PATH` หรือค่า default) ถ้า `redact` ยังเป็น 1 สองก้อนนี้ว่างต่อไป
บล็อกสาธารณะเลยไม่มีทั้งสามฟิลด์ **ฟิลด์ที่บอกว่าไฟล์อยู่ที่ไหนในเครื่อง มีเฉพาะบล็อกของ repo ที่พิสูจน์แล้วว่าเป็นส่วนตัว**
สังเกตว่า transcript ถูกแปลง `$HOME` เป็น `~` ก่อนพิมพ์ด้วย

คอมเมนต์ด้านบนของชิ้นนี้ยังเล่าที่มาของโครงสร้างนี้ด้วย
แต่ก่อนมีบล็อก full กับบล็อก public แยกกันสองก้อน บรรทัดที่เติมลง full เงียบ ๆ ไม่เคยไปถึง public
ตอนนี้ทั้งสองบล็อกมาจากแม่แบบเดียว ต่างกันแค่สองตัวแปรนี้ว่างหรือไม่ว่าง
อ่านโค้ดทั้งไฟล์ได้ที่ `09-code.md` ส่วน herdr-pr

### 6.3 tombstone.py หา worktree แล้วปฏิเสธ main checkout

#### ขั้นที่ 1 — อ่านวิธีหา worktree จาก porcelain

ฝั่ง /herdr-dissolve เปิด `tombstone.py` บรรทัด 18 ถึง 40 ซึ่งเป็นต้นของ `main()`

```bash
sed -n 18,40p ~/.claude/skills/herdr-dissolve/tombstone.py
```

![บรรทัด 18 ถึง 40 ของ tombstone.py ลูปอ่าน git worktree list --porcelain](images/62-tombstone-refuse.png)

สคริปต์รับ path ตัวแรกแล้วทำ **`os.path.realpath` ก่อน** เพื่อให้ symlink ไม่หลอกการเทียบ
จากนั้นรัน `git -C path worktree list --porcelain` ผลลัพธ์แยกเป็นก้อนด้วยบรรทัดว่าง
ลูปเก็บแต่ละก้อนเป็น dict โดยตัดบรรทัดที่ช่องว่างแรก ได้ key เช่น `worktree`, `HEAD`, `branch`
แล้วหา `me` คือก้อนที่ realpath ของ `worktree` ตรงกับ path ที่ได้รับ

#### ขั้นที่ 2 — ดูเงื่อนไขปฏิเสธ

บรรทัดที่สำคัญที่สุดของชิ้นนี้คือ

```
    if not me or me is wts[0]:
        print("refusing: not a linked worktree (a main checkout …")
```

`git worktree list` พิมพ์ main checkout เป็นรายการแรกเสมอ สคริปต์เลยใช้ `me is wts[0]` เป็นตัวตัดสิน
ไม่ต้องเดาจากชื่อโฟลเดอร์ และถ้าหา `me` ไม่เจอ (path ไม่ใช่ worktree เลย) ก็ปฏิเสธด้วยข้อความเดียวกัน
**ทั้งสองกรณีออกด้วย `sys.exit(2)` ก่อนจะทำอะไรต่อ** หลังผ่านด่านนี้ถึงอ่าน `main_path`, `main_sha`
ชื่อ repo จาก `basename` และชื่อ branch ที่ตัด `refs/heads/` ออก
ถ้า detached ก็ขึ้น `(detached)` บทที่ 5 เรารันด่านนี้กับ main checkout จริงแล้วเห็นข้อความนี้ออกมา
ส่วน exit 0 ที่เห็นในภาพนั้นเป็นของ wrapper ที่เรียกสคริปต์ ไม่ใช่ค่าที่ `sys.exit(2)` คืนมา

### 6.4 ไม่เขียนทับ ไม่ลบ เขียนเมื่อสั่ง --write เท่านั้น

#### ขั้นที่ 1 — ค้นคำที่เกี่ยวกับการเขียนทั้งไฟล์

ไฟล์ยาวเกินจะอ่านทีละบรรทัดในหน้าเดียว เราเลยใช้ `rg` ดึงเฉพาะบรรทัดที่มีคำว่า
`write`, `exists` หรือ `never`

```bash
rg -n 'write|exists|never' ~/.claude/skills/herdr-dissolve/tombstone.py
```

![ผล rg ในแต่ละบรรทัดของ tombstone.py ที่เกี่ยวกับ write exists never](images/63-tombstone-write.png)

เรียงตามเลขบรรทัดแล้วเห็น **สามจุดที่คุมการเขียน**
บรรทัด 5 ใน docstring บอกว่า `Dry run unless --write. Never overwrites`
บรรทัด 20 กับ 24 เก็บ `write = "--write" in args` แล้วกรอง flag ออกจาก args
บรรทัด 110 มี `while os.path.exists(dest):` ซึ่งหาชื่อไฟล์ใหม่เมื่อชื่อเดิมถูกใช้แล้ว

#### ขั้นที่ 2 — อ่านท้ายไฟล์ที่เขียนจริง

สองบรรทัดสุดท้ายในผลคือหัวใจ

```
118:        open(dest, "x", encoding="utf-8").write(text)
121:        print("dry run - add --write to save it")
```

`if write:` ที่บรรทัด 116 คือประตูเดียว ถ้าไม่ใส่ `--write` สคริปต์พิมพ์ข้อความ dry run แล้วจบ
ถ้าใส่ ก็เปิดไฟล์ด้วยโหมด `"x"` ซึ่ง Python จะล้มทันทีถ้าไฟล์มีอยู่แล้ว
**สองชั้นกันเขียนทับ คือลูป `os.path.exists` หาชื่อใหม่ กับโหมด `"x"` ที่ปฏิเสธไฟล์เดิม**
rg ชุดแรกค้นแค่ `write|exists|never` เลยยังพิสูจน์ไม่ได้ว่าไม่มีคำสั่งลบ ขั้นต่อไปค้นคำพวกนั้นตรง ๆ

#### ขั้นที่ 3 — ค้นหาคำสั่งลบทั้งไฟล์

ค้นคำที่เกี่ยวกับการลบไฟล์ ได้แก่ `remove`, `rmtree`, `unlink`, `os.rm` และ `shutil`

```bash
rg -n 'remove|rmtree|unlink|os\.rm|shutil' \
  ~/.claude/skills/herdr-dissolve/tombstone.py
```

![ผล rg หาคำสั่งลบใน tombstone.py ตรงแค่ docstring กับบรรทัด removed_path](images/67-tombstone-no-remove.png)

มีแค่สามบรรทัดที่ตรง บรรทัด 2 กับ 6 เป็น docstring ที่เขียนว่า `Never removes anything` และบรรทัด 88 เป็นข้อความ `removed_path:` ที่เขียนลงบันทึก **ไม่มีคำสั่งลบจริงสักบรรทัด** สคริปต์นี้ทำหน้าที่จดบันทึก
ส่วนการถอด worktree จริงเป็นงานของสกิลที่เรียกมัน หลังจากแสดงแผนและถามคนก่อน

ตอนนี้เราเห็นทั้งสองสคริปต์ว่าระวังเรื่องเดียวกัน คือถ้าไม่แน่ใจ ให้ทำน้อยที่สุด
บทหน้ารวมสิ่งที่พลาดจริงตลอดงานนี้ พร้อมการ์ดสรุปใบเดียว

## 7. กับดักที่เจอจริง และการ์ดสรุป
บทนี้เริ่มด้วยการ์ดสรุปแผ่นเดียว แล้วไปดูทางที่พลาดกัน ทุกข้อเกิดขึ้นจริง
ที่ 3 พ.ย. ตอนเดโม `demo-hello-world` กับ `bring neo` และที่ 8 พ.ย. ตอนปิด
worktree ของ issue #3 แต่ละข้อเขียนเป็นสามท่อน: เกิดอะไร, สาเหตุ, วิธีแก้

### การ์ดสรุปหนึ่งใบ

#### ขั้นที่ 1 — ดูสี่ skill ในตารางเดียว

เปิดการ์ดนี้เมื่อลืมว่าต้องพิมพ์อะไร แต่ละแถวคือหนึ่ง skill: คำสั่ง, ท่อนที่
มันทำ และเงื่อนไขสำคัญ **ข้อที่ต้องจำที่สุดคือ /herdr-pr ต้องพิมพ์ใน pane ที่ทำงานเอง**
ซึ่งก็คือกับดักข้อแรกของบทนี้

![การ์ดสรุปสี่ skill: wt เปิด, bring ดึงมา, pr เซ็น, dissolve ปิด](images/D3-recipe.png)

ภาพนี้ให้เห็นลำดับ open, bring, sign, close ในหน้าเดียว

#### ขั้นที่ 2 — ที่เหลือถาม herdr --help

เรื่องอื่นนอกสี่ skill เช่น `herdr worktree`, `herdr pane`, `herdr agent`,
`herdr machine` ให้ถาม help ของ herdr เอง **ทุกกลุ่มคำสั่งมี subcommand ของตัวเอง**
และหน้านี้คือแผนที่ของทั้งหมด

พิมพ์ `herdr --help` แล้วบรรทัดแรกที่เห็นคือ:

```
herdr — terminal workspace manager for AI coding agents
```

![หน้า herdr --help แสดง usage คำสั่งหลักและ options](images/00-help.png)

ท้ายหน้ามีบรรทัดบอก agent ว่าถ้างานคือควบคุม pane ให้รัน `herdr --skill`
เพื่อพิมพ์ไฟล์ skill ออกมาอ่าน

### กับดักหกข้อ

#### ขั้นที่ 1 — /herdr-pr พิมพ์ผิด pane

ที่ 3 พ.ย. เวลา 21:33 Nat พิมพ์ `/herdr-pr for demo` ลงใน pane ของงาน
fan check บน white ไม่ใช่ pane ที่ทำเดโม pane นั้นตอบว่า "nothing to sign
yet" **สาเหตุคือ /herdr-pr เซ็นจากสิ่งที่ pane ตัวเองทำ** ใน pane ที่ไม่ได้ทำ
อะไรก็ไม่มีอะไรให้เซ็น

(บันทึก relic5 ของคืนนั้นอยู่ในบทที่ 2 หัวข้อ 2.5)

วิธีแก้คือให้ agent ที่ทำงานเซ็นเอง ซึ่งก็เกิดขึ้นจริง agent ของเดโมโพสต์
ลายเซ็นบน PR #130 ด้วยตัวเอง:

```bash
herdr-sign.sh | gh pr comment 130
```

#### ขั้นที่ 2 — /herdr-rename วิ่งใน worktree ที่สอง

เวลา 21:32 `/herdr-rename` ทำงานใน worktree ที่สอง (งาน fan check บน
white) ไม่ใช่ worktree ของเดโม ชื่อ `worktree/calm-field-2991` เลยกลายเป็น
`white-fan-surge-laris-team-3nov-tue2026` ส่วน branch ของเดโมยังใช้ชื่อเดิม
**สิ่งที่บันทึกบอกได้มีแค่นี้ คือ rename แก้ branch ของ worktree ที่มันรันอยู่**
ถ้าอยากรู้ว่า pane ไหนจะถูกแก้ ให้ดู `git branch --show-current` ใน pane นั้น
ก่อนสั่ง

#### ขั้นที่ 3 — worktree ที่ล็อกและมี PR ยังไม่ merge จะไม่หายไป

หลัง `/herdr-dissolve` ตอน 21:35 worktree ของ fan check ถูกลบตอน 21:37 แต่
worktree ของเดโมยังอยู่ agent ของเดโมรัน dissolve แบบ self mode ซึ่งลบ
worktree ที่ตัวเองรันอยู่ไม่ได้ ขั้นสุดท้ายเลยเป็นของ pane host และ pane host
หยุดที่ **สองข้อ คือ PR ยังไม่ merge กับ worktree ถูกล็อกโดยตั้งใจ**

วิธีแก้คือ merge ก่อนแล้วค่อยปิด ตอน 22:01 Nat สั่ง "merge PR #130 and
dissolve it" 22:05 merge เป็น `04b87c5` issue #129 ปิด เขียน tombstone แล้ว
และลบ space wFA ออก นับจากเปิด issue ถึง merge ใช้เวลา 35 นาที

```bash
gh pr view 130 --repo laris-co/laris-team \
  --json number,mergedAt,mergeCommit,headRefName
```

![gh pr view 130 แสดง mergedAt 2026-11-03T15:04:27Z และ merge commit 04b87c5](images/70-pr-130-merged.png)

#### ขั้นที่ 4 — bring ไม่เจอ repo path

เวลา 22:06:40 และ 22:09:59 Nat พิมพ์ `/herdr-bring bring neo` สองรอบ agent
ตอบว่า `maw locate neo` ไม่คืน repo path และ Neo มีหลาย body อยู่แล้ว มัน
เลยไม่เดา แต่ถามกลับ 3 ข้อให้ Nat เลือก **สาเหตุคือ handle เดียวชี้ได้หลาย body**
วิธีแก้คือให้คนเลือก ส่วนวันนี้ (8 พ.ย.) `maw locate neo` คืน path ได้
แล้ว เรื่อง bring นี้เกิดคืนเดียวกับเดโม แต่ไม่ได้อยู่ในสายงานของ issue #129

#### ขั้นที่ 5 — herdr-unpromote หยุดบน space ที่มี linked worktree

หลัง Nat เลือกข้อ 1 (รวม session `neo` ของ m5 เข้า laris-co ด้วย
`herdr-unpromote --session neo --to laris-co`) tool นี้ปิด neo-oracle main
ไม่ได้ **สาเหตุคือ space นี้มี linked worktree space ผูกอยู่** มันเลยหยุดที่นั่น

(บันทึก relic5 ของเรื่องนี้อยู่ในบทที่ 3)

agent แก้ด้วยมือ ด้วยการ resume neo-oracle main (`08f33511`) กับ
builder-neo (`840b12d9`) ทีละตัว ต่อมา `/herdr-promote neo back session`
ย้าย Neo กลับออกมา ตอนนั้น herdr-move ติดข้อจำกัดเดิมอีกรอบที่ neo main
agent จึงปิด space ด้วย `--group` ข้อนี้บอกว่า skill ที่หยุดแล้วบอกเหตุผล
ดีกว่าที่ลบของที่ยังมีของผูกอยู่

#### ขั้นที่ 6 — โฟลเดอร์ที่ถูก ignore หนัก 61 MB ใน worktree

ตอนปิด worktree `workshop-for-ai-aiexpo-issue3-30oct-fri2026` ที่ 8 พ.ย. มี
สองอย่างที่ git ไม่เห็น ไฟล์ untracked คือ deck-shots (PNG 17 ไฟล์กับ
`deck_report.json`) และโฟลเดอร์ `books/dist` ที่ถูก ignore หนัก 61 MB
**สาเหตุคือ `git status` ไม่แสดงของที่ ignore** ลบ worktree แล้วของพวกนี้หายเงียบ ๆ

วิธีแก้คือเก็บก่อนลบ deck-shots ถูกคัดลอกไป main ส่วน `books/dist` ถูก tar
ไว้ ไฟล์ tarball ขนาด 55M:

```bash
ls -lh ~/.herdr/tombstones/aiexpo-oracle/
```

![ls -lh แสดง 2026-11-08_wt-issue3_books-dist.tgz ขนาด 55M](images/71-issue3-dist-tgz.png)

worktree นี้ถูก herdr ล็อกไว้ agent ของ main checkout จึงปลดล็อกแล้ว
ลบจากข้างนอก จากนั้นปิด pane ขวา wCM:p2 ส่วน branch เก็บไว้
### ต่อไป

บทต่อไปคือภาคผนวก โค้ดเต็มของสคริปต์ทั้งหมดที่เล่มนี้พูดถึง พิมพ์ครบทุก
บรรทัดตามต้นฉบับ ไว้ให้เปิดเทียบกับที่อ่านมา

## ภาพปก และวิธีทำเล่มนี้

ภาพปก `images/cover-art.jpg` เป็นภาพที่ AI วาด (AI-generated, Codex `codex exec`) ไม่ใช่ภาพถ่ายและไม่ใช่ capture ภาพอื่นทั้งหมดเรนเดอร์จากข้อความใน `captures/` และ `diagrams/` เล่มทำตาม /oracle-write-proof-book กับ /app-guide-book: capture.sh รันทุกคำสั่งจริง, cards.py แปลงเป็นภาพ, เขียนบทพร้อมกันจาก BRIEF.md + OUTLINE.md, ตรวจด้วย verify.py และตรวจข้ออ้างอีกรอบ, แล้ว `make pdf` + `make check`

— AIExpo Oracle (Oracle AI)
