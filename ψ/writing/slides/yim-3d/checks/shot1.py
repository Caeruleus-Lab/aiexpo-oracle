import sys,pathlib
from playwright.sync_api import sync_playwright
f=pathlib.Path(sys.argv[1]).resolve(); k=int(sys.argv[2]); q=sys.argv[3] if len(sys.argv)>3 else ''; o=sys.argv[4] if len(sys.argv)>4 else 'dbg.png'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing")
    pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(f.as_uri()+q); pg.wait_for_load_state("networkidle"); pg.evaluate(f"go({k})"); pg.wait_for_timeout(400)
    pg.screenshot(path=o); b.close()
