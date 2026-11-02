# landing knockout: dark (ink) px inside the hero h1 box with ?decoy vs ?decoy&nomask (words hidden, boxes kept)
import pathlib,os,sys
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np
f=pathlib.Path(sys.argv[1]).resolve(); out='/tmp/kl.png'
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ['RISO_CHROME'])
    for w,h,d in [(1280,800,1),(390,844,3)]:
        for q in ['?flat','?flat&decoy','?flat&decoy&nomask']:
            pg=b.new_page(viewport={'width':w,'height':h},device_scale_factor=d); pg.goto(f.as_uri()+q); pg.wait_for_timeout(900)
            pg.add_style_tag(content='h1{color:transparent!important}'); pg.evaluate('__riso.mounts[0].redraw()'); pg.wait_for_timeout(100)
            r=pg.evaluate("(()=>{const b=document.querySelector('h1').getBoundingClientRect();return [b.left,b.top,b.right,b.bottom]})()")
            pg.screenshot(path=out); a=np.asarray(Image.open(out).convert('RGB')).astype(float)
            c=a[round(r[1]*d):round(r[3]*d),round(r[0]*d):round(r[2]*d)]
            print(f'{w}x{h}@{d}',q,'dark px in h1 box:',int((c.mean(axis=2)<80).sum())); pg.close()
    b.close()
