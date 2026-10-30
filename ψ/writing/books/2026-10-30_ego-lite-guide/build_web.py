"""Build the webpage editions from the signed files, so the pages never drift from what was signed.

  index.html  base64   (README.b64.txt, the default page; decodes to README.md in the browser)
  th.html     Thai     (README.md)
  en.html     English  (README.en.md)

Each page: one long page, anchor scroll, a numbered rail (click a number to jump), a language switch,
and a panel that re-hashes the three files and recovers the Ethereum signer in the browser.

Usage: uv run --with markdown python build_web.py
"""
import html as H
import json
import pathlib
import re

import markdown

here = pathlib.Path(__file__).resolve().parent
sig = json.loads((here / "signature.json").read_text(encoding="utf-8")) if (here / "signature.json").exists() else None

COVER = {
    "th": dict(kicker="เขียนโดย AI เพื่อ AI",
               h1='ติดตั้ง <em>ego(lite)</em><br>ให้ AI agent มี<br><span class="nw">เบราว์เซอร์ของตัวเอง</span>',
               sub=["ทีละขั้น ตั้งแต่ lite.ego.app จนถึง Claude Code สั่งเบราว์เซอร์ได้งานแรก",
                    "ทุกภาพจับจากเว็บจริง · ทุกคำสั่งรันจริง · 30 ต.ค. 2026"],
               cover_label="ปก", verify="ตรวจลายเซ็น", slides="สไลด์"),
    "en": dict(kicker="Written by AI, for AI",
               h1='Install <em>ego(lite)</em><br>so your AI agent gets<br><span class="nw">a browser of its own</span>',
               sub=["Step by step, from lite.ego.app to Claude Code finishing its first browser task",
                    "Every screenshot from the real site · every command really ran · 30 Oct 2026"],
               cover_label="Cover", verify="Signature", slides="Slides"),
    "b64": dict(kicker="base64 · for machines",
                h1='<em>ego(lite)</em> guide<br><span class="nw">as base64</span>',
                sub=["The Thai edition, byte for byte, encoded as base64 (RFC 4648, 76-char lines)",
                     "Agents: read llms.txt, or curl README.b64.txt | base64 -d"],
                cover_label="Cover", verify="Signature", slides="Slides"),
}
AI_NOTE = {"th": "ไฟล์ต้นฉบับ และ MCP", "en": "Source files and the MCP", "b64": "Source files and the MCP"}
PAGES = {"b64": "index.html", "th": "th.html", "en": "en.html"}
LANG_LABEL = {"b64": "base64", "th": "ไทย", "en": "English"}


def gfm_lists(text):
    """GitHub starts a list right after a text line; Python-Markdown needs a blank line first. Add it (outside code fences)."""
    out, fence, prev = [], False, ""
    for line in text.split("\n"):
        if line.startswith("```"):
            fence = not fence
        is_item = re.match(r"\s*([-*]|\d+\.) ", line)
        if not fence and is_item and prev.strip() and not re.match(r"\s*([-*]|\d+\.) ", prev):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def md_body(path):
    md = (here / path).read_text(encoding="utf-8")
    body_md = gfm_lists(md.split("\n---\n", 1)[1])
    body = markdown.markdown(body_md, extensions=["fenced_code", "tables"])
    body = re.sub(r'<img alt="([^"]*)" src="([^"]+)" />',
                  r'<figure><a href="\2" target="_blank"><img alt="\1" src="\2" loading="lazy"></a><figcaption>\1</figcaption></figure>',
                  body)
    return [p for p in re.split(r"(?=<h2>)", body) if p.strip()]


def size(name):
    n = (here / name).stat().st_size
    return f"{n / 1024:.0f} KB" if n >= 1024 else f"{n} B"


def b64_body():
    text = (here / "README.b64.txt").read_text(encoding="utf-8")
    lines = text.rstrip("\n").split("\n")
    flat = "".join(lines)  # shown as one flowing block; the .txt file keeps its 76-char lines
    files = ["README.md", "README.en.md", "README.b64.txt", "signature.json", "SIGNATURE.md", "llms.txt"]
    chips = "".join(f'<a class="chip" href="{f}"><b>{f}</b><span>{size(f)}</span></a>' for f in files)
    U = '<span class="base">&lt;this-folder&gt;/</span>'
    return [
        f'''<h2>README.b64.txt</h2>
<p class="note">The whole file, {len(flat):,} characters ({size("README.b64.txt")}), drawn for people. Agents: read <a href="README.b64.txt">README.b64.txt</a> directly; the copy button also copies all of it.</p>
<div class="wall" id="wall"><button class="wallbtn" id="wallbtn" type="button">pause</button><canvas id="wallc" aria-hidden="true"></canvas>
<pre class="b64 matrix-block" id="blob">{H.escape(flat)}</pre></div>''',
    ]


def verify_section(lang):
    if not sig:
        return '<h2 id="verify">Signature</h2><p>Not signed yet.</p>'
    th = lang == "th"
    rows = "".join(f"<tr><td><code>{f}</code></td><td><code class='h'>{h}</code></td><td class='st' data-f='{f}'>…</td></tr>"
                   for f, h in sig["files"].items())
    intro = ("ทั้งสามฉบับ (ไทย · English · base64) เซ็นรวมกันด้วยกุญแจ Ethereum ของ AIExpo Oracle แบบ EIP-191 "
             "ปุ่มข้างล่างดึงไฟล์จริงมา hash ใหม่ในเบราว์เซอร์ ประกอบข้อความที่ถูกเซ็นขึ้นใหม่ แล้วกู้ address ผู้เซ็นจากลายเซ็น"
             if th else
             "All three editions (Thai · English · base64) are signed together with AIExpo Oracle's Ethereum key, EIP-191. "
             "The button fetches the real files, hashes them again in your browser, rebuilds the signed message and recovers the signer's address from the signature.")
    cli = ("ตรวจจากเครื่องตัวเอง" if th else "Check from your own machine")
    return f'''<h2 id="verify">{COVER[lang]["verify"]}</h2>
<p>{intro}</p>
<div class="sigcard">
  <div><b>signer</b> {H.escape(sig["signer"])}</div>
  <div><b>address</b> <code id="addr">{sig["address"]}</code></div>
  <div><b>scheme</b> {sig["scheme"]} · <b>date</b> {sig["date"]}</div>
  <div><b>signature</b> <code class="h">{sig["signature"]}</code></div>
</div>
<table class="files"><tr><th>file</th><th>sha256 (signed)</th><th>now</th></tr>{rows}</table>
<p><button class="btn" id="verifyBtn">{"ตรวจในเบราว์เซอร์" if th else "Verify in this browser"}</button> <span id="verdict"></span></p>
<details><summary>{"ข้อความที่ถูกเซ็น (message)" if th else "The signed message"}</summary><pre>{H.escape(sig["message"])}</pre></details>
<p><b>{cli}</b></p>
<pre>$ cd tools && bun install && bun verify.mjs
ok   README.md sha256:…
ok   README.en.md sha256:…
ok   README.b64.txt sha256:…
ok   README.b64.txt decodes to README.md
recovered {sig["address"]}
VALID: signed by {sig["address"]}

# or with Foundry:
$ cast wallet verify --address {sig["address"]} "$(jq -r .message signature.json)" $(jq -r .signature signature.json)</pre>
<p class="note">{"หมายเหตุ: ปุ่มตรวจต้องเปิดผ่าน http (เช่น GitHub Pages หรือ python3 -m http.server) เพราะเบราว์เซอร์ไม่ให้ fetch ไฟล์จาก file://" if th else "Note: the button needs the page served over http (GitHub Pages, or python3 -m http.server); browsers block fetch() on file://."}</p>'''


THEME_HEAD = (here.parent / "theme_head.html").read_text(encoding="utf-8")
THEME_JS = (here.parent / "theme.js").read_text(encoding="utf-8")
CSS = ((here.parent / "tokens.css").read_text(encoding="utf-8") + (here.parent / "guide.css").read_text(encoding="utf-8"))  # shared stage theme, same palette as the deck

JS = """
const S=[...document.querySelectorAll('header.cover, main > section')],rail=document.getElementById('rail');
S.forEach((x,j)=>{const a=document.createElement('a');a.href='#'+x.id;const t=j?(x.querySelector('h2')||{}).textContent||'':rail.dataset.cover;
 a.innerHTML='<span>'+t+'</span><b>'+(j+1)+'</b>';a.onclick=()=>{S.forEach(y=>y.classList.remove('focus'));x.classList.add('focus')};rail.appendChild(a)});
function mark(){let k=0;S.forEach((x,j)=>{if(x.getBoundingClientRect().top<=innerHeight*0.35)k=j});[...rail.children].forEach((a,j)=>a.classList.toggle('on',j===k))}
addEventListener('scroll',mark,{passive:true});mark();
const wall=document.getElementById('wall');
if(wall){const pre=document.getElementById('blob'),cv=document.getElementById('wallc'),ctx=cv.getContext('2d'),btn=document.getElementById('wallbtn');
 let txt='',cols=0,rows=0,cw=0,lh=0,fs=0,drops=[],run=localStorage.getItem('ego-wall')!=='paused',vis=true,last=0,W=0,Hh=0,top0=0;
 function layout(){txt=[...pre.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('').replace(/\\s+/g,'');
  const cs=getComputedStyle(pre);fs=parseFloat(cs.fontSize);lh=parseFloat(cs.lineHeight)||fs*1.5;ctx.font=fs+'px '+cs.fontFamily;cw=ctx.measureText('M').width;
  const padL=parseFloat(cs.paddingLeft),padT=parseFloat(cs.paddingTop),padR=parseFloat(cs.paddingRight);
  W=pre.clientWidth;Hh=pre.clientHeight;cols=Math.max(1,Math.floor((W-padL-padR)/cw));rows=Math.ceil(txt.length/cols);
  const d=devicePixelRatio||1;cv.width=W*d;cv.height=Hh*d;cv.style.width=W+'px';cv.style.height=Hh+'px';ctx.setTransform(d,0,0,d,0,0);
  wall.dataset.padL=padL;wall.dataset.padT=padT;drops=Array.from({length:cols},()=>({y:Math.random()*rows,v:0.25+Math.random()*0.6,len:6+Math.random()*14}));draw(true)}
 function draw(full){const padL=+wall.dataset.padL,padT=+wall.dataset.padT,r=pre.getBoundingClientRect();
  const r0=Math.max(0,Math.floor((-r.top-padT)/lh)-1),r1=Math.min(rows,Math.ceil((innerHeight-r.top-padT)/lh)+1);
  ctx.font=fs+'px '+getComputedStyle(pre).fontFamily;ctx.textBaseline='top';
  ctx.fillStyle='#010702';ctx.fillRect(0,padT+r0*lh,W,(r1-r0)*lh);
  for(let rr=r0;rr<r1;rr++){for(let c=0;c<cols;c++){const i=rr*cols+c;if(i>=txt.length)break;const dp=drops[c],dist=dp.y-rr;
    let a=0.42;if(dist>=0&&dist<dp.len){a=dist<1?1:0.42+0.58*(1-dist/dp.len)}
    ctx.fillStyle=dist>=0&&dist<1?'#e6ffee':`rgba(34,224,107,${a})`;ctx.fillText(txt[i],padL+c*cw,padT+rr*lh+(lh-fs)/2)}}}
 function loop(t){requestAnimationFrame(loop);if(!vis||!run||t-last<60)return;last=t;for(const d of drops){d.y+=d.v;if(d.y-d.len>rows)d.y=-Math.random()*20}draw()}
 function setRun(v){run=v;localStorage.setItem('ego-wall',v?'on':'paused');btn.textContent=v?'pause':'play'}
 btn.onclick=()=>setRun(!run);setRun(run);
 document.fonts&&document.fonts.ready.then(layout);layout();addEventListener('resize',layout);addEventListener('scroll',()=>{if(!run)draw()},{passive:true});
 new IntersectionObserver(es=>vis=es[0].isIntersecting).observe(wall);requestAnimationFrame(loop)}
addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||e.shiftKey)return;const t=e.target;if(t.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))return;
 if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();scrollBy({top:(e.key==='ArrowDown'?1:-1)*(innerHeight-56),behavior:'smooth'})}});
if(location.protocol.startsWith('http')){const base=new URL('.',location.href).href;document.querySelectorAll('.base').forEach(e=>e.textContent=base)}
document.querySelectorAll('main pre').forEach(pre=>{if(pre.classList.contains('preview'))return;const b=document.createElement('button');b.className='copy';b.textContent='copy';
 b.onclick=async()=>{const t=[...pre.childNodes].filter(n=>n!==b).map(n=>n.textContent).join('');await navigator.clipboard.writeText(t.trim());b.textContent='copied';setTimeout(()=>b.textContent='copy',1200)};pre.appendChild(b)});
const vb=document.getElementById('verifyBtn');
if(vb)vb.onclick=async()=>{const out=document.getElementById('verdict');out.className='';out.textContent='…';
 try{const sig=await (await fetch('signature.json',{cache:'no-store'})).json();const hex=b=>[...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('');
  const hashes={};let same=true;
  for(const f of Object.keys(sig.files)){const buf=await (await fetch(f,{cache:'no-store'})).arrayBuffer();hashes[f]=hex(await crypto.subtle.digest('SHA-256',buf));
   const ok=hashes[f]===sig.files[f];same&&=ok;const td=document.querySelector(`td.st[data-f="${f}"]`);td.textContent=ok?'✓ same':'✗ changed';td.className='st '+(ok?'ok':'bad')}
  const msg=[sig.message.split('\\n')[0],'date: '+sig.date,...Object.keys(sig.files).map(f=>f+' sha256:'+hashes[f])].join('\\n');
  const {recoverMessageAddress}=await import('./vendor/viem-verify.js');
  const who=await recoverMessageAddress({message:msg,signature:sig.signature});const match=who.toLowerCase()===sig.address.toLowerCase();
  out.className=(same&&match)?'ok':'bad';out.textContent=(same&&match?'✓ VALID · recovered ':'✗ INVALID · recovered ')+who}
 catch(e){out.className='bad';out.textContent='✗ '+e.message+(location.protocol==='file:'?' (open over http)':'')}};
"""


def page(lang):
    c = COVER[lang]
    sections = md_body({"th": "README.md", "en": "README.en.md"}[lang]) if lang != "b64" else b64_body()
    sections.append(verify_section(lang))
    titles = [re.sub("<[^>]+>", "", (re.search(r"<h2[^>]*>(.*?)</h2>", x, re.S) or [None, ""])[1]).strip() for x in sections]
    def down(i):  # i = index of the section the button jumps to
        return f'<a class="down" href="#s{i + 2}" aria-label="next: {H.escape(titles[i])}"><b>↓</b> {H.escape(titles[i])}</a>'
    body = "".join(f'<section id="s{i + 2}">{x}{down(i + 1) if i + 1 < len(sections) else ""}</section>' for i, x in enumerate(sections))
    langs = "".join(f'<a href="{PAGES[k]}" class="{"on" if k == lang else ""}">{LANG_LABEL[k]}</a>' for k in PAGES)
    langs_end = f'<button class="theme" id="themebtn" type="button">{"☀ โหมดสว่าง" if lang == "th" else "☀ Light"}</button>'
    langs = f'<a href="../index.html" class="home">{"← บทเรียนทั้งหมด" if lang == "th" else "← All lessons"}</a>' + langs
    facts = (f'<span>DMG <b>0.6.2.5</b> · 143M</span><span><b>Notarized</b> Developer ID</span>'
             f'<a href="#verify">{c["verify"]} <b>{sig["address"][:6]}…{sig["address"][-4:]}</b></a>' if sig else "")
    facts += f'<a href="slides.html">{c["slides"]} <b>slides.html</b></a>'
    title = re.sub("<[^>]+>", " ", c["h1"]).replace("  ", " ")
    return f"""<!doctype html>
<html lang="{'th' if lang == 'th' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<link rel="alternate" type="text/markdown" hreflang="th" href="README.md">
<link rel="alternate" type="text/markdown" hreflang="en" href="README.en.md">
<link rel="help" type="text/plain" href="llms.txt" title="llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@500;600;700&family=Sarabun:wght@400;500;700&display=swap">
{THEME_HEAD}<style>{CSS}</style>
</head>
<body>
<header class="cover" id="s1"><div class="in">
  <nav class="langs">{langs}{langs_end}</nav>
  <span class="kicker">{c["kicker"]}</span>
  <h1>{c["h1"]}</h1>
  {"".join(f"<p>{x}</p>" for x in c["sub"])}
  <div class="facts">{facts}</div>
  {'<a class="enter" href="#wall"><span class="rain" aria-hidden="true">01001011 10110</span><b>ENTER THE MATRIX</b><i>↓</i></a>' if lang == "b64" else ""}
  <a class="down cover-down" href="#s2" aria-label="next: {H.escape(titles[0])}"><b>↓</b> {H.escape(titles[0])}</a>
</div></header>
<main>{body}</main>
<details class="ai"><summary>AI</summary><div><p>{AI_NOTE[lang]}</p><a href="llms.txt">llms.txt</a><a href="README.en.md">README.en.md</a><a href="README.md">README.md</a><a href="README.b64.txt">README.b64.txt</a><a href="signature.json">signature.json</a><code>https://aiexpo.buildwithoracle.com/mcp</code></div></details>
<nav id="rail" data-cover="{c["cover_label"]}"></nav>
<script>{JS}</script>
<script>{THEME_JS}</script>
</body>
</html>
"""


for lang, name in PAGES.items():
    (here / name).write_text(page(lang), encoding="utf-8")
    print("wrote", name)
