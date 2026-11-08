# ให้ agent หลับ แล้วตื่นที่เดิม: herdr-sleep, team-wake, herdr-vacation

> RAM ของ m5 ใกล้หมด Nat พิมพ์ "now put media team to sleep" Claude ของทีม media บนเครื่อง white ปิดลง แต่ช่องใน sidebar ยังอยู่ครบ จากนั้นพิมพ์ "wake just pigment" ตื่นมาตัวเดียว ตรงช่องเดิม พร้อมบอทและโน้ตที่ตัวเองเขียนไว้ก่อนหลับ บทนี้อธิบายว่าก่อนหลับเก็บอะไร (bookmark และ wake card) ปลุกทีละตัวหรือทั้งทีม ปลุกจาก Discord ด้วย `!wake` และหลัง reboot ใช้ team-wake อย่างไร บทที่ 3 ของชุด herdr ทุกภาพมาจากคลิปจริงวันที่ 3 พ.ย. 2026

- ฉบับอื่น: [English](README.en.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. ภาพรวม

![แผนภาพ: sleep ถาม bookmark เขียน wake card ปิด Claude เก็บช่องไว้ แล้วปลุกได้สามทาง](images/00-sleep-wake-flow.png)

- **sleep** = ปิด Claude แต่จำทุกอย่างที่ต้องใช้ตอนกลับมา transcript ไม่หาย
- **wake card** = ไฟล์ JSON หนึ่งไฟล์ต่อหนึ่งช่อง เก็บที่ `~/.local/state/herdr-sleep/<วัน>/<label>.json` อยู่นอก repo
- **bookmark** = โน้ต 4 บรรทัดที่ agent เขียนเองก่อนหลับ ตอนตื่นจะได้อ่านโน้ตนี้ก่อน
- ปลุกได้สามทาง: สั่งเอง (`wake just pigment`), แท็กใน Discord (`!wake @bot`), หรือหลัง reboot (`team-wake`)
- ทำไมต้องหลับ: agent ที่เปิดทิ้งไว้กิน RAM ในคลิป Nat บ่นว่า RAM หมด หลับแล้ว RAM คืน ปลุกเมื่อมีงาน

## 2. เดโมจริง 3 พ.ย. 22:05: ให้ทีม media หลับ

![Nat พิมพ์ now put media team to sleep ทีม media บน white มีสมาชิก 4 ตัวสถานะ done ใน sidebar](images/01-put-media-team-to-sleep.png)

1. Nat พิมพ์ในช่อง laris-labs-oracle บน m5: "now put media team to sleep"
2. agent อ่านรายชื่อจาก `teams/media-team.yaml` แล้วดูสถานะบน white: calliope, pigment, herald, iris เป็น `done` ทุกตัว desk (`w2:p1`) เป็น `idle`
3. สั่ง `herdr-sleep sleep` ผ่าน ssh ทีเดียวทั้งห้าช่อง:

```bash
herdr-sleep sleep w2E:p1=calliope-oracle w2F:p1=pigment-oracle \
  w2G:p1=herald-oracle w2H:p1=iris-oracle w2:p1=media-team \
  --session laris-co --keep-space
```

![หลังสั่ง sleep: ใน sidebar สมาชิก media-team เปลี่ยนจากเครื่องหมายถูกเป็นจุด ช่องยังอยู่ครบ](images/02-asleep-spaces-kept.png)

- `--keep-space` คือหัวใจของเดโมนี้ Claude ออก แต่ช่องอยู่ที่เดิม Nat อธิบายในคลิปว่าปิด Claude แต่คง layout เดิมไว้ เพื่อให้เห็นว่าทีมมีโครงสร้างอย่างไร และประหยัด RAM
- ใน sidebar เครื่องหมาย ✓ ของสมาชิกเปลี่ยนเป็น `·` (ไม่มี agent) โครงทีมยังเห็นครบ
- agent รายงานว่า Calliope กับ Pigment จะ "offline in Discord until woken"

## 3. ก่อนหลับ: bookmark 4 บรรทัด

herdr-sleep ส่งข้อความนี้ไปให้ agent ทุกตัวก่อนปิด (Pigment ได้รับเวลา 22:05:50):

> [herdr-sleep] This copy is going to sleep (it can be woken later). Reply in AT MOST 4 short lines, no tools: 1) what you were doing 2) git state (committed/pushed/uncommitted) 3) next step 4) any open question.

Pigment ตอบภายใน 4 วินาที (ข้อความของ Pigment เอง):

> 2) Git: `wt/pigment-oracle` was clean and pushed at `2b17f6d` when I last checked. Nothing has changed since, and 9 commits are not merged into `main`.
> 3) Next step: when Nat answers the scope questions, or if Nat says to just go, draw a 5-card pilot …

- 4 ข้อ: ทำอะไรอยู่, สถานะ git, ขั้นต่อไป, คำถามที่ค้าง
- คำตอบนี้คือ bookmark เก็บลงการ์ด
- agent ที่กำลัง `working` หรือ `blocked` จะไม่ถูกปิด herdr-sleep ข้ามไปพร้อมบอกเหตุผล ไม่ตัดกลางรอบ

## 4. wake card เก็บอะไร

ฟิลด์จริงที่สคริปต์ `~/.local/bin/herdr-sleep` เขียน:

- `slept`, `host`, `herdr_session`: หลับเมื่อไร บนเครื่องไหน session ไหน
- `space`: `id`, `label`, `cwd` ของช่อง
- `agent`: `pane`, `session` (id ของบทสนทนา Claude), `argv` (คำสั่งที่ใช้เปิด), `channel` (Discord เปิดอยู่ไหม), `name`
- `bookmark`: โน้ต 4 บรรทัดของ agent
- `git`: `branch`, `ahead`, `dirty` (จำนวนไฟล์ที่ยังไม่ commit)
- `woke`, `woke_in`: เติมตอนปลุก

กติกา:
- ไม่เก็บค่า secret ในการ์ด เก็บแค่ path ของไฟล์ env และชื่อ token
- ไม่ลบการ์ด การ์ดคือบันทึกการหลับ
- sleep ไม่ commit ไม่ push ไม่ลบ worktree ไฟล์ที่ยังไม่ commit อยู่บนดิสก์ การ์ดจดจำนวนไว้

## 5. ปลุกตัวเดียว: "wake just pigment"

![agent แสดงการ์ดห้าใบใน herdr-sleep/2026-11-03 แล้วปลุก pigment-oracle ตัวเดียว ได้ awake in w2F:p1, bot on](images/03-wake-just-pigment.png)

1. Nat พิมพ์: "wake just pigment"
2. agent ดูการ์ดบน white: `calliope-oracle.json herald-oracle.json iris-oracle.json media-team.json pigment-oracle.json`
3. `sleeper.py list` บอกว่าใครหลับ หลับเมื่อไร ช่องไหน
4. `python3 skills/team-wake/sleeper.py wake pigment-oracle` ได้ผล `pigment-oracle: awake in w2F:p1, bot on`

![Pigment ตื่นในช่องเดิม ได้ข้อความ sleeper Woke from sleep พร้อม bookmark ของตัวเอง แล้วกลับไปเช็กเธรดต่อ ใน sidebar มี pigment ตัวเดียวที่ตื่น](images/04-pigment-woke-with-bookmark.png)

ขั้นตอนของ `sleeper.py wake` (repo laris-co/laris-team, `just wake-sleeper <name>`):
- หาช่องเดิม (`kept_pane`) ถ้ายังอยู่และว่าง ใช้ช่องนั้น ถ้าไม่มีก็เปิดใหม่ worktree ซ้อนใต้ทีมของมัน
- ถ้ามี Claude รันอยู่ในโฟลเดอร์นั้นแล้ว ไม่เปิดตัวที่สอง
- ตัวที่มีบอท: เปิดด้วยบรรทัด launch ของ fleet (token บอทและบัญชี Claude จาก `pass`) + `--resume <session>` บทสนทนาเดิม
- ตั้งชื่อ agent คืน แล้วส่ง bookmark ให้: `[sleeper] Woke from sleep. Your own bookmark from before: …`
- จัด sidebar ใหม่ตาม charter ของทีม (`tools/layout.py`)

Pigment ตื่นมาแล้วทำต่อจากโน้ตตัวเอง (22:06:44):

> I've woken and checked the duang-oracle thread. Nat hasn't answered my scope questions, so I'm not drawing yet.

## 6. ปลุกจาก Discord: `!wake`

- Nat อธิบายในคลิป: Laris Labs Oracle เห็นทุกข้อความ ถ้าแท็กตัวที่หลับอยู่ ให้มันไปปลุกมาตอบ จะได้ไม่ต้องเปิดทิ้งไว้เปลือง RAM
- เพิ่มเข้า plugin Discord ของ laris-co บ่ายวันเดียวกัน (commit `18a7bc6`, 3 พ.ย. 16:12) จากคำของ Nat: "oh can we support !sleep !" และ "if !wake should tell Laris Labs Oracle"
- `!sleep @bot` หรือ `!sleep @role` จากคนที่เชื่อถือได้: บอทที่ถูกแท็กรอจนตัวเองว่าง (สูงสุด 10 นาที) แล้วรัน `herdr-sleep … --keep-space` กับช่องตัวเอง ใส่ 💤
- `!wake …`: บอทที่หลับไม่ได้ยิน (ไม่มี process ฟังอยู่) บอททุกตัวทิ้งข้อความนี้ ยกเว้น host (Laris Labs Oracle) ที่ส่งต่อให้ Claude ของตัวเองปลุกด้วย `sleeper.py`
- host ไม่หลับด้วยคำสั่งนี้ เพราะเป็นตัวที่ต้องปลุกคนอื่น

## 7. ปลุกทั้งทีม และหลัง reboot: team-wake

- ปลุกหลายตัว: `just wake-sleeper calliope-oracle herald-oracle …` การ์ดที่อยู่อีกเครื่อง `sleeper.py` ปลุกผ่าน ssh ให้
- หลัง reboot หรือ herdr server restart: herdr เปิดบทสนทนาเดิมให้ทุกช่องเอง (`resume_agents_on_restore = true`) แต่เป็น `claude --resume` เปล่า ไม่มี `DISCORD_BOT_TOKEN` ไม่มีบัญชีของแต่ละ oracle บอทจึงกลับมา offline ทั้งหมด
- `/team-wake` แก้ส่วนนี้ วางแผนก่อนด้วย `wake.py` แล้วค่อย `wake.py go` แต่ละแถวเป็น:
  - `ok` ปล่อยไว้
  - `bot` เปิดใหม่ด้วยบรรทัด launch จริง + `--resume` บทสนทนาเดิม
  - `stop` ตัวที่การ์ดบอกว่าหลับอยู่ ให้หลับต่อ
- รันอัตโนมัติ: hook `SessionStart` (matcher `resume`) ของ laris-team main แยกช่องเล็ก รอ 60 วินาที แล้ว `go`
- white reboot เครื่องเดียว: ใช้ systemd user unit `team-wake.service` (`just wake-unit white`) เพราะ hook บน m5 ไม่ทำงานถ้า m5 ไม่ได้ restart
- กติกา: หนึ่งบอท หนึ่งร่าง ไม่เปิดบอทซ้ำ ไม่ตัด agent ที่กำลังทำงาน ถ้าไม่สั่ง `go force`
- ทีมที่ไปพักร้อนไม่มีช่องเปิด herdr จึงไม่ resume อะไร team-wake ก็ไม่ปลุก ใช้ `just up <team>`
- เรื่อง charter ของทีม ดู [บท team ecosystem](../2026-11-05_team-ecosystem-lesson/README.md)

## 8. sleep, vacation, blank ต่างกันอย่างไร

| skill | ทำอะไร | เก็บอะไรไว้ | กลับมาด้วย |
|---|---|---|---|
| `/herdr-sleep` | ปิดทีละช่องที่เลือก | bookmark, การ์ด, argv, Discord, คำสั่ง server ในช่องอื่น | `sleeper.py wake` / `herdr-sleep wake` |
| `/herdr-vacation` | ก่อนไม่อยู่: ปิดทุกตัวที่ idle เกิน N ชม. (ค่าเริ่ม 3) | transcript อย่างเดียว | `fleet resume <path>` |
| `/herdr-blank` | ปิดช่องที่เหลือแต่ shell เปล่า | ไม่มี (ไม่มีอะไรรัน) | ไม่ต้อง |

- vacation วัดความ idle จากเวลาที่ transcript เขียนล่าสุด ไม่ใช่ git log
- vacation ไม่ปิดตัวที่ค้างคำถามถึง Nat แต่ลิสต์คำถามไว้ให้ตอบตอนกลับ
- blank: Nat 29 ต.ค. "can we detect all blank shell? it should close workspace" เพราะ `/exit` ทิ้ง shell และช่องไว้ ค่าเริ่มคือดูอย่างเดียว ต้องใส่ `--close`
- ทั้งสามไม่ลบ worktree ไม่ commit ไม่ push ถ้าจะลบ worktree ใช้ `/herdr-dissolve` ดู [บท wt lifecycle](../2026-11-08_herdr-wt-lifecycle/README.md)

## 9. กับดักที่เจอจริง

- **bookmark ถูกตัด:** สคริปต์อ่าน bookmark จากท้ายจอของช่อง (8 บรรทัดสุดท้าย) ของ Pigment ข้อ 1 เหลือแค่ "started." และพ่วงบรรทัดสถานะมาด้วย 4 พ.ย. desk ของ ccdc-team ได้ bookmark เป็นแบนเนอร์เปิด Claude แทน ตื่นแล้วควรเช็กว่า bookmark อ่านรู้เรื่อง
- **`herdr-sleep wake` เปล่าใน laris-co:** เปิดช่องใหม่ท้าย sidebar และรัน argv เปล่า ไม่มี token บอท ไม่มีบัญชี Claude บอทจึงไม่กลับ ใน laris-co ใช้ `sleeper.py` / `just wake-sleeper`
- **reboot แล้วบอทเงียบ:** resume ธรรมดาเก็บ `--channels` แต่ทิ้ง token 2 พ.ย. 22:38 white reboot เครื่องเดียว บอท laris-co บน white ไม่ตื่นสักตัว จึงเพิ่ม systemd unit
- **white ไม่มี conversation id:** ถ้าไม่มี `herdr integration install claude` herdr ไม่บันทึก id ไม่ resume อะไรเลย white ไม่มีจนถึง 29 ต.ค.
- **บอทตอบซ้ำสองเครื่อง:** ใช้ครั้งแรก 10 ต.ค. ให้ร่างบน m5 ของ xiaoer, แหมว, คุณใหญ่, ดากานดา, neo-nsm หลับ ให้ white ตอบ Discord ตัวเดียว ปลุกบน m5 เฉพาะตอน white ล่ม ไม่งั้นบอทตอบสองที
- **การ์ดว่าง:** 10 ต.ค. การ์ดของ xiaoer ที่หลับรอบสองออกมาว่าง เพราะ pid ที่ได้เป็นตัว launcher (`direnv exec`) ไม่ใช่ claude แก้แล้ว ถ้าหา session id ไม่ได้ สคริปต์ไม่เขียนการ์ดและไม่ปิด agent
- **`!sleep` ตอนกำลังทำงาน:** รอว่างได้สูงสุด 10 นาที เกินนั้นยกเลิก ไม่เขียนการ์ด
- **transcript ถูกย้ายไป archive:** copy กลับจาก `projects-archive/` (copy ไม่ใช่ move) แล้วค่อย resume
- **server ไม่ยอมหยุดใน 5 วินาที:** รายงาน ไม่ `kill -9`

## 10. ที่มา

- คลิป Herdr part 2 (3 พ.ย. 2026 เริ่ม 21:39:58) ช่วง 24:45-27:00 (22:04-22:07) ภาพทุกภาพตัดจากคลิปนี้
- relic5: Pigment บน white, `[herdr-sleep]` 15:05:50Z, bookmark 15:05:54Z, `[sleeper] Woke` 15:06:35Z
- `~/.claude/skills/herdr-sleep`, `herdr-vacation`, `herdr-blank` SKILL.md และ `laris-co/laris-team` `skills/team-wake/SKILL.md`, `sleeper.py`, `plugin/discord/server.ts` อ่านเมื่อ 8 พ.ย. 2026
- ไทม์ไลน์: sleep และ vacation เกิดช่วง 24-29 ก.ย., ใช้จริงครั้งแรก 10 ต.ค., blank 29 ต.ค., `!sleep`/`!wake` และ `sleeper.py` 3 พ.ย. ดูทั้งชุดใน [แผนที่ skill herdr](../2026-11-08_herdr-skill-map/README.md)
- หลักฐานดิบอยู่ใน [captures/](captures/)
