# screenshot mid-transition (live) 7 -> 8 and 4 -> 5 at 350 ms
import pathlib
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(pathlib.Path('deck.html').resolve().as_uri()+'?live#7'); pg.wait_for_timeout(2000)
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(350); pg.screenshot(path='checks/r6/mid78.png')
    pg.evaluate('go(3)'); pg.wait_for_timeout(2000); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(350); pg.screenshot(path='checks/r6/mid45.png')
    b.close()
