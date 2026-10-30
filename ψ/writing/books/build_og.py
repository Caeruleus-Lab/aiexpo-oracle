"""Build the Open Graph / Facebook share cards: og/index.png and og/<lesson>.png, 1200x630.

Each card is an HTML page in the deck palette (tokens.css), rendered by ego-browser so Thai shapes correctly,
with the lesson's real cover screenshot beside the title. Re-renders a card only when its HTML changes
(hash kept in og/cards.json).

Usage: python3 build_og.py   (after build_index.py; needs ego-browser; then commit og/ and ./deploy.sh)
"""
import base64
import hashlib
import html as H
import json
import pathlib
import subprocess

here = pathlib.Path(__file__).resolve().parent
OG = here / "og"
SITE = "aiexpo.buildwithoracle.com"
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@500;600;700&family=Sarabun:wght@400;500;700&display=swap">'

CARD_CSS = """
*{box-sizing:border-box;margin:0}
html,body{width:1200px;height:630px;overflow:hidden;background:var(--paper);color:var(--ink);font-family:var(--body)}
.card{position:relative;width:1200px;height:630px;padding:64px 72px;display:grid;grid-template-columns:1fr 430px;gap:56px;align-items:center}
.lamp{position:absolute;left:0;top:0;width:12px;height:100%;background:var(--accent)}
.num{font:700 44px/1 var(--display);color:var(--accent);margin-bottom:22px}
h1{font:700 60px/1.18 var(--display);color:var(--ink)}
.en{margin-top:20px;font:500 26px/1.35 var(--body);color:var(--ink-2)}
.foot{position:absolute;left:72px;right:72px;bottom:40px;display:flex;justify-content:space-between;font:600 22px var(--body);color:var(--ink-3)}
.foot b{color:var(--ink-2);font-weight:700}
.shot{width:430px;height:430px;border:1px solid var(--rule);border-radius:14px;overflow:hidden;background:var(--paper-2)}
.shot img{width:100%;height:100%;object-fit:cover;object-position:left top;display:block}
ol{list-style:none;padding:0;display:grid;gap:18px}
ol li{display:grid;grid-template-columns:56px 1fr;gap:16px;align-items:center;font:600 27px/1.3 var(--display);color:var(--ink)}
ol li b{display:inline-flex;width:56px;height:56px;border-radius:50%;align-items:center;justify-content:center;background:var(--accent);color:var(--accent-ink);font:700 24px var(--display)}
.idx{grid-template-columns:1fr 520px}
"""


def data_uri(path):
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def page(body, extra=""):
    tokens = (here / "tokens.css").read_text(encoding="utf-8")
    return f'<!doctype html><html lang="th"><head><meta charset="utf-8">{FONTS}<style>{tokens}{CARD_CSS}</style></head><body>{body}</body></html>'


def lesson_card(i, l):
    return page(f'''<div class="card"><div class="lamp"></div>
<div><div class="num">{i:02d}</div><h1>{H.escape(l["th"])}</h1><p class="en">{H.escape(l["en"])}</p></div>
<div class="shot"><img src="{data_uri(here / l["dir"] / l["cover"])}"></div>
<div class="foot"><span><b>AIExpo Oracle</b> · AI Expo · 6 พ.ย. 2026</span><span>{SITE}</span></div></div>''')


def index_card(lessons):
    items = "".join(f'<li><b>{i + 1:02d}</b><span>{H.escape(l["th"])}</span></li>' for i, l in enumerate(lessons))
    return page(f'''<div class="card idx"><div class="lamp"></div>
<div><h1>บทเรียน workshop<br><span style="color:var(--accent)">ARRA Oracle</span></h1><p class="en">ARRA Oracle &amp; Multi-Agent Workflow · AI Expo · Fri 6 Nov 2026</p></div>
<ol>{items}</ol>
<div class="foot"><span><b>AIExpo Oracle</b> · {len(lessons)} บทเรียน</span><span>{SITE}</span></div></div>''')


def render(jobs):
    """jobs: list of (html_path, png_path). One ego-browser round renders them all at 1200x630."""
    pairs = json.dumps([[str(h), str(p)] for h, p in jobs])
    script = f"""
const fs = await import('node:fs')
const task = await taskSpace('og cards: aiexpo lessons')
const page = task.page('p1')
for (const [h, p] of {pairs}) {{
  await page.goto('file://' + h, {{ timeout: 20000 }})
  await page.cdp('Emulation.setDeviceMetricsOverride', {{ width: 1200, height: 630, deviceScaleFactor: 1, mobile: false, screenWidth: 1200, screenHeight: 630 }})
  await page.waitForFunction(() => document.fonts.status === 'loaded', undefined, {{ timeout: 15000 }}).catch(() => {{}})
  await page.waitForTimeout(800)
  let ok = false
  for (let i = 0; i < 8 && !ok; i++) {{
    try {{ const r = await page.cdp('Page.captureScreenshot', {{ format: 'png' }}, {{ timeout: 6000 }}); fs.writeFileSync(p, Buffer.from(r.data, 'base64')); ok = true }}
    catch (e) {{ await page.waitForTimeout(800) }}
  }}
  console.log((ok ? 'ok   ' : 'FAIL ') + p)
}}
await task.finish({{ keep: [] }})
"""
    out = subprocess.run(["ego-browser", "nodejs"], input=script, text=True, capture_output=True)
    print(out.stdout.strip() or out.stderr.strip())


def main():
    lessons = json.loads((here / "lessons.json").read_text(encoding="utf-8"))
    OG.mkdir(exist_ok=True)
    src = OG / "src"
    src.mkdir(exist_ok=True)
    state_path = OG / "cards.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    cards = {"index": index_card(lessons)}
    cards.update({l["key"]: lesson_card(i + 1, l) for i, l in enumerate(lessons)})
    jobs = []
    for key, doc in cards.items():
        h = hashlib.sha256(doc.encode()).hexdigest()[:16]
        (src / f"{key}.html").write_text(doc, encoding="utf-8")
        png = OG / f"{key}.png"
        if state.get(key) != h or not png.exists():
            jobs.append((src / f"{key}.html", png))
            state[key] = h
    if jobs:
        render(jobs)
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"og cards: {len(cards)} total, {len(jobs)} rendered now")


main()
