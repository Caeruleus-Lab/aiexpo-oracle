# งานหนึ่งชิ้น ตั้งแต่ต้นจนจบ: /herdr-wt → /herdr-rename → /herdr-pr → /herdr-dissolve

> บทที่ 2 ของชุด herdr งานหนึ่งชิ้นใน herdr มีสี่ขั้น `/herdr-wt` เปิด issue ที่มีบริบทครบ ตัด worktree เปิด space ของมันเอง แล้วสั่ง agent จาก issue นั้น `/herdr-rename` ตั้งชื่อ branch ให้มีความหมาย `/herdr-pr` เซ็นชื่อใน PR ว่าใครทำ จากไหน และคุยกลับได้ทางไหน `/herdr-dissolve` เก็บงานก่อน เขียน tombstone แล้วค่อยปิด worktree บทนี้เดินตามเดโมจริงของ Nat คืนวันที่ 3 พ.ย. 2026 (issue #129, PR #130 ใน laris-co/laris-team) และรอบที่เกิดซ้ำใน repo นี้เมื่อ 8 พ.ย.

- ฉบับอื่น: [English](README.en.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. ภาพรวม

![ไทม์ไลน์จริงของคืน 3 พ.ย. 2026: /herdr-wt 21:28, PR #130 21:31, /herdr-rename 21:32, /herdr-pr 21:33, /herdr-dissolve 21:35, merge และปิด worktree 22:05](images/00-wt-lifecycle.png)

- งานหนึ่งชิ้น = issue หนึ่งใบ + branch หนึ่งเส้น + worktree หนึ่งโฟลเดอร์ + herdr space หนึ่งอัน + agent หนึ่งตัว
- สี่ skill นี้พางานชิ้นนั้นจากเกิด ไปตั้งอยู่ ไปดับ แต่ละขั้นทิ้งร่องรอยไว้ให้คนอ่านทีหลัง
- เดโมคืนนั้นเป็นงานเล็กจงใจ: สคริปต์ hello world สามบรรทัด ตามที่ issue เขียนไว้ "the point is the workflow, not the code"
- คลิปนี้อยู่ใน "Herdr part 1" ช่วงนาทีที่ 21:00–28:17 จอที่อัดเห็นแค่ browser หน้า terminal ไม่ได้อัด รูปในบทนี้เลยเป็นหน้า GitHub ส่วนลำดับเหตุการณ์ใน terminal มาจาก relic5

## 2. /herdr-wt: issue ก่อน แล้วค่อย worktree

21:28 Nat พิมพ์ `/herdr-wt demo-hello-world` ใน pane หลักของ laris-team (Laris Labs Oracle, pane `wDW:p1`) แค่นั้น ไม่ได้บอกงานอะไรเพิ่ม

skill ทำห้าขั้นตามลำดับ (Nat กำหนด 28 ก.ย. 2026):

1. **เปิด issue ก่อน** เช็คว่า repo นี้เปิด issue ได้และเรามีสิทธิ์เขียน แล้วเขียน issue ที่อ่านจบในตัว: Goal, Context, Deliverables, Rules, Done when, Out of scope
2. **ตัด worktree** ที่ `<repo>/wt/<slug>-<oracle>-issue<N>-<วันที่>` แล้ว lock ไว้
3. **บันทึก workspace ลง issue** เป็น comment: branch, path, space, pane, ชื่อ agent
4. **เปิด agent** ด้วย `herdr pane run "claude"` แล้วตั้งชื่อ agent
5. **สั่งงานจาก issue** prompt สั้น ๆ บอกแค่ว่างานอยู่ issue ไหน รายงานกลับทางไหน

![issue #129 ที่ /herdr-wt เขียน: Goal, Context, Deliverables, Rules, Done when](images/01-issue-129-brief.png)

ผลจริงคืนนั้น:

- issue #129 เกิด 21:29 ท้าย issue เขียนว่า "Opened by Laris Labs Oracle (AI) via /herdr-wt · session 51fdd0de"
- worktree `wt/demo-hello-world-laris-team-issue129-3nov-tue2026` เกิด 21:29:29
- space `wFA`, pane `wFA:p1`, agent ชื่อ `demo-hello-world-laris`
- laris-team ไม่มี `ψ/` เลยไม่มีโฟลเดอร์ lab

![comment Workspace ใน issue #129: branch, path, herdr space wFA, pane wFA:p1, agent demo-hello-world-laris](images/02-issue-129-workspace.png)

**ทำไมต้องมี issue:** skill เขียนไว้ว่า "a prompt typed into a pane lives in that agent's scrollback and dies with it." issue อยู่ถาวร คนอ่านได้ agent ตัวอื่นอ่านได้ และ PR ปิดมันได้ด้วย `Closes #N` เหตุจริงคือ 28 ก.ย. agent สองตัวได้ brief ยาวราว 60 บรรทัดที่อยู่แค่ใน pane แล้วหายไปกับ pane

Nat เล่าในคลิปว่า issue บอกทุกอย่าง ทำงานที่ space ไหน pane ไหน เครื่องไหน session id อะไร agent ชื่ออะไร คนกดเข้าไปอ่านได้

## 3. ทำไมชื่อเป็น slug-oracle-date

ชื่อ `demo-hello-world-laris-team-issue129-3nov-tue2026` มีสี่ท่อน แต่ละท่อนมีเหตุผลที่วัดมาแล้ว

- **slug ขึ้นก่อน** (เปลี่ยน 20 ก.ย. 2026) sidebar ของ herdr จัดกลุ่มตาม repo และตัดชื่อจากขวา ถ้าชื่อ oracle นำหน้า ทุกแถวใต้ `neo-oracle` จะขึ้นต้น `neo-` ซ้ำกับหัวกลุ่ม วัดจาก 38 space ที่ความกว้าง 14 ตัวอักษร: oracle นำหน้าชนกัน 3 คู่ slug นำหน้าชน 0
- **oracle ยังอยู่ในชื่อ** เพราะ branch, PR และ `git worktree list` เป็นรายการแบน ไม่มีหัวกลุ่มบอกว่าของใคร
- **issue ตามหลัง oracle** เขียน `issue129` เต็ม ไม่ใช่ `i129` เพื่อให้อ่านออกโดยไม่ต้องมีคำอธิบาย branch ชี้ไปหา brief ของตัวเองได้เลย
- **วันที่ไว้ท้าย** maw เขียนวันที่หลักเดียวไม่เติมศูนย์ `9sep` จึงเรียงหลัง `10sep` ถ้าวันที่นำหน้า การเรียงจะผิด และวันที่ท้ายทำให้งานเรื่องเดียวกันอยู่ติดกัน
- **วางใน `<repo>/wt/`** herdr ตั้งโฟลเดอร์ worktree ได้ที่เดียวทั้งเครื่อง (`worktrees.directory`) บอก "ข้างใน repo นี้" ไม่ได้ ต้องใช้ `--path`
- **owner คิดจาก main checkout** (`--git-common-dir`) ไม่ใช่ `--show-toplevel` เพราะถ้ารันจากใน worktree จะได้ชื่อ worktree แทน (วัด 8 ต.ค. 2026)

**lock ไม่ใช่ security** เป็นป้าย "อย่าลบฉันอัตโนมัติ" `git worktree prune` จะไม่ทิ้งมัน และ `git worktree remove --force` จะปฏิเสธ

## 4. agent ทำงาน แล้วเปิด PR

21:31 agent ใน `wFA:p1` เปิด PR #130 สองนาทีหลัง issue เกิด

![PR #130 จาก branch demo-hello-world-laris-team-issue129-3nov-tue2026: สองไฟล์ใน demos/hello-world](images/03-pr-130-files.png)

- แตะแค่ `demos/hello-world/` สองไฟล์ ตาม Rules ใน issue
- body ขึ้นต้น `Closes #129` และมีบล็อก "Built by" อยู่แล้ว เพราะ issue สั่งไว้ว่า "signed with `/herdr-pr`"
- agent comment กลับใน issue ว่าเช็คอะไรแล้ว: สคริปต์พิมพ์ `Hello, world from m5`, `shellcheck` ผ่าน และ "not merged; Nat merges"

## 5. /herdr-rename: ชื่อที่บอกว่างานคืออะไร

worktree ที่สร้างจากเมนูคลิกขวาของ herdr ได้ชื่อสุ่ม เช่น `worktree/calm-field-2991` คืนนั้น Nat เปิด worktree ที่สองแบบนี้ สั่ง "investigte fan on white machine" แล้วพิมพ์ `/herdr-rename` ในนั้น

21:32 AI ตอบ: "Renamed `worktree/calm-field-2991` to `white-fan-surge-laris-team-3nov-tue2026`. The sidebar now shows the new name, and the space label was renamed to match."

skill ทำแบบนี้:

1. ดูหลักฐานก่อน: `git log`, `git status`, และเรื่องที่คุยกันจริง ตั้งชื่อตามงานที่เกิดขึ้น ไม่ใช่งานที่ตั้งใจ
2. ร่างสามชื่อ รูปเดียวกับ `/herdr-wt` คือ `<topic>-<owner>[-issue<N>]-<วันที่>`
3. เปลี่ยนชื่อทันทีด้วย `git branch -m` แถวใน sidebar เปลี่ยนตาม session ยังทำงานต่อ ไม่สะดุด
4. ถ้าคนรออยู่ ถามด้วย popup ครั้งเดียว: เก็บชื่อนี้ หรือเลือกอีกสองชื่อ (Nat เล่าในคลิป: ให้มันเสนอชื่อ ใส่วันที่ แล้วถามเราว่าเอาชื่อไหน)
5. ถ้า rename เป็นขั้นหนึ่งใน brief ห้ามมี popup ให้เปลี่ยนแล้วทำงานต่อ บอกชื่อสำรองไว้ในรายงานท้าย (Nat, 9 ต.ค.: "go implement work first then can rename again")

- เปลี่ยนแค่ branch โฟลเดอร์ชื่อเดิม การย้ายโฟลเดอร์จะทำให้ agent ที่รันอยู่หลง cwd
- ป้าย space เปลี่ยนตามด้วย ถ้ายังเป็นชื่ออัตโนมัติ (แอปที่อ่านป้าย space จะได้ชื่อใหม่)
- branch ที่มี PR เปิดอยู่ ห้าม rename โดยไม่ถาม

## 6. /herdr-pr: เซ็นชื่อ พร้อมที่อยู่ให้คุยกลับ

> body ของ PR บอกว่าเปลี่ยนอะไร บล็อก Built by บอกว่าถ้าผิด ต้องไปถามใคร

21:33 agent ของเดโมรัน `herdr-sign.sh claude-opus-5-5 | gh pr comment 130 --body-file -` บล็อกขึ้นใน PR

![บล็อก Built by ใน PR #130: agent, model, worktree, branch, head, session id, herdr address demo-hello-world-laris](images/04-pr-130-built-by.png)

บล็อกมีสี่กลุ่ม เรียงตามคำถามที่คนรีวิวถาม:

- **agent** ใครทำ: oracle, model (`claude-opus-5-5`), runtime (claude, omp หรือ codex)
- **worktree** จาก tree ไหน: cwd, branch, head commit
- **session** เหตุผลอยู่ที่ไหน: session id, ไฟล์ transcript
- **herdr** คุยกลับทางไหน: ชื่อ agent, pane, tab, space

ท้ายบล็อกมีคำสั่งให้ใครก็ได้ ทั้งคนและ AI คุยกับ session นั้นต่อ:

```bash
herdr agent prompt demo-hello-world-laris "question about this PR"
herdr agent read   demo-hello-world-laris
```

- Nat เล่าในคลิปว่า ถ้า AI ทำอะไรเจ๋งมา เราจะสืบได้ว่ามันทำยังไง และ AI อีกตัวมาตรวจงานแล้วยิงคำถามกลับไปที่ session นั้นได้
- **ชื่อ agent คือที่อยู่** ต้องตั้งชื่อก่อนเซ็น pane id อย่าง `wFA:p1` เปลี่ยนได้หลัง herdr restart
- **repo private ได้บล็อกเต็ม** laris-team เป็น private จึงมี path transcript, memory และ socket
- **repo public ตัดของส่วนตัวออก** transcript, memory dir, socket ไม่ขึ้น ถ้าเช็ค visibility ไม่ได้ ถือว่า public ไว้ก่อน

## 7. /herdr-dissolve: เก็บงานก่อน แล้วค่อยปิด

> agent ที่ทำงานเก็บงานของตัวเองและรายงานก่อน แล้วถึงจะลบอะไรได้

21:35 สั่ง dissolve ทั้งสอง worktree skill เดินสี่ขั้น: survey, plan, ask, act

- **save first** agent แต่ละตัว commit, push, เปิด PR ที่เซ็นแล้ว แล้วรายงาน PARENT คือ agent ใน main checkout (`wDW:p1`) ปิดท้ายด้วยบรรทัด `DISSOLVE-READY <pr-url|no-changes>`
- agent ลบ worktree ที่ตัวเองยืนอยู่ไม่ได้ เลยใช้ self mode ฝากขั้นสุดท้ายให้ parent ตัวเดโมเขียนว่า "An agent can't remove the worktree it is running in, so the host pane does that last step."
- **tombstone ก่อนลบ** `tombstone.py` บันทึกว่า worktree นี้คืออะไร เกิดเมื่อไร จบเพราะอะไร ผู้สืบทอดคือ PR ไหน และ session id
- ลบผ่าน `herdr worktree remove` ให้ sidebar กับ git ตรงกัน **branch ยังอยู่**

ผลจริงคืนนั้น:

| worktree | สถานะ | ผล |
|---|---|---|
| `white-fan-surge-…` (ดูพัดลม) | อ่านอย่างเดียว 0 commit | `DISSOLVE-READY no-changes`, tombstone, ลบเมื่อ 21:37 |
| `demo-hello-world-…` | 1 commit, PR ยังไม่ merge, lock อยู่ | เก็บไว้ก่อน |

- host ตอบว่า "The dissolve check stops on two things: the PR isn't merged yet; the worktree is locked on purpose, so it can't be cleaned up by accident."
- 22:01 Nat: "merge PR #130 and dissolve it"
- 22:05 merge เป็น `04b87c5` issue #129 ปิดเอง tombstone เขียนแล้ว space `wFA` ปิด สิ่งที่เหลือ: branch, session `0b82f9e8`, ไฟล์ tombstone
- host สรุป: "That was the whole `/herdr-wt` cycle end to end: issue, worktree, agent, PR, merge, dissolve."

**skill ไม่ merge เอง** PR รอคน merge เสมอ

## 8. เกิดซ้ำใน repo นี้ 8 พ.ย. 2026

วงเดียวกันเกิดซ้ำใน Caeruleus-Lab/aiexpo-oracle (repo นี้ เป็น public)

- worktree `wt/workshop-for-ai-aiexpo-issue3-30oct-fri2026` เกิดจาก issue #3 วันที่ 30 ต.ค.
- งานเปลี่ยนไปเป็นสคริปต์ `rrr_notion.py` branch ถูก rename เป็น `rrr-notion-mirror-aiexpo-07nov-sat2026` โฟลเดอร์ยังชื่อเดิม ตรงกับที่ `/herdr-rename` บอกไว้
- PR #7 merge แล้วเมื่อ 7 พ.ย.
- 8 พ.ย. 09:45 pane ขวาเซ็น PR #7 ด้วย `/herdr-pr` (comment 6716331029) ขึ้นต้นว่า "Signed after merge by the right pane, which wrote `rrr_notion.py` (5de0408). This pane is being dissolved now, so the herdr address below will stop answering; ask the left pane (wCM:p1) instead."
- repo public บล็อกจึงตัดของส่วนตัว: "Agent-private storage — transcript, memory dir, herdr socket — is omitted: this repo is public."
- 09:48 dissolve tombstone อยู่ที่ `ψ/memory/tombstones/2026-11-08_workshop-for-ai-aiexpo-issue3-30oct-fri2026.md` เหตุผลที่จบ: "merged PR #7 (f582893); right pane done." ของที่ยังไม่ commit ถูกย้ายไปก่อน: deck-shots ไป main, `books/dist` บีบเป็น `.tgz` เก็บใน `~/.herdr/tombstones/aiexpo-oracle/`

## 9. skill ที่ทำงานคล้ายกัน

- `/herdr-issue` แปลงงานเป็น issue ใน repo ของ oracle ที่ถูกตัว แล้วตัด worktree ทีละหลายงานข้ามหลาย oracle ได้
- `/herdr-ticket` เริ่มจาก issue ที่**มีอยู่แล้ว** (`/herdr-wt` เป็นคนเขียน issue เอง)
- `/herdr-fib-wt` ตัดหลาย worktree แล้วเปิดเป็น pane ในแท็บนี้ วางแบบเกลียว Fibonacci
- `/herdr-wt-ship` ตารางทุก worktree ของ repo แล้วปิดตัวที่ PR merge แล้ว
- `/herdr-done` เช็คอย่างเดียวว่า session นี้ปิดได้ไหม ไม่ลบอะไร
- `/herdr-finished` จบ session เดียวรวดเดียว: herdr-done, `/rrr`, `/herdr-pr`, แล้วปิด
- `/herdr-trinity` ปิดทุก worktree ของ repo ตามหลัก เกิดขึ้น ตั้งอยู่ ดับไป merge เมื่อ Nat บอก go

รายการ skill ทั้งหมดดูที่ [แผนที่ skill herdr](../2026-11-08_herdr-skill-map/README.md) ส่วนการพา worktree agent มานั่งข้างกันดูที่ [บท herdr-room](../2026-10-31_herdr-room-lesson/README.md)

## 10. กับดักที่เจอจริง

- **space ต้องเป็นของ repo ที่สั่ง** herdr จัดกลุ่ม sidebar ตาม space ไม่ใช่ตาม cwd ของ pane ถ้าโค้ดอยู่อีก repo ต้องใช้สูตร "Under the oracle" พลาดมาแล้วห้าครั้ง (6 ต.ค. ถึง 30 ต.ค.) จนกลายเป็นด่านตรวจใน skill
- **อย่าใช้ `herdr agent start`** มันไม่ผ่าน direnv agent ได้ token ผิดตัว (วัด 17 ก.ย.: ได้ `pb` แทน `dd2`) ใช้ `herdr pane run "claude"`
- **`pane run` อย่างเดียวยังไม่พอ** ใน worktree ใหม่ shell ขึ้นก่อน direnv ได้รับอนุญาต ต้องรันคำสั่งทิ้งหนึ่งคำสั่งก่อน (`echo TOK=…`) แล้วค่อยเปิด claude
- **ชื่อ agent ยาวได้ไม่เกิน 32 ตัว** ตั้งเกิน agent เปิดแต่ไม่มีชื่อ ใช้ `<slug>-<owner>`
- **`--timeout` ของ `wait-output` เป็นมิลลิวินาที** `--timeout 40` คือ 40 ms
- **อย่าย้ายโฟลเดอร์ worktree ที่มี agent รันอยู่** agent จะหลงกลับไป main repo เงียบ ๆ
- **เรียก `/herdr-pr` ใน pane ที่ทำงานนั้น** คืน 3 พ.ย. Nat พิมพ์ "/herdr-pr for demo" ใน pane ดูพัดลม AI ตอบว่า "There's nothing to sign yet. This branch has no commits and no open PR." บล็อกจริงมาจาก pane ของเดโม
- **pane id เก่าหลังย้าย pane** `$HERDR_PANE_ID` ค้างค่าเดิม script ตอนนี้หา pane ที่ถูกเองได้ แต่ถ้าส่ง id ผิดมาตรง ๆ จะ fail
- **✓ ไม่ได้แปลว่างานเสร็จ** ✓ แปลว่าจบเทิร์น agent ที่จบด้วยคำถามกำลังรอคน ห้าม dissolve และห้ามพิมพ์ใส่ pane มัน
- **ไฟล์ที่ยังไม่ commit หายไปกับ worktree** ใน repo public ให้ดูรายการไฟล์ก่อนเปิด PR (24 ก.ย. เคย push log ของ Codex ขึ้น PR public)
- **commit ที่ "ยังไม่ push" อาจเป็นของ main** ถ้า main ในเครื่องนำ origin อยู่ worktree เปล่าจะดูเหมือนมีงานค้าง (วัด 29 ต.ค. ใน repo นี้)

## 11. ที่มา

- skill: `~/.claude/skills/herdr-wt`, `herdr-rename`, `herdr-pr`, `herdr-dissolve` (SKILL.md อ่านเมื่อ 8 พ.ย. 2026) และคำอธิบายของ skill ในหัวข้อ 9
- GitHub: laris-co/laris-team issue #129 และ PR #130 (อ่านแบบ read-only) Caeruleus-Lab/aiexpo-oracle PR #7 comment 6716331029
- tombstone: `~/.herdr/tombstones/laris-team/2026-11-03_demo-hello-world-laris-team-issue129-3nov-tue2026.md` และ `ψ/memory/tombstones/2026-11-08_workshop-for-ai-aiexpo-issue3-30oct-fri2026.md`
- relic5: ข้อความใน session 51fdd0de (host), 0b82f9e8 (เดโม), 59a9b212 (ดูพัดลม) วันที่ 3 พ.ย. 2026
- คลิป "Herdr part 1" (3 พ.ย. 2026 เริ่ม 21:07:28) นาทีที่ 21:00–28:17 รูป 01–04 ตัดจากคลิปนี้
- หลักฐานดิบ: [captures/](captures/)
