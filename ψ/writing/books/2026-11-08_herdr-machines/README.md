# herdr หลายเครื่อง: เพิ่มเครื่อง ย้ายทีมไป white คุยข้ามเครื่อง

> herdr ตัวเดียวเห็นได้หลายเครื่อง sidebar ด้านบนคือ Local (เครื่องที่นั่งอยู่) ด้านล่างคือ machine ที่ save ไว้ เช่น white ที่เป็น Linux ทุกเครื่องต่อกันผ่าน tailscale (ชื่อ `*.ts.net`) เพิ่มเครื่องด้วย `herdr machine add` แล้วสั่งงานด้วย `herdr --machine <label>` โดยไม่ต้องพิมพ์ ssh เอง ข้อดีที่ ssh ให้ไม่ได้คือลากไฟล์หรือวางภาพหน้าจอข้ามเครื่องได้ บทนี้มาจากเดโมจริงของ Nat วันที่ 3 พ.ย. 2026 รวมถึงตอนย้าย ccdc-team จาก m5 ไป white ในคำสั่งเดียว (rc=0, 51 วินาที)

- ฉบับอื่น: [English](README.en.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. ภาพรวม

![แผนภาพ m5 กับ white ต่อกันผ่าน tailscale: m5 save white เป็น machine, white ส่งข้อความกลับด้วย herdr --machine m5-laris-co](images/00-m5-white-tailscale.png)

- **m5** คือ Mac ที่ Nat นั่งทำงาน **white** คือเครื่อง Linux (Ubuntu x86_64) ที่รับงานหนักแทน
- ทั้งคู่อยู่ใน tailnet เดียวกัน เรียกกันด้วยชื่อ MagicDNS เช่น `white.follow-rankine.ts.net`
- herdr บน m5 save white ไว้เป็น **machine** หนึ่งตัว (หนึ่ง machine = หนึ่ง session บนเครื่องนั้น)
- ssh ยังทำงานอยู่ข้างใต้ แต่ไม่มีใครต้องพิมพ์ ("ssh runs underneath; nobody types it" จาก `/herdr-link-talk`)

## 2. Local ข้างบน machine ข้างล่าง

![sidebar ของ herdr บน m5 วันที่ 3 พ.ย.: Local ข้างบนมี laris-team, aiexpo-oracle, ccdc-team ข้างล่างเป็น machine 12 ตัว เช่น black-phd, white-laris-co, gb300 จุดเขียวคือต่อได้](images/01-sidebar-local-and-machines.png)

- ภาพนี้จากคลิป part 2 นาที 27:15 Nat อธิบายว่า "ข้างบนคือ Local ก็คือเครื่องเราเอง ข้างล่างเรียกว่า Machine หรือ Remote"
- แต่ละ machine กด `▸` กางดู space ของเครื่องนั้นได้ ไม่สลับออกจากหน้าที่อยู่
- จุดเขียวข้างชื่อ = ต่ออยู่
- ใช้คีย์บอร์ด: `prefix+w` แล้ว ↑/↓ เลือก Enter ไป (จาก `/herdr-machine-labels`)
- ในคลิป part 1 นาที 07:00-07:45 Nat พิมพ์ `uname -a` ในแต่ละเครื่องให้ดูว่าอันนี้ Mac อันนี้ Linux แล้วยุบ/กางแต่ละเครื่อง ("อันนี้คือกระบวนท่าที่หนึ่ง") ส่วนนี้มีแต่เสียง จอที่อัดไว้เป็นแท็บ draw.io ว่าง ๆ เลยไม่มีภาพ

## 3. เพิ่มเครื่อง

คำสั่งจริงจาก `/herdr-link-talk`:

```bash
# บน m5: save session laris-co ของ white เป็น machine
herdr machine add nat@white.follow-rankine.ts.net --label white-laris-co --remote-session laris-co
herdr --machine white-laris-co agent list
```

- ชื่อ label ตามกฎ Nat ("white first"): เครื่องก่อน session ทีหลัง สคริปต์ `herdr-machine-labels` ตั้งให้เป็น `<host> · <session>`
- อยากเห็นอีก session ของเครื่องเดียวกัน ต้อง add อีก machine (`--machine X --session Y` ถูกปฏิเสธ)
- เครื่องที่ save ไว้บน m5 วันนี้ (8 พ.ย., `herdr machine list`, herdr 0.9.5):

```text
83ef54c5  white-laris-co   nat@white.follow-rankine.ts.net          laris-co   enabled
58f05059  white-nsm        nat@white.follow-rankine.ts.net          nsm        enabled
932c2bd2  gb300            gb300                                    default    enabled
b17ec972  white-arkkra     nat@white.follow-rankine.ts.net          arkkra     enabled
c7cd7887  white-arraxccdc  nat@white.follow-rankine.ts.net          arraxccdc  enabled
be7b3860  arra-arraxccdc   <user>@<another-tailnet>.ts.net arraxccdc enabled
```

- วันที่ 3 พ.ย. sidebar มี 12 เครื่อง วันนี้เหลือ 6 รายการนี้เปลี่ยนได้ อ่านจาก `herdr machine list` ทุกครั้ง อย่าจำเอา
- คำสั่งย่อยอื่น: `status` (เช็กโดยไม่ถามรหัส), `rename`, `remove`, `fold`/`unfold`/`fold-others`

## 4. ทำไม add machine ดีกว่า ssh เข้าไปเปิด herdr

![ซ้าย: herdr บน m5 กาง white-laris-co เห็น media-team, rd-team, manager-team, ccdc-team ขวา: หน้าต่างที่ ssh เข้า white แล้วเปิด herdr เห็นต้นไม้เดียวกันในชื่อ Local](images/02-machine-vs-ssh.png)

- ภาพจาก part 2 นาที 28:26 ซ้ายคือ m5 กาง machine `white-laris-co` ขวาคือ ssh เข้า white แล้วรัน herdr ในนั้น
- สองฝั่งเห็นของเดียวกัน Nat: "มันจะได้ของแบบเดียวกันขึ้นมา"
- ต่างกันตรงไฟล์ ถ้ารัน herdr ใต้ ssh "ผมจะไม่สามารถอัปโหลดไฟล์เข้าไปได้" แต่ถ้า add เป็น machine แล้วทำงานจาก m5 "เราจะส่งไฟล์ข้ามไปได้"
- ใช้จริง: แคปหน้าจอบน Mac แล้ววางลงใน agent ที่อยู่บน white ได้เลย ไม่ต้องส่งผ่าน Discord (part 1 นาที 08:00-08:45)

## 5. คุยข้ามเครื่อง ทั้งไปและกลับ

```bash
herdr --machine white-laris-co agent list
herdr --machine white-laris-co agent prompt <pane> "<ข้อความ>"
herdr --machine white-laris-co pane read <pane> --source recent-unwrapped --lines 40
```

- ขากลับ: บน white save m5 เป็น machine `m5-laris-co` แล้ว agent บน white ตอบด้วย `herdr --machine m5-laris-co agent prompt <pane> "..."`
- ก่อนขากลับใช้ได้ ต้องเช็กว่า user บน white ssh ถึง m5 ได้ (`ssh -o BatchMode=yes ...`) ถ้าเจอ `Permission denied (publickey)` ให้หยุดแล้วถามคน
- `/herdr-link-talk` มีสคริปต์ทำครบ: `herdr-link talk nat@white.follow-rankine.ts.net neo` (dry ก่อน แล้ว `--go`)
- กฎ fleet (Nat, 5 พ.ย.: "ask herdr say in each machine not ssh to do"): จะเปลี่ยนอะไรบนเครื่องอื่น ให้สั่ง agent ที่อยู่บนเครื่องนั้น ssh ใช้แค่ดูอย่างเดียว (status, log)
- เรียก agent ด้วย pane id ไม่ใช่ชื่อ ชื่อ prefix-match กันได้ และ pane id เปลี่ยนทุกครั้งที่ย้ายหรือรีบูต

## 6. ย้ายทั้งทีมไป white

เดโมจริง part 1 นาที 19:45-21:00 (21:27 เวลาไทย) Nat เหตุผล: ถ้า m5 ค้างคือความเสี่ยง ให้ทีมไปอยู่ white ประหยัด RAM ฝั่ง Mac

1. 14:27Z Nat พิมพ์ถึง LarisCo (ตัวคุมทีม): "send ccdc-team to white machine"
2. LarisCo รัน `just team-move ccdc white --go --merge` ใน pane ข้าง ๆ
3. สคริปต์เปิด PR #128 (`machine: white` ใน config ของสมาชิก) แล้ว merge เอง
4. ทีละคน: ปิดที่ m5 รอให้ process หายจริง ก๊อปบทสนทนาไป แล้วเปิดใหม่บน white ด้วยบทสนทนาเดิมและ bot ตัวเดิม
5. pane ส่งผลกลับมาเอง:

```text
PANE wDW:p1Y team-move ccdc white rc=0
team ccdc (laris-co/ccdc-team) -> white · session laris-co · desk ccdc-oracle stays
  plan floodboy-oracle: m5 -> white · wF7:p1 wF7 ad9a92c6 done
  plan dustboy-oracle: m5 -> white · wF8:p1 wF8 f7c606e0 done
  plan fireman-oracle: m5 -> white · wF9:p1 wF9 de5c0c13 done
PR https://github.com/laris-co/laris-team/pull/128
merged
...
just team-move ccdc white --go --merge  ... 50.940 total
```

- ผล: สมาชิก 3 ตัวอยู่บน white (`w2B`, `w2C`, `w2D` ซ้อนใต้ space ของทีม) bot on ทุกตัว ตัว desk `ccdc-oracle` อยู่ m5 ต่อ
- ภาพใน §4 (ซ้าย ล่างสุด) คือ `ccdc-team` บน white ที่มี `wt/floodboy-oracle`, `wt/dustboy-oracle` หลังย้าย
- ขากลับก็คำสั่งเดียว: `just team-move ccdc m5 --go --merge`
- skill ที่ทำเรื่องเดียวกันจาก charter: `/team-ship <team> dry|go` (Nat, 2 พ.ย.: "make go support white? make skill! for me") เริ่มด้วย `dry` เสมอ
- เปิด/ปิดทั้งทีมบนเครื่องไหนก็ได้: `/herdr-team-ctl start|stop|status <team> --machine <label>`
- ทีมที่ย้ายแล้ว พักให้หลับได้ ดูบท [herdr sleep/wake](../2026-11-08_herdr-sleep-wake/)

## 7. ดูทุกเครื่องในทีเดียว

- `/herdr-link-check` อ่านอย่างเดียว: session ที่รันอยู่, machine ที่ต่อได้, agent ในแต่ละเครื่อง (`herdr-link check`)
- `/herdr-twin`: session นี้รันอยู่ที่ไหนบ้าง เช่น `nsm · 2 places · ● m5 ◐ 3 · ● white ✓ 6`
- sidebar รก: บน m5 เปิด `fold_machines_by_session = true` ไว้ หน้าต่างแต่ละ session กางเฉพาะเครื่องที่ session ชื่อเดียวกัน ที่เหลือยุบ หรือสั่งเอง `herdr machine fold-others --same-session`
- ยุบ (fold) ไม่ตัดการเชื่อมต่อ ส่วน `disable` ซ่อนเครื่องนั้นในทุกหน้าต่างของ m5

## 8. skill ในชุดนี้

- `/herdr-link`: สารบัญของชุด เลือกว่าจะใช้ตัวไหน
- `/herdr-link-local`: ย้าย oracle ไป session ของตัวเองบนเครื่องเดียวกัน
- `/herdr-link-remote`: ตั้ง worker oracle บนเครื่องอื่นให้รอดรีบูต (worktree, `.envrc`, systemd user unit)
- `/herdr-link-talk`: add machine ทั้งสองทาง ทดสอบไปกลับ
- `/herdr-link-check`: ดูทุกอย่าง ไม่แก้อะไร
- `/herdr-link-teardown`: ถอด worker ออกให้เครื่องกลับเหมือนเดิม
- `/herdr-machine-labels`, `/herdr-twin`: ตั้งชื่อและจัด sidebar
- `/team-ship`, `/herdr-team-ctl`: ย้ายทีม เปิด/ปิดทีม
- กฎห้าข้อของชุด: หนึ่งวิญญาณหนึ่งร่าง (เครื่องที่สองได้ชื่อใหม่ เช่น `neo-white`), Discord อยู่ร่างเดียว, หนึ่ง worker ต่อหนึ่ง worktree, คุยผ่าน herdr, backup ก่อนแก้
- ส่งข้อความหลายเครื่องพร้อมกันด้วยปุ่ม ดูบท [⌘J ⌘L](../2026-11-05_herdr-cmd-j-lesson/) รวม agent เป็นห้องดูบท [herdr room](../2026-10-31_herdr-room-lesson/) ภาพรวมทุก skill ดู [แผนที่ skill](../2026-11-08_herdr-skill-map/)

## 9. กับดักที่เจอจริง

- **ย้ายครั้งแรกพังกลางทาง** (3 พ.ย. ก่อนเดโม): ขั้น "end agent" ทุกตัวขึ้น Python syntax error เพราะ quote ซ้อนกันข้าม ssh ไม่มีใครย้ายจริง แก้โดยส่งผ่านไฟล์ `tools/agent-quit.py` และหาสมาชิกจากเครื่องที่มันรันอยู่จริง ไม่ใช่จาก config
- **pane id เปลี่ยน**: สมาชิก ccdc เคยเป็น `wF1`-`wF3` ตอนย้ายเป็น `wF7`-`wF9` สคริปต์ต้องหาใหม่ทุกครั้ง
- **bot ขึ้นมาโดยไม่มี Discord**: config ยังเป็น `machine: m5` ต้อง merge PR `machine: white` ก่อน (`dry` เตือน)
- **`--machine` ใช้คู่กับ `--session` ไม่ได้**: add machine ใหม่สำหรับอีก session
- **`unknown machine 'efe95d03'`**: ใช้ id เต็มหรือ label
- **รายชื่อ machine บน m5 มีชุดเดียวทุก session**: `disable` เครื่องหนึ่ง หายจากทุกหน้าต่าง ใช้ `fold` แทน
- **`herdr --remote` แค่เปิดจอ** สั่ง `agent list`/`agent prompt` ไม่ได้ ต้อง save เป็น machine
- **agent กดลูกศรใน sidebar เองไม่ได้**: บอกคน หรือใช้ `prefix+w`
- **ssh เข้าเครื่องแล้วไม่มี `~/.local/bin`**: ใส่ `PATH=$HOME/.local/bin:$PATH` ก่อน
- **ชื่อเครื่อง**: ในคลิป Nat พิมพ์ `ssh white.local` และสคริปต์ team-ship ยังเขียน `white.local` อยู่ กฎ fleet ตอนนี้ใช้ tailscale ทางเดียว ให้ใช้ `white.follow-rankine.ts.net`

## 10. ที่มา

- คลิป Herdr part 1 (3 พ.ย. 2026, 21:07): นาที 07:00-08:45 (machine, `uname -a`, ส่งไฟล์) และ 19:45-21:00 (ย้าย ccdc-team) มีแต่เสียง ภาพจอเป็น draw.io
- คลิป Herdr part 2 (21:39): นาที 27:00-28:45 ภาพ §2 และ §4 มาจากช่วงนี้ (ตัดส่วนที่มีอีเมลและที่อยู่ LAN ออก)
- relic5 session `51fdd0de` (LarisCo, laris-team) 14:01Z-14:28Z: แผน ผล rc=0 และ PR #126/#127/#128 ([captures/relic5-team-move-2026-11-03.txt](captures/relic5-team-move-2026-11-03.txt))
- SKILL.md ของ `herdr-link`, `herdr-link-local`, `herdr-link-remote`, `herdr-link-talk`, `herdr-link-teardown`, `herdr-link-check`, `herdr-machine-labels`, `herdr-twin`, `team-ship`, `herdr-team-ctl` (ชุด herdr-link สร้าง 11 ต.ค. 2026)
- `herdr machine list` และ `herdr machine --help` บน m5 วันที่ 8 พ.ย. 2026 (herdr 0.9.5)
- กฎ fleet: tailscale เป็นเครือข่ายเดียว, ทำงานบนเครื่องอื่นผ่าน agent ของเครื่องนั้น ssh แค่ดู
