"""Screenshots of the relic5 hub UI on white (tailnet), with every private text blurred in the page before the shot:
session text, search words, project, repo and people names, tokens. Headings, labels, numbers and charts stay.
Usage: uv run --with playwright python captures/ui_capture.py      AIExpo Oracle (Oracle AI), 2026-11-04."""
import pathlib, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent.parent; IMG = HERE / "images"
HUB = "http://white.follow-rankine.ts.net:8795/"
BLUR = "filter:blur(7px)!important;"
# (file, tab, css to blur private text, js to run first, scroll y)
# A box of the page blurred as a whole, in page pixels (x, y, w, h): for cards whose text is private
BOX = {"01-home": [(40, 770, 1160, 230)], "02-search": [(40, 250, 1520, 750)], "04-knowledge": [(0, 640, 1600, 360)],
       "05-oracles": [(40, 860, 1520, 140)]}
SHOTS = [
 ("01-home", "", "main section:has(h2) li, main [class*=cloud] *, main a[href*='q='], main ul li", "", 0),
 ("02-search", "search", "main article, main li, main select, main table, main [role=listitem]", "S", 0),
 ("03-live", "live", "main tbody td:nth-child(n+4), main tbody td:nth-child(4)", "", 0),
 ("04-knowledge", "memory", "main li, main article, main a, main select, main table", "", 0),
 ("05-oracles", "oracles", "main li, main article, main a, main table", "", 0),
 ("06-map", "map", "main li, main table, main [class*=legend] *, main aside *", "", 0),
 ("07-family", "family", "main li, main table, main svg text", "", 0),
 ("08-asked", "queries", "main table, main li", "", 0),
 ("09-jobs", "jobs", "main tbody td:last-child", "", 0),
 ("10-perf", "perf", "", "", 0),
 ("11-quality", "compare", "", "", 0),
 ("12-disk", "store", "", "", 0),
 ("13-connect", "connect", "", "", 0),
 ("14-settings", "settings", "main table, main li, main input", "", 0),
]
only = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1600, "height": 1000})
    for name, tab, css, js, y in SHOTS:
        if only and name not in only: continue
        pg.goto(HUB + (f"#tab={tab}" if tab else "")); pg.wait_for_timeout(5000)
        pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(3000)
        # the "open incidents" panel floats over every page: take it out of this screenshot
        pg.evaluate("""() => { for (const e of document.querySelectorAll('body *')) { const cs = getComputedStyle(e);
            if ((cs.position === 'fixed' || cs.position === 'absolute') && /open\\s*incidents/i.test(e.textContent || '') && e.offsetHeight > 200) e.remove() } }""")
        if js == "S":   # a search everyone may see: the words of this public workshop
            box = pg.query_selector("main input[type=search], main input")
            box.fill("AIExpo workshop"); box.press("Enter"); pg.wait_for_timeout(4000)
        if css: pg.add_style_tag(content=f"{css}{{{BLUR}}}")
        for x, y0, w, h in BOX.get(name, []):
            pg.evaluate(f"""() => {{ const d = document.createElement('div'); d.style.cssText = 'position:fixed;left:{x}px;top:{y0}px;width:{w}px;height:{h}px;backdrop-filter:blur(9px);-webkit-backdrop-filter:blur(9px);z-index:99;border-radius:12px'; document.body.appendChild(d) }}""")
        pg.add_style_tag(content=".max-\\[1100px\\]\\:hidden{} ")
        if y: pg.evaluate(f"window.scrollTo(0,{y})")
        pg.wait_for_timeout(600); pg.screenshot(path=str(IMG / f"{name}.png"))
        print("shot", name)
    b.close()
