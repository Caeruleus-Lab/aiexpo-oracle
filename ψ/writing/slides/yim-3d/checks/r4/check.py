# Round 4 checks (copied from r3, unchanged logic): offline (all http/https aborted), fonts, 3D, type sizes, contrast, dashes, nav, still mode.
import sys,pathlib,json
from playwright.sync_api import sync_playwright
deck=pathlib.Path(sys.argv[1]).resolve(); out=pathlib.Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
CH="/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=CH); ctx=b.new_context(viewport={"width":1920,"height":1080})
    aborted=[]; local=[]
    def route(r):
        u=r.request.url
        if u.startswith(('http://','https://')): aborted.append(u); r.abort()
        else: local.append(u.rsplit('/',1)[-1]); r.continue_()
    ctx.route('**/*',route)
    pg=ctx.new_page(); errs=[]; pg.on('console',lambda m: m.type in('error','warning') and errs.append(m.text))
    pg.goto(deck.as_uri()+'?live'); pg.wait_for_timeout(1500)
    n=pg.locator('.slide').count()
    for k in range(n):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(1300)
        r=pg.evaluate("""()=>{
          const s=document.querySelector('.slide.on'), sc=document.getElementById('stage').getBoundingClientRect().width/1920;
          let min=1e9,minWho='';
          s.querySelectorAll('p,span,div,h1,h2,b,text').forEach(e=>{
            if(e.closest('.notes'))return; const own=[...e.childNodes].some(c=>c.nodeType===3&&c.textContent.trim()); if(!own)return;
            let fs=parseFloat(getComputedStyle(e).fontSize);
            if(e instanceof SVGElement){fs=fs*e.getScreenCTM().a/sc}
            if(fs<min){min=fs;minWho=e.textContent.trim().slice(0,24)}});
          const faces=[...document.fonts].filter(f=>/Bai Jamjuree|Sarabun/.test(f.family)).map(f=>f.family.replace(/"/g,'')+' '+f.weight+' '+f.status);
          const w=window.__world;
          return {min:Math.round(min*10)/10,minWho,fontsCheck:document.fonts.check('40px "Bai Jamjuree"')&&document.fonts.check('36px "Sarabun"'),
                  loadedFaces:faces.filter(x=>x.endsWith(' loaded')).length, errorFaces:faces.filter(x=>x.endsWith('error')).length,
                  world:!!w, frames:w?w.frames():null, faces}}""")
        f0=r['frames']; pg.wait_for_timeout(400); r['framesAdvancing']=(pg.evaluate("window.__world?window.__world.frames():null") or 0)>(f0 or 0)
        pg.screenshot(path=str(out/f"o{k+1}.png")); print(k+1,json.dumps(r,ensure_ascii=False))
    # contrast of the secondary inks on paper (resolved by the browser, WCAG formula)
    c=pg.evaluate("""()=>{const cv=document.createElement('canvas').getContext('2d');const rs=getComputedStyle(document.documentElement);
      const rgb=n=>{cv.fillStyle=rs.getPropertyValue(n).trim();cv.fillRect(0,0,1,1);return [...cv.getImageData(0,0,1,1).data].slice(0,3)};
      const L=a=>{const f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4};return .2126*f(a[0])+.7152*f(a[1])+.0722*f(a[2])};
      const cr=(a,b)=>{const x=L(rgb(a)),y=L(rgb(b));return Math.round((Math.max(x,y)+.05)/(Math.min(x,y)+.05)*100)/100};
      return {ink:cr('--color-ink','--color-paper'),ink2:cr('--color-ink-2','--color-paper'),ink3:cr('--color-ink-3','--color-paper'),accent:cr('--color-accent','--color-paper'),amberInk:cr('--color-accent-ink','--color-accent')}}""")
    print('contrast',c)
    dash=pg.evaluate("[...document.querySelectorAll('.slide')].map(s=>s.textContent).join(' ').match(/[—–]/g)?.length||0")
    print('dashes in all slide text incl. notes:',dash)
    # nav: same-slide go() must not re-emit; held key must not skip; S toggles still and stops the loop
    nav=None if not pg.evaluate('!!window.__world') else pg.evaluate("""async()=>{let ev=0;addEventListener('slide',()=>ev++);go(2);const a=ev;go(2);go(2);const b=ev;
      dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',repeat:true}));const afterRepeat=window.__slide;
      dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight'}));const afterPress=window.__slide;
      dispatchEvent(new KeyboardEvent('keydown',{key:'s'}));const f1=window.__world.frames();await new Promise(r=>setTimeout(r,500));const f2=window.__world.frames();
      const btn=document.getElementById('still').textContent, still=window.__world.still();
      dispatchEvent(new KeyboardEvent('keydown',{key:'s'}));await new Promise(r=>setTimeout(r,500));const f3=window.__world.frames();
      return {eventsFirstGo:a,eventsAfterTwoSameGo:b-a,slideAfterRepeatKey:afterRepeat,slideAfterRealKey:afterPress,
              stillOn:still,button:btn,framesWhileStill:f2-f1,framesAfterResume:f3-f2}}""")
    print('nav',json.dumps(nav,ensure_ascii=False))
    print('aborted http(s) requests:',len(aborted),aborted[:3]); print('local files loaded:',sorted(set(local)))
    print('console warnings/errors:',errs[:5])
    b.close()
