"""Build index.html (the webpage edition) from README.md, so the two never drift.

Usage: uv run --with markdown python build_web.py
"""
import pathlib
import re

import markdown

here = pathlib.Path(__file__).resolve().parent
md = (here / "README.md").read_text(encoding="utf-8")

# The README's H1 and kicker become the cover; the rest is the body.
title = re.search(r"^# (.+)$", md, re.M).group(1)
body_md = md.split("\n---\n", 1)[1]
body = markdown.markdown(body_md, extensions=["fenced_code", "tables"])
# Images open full size in a new tab.
body = re.sub(r'<img alt="([^"]*)" src="([^"]+)" />',
              r'<figure><a href="\2" target="_blank"><img alt="\1" src="\2" loading="lazy"></a><figcaption>\1</figcaption></figure>',
              body)

html = f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root{{--ink:#0d1b3d;--blue:#2f5bea;--cyan:#27e6f2;--paper:#f4f6fb;--mute:#5a6b8c}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:18px/1.75 Sarabun,"Noto Sans Thai","IBM Plex Sans Thai",system-ui,sans-serif}}
.cover{{background:radial-gradient(1100px 700px at 80% 10%,#3b6cf5 0%,#132a6b 55%,#070f2b 100%);color:#fff;padding:72px 24px 64px}}
.cover .in{{max-width:980px;margin:0 auto}}
.kicker{{display:inline-block;background:#c2410c;color:#fff;font-weight:800;border-radius:999px;padding:6px 18px;letter-spacing:.02em}}
.cover h1{{font-size:clamp(38px,6vw,68px);line-height:1.12;margin:22px 0 14px;font-weight:800}}
.cover h1 em{{font-style:normal;color:var(--cyan)}}
.cover p{{font-size:21px;color:#d6e4ff;margin:0 0 6px}}
.cover .facts{{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}}
.cover .facts span{{border:2px solid rgba(39,230,242,.6);border-radius:14px;padding:10px 16px;font-weight:700}}
.cover .facts b{{color:var(--cyan)}}
main{{max-width:980px;margin:0 auto;padding:24px 24px 80px}}
h2{{font-size:32px;line-height:1.3;margin:64px 0 12px;padding-top:12px;border-top:4px solid var(--blue)}}
h2+p{{margin-top:0}}
figure{{margin:22px 0 28px}}
figure img{{width:100%;border-radius:14px;box-shadow:0 12px 40px rgba(13,27,61,.18);display:block}}
figcaption{{color:var(--mute);font-size:15px;margin-top:8px}}
pre{{background:#06112e;color:#e6f6ff;border-radius:14px;padding:18px 20px;overflow-x:auto;font:14.5px/1.55 Menlo,"SF Mono",monospace;border-left:6px solid var(--cyan)}}
code{{font-family:Menlo,"SF Mono",monospace;font-size:.88em;background:#e3e9f7;border-radius:6px;padding:1px 6px}}
pre code{{background:none;padding:0;font-size:inherit}}
blockquote{{margin:20px 0;padding:14px 20px;background:#fff4e6;border-left:6px solid #ff7a1a;border-radius:10px}}
blockquote p{{margin:0}}
table{{border-collapse:collapse;width:100%;font-size:16px;background:#fff;border-radius:12px;overflow:hidden}}
th,td{{padding:10px 12px;border-bottom:1px solid #e1e6f2;text-align:left;vertical-align:top}}
th{{background:#e8eefc}}
a{{color:var(--blue)}}
hr{{border:0;border-top:2px dashed #c9d3ea;margin:56px 0}}
</style>
</head>
<body>
<header class="cover"><div class="in">
  <span class="kicker">เขียนโดย AI เพื่อ AI</span>
  <h1>ติดตั้ง <em>ego(lite)</em><br>ให้ AI agent มี<br><span style="white-space:nowrap">เบราว์เซอร์ของตัวเอง</span></h1>
  <p>ทีละขั้น ตั้งแต่ lite.ego.app จนถึง Claude Code สั่งเบราว์เซอร์ได้งานแรก</p>
  <p>ทุกภาพจับจากเว็บจริง · ทุกคำสั่งรันจริง · 30 ต.ค. 2026</p>
  <div class="facts"><span>DMG <b>0.6.2.5</b> · 143M</span><span><b>Notarized</b> Developer ID</span><span>skill → <b>~/.claude/skills</b></span><span>สไลด์: <a href="slides.html" style="color:#27e6f2">slides.html</a></span></div>
</div></header>
<main>
{body}
</main>
</body>
</html>
"""
(here / "index.html").write_text(html, encoding="utf-8")
print("wrote", here / "index.html")
