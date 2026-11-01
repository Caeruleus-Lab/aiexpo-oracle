# mid-move frames for eyeballing motion: slide a -> b, screenshots at given ms (live mode)
import sys,pathlib
from playwright.sync_api import sync_playwright
CHROME="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
f=pathlib.Path(sys.argv[1]).resolve(); a,b=int(sys.argv[2]),int(sys.argv[3]); out=sys.argv[4]
with sync_playwright() as p:
    br=p.chromium.launch(executable_path=CHROME); pg=br.new_page(viewport={"width":1920,"height":1080})
    pg.goto(f.as_uri()+"?live"); pg.wait_for_load_state("networkidle"); pg.evaluate(f"go({a})"); pg.wait_for_timeout(1500)
    pg.evaluate(f"go({b})"); t=0
    for ms in (250,500):
        pg.wait_for_timeout(ms-t); t=ms; pg.screenshot(path=f"{out}-{ms}.png")
    br.close()
