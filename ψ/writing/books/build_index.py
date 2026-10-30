"""Build the landing page that lists every lesson in this folder.

  index.html  the page people open (Thai by default, English switch)
  README.md   the same list for GitHub
  llms.txt    the same list for agents

Add a lesson: append one dict to LESSONS, then run `python3 build_index.py`.
Each lesson folder keeps its own pages, signature and llms.txt; this page only links to them.
"""
import html as H
import json
import pathlib

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
]


def info(l):
    d = here / l["dir"]
    sig = json.loads((d / "signature.json").read_text(encoding="utf-8"))
    return dict(address=sig["address"], date=sig["date"], slides=(d / "slides.html").exists(),
                images=len(list((d / "images").glob("*.png"))))


def card(i, l):
    x = info(l)
    d = l["dir"] + "/"
    links = [("index.html", "base64"), ("th.html", "ไทย"), ("en.html", "English"), ("llms.txt", "llms.txt")]
    if x["slides"]:
        links.append(("slides.html", '<span data-l="th">สไลด์</span><span data-l="en">slides</span>'))
    chips = "".join(f'<a class="chip" href="{d}{h}">{t}</a>' for h, t in links)
    facts = "".join(f'<span><span data-l="th">{a}</span><span data-l="en">{b}</span></span>'
                    for a, b in zip(l["facts_th"], l["facts_en"]))
    addr = x["address"]
    return f'''<article class="card">
  <a class="thumb" href="{d}th.html" data-href-en="{d}en.html"><img src="{d}{l["cover"]}" alt="" loading="lazy"></a>
  <div class="body">
    <div class="num">{i:02d}</div>
    <h2><a href="{d}th.html" data-href-en="{d}en.html"><span data-l="th">{H.escape(l["th"])}</span><span data-l="en">{H.escape(l["en"])}</span></a></h2>
    <p><span data-l="th">{H.escape(l["th_sub"])}</span><span data-l="en">{H.escape(l["en_sub"])}</span></p>
    <div class="facts">{facts}<span>✓ <span data-l="th">เซ็นแล้ว</span><span data-l="en">signed</span> {addr[:6]}…{addr[-4:]}</span><span>{x["date"]}</span></div>
    <div class="chips">{chips}</div>
  </div>
</article>'''


CSS = """
:root{--ink:#0d1b3d;--blue:#2f5bea;--cyan:#27e6f2;--paper:#f4f6fb;--mute:#5a6b8c;--pad:clamp(18px,5vw,120px)}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font:clamp(17px,0.55vw + 12px,24px)/1.7 Sarabun,"Noto Sans Thai","IBM Plex Sans Thai",system-ui,sans-serif}
html[lang=th] [data-l=en],html[lang=en] [data-l=th]{display:none}
.cover{background:radial-gradient(60vw 60vh at 85% 0%,#3b6cf5 0%,#132a6b 55%,#070f2b 100%);color:#fff;padding:0 var(--pad) clamp(36px,6vh,80px)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:clamp(14px,2.2vh,26px) 0}
.brand{font-weight:800;letter-spacing:.02em;color:#fff;text-decoration:none}.brand em{font-style:normal;color:var(--cyan)}
.bar .right{display:flex;align-items:center;gap:10px}
.bar .mcplink{color:#cfe0ff;text-decoration:none;font-weight:700;font-size:15px;border:2px solid rgba(39,230,242,.5);border-radius:999px;padding:4px 14px}
.hero{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(24px,4vw,80px);align-items:center;margin-top:clamp(10px,3vh,40px)}
.path{background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.18);border-radius:22px;padding:clamp(14px,1.6vw,28px);display:grid;gap:10px}
.path .lbl{font-size:.8em;font-weight:800;letter-spacing:.08em;color:#9fdcff;text-transform:uppercase}
.path a{display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center;color:#fff;text-decoration:none;padding:10px 12px;border-radius:14px;transition:background .15s}
.path a:hover{background:rgba(39,230,242,.12)}
.path a b{display:inline-flex;width:2.2em;height:2.2em;border-radius:50%;align-items:center;justify-content:center;background:var(--cyan);color:var(--ink);font-weight:800}
.path a span.t{font-weight:700;line-height:1.35}
@media (max-width:980px){.hero{grid-template-columns:1fr}}
.langs{display:flex;gap:8px}
.langs button{color:#cfe0ff;background:none;border:2px solid rgba(255,255,255,.35);border-radius:999px;padding:4px 14px;font:700 15px Sarabun,sans-serif;cursor:pointer}
.langs button.on{background:#fff;color:var(--ink);border-color:#fff}
.kicker{display:inline-block;background:#c2410c;color:#fff;font-weight:800;border-radius:999px;padding:6px 18px}
.cover h1{font-size:clamp(34px,4.4vw,88px);line-height:1.12;margin:18px 0 12px;font-weight:800}
.cover h1 em{font-style:normal;color:var(--cyan)}
.cover p{font-size:clamp(17px,1.2vw,28px);color:#d6e4ff;margin:0 0 6px}
.down{display:inline-flex;align-items:center;gap:12px;margin-top:clamp(28px,6vh,80px);padding:10px 22px 10px 10px;border-radius:999px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.4);color:#fff;text-decoration:none;font-weight:700}
.down b{display:inline-flex;width:2.1em;height:2.1em;border-radius:50%;align-items:center;justify-content:center;background:var(--cyan);color:var(--ink)}
main{padding:clamp(26px,5vh,64px) var(--pad) 12vh}
main>h2{font-size:clamp(28px,3vw,56px);margin:0 0 clamp(18px,3vh,36px)}
.list{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr));gap:clamp(18px,2vw,36px)}
.card{display:flex;flex-direction:column;background:#fff;border:2px solid #c9d3ea;border-radius:22px;overflow:hidden;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--blue);transform:translateY(-2px)}
.thumb{display:block;background:#06112e}
.thumb img{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;display:block}
.body{padding:clamp(18px,2.2vw,40px)}
.num{font-weight:800;color:var(--blue);font-size:.9em;letter-spacing:.08em}
.card h2{font-size:clamp(22px,1.6vw,34px);line-height:1.25;margin:4px 0 8px}
.card h2 a{color:var(--ink);text-decoration:none}
.card h2 a:hover{color:var(--blue)}
.card p{color:var(--mute);margin:0 0 14px}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.facts>span{background:#e8eefc;border-radius:10px;padding:2px 10px;font-size:.8em;font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chip{display:inline-flex;background:#fff;border:2px solid #c9d3ea;border-radius:999px;padding:4px 14px;text-decoration:none;color:var(--ink);font-size:.88em;font-weight:700}
.chip:hover{border-color:var(--blue)}
.note{color:var(--mute);font-size:.85em;margin-top:clamp(24px,4vh,48px)}
.mcp{margin-top:clamp(28px,5vh,64px);background:#06112e;color:#e6f6ff;border-radius:22px;padding:clamp(18px,2.4vw,44px)}
.mcp h2{font-size:clamp(24px,2.2vw,44px);margin:0 0 10px;color:#fff}
.mcp code{background:rgba(39,230,242,.12);color:var(--cyan);border-radius:8px;padding:4px 10px;font:clamp(15px,1vw,22px) Menlo,"SF Mono",monospace;word-break:break-all}
.mcp ol{margin:14px 0 6px;padding-left:1.3em}.mcp li{margin:6px 0}
.mcp a{color:var(--cyan)}
.mcp .copy{margin-left:8px;background:none;border:1px solid rgba(255,255,255,.35);color:#e6f6ff;border-radius:8px;padding:2px 10px;font:600 14px Sarabun,sans-serif;cursor:pointer}
main>h2{scroll-margin-top:16px}
"""

JS = """
const root=document.documentElement;
function setLang(l){root.lang=l;localStorage.setItem('books-lang',l);document.querySelectorAll('.langs button').forEach(b=>b.classList.toggle('on',b.dataset.set===l));
 document.querySelectorAll('[data-href-en]').forEach(a=>{a.dataset.hrefTh=a.dataset.hrefTh||a.getAttribute('href');a.setAttribute('href',l==='en'?a.dataset.hrefEn:a.dataset.hrefTh)})}
document.querySelectorAll('.langs button').forEach(b=>b.onclick=()=>setLang(b.dataset.set));
setLang(localStorage.getItem('books-lang')||'th');
"""


def page():
    cards = "\n".join(card(i + 1, l) for i, l in enumerate(LESSONS))
    path = "\n".join(f'      <a href="{l["dir"]}/th.html" data-href-en="{l["dir"]}/en.html"><b>{i + 1:02d}</b><span class="t"><span data-l="th">{H.escape(l["th"])}</span><span data-l="en">{H.escape(l["en"])}</span></span></a>'
                      for i, l in enumerate(LESSONS))
    n = len(LESSONS)
    return f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AIExpo Oracle · บทเรียน / Lessons</title>
<link rel="help" type="text/plain" href="llms.txt" title="llms.txt">
<style>{CSS}</style>
</head>
<body>
<header class="cover">
  <div class="bar">
    <a class="brand" href="./">AIExpo <em>Oracle</em></a>
    <div class="right"><a class="mcplink" href="#mcp">MCP</a><nav class="langs"><button data-set="th">ไทย</button><button data-set="en">English</button></nav></div>
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
<h2><span data-l="th">บทเรียนทั้งหมด</span><span data-l="en">All lessons</span></h2>
<div class="list">
{cards}
</div>
<section class="mcp" id="mcp">
  <h2><span data-l="th">ให้ AI อ่านบทเรียนเองผ่าน MCP</span><span data-l="en">Let your AI read the lessons over MCP</span></h2>
  <p><code id="mcpurl">https://aiexpo.buildwithoracle.com/mcp</code><button class="copy" type="button" onclick="navigator.clipboard.writeText(document.getElementById('mcpurl').textContent);this.textContent='copied'">copy</button></p>
  <ol>
    <li><b>claude.ai</b>: <span data-l="th">Customize → Connectors → Add → Add custom connector · ใส่ URL · เลือก No sign-in</span><span data-l="en">Customize → Connectors → Add → Add custom connector · paste the URL · No sign-in</span></li>
    <li><b>ChatGPT</b>: <span data-l="th">Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication</span><span data-l="en">Settings → Plugins → Browse directory → Add → Add custom MCP server · Authentication: No authentication</span></li>
    <li><b>Claude Code</b>: <code>claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp</code></li>
    <li><b>Codex</b>: <code>codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp</code></li>
  </ol>
  <p><span data-l="th">อ่านอย่างเดียว ไม่ต้องล็อกอิน · เครื่องมือ search, fetch, get_image, list_lessons · ทีละขั้นพร้อมภาพ:</span><span data-l="en">Read-only, no sign-in · tools search, fetch, get_image, list_lessons · step by step with screenshots:</span> <a href="2026-10-30_mcp-connect-guide/th.html" data-href-en="2026-10-30_mcp-connect-guide/en.html"><span data-l="th">บทเรียน 03</span><span data-l="en">lesson 03</span></a></p>
</section>
<p class="note"><span data-l="th">แต่ละบทมีสามฉบับ (base64 · ไทย · English) เซ็นรวมกัน กดปุ่มตรวจลายเซ็นท้ายหน้าได้ · agent อ่าน</span><span data-l="en">Each lesson has three editions (base64 · Thai · English) signed together; the button at the end of each page checks the signature · agents read</span> <a href="llms.txt">llms.txt</a></p>
</main>
<script>{JS}</script>
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

Each lesson ships three editions (base64 · Thai · English) signed together with AIExpo Oracle's key; see the lesson's `SIGNATURE.md`.
## Ask the lessons from your AI (MCP)

Read-only MCP, no sign-in: `https://aiexpo.buildwithoracle.com/mcp` (tools: search, fetch, get_image, list_lessons).

- **claude.ai**: Customize → Connectors → Add → Add custom connector, paste the URL, choose No sign-in
- **ChatGPT**: Settings → Plugins → Browse directory → Add → Add custom MCP server, Authentication: No authentication
- **Claude Code**: `claude mcp add --transport http aiexpo https://aiexpo.buildwithoracle.com/mcp` (this repo already ships `.mcp.json`)
- **Codex**: `codex mcp add aiexpo --url https://aiexpo.buildwithoracle.com/mcp`

Step by step with screenshots: [lesson 03](2026-10-30_mcp-connect-guide/README.en.md).

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
(here / "lessons.json").write_text(json.dumps([dict(key=l["key"], dir=l["dir"], th=l["th"], en=l["en"], th_sub=l["th_sub"], en_sub=l["en_sub"])
                                              for l in LESSONS], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("wrote index.html README.md llms.txt lessons.json,", len(LESSONS), "lessons")
