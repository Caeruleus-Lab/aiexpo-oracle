#!/usr/bin/env python3
"""Build README.md (Thai) and README.en.md (English) from skills/<name>/ — the full text of every herdr skill.

Run from anywhere: python3 tools/build_readme.py. The skill texts are copied verbatim; only the
one-line summaries and the group headings below are written by hand.
"""
import pathlib, re

here = pathlib.Path(__file__).resolve().parent.parent
skills = here / "skills"

GROUPS = [
    ("base", "พื้นฐาน และ ฉันอยู่ตรงไหน", "Base, and where am I",
     ["herdr", "herdr-whoami", "herdr-info", "herdr-tree", "herdr-structure", "herdr-neighbors", "herdr-twin"]),
    ("wt", "หนึ่ง worktree ตั้งแต่เริ่มจนจบ", "One worktree, start to finish",
     ["herdr-wt", "herdr-fib-wt", "herdr-idea", "herdr-issue", "herdr-ticket", "herdr-work", "herdr-rename",
      "herdr-pr", "herdr-wt-ship", "herdr-done", "herdr-finished", "herdr-dissolve", "herdr-clean-up-sync",
      "herdr-trinity"]),
    ("talk", "คุยกับ agent", "Talking to agents",
     ["herdr-hey", "herdr-peek", "herdr-ask", "herdr-roomcast", "herdr-sessioncast", "herdr-soulcast",
      "herdr-send", "herdr-handover", "herdr-pane-run"]),
    ("rooms", "ห้อง และ ทีม", "Rooms and teams",
     ["herdr-room", "herdr-team", "herdr-team-ctl", "herdr-lead-scouts", "herdr-buddy", "herdr-bring-beside"]),
    ("move", "ย้าย agent", "Moving agents",
     ["herdr-bring", "herdr-move", "herdr-promote", "herdr-unpromote", "herdr-incubate", "herdr-soul"]),
    ("machines", "หลายเครื่อง", "Machines",
     ["herdr-link", "herdr-link-local", "herdr-link-remote", "herdr-link-talk", "herdr-link-teardown",
      "herdr-link-check", "herdr-machine-labels"]),
    ("sleep", "พัก และ เก็บกวาด", "Sleep and clean-up",
     ["herdr-sleep", "herdr-vacation", "herdr-blank"]),
]

# One line per skill, summarised from its own description: field.
TH = {
    "herdr": "สกิลฐานของ herdr: คำสั่ง CLI สำหรับดูและควบคุม pane, tab, workspace และ agent ตัวอื่น ใช้เมื่อพูดถึง herdr ตรง ๆ",
    "herdr-whoami": "บอกว่า agent ตัวนี้รันอยู่ที่ไหน: เครื่อง, session/space/tab/pane, Claude session id, branch, worktree หรือ main",
    "herdr-info": "แสดงทุกร่างของ oracle หนึ่งตัวบนเครื่องนี้ ทั้งใน herdr และนอก herdr พร้อม Discord แล้วเช็กกฎ one soul many bodies",
    "herdr-tree": "แสดง main checkout กับทุก worktree ของ repo เป็นต้นไม้ พร้อม space, สถานะ agent และสถานะ git",
    "herdr-structure": "วาดทั้ง session เป็นต้นไม้: ทุก space, ห้องไหนมี 2 agent ขึ้นไป, ชื่อ agent, สถานะ, หัวหน้าทีม และ \"me\"",
    "herdr-neighbors": "สำรวจทุก pane รอบตัวก่อนแตะ ทั้งสี่ทิศและทั้ง workspace ว่าเป็น agent หรือ shell อ่านอย่างเดียว",
    "herdr-twin": "หาว่า session เดียวกันรันอยู่บนเครื่องไหนบ้าง พร้อมจำนวน agent และสถานะ แล้วสลับ twin mode ใน sidebar",
    "herdr-wt": "ตัด git worktree ที่ <repo>/wt/<slug>-<oracle>-<date> เปิดเป็น space ของมันเอง เปิด issue ก่อน แล้ว brief agent จาก issue",
    "herdr-fib-wt": "ตัดหนึ่ง worktree ต่อหนึ่ง slug แล้วเปิดเป็น pane ใน tab นี้ จัดเป็นเกลียว Fibonacci รอบ pane ของเรา",
    "herdr-idea": "เริ่ม lab ที่มีเลขลำดับ: ตัด worktree ที่ wt/NN-slug เปิด space และเขียน README แบบ charter-lite",
    "herdr-issue": "เปลี่ยนงานเป็น GitHub issue ใน repo ของ oracle ที่ถูกตัวก่อน แล้วตัด worktree เปิด space และ brief agent ให้ทำจนเป็น PR",
    "herdr-ticket": "พา GitHub issue หนึ่งใบไปทำใน space และ worktree แยกของมัน ตั้งชื่อแบบ /herdr-wt ด้วยสคริปต์ ticket.sh",
    "herdr-work": "คำสั่งเดียวจากชื่อ repo ถึงร่างที่ทำงานได้: สร้างหรือหา repo, clone เข้า ghq, เปิด space และเริ่ม Claude",
    "herdr-rename": "เปลี่ยนชื่อ branch ของ worktree (ป้ายใน sidebar) เป็นชื่อที่สื่อความหมาย AI เลือกจากงานจริงของ session",
    "herdr-pr": "เซ็น PR, issue หรือ comment ด้วยบล็อก \"Built by\": oracle, model, worktree, branch, transcript และที่อยู่ herdr",
    "herdr-wt-ship": "แสดงทุก worktree เป็นตารางที่วัดจริงก่อน แล้วปิดตัวที่เสร็จ: เซ็น PR ที่ merge แล้ว เขียน tombstone ลบ worktree",
    "herdr-done": "ตัดสินว่า session ปิดได้หรือยัง: ตรวจงานที่จะหาย (ไม่ commit, ไม่ push, ไม่มี upstream) แล้วพาทำขั้นส่งต่อ",
    "herdr-finished": "ปิด session นี้ในรอบเดียวไม่มี popup: ตรวจด้วย herdr-done, เขียน /rrr, เซ็น PR, ลบ worktree เมื่อ PR merge แล้ว",
    "herdr-dissolve": "ด้านกลับของ /herdr-wt: เก็บงานก่อน แล้วปิด worktree, pane และ space ตั้งแต่ worktree เดียวจนทั้งเครื่อง ถามก่อนเสมอ",
    "herdr-clean-up-sync": "ชื่อเก่า รวมเข้า /herdr-dissolve แล้วเมื่อ 29 ต.ค. 2026 (ใช้ --sweep หรือ --sync) ไฟล์นี้แค่ชี้ทาง",
    "herdr-trinity": "ปิดทุก worktree ของ repo ตามกฎ trinity (เกิดขึ้น ตั้งอยู่ ดับไป): ตาราง, peek, brief ให้ commit push PR, merge เมื่อ Nat บอก go",
    "herdr-hey": "ส่งข้อความถึง agent ใน pane ข้าง ๆ แล้วอ่านคำตอบ แยกทางส่งระหว่าง agent กับ shell เปล่า",
    "herdr-peek": "ดูว่า agent ใน pane ข้าง ๆ ทำอะไรอยู่โดยไม่ขัดจังหวะ อ่าน scrollback ล่าสุดของมัน",
    "herdr-ask": "⌘J: กล่อง popup พิมพ์หนึ่งบรรทัดส่งถึงทุก agent ใน tab นี้ หรือกด ←/→ เลือก pane เดียว",
    "herdr-roomcast": "ส่งหนึ่งบรรทัดถึงทุก agent ในห้องหนึ่ง (space ตามชื่อ) บนเครื่องนี้หรือเครื่องอื่นที่บันทึกไว้",
    "herdr-sessioncast": "ส่งหนึ่งบรรทัดถึงทุก agent ใน session เดียว พร้อมบอกต้นทาง บอกแต่ละตัวว่ามันคือ session:pane ไหน และทางตอบกลับ",
    "herdr-soulcast": "ส่งหนึ่งบรรทัดถึงทุกร่างของ oracle ตัวเดียวบนเครื่องนี้ ทุก session ทุก space ทุก worktree",
    "herdr-send": "ส่งงานให้ oracle ตัวอื่นและเลือก engine: เปิด issue ใน repo ปลายทาง ตัด worktree เริ่ม claude, codex หรือ omx แล้ว brief",
    "herdr-handover": "ส่งมอบสิ่งที่ยังรันอยู่ (repo, server, extension) ให้ agent อีก pane แล้วเฝ้าดูโดยไม่แทรก",
    "herdr-pane-run": "รันคำสั่งยาวใน pane ให้คนเห็นสด ๆ แล้วให้ pane อ่าน output ตัวเอง ส่งผลจริงพร้อม exit code กลับมา",
    "herdr-room": "ดึง agent ที่รันอยู่มารวมในห้องเดียว (space เดียว tab เดียว) แล้วส่งกลับ space ของตัวเอง สลับได้ไม่ต้อง restart",
    "herdr-team": "เปิด team charter (ψ/teams/*.yaml) เป็น agent ใน space เดียว จัดแบบ Fibonacci เริ่มแต่ละคนด้วย engine ของมัน",
    "herdr-team-ctl": "start, stop หรือ status ทั้งทีมตามชื่อ charter บน session และเครื่องที่เลือก resume แต่ละคนด้วย session id ของมันเอง",
    "herdr-lead-scouts": "จัด lead หนึ่ง pane ทางซ้าย กับ scout สองตัวทางขวา brief คนละครึ่งงาน แล้วให้รายงานกลับเข้า pane lead",
    "herdr-buddy": "แยก pane แล้ววาง buddy agent แบบไม่ถาม approval ข้าง ๆ (omx, omp หรือ claude) ไม่ยอมรันใน main checkout",
    "herdr-bring-beside": "ย้าย pane อื่น (agent หรือ shell) มาไว้ใน tab ของเรา ข้างขวาหรือข้างล่าง agent ยังรันต่อ แค่ pane id เปลี่ยน",
    "herdr-bring": "หา maw handle ด้วย maw locate แล้วเปิด space ของมันใน herdr พร้อม resume ประวัติ Claude ที่มีอยู่",
    "herdr-move": "ย้าย oracle หนึ่งตัว ทุก agent ของ repo ทั้ง main และ worktree เข้า session ของมันเอง resume ด้วย id เดิม",
    "herdr-promote": "ให้ทีม, repo หรือ space หนึ่ง มี session ของมันเอง: จบ agent ที่เดิม แล้ว resume ที่ปลายทางด้วย session id เดิม",
    "herdr-unpromote": "พาทีม, oracle หรือ session ที่ promote ไป กลับเข้า session (ค่าเริ่มต้นคือของเรา) ด้วย id เดิม แล้วลบ session ที่ว่าง",
    "herdr-incubate": "ทำงานหัวข้อของ oracle ตัวอื่นจากใน repo นี้: ตัด worktree ที่ wt/<owner>-<target>-<date> และวาง breadcrumb INCUBATED_BY",
    "herdr-soul": "หนึ่งสกิลหกคำสั่ง (list, ls, check, in, out, ears) เอาวิญญาณ oracle ไปทำงานใน repo อื่น ทำงานด้วยสคริปต์ bin/herdr-soul",
    "herdr-link": "ดัชนีของชุด link: session ต่อ oracle, worker บนเครื่องอื่น, ให้ session คุยกันไม่ต้องพิมพ์ ssh, เช็กเส้นทาง, รื้อ worker",
    "herdr-link-local": "ให้ oracle มี session ของมันเองบน m5: ย้ายทุก agent ออกจาก session รวมอย่าง laris-co บทสนทนาเดิม",
    "herdr-link-remote": "ตั้ง worker oracle บนเครื่องอื่น (white, black) ครบขั้น: เช็กเครื่อง, token, worktree, .envrc, autostart, เริ่มครั้งแรก",
    "herdr-link-talk": "ให้สอง session บนสองเครื่องคุยกันได้ทั้งสองทางโดยไม่พิมพ์ ssh แล้วยืนยันด้วยการส่งไปกลับหนึ่งรอบ",
    "herdr-link-teardown": "ถอด worker oracle ออกจากเครื่องอื่นให้เรียบร้อย: ลบ machine, ปิด systemd unit, ลบ roster row, ลบ worktree และ branch",
    "herdr-link-check": "เช็กแบบอ่านอย่างเดียว: ทุก session, ทุกเครื่องที่บันทึกไว้, ทุกเส้นทางข้ามเครื่อง, autostart และ Discord body",
    "herdr-machine-labels": "ตั้งชื่อเครื่องที่บันทึกไว้เป็น \"<host> · <session>\" ให้ sidebar เรียง session เดียวกันจากสองเครื่องเป็นคู่",
    "herdr-sleep": "พัก space ให้ตื่นมาที่เดิมเป๊ะ: ขอ bookmark จาก agent เขียน wake card (cwd, kind, session id, argv) แล้วค่อยปิด",
    "herdr-vacation": "พัก agent ที่ idle นานกว่า N ชั่วโมง (ค่าเริ่มต้น 3) ก่อนคนไม่อยู่: quit แล้วปิด space transcript ยังอยู่ resume ได้",
    "herdr-blank": "หา space ที่ทุก pane เป็น shell เปล่าว่าง ๆ แล้วปิดด้วย --close ไม่ปิด space ที่มีอะไรรันอยู่",
}

EN = {
    "herdr": "The base herdr skill: the CLI to inspect and control panes, tabs, workspaces and other agents; used when herdr is named.",
    "herdr-whoami": "Where THIS agent runs: machine, session/space/tab/pane, Claude session id, branch, worktree or main.",
    "herdr-info": "Every body of one oracle on this machine, in and out of herdr, plus Discord, checked against the one-soul-many-bodies rules.",
    "herdr-tree": "This repo's main checkout and every worktree as a tree, with herdr space, agent status and git status.",
    "herdr-structure": "A whole herdr session drawn as a tree: spaces, rooms (2+ agents), agent names, status, team lead and \"me\".",
    "herdr-neighbors": "Survey every pane around you (four directions and the workspace) as agent or shell before touching any. Read-only.",
    "herdr-twin": "Find every machine running the same session, with agent count and status, and toggle the sidebar's twin mode.",
    "herdr-wt": "Cut a worktree at <repo>/wt/<slug>-<oracle>-<date>, open it as its own space; opens an issue first and briefs the agent from it.",
    "herdr-fib-wt": "One worktree per slug, each a pane in the current tab, laid out as a Fibonacci spiral around your pane.",
    "herdr-idea": "Start a numbered lab: worktree at wt/NN-slug, its own space, and a charter-lite README.",
    "herdr-issue": "Turn a task into an issue in the right oracle's repo, then cut a worktree, open a space and brief an agent to a PR.",
    "herdr-ticket": "Take one GitHub issue through its own space and worktree, named the /herdr-wt way, with ticket.sh.",
    "herdr-work": "One command from a repo name to a working body: create or find the repo, clone into ghq, open a space, start Claude.",
    "herdr-rename": "Rename the worktree's branch (the sidebar label) to a meaningful name the AI picks from the session's real work.",
    "herdr-pr": "Sign a PR, issue or comment with a \"Built by\" block: oracle, model, worktree, branch, transcript and herdr address.",
    "herdr-wt-ship": "Show every worktree as one measured table first, then finish the done ones: sign, tombstone, remove, delete branch.",
    "herdr-done": "Decide whether a session can be closed: audit for work that would be lost, then walk the hand-off steps.",
    "herdr-finished": "Finish this session in one pass with no popups: herdr-done audit, /rrr, signed PR, remove the worktree only if merged.",
    "herdr-dissolve": "The reverse of /herdr-wt: save the work, then close worktrees, panes and spaces, from one worktree up to the whole machine; asks first.",
    "herdr-clean-up-sync": "Old name, merged into /herdr-dissolve on 29 Oct 2026 (--sweep or --sync); this file only redirects.",
    "herdr-trinity": "Wind down every worktree of the repo under the trinity rule (arise, stand, cease): table, peek, brief, merge on Nat's go.",
    "herdr-hey": "Send a message to the agent in the neighbouring pane and read its answer; routes differently for an agent or a bare shell.",
    "herdr-peek": "Look at what the neighbouring agent is doing without interrupting it, by reading its recent scrollback.",
    "herdr-ask": "⌘J: a popup that types one line into every agent pane of the current tab, or ←/→ to pick one pane.",
    "herdr-roomcast": "Send one line to every agent of one room (a space, by label), here or on a saved remote machine.",
    "herdr-sessioncast": "Broadcast one line to every agent of one session, origin stamped, each told its session:pane, with a reply route.",
    "herdr-soulcast": "Broadcast one line to every body of one oracle on this machine: all sessions, spaces and worktrees.",
    "herdr-send": "Hand a task to another oracle and pick the engine: issue in its repo, worktree, claude/codex/omx, brief from the issue.",
    "herdr-handover": "Hand a live surface (repo, server, extension) to a peer agent in another pane, then watch without interfering.",
    "herdr-pane-run": "Run a long command in a pane so the human watches it live; the pane sends back the real output and exit code.",
    "herdr-room": "Pull live agents into one room (one space, one tab) and send them back to their own spaces, as often as you like, no restart.",
    "herdr-team": "Bring up a team charter (ψ/teams/*.yaml) as agents in one space, Fibonacci layout, each started with its engine.",
    "herdr-team-ctl": "Start, stop or check a whole team by charter name on a session and machine; each member resumes its own conversation.",
    "herdr-lead-scouts": "One lead pane on the left and two scouts on the right, each briefed with half a task, reporting back to the lead.",
    "herdr-buddy": "Split the pane and drop a bypass-approvals buddy (omx, omp or claude) beside you; refuses to run in a main checkout.",
    "herdr-bring-beside": "Move another pane (agent or shell) into my tab, right of me or below; the agent keeps running, only its pane id changes.",
    "herdr-bring": "Resolve a maw handle with maw locate, open its own herdr space and resume its local Claude history.",
    "herdr-move": "Move one oracle (every live agent of its repo, main and worktrees) into a session of its own, resuming each by id.",
    "herdr-promote": "Give a team, repo or space a session of its own: each agent ends where it runs and resumes there with the same id.",
    "herdr-unpromote": "Bring a promoted team, oracle or session back (default: here) with the same ids, then remove the emptied session.",
    "herdr-incubate": "Work on another oracle's topic from inside this repo: worktree at wt/<owner>-<target>-<date> plus an INCUBATED_BY breadcrumb.",
    "herdr-soul": "One skill, six verbs (list, ls, check, in, out, ears) to put an oracle's soul to work in another repo, via bin/herdr-soul.",
    "herdr-link": "Index of the link family: a session per oracle, a worker on another machine, sessions that talk without ssh, checks, teardown.",
    "herdr-link-local": "Give an oracle its own session on m5: move its agents out of a shared session like laris-co, same conversations.",
    "herdr-link-remote": "Provision a worker oracle on another machine (white, black) end to end: box, token, worktree, .envrc, autostart, first start.",
    "herdr-link-talk": "Make two sessions on two machines talk both ways with no ssh typed, verified by a round trip.",
    "herdr-link-teardown": "Remove a worker oracle from another machine cleanly: saved machine, systemd unit, roster row, worktree, branch.",
    "herdr-link-check": "Read-only check of every session, saved machine and cross-machine route, autostart units and the Discord body.",
    "herdr-machine-labels": "Name every saved machine \"<host> · <session>\" so the sidebar shows the same session on two machines as a pair.",
    "herdr-sleep": "Put spaces to sleep so they wake exactly where they were: bookmark from the agent, a wake card, then close.",
    "herdr-vacation": "Park agents idle longer than N hours (default 3) before the human goes away: quit and close; transcripts stay resumable.",
    "herdr-blank": "Find spaces whose every pane is a bare idle shell and close them with --close; never closes a space where anything runs.",
}

NOTE = {
    "herdr": {"th": "`herdr` ใน `~/.claude/skills/` เป็น symlink ไปที่ `~/.agents/skills/herdr` ที่นี่คัดลอกไฟล์ปลายทาง",
              "en": "`herdr` in `~/.claude/skills/` is a symlink to `~/.agents/skills/herdr`; the target's files are copied here."},
    "herdr-soul": {"th": "เป็น symlink ไปที่ `laris-co/soul-in-repo/skills/herdr-soul` ที่นี่คัดลอกไฟล์ปลายทาง",
                   "en": "A symlink to `laris-co/soul-in-repo/skills/herdr-soul`; the target's files are copied here."},
    "herdr-work": {"th": "เป็น symlink ไปที่ `laris-co/neo-oracle/.claude/skills/herdr-work` ที่นี่คัดลอกไฟล์ปลายทาง",
                   "en": "A symlink to `laris-co/neo-oracle/.claude/skills/herdr-work`; the target's files are copied here."},
}

all_names = sorted(p.name for p in skills.iterdir() if (p / "SKILL.md").exists())
grouped = [n for g in GROUPS for n in g[3]]
assert sorted(grouped) == all_names, set(grouped) ^ set(all_names)
assert set(TH) == set(all_names) == set(EN)


def nlines(p):
    return len(p.read_text(encoding="utf-8").splitlines())


def fence_for(text):
    runs = [len(m) for m in re.findall(r"`{3,}", text)]
    return "`" * (max(runs) + 1 if runs else 3)


total_skill_lines = sum(nlines(skills / n / "SKILL.md") for n in all_names)
all_files = sorted(p for p in skills.rglob("*") if p.is_file())
total_file_lines = sum(nlines(p) for p in all_files)

T = {
    "th": dict(
        title="# herdr ทุกสกิล ฉบับเต็ม",
        summary=("> บทที่ 6 ของชุด herdr: สกิล `/herdr-*` ครบทั้ง {n} ตัว ตามที่อยู่บน m5 วันที่ 8 พ.ย. 2026 "
                 "ทุก SKILL.md อยู่ในหน้านี้แบบคำต่อคำ พร้อมสคริปต์และไฟล์อื่นของแต่ละสกิลในโฟลเดอร์ `skills/` "
                 "รวม {f} ไฟล์ {l:,} บรรทัด สแกน secret แล้วไม่เจอ คนอ่านได้ AI คัดลอกไปใช้ได้"),
        other="- ฉบับอื่น: [English](README.en.md)",
        byai="- เขียนโดย AIExpo Oracle (AI) ไม่ใช่คน",
        intro_h="## 1. หน้านี้คืออะไร",
        intro=[
            "- Nat บอกเมื่อ 8 พ.ย.: \"the 6th lesson do write full all skills and content full again one\"",
            "- บทอื่นในชุดอธิบายว่าใช้สกิลไหนเมื่อไร หน้านี้คือตัวจริงทั้งหมด ไว้อ่านหรือคัดลอก",
            "- ข้อความในสกิลเป็นภาษาเดิม (ส่วนใหญ่อังกฤษ) ไม่ได้แปล คำอธิบายบรรทัดเดียวเหนือแต่ละสกิลเป็นภาษาไทย",
            "- แต่ละสกิลมีลิงก์ไปที่ `skills/<name>/SKILL.md` และไฟล์อื่น (สคริปต์, ไฟล์ .bak) ของมัน",
            "- ภาพรวมทั้ง 52 ตัวกับไทม์ไลน์อยู่ใน [แผนที่สกิล herdr](../2026-11-08_herdr-skill-map/README.md)",
        ],
        groups_h="## 2. 7 กลุ่ม",
        groups_intro="สกิลแบ่งตามงานเป็น 7 กลุ่ม เหมือนบทแผนที่สกิล:",
        img_groups_alt="แผนภาพ 7 กลุ่มของสกิล herdr 52 ตัว พร้อมชื่อสกิลในแต่ละกลุ่ม",
        install_h="## 3. ติดตั้ง",
        install=[
            "- สกิลหนึ่งตัวคือหนึ่งโฟลเดอร์ คัดลอกโฟลเดอร์นั้นไปไว้ใน `~/.claude/skills/` แล้วเปิด Claude Code ใหม่",
            "- เรียกด้วย `/<ชื่อโฟลเดอร์>` เช่น `/herdr-wt`",
            "- สกิลส่วนใหญ่ต้องรันใน pane ของ herdr (`HERDR_ENV=1`) และหลายตัวอ้างถึงเครื่อง m5, white, repo และ oracle ของ Nat ต้องปรับเองก่อนใช้ที่อื่น",
            "- ไฟล์ `.bak` คือเวอร์ชันก่อนหน้าที่เก็บไว้ในโฟลเดอร์สกิลบน m5 ไม่ต้องคัดลอกไปด้วยก็ได้",
        ],
        install_code="ขั้นตอนตัวอย่าง:",
        video_h="## 4. ในวิดีโอ",
        video=("3 พ.ย. 2026 Nat อัดจอสองคลิป (\"Herdr part 1\" และ \"Herdr part 2\") ระหว่างนั้นสั่ง `/herdr-wt demo-hello-world` "
               "ตอน 21:28 แล้วตามด้วย `/herdr-rename`, `/herdr-pr` และ `/herdr-dissolve` "
               "ภาพนี้คือนาที 23:30 ของคลิปแรก: issue #129 ใน laris-co/laris-team ที่ `/herdr-wt` เปิดให้เองก่อนตัด worktree "
               "มีหัวข้อ Rules, Done when, Out of scope, Workspace และบรรทัดท้าย \"Opened by Laris Labs Oracle (AI) via /herdr-wt\" "
               "ข้อความนี้มาจากขั้นตอนใน [skills/herdr-wt/SKILL.md](skills/herdr-wt/SKILL.md)"),
        frame_alt="เฟรมจากวิดีโอ Herdr part 1: issue #129 ที่ /herdr-wt เปิดให้ มีหัวข้อ Rules, Done when, Out of scope และ Workspace",
        oneline="ทำอะไร:",
        file_link="ไฟล์",
        extra="ไฟล์อื่นในโฟลเดอร์นี้:",
        lines="บรรทัด",
        traps_h="## 12. กับดักที่เจอจริง",
        traps=[
            "- `herdr`, `herdr-soul` และ `herdr-work` บน m5 เป็น symlink ถ้าคัดลอกด้วย `cp -r` ธรรมดาจะได้แค่ลิงก์ ต้องใช้ `cp -RL` เพื่อเอาไฟล์จริง",
            "- `herdr-info/__pycache__/` เป็นไฟล์ binary ของ Python ไม่ใช่ส่วนของสกิล ไม่ได้คัดลอก",
            "- `herdr-clean-up-sync` ยังอยู่แต่เป็นชื่อเก่า ใช้ `/herdr-dissolve --sweep` หรือ `--sync` แทน",
            "- หลายสกิลมีชื่อเครื่องและ user แบบ `nat@white.follow-rankine.ts.net` นี่คือที่อยู่ ssh บน tailnet ไม่ใช่อีเมล",
        ],
        src_h="## 13. ที่มา",
        src=[
            "- คัดลอกจาก `~/.claude/skills/herdr*/` บน m5 วันที่ 8 พ.ย. 2026 (ตามลิงก์ symlink ไปที่ไฟล์จริง)",
            "- {n} สกิล, {f} ไฟล์ข้อความ, SKILL.md รวม {s:,} บรรทัด ทุกไฟล์รวม {l:,} บรรทัด",
            "- ข้าม 1 ไฟล์: `herdr-info/__pycache__/herdr-info.cpython-314.pyc` (binary 35,606 ไบต์) ไม่มีไฟล์เกิน 200 KB",
            "- สแกน secret: `gitleaks detect --no-git --source skills -v` ผล \"no leaks found\" และ rg หา key, token, รหัสผ่าน, อีเมล, เบอร์โทร ไม่เจอค่าจริง ไม่มีการแก้ไขข้อความ ดู [captures/scan.txt](captures/scan.txt)",
            "- วิดีโอ: Screen Recording 3 พ.ย. 2026 21:07:28 (Herdr part 1)",
            "- กลุ่มทั้ง 7 ตรงกับ [แผนที่สกิล herdr](../2026-11-08_herdr-skill-map/README.md)",
            "- ชุด herdr: [แผนที่สกิล](../2026-11-08_herdr-skill-map/README.md) · [worktree ตั้งแต่เกิดจนดับ](../2026-11-08_herdr-wt-lifecycle/README.md) · [พักและปลุก](../2026-11-08_herdr-sleep-wake/README.md) · [bring และ promote](../2026-11-08_herdr-bring-promote/README.md) · [หลายเครื่อง](../2026-11-08_herdr-machines/README.md)",
            "- บทที่เกี่ยวข้อง: [herdr-room](../2026-10-31_herdr-room-lesson/README.md) · [⌘J ⌘L](../2026-11-05_herdr-cmd-j-lesson/README.md) · [ทีม](../2026-11-05_team-ecosystem-lesson/README.md)",
        ],
        count="หน้านี้ยาว {r:,} บรรทัด",
        sign="— AIExpo Oracle (Oracle AI)",
    ),
    "en": dict(
        title="# Every herdr skill, full text",
        summary=("> Lesson 6 of the herdr series: all {n} `/herdr-*` skills exactly as they are on m5 on 8 Nov 2026. "
                 "Every SKILL.md is on this page word for word, and each skill's scripts and other files are in `skills/`: "
                 "{f} files, {l:,} lines in all, scanned for secrets with nothing found. People can read it; an AI can copy it."),
        other="- Other edition: [ไทย (Thai, the original)](README.md)",
        byai="- Written by AIExpo Oracle (AI), not a person",
        intro_h="## 1. What this page is",
        intro=[
            "- Nat, 8 Nov: \"the 6th lesson do write full all skills and content full again one\"",
            "- The other lessons explain which skill to use when; this page is the real thing, all of it, to read or copy",
            "- The skill texts stay in their own language (mostly English); the one-line summary above each skill is written for this page",
            "- Each skill links to `skills/<name>/SKILL.md` and to its other files (scripts, `.bak` copies)",
            "- The map of all 52 with a timeline is in [the herdr skill map](../2026-11-08_herdr-skill-map/README.en.md)",
        ],
        groups_h="## 2. The 7 groups",
        groups_intro="The skills are sorted by job into 7 groups, the same as in the skill map:",
        img_groups_alt="Diagram of the 7 groups of the 52 herdr skills with the skill names in each group",
        install_h="## 3. Install",
        install=[
            "- One skill is one folder. Copy the folder into `~/.claude/skills/` and restart Claude Code",
            "- Call it as `/<folder name>`, for example `/herdr-wt`",
            "- Most skills need to run inside a herdr pane (`HERDR_ENV=1`), and many name Nat's machines (m5, white), repos and oracles; adapt them before using them elsewhere",
            "- `.bak` files are earlier versions kept in the skill folder on m5; you do not need to copy them",
        ],
        install_code="For example:",
        video_h="## 4. In the video",
        video=("On 3 Nov 2026 Nat made two screen recordings (\"Herdr part 1\" and \"Herdr part 2\"). At 21:28 Nat ran "
               "`/herdr-wt demo-hello-world`, then `/herdr-rename`, `/herdr-pr` and `/herdr-dissolve`. "
               "This frame is minute 23:30 of part 1: issue #129 in laris-co/laris-team, which `/herdr-wt` opened by itself before cutting the worktree, "
               "with the sections Rules, Done when, Out of scope, Workspace and the closing line \"Opened by Laris Labs Oracle (AI) via /herdr-wt\". "
               "That text comes from the steps in [skills/herdr-wt/SKILL.md](skills/herdr-wt/SKILL.md)."),
        frame_alt="Frame from the video Herdr part 1: issue #129 opened by /herdr-wt, with Rules, Done when, Out of scope and Workspace sections",
        oneline="What it does:",
        file_link="file",
        extra="Other files in this folder:",
        lines="lines",
        traps_h="## 12. Real traps",
        traps=[
            "- `herdr`, `herdr-soul` and `herdr-work` are symlinks on m5. A plain `cp -r` copies only the link; use `cp -RL` to get the real files",
            "- `herdr-info/__pycache__/` is Python bytecode, not part of the skill; it was not copied",
            "- `herdr-clean-up-sync` still exists but is an old name; use `/herdr-dissolve --sweep` or `--sync`",
            "- Many skills contain `nat@white.follow-rankine.ts.net`-style strings: these are ssh targets on the tailnet, not email addresses",
        ],
        src_h="## 13. Sources",
        src=[
            "- Copied from `~/.claude/skills/herdr*/` on m5 on 8 Nov 2026 (symlinks followed to the real files)",
            "- {n} skills, {f} text files; the SKILL.md files total {s:,} lines, all files {l:,} lines",
            "- Skipped 1 file: `herdr-info/__pycache__/herdr-info.cpython-314.pyc` (binary, 35,606 bytes); no file was over 200 KB",
            "- Secret scan: `gitleaks detect --no-git --source skills -v` said \"no leaks found\", and rg for keys, tokens, passwords, emails and phone numbers found no real values; nothing was redacted. See [captures/scan.txt](captures/scan.txt)",
            "- Video: Screen Recording, 3 Nov 2026 21:07:28 (Herdr part 1)",
            "- The 7 groups match [the herdr skill map](../2026-11-08_herdr-skill-map/README.en.md)",
            "- The herdr series: [skill map](../2026-11-08_herdr-skill-map/README.en.md) · [worktree lifecycle](../2026-11-08_herdr-wt-lifecycle/README.en.md) · [sleep and wake](../2026-11-08_herdr-sleep-wake/README.en.md) · [bring and promote](../2026-11-08_herdr-bring-promote/README.en.md) · [machines](../2026-11-08_herdr-machines/README.en.md)",
            "- Related: [herdr-room](../2026-10-31_herdr-room-lesson/README.en.md) · [⌘J ⌘L](../2026-11-05_herdr-cmd-j-lesson/README.en.md) · [teams](../2026-11-05_team-ecosystem-lesson/README.en.md)",
        ],
        count="This page is {r:,} lines long",
        sign="— AIExpo Oracle (Oracle AI)",
    ),
}


def build(lang):
    t = T[lang]
    one = TH if lang == "th" else EN
    fmt = dict(n=len(all_names), f=len(all_files), l=total_file_lines, s=total_skill_lines)
    out = [t["title"], "", t["summary"].format(**fmt), "", t["other"], t["byai"], "", "---", ""]
    out += [t["intro_h"], ""] + t["intro"] + [""]
    out += [t["groups_h"], "", t["groups_intro"], "", f"![{t['img_groups_alt']}](images/00-seven-groups.png)", ""]
    for i, (key, th, en, names) in enumerate(GROUPS, 5):
        label = th if lang == "th" else en
        out.append(f"- {i}. [{label}](#{i}-{anchor(label)}) ({len(names)}): " + ", ".join(f"`/{n}`" for n in names))
    out.append("")
    out += [t["install_h"], ""] + t["install"] + ["", t["install_code"], "", "```bash",
            "# one skill / สกิลเดียว",
            "cp -RL skills/herdr-wt ~/.claude/skills/",
            "# all of them / ทั้งหมด",
            "cp -RL skills/herdr* ~/.claude/skills/", "```", ""]
    out += [t["video_h"], "", t["video"], "", f"![{t['frame_alt']}](images/01-video-herdr-wt.png)", ""]
    sec = 5
    for key, th, en, names in GROUPS:
        label = th if lang == "th" else en
        out += ["---", "", f"## {sec}. {label}", ""]
        for n in names:
            d = skills / n
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            f = fence_for(text)
            out += [f"### /{n}", "", f"{t['oneline']} {one[n]}", ""]
            if n in NOTE:
                out += [f"> {NOTE[n][lang]}", ""]
            out += [f"- [skills/{n}/SKILL.md](skills/{n}/SKILL.md) ({nlines(d / 'SKILL.md')} {t['lines']})"]
            extras = sorted(p for p in d.rglob("*") if p.is_file() and p.name != "SKILL.md")
            if extras:
                out.append(f"- {t['extra']}")
                for p in extras:
                    rel = p.relative_to(here).as_posix()
                    out.append(f"  - [{p.relative_to(d).as_posix()}]({rel}) ({nlines(p)} {t['lines']})")
            out += ["", f"{f}markdown", text.rstrip("\n"), f, ""]
        sec += 1
    out += ["---", "", t["traps_h"], ""] + t["traps"] + [""]
    out += [t["src_h"], ""] + [s.format(**fmt) for s in t["src"]]
    body_len = len("\n".join(out).splitlines()) + 3
    out += [f"- {t['count'].format(r=body_len)}", "", t["sign"], ""]
    return "\n".join(out)


def anchor(label):
    a = label.lower()
    import unicodedata
    a = "".join(c for c in a if c in "-_ " or unicodedata.category(c)[0] in "LMN")
    return a.replace(" ", "-")


for lang, name in (("th", "README.md"), ("en", "README.en.md")):
    text = build(lang)
    (here / name).write_text(text, encoding="utf-8")
    print(name, len(text.splitlines()), "lines")
print("skills", len(all_names), "files", len(all_files), "skill lines", total_skill_lines, "all lines", total_file_lines)
