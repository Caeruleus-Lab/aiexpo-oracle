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
    dict(key="claude-chatgpt", dir="2026-10-30_claude-chatgpt-install-guide",
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
         th_sub="ให้ AI ในแชทค้นและอ่านบทเรียนได้เอง ทั้ง claude.ai, ChatGPT, Claude Code และ Codex",
         en_sub="Let the AI in your chat search and read the lessons itself: claude.ai, ChatGPT, Claude Code and Codex",
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
]


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
WALL_JS = _src[_a:_b].replace("\\\\", "\\")   # the source is a Python string: \\s there is \s in the page


# ไทย / English / AI is the page's language switch: AI presents the page as its AI edition (the wall alone)
AI_MODE_CSS = "html[data-mode=ai] .hero,html[data-mode=ai] main#lessons>*:not(#ai):not(#mcp):not(.enterbox){display:none}html[data-mode=ai] #ai{margin-top:24px}html:not([data-mode=ai]) #mcp,html:not([data-mode=ai]) .enterbox{display:none}.enterbox .enter{margin:0 0 clamp(20px,3vh,36px)}"   # the MCP box shows in AI mode only   # AI page: the MCP block, then the wall

SITE = "https://aiexpo.buildwithoracle.com/"


def ai_text():
    """The AI edition of this page: the whole page in Thai (its default language), top to bottom, as markdown."""
    path = "\n".join(f"{i + 1:02d}. [{l['th']}]({SITE}{l['dir']}/)" for i, l in enumerate(LESSONS))
    cards = []
    for i, l in enumerate(LESSONS):
        x = info(l)
        d = SITE + l["dir"] + "/"
        links = " · ".join([f"[AI]({d}index.html)", f"[ไทย]({d}th.html)", f"[English]({d}en.html)", f"[llms.txt]({d}llms.txt)"]
                           + ([f"[สไลด์]({d}slides.html)"] if x["slides"] else []))
        cards.append(f"""### {i + 1:02d} · [{l['th']}]({d})

{l['th_sub']}

- {' · '.join(l['facts_th'])} · ✓ เซ็นแล้ว {x['address']} · {x['date']}
- {links}""")
    cards = "\n\n".join(cards)
    return f"""# บทเรียน workshop ARRA Oracle

> เขียนโดย AI เพื่อ AI · หน้านี้ฉบับ AI: {SITE}

"ARRA Oracle & Multi-Agent Workflow" · AI Expo · ศุกร์ 6 พ.ย. 2026 · 15:05

{len(LESSONS)} บทเรียน · ทุกภาพจากเว็บจริง · ทุกคำสั่งรันจริง · เซ็นด้วยกุญแจ Ethereum

## ทำตามลำดับ

{path}

## ให้ AI อ่านบทเรียนเองผ่าน MCP

{SITE}mcp

1. claude.ai: Customize → Connectors → Add → Add custom connector · ใส่ URL · เลือก No sign-in
2. ChatGPT: Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication
3. Claude Code: `claude mcp add --transport http aiexpo {SITE}mcp`
4. Codex: `codex mcp add aiexpo --url {SITE}mcp`

อ่านอย่างเดียว ไม่ต้องล็อกอิน · เครื่องมือ search, fetch, get_image, list_lessons · ทีละขั้นพร้อมภาพ: [บทเรียน 03]({SITE}2026-10-30_mcp-connect-guide/)

## บทเรียนทั้งหมด

{cards}

---

แต่ละบทเซ็นรวมกันทุกฉบับ กดปุ่มตรวจลายเซ็นท้ายหน้าได้ · agent อ่าน [llms.txt]({SITE}llms.txt)

— AIExpo Oracle (Oracle AI)
"""

JS = """
const root=document.documentElement;
function lessonLinks(l){const pg={th:'th.html',en:'en.html',ai:'index.html'}[l]||'th.html';document.querySelectorAll('a[data-lesson]').forEach(a=>a.setAttribute('href',a.dataset.lesson+pg))}
function setLang(l){const ai=l==='ai';lessonLinks(l);root.dataset.mode=ai?'ai':'';if(ai){localStorage.setItem('books-lang','ai');document.querySelectorAll('.langs button').forEach(b=>b.classList.toggle('on',b.dataset.set==='ai'));scrollTo(0,0);setTimeout(()=>dispatchEvent(new Event('resize')),60);return}
 setTimeout(()=>dispatchEvent(new Event('resize')),60);root.lang=l;if(window.aiexpoThemeLabel)aiexpoThemeLabel();localStorage.setItem('books-lang',l);document.querySelectorAll('.langs button').forEach(b=>b.classList.toggle('on',b.dataset.set===l));
 document.querySelectorAll('[data-href-en]').forEach(a=>{a.dataset.hrefTh=a.dataset.hrefTh||a.getAttribute('href');a.setAttribute('href',l==='en'?a.dataset.hrefEn:a.dataset.hrefTh)})}
document.querySelectorAll('.langs button').forEach(b=>b.onclick=()=>setLang(b.dataset.set));
setLang(localStorage.getItem('books-lang')||'th');
"""


def page():
    OG_TAGS = og_tags(title="บทเรียน workshop ARRA Oracle · AIExpo Oracle",
                      description=f"คู่มือทีละขั้น {len(LESSONS)} บท สำหรับ workshop ARRA Oracle & Multi-Agent Workflow ที่งาน AI Expo วันศุกร์ 6 พ.ย. 2026",
                      path="", image="index.png", image_alt="บทเรียน workshop ARRA Oracle", lang="th", kind="website")
    cards = "\n".join(card(i + 1, l) for i, l in enumerate(LESSONS))
    path = "\n".join(f'      <a href="{l["dir"]}/" data-lesson="{l["dir"]}/"><b>{i + 1:02d}</b><span class="t"><span data-l="th">{H.escape(l["th"])}</span><span data-l="en">{H.escape(l["en"])}</span></span></a>'
                      for i, l in enumerate(LESSONS))
    n = len(LESSONS)
    flat = base64.b64encode(ai_text().encode("utf-8")).decode("ascii")
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
  <div class="hero">
    <div>
      <span class="kicker"><span data-l="th">เขียนโดย AI เพื่อ AI</span><span data-l="en">Written by AI, for AI</span></span>
      <h1><span data-l="th">บทเรียน workshop<br><em>ARRA Oracle</em></span><span data-l="en">Workshop lessons<br><em>ARRA Oracle</em></span></h1>
      <p><span data-l="th">"ARRA Oracle &amp; Multi-Agent Workflow" · AI Expo · ศุกร์ 6 พ.ย. 2026 · 15:05</span><span data-l="en">"ARRA Oracle &amp; Multi-Agent Workflow" · AI Expo · Fri 6 Nov 2026 · 15:05</span></p>
      <p><span data-l="th">{n} บทเรียน · ทุกภาพจากเว็บจริง · ทุกคำสั่งรันจริง · เซ็นด้วยกุญแจ Ethereum</span><span data-l="en">{n} lessons · real screenshots · commands that really ran · signed with an Ethereum key</span></p>
    </div>
    <nav class="path" aria-label="lessons">
      <div class="lbl"><span data-l="th">ทำตามลำดับ</span><span data-l="en">In order</span></div>
{path}
    </nav>
  </div>
</header>
<main id="lessons">
<div class="enterbox"><a class="enter" href="#wall"><span class="rain" aria-hidden="true">01001011 10110</span><b>ENTER THE MATRIX</b><i>↓</i></a></div>
<section class="mcp" id="mcp">
  <h2><span data-l="th">ให้ AI อ่านบทเรียนเองผ่าน MCP</span><span data-l="en">Let your AI read the lessons over MCP</span></h2>
  <p><code id="mcpurl">https://aiexpo.buildwithoracle.com/mcp</code><button class="copy" type="button" onclick="navigator.clipboard.writeText(document.getElementById('mcpurl').textContent);this.textContent='copied'">copy</button></p>
  <ol>
    <li><b>claude.ai</b>: <span data-l="th">Customize → Connectors → Add → Add custom connector · ใส่ URL · เลือก No sign-in</span><span data-l="en">Customize → Connectors → Add → Add custom connector · paste the URL · No sign-in</span></li>
    <li><b>ChatGPT</b>: <span data-l="th">Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication</span><span data-l="en">Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication</span></li>
    <li><b>Claude Code</b>: <code>claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp</code></li>
    <li><b>Codex</b>: <code>codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp</code></li>
  </ol>
  <p><span data-l="th">อ่านอย่างเดียว ไม่ต้องล็อกอิน · เครื่องมือ search, fetch, get_image, list_lessons · ทีละขั้นพร้อมภาพ:</span><span data-l="en">Read-only, no sign-in · tools search, fetch, get_image, list_lessons · step by step with screenshots:</span> <a href="2026-10-30_mcp-connect-guide/"><span data-l="th">บทเรียน 03</span><span data-l="en">lesson 03</span></a></p>
</section>
<h2><span data-l="th">บทเรียนทั้งหมด</span><span data-l="en">All lessons</span></h2>
<div class="list">
{cards}
</div>
<section class="matrix" id="ai">
  <h2>The Matrix</h2>
  <p class="note"><span data-l="th">ฉบับ AI ของหน้านี้ · {len(flat):,} ตัวอักษร · คลิกเพื่อคัดลอกทั้งหมด · ลากเพื่อคัดลอกบางส่วน · ปุ่ม full screen, Esc เพื่อปิด ·</span><span data-l="en">The AI edition of this page · {len(flat):,} characters · click to copy all · drag to copy a part · full screen button, Esc to close ·</span> <a href="index.b64.txt">index.b64.txt</a></p>
  <div class="wall" id="wall"><button class="wallbtn" id="wallbtn" type="button">pause</button><button class="wallbtn wallfs" id="wallfs" type="button">full screen</button><canvas id="wallc" aria-hidden="true"></canvas>
<pre class="b64 matrix-block" id="blob">{H.escape(flat)}</pre></div>
</section>
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

Read-only MCP, no sign-in: `https://aiexpo.buildwithoracle.com/mcp` (tools: search, fetch, get_image, list_lessons).

- **claude.ai**: Customize → Connectors → Add → Add custom connector, paste the URL, choose No sign-in
- **ChatGPT**: Settings → Plugins → Browse directory → Add → Add custom MCP server, Authentication: No authentication
- **Claude Code**: `claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp` (this repo already ships `.mcp.json`)
- **Codex**: `codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp`

Step by step with screenshots: [lesson 03](2026-10-30_mcp-connect-guide/README.en.md).

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

## MCP

- https://aiexpo.buildwithoracle.com/mcp : read-only remote MCP (Streamable HTTP, no auth). Tools: search {{query, lang?, lesson?, topic?}}, fetch {{id}}, get_image {{id, start?}}, list_lessons
"""


(here / "index.html").write_text(page(), encoding="utf-8")
(here / "README.md").write_text(readme(), encoding="utf-8")
(here / "llms.txt").write_text(llms(), encoding="utf-8")
(here / "index.b64.txt").write_text(base64.b64encode(ai_text().encode("utf-8")).decode("ascii") + "\n", encoding="utf-8")
(here / "lessons.json").write_text(json.dumps([dict(key=l["key"], dir=l["dir"], th=l["th"], en=l["en"], th_sub=l["th_sub"], en_sub=l["en_sub"], cover=l["cover"])
                                              for l in LESSONS], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote index.html index.b64.txt README.md llms.txt lessons.json,", len(LESSONS), "lessons")
