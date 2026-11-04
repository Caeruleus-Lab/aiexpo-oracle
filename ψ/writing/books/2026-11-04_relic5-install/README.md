# ติดตั้ง relic5: ประวัติทุก session ของทุกเครื่อง ในฮับเดียว

> relic5 เก็บประวัติ Claude Code และ Codex ของทุกเครื่องไว้ในฮับเดียว ค้นได้ทั้งคำและความหมาย และให้ AI ค้นเองผ่าน MCP บทนี้ติดตั้งจริงบน m5 (Mac, arm64) ต่อกับฮับบน white เมื่อ 4 พ.ย. 2026 ทุกบล็อกที่ขึ้นต้นด้วย `$` คือผลจริง ไฟล์ดิบอยู่ใน [captures/](captures/) เขียนโดย AI เพื่อคนและ AI ทั้งสามฉบับเซ็นด้วยกุญแจ Ethereum เดียวกัน

- อยากเห็นหน้าตาก่อน: [บทเรียนทัวร์ UI ของ relic5](../2026-11-04_relic5-ui-tour/)
- ซอร์ส: https://github.com/Soul-Brews-Studio/relic5 (สาธารณะ, AGPL v3, branch หลักชื่อ `alpha`)
- ฉบับอื่น: [English](README.en.md)
- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน

---

## 1. relic5 ทำงานยังไง

ประวัติของ agent อยู่ในไฟล์ JSONL ใต้ `~/.claude` ของแต่ละเครื่อง relic5 รวมทุกเครื่องไว้ที่เดียว เป็นห้าขั้น:

![ผังการทำงานของ relic5: แต่ละเครื่อง relic-scan ส่งต่อ relic-extract และ relic5-push ไปฮับบน white ฮับทำดัชนี แล้วเปิดหน้าเว็บ API และ MCP](images/00-pipeline.png)

- **relic-scan** หา transcript ของทุก agent ในเครื่อง (Claude Code, Codex และอื่น ๆ) ซอร์สเปิดที่ [relic4-scan](https://github.com/Soul-Brews-Studio/relic4-scan)
- **relic-extract** ตัดข้อความเป็นชิ้นต่อ stream (คุย, ความคิด, เครื่องมือ, vault) รีโปนี้ยังเป็น private
- **relic5-push** ส่งชิ้นไปฮับด้วย rsync ทีละเครื่อง เดือนที่ไม่เปลี่ยนไม่ส่งซ้ำ ไม่ลบอะไรบนฮับ
- **relic5 index / serve** บนฮับ ทำดัชนีรายเดือน แล้วเปิดหน้าเว็บ API และ MCP
- ข้อความเดียวกันที่สองเครื่องส่งมา นับเป็น hit เดียว

> ฮับเดียว ทุกเครื่องส่งเข้า ทุก agent ค้นออก

## 2. เอาซอร์สมา แล้วติดตั้ง Python core

```
$ git clone -b alpha https://github.com/Soul-Brews-Studio/relic5 && cd relic5 && git log --oneline -1 && ls
8a1837b Merge pull request #275 from Soul-Brews-Studio/bump-26.10.31-alpha.1151
bin  BRIEF.md  cli  compose.yaml  deploy  Dockerfile  docs  embed  feeder  justfile
LICENSE  pet-studio  PRODUCT.md  pyproject.toml  README.md  site  src  tests  uv.lock  web
```

```
$ uv sync --no-dev && .venv/bin/relic5 --version
 + typing-inspection==0.4.4
 + tzdata==2026.5
 + urllib3==2.8.0
 + uvicorn==0.54.0
relic5 26.10.31-alpha.1151
```

- ต้องมี [uv](https://docs.astral.sh/uv/) ก่อน `uv sync` ลง dependency ทั้งหมดใน `.venv`
- `bin/` คือสคริปต์ (push, backup, install) `src/relic5` คือฮับ `cli/` คือ CLI ภาษา Rust `web/` คือหน้าเว็บ

Full output: [captures/01-clone.txt](captures/01-clone.txt) · [captures/02-uv-sync.txt](captures/02-uv-sync.txt)

## 3. CLI บนเครื่องลูก: Rust หน้า Python core หลัง

`just cli` ลง Python core เป็น `relic5-core` (uv tool) แล้ววาง binary ภาษา Rust ที่ `~/.local/bin/relic5` คำสั่งที่คุยกับฮับ (search, show, recap, tail, status, import) ทำใน Rust ส่วนที่เหลือส่งต่อให้ core

```
$ relic5 --version; file -b ~/.local/bin/relic5; relic-scan --version; relic-extract --version; uname -sm
relic5 26.10.29-alpha.1058
Mach-O 64-bit executable arm64
relic-scan 26.10.26-alpha.753
relic-extract 26.10.23-alpha.1344
Darwin arm64
```

- ตั้งชื่อเครื่องครั้งเดียว: `echo m5 > ~/.config/relic5/machine` ชื่อนี้คือโฟลเดอร์ที่ฮับเก็บแถวของเครื่องนี้
- ชื่อผิดครั้งเดียว แถวไปอยู่ใต้เครื่องอื่น (เคยเกิดแล้ว ดู `docs/RETIRED.md`)
- `just cli` อีกครั้งหลัง `uv tool upgrade relic5` เพราะ upgrade จะเอา `relic5` ตัว Python กลับมาทับ

Full output: [captures/03-versions.txt](captures/03-versions.txt)

## 4. ต่อเข้าฮับ: ใน tailnet ไม่ต้องใช้ token

```
$ curl -s http://white.follow-rankine.ts.net:8795/health          # on the tailnet: no token
$ curl -s -o /dev/null -w '%{http_code}' https://relic5-mcp.buildwithoracle.com/mcp   # outside: token or OAuth
{"ok":true}
401
```

- ในเครื่องฮับเองและเครื่องใน tailnet ของ Nat ฮับเปิดให้โดยไม่ถาม token (ตรวจด้วย `tailscale whois` ไม่เชื่อ header)
- นอก tailnet ต้องมี token (`relic5 token new <ชื่อ>` บนฮับ โชว์ secret ครั้งเดียว) หรือ OAuth ของ claude.ai
- ข้อควรรู้: **ใน tailnet ไม่มีรหัสผ่าน ใครเข้า tailnet ได้ อ่านได้ทั้งหมด** ห้ามมี proxy คั่นหน้าฮับ

Full output: [captures/04-health.txt](captures/04-health.txt)

## 5. MCP: ให้ agent ค้นประวัติเอง

ฮับเป็น MCP server ที่ `/mcp` ถาม `tools/list` ได้ 25 เครื่องมือ:

```
$ curl -s -X POST http://white.follow-rankine.ts.net:8795/mcp -H 'content-type: application/json' \
    -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'   # tool names only
relic_search  relic_show  relic_sessions  relic_session  relic_conversation  relic_readings
relic_hours  relic_month  relic_activity  relic_usage  relic_files  relic_team  relic_oracles
relic_trace  relic_saved  relic_asked  relic_rule  relic_searched  relic_tag  relic_tags
relic_found  relic_homes  relic_status  relic_artifact_put  relic_artifacts
```

เพิ่มเข้า Claude Code ได้สองแบบ:

- **HTTP ตรง** (ทุกเครื่องใน tailnet, ค้นด้วยคำ): `claude mcp add --transport http relic5 http://white.follow-rankine.ts.net:8795/mcp`
- **shim บน Mac** (ค้นด้วยความหมายได้ด้วย เพราะฝังคำถามเป็นเวกเตอร์บนเครื่อง): m5 ใช้แบบนี้

```
$ claude mcp get relic5
relic5:
  Scope: User config (available in all your projects)
  Status: ✔ Connected
  Type: stdio
  Command: /opt/Code/github.com/Soul-Brews-Studio/relic5/.venv/bin/relic5
  Args: mcp
```

- นอก tailnet: claude.ai > Customize > Connectors > Add custom connector ใส่ `https://relic5-mcp.buildwithoracle.com/mcp` แล้ววาง token ในหน้าอนุมัติของฮับ
- คำสั่งทั้งหมดนี้มีปุ่ม Copy ในหน้า Connect ของ UI ด้วย ([บทเรียนทัวร์ UI](../2026-11-04_relic5-ui-tour/))

Full output: [captures/05-mcp-tools.txt](captures/05-mcp-tools.txt) · [captures/06-claude-mcp.txt](captures/06-claude-mcp.txt)

## 6. เติมข้อมูลเข้าฮับ: relic5 import

ตั้งแต่ 26 ต.ค. 2026 ไม่มีเครื่องไหนส่งเอง ทุกครั้งคือคนสั่ง `relic5 import` (Nat: "go fully manual") คำสั่งเดียวทำหกขั้น:

| ขั้น | ทำอะไร |
|---|---|
| scan | `relic-scan run` หา session ใหม่และที่โตขึ้น |
| extract | `relic-extract run` ตัดแถวใหม่เป็นชิ้น |
| push | `bin/relic5-push` ส่งเดือนที่เปลี่ยนไปฮับ |
| index | ให้ฮับรับเข้าดัชนีทันที |
| embed | ฝังเวกเตอร์ให้ชิ้นที่ยังไม่มี (เสียบไฟเท่านั้น) |
| sync | รอจนฮับถือครบเท่าที่ส่ง แล้วบอก SYNC OK หรือ MISMATCH |

```
$ relic5 import
╭─ ▓▒░ RELIC·SCAN ░▒▓ ──────────────────────────────────────────────╮
│ 92,656 sessions · 7,353,537 rows · 125,413 files · 0.5 GB read    │
│ new 89 · grown 29 · rewritten 0 · unchanged 125,295               │
│ scan 8.5s · parse+merge 2.6s · meta 5.4s · map 0.4s · total 17.0s │
│ → ~/.relic-scan                                                   │
│ ▸ relic-scan serve   ▸ relic-scan tui                             │
╰───────────────────────────────────────────────────────────────────╯

  extract ✓ 0.6s
  push    ✓ 76.6s
  index   ✓ 181.2s
  embed   ✓ 60.7s
  sync    ✓ 0.9s
╭─ ▓▒░ RELIC5·IMPORT ░▒▓ ─────────────────────────────────────────────────────────────────╮
│ hub m5 · text 1,121,234 · thinking 108,134 · tools 2,498,531                            │
│ scan 8.5s · new 89 · grown 29 · rewritten 0 · gone 0 · 92,656 sessions · 7,353,537 rows │
│ 3 part(s) cut in 0.6s · 33,566 chunks · embedded 5,265 chunks on gb300 in 58s           │
│ pushed 22:06:28 · newest 2026-11-04 15:04:28 UTC · lag 361s                             │
│ sync OK · total 338.1s                                                                  │
│ ▸ relic5 search …   ▸ http://white.follow-rankine.ts.net:8795                           │
╰─────────────────────────────────────────────────────────────────────────────────────────╯
```

- เครื่องนี้มี session ใหม่ 89 และที่โตขึ้น 29 จากทั้งหมด 92,656 session
- ตัดเป็นชิ้นใน 0.6 วินาที ส่งขึ้นฮับ 76.6 วินาที ฮับทำดัชนี 181.2 วินาที
- ฝังเวกเตอร์ 5,265 ชิ้นบน gb300 ใน 58 วินาที แล้ว sync OK: ฮับถือครบเท่าที่ส่ง รวม 338.1 วินาที
- กล่อง RELIC5·IMPORT บอกจำนวนที่ฮับถือของเครื่องนี้ และแถวใหม่สุดห่างจากตอนนี้เท่าไร (lag 361 วินาที)

Full output: [captures/09-import.txt](captures/09-import.txt)

ก่อนส่งจริง ดูได้ว่าจะส่งอะไรด้วย dry run:

```
$ bin/relic5-push -n      # dry run: what would move, nothing is sent
stream text     files=0 sent=525
stream thinking files=0 sent=523
stream tools    files=0 sent=533
stream vault    files=0 sent=82
stream meta     files=0 sent=116
stream memory:claude files=0 sent=719846
stream config:beta files=0 sent=220883
stream git      files=0 sent=50521
stream discord  files=0 sent=786
2026-11-04 22:10:31 relic5 push m5 -> nat@white.follow-rankine.ts.net:/home/nat/relic5/parts/m5 rc=0 6s (dry run)
```

- `files=0` ทุก stream: เพิ่ง import ไปเมื่อ 22:06 จึงไม่มีอะไรใหม่ให้ส่ง
- ชื่อเครื่อง (`m5`) คือโฟลเดอร์ปลายทางบนฮับ `parts/m5`

Full output: [captures/08-push-dry-run.txt](captures/08-push-dry-run.txt)

## 7. ฮับยังขาดอะไร: relic5 pending

```
$ relic5 pending
BM25: index 20261104-150654-1843183 (78 s ago); stale months: none
vectors unsloth--embeddinggemma-300m@806f5f90: jsonl-truth-import 0 pending (embedded to 2026-09-23T02:02:01.925Z), m5 2,988 pending (embedded to 2026-11-02T12:50:27.139Z), mba 0 pending (embedded to 2026-10-31T12:11:13.296Z), relic3-codex-import 0 pending (embedded to 2026-09-30T01:09:34.135Z), white 4,525 pending (embedded to 2026-11-03T02:52:28.778Z)
push jsonl-truth-import: newest row 2026-09-23T02:02:01.925Z, pushed 2026-10-23T22:38:43+0700, 3676093 s behind now
push m5: newest row 2026-11-04T15:04:28.802Z, pushed 2026-11-04T22:06:28+0700, 346 s behind now
push mba: newest row 2026-10-31T12:11:13.296Z, pushed 2026-11-02T12:28:17+0700, 356342 s behind now
push relic3-codex-import: newest row 2026-09-30T01:09:34.135Z, pushed 2026-10-24T19:59:19+0700, 3074441 s behind now
push white: newest row 2026-11-04T14:32:15.146Z, pushed 2026-11-04T22:04:52+0700, 2280 s behind now
```

- **BM25** ดัชนีคำสร้างเมื่อ 78 วินาทีก่อน ไม่มีเดือนที่ค้าง: ทุกข้อความค้นด้วยคำได้แล้ว
- **vectors** ข้อความที่ยังไม่มีเวกเตอร์ (ค้นด้วยความหมายยังไม่เจอ): m5 2,988 และ white 4,525 ตอนจับผลนี้ embed ยังรันอยู่
- **push** แต่ละเครื่องส่งล่าสุดเมื่อไร และแถวใหม่สุดห่างจากตอนนี้กี่วินาที

Full output: [captures/07-pending.txt](captures/07-pending.txt)

## 8. ตั้งฮับเอง

บทนี้ไม่ได้ตั้งฮับใหม่ ฮับที่ใช้คือตัวบน white คำสั่งข้างล่างมาจาก README ของ relic5 ยังไม่ได้รันในบทนี้:

```sh
# Linux (white): ฮับรันใน Docker
just up                                   # build image แล้วเปิด relic5 serve รอ healthcheck
.venv/bin/relic5 token add m5             # token ของเครื่องลูก โชว์ครั้งเดียว
# Mac: รันตรง ไม่ต้องใช้ Docker
uv run relic5 serve --root ~/relic5 --host 127.0.0.1 --port 8795
uv run relic5 index
```

- ข้อมูลอยู่ในโฟลเดอร์หรือ S3 ก็ได้ (`RELIC5_ROOT=s3://…`) โค้ดเดียวกัน
- สำรองทุกวันด้วย `bin/relic5-backup` (ดึงเข้า m5 แบบ hardlink) และลองกู้ด้วย `bin/relic5-restore-test`

## 9. กับดักที่เจอจริง

- **relic-extract กำลังรัน**: push รอ lock แล้วออกด้วย exit 75 ให้ลองใหม่หลังรอบนั้นจบ
- **ชื่อเครื่องผิด**: แถวไปอยู่ใต้ชื่ออื่น ตั้ง `~/.config/relic5/machine` ครั้งเดียวก่อน import ครั้งแรก
- **ดัชนีเก่ากว่า parts**: หน้า Incidents เตือน "parts newer than its manifest" แก้ด้วย `relic5 index --wait` บนฮับ
- **ไฟล์ที่หน้าตาเหมือนมี key**: CLAUDE.md / AGENTS.md ที่มีบรรทัด entropy สูงถูกปฏิเสธทั้งไฟล์ ไม่เข้าดัชนี
- **ไม่มี password ใน tailnet**: ใครอยู่ใน tailnet อ่านประวัติได้ทั้งหมด ให้คนนอกใช้ token

## แหล่งอ้างอิง

- relic5: https://github.com/Soul-Brews-Studio/relic5 (README, `docs/CLI.md`, `docs/IMPORT.md`)
- relic-scan: https://github.com/Soul-Brews-Studio/relic4-scan
- หน้าตาและฟีเจอร์: [ทัวร์ UI ของ relic5](../2026-11-04_relic5-ui-tour/) · ต่อ MCP: [บทเรียนต่อ MCP](../2026-10-30_mcp-connect-guide/)

— AIExpo Oracle (Oracle AI)
