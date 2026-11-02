# Verification suite for deck.html (Osaa, round 2).
# usage: uv run -q --with playwright --with pillow python checks/verify.py <deck.html> <mode>
#   mode = text      : visible text has no [—–], no emoji, min font size, placeholder present
#        = contrast  : worst-case WCAG contrast of every text box against what is drawn behind it,
#                      sampled at 0/150/300/450/600/900 ms of every slide move (live mode), plus rest
#        = contrast-nomask : same, with the clearance turned off (negative control, must go red)
#        = fps       : requestAnimationFrame count over 3 s on every slide (live mode)
#        = reduced   : prefers-reduced-motion run: world ok, loop frames == 0
#        = neg       : CDN broken copy: world absent, every slide still shows its text
import sys, pathlib, re, json, io
from playwright.sync_api import sync_playwright
from PIL import Image

CHROME = "/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
deck = pathlib.Path(sys.argv[1]).resolve(); mode = sys.argv[2]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿️]")

def lum(c):
    def ch(v):
        v /= 255; return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = c[:3]; return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)
def ratio(a, b):
    la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb); return (hi + 0.05) / (lo + 0.05)

TEXT_JS = """() => {
  const hs = document.getElementById("hide"); if (hs) hs.disabled = true;   // read real colours, then hide again
  const probe = document.createElement('canvas').getContext('2d', {willReadFrequently:true});
  const rgb = v => { probe.clearRect(0,0,1,1); probe.fillStyle='#000'; probe.fillStyle=v; probe.fillRect(0,0,1,1); return [...probe.getImageData(0,0,1,1).data]; };
  const s = document.querySelector('.slide.on'); s.classList.add('measuring');   // resting boxes, not the entrance offset
  const res = [...s.querySelectorAll('h1,h2,p,li,.row .t,.row .n,.row .m,svg text')].filter(e => !e.closest('.notes')).map(e => {
    const r0 = e.getBoundingClientRect(), cs = getComputedStyle(e), pl = parseFloat(cs.paddingLeft)||0, pr = parseFloat(cs.paddingRight)||0;
    const b = { left: r0.left + pl, top: r0.top, right: r0.right - pr, bottom: r0.bottom };   // content box: bullets and padding are not background
    return { tag: e.tagName + '.' + (e.getAttribute('class')||''), text: (e.textContent||'').trim().slice(0,24),
             box: [b.left, b.top, b.right, b.bottom].map(Math.round), color: rgb(e.tagName.toLowerCase()==='text' ? cs.fill : cs.color) };
  });
  s.classList.remove('measuring'); if (hs) hs.disabled = false; return res;
}"""
HIDE = ".slide.on, .slide.on *{color:transparent!important} .slide.on svg text{fill:transparent!important} .todo{outline-color:transparent!important}"

OPAC_JS = """() => [...document.querySelector('.slide.on').querySelectorAll('h1,h2,p,li,.row .t,.row .n,.row .m,svg text')].filter(e => !e.closest('.notes')).map(e => {
  let o = 1; for (let n = e; n && n.nodeType === 1; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity); return o; })"""

def worst(img, items, opac=None):
    out = []
    assert all(it['color'][3] == 255 for it in items), 'instrument: a text colour read as transparent'
    for j, it in enumerate(items):
        if opac is not None and opac[j] < 0.5: continue
        l, t, r, b = it["box"]; l, t = max(l, 0), max(t, 0); r, b = min(r, 1920), min(b, 1080)
        if r <= l or b <= t: continue
        crop = img.crop((l, t, r, b)).convert("RGB")
        px = list(crop.get_flattened_data()) if hasattr(crop,'get_flattened_data') else list(crop.getdata())
        w = min(ratio(it["color"], p) for p in px)
        out.append((round(w, 2), it["text"]))
    out.sort(); return out

with sync_playwright() as p:
    import os; args = os.environ.get('CHROME_ARGS', '').split()
    br = p.chromium.launch(executable_path=CHROME, args=args)
    if mode in ("contrast", "contrast-nomask"):
        q = "?live" + ("&nomask" if mode.endswith("nomask") else "")
        pg = br.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(deck.as_uri() + q); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(500)
        pg.evaluate("css => { const st = document.createElement('style'); st.id = 'hide'; st.textContent = css; document.head.appendChild(st); }", HIDE)
        n = pg.locator(".slide").count(); overall = 99; report = []
        for k in range(n):
            pg.evaluate(f"go({(k - 1) % n})"); pg.wait_for_timeout(1200)          # settle on the previous slide
            pg.evaluate(f"go({k})")
            items = pg.evaluate(TEXT_JS); lo = 99; worst_txt = ""; t_prev = 0
            for ms in (0, 150, 300, 450, 600, 900, 1500):
                pg.wait_for_timeout(ms - t_prev); t_prev = ms
                op = pg.evaluate(OPAC_JS); img = Image.open(io.BytesIO(pg.screenshot()))
                w = worst(img, items, op)
                if w and w[0][0] < lo: lo, worst_txt = w[0][0], f"{w[0][1]} @{ms}ms"
                if ms == 1500: rest = w[0][0] if w else None
            overall = min(overall, lo); report.append(f"slide {k+1}: worst text contrast {lo}:1 ({worst_txt}) · at rest {rest}:1")
        print("\n".join(report)); print(f"MIN {overall}:1  -> {'PASS' if overall >= 4.5 else 'FAIL'} (>= 4.5:1)")
    elif mode == "text":
        pg = br.new_page(viewport={"width": 1920, "height": 1080}); pg.goto(deck.as_uri()); pg.wait_for_load_state("networkidle")
        n = pg.locator(".slide").count(); bad = 0
        for k in range(n):
            pg.evaluate(f"go({k})")
            r = pg.evaluate("""() => { const s = document.querySelector('.slide.on'); const c = s.cloneNode(true); c.querySelectorAll('.notes').forEach(x=>x.remove());
              let min = 999; const tw = document.createTreeWalker(s, NodeFilter.SHOW_TEXT);
              while (tw.nextNode()) { const el = tw.currentNode.parentElement; if (!tw.currentNode.textContent.trim() || el.closest('.notes')) continue;
                const fs = parseFloat(getComputedStyle(el).fontSize) * (el.closest('svg') ? el.closest('svg').getBoundingClientRect().width / 900 : 1); min = Math.min(min, fs); }
              return { text: c.textContent, min: Math.round(min*10)/10, todo: s.querySelectorAll('.todo').length }; }""")
            d = re.findall("[—–]", r["text"]); e = EMOJI.findall(r["text"])
            bad += len(d) + len(e) + (r["min"] < 30)
            print(f"slide {k+1}: dashes={len(d)} emoji={len(e)} min_font={r['min']}px placeholder={r['todo']}")
        print("PASS" if bad == 0 else f"FAIL ({bad})")
    elif mode == "fps":
        pg = br.new_page(viewport={"width": 1920, "height": 1080}); pg.goto(deck.as_uri() + "?live"); pg.wait_for_load_state("networkidle")
        n = pg.locator(".slide").count()
        print("renderer:", pg.evaluate("()=>{const g=document.createElement('canvas').getContext('webgl2');const x=g&&g.getExtension('WEBGL_debug_renderer_info');return x?g.getParameter(x.UNMASKED_RENDERER_WEBGL):'?'}"))
        for k in range(n):
            pg.evaluate(f"go({k})"); pg.wait_for_timeout(1000)
            c = pg.evaluate("()=>new Promise(r=>{let n=0;const t0=performance.now();(function f(){n++;if(performance.now()-t0<3000)requestAnimationFrame(f);else r(n)})()})")
            print(f"slide {k+1}: {c} frames / 3 s = {c/3:.1f} fps")
    elif mode == "reduced":
        pg = br.new_page(viewport={"width": 1920, "height": 1080}, reduced_motion="reduce"); pg.goto(deck.as_uri() + "?live"); pg.wait_for_load_state("networkidle")
        pg.evaluate("go(2)"); pg.wait_for_timeout(1500)
        print("world:", pg.evaluate("()=>window.__world&&window.__world.ok"), "loop frames after 1.5 s:", pg.evaluate("()=>window.__world.frames()"))
        pg.screenshot(path=str(deck.parent / "checks" / "rm3.png"))
    elif mode == "neg":
        pg = br.new_page(viewport={"width": 1920, "height": 1080}); fails = []
        pg.on("requestfailed", lambda r: fails.append(r.url)); resp = []
        pg.on("response", lambda r: resp.append((r.status, r.url)) if "jsdelivr" in r.url else None)
        pg.goto(deck.as_uri()); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
        print("cdn responses:", resp, "failed:", [u for u in fails if "jsdelivr" in u])
        print("window.__world =", pg.evaluate("()=>typeof window.__world==='undefined'?'undefined':JSON.stringify(window.__world)"))
        n = pg.locator(".slide").count()
        for k in range(n):
            pg.evaluate(f"go({k})"); pg.wait_for_timeout(200)
            t = pg.evaluate("()=>{const s=document.querySelector('.slide.on');const c=s.cloneNode(true);c.querySelectorAll('.notes').forEach(x=>x.remove());return c.textContent.replace(/\\s+/g,' ').trim()}")
            vis = pg.evaluate("()=>{const h=document.querySelector('.slide.on h1,.slide.on h2,.slide.on .name');const b=h.getBoundingClientRect();return getComputedStyle(h).opacity+' '+Math.round(b.width)}")
            pg.screenshot(path=str(deck.parent / f"neg{k+1}.png"))
            print(f"slide {k+1}: chars={len(t)} heading opacity/width={vis} :: {t[:40]}")
    br.close()
