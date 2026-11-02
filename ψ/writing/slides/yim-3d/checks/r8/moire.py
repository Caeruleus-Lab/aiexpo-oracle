# Round 6 moire check. Prints the Riso canvas without grain (?flat), hides every word, screenshots each slide,
# then measures horizontal and vertical runs of kuro-dark pixels inside the stage. If the dots map 1:1 to device
# pixels, every run is a whole number of cells (run % cell == 0). Browser resampling breaks that.
# usage: moire.py deck.html WxH [extra-query]   e.g. "&fixed1920" = negative control (canvas 1920 drawn at 1280)
import sys,pathlib,json
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
deck=pathlib.Path(sys.argv[1]).resolve(); W,H=(int(x) for x in sys.argv[2].split('x')); extra=sys.argv[3] if len(sys.argv)>3 else ''
out=pathlib.Path('checks/r8/moire'); out.mkdir(parents=True,exist_ok=True)
def runs(row):
    r=[];n=0
    for v in row:
        if v: n+=1
        elif n: r.append(n); n=0
    if n: r.append(n)
    return r
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); pg=b.new_page(viewport={"width":W,"height":H})
    pg.goto(deck.as_uri()+'?flat'+extra); pg.wait_for_timeout(1200)
    pg.add_style_tag(content='.slide *{visibility:hidden!important} #chrome,#prog{display:none!important} .slide::before{display:none}')
    info=pg.evaluate('__world.info()'); cell=info['cell'] if not extra else round(info['cell']*W/1920)
    st=pg.evaluate("(()=>{const r=document.getElementById('stage').getBoundingClientRect();return [r.left,r.top,r.right,r.bottom].map(Math.round)})()")
    tot_ok=tot=0; per=[]
    for k in range(8):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(500)
        f=out/f"m{W}{'-neg' if extra else ''}-{k+1}.png"; pg.screenshot(path=str(f))
        a=np.asarray(Image.open(f).convert('RGB')).astype(float)[st[1]+8:st[3]-8, st[0]+8:st[2]-8]
        dark=(a.mean(axis=2)<80)
        rs=[x for row in dark for x in runs(row)]+[x for col in dark.T for x in runs(col)]
        ok=sum(1 for x in rs if x%cell==0); tot_ok+=ok; tot+=len(rs); per.append(round(ok/max(1,len(rs)),3))
    print(json.dumps({'viewport':f'{W}x{H}','query':'?flat'+extra,'canvas':[info['canvasW'],info['canvasH']],'cell_device_px':cell,
                      'runs':tot,'runs_whole_cells':round(tot_ok/max(1,tot),4),'per_slide':per}))
    b.close()
