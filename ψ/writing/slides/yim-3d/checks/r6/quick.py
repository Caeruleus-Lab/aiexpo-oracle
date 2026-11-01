# Round 6 quick look: live mode, wait, screenshot each slide, print console errors and world info.
import sys,pathlib,json
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
deck=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
W,H=(int(x) for x in (sys.argv[3] if len(sys.argv)>3 else '1920x1080').split('x')); q=sys.argv[4] if len(sys.argv)>4 else '?live'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":W,"height":H}); errs=[]
    pg.on('console',lambda m: m.type in('error','warning') and errs.append(m.text)); pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto(deck.as_uri()+q); pg.wait_for_timeout(1200)
    print('world',pg.evaluate("window.__world&&window.__world.info()"))
    for k in range(pg.locator('.slide').count()):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(int(sys.argv[5]) if len(sys.argv)>5 else 2500)
        pg.screenshot(path=str(out/f"q{k+1}.png"))
    print('errors',errs[:6]); b.close()
