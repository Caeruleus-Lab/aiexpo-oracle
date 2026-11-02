# Live (not capture) run of slide 4: screenshot right after arrival and after the 17 settle; count anchors.
import sys,pathlib,json
from playwright.sync_api import sync_playwright
deck=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(deck.as_uri()+'?live#3'); pg.wait_for_timeout(1500)
    pg.evaluate("go(3)"); pg.wait_for_timeout(700); pg.screenshot(path=str(out/'s4-t0.7.png'))
    pg.wait_for_timeout(3300); pg.screenshot(path=str(out/'s4-t4.0.png'))
    d=pg.evaluate("window.__world.dbg()"); print('slide',d['cur']+1,'anchors',len(d['anchors']))
    b.close()
