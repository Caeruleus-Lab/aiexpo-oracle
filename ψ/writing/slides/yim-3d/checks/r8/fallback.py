# Round 8 negative controls: (1) WebGL lost on slide 8 -> the deck drops the canvas and shows opaque CSS paper;
# restore + W brings the print back. (2) W toggles the print. (3) slide 4 arrows: no 3D ink inside the arrow boxes,
# and the same count goes non-zero with ?nomask (proves the measure can see ink there).
import sys,pathlib,json,io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
deck=pathlib.Path(sys.argv[1]).resolve(); out=sys.argv[2]
ST="""()=>({world:window.__world===false?false:!!(window.__world&&window.__world.ok),cls:document.documentElement.className,
  canvas:getComputedStyle(document.getElementById('world')).display,stageBg:getComputedStyle(document.getElementById('stage')).backgroundColor})"""
def arrow_ink(pg):
    boxes=pg.evaluate("""()=>{const sr=document.getElementById('stage').getBoundingClientRect(),sc=sr.width/1920;return [...document.querySelectorAll('.slide.on .arch .d-arc')].map(e=>{const b=e.getBoundingClientRect();return [(b.left-sr.left)/sc,(b.top-sr.top)/sc,(b.right-sr.left)/sc,(b.bottom-sr.top)/sc]})}""")
    pg.add_style_tag(content="#stage{visibility:hidden!important}#chrome{display:none}")
    a=np.asarray(Image.open(io.BytesIO(pg.screenshot())).convert("L")).astype(int)
    bg=np.median(a[300:900,40:120]); tot=0
    for l,t,r,b in boxes:
        tot+=int(((bg-a[int(t)-4:int(b)+4,int(l)-4:int(r)+4])>36).sum())
    return len(boxes),tot
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH)
    pg=b.new_page(viewport={"width":1920,"height":1080}); pg.goto(deck.as_uri()+"#8"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(500)
    print("start  ",pg.evaluate(ST))
    pg.evaluate("window.__lc=document.getElementById('world').getContext('webgl2').getExtension('WEBGL_lose_context'); __lc.loseContext()"); pg.wait_for_timeout(400)
    s=pg.evaluate(ST); print("lost   ",s); pg.screenshot(path=f"{out}/lost-s8.png")
    pg.keyboard.press("w"); pg.wait_for_timeout(200); print("W while lost",pg.evaluate(ST))
    pg.evaluate("__lc.restoreContext()"); pg.wait_for_timeout(600); print("restored",pg.evaluate(ST))
    pg.keyboard.press("w"); pg.wait_for_timeout(500); print("W after restore",pg.evaluate(ST)); pg.screenshot(path=f"{out}/restored-s8.png")
    pg.keyboard.press("w"); pg.wait_for_timeout(300); print("W off  ",pg.evaluate(ST)); pg.screenshot(path=f"{out}/woff-s8.png")
    pg.keyboard.press("w"); pg.wait_for_timeout(300); print("W on   ",pg.evaluate(ST))
    pg.close()
    for d,q in [(deck,""),(deck,"?nomask"),(pathlib.Path(sys.argv[3]).resolve() if len(sys.argv)>3 else deck,"")]:
        pg=b.new_page(viewport={"width":1920,"height":1080}); pg.goto(d.as_uri()+q+"#4"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(600)
        print("slide4 arrows",d.name+(q or ""),"boxes,ink px =",arrow_ink(pg)); pg.close()
    b.close()
