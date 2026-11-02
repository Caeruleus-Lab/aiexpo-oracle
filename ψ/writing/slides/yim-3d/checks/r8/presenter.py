# P opens a separate notes window that follows the slide; arrow keys inside it drive the deck.
import sys,pathlib
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
deck=pathlib.Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080}); pg.goto(deck.as_uri()+"#5"); pg.wait_for_load_state("networkidle")
    with pg.expect_popup() as pop: pg.keyboard.press("p")
    w=pop.value; w.wait_for_timeout(300)
    print("popup slide 5:", w.inner_text("#c"), "|", w.inner_text("#n")[:70].replace("\n"," "), "|", w.inner_text("#x"))
    w.keyboard.press("ArrowRight"); w.wait_for_timeout(300)
    print("after ArrowRight in popup:", w.inner_text("#c"), "| deck hash", pg.evaluate("location.hash"), "|", w.inner_text("#n")[:40].replace("\n"," "))
    print("projector notes hidden:", pg.evaluate("getComputedStyle(document.querySelector('.slide.on .notes')).display"))
    b.close()
