# Round 8: space and composition audit, one row per slide.
# usage: python3 checks/r8/space.py deck.html out.json [WxH]
# Boxes come from three sources, measured, not eyeballed:
#   text    = DOM boxes of h1,h2,p,.label,.num,svg text (stage px)
#   diagram = DOM boxes of svg rect/circle/path (stage px)
#   world   = ink pixels of the 3D print alone (#stage hidden), so the formation's projected box is what was printed
#   ink     = ink pixels of the full screenshot (text + diagram + 3D), used for centre of mass, empty bands and the
#             largest empty rectangle. Chrome (counter, still button) and the progress bar are masked out.
# Every number is in stage px (1920x1080), whatever the viewport.
import sys, json, pathlib, io
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright

CHROME = "/Users/yim/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
f = pathlib.Path(sys.argv[1]).resolve(); out = sys.argv[2]
VW, VH = (int(x) for x in (sys.argv[3] if len(sys.argv) > 3 else "1920x1080").split("x"))
W, H, CELL = 1920, 1080, 20   # empty-rectangle grid: 20 stage px cells (96 x 54)

def ink_mask(png, sr):
    im = np.asarray(Image.open(io.BytesIO(png)).convert("RGB")).astype(np.int16)
    x0, y0, s = sr["x"], sr["y"], sr["s"]
    # crop the stage and resample to 1920x1080 so every slide is measured in stage px
    crop = Image.fromarray(im[int(round(y0)):int(round(y0 + H * s)), int(round(x0)):int(round(x0 + W * s))].astype(np.uint8)).resize((W, H), Image.NEAREST)
    a = np.asarray(crop).astype(np.int16)
    bg = np.median(a[300:900:7, 40:120:3].reshape(-1, 3), axis=0)   # paper tone from the left margin band
    # ink is darker than the sheet: every Rikyu ink (kuro, moss, sabi on shiro) and the text are; the paper fibre,
    # the old flood streaks (~20 levels) and the riso speckle (lighter) are not
    lum = a @ np.array([0.299, 0.587, 0.114]); d = float(bg @ np.array([0.299, 0.587, 0.114])) - lum
    m = d > 36
    m[H - 12:, :] = False                 # progress bar
    m[H - 60:, W - 160:] = False          # chrome
    m[80:100, 130:270] = False            # lamp rule (same on every slide, not content)
    # drop paper/flood speckle: keep a pixel only if its 4x4 block is at least 3/8 ink (text, rules and dithered
    # blocks pass; a lone 2x2 speck of the riso flood does not)
    blk = m.reshape(H // 4, 4, W // 4, 4).sum(axis=(1, 3)) >= 6
    return np.repeat(np.repeat(blk, 4, axis=0), 4, axis=1) & m

def bbox(m):
    ys, xs = np.nonzero(m)
    if len(xs) == 0: return None
    return dict(l=int(xs.min()), t=int(ys.min()), r=int(xs.max()) + 1, b=int(ys.max()) + 1)

def union(bs):
    bs = [b for b in bs if b]
    if not bs: return None
    return dict(l=min(b["l"] for b in bs), t=min(b["t"] for b in bs), r=max(b["r"] for b in bs), b=max(b["b"] for b in bs))

def runs(v):
    """longest run of True in a 1-D bool array -> (start, length)"""
    best = (0, 0); s = None
    for k, x in enumerate(list(v) + [False]):
        if x and s is None: s = k
        if not x and s is not None:
            if k - s > best[1]: best = (s, k - s)
            s = None
    return best

def max_empty_rect(m):
    g = m.reshape(H // CELL, CELL, W // CELL, CELL).any(axis=(1, 3))   # True = some ink in the cell
    R, C = g.shape; h = np.zeros(C, int); best = (0, None)
    for r in range(R):
        h = np.where(g[r], 0, h + 1)
        st = []
        for c in range(C + 1):
            cur = h[c] if c < C else 0
            while st and h[st[-1]] >= cur:
                top = st.pop(); left = st[-1] + 1 if st else 0
                area = h[top] * (c - left)
                if area > best[0]: best = (area, dict(l=left * CELL, r=c * CELL, t=(r - h[top] + 1) * CELL, b=(r + 1) * CELL))
            st.append(c)
    return best[1]

rows = []
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME)
    pg = b.new_page(viewport={"width": VW, "height": VH})
    pg.goto(f.as_uri()); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(400)
    n = pg.locator(".slide").count()
    for k in range(n):
        pg.evaluate(f"go({k})"); pg.wait_for_timeout(350)
        dom = pg.evaluate("""()=>{const st=document.getElementById('stage'),sr=st.getBoundingClientRect(),sc=sr.width/1920,s=document.querySelector('.slide.on');
          const bx=e=>{const b=e.getBoundingClientRect();return {l:(b.left-sr.left)/sc,t:(b.top-sr.top)/sc,r:(b.right-sr.left)/sc,b:(b.bottom-sr.top)/sc}};
          const ok=b=>b.r-b.l>0.5&&b.b-b.t>0.5;
          return {sr:{x:sr.left,y:sr.top,s:sc},
            text:[...s.querySelectorAll('h1,h2,p,.label,.num,svg text')].map(bx).filter(ok),
            diagram:[...s.querySelectorAll('svg rect,svg circle,svg path')].map(bx).filter(ok),
            overlaps:(()=>{const L=[...s.querySelectorAll('h1,h2,p,.label,.num,svg text')].filter(e=>e.getClientRects().length).map(e=>[e,bx(e)]);const o=[];
              for(let a=0;a<L.length;a++)for(let c=a+1;c<L.length;c++){const [ea,A]=L[a],[ec,C]=L[c];if(ea.contains(ec)||ec.contains(ea))continue;
                const w=Math.min(A.r,C.r)-Math.max(A.l,C.l),h=Math.min(A.b,C.b)-Math.max(A.t,C.t);if(w>4&&h>4)o.push((ea.textContent.slice(0,14)+' x '+ec.textContent.slice(0,14)).trim())}return o})()}}""")
        full = pg.screenshot()
        pg.add_style_tag(content="#stage{visibility:hidden!important}#chrome{display:none}")
        world = pg.screenshot()
        pg.evaluate("document.querySelectorAll('style').forEach(s=>{if(s.textContent.startsWith('#stage{visibility:hidden'))s.remove()})")
        sr = dom["sr"]
        mi = ink_mask(full, sr); mw = ink_mask(world, sr)
        tb = union([{kk: int(round(v)) for kk, v in x.items()} for x in dom["text"]])
        db = union([{kk: int(round(v)) for kk, v in x.items()} for x in dom["diagram"]])
        wb = bbox(mw)
        allb = union([tb, db, wb])
        ys, xs = np.nonzero(mi)
        com = (float(xs.mean()), float(ys.mean())) if len(xs) else (W / 2, H / 2)
        rowe = ~mi.any(axis=1); cole = ~mi.any(axis=0)
        hr = runs(rowe); vr = runs(cole)
        er = max_empty_rect(mi)
        era = (er["r"] - er["l"]) * (er["b"] - er["t"]) / (W * H) if er else 0
        row = dict(slide=k + 1,
                   used_pct=round(100 * (allb["r"] - allb["l"]) * (allb["b"] - allb["t"]) / (W * H), 1),
                   margins=dict(L=allb["l"], R=W - allb["r"], T=allb["t"], B=H - allb["b"]),
                   text=tb, diagram=db, world=wb,
                   com_dx=round(com[0] - W / 2), com_dy=round(com[1] - H / 2),
                   empty_row_band=dict(y=hr[0], h=hr[1], pct=round(100 * hr[1] / H, 1)),
                   empty_col_band=dict(x=vr[0], w=vr[1], pct=round(100 * vr[1] / W, 1)),
                   max_empty_rect=dict(**er, pct=round(100 * era, 1)) if er else None)
        row["overlaps"] = dom["overlaps"]
        rows.append(row)
        flags = [f"OVERLAP {o}" for o in dom["overlaps"]]
        if row["empty_row_band"]["pct"] > 25: flags.append(f"ROWBAND {row['empty_row_band']['pct']}% at y{hr[0]}")
        if row["empty_col_band"]["pct"] > 25: flags.append(f"COLBAND {row['empty_col_band']['pct']}% at x{vr[0]}")
        print(f"{k+1} used {row['used_pct']}% · L{allb['l']} R{W-allb['r']} T{allb['t']} B{H-allb['b']} · com dx{row['com_dx']} dy{row['com_dy']} · "
              f"rowband {row['empty_row_band']['pct']}% colband {row['empty_col_band']['pct']}% · max empty rect {row['max_empty_rect']['pct']}% "
              f"{er['l']},{er['t']}-{er['r']},{er['b']} · world {wb} {' '.join(flags)}")
    b.close()
json.dump(rows, open(out, "w"), indent=1, default=int)
