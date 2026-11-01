import sys,pathlib
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
f=pathlib.Path(sys.argv[1]).resolve(); k=int(sys.argv[2]); sel=sys.argv[3]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate(f"go({k-1})"); pg.wait_for_timeout(300)
    print(pg.evaluate("q=>[...document.querySelectorAll('.slide.on '+q)].map(e=>{const r=e.getBoundingClientRect();return [e.tagName+'.'+e.className.baseVal??e.className, Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)].join(' ')})",sel))
    print(pg.evaluate("JSON.stringify(window.__world&&__world.dbg&&{N:__world.dbg().N,L:__world.dbg().LEARNED,C:__world.dbg().CHOSEN,ok:__world.ok})"))
    b.close()
