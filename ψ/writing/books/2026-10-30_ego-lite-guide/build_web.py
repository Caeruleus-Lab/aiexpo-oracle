"""Build the webpage editions from the signed files, so the pages never drift from what was signed.

  index.html  Thai     (README.md)
  en.html     English  (README.en.md)
  b64.html    base64   (README.b64.txt, decodes to README.md in the browser)

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
                     "Decode it here, or: base64 -d README.b64.txt"],
                cover_label="Cover", verify="Signature", slides="Slides"),
}
PAGES = {"th": "index.html", "en": "en.html", "b64": "b64.html"}
LANG_LABEL = {"th": "ไทย", "en": "English", "b64": "base64"}


def md_body(path):
    md = (here / path).read_text(encoding="utf-8")
    body_md = md.split("\n---\n", 1)[1]
    body = markdown.markdown(body_md, extensions=["fenced_code", "tables"])
    body = re.sub(r'<img alt="([^"]*)" src="([^"]+)" />',
                  r'<figure><a href="\2" target="_blank"><img alt="\1" src="\2" loading="lazy"></a><figcaption>\1</figcaption></figure>',
                  body)
    return [p for p in re.split(r"(?=<h2>)", body) if p.strip()]


def b64_body():
    blob = H.escape((here / "README.b64.txt").read_text(encoding="utf-8"))
    return [
        '<h2>README.b64.txt</h2><p>base64 of <code>README.md</code>. The decode button turns it back into the Thai text, '
        'and the signature panel checks that both files hash to what was signed.</p>'
        '<p><button class="btn" id="decode">Decode → Thai text</button> <a class="btn ghost" href="README.b64.txt" download>Download .txt</a></p>'
        f'<pre class="b64" id="blob">{blob}</pre>',
        '<h2>Decoded</h2><pre class="decoded" id="decoded">(press Decode)</pre>',
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
:root{--ink:#0d1b3d;--blue:#2f5bea;--cyan:#27e6f2;--paper:#f4f6fb;--mute:#5a6b8c}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:16px}
body{margin:0;background:var(--paper);color:var(--ink);font:18px/1.75 Sarabun,"Noto Sans Thai","IBM Plex Sans Thai",system-ui,sans-serif}
.cover{background:radial-gradient(1100px 700px at 80% 10%,#3b6cf5 0%,#132a6b 55%,#070f2b 100%);color:#fff;padding:64px 24px 56px}
.cover .in{max-width:980px;margin:0 auto}
.langs{display:flex;gap:8px;margin-bottom:26px}
.langs a{color:#cfe0ff;text-decoration:none;border:2px solid rgba(255,255,255,.35);border-radius:999px;padding:4px 14px;font-weight:700;font-size:15px}
.langs a.on{background:#fff;color:var(--ink);border-color:#fff}
.kicker{display:inline-block;background:#c2410c;color:#fff;font-weight:800;border-radius:999px;padding:6px 18px}
.cover h1{font-size:clamp(38px,6vw,68px);line-height:1.12;margin:22px 0 14px;font-weight:800}
.cover h1 em{font-style:normal;color:var(--cyan)}
.nw{white-space:nowrap}
.cover p{font-size:21px;color:#d6e4ff;margin:0 0 6px}
.cover .facts{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}
.cover .facts span,.cover .facts a{border:2px solid rgba(39,230,242,.6);border-radius:14px;padding:10px 16px;font-weight:700;color:#fff;text-decoration:none}
.cover .facts b{color:var(--cyan)}
main{max-width:980px;margin:0 auto;padding:8px 24px 80px}
h2{font-size:32px;line-height:1.3;margin:64px 0 12px;padding-top:12px;border-top:4px solid var(--blue)}
section.focus h2{border-top-color:#ff7a1a}
figure{margin:22px 0 28px}
figure img{width:100%;border-radius:14px;box-shadow:0 12px 40px rgba(13,27,61,.18);display:block}
figcaption{color:var(--mute);font-size:15px;margin-top:8px}
pre{background:#06112e;color:#e6f6ff;border-radius:14px;padding:18px 20px;overflow-x:auto;font:14.5px/1.55 Menlo,"SF Mono",monospace;border-left:6px solid var(--cyan)}
pre.b64{max-height:420px;font-size:12.5px;word-break:break-all;white-space:pre-wrap}
pre.decoded{white-space:pre-wrap;font-family:Sarabun,"Noto Sans Thai",sans-serif;font-size:16px;max-height:600px}
code{font-family:Menlo,"SF Mono",monospace;font-size:.88em;background:#e3e9f7;border-radius:6px;padding:1px 6px}
pre code{background:none;padding:0;font-size:inherit}
code.h{word-break:break-all;font-size:.78em}
blockquote{margin:20px 0;padding:14px 20px;background:#fff4e6;border-left:6px solid #ff7a1a;border-radius:10px}
blockquote p{margin:0}
table{border-collapse:collapse;width:100%;font-size:16px;background:#fff;border-radius:12px;overflow:hidden}
th,td{padding:10px 12px;border-bottom:1px solid #e1e6f2;text-align:left;vertical-align:top}
th{background:#e8eefc}
a{color:var(--blue)}
.sigcard{background:#fff;border:2px solid #c9d3ea;border-radius:14px;padding:16px 20px;display:grid;gap:6px;margin:16px 0}
.sigcard b{display:inline-block;min-width:92px;color:var(--mute)}
.btn{background:var(--ink);color:#fff;border:0;border-radius:999px;padding:10px 20px;font:700 16px Sarabun,sans-serif;cursor:pointer;text-decoration:none;display:inline-block}
.btn.ghost{background:#fff;color:var(--ink);border:2px solid var(--ink)}
#verdict{font-weight:800;margin-left:10px}
.ok{color:#0a7a32}.bad{color:#c0262d}
.note{color:var(--mute);font-size:15px}
#rail{position:fixed;right:14px;top:50%;transform:translateY(-50%);z-index:8;display:flex;flex-direction:column;gap:6px}
#rail a{display:flex;align-items:center;justify-content:flex-end;gap:8px;text-decoration:none;color:var(--mute);font:700 13px Sarabun,sans-serif}
#rail a b{display:inline-flex;width:30px;height:30px;border-radius:50%;align-items:center;justify-content:center;background:#fff;border:2px solid #c9d3ea;color:var(--ink)}
#rail a span{opacity:0;transition:opacity .15s;background:var(--ink);color:#fff;border-radius:8px;padding:3px 8px;white-space:nowrap}
#rail a:hover span{opacity:1}
#rail a.on b{background:var(--blue);border-color:var(--blue);color:#fff}
@media (max-width:900px){#rail{display:none}}
"""

JS = """
const S=[...document.querySelectorAll('header.cover, main > section')],rail=document.getElementById('rail');
S.forEach((x,j)=>{const a=document.createElement('a');a.href='#'+x.id;const t=j?(x.querySelector('h2')||{}).textContent||'':rail.dataset.cover;
 a.innerHTML='<span>'+t+'</span><b>'+(j+1)+'</b>';a.onclick=()=>{S.forEach(y=>y.classList.remove('focus'));x.classList.add('focus')};rail.appendChild(a)});
function mark(){let k=0;S.forEach((x,j)=>{if(x.getBoundingClientRect().top<=innerHeight*0.35)k=j});[...rail.children].forEach((a,j)=>a.classList.toggle('on',j===k))}
addEventListener('scroll',mark,{passive:true});mark();
const dec=document.getElementById('decode');
if(dec)dec.onclick=()=>{const b=document.getElementById('blob').textContent.replace(/\\s+/g,'');
 const bytes=Uint8Array.from(atob(b),c=>c.charCodeAt(0));document.getElementById('decoded').textContent=new TextDecoder('utf-8').decode(bytes)};
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
    body = "".join(f'<section id="s{i + 2}">{s}</section>' for i, s in enumerate(sections))
    langs = "".join(f'<a href="{PAGES[k]}" class="{"on" if k == lang else ""}">{LANG_LABEL[k]}</a>' for k in PAGES)
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
<style>{CSS}</style>
</head>
<body>
<header class="cover" id="s1"><div class="in">
  <nav class="langs">{langs}</nav>
  <span class="kicker">{c["kicker"]}</span>
  <h1>{c["h1"]}</h1>
  {"".join(f"<p>{x}</p>" for x in c["sub"])}
  <div class="facts">{facts}</div>
</div></header>
<main>{body}</main>
<nav id="rail" data-cover="{c["cover_label"]}"></nav>
<script>{JS}</script>
</body>
</html>
"""


for lang, name in PAGES.items():
    (here / name).write_text(page(lang), encoding="utf-8")
    print("wrote", name)
