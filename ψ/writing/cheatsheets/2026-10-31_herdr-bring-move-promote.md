# herdr bring · move · promote · unpromote สูตรโกง

> ย้าย agent ข้าม herdr session โดยบทสนทนาไม่หาย + dry run ก่อนเสมอ + แก้แล้วเปิด PR + ขุดประวัติด้วย relic5 — จาก session `bfe79650` (AIExpo Oracle, m5, 31 ต.ค. 2026)

---

## 🪪 ฉันอยู่ตรงไหน

```bash
echo "HERDR_SESSION=$HERDR_SESSION"          # laris-co
herdr pane get wBZ:p2 | python3 -c "import json,sys;p=json.load(sys.stdin)['result']['pane'];print(p['workspace_id'],p['agent_session']['value'])"
herdr agent rename wBZ:p2 aiexpo-wt          # ชื่อ = ที่อยู่ สำหรับ herdr agent prompt
```

`$HERDR_PANE_ID` ค้างค่าเก่าหลังย้าย pane (`w6A:p9` แต่จริงคือ `wBZ:p2`) — เช็คจาก `herdr pane get` หรือ process tree

## 🔁 เลือกเครื่องมือ

| อยากทำ | ใช้ |
|---|---|
| agent อยู่ใน maw/tmux หรือเหลือแค่ transcript | `herdr-bring` |
| ย้าย oracle ทั้งตัว (main + worktree) หรือ space เดียว ไป session อื่น | `herdr-move` |
| ให้ทั้งทีม (desk + `wt/*`) มี session ของตัวเอง | `herdr-promote` |
| เอากลับ + ตั้งชื่อ pane + ลบ session ที่ว่าง | `herdr-unpromote` |
| session เดิม แค่จัดหน้าจอ (ไม่ restart) | `herdr-room` / `herdr-bring-beside` |

ทุกตัวคือ "ปิดที่นี่ → resume ที่โน่นด้วย session id เดิม" — pane ข้าม session ไม่ได้

## 🐾 herdr-move — ตัวทำงานจริง

```bash
herdr-move aiexpo-oracle --dry                      # ใครจะย้าย จาก session ไหน
herdr-move aiexpo-oracle --to aiexpo                # ย้ายจริง: รันจาก pane ที่ไม่อยู่ในชุด
herdr-move --workspace wBZ --from laris-co --dry    # เฉพาะ agent ใน space เดียว
```

ลำดับ: ปิด pane → รอ id หายทุกตัว (10 วิ) → ปิด space ที่เหลือแต่ shell → start session ปลายทาง → `maw herdr ticket open … --session-id <id>`

## 🎖️ herdr-promote / herdr-unpromote

```bash
herdr-promote wBZ --from laris-co --dry             # space wBZ → session ของมันเอง
herdr-promote wBZ --from laris-co --to aiexpo --dry # ตั้งชื่อเอง (label มี / ต้องใช้ --to ถ้ายังไม่ได้ merge #25)
herdr-promote rd-team --dry                         # ทั้งทีม: desk + wt/<oracle>
herdr-unpromote aiexpo --dry                        # เอากลับเข้า session ที่เรียก
herdr-unpromote --session phd --dry                 # session ว่าง → ลบ session + link + room state
```

promote เรียก herdr-move · unpromote เรียก herdr-move แล้วตั้งชื่อ pane + เก็บกวาด

## 🔍 ก่อนย้ายจริง — เช็ค 3 อย่าง

```bash
# 1. flag ที่ resume จะทิ้ง (--channels = Discord bot หาย, --model = กลับเป็น default)
herdr --session laris-co pane process-info --pane wBZ:p2 | python3 -c "
import json,sys
for f in json.load(sys.stdin)['result']['process_info']['foreground_processes']:
    if 'claude' in f['name'].lower(): print(f['pid'], f['cmdline'][:160])"

# 2. ใคร idle ใคร working
herdr --session laris-co agent list | python3 -c "import json,sys;[print(a['pane_id'],a.get('name'),a.get('agent_status')) for a in json.load(sys.stdin)['result']['agents']]"

# 3. session ไหนว่าง / มีร่างซ้ำ
herdr session list
for s in people oracle-gods-eys-os phd; do herdr --session $s agent list | python3 -c "import json,sys;a=json.load(sys.stdin)['result']['agents'];print('$s',len(a))"; done
```

## 🔎 อ่านสคริปต์ก่อนเชื่อ --dry

```bash
P=$(readlink -f ~/.local/bin/herdr-promote); rg -n -i 'dry' "$P"
sed -n 37,113p ~/.local/bin/herdr-move | rg -n 'herdr |maw |kill|close|stop|create|rename|rm '   # ก่อน exit ของ --dry มีแต่คำสั่งอ่าน
```

## 🛠️ แก้แล้วเปิด PR (worktree, ไม่แตะ main)

```bash
R=/opt/Code/github.com/Soul-Brews-Studio/herdr-orca-oracle
WT=$R/wt/herdr-move-safe-name-aiexpo-31oct-sat2026
git -C $R fetch -q origin
git -C $R worktree add -b herdr-move-safe-name-aiexpo-31oct-sat2026 "$WT" origin/main
/bin/bash -n "$WT/scripts/herdr-move"                               # macOS bash 3.2 ต้องผ่าน
/bin/bash "$WT/scripts/herdr-promote" wBZ --from laris-co --dry     # ทดสอบด้วย --dry เท่านั้น
git -C "$WT" push -u origin herdr-move-safe-name-aiexpo-31oct-sat2026
~/.claude/skills/herdr-pr/herdr-sign.sh claude-opus-5-5 --work "$WT"   # บล็อก "Built by" ท้าย PR
gh pr create --repo Soul-Brews-Studio/herdr-orca-oracle --base main --head herdr-move-safe-name-aiexpo-31oct-sat2026 --body-file "$B"
```

ผล: Soul-Brews-Studio/herdr-orca-oracle#25 (ชื่อ session ปลอดภัย + เตือน flag) · Soul-Brews-Studio/herdr-fleet#2 (เปลี่ยนชื่อ herdr-promote ตัวที่ชนกัน)

## ⏳ งานยาว → herdr pane (ไม่ block)

```bash
P=$(herdr pane split wBZ:p2 --direction down --no-focus | python3 -c "import json,sys;print(json.load(sys.stdin)['result']['pane']['pane_id'])")
herdr pane run $P 'time python3 ~/.claude/skills/dig/scripts/dig.py 0 --deep > /tmp/dig-deep-all.json; RC=$?; OUT=$(ls -la /tmp/dig-deep-all.json); herdr agent prompt aiexpo-wt "PANE '$P' rc=$RC
$OUT" && herdr pane close '$P''
```

## 🧭 ขุดด้วย relic5 (MCP)

```text
relic_searched  query="skills list compare"                      # ถามก่อนว่าเคยมีใครค้นแล้วไหม
relic_search    query="herdr-bring"  horizon="archive"           # BM25 ทุกเดือน
relic_search    query="herdr-bring herdr-promote" with="git"      # commits · tools · memory · discord · vault
relic_search    query="give a team its own herdr session and bring it back later" semantic=true
relic_session   id="bfe79650"                                    # session นี้ + resume command
relic_found     parent=<trace.id> goal=… how=… found=… links=[…]  # ปิด trace ทุกครั้ง
```

## 📊 นับ skills + เทียบเครื่อง

```bash
ls ~/.claude/skills | wc -l                                              # 303 (301 skill + zip + VERSION.md)
rg -o --no-filename "<command-name>/[a-z0-9:_-]+</command-name>" ~/.claude/projects | sed "s/<[^>]*>//g;s#^/##" | sort | uniq -c | sort -rn | head
ssh nat@white 'ls ~/.claude/skills' > /tmp/skillcmp/white-claude.txt
comm -13 <(sort /tmp/skillcmp/m5-beta-claude.txt) <(sort /tmp/skillcmp/white-claude.txt)   # มีแต่ white
md5 -q ~/.claude/skills/herdr-bring/SKILL.md                             # เทียบ copy แต่ละเครื่อง
```

## 🪣 ralph-dig (digger wiki)

```bash
cd /opt/Code/github.com/Soul-Brews-Studio/digger-oracle
bun ψ/ralph/scripts/registry-lookup.ts promote        # เคยขุดหรือยัง
bun ψ/ralph/scripts/next-dig-seq.ts                    # เลข dig ถัดไป (268)
bun ψ/ralph/scripts/index-build.ts && bun ψ/ralph/scripts/registry-build.ts && bun ψ/ralph/scripts/wiki-health.ts
rtk maw hey digger "[m5:aiexpo-oracle] ralph-dig #268: promote unpromote bring — …"
```

## ⚡ ลัด

| ทำอะไร | คำสั่ง |
|--------|--------|
| ดูแผนย้าย space | `herdr-promote wBZ --from laris-co --dry` |
| ดูแผนย้าย oracle | `herdr-move aiexpo-oracle --dry` |
| เอาทีมกลับ | `herdr-unpromote <team> --dry` แล้วค่อยรันจริง |
| เปิด session ตามชื่อ | `herdr --session manager-team` |
| คำสั่ง session สั้น | `ln -s herdr-by-name ~/.local/bin/<session>` |
| session ของฉัน + resume | relic5 `relic_session id=bfe79650` |
| ใครย้ายได้ | pane นอกชุด (desk ของ laris-team = LarisCo) |
| เซ็น PR | `~/.claude/skills/herdr-pr/herdr-sign.sh claude-opus-5-5 --work "$WT"` |

## ⚠️ trap ที่เจอจริง

| trap | วิธีเลี่ยง |
|------|-----------|
| label `wt/aiexpo-oracle` → ชื่อ session `wt/aiexpo` (มี `/`) | ใส่ `--to aiexpo` · แก้แล้วใน herdr-orca-oracle#25 |
| resume ทิ้ง `--channels` / `--model` (bot Discord หาย) | ดูใน `--dry` (#25 ขึ้น ⚠) · relaunch ด้วย team-wake |
| รันจาก pane ที่อยู่ในชุด → ถูกปฏิเสธ (`!` ใน pane สมาชิกก็นับ) | รันจาก space อื่น / desk ของ laris-team |
| `$HERDR_PANE_ID` ค้างหลังย้าย | `herdr pane get` / `herdr agent list` ใหม่ทุกครั้ง |
| pane id เปลี่ยนทุกครั้งที่ room in/out | อ่าน `herdr agent list` ก่อนส่งข้อความ |
| ชื่อ `herdr-promote` ซ้ำ 2 ตัว (herdr-fleet = จบ incubation) | herdr-fleet#2 เปลี่ยนเป็น `herdr-incubate-promote` |
| unpromote ทันทีหลัง promote → ไม่ย้ายอะไร | รอสักครู่ให้ herdr เห็น agent ก่อน |
| herdr-bring เลือก `.jsonl` ใหม่สุด อาจผิดตัวถ้ามี fork | เช็คด้วย `maw peek <handle>` ก่อน |
| ย้ายแบบปิดแล้วเปิดใหม่ (31 ต.ค.) → ได้ conversation id ใหม่ | ใช้ herdr-move: id เดิม |
| ทดสอบ move จริงบน session ที่ใช้งานอยู่ | กฎ desk: ของจริงเฉพาะ scratch session · live ใช้ `--dry` เท่านั้น |
| `pane process-info` ฟิลด์ `pid` ตัวแรกไม่ใช่ claude | กรอง `foreground_processes` ด้วยชื่อ / `argv0` |
| zsh: `echo ===` → `== not found` | ใส่ quote หรือใช้ตัวคั่นอื่น |
| relic5 semantic ไม่ค้น SKILL.md (config layer ไม่มี vector) · hub OOM 1 ครั้ง | ใช้ keyword `with="config"` · ลองใหม่ภายหลัง |
| `dig.py` อ่านแค่ metadata → เจอ 1 ใน ~15 session | ใช้ relic5 ค้นเนื้อความ |
| herdr-bring บน white / codex เป็นรุ่นเก่า (240 บรรทัด) | เทียบ `md5` แล้ว copy รุ่น 270 บรรทัด |
| white ไม่มี herdr-move / promote / unpromote | ติดตั้งจาก herdr-orca-oracle `scripts/` หลัง merge |

---

🤖 ตอบโดย AIExpo Oracle (Oracle AI) จาก Nat → aiexpo-oracle
