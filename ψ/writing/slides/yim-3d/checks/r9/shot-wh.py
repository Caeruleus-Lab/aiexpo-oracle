# Round 9: ../r5/shot.py with the viewport as argv 3 and 4 (the r5 copy is pinned at 1920x1080).
# Copy of the round-3/4 shot.py (scratchpad .../5aabf861.../scratchpad/shot.py), pinned here in round 5 because the
# scratchpad copy was overwritten by another session at 14:34 on 2026-11-01. Logic unchanged.
import sys,pathlib
from playwright.sync_api import sync_playwright
f=pathlib.Path(sys.argv[1]).resolve(); out=sys.argv[2]; W,H=int(sys.argv[3]),int(sys.argv[4])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"); pg=b.new_page(viewport={"width":W,"height":H})
    pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle")
    n=pg.locator(".slide").count()
    for k in range(n):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(300)
        over=pg.evaluate("""()=>{const s=document.querySelector('.slide.on');const r=[];s.querySelectorAll('h1,h2,h3,p,span,div').forEach(e=>{if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible')r.push(e.className);const b=e.getBoundingClientRect();if(b.right>1922||b.bottom>1082)r.push('OUT:'+e.tagName+'.'+e.className)});return r}""")
        pg.screenshot(path=f"{out}/b{k+1}.png"); print(k+1,over)
    b.close()
