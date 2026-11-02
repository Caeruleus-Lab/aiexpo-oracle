import sys,pathlib
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
f=pathlib.Path(sys.argv[1]).resolve(); q=sys.argv[2] if len(sys.argv)>2 else ""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080})
    msgs=[]; pg.on("console",lambda m:msgs.append(m.type+": "+m.text)); pg.on("pageerror",lambda e:msgs.append("pageerror: "+str(e)))
    pg.goto(f.as_uri()+q); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(500)
    for k in range(8): pg.evaluate(f"go({k})"); pg.wait_for_timeout(150)
    print(pg.evaluate("JSON.stringify(window.__world===false?false:{ok:__world.ok,info:__world.info(),dbg:(({N,LEARNED,CHOSEN})=>({N,LEARNED,CHOSEN}))(__world.dbg())})"))
    print("\n".join(msgs) or "console: (empty)")
    b.close()
