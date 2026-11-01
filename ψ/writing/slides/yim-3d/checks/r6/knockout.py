# Round 6 text exclusion check. Hides every word (visibility only, layout kept), screenshots each slide and counts
# printed ink pixels inside the word boxes (the boxes the knockout uses, without the pad).
# Ink pixel = colour more than 40 (RGB distance) from the slide's median paper colour.
# usage: knockout.py deck.html [query]   "?decoy" puts a big kuro block under each heading; add "&nomask" to switch the knockout off
import sys,pathlib,json
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
deck=pathlib.Path(sys.argv[1]).resolve(); q=sys.argv[2] if len(sys.argv)>2 else ''
out=pathlib.Path('checks/r6/knockout'); out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":1920,"height":1080})
    pg.goto(deck.as_uri()+q); pg.wait_for_timeout(1200); res=[]
    for k in range(8):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(400)
        boxes=pg.evaluate("""()=>[...document.querySelector('.slide.on').querySelectorAll('h1,h2,p,.label,.num,svg text')].map(e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom].map(Math.round)})""")
        pg.add_style_tag(content='.slide.on *{visibility:hidden!important}')
        f=out/f"k{k+1}{q.replace('?','_').replace('&','_')}.png"; pg.screenshot(path=str(f))
        pg.evaluate("document.querySelectorAll('style').forEach((s,i,a)=>{if(i===a.length-1)s.remove()})")
        a=np.asarray(Image.open(f).convert('RGB')).astype(float); bg=np.median(a.reshape(-1,3),axis=0)
        ink=np.linalg.norm(a-bg,axis=2)>40; n=0; area=0
        for l,t,r,bo in boxes: n+=int(ink[max(0,t):bo,max(0,l):r].sum()); area+=max(0,r-l)*max(0,bo-t)
        res.append(n)
    print(json.dumps({'query':q or '(none)','ink_px_under_words_per_slide':res,'total':sum(res)}))
    b.close()
