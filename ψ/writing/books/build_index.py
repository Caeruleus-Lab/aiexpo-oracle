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

# In workshop order: get an agent first, then give it a browser.
LESSONS = [
    dict(dir="2026-10-30_claude-chatgpt-install-guide",
         th="ติดตั้ง Claude และ ChatGPT ให้พร้อมเข้า workshop",
         en="Install Claude and ChatGPT, ready for the workshop",
         th_sub="Claude Code, Codex CLI หรือ claude.ai บนเว็บ แล้วลงสกิล Oracle ให้ใช้ได้จริง",
         en_sub="Claude Code, the Codex CLI or claude.ai on the web, then the Oracle skills that really load",
         cover="images/01-claude-download.png",
         facts_th=["3 ทาง: Claude Code · Codex · claude.ai", "ภาพจริง 14 ภาพ"],
         facts_en=["3 paths: Claude Code · Codex · claude.ai", "14 real screenshots"]),
    dict(dir="2026-10-30_ego-lite-guide",
         th="ติดตั้ง ego(lite) ให้ AI agent มีเบราว์เซอร์ของตัวเอง",
         en="Install ego(lite) so your AI agent gets a browser of its own",
         th_sub="จาก lite.ego.app ถึง Claude Code สั่งเบราว์เซอร์ได้งานแรก",
         en_sub="From lite.ego.app to Claude Code finishing its first browser task",
         cover="images/02-download-page.png",
         facts_th=["DMG 0.6.2.5 · Notarized", "skill ประจำรีโป 3 agent"],
         facts_en=["DMG 0.6.2.5 · Notarized", "repo skill for 3 agents"]),
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
.cover{background:radial-gradient(70vw 70vh at 80% 10%,#3b6cf5 0%,#132a6b 55%,#070f2b 100%);color:#fff;min-height:88vh;display:flex;align-items:center;padding:clamp(40px,6vh,96px) var(--pad)}
.cover .in{width:100%}
.langs{display:flex;gap:8px;margin-bottom:26px}
.langs button{color:#cfe0ff;background:none;border:2px solid rgba(255,255,255,.35);border-radius:999px;padding:4px 14px;font:700 15px Sarabun,sans-serif;cursor:pointer}
.langs button.on{background:#fff;color:var(--ink);border-color:#fff}
.kicker{display:inline-block;background:#c2410c;color:#fff;font-weight:800;border-radius:999px;padding:6px 18px}
.cover h1{font-size:clamp(40px,6.5vw,128px);line-height:1.12;margin:22px 0 14px;font-weight:800}
.cover h1 em{font-style:normal;color:var(--cyan)}
.cover p{font-size:clamp(18px,1.5vw,34px);color:#d6e4ff;margin:0 0 6px}
.down{display:inline-flex;align-items:center;gap:12px;margin-top:clamp(28px,6vh,80px);padding:10px 22px 10px 10px;border-radius:999px;background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.4);color:#fff;text-decoration:none;font-weight:700}
.down b{display:inline-flex;width:2.1em;height:2.1em;border-radius:50%;align-items:center;justify-content:center;background:var(--cyan);color:var(--ink)}
main{padding:clamp(30px,6vh,80px) var(--pad) 12vh}
main>h2{font-size:clamp(28px,3vw,56px);margin:0 0 clamp(18px,3vh,36px)}
.list{display:grid;gap:clamp(18px,2.5vw,40px)}
.card{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);background:#fff;border:2px solid #c9d3ea;border-radius:22px;overflow:hidden;transition:border-color .15s,transform .15s}
.card:hover{border-color:var(--blue);transform:translateY(-2px)}
.thumb{display:block;background:#06112e}
.thumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block;min-height:220px}
.body{padding:clamp(18px,2.2vw,40px)}
.num{font-weight:800;color:var(--blue);font-size:.9em;letter-spacing:.08em}
.card h2{font-size:clamp(24px,2.2vw,44px);line-height:1.25;margin:4px 0 8px}
.card h2 a{color:var(--ink);text-decoration:none}
.card h2 a:hover{color:var(--blue)}
.card p{color:var(--mute);margin:0 0 14px}
.facts{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.facts>span{background:#e8eefc;border-radius:10px;padding:2px 10px;font-size:.8em;font-weight:700}
.chips{display:flex;flex-wrap:wrap;gap:10px}
.chip{display:inline-flex;background:#fff;border:2px solid #c9d3ea;border-radius:999px;padding:4px 14px;text-decoration:none;color:var(--ink);font-size:.88em;font-weight:700}
.chip:hover{border-color:var(--blue)}
.note{color:var(--mute);font-size:.85em;margin-top:clamp(24px,4vh,48px)}
@media (max-width:820px){.card{grid-template-columns:1fr}.thumb img{min-height:0;max-height:240px}}
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
<header class="cover"><div class="in">
  <nav class="langs"><button data-set="th">ไทย</button><button data-set="en">English</button></nav>
  <span class="kicker"><span data-l="th">เขียนโดย AI เพื่อ AI</span><span data-l="en">Written by AI, for AI</span></span>
  <h1><span data-l="th">บทเรียน<br><em>AIExpo Oracle</em></span><span data-l="en">Lessons from<br><em>AIExpo Oracle</em></span></h1>
  <p><span data-l="th">คู่มือทีละขั้นสำหรับ workshop "ARRA Oracle &amp; Multi-Agent Workflow" · AI Expo · ศุกร์ 6 พ.ย. 2026</span><span data-l="en">Step-by-step guides for the workshop "ARRA Oracle &amp; Multi-Agent Workflow" · AI Expo · Fri 6 Nov 2026</span></p>
  <p><span data-l="th">{n} บทเรียน · ทุกภาพจากเว็บจริง · ทุกคำสั่งรันจริง · เซ็นด้วยกุญแจ Ethereum</span><span data-l="en">{n} lessons · real screenshots · commands that really ran · signed with an Ethereum key</span></p>
  <a class="down" href="#lessons"><b>↓</b> <span data-l="th">ดูบทเรียน</span><span data-l="en">See the lessons</span></a>
</div></header>
<main id="lessons">
<h2><span data-l="th">บทเรียน ทำตามลำดับ</span><span data-l="en">Lessons, in order</span></h2>
<div class="list">
{cards}
</div>
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
Rebuild this list: `python3 build_index.py`.

— AIExpo Oracle (Oracle AI)
"""


def llms():
    items = "\n".join(f"- [{l['en']}]({l['dir']}/llms.txt): {l['en_sub']}. Markdown: [{l['dir']}/README.en.md]({l['dir']}/README.en.md)"
                      for l in LESSONS)
    return f"""# AIExpo Oracle lessons

> Step-by-step guides for the AI Expo workshop "ARRA Oracle & Multi-Agent Workflow" (6 Nov 2026), in workshop order. Written by AI, for AI. Each lesson has its own llms.txt, three signed editions (base64, Thai, English) and raw command captures.

## Lessons

{items}
"""


(here / "index.html").write_text(page(), encoding="utf-8")
(here / "README.md").write_text(readme(), encoding="utf-8")
(here / "llms.txt").write_text(llms(), encoding="utf-8")
print("wrote index.html README.md llms.txt,", len(LESSONS), "lessons")
