# Proto checks: screenshot state 1 (and state 2 after its auto-resolve), text overflow, FPS over 3 s, GL renderer, offline.
import sys,pathlib,json
from playwright.sync_api import sync_playwright
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
here=pathlib.Path(__file__).parent
names=sys.argv[1:] or ['sumi','aurora','riso']
OVER="""()=>{const out=[];const st=document.getElementById('stage').getBoundingClientRect(),sc=st.width/1920;
 document.querySelectorAll('.layer').forEach(L=>{if(+getComputedStyle(L).opacity<.5)return;
  L.querySelectorAll('p,span').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;
   if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).display!=='inline')out.push('scroll:'+e.textContent.slice(0,20));
   if(r.left<st.left-1||r.right>st.right+1||r.top<st.top-1||r.bottom>st.bottom+1)out.push('outside:'+e.textContent.slice(0,20))})});
 // sibling items in the stage grid must not overlap
 const it=[...document.querySelectorAll('.stages .item')].map(e=>e.getBoundingClientRect());
 for(let i=0;i<it.length-1;i++)[...document.querySelectorAll('.stages .item')][i].querySelectorAll('p').forEach(p=>{if(p.getBoundingClientRect().right>it[i+1].left)out.push('overlap:'+p.textContent.slice(0,20))});
 const bad=(document.getElementById('stage').innerText.match(/[—–]|ด่าน/g)||[]).length; if(bad)out.push('forbidden chars/words: '+bad);
 return out}"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH,args=['--use-angle=metal','--ignore-gpu-blocklist','--enable-gpu-rasterization'])
    ctx=b.new_context(viewport={"width":1920,"height":1080})
    aborted=[]
    ctx.route('**/*',lambda r:(aborted.append(r.request.url),r.abort()) if r.request.url.startswith(('http://','https://')) else r.continue_())
    for n in names:
        pg=ctx.new_page();errs=[];pg.on('console',lambda m:m.type=='error' and errs.append(m.text));pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto((here/f'{n}.html').as_uri());pg.wait_for_timeout(3200)
        info=pg.evaluate("()=>({gl:__proto.gl,renderer:__proto.gl?__proto.renderer():null,fonts:[document.fonts.check('40px Satoshi'),document.fonts.check('40px \"IBM Plex Sans Thai\"','ก')]})")
        f0=pg.evaluate("__proto.frames()");pg.wait_for_timeout(3000);f1=pg.evaluate("__proto.frames()")
        fps=round((f1-f0)/3,1)
        ov1=pg.evaluate(OVER);pg.screenshot(path=str(here/f'{n}.png'))
        pg.keyboard.press('ArrowRight');pg.wait_for_timeout(5200)
        g0=pg.evaluate("__proto.frames()");pg.wait_for_timeout(3000);g1=pg.evaluate("__proto.frames()")
        ov2=pg.evaluate(OVER);pg.screenshot(path=str(here/f'{n}-2.png'))
        print(n,json.dumps({**info,'fps_state1':fps,'fps_state2':round((g1-g0)/3,1),'overflow1':ov1,'overflow2':ov2,'errors':errs},ensure_ascii=False))
        pg.close()
    print('aborted network requests:',len(aborted))
