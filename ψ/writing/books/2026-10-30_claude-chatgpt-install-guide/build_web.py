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
               h1='ติดตั้ง <em>Claude</em><br>และ <em>ChatGPT</em><br><span class="nw">ให้พร้อมเข้า workshop</span>',
               sub=["ทีละขั้น ตั้งแต่หน้าดาวน์โหลด จนถึงลงสกิล Oracle ได้จริง ทั้งในเครื่องและบน claude.ai",
                    "ทุกภาพจับจากเว็บจริง · ทุกคำสั่งรันจริง · 30 ต.ค. 2026"],
               cover_label="ปก", verify="ตรวจลายเซ็น", slides="สไลด์", back="ย้อน", next="ถัดไป"),
    "en": dict(kicker="Written by AI, for AI",
               h1='Install <em>Claude</em><br>and <em>ChatGPT</em>,<br><span class="nw">ready for the workshop</span>',
               sub=["Step by step, from the download pages to Oracle skills that really load, locally and on claude.ai",
                    "Every screenshot from the real site · every command really ran · 30 Oct 2026"],
               cover_label="Cover", verify="Signature", slides="Slides", back="Back", next="Next"),
    "b64": dict(kicker="base64 · for machines",
                h1='<em>Claude + ChatGPT</em> guide<br><span class="nw">as base64</span>',
                sub=["The Thai edition, byte for byte, encoded as base64 (RFC 4648, 76-char lines)",
                     "Agents: read llms.txt, or curl README.b64.txt | base64 -d"],
                cover_label="Cover", verify="Signature", slides="Slides", back="Back", next="Next"),
}
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
    files = ["README.md", "README.en.md", "README.b64.txt", "signature.json", "SIGNATURE.md", "llms.txt", "skills/awaken.zip"]
    chips = "".join(f'<a class="chip" href="{f}"><b>{f}</b><span>{size(f)}</span></a>' for f in files)
    U = '<span class="base">&lt;this-folder&gt;/</span>'
    return [
        f'''<h2 id="agents">For AI agents</h2>
<p class="human">Human? Read the guide in <a class="chip" href="th.html"><b>ไทย</b></a> <a class="chip" href="en.html"><b>English</b></a></p>
<p>This page holds the guide as base64. Skip the decode if you can and fetch the markdown. The index for agents is <a href="llms.txt"><code>llms.txt</code></a>.</p>
<p class="step">1 · Fastest: the markdown</p>
<pre>curl -fsSL {U}README.en.md
curl -fsSL {U}README.md</pre>
<p class="step">2 · Or decode the base64 (same bytes as README.md)</p>
<pre>curl -fsSL {U}README.b64.txt | base64 -d</pre>
<p class="step">3 · Check it is the signed text</p>
<pre>curl -fsSL {U}signature.json
shasum -a 256 README.md
cd tools && bun install && bun verify.mjs</pre>
<p class="note">The sha256 must equal <code>files["README.md"]</code> in signature.json. verify.mjs prints <code>VALID: signed by 0xaBF1…5f78</code>.</p>
<div class="chips">{chips}</div>''',
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


CSS = """
:root{--ink:#0d1b3d;--blue:#2f5bea;--cyan:#27e6f2;--paper:#f4f6fb;--mute:#5a6b8c;--pad:clamp(18px,5vw,120px);--railw:clamp(0px,4vw,64px)}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px}
body{margin:0;background:var(--paper);color:var(--ink);font:clamp(17px,0.55vw + 12px,24px)/1.75 Sarabun,"Noto Sans Thai","IBM Plex Sans Thai",system-ui,sans-serif}
.cover{background:radial-gradient(70vw 70vh at 80% 10%,#3b6cf5 0%,#132a6b 55%,#070f2b 100%);color:#fff;min-height:100vh;display:flex;align-items:center;padding:clamp(40px,6vh,96px) calc(var(--pad) + var(--railw)) clamp(40px,6vh,96px) var(--pad)}
.cover .in{width:100%}
.langs{display:flex;gap:8px;margin-bottom:26px}
.langs a{color:#cfe0ff;text-decoration:none;border:2px solid rgba(255,255,255,.35);border-radius:999px;padding:4px 14px;font-weight:700;font-size:15px}
.langs a.on{background:#fff;color:var(--ink);border-color:#fff}
.kicker{display:inline-block;background:#c2410c;color:#fff;font-weight:800;border-radius:999px;padding:6px 18px}
.cover h1{font-size:clamp(40px,7vw,140px);line-height:1.12;margin:22px 0 14px;font-weight:800}
.cover h1 em{font-style:normal;color:var(--cyan)}
.nw{white-space:nowrap}
.cover p{font-size:clamp(18px,1.5vw,34px);color:#d6e4ff;margin:0 0 6px}
.cover .facts{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}
.cover .facts span,.cover .facts a{border:2px solid rgba(39,230,242,.6);border-radius:14px;padding:10px 16px;font-weight:700;color:#fff;text-decoration:none}
.cover .facts b{color:var(--cyan)}
main{padding:8px calc(var(--pad) + var(--railw)) 12vh var(--pad)}
h2{font-size:clamp(28px,3vw,64px);line-height:1.25;margin:clamp(36px,6vh,96px) 0 12px;padding-top:12px;border-top:4px solid var(--blue)}
section.focus h2{border-top-color:#ff7a1a}
figure{margin:22px 0 28px}
figure img{width:100%;border-radius:14px;box-shadow:0 12px 40px rgba(13,27,61,.18);display:block}
figcaption{color:var(--mute);font-size:.82em;margin-top:8px}
pre{background:#06112e;color:#e6f6ff;border-radius:14px;padding:clamp(14px,1.4vw,28px) clamp(16px,1.8vw,34px);white-space:pre-wrap;overflow-wrap:anywhere;font:clamp(13px,0.45vw + 10px,19px)/1.55 Menlo,"SF Mono",monospace;border:1px solid rgba(39,230,242,.28)}
pre.b64{padding-top:48px;font-size:clamp(11px,0.35vw + 8px,16px);white-space:normal;word-break:break-all;line-height:1.5}
pre.decoded{font-family:Sarabun,"Noto Sans Thai",sans-serif;font-size:16px}
code{font-family:Menlo,"SF Mono",monospace;font-size:.88em;background:#e3e9f7;border-radius:6px;padding:1px 6px}
pre code{background:none;padding:0;font-size:inherit}
code.h{word-break:break-all;font-size:.78em}
blockquote{margin:20px 0;padding:14px 20px;background:#fff4e6;border:1px solid #f3c9a0;border-radius:10px}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;font-size:.9em;background:#fff;border-radius:12px;table-layout:fixed;overflow-wrap:anywhere}
th,td{padding:10px 12px;border-bottom:1px solid #e1e6f2;text-align:left;vertical-align:top}
th{background:#e8eefc}
a{color:var(--blue)}
.sigcard{background:#fff;border:2px solid #c9d3ea;border-radius:14px;padding:16px 20px;display:grid;gap:6px;margin:16px 0}
.sigcard{min-width:0}.sigcard div{min-width:0;overflow-wrap:anywhere}.sigcard code{word-break:break-all}
.sigcard b{display:inline-block;min-width:92px;color:var(--mute)}
.btn{background:var(--ink);color:#fff;border:0;border-radius:999px;padding:10px 20px;font:700 16px Sarabun,sans-serif;cursor:pointer;text-decoration:none;display:inline-block}
.btn.ghost{background:#fff;color:var(--ink);border:2px solid var(--ink)}
#verdict{font-weight:800;margin-left:10px}
.ok{color:#0a7a32}.bad{color:#c0262d}
.note{color:var(--mute);font-size:15px}
.down{display:inline-flex;align-items:center;gap:12px;margin:clamp(20px,3vh,40px) 0 0;padding:10px 22px 10px 10px;border-radius:999px;background:#fff;border:2px solid #c9d3ea;color:var(--ink);text-decoration:none;font-weight:700;font-size:.92em;transition:transform .15s,border-color .15s}
.down b{display:inline-flex;width:2.1em;height:2.1em;border-radius:50%;align-items:center;justify-content:center;background:var(--blue);color:#fff;font-size:1.05em}
.down:hover{border-color:var(--blue);transform:translateY(3px)}
.cover-down{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.4);color:#fff;margin-top:clamp(28px,6vh,80px)}
.cover-down b{background:var(--cyan);color:var(--ink)}
.chips{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}
.chip{display:inline-flex;align-items:baseline;gap:8px;background:#fff;border:2px solid #c9d3ea;border-radius:999px;padding:6px 14px;text-decoration:none;color:var(--ink);font-size:.9em}
.chip:hover{border-color:var(--blue)}
.chip span{color:var(--mute);font-size:.85em}
.human{background:#fff;border:2px dashed #c9d3ea;border-radius:14px;padding:10px 16px}
.human .chip{margin-left:6px}
.step{font-weight:800;margin:22px 0 6px}
.step+pre{margin-top:0}
pre{position:relative}
pre .copy{position:absolute;top:10px;right:10px;background:rgba(255,255,255,.12);color:#e6f6ff;border:1px solid rgba(255,255,255,.3);border-radius:8px;padding:3px 10px;font:600 13px Sarabun,sans-serif;cursor:pointer;opacity:.75}
pre .copy:hover{opacity:1}
pre.preview{margin-bottom:0;border-bottom-left-radius:0;border-bottom-right-radius:0;-webkit-mask-image:linear-gradient(#000 55%,transparent);mask-image:linear-gradient(#000 55%,transparent)}
details.blob summary{cursor:pointer;font-weight:800;color:var(--blue);margin:8px 0}
details.blob pre{margin-top:0}
.base{color:var(--cyan)}
pre.matrix-block{background:#010702;color:#22e06b;border-color:rgba(61,255,138,.35);text-shadow:0 0 6px rgba(34,224,107,.55);box-shadow:inset 0 0 80px rgba(0,0,0,.9)}
pre.matrix-block .copy{color:#b9ffd2;border-color:rgba(61,255,138,.5)}
.wall{position:relative}
.wall pre.matrix-block{color:transparent;text-shadow:none;margin:0}
.wall pre.matrix-block::selection,.wall pre.matrix-block *::selection{color:#020a04;background:#3dff8a}
.wall canvas{position:absolute;left:0;top:0;z-index:1;pointer-events:none;border-radius:14px}
.wall .copy{z-index:2;color:#b9ffd2!important}
.wallbtn{position:absolute;top:10px;right:74px;z-index:2;background:rgba(255,255,255,.12);color:#b9ffd2;border:1px solid rgba(61,255,138,.5);border-radius:8px;padding:3px 10px;font:600 13px Sarabun,sans-serif;cursor:pointer}
#rail{position:fixed;right:14px;top:50%;transform:translateY(-50%);z-index:8;display:flex;flex-direction:column;gap:6px}
#rail a{display:flex;align-items:center;justify-content:flex-end;gap:8px;text-decoration:none;color:var(--mute);font:700 13px Sarabun,sans-serif}
#rail a b{display:inline-flex;width:30px;height:30px;border-radius:50%;align-items:center;justify-content:center;background:#fff;border:2px solid #c9d3ea;color:var(--ink)}
#rail a span{opacity:0;transition:opacity .15s;background:var(--ink);color:#fff;border-radius:8px;padding:3px 8px;white-space:nowrap}
#rail a:hover span{opacity:1}
#rail a.on b{background:var(--blue);border-color:var(--blue);color:#fff}
@media (max-width:900px){#rail{display:none}}
#navback,#navnext{position:fixed;left:50%;transform:translateX(-50%);z-index:9;display:inline-flex;align-items:center;gap:6px;border:2px solid #c9d3ea;background:#fff;color:var(--ink);border-radius:999px;padding:8px 18px;font:700 15px Sarabun,sans-serif;cursor:pointer;box-shadow:0 6px 20px rgba(13,27,61,.15);opacity:.28;transition:opacity .2s,border-color .2s}
#navback{top:12px}#navnext{bottom:14px}
#navback:hover,#navnext:hover,#navback:focus-visible,#navnext:focus-visible{opacity:1;border-color:var(--blue)}
#navback b,#navnext b{display:inline-flex;width:1.6em;height:1.6em;border-radius:50%;align-items:center;justify-content:center;background:var(--blue);color:#fff}
#navback:disabled,#navnext:disabled{display:none}
@media (hover:none){#navback,#navnext{opacity:.85}}
"""

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
 const dn=e.key==='ArrowDown'||e.key==='ArrowRight'||e.key==='PageDown',up=e.key==='ArrowUp'||e.key==='ArrowLeft'||e.key==='PageUp';if(!dn&&!up)return;e.preventDefault();nav(dn)});
function nav(dn){const y=scrollY,step=innerHeight-56,tops=S.map(x=>x.getBoundingClientRect().top+y-16);
 const nx=Math.min(...tops.filter(v=>v>y+4)),pv=Math.max(...tops.filter(v=>v<y-4),0);const to=dn?(nx-y<=step*1.2?nx:y+step):(y-pv<=step*1.2?pv:y-step);scrollTo({top:to,behavior:'smooth'})}
document.getElementById('navback').onclick=()=>nav(false);document.getElementById('navnext').onclick=()=>nav(true);
function navstate(){const end=scrollY+innerHeight>=document.documentElement.scrollHeight-4;document.getElementById('navback').disabled=scrollY<4;document.getElementById('navnext').disabled=end}
addEventListener('scroll',navstate,{passive:true});navstate();
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
    facts = (f'<span>Claude Code <b>2.1.314</b></span><span>codex-cli <b>0.166.0</b></span><a href="skills/awaken.zip">skill <b>awaken.zip</b></a>'
             f'<a href="#verify">{c["verify"]} <b>{sig["address"][:6]}…{sig["address"][-4:]}</b></a>' if sig else "")
    title = re.sub(r"\s+([,.])", r"\1", " ".join(re.sub("<[^>]+>", " ", c["h1"]).split()))
    return f"""<!doctype html>
<html lang="{'th' if lang == 'th' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{H.escape(title)}</title>
<link rel="alternate" type="text/markdown" hreflang="th" href="README.md">
<link rel="alternate" type="text/markdown" hreflang="en" href="README.en.md">
<link rel="help" type="text/plain" href="llms.txt" title="llms.txt">
<style>{CSS}</style>
</head>
<body>
<header class="cover" id="s1"><div class="in">
  <nav class="langs">{langs}</nav>
  <span class="kicker">{c["kicker"]}</span>
  <h1>{c["h1"]}</h1>
  {"".join(f"<p>{x}</p>" for x in c["sub"])}
  <div class="facts">{facts}</div>
  <a class="down cover-down" href="#s2" aria-label="next: {H.escape(titles[0])}"><b>↓</b> {H.escape(titles[0])}</a>
</div></header>
<main>{body}</main>
<nav id="rail" data-cover="{c["cover_label"]}"></nav>
<button id="navback" type="button" aria-label="{c["back"]}"><b>↑</b> {c["back"]}</button>
<button id="navnext" type="button" aria-label="{c["next"]}"><b>↓</b> {c["next"]}</button>
<script>{JS}</script>
</body>
</html>
"""


for lang, name in PAGES.items():
    (here / name).write_text(page(lang), encoding="utf-8")
    print("wrote", name)
