# frames per second in live mode, per slide, over 3 s each (Apple M4, headless Chromium)
import pathlib
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(pathlib.Path('deck.html').resolve().as_uri()+'?live'); pg.wait_for_timeout(1000); r=[]
    for k in range(8):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(1000)
        r.append(round(pg.evaluate("new Promise(res=>{const f=__world.frames(),t=performance.now();setTimeout(()=>res((__world.frames()-f)/(performance.now()-t)*1000),3000)})"),1))
    print('fps',r,'renderer',pg.evaluate('__world.renderer()')); b.close()
