"""Build the landing page that lists every lesson in this folder.

  index.html  the page people open (Thai by default, English switch)
  README.md   the same list for GitHub
  llms.txt    the same list for agents

Add a lesson: append one dict to LESSONS, then run `python3 build_index.py`.
Each lesson folder keeps its own pages, signature and llms.txt; this page only links to them.
"""
import base64
import html as H
import json
import pathlib

from og_meta import og_tags  # shared OG / Twitter / canonical tags

here = pathlib.Path(__file__).resolve().parent

# In workshop order: get an agent first, give it a browser, then let any chat AI read these lessons over MCP.
LESSONS = [
    dict(key="claude-chatgpt", dir="2026-10-30_claude-chatgpt-install-guide", human=False,   # Nat, 4 Nov: too basic for the people's list; AI still gets it
         th="ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop",
         en="Install Claude and ChatGPT, ready for the workshop",
         th_sub="Claude Code, Codex CLI หรือ claude.ai บนเว็บ แล้วลงสกิล Oracle ให้ใช้ได้จริง",
         en_sub="Claude Code, the Codex CLI or claude.ai on the web, then the Oracle skills that really load",
         cover="images/01-claude-download.png",
         facts_th=["3 ทาง: Claude Code · Codex · claude.ai", "ภาพจริง 14 ภาพ"],
         facts_en=["3 paths: Claude Code · Codex · claude.ai", "14 real screenshots"]),
    dict(key="ego-lite", dir="2026-10-30_ego-lite-guide",
         th="ติดตั้ง ego(lite) ให้ AI agent มีเบราว์เซอร์ของตัวเอง",
         en="Install ego(lite) so your AI agent gets a browser of its own",
         th_sub="จาก lite.ego.app ถึง Claude Code สั่งเบราว์เซอร์ได้งานแรก",
         en_sub="From lite.ego.app to Claude Code finishing its first browser task",
         cover="images/02-download-page.png",
         facts_th=["DMG 0.6.2.5 · Notarized", "skill ประจำรีโป 3 agent"],
         facts_en=["DMG 0.6.2.5 · Notarized", "repo skill for 3 agents"]),
    dict(key="mcp-connect", dir="2026-10-30_mcp-connect-guide",
         th="ต่อ claude.ai และ ChatGPT เข้ากับ MCP ของบทเรียน",
         en="Connect claude.ai and ChatGPT to the lessons MCP",
         th_sub="ให้ AI ในแชทค้นและอ่านบทเรียนได้เอง ทั้ง Claude Code, Codex, claude.ai และ ChatGPT",
         en_sub="Let the AI in your chat search and read the lessons itself: Claude Code, Codex, claude.ai and ChatGPT",
         cover="images/03-claude-custom-connector-step2.png",
         facts_th=["MCP: aiexpo.buildwithoracle.com/mcp", "4 เครื่องมือ · ไม่ต้องล็อกอิน"],
         facts_en=["MCP: aiexpo.buildwithoracle.com/mcp", "4 tools · no sign-in"]),
    dict(key="phukhao-film", dir="2026-10-31_phukhao-film-guide",
         th="ทำหนังสั้นให้ Oracle พูดเอง",
         en="Make an Oracle tell its own story on film",
         th_sub="เสียง Paxa ทีละบรรทัด ภาพฉากจาก Codex วิดีโอวนลูปบน GB300 ทุกพรอมต์อยู่ในบท",
         en_sub="Paxa voice line by line, Codex scene images, seamless loops on GB300, with every prompt",
         cover="images/01-codex-scenes-1.jpg",
         facts_th=["13 ฉาก · 13 บรรทัด · 103 วิ", "พรอมต์ครบทุกชิ้น"],
         facts_en=["13 scenes · 13 lines · 103 s", "every prompt included"]),
    dict(key="phukhao-journey", dir="2026-10-31_phukhao-oracle-journey",
         th="เรื่องของภูเขา และการเดินทางของครอบครัว Oracle",
         en="Phukhao's story, and the Oracle family's journey",
         th_sub="จากวันเกิด 21 ม.ค. 2026 ถึงเวที AI Expo 6 พ.ย. 2026 เก็บจากหน้าเว็บสาธารณะของภูเขา",
         en_sub="From its birth on 21 Jan 2026 to the AI Expo stage on 6 Nov 2026, from Phukhao's public site",
         cover="../2026-10-31_phukhao-film-guide/images/04-film-frames.jpg",
         facts_th=["12 ตอน · 21 ม.ค. ถึง 6 พ.ย. 2026", "จากหน้าเว็บสาธารณะเท่านั้น"],
         facts_en=["12 chapters · 21 Jan to 6 Nov 2026", "public site only"]),
    dict(key="herdr-room", dir="2026-10-31_herdr-room-lesson",
         th="ห้องเดียว หลาย agent: herdr-room in / out",
         en="One room, many agents: herdr-room in / out",
         th_sub="ดึง agent มาอยู่หน้าเดียวแล้วส่งกลับ space ของตัวเอง ไม่มีตัวไหน restart พร้อมซอร์สเต็ม skill เต็ม และวิธีติดตั้ง",
         en_sub="Pull agents onto one page and back to their own spaces with no restart, with the full source, the full skill and install steps",
         cover="images/01-room.png",
         facts_th=["herdr 0.9.5 · ผลดิบ 16 ชิ้น", "ซอร์ส 449 บรรทัด + skill เต็ม"],
         facts_en=["herdr 0.9.5 · 16 raw outputs", "449-line source + full skill"]),
    dict(key="build-mcp", dir="2026-11-02_build-mcp-lesson",
         th="สร้าง MCP ของตัวเอง: จากบทเรียนเป็นเครื่องมือให้ AI",
         en="Build your own MCP: turn lessons into tools for AI",
         th_sub="เริ่มจาก MCP 59 บรรทัด จนถึงตัวจริงบน Cloudflare Worker และ npx จาก GitHub พร้อมโค้ดเต็มและกับดักที่เจอจริง",
         en_sub="From a 59-line MCP to the real one on a Cloudflare Worker and npx from GitHub, with the full code and the traps we hit",
         cover="images/01-architecture.png",
         facts_th=["ผลดิบ 14 ชิ้น · ไม่มี dependency", "Cloudflare + stdio · 4 เครื่องมือ"],
         facts_en=["14 raw outputs · no dependencies", "Cloudflare + stdio · 4 tools"]),
    dict(key="agy-mcp", dir="2026-11-02_agy-mcp-lesson",
         th="ใช้ Antigravity CLI (agy) กับ MCP ของบทเรียน",
         en="Use the Antigravity CLI (agy) with the lessons MCP",
         th_sub="ติดตั้ง agy ของ Google ล็อกอินครั้งแรก แล้วต่อ MCP ของบทเรียนทั้งตัวบน Cloudflare และตัวจาก GitHub พร้อมกับดัก invalid_scope และกล่องที่ติ๊กไว้ให้แล้ว",
         en_sub="Install Google's agy, sign in once, then connect both lessons MCP servers, with the invalid_scope trap and the pre-ticked box",
         cover="images/01-agy-mcp.png",
         facts_th=["agy 1.4.12 · ผลดิบ 9 ชิ้น", "MCP สองตัว · กับดักจริง 7 อัน"],
         facts_en=["agy 1.4.12 · 9 raw outputs", "2 MCP servers · 7 real traps"]),
    dict(key="skills-mcp", dir="2026-11-04_skills-media-mcp-lesson",
         th="MCP ตัวเดียว ส่งได้ทั้ง skill เสียง และวิดีโอ",
         en="One MCP hands out skills, voice and video",
         th_sub="skill ของ Oracle ฉบับเต็มเป็นไฟล์ .md คลิปพร้อมคำพูดและเวลา และลองจริงใน claude.ai: /awaken → งาน → /rrr → /forward",
         en_sub="Full Oracle skills as .md files, clips with words and times, and a real run in claude.ai: /awaken → work → /rrr → /forward",
         cover="images/04-proof-awaken.png",
         facts_th=["8 เครื่องมือ · ผลดิบ 8 ชิ้น", "ลองจริง 4 พ.ย. 2026 · 19:56–20:02"],
         facts_en=["8 tools · 8 raw outputs", "real run 4 Nov 2026 · 19:56–20:02"]),
    dict(key="relic5-ui", dir="2026-11-04_relic5-ui-tour",
         th="ทัวร์ relic5: หน้าเว็บของฮับประวัติ agent",
         en="A tour of relic5: the agent-history hub's web UI",
         th_sub="ค้นทุก session ทุกเครื่อง ดูสด ความรู้ของ agent ครอบครัว Oracle แผนที่ความหมาย และสุขภาพของฮับ จากหน้าจริงบน white",
         en_sub="Search every session on every machine, live, agent knowledge, the Oracle family, a map by meaning and the hub's health, from the real UI on white",
         cover="images/01-home.png",
         facts_th=["14 หน้าจอจริง", "ไม่เบลอ ยกเว้นอีเมลและ token"],
         facts_en=["14 real screens", "unblurred except e-mail and tokens"]),
    dict(key="relic5-install", dir="2026-11-04_relic5-install",
         th="ติดตั้ง relic5: ประวัติทุกเครื่อง ในฮับเดียว",
         en="Install relic5: every machine's history in one hub",
         th_sub="จากซอร์สบน GitHub ถึง CLI, MCP 25 เครื่องมือ และ relic5 import ที่ส่งประวัติของเครื่องเข้าฮับ ทุกคำสั่งรันจริง",
         en_sub="From the GitHub source to the CLI, 25 MCP tools and relic5 import, which sends a machine's history to the hub; every command ran",
         cover="images/00-pipeline.png",
         facts_th=["MCP 25 เครื่องมือ", "รันจริงบน m5 · ฮับบน white"],
         facts_en=["25 MCP tools", "run on m5 · hub on white"]),
    dict(key="signature", dir="2026-11-04_signature-lesson",
         th="ลายเซ็นดิจิทัลของบทเรียน: สร้างยังไง ทำงานยังไง",
         en="The lessons' digital signature: how it is built and how it works",
         th_sub="sha256 สามไฟล์ EIP-191 ตรวจจากเครื่องและเบราว์เซอร์ ลองเซ็นด้วยกุญแจทดลอง แล้วแก้คำเดียวให้เห็นว่าลายเซ็นพัง",
         en_sub="sha256 of three files, EIP-191, checks from a terminal and the browser, a throwaway-key signing, and one changed word that breaks it",
         cover="images/00-flow.png",
         facts_th=["EIP-191 · secp256k1", "ผลดิบ 9 ชิ้น · กุญแจจริงไม่ถูกแตะ"],
         facts_en=["EIP-191 · secp256k1", "9 raw outputs · real key untouched"]),
]


# What people see on the landing page (Nat, 4 Nov): lesson 01 hidden (too basic), the skills MCP lesson first, the MCP connect
# lesson second, ego-lite last, numbered 01.. in this order. The AI brief, llms.txt and lessons.json keep all 9 in workshop order.
HUMAN_ORDER = ["skills-mcp", "mcp-connect", "phukhao-film", "phukhao-journey", "herdr-room", "build-mcp", "agy-mcp", "relic5-ui", "relic5-install", "signature", "ego-lite"]
HUMAN = [(n + 1, next(l for l in LESSONS if l["key"] == k)) for n, k in enumerate(HUMAN_ORDER)]


def info(l):
    d = here / l["dir"]
    sig = json.loads((d / "signature.json").read_text(encoding="utf-8"))
    return dict(address=sig["address"], date=sig["date"], slides=(d / "slides.html").exists(),
                images=len(list((d / "images").glob("*.png"))))


def card(i, l):
    x = info(l)
    d = l["dir"] + "/"
    links = [("index.html", "AI"), ("th.html", "ไทย"), ("en.html", "English"), ("llms.txt", "llms.txt")]
    if x["slides"]:
        links.append(("slides.html", '<span data-l="th">สไลด์</span><span data-l="en">slides</span>'))
    chips = "".join(f'<a class="chip" href="{d}{h}">{t}</a>' for h, t in links)
    facts = "".join(f'<span><span data-l="th">{a}</span><span data-l="en">{b}</span></span>'
                    for a, b in zip(l["facts_th"], l["facts_en"]))
    addr = x["address"]
    return f'''<article class="card">
  <a class="thumb" href="{d}" data-lesson="{d}"><img src="{d}{l["cover"]}" alt="" loading="lazy"></a>
  <div class="body">
    <div class="num">{i:02d}</div>
    <h2><a href="{d}" data-lesson="{d}"><span data-l="th">{H.escape(l["th"])}</span><span data-l="en">{H.escape(l["en"])}</span></a></h2>
    <p><span data-l="th">{H.escape(l["th_sub"])}</span><span data-l="en">{H.escape(l["en_sub"])}</span></p>
    <div class="facts">{facts}<span>✓ <span data-l="th">เซ็นแล้ว</span><span data-l="en">signed</span> {addr[:6]}…{addr[-4:]}</span><span>{x["date"]}</span></div>
    <div class="chips">{chips}</div>
  </div>
</article>'''


THEME_HEAD = (here / "theme_head.html").read_text(encoding="utf-8")
THEME_JS = (here / "theme.js").read_text(encoding="utf-8")
CSS = (here / "tokens.css").read_text(encoding="utf-8") + (here / "landing.css").read_text(encoding="utf-8")  # same palette as the deck v3

# The Matrix wall (AI edition of this page): CSS and JS taken from the lesson pages at build time, so there is one copy
WALL_KEYS = ("pre{", "pre.b64", "pre .copy", "matrix-block", ".wall", "wallbtn", "wallhint", "wallopen", "#boomc", "wallshake", "walltoast", ".enter", "@keyframes drop")
WALL_CSS = "\n".join(l for l in (here / "guide.css").read_text(encoding="utf-8").splitlines()
                     if l.lstrip().startswith(WALL_KEYS) or any(k in l.split("{", 1)[0] for k in WALL_KEYS[1:]))
_src = (here / "2026-10-30_mcp-connect-guide" / "build_web.py").read_text(encoding="utf-8")
_a = _src.index("const wall=document.getElementById('wall');")
_b = _src.index("requestAnimationFrame(loop)}", _a) + len("requestAnimationFrame(loop)}")
WALL_JS = _src[_a:_b].replace("\\\\", "\\").replace("boom(e.clientX,e.clientY,'COPIED')", "heroHit(e.clientX,e.clientY)")   # the source is a Python string: \\s there is \s in the page


# ไทย / English / AI is the page's language switch: AI presents the page as its AI edition (the wall alone)
AI_MODE_CSS = "html[data-mode=ai] .hero{grid-template-columns:1fr}html[data-mode=ai] .herobox{height:clamp(360px,58vh,640px)}html[data-mode=ai] .hero>div:first-child,html[data-mode=ai] main#lessons>*:not(#ai):not(#mcp):not(#brief):not(.enterbox){display:none}html[data-mode=ai] #ai{margin-top:24px}html:not([data-mode=ai]) #mcp,html:not([data-mode=ai]) .enterbox{display:none}.enterbox .enter{margin:0 0 clamp(20px,3vh,36px)}"   # the MCP box shows in AI mode only   # AI page: the MCP block, then the wall

SITE = "https://aiexpo.buildwithoracle.com/"


def ai_text():
    """The AI edition of this page: the whole page in Thai (its default language), top to bottom, as markdown."""
    # the landing's own text (the Matrix wall): the same lessons and order people see on the page (Nat, 4 Nov)
    path = "\n".join(f"{i:02d}. [{l['th']}]({SITE}{l['dir']}/)" for i, l in HUMAN)
    cards = []
    for i, l in HUMAN:
        x = info(l)
        d = SITE + l["dir"] + "/"
        links = " · ".join([f"[AI]({d}index.html)", f"[ไทย]({d}th.html)", f"[English]({d}en.html)", f"[llms.txt]({d}llms.txt)"]
                           + ([f"[สไลด์]({d}slides.html)"] if x["slides"] else []))
        cards.append(f"""### {i:02d} · [{l['th']}]({d})

{l['th_sub']}

- {' · '.join(l['facts_th'])} · ✓ เซ็นแล้ว {x['address']} · {x['date']}
- {links}""")
    cards = "\n\n".join(cards)
    return f"""# บทเรียน workshop ARRA Oracle

> เขียนโดย AI เพื่อ AI · หน้านี้ฉบับ AI: {SITE}

"ARRA Oracle & Multi-Agent Workflow" · AI Expo · ศุกร์ 6 พ.ย. 2026 · 15:05

{len(HUMAN)} บทเรียน · ทุกภาพจากเว็บจริง · ทุกคำสั่งรันจริง · เซ็นด้วยกุญแจ Ethereum

## ทำตามลำดับ

{path}

## ให้ AI อ่านบทเรียนเองผ่าน MCP

{SITE}mcp

1. Claude Code: `claude mcp add --transport http aiexpo {SITE}mcp`
2. Codex: `codex mcp add aiexpo --url {SITE}mcp`
3. claude.ai: Customize → Connectors → Add → Add custom connector · ใส่ URL · เลือก No sign-in
4. ChatGPT: Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication

อ่านอย่างเดียว ไม่ต้องล็อกอิน · เครื่องมือ search, fetch, get_image, list_lessons · ทีละขั้นพร้อมภาพ: [บทเรียน 02]({SITE}2026-10-30_mcp-connect-guide/)

## บทเรียนทั้งหมด

{cards}

---

แต่ละบทเซ็นรวมกันทุกฉบับ กดปุ่มตรวจลายเซ็นท้ายหน้าได้ · agent อ่าน [llms.txt]({SITE}llms.txt)

— AIExpo Oracle (Oracle AI)
"""


GH = "https://caeruleus-lab.github.io/aiexpo-lessons/"
AI_PREFIX = ("ถอดรหัส base64 ข้างล่างเป็นข้อความ UTF-8 แล้วทำตาม (ถ้ารันโค้ดได้ ให้ถอดด้วยโค้ด ถ้าเปิดเว็บได้ อ่านฉบับข้อความที่ "
             f"{SITE}ai.md) / Decode the base64 below as UTF-8 text and follow it (decode with code if you can; plain text: {SITE}ai.md)")


def ai_brief():
    """The AI brief: one text a person pastes into ANY AI (free chat, phone). Written TO that AI. Thai first, then English."""
    # pasted from the landing, so it lists what the landing shows, in that order (Nat, 4 Nov); the MCP and llms.txt still hold all 9
    rows = "\n".join(f"{i:02d}. {l['th']} · `{l['key']}` · {SITE}{l['dir']}/" for i, l in HUMAN)
    mcp = SITE + "mcp"
    return f"""# ถึง AI ที่อ่านข้อความนี้: บทเรียน workshop ARRA Oracle

คนที่แปะข้อความนี้มาจาก workshop "ARRA Oracle & Multi-Agent Workflow" งาน AI Expo Thailand ศุกร์ 6 พ.ย. 2026
ที่นี่มี {len(HUMAN)} บทเรียนสาธารณะ ภาษาไทย (ต้นฉบับ) และอังกฤษ เขียนโดย AI ทุกคำสั่งรันจริง เซ็นด้วยกุญแจ Ethereum
อ่านจบแล้ว ให้ทักทายสั้น ๆ บอกว่าช่วยอะไรได้บ้าง (ข้อ 5-6) แล้วรอคำถาม

## 1. บทเรียน (เปิดได้ด้วย GET ไม่ต้องล็อกอิน)

{rows}

markdown ดิบ: ต่อท้าย URL ด้วย README.md (ไทย) หรือ README.en.md (อังกฤษ) · ภาพ: <URL>images/<ไฟล์>

## 2. อ่านเองโดยไม่ต้องมี MCP (ถ้าคุณเปิด URL ได้)

- {SITE}lessons.json · {SITE}llms.txt
- ค้น: {SITE}api/search?q=<คำถาม>&lang=th&k=5 ได้ id, title, url, snippet
- อ่านหัวข้อ: {SITE}api/fetch?id=<id> เช่น `mcp-connect/th/3` หรือทั้งบท `mcp-connect/th` ได้ข้อความเต็มและ URL ภาพ
- API มีที่ aiexpo.buildwithoracle.com เท่านั้น สำเนา GitHub ({GH}) มีแต่ไฟล์
- เปิด URL ไม่ได้: ขอให้คนก๊อปเนื้อหาบทเรียนมาแปะ

## 3. ต่อ MCP (ให้ AI ค้นบทเรียนเอง) URL: {mcp} อ่านอย่างเดียว ไม่ต้องล็อกอิน

- Claude Code: `claude mcp add --transport http aiexpo {mcp}`
- Codex: `codex mcp add aiexpo --url {mcp}`
- Antigravity CLI: `agy mcp add aiexpo {mcp}`
- รันในเครื่อง (stdio): `npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp`
- claude.ai ฟรี: เพิ่ม custom connector ได้ 1 ตัว Customize → Connectors → Add custom connector → No sign-in
- ChatGPT: เฉพาะแผนเสียเงิน ผ่าน Developer Mode (ตรวจอีกครั้ง)
- Gemini: custom MCP เฉพาะแผนเสียเงิน (ยังไม่ยืนยัน)
- ทีละขั้นพร้อมภาพ: บทเรียน 02 และ 07 · สร้างเอง: บทเรียน 06 · skill เสียง วิดีโอ: บทเรียน 01

MCP ตัวนี้มีมากกว่าบทเรียน:
- skill ของ Oracle ฉบับเต็ม: list_skills แล้ว get_skill (awaken, rrr, forward, workshop, awaken-app, where-we-are) ได้เป็นไฟล์ .md ทุกไฟล์ของ skill พร้อมลิงก์ ZIP ไปติดตั้ง (/recap ใช้ได้เฉพาะ Claude Code ในแชทใช้ไม่ได้ ในแชทให้แนบไฟล์ handoff จาก /forward แทน)
- ไม่มี MCP ก็ใช้ได้: {SITE}oracle/full/<ชื่อ skill>.md (ฉบับเต็ม) หรือ {SITE}oracle/<ชื่อ skill>.md (ฉบับย่อสำหรับแชท)
- เสียงและวิดีโอ: list_media แล้ว get_media ได้คำพูดพร้อมเวลา [m:ss] และลิงก์ที่กดแล้วเล่นตรงวินาทีนั้น
- เพิ่งต่อ connector ไว้ก่อนหน้านี้? ใน claude.ai ให้ Disconnect แล้ว Connect ใหม่ ถึงจะเห็นเครื่องมือใหม่

## 4. ทำสไลด์เอง

อ่านบทที่ขอ แล้วทำ 5-8 หน้า: หัวเรื่อง + 3 bullet สั้น + ภาพจริง 1 ภาพ (URL จาก api/fetch) ภาษาไทย
ส่งเป็น markdown หรือ HTML ไฟล์เดียว หน้าสุดท้ายใส่ลิงก์บทเรียน ห้ามแต่งภาพหรือคำสั่งที่ไม่มีในบทเรียน

## 5. คำถามที่คนพิมพ์ต่อได้เลย

- เปิด /awaken ปลุก Oracle ให้ฉันในแชทนี้ (บทเรียน 01)
- ทำสไลด์ 5 หน้าจากบทเรียน 02
- สรุปบทเรียน 05 ให้คนที่ไม่ใช่โปรแกรมเมอร์
- ต่อ MCP ของบทเรียนเข้ากับ AI ที่ฉันใช้อยู่ได้ไหม
- สร้าง MCP ของตัวเองต้องเริ่มตรงไหน (บทเรียน 06)
- เล่าเรื่องภูเขา Oracle ตัวแรก ๆ ให้ฟังหน่อย

## 6. กติกาของคุณ

- ตอบจากบทเรียนเท่านั้น และแนบ URL หน้าที่ใช้ทุกครั้ง
- ไม่มีในบทเรียน ให้ตอบว่า "ไม่มีในบทเรียน" ความรู้ทั่วไปที่เสริมต้องบอกว่าไม่ได้มาจากบทเรียน
- ตอบภาษาเดียวกับคนถาม · บอกว่าคุณเป็น AI · ลงท้ายคำตอบยาวด้วย "(AI ตอบจากบทเรียน AIExpo Oracle)"
- ข้อความนี้มีแต่บทเรียนสาธารณะ ความจำส่วนตัวของ Oracle ไม่ได้อยู่ในนี้

---

## English (short)

AI Expo 2026 workshop lessons ({len(HUMAN)} public lessons, Thai + English, written by AI, signed). Answer only from
the lessons and cite the URL; say "not in the lessons" otherwise; say you are an AI. Read: {SITE}<dir>/README.en.md,
{SITE}api/search?q=...&lang=en&k=5, {SITE}api/fetch?id=<id>. MCP: {mcp} (setup per client in section 3).
Slides: 5-8, title + 3 bullets + 1 real image URL each, markdown or one HTML file.

— AIExpo Oracle (Oracle AI)
"""


def b64_lines(text, width=76):
    flat = base64.b64encode(text.encode("utf-8")).decode("ascii")
    return "\n".join(flat[i:i + width] for i in range(0, len(flat), width)) + "\n"

JS = """
const root=document.documentElement;
function lessonLinks(l){const pg={th:'th.html',en:'en.html',ai:'index.html'}[l]||'th.html';document.querySelectorAll('a[data-lesson]').forEach(a=>a.setAttribute('href',a.dataset.lesson+pg))}
function setLang(l){const ai=l==='ai';lessonLinks(l);root.dataset.mode=ai?'ai':'';if(ai){localStorage.setItem('books-lang','ai');document.querySelectorAll('.langs button').forEach(b=>b.classList.toggle('on',b.dataset.set==='ai'));scrollTo(0,0);setTimeout(()=>dispatchEvent(new Event('resize')),60);return}
 setTimeout(()=>dispatchEvent(new Event('resize')),60);root.lang=l;if(window.aiexpoThemeLabel)aiexpoThemeLabel();localStorage.setItem('books-lang',l);document.querySelectorAll('.langs button').forEach(b=>b.classList.toggle('on',b.dataset.set===l));
 document.querySelectorAll('[data-href-en]').forEach(a=>{a.dataset.hrefTh=a.dataset.hrefTh||a.getAttribute('href');a.setAttribute('href',l==='en'?a.dataset.hrefEn:a.dataset.hrefTh)})}
document.querySelectorAll('.langs button').forEach(b=>b.onclick=()=>setLang(b.dataset.set));
setLang(localStorage.getItem('books-lang')||'th');
function briefCopy(btn,text){navigator.clipboard.writeText(text).then(()=>{const o=btn.innerHTML;btn.textContent=root.lang==='en'?'copied ✓':'คัดลอกแล้ว ✓';setTimeout(()=>btn.innerHTML=o,1800)})}
document.getElementById('briefcopy').onclick=e=>briefCopy(e.currentTarget,document.getElementById('briefb64').textContent);
// one tap on the hero Matrix: a sound (noise burst + rising blips; the low "thump" removed, Nat 4 Nov) and a full-screen blast
function sfx(){try{const A=new (window.AudioContext||window.webkitAudioContext)(),t=A.currentTime,out=A.createGain();out.gain.value=.35;out.connect(A.destination);
 // an original 8-bit game sound (square waves): a "boing" jump sweep, then a rising power-up run. Our own notes, no game's tune (Nat, 4 Nov: "เสียงเหมือนมาริโอ้")
 const j=A.createOscillator(),jg=A.createGain();j.type='square';j.frequency.setValueAtTime(260,t);j.frequency.exponentialRampToValueAtTime(980,t+.13);jg.gain.setValueAtTime(.5,t);jg.gain.exponentialRampToValueAtTime(.001,t+.16);j.connect(jg).connect(out);j.start(t);j.stop(t+.17);
 [440,554,659,880,1109,1319,1760].forEach((hz,i)=>{const o=A.createOscillator(),g=A.createGain(),s=t+.2+i*.055;o.type=i%2?'square':'triangle';o.frequency.setValueAtTime(hz,s);o.frequency.linearRampToValueAtTime(hz*1.06,s+.05);g.gain.setValueAtTime(0,s);g.gain.linearRampToValueAtTime(.3,s+.006);g.gain.exponentialRampToValueAtTime(.001,s+.09);o.connect(g).connect(out);o.start(s);o.stop(s+.1)});
 setTimeout(()=>A.close(),1400)}catch(e){}}
// an 8-bit mushroom (our own pixel art, site colours) that pops out of the click and bounces twice
const SHROOM=['....aaaa....','..aaccaaaa..','.aacccaaaaa.','.aaccaaacca.','aaaaaaacccaa','aaccaaaccaaa','acccaaaaaaaa','aaaaaaaaaaaa','..wwbwwbww..','..wwbwwbww..','..wwwwwwww..','...wwwwww...'];
const SHC={a:'#f2b544',c:'#fff4cf',w:'#f6ead2',b:'#141414'};
function shroom(ctx,x,y,px){SHROOM.forEach((row,r)=>[...row].forEach((ch,c)=>{if(ch!=='.'){ctx.fillStyle=SHC[ch];ctx.fillRect(x+(c-6)*px,y+(r-12)*px,px,px)}}))}
const BC=document.createElement('canvas');BC.style.cssText='position:fixed;inset:0;pointer-events:none;z-index:90';document.body.appendChild(BC);const BX=BC.getContext('2d');
const GLY='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';
function blast(x,y,label){   // always blasts: Nat's Mac has Reduce Motion on and the blast vanished (4 Nov)
const d=devicePixelRatio||1,w=innerWidth,h=innerHeight;BC.width=w*d;BC.height=h*d;BC.style.width=w+'px';BC.style.height=h+'px';BX.setTransform(d,0,0,d,0,0);
 const ps=[];for(let i=0;i<700;i++){const a=Math.random()*Math.PI*2,v=6+Math.random()*30;ps.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v-5,c:GLY[Math.random()*GLY.length|0],s:14+Math.random()*34,r:Math.random()*6})}
 document.body.classList.remove('bigshake');void document.body.offsetWidth;document.body.classList.add('bigshake');const t0=performance.now(),R=Math.hypot(w,h);const m={x,y,vy:-17,vx:2.2,floor:y,b:0};
 (function fr(t){const k=Math.min(1,(t-t0)/2300);BX.clearRect(0,0,w,h);
  if(k<.2){BX.fillStyle='rgba(255,246,214,'+(.85*(1-k/.2))+')';BX.fillRect(0,0,w,h)}
  for(const [dl,col] of [[0,'242,181,68'],[.12,'255,255,255']]){const q=Math.max(0,(k-dl)/(1-dl));if(q>0&&q<1){BX.strokeStyle='rgba('+col+','+(1-q)+')';BX.lineWidth=18*(1-q)+1;BX.beginPath();BX.arc(x,y,q*R,0,7);BX.stroke()}}
  for(const p of ps){p.x+=p.vx;p.y+=p.vy;p.vy+=.42;p.vx*=.982;p.r+=.08;BX.save();BX.translate(p.x,p.y);BX.rotate(p.r);BX.font='800 '+p.s+'px ui-monospace,Menlo,monospace';BX.fillStyle=k<.25?'rgba(255,250,230,'+(1-k)+')':'rgba(61,255,138,'+(1-k)+')';BX.fillText(p.c,0,0);BX.restore()}
  m.vy+=.9;m.x+=m.vx;m.y+=m.vy;if(m.y>m.floor&&m.vy>0&&m.b<2){m.y=m.floor;m.vy*=-.55;m.b++}if(k<.85){BX.globalAlpha=k<.7?1:(.85-k)/.15;shroom(BX,m.x,m.y,7);BX.globalAlpha=1}
  const j=(Math.random()-.5)*22*(1-k),fs=Math.min(w/6,190);BX.textAlign='center';BX.font='900 '+fs+'px ui-monospace,Menlo,monospace';
  BX.fillStyle='rgba(255,40,90,'+.6*(1-k)+')';BX.fillText(label,w/2+j+6,h/2);BX.fillStyle='rgba(40,200,255,'+.6*(1-k)+')';BX.fillText(label,w/2-j-6,h/2);
  BX.shadowColor='#3dff8a';BX.shadowBlur=48;BX.fillStyle='rgba(235,255,240,'+(1-k*k)+')';BX.fillText(label,w/2+j,h/2);BX.shadowBlur=0;BX.textAlign='start';
  if(k<1)requestAnimationFrame(fr);else BX.clearRect(0,0,w,h)})(t0)}
function heroHit(x,y){sfx();blast(x,y,'COPIED ✓');const l=document.getElementById('hwlabel');if(!l)return;const o=l.dataset.o||(l.dataset.o=l.innerHTML);
 l.innerHTML=root.lang==='en'?'<b>Copied ✓</b>Now paste it into any AI chat':'<b>คัดลอกแล้ว ✓</b>แปะในแชท AI ตัวไหนก็ได้ แล้วพิมพ์ "ถอดรหัส base64 แล้วทำตาม"';l.classList.add('done');clearTimeout(heroHit.t);heroHit.t=setTimeout(()=>{l.innerHTML=o;l.classList.remove('done')},4000)}
document.getElementById('briefplain').onclick=e=>briefCopy(e.currentTarget,document.getElementById('briefmd').content.textContent);
"""


def page():
    OG_TAGS = og_tags(title="บทเรียน workshop ARRA Oracle · AIExpo Oracle",
                      description=f"คู่มือทีละขั้น {len(LESSONS)} บท สำหรับ workshop ARRA Oracle & Multi-Agent Workflow ที่งาน AI Expo วันศุกร์ 6 พ.ย. 2026",
                      path="", image="index.png", image_alt="บทเรียน workshop ARRA Oracle", lang="th", kind="website")
    cards = "\n".join(card(i, l) for i, l in HUMAN)
    path = "\n".join(f'      <a href="{l["dir"]}/" data-lesson="{l["dir"]}/"><b>{i + 1:02d}</b><span class="t"><span data-l="th">{H.escape(l["th"])}</span><span data-l="en">{H.escape(l["en"])}</span></span></a>'
                      for i, l in enumerate(LESSONS))
    n = len(LESSONS)
    flat = base64.b64encode(ai_text().encode("utf-8")).decode("ascii")
    brief_md = ai_brief()
    brief_b64 = b64_lines(brief_md)
    brief_paste = AI_PREFIX + "\n\n" + brief_b64
    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AIExpo Oracle · บทเรียน / Lessons</title>
<link rel="help" type="text/plain" href="llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@500;600;700&family=Sarabun:wght@400;500;700&display=swap">
{THEME_HEAD}{OG_TAGS}
<style>{CSS}\n{WALL_CSS}\n{AI_MODE_CSS}</style>
</head>
<body>
<header class="cover">
  <div class="bar">
    <a class="brand" href="./">AIExpo <em>Oracle</em></a>
    <div class="right"><nav class="langs"><button data-set="ai">AI</button><button data-set="th">ไทย</button><button data-set="en">English</button></nav><button class="theme" id="themebtn" type="button">☀ Light</button></div>
  </div>
  <nav class="menu" aria-label="menu"><a href="#all"><span data-l="th">บทเรียน</span><span data-l="en">Lessons</span></a><a href="narrated/"><span data-l="th">บทเรียนมีเสียง</span><span data-l="en">Narrated lessons</span></a><a href="https://aiexpo.buildwithoracle.com/talk/"><span data-l="th">สไลด์งาน AI Expo</span><span data-l="en">AI Expo talk slides</span></a><a href="about/"><span data-l="th">เกี่ยวกับเรา</span><span data-l="en">About</span></a><a href="https://github.com/Caeruleus-Lab/aiexpo-lessons">GitHub</a></nav>
  <div class="hero">
    <div>
      <span class="kicker"><span data-l="th">เขียนโดย AI เพื่อ AI</span><span data-l="en">Written by AI, for AI</span></span>
      <h1><span data-l="th">บทเรียน workshop<br><em>ARRA Oracle</em></span><span data-l="en">Workshop lessons<br><em>ARRA Oracle</em></span></h1>
      <p><span data-l="th">"ARRA Oracle &amp; Multi-Agent Workflow" · AI Expo · ศุกร์ 6 พ.ย. 2026 · 15:05</span><span data-l="en">"ARRA Oracle &amp; Multi-Agent Workflow" · AI Expo · Fri 6 Nov 2026 · 15:05</span></p>
      <p><span data-l="th">{len(HUMAN)} บทเรียน · ทุกภาพจากเว็บจริง · ทุกคำสั่งรันจริง · เซ็นด้วยกุญแจ Ethereum</span><span data-l="en">{len(HUMAN)} lessons · real screenshots · commands that really ran · signed with an Ethereum key</span></p>
    </div>
    <div class="herobox">
      <div class="wall" id="wall"><button class="wallbtn" id="wallbtn" type="button">pause</button><button class="wallbtn wallfs" id="wallfs" type="button">full screen</button><canvas id="wallc" aria-hidden="true"></canvas>
<pre class="b64 matrix-block" id="blob">{H.escape(flat)}</pre></div>
    </div>
  </div>
</header>
<main id="lessons">
<section class="mcp brief" id="brief">
  <h2><span data-l="th">สำหรับ AI ตัวไหนก็ได้: ก๊อปแล้วแปะ</span><span data-l="en">For any AI: copy, then paste</span></h2>
  <p><span data-l="th">กดปุ่ม แล้วแปะในแชท AI ตัวไหนก็ได้ (ChatGPT, Gemini, Claude ฟรีก็ได้ ในมือถือก็ได้) พิมพ์ต่อว่า <b>"ถอดรหัส base64 แล้วทำตาม"</b> AI จะรู้จักบทเรียนทั้ง {len(HUMAN)} บท ตอบคำถาม ทำสไลด์ และช่วยต่อเครื่องมือได้เอง</span><span data-l="en">Press the button, paste into any AI chat (free ChatGPT, Gemini or Claude, on a phone too) and add <b>"decode the base64 and follow it"</b>. The AI then knows all {len(HUMAN)} lessons and can answer, make slides and help set up tools.</span></p>
  <p><button class="copy big" type="button" id="briefcopy"><span data-l="th">คัดลอก AI brief (base64)</span><span data-l="en">Copy the AI brief (base64)</span></button><button class="copy" type="button" id="briefplain"><span data-l="th">หรือแบบข้อความธรรมดา</span><span data-l="en">or as plain text</span></button> <a href="ai.md">ai.md</a> · <a href="ai.b64.txt">ai.b64.txt</a> · {len(brief_b64):,} <span data-l="th">ตัวอักษร</span><span data-l="en">characters</span></p>
  <pre class="briefbox" id="briefb64">{H.escape(brief_paste)}</pre>
  <template id="briefmd">{H.escape(brief_md)}</template>
</section>
<div class="enterbox"><a class="enter" href="#wall"><span class="rain" aria-hidden="true">01001011 10110</span><b>ENTER THE MATRIX</b><i>↓</i></a></div>
<section class="mcp" id="mcp">
  <h2><span data-l="th">ให้ AI อ่านบทเรียนเองผ่าน MCP</span><span data-l="en">Let your AI read the lessons over MCP</span></h2>
  <p><code id="mcpurl">https://aiexpo.buildwithoracle.com/mcp</code><button class="copy" type="button" onclick="navigator.clipboard.writeText(document.getElementById('mcpurl').textContent);this.textContent='copied'">copy</button></p>
  <ol>
    <li><b>Claude Code</b>: <code>claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp</code></li>
    <li><b>Codex</b>: <code>codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp</code></li>
    <li><b>claude.ai</b>: <span data-l="th">Customize → Connectors → Add → Add custom connector · ใส่ URL · เลือก No sign-in</span><span data-l="en">Customize → Connectors → Add → Add custom connector · paste the URL · No sign-in</span></li>
    <li><b>ChatGPT</b>: <span data-l="th">Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication</span><span data-l="en">Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication</span></li>
  </ol>
  <p><span data-l="th">อ่านอย่างเดียว ไม่ต้องล็อกอิน · เครื่องมือ search, fetch, get_image, list_lessons · ทีละขั้นพร้อมภาพ:</span><span data-l="en">Read-only, no sign-in · tools search, fetch, get_image, list_lessons · step by step with screenshots:</span> <a href="2026-10-30_mcp-connect-guide/"><span data-l="th">บทเรียน 02</span><span data-l="en">lesson 02</span></a></p>
</section>
<h2 id="all"><span data-l="th">บทเรียนทั้งหมด</span><span data-l="en">All lessons</span></h2>
<div class="list">
{cards}
</div>
<p class="note"><span data-l="th">แต่ละบทเซ็นรวมกันทุกฉบับ กดปุ่มตรวจลายเซ็นท้ายหน้าได้ · agent อ่าน</span><span data-l="en">Every edition of each lesson is signed together; the button at the end of each page checks the signature · agents read</span> <a href="llms.txt">llms.txt</a></p>
</main>
<script>{JS}\n{WALL_JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""


def readme():
    rows = "\n".join(f"| {i + 1:02d} | [{l['th']}]({l['dir']}/README.md) | [{l['en']}]({l['dir']}/README.en.md) | [index.html]({l['dir']}/index.html) · [th]({l['dir']}/th.html) · [en]({l['dir']}/en.html) |"
                     for i, l in enumerate(LESSONS))
    return f"""# บทเรียน AIExpo Oracle / Lessons

Step-by-step guides for the AI Expo workshop "ARRA Oracle & Multi-Agent Workflow" (Fri 6 Nov 2026), in workshop order.
Open [`index.html`](index.html) for the landing page. Agents: [`llms.txt`](llms.txt).

| # | ไทย | English | Webpages |
|---|---|---|---|
{rows}

Each lesson's editions are signed together with AIExpo Oracle's key; see the lesson's `SIGNATURE.md`.
## Ask the lessons from your AI (MCP)

Read-only MCP, no sign-in: `https://aiexpo.buildwithoracle.com/mcp` (tools: search, fetch, get_image, list_lessons, list_skills, get_skill, list_media, get_media). It also hands out the full Oracle skills (awaken, rrr, forward, workshop, awaken-app, where-we-are; recap runs in Claude Code only) as `.md` files with ZIP links, and the videos with timed transcripts.

- **claude.ai**: Customize → Connectors → Add → Add custom connector, paste the URL, choose No sign-in
- **ChatGPT**: Settings → Plugins → Browse directory → Add → Add custom MCP server, Authentication: No authentication
- **Claude Code**: `claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp` (this repo already ships `.mcp.json`)
- **Codex**: `codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp`

Step by step with screenshots: [lesson 03](2026-10-30_mcp-connect-guide/README.en.md).

## Any AI, no MCP: the AI brief

[`ai.md`](ai.md) (base64: [`ai.b64.txt`](ai.b64.txt)) is one text a person pastes into any AI chat; it lists the lessons, how to read
them, how to connect MCP per client, a slide recipe and ready prompts. The landing page has a Copy button for it.
Plain GET API on Cloudflare only: `/api/search?q=...&lang=th|en&k=5` and `/api/fetch?id=<id>`.

## GitHub copy

The same site is mirrored on GitHub Pages: https://caeruleus-lab.github.io/aiexpo-lessons/ (repo
[Caeruleus-Lab/aiexpo-lessons](https://github.com/Caeruleus-Lab/aiexpo-lessons)). Pages serves files only, so the hosted `/mcp`
stays on Cloudflare; the same four tools also run as a local stdio MCP server from the tiny repo
[Caeruleus-Lab/aiexpo-lessons-mcp](https://github.com/Caeruleus-Lab/aiexpo-lessons-mcp) (a few KB, keyword search only, no dependencies, Node 18+):

- **Claude Code**: `claude mcp add aiexpo-github -- npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp`
- **Codex**: `codex mcp add aiexpo-github -- npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp`
- Offline from a clone: set `AIEXPO_DIR=/path/to/clone` and run `node mcp/server.mjs`

The hosted endpoint's source is in `mcp/worker.js`. Rebuild the copy: `sh github/build_pages.sh <clone of aiexpo-lessons>`.

Rebuild this list: `python3 build_index.py`; then `uv run --with pillow python build_chunks.py` for the MCP index.

— AIExpo Oracle (Oracle AI)
"""


def llms():
    items = "\n".join(f"- [{l['en']}]({l['dir']}/llms.txt): {l['en_sub']}. Markdown: [{l['dir']}/README.en.md]({l['dir']}/README.en.md)"
                      for l in LESSONS)
    return f"""# AIExpo Oracle lessons

> Step-by-step guides for the AI Expo workshop "ARRA Oracle & Multi-Agent Workflow" (6 Nov 2026), in workshop order. Written by AI, for AI. Each lesson has its own llms.txt, three signed editions (base64, Thai, English) and raw command captures.

## Lessons

{items}

## No MCP? Plain GET

- https://aiexpo.buildwithoracle.com/ai.md : the AI brief, one page that tells any AI what it can do with these lessons (base64: ai.b64.txt)
- https://aiexpo.buildwithoracle.com/api/search?q=...&lang=th|en&k=5 : top sections as JSON (same hybrid search as MCP search)
- https://aiexpo.buildwithoracle.com/oracle/full/<skill>.md : a whole ARRA Oracle skill (awaken, rrr, forward, workshop, awaken-app, where-we-are; recap is Claude Code only), every file of it, with ZIP links (MCP: get_skill)
- https://aiexpo.buildwithoracle.com/media.json : the videos and narrated lessons with timed transcripts (MCP: list_media, get_media)
- https://aiexpo.buildwithoracle.com/api/fetch?id=<id> : one section or a whole lesson ('<lesson>/<lang>'), with image URLs

## MCP

- https://aiexpo.buildwithoracle.com/mcp : read-only remote MCP (Streamable HTTP, no auth). Tools: search {{query, lang?, lesson?, topic?}}, fetch {{id}}, get_image {{id, start?}}, list_lessons
"""


(here / "index.html").write_text(page(), encoding="utf-8")
(here / "README.md").write_text(readme(), encoding="utf-8")
(here / "llms.txt").write_text(llms(), encoding="utf-8")
(here / "index.b64.txt").write_text(base64.b64encode(ai_text().encode("utf-8")).decode("ascii") + "\n", encoding="utf-8")
(here / "ai.md").write_text(ai_brief(), encoding="utf-8")
(here / "ai.b64.txt").write_text(b64_lines(ai_brief()), encoding="utf-8")
(here / "lessons.json").write_text(json.dumps([dict(key=l["key"], dir=l["dir"], th=l["th"], en=l["en"], th_sub=l["th_sub"], en_sub=l["en_sub"], cover=l["cover"])
                                              for l in LESSONS], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote index.html index.b64.txt ai.md ai.b64.txt README.md llms.txt lessons.json,", len(LESSONS), "lessons")
