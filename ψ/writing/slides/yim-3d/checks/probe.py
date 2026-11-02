import sys,pathlib,json
from playwright.sync_api import sync_playwright
f=pathlib.Path(sys.argv[1]).resolve(); k=int(sys.argv[2])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
    pg=b.new_page(viewport={"width":1920,"height":1080}); logs=[]
    pg.on("console",lambda m:logs.append(m.text)); pg.on("pageerror",lambda e:logs.append(str(e)))
    pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.evaluate(f"go({k})"); pg.wait_for_timeout(400)
    print(pg.evaluate("()=>JSON.stringify(window.__world.dbg())"));print(pg.evaluate("()=>[...document.querySelectorAll('.slide.on .anc')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height].map(Math.round)})"))
    print(logs)
    b.close()
