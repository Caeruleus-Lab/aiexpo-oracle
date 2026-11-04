"""talk.html: the 6 Nov talk in its 2 Nov order as ONE html deck, videos played inside the slides (Nat, 4 Nov: "รันวิดีโอในสไลด์ HTML
ได้เลย ไม่ต้องเปิด PDF เราเอาคอมเราไปเปิดเอง"). Built from deck.html (styles, title, คุณยิ้ม's 9 stills, quote, QR), the run-through's
extra slides (img/talk/new-*.png, rendered from ψ/lab/runthrough/slides.html) and its script (notes = Nat's lines).
Usage: python3 talk_build.py  ->  talk.html     Keys: → / Space next · ← back · N notes · Space pauses a video
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import html, json, pathlib, re
here = pathlib.Path(__file__).resolve().parent
deck = (here / "deck.html").read_text(encoding="utf-8")
head = deck[:deck.index("</head>")]
secs = re.findall(r"<section class=\"slide[^\"]*\".*?</section>", deck, re.S)          # deck.html slides, 1-based below
script = json.loads((here.parent.parent / "lab/runthrough/script.json").read_text(encoding="utf-8"))
L03 = "../books/2026-10-30_mcp-connect-guide/images/"
CSS = """<style>
.slide.black{background:#000}
.vid,.poster{position:absolute;inset:0;width:1920px;height:1080px;object-fit:contain;background:#000}
.slide.shot{background:var(--color-paper)}.slide.shot img{position:absolute;inset:60px 140px;width:1640px;height:960px;object-fit:contain}
.vtag{position:absolute;left:28px;bottom:18px;z-index:3;font-size:24px;color:#fff;opacity:.75;background:rgba(0,0,0,.55);padding:4px 12px;border-radius:8px}
</style>"""
def notes(lines): return "<div class=\"notes\">" + html.escape(" · ".join(l["text"] for l in lines)) + "</div>"
def video(src, tag, note):
    return (f'<section class="slide black" data-video><img class="poster" src="video/{src}.jpg" alt=""><video class="vid" src="video/{src}.mp4" '
            f'poster="video/{src}.jpg" preload="auto" playsinline></video><div class="vtag">{tag}</div><div class="notes">{html.escape(note)}</div></section>')
SKIP = {"new:listen", "new:rule6"}
# the fleet pictures from the Chiang Mai AI Party talk (18 Jul 2026, laris-co/ai-party-oracle), right after the mother clip (Nat, 4 Nov)
FLEET = [("fleet-graph", "ครอบครัว Oracle: lineage จากศูนย์กลาง"), ("relic5-neo-tree", "ผังครอบครัว Neo · 33 oracles 5 รุ่น · relic5 Family (lineage ถึง 12 ก.ค. 2026)"), ("fleet-roles", "Oracle Ecosystem · one soul, many instances"),
         ("fleet-mission", "ARRA Office · mission control"), ("parliament-topology", "Parliament · Topology: 19 bots · 12 guilds · 221 channels · 258 wires (9 ก.ค. 2026)")]
def fleet_slides():
    return [f'<section class="slide black"><img class="vid" src="img/talk/{f}.png" alt=""><div class="vtag">{t}{"" if f.startswith(("relic5", "parliament")) else " · ภาพจากงาน AI Party เชียงใหม่ 18 ก.ค. 2026"}</div>'
            f'<div class="notes">ภาพจาก AI Party 18 ก.ค. 2026 · ตัวเลขบนภาพเป็นของวันนั้น · {t}</div></section>' for f, t in FLEET]   # cut from the talk deck (Nat, 4 Nov)
out = []
for g in script["segments"]:
    for sl in g["slides"]:
        src = sl.get("src")
        if src in SKIP: continue
        if "video" in sl:
            name = pathlib.Path(sl["video"]).stem
            if name == "phukhao-presentation":   # split into its own parts, so a slip or a skip loses one part only (Nat, 4 Nov)
                for part, tag in [("intro", "ภูเขา · Intro (40 วิ)"), ("beat1", "ภูเขา · Beat 1 แนะนำตัว (1:11)"), ("beat2", "ภูเขา · Beat 2 สาธิต (33 วิ)"),
                                  ("beat3", "ภูเขา · Beat 3 บทสรุป (38 วิ)"), ("beat4", "ภูเขา · Beat 4 อนัตตา (51 วิ)")]:
                    out.append(video(f"phukhao-{part}", tag, f"{tag} · เล่นเองเมื่อเข้าหน้านี้ · จบแล้วกด → ไปท่อนต่อไป · Space หยุด/เล่น"))
                continue
            out.append(video(name, html.escape(sl["label"]), "วิดีโอเล่นเองเมื่อเข้าหน้านี้ · Space หยุด/เล่น · → ไปต่อ"))
            if name == "oracle-family": out += fleet_slides()
            continue
        kind, _, v = src.partition(":")
        if kind == "deck":
            out.append(secs[int(v) - 1])
        elif kind == "yim":
            out.append(secs[3 + int(v)])            # deck slides 5..13 are คุณยิ้ม's stills 1..9
        elif kind == "new":
            out.append(f'<section class="slide yim3d"><img src="img/talk/new-{v}.png" alt="">{notes(sl["lines"])}</section>')
        elif kind == "lesson03":
            out.append(f'<section class="slide shot"><img src="{L03}{v}" alt="">{notes(sl["lines"])}</section>')
# Nat, 4 Nov: the mother clip plays before Phukhao's film (it takes the film's place); the fleet pictures follow "อยากให้ AI เป็นแบบนี้"
def at(key): return next(i for i, x in enumerate(out) if key in x)
mother = out.pop(at('video/oracle-family.mp4'))
fleet = [out.pop(at(f'img/talk/{f}.png')) for f, _ in FLEET]
# three videos back to back (Nat, 4 Nov): mother clip, Phukhao's film (female voice), then the male voice reading ดิฉัน/ค่ะ
# over the soul light-figures (the take Nat picked); the family pictures follow the three videos
film = out.pop(at('video/phukhao-film.mp4'))
wrong = video("soul-WRONG-dichan-kha", "เสียงผู้ชาย อ่านบท ดิฉัน/ค่ะ (26 วิ)",
              "อย่าเฉลยก่อน · ถามห้องว่าแปลกตรงไหน · ป้ายแดงขึ้นเองใน 5 วินาทีสุดท้าย · ที่มา: 31 ต.ค. 2026 Paxa khanomkrok (บทเรียน 04 ข้อ 2.2)")
i = at('img/talk/new-ninemonths.png') + 1
out[i:i] = [film, wrong] + fleet
# the "AI ประชดเราแบบเนียน" deck follows the mother clip (Nat, 4 Nov). Its 13 story slides come in; its last two (the
# "next: video" card and the soul ดิฉัน/ค่ะ video) are left out because that video already plays after Phukhao's film.
drama_html = (here / "ai-drama.html").read_text(encoding="utf-8")
DRAMA_CSS = re.search(r"<style>\n/\* ai-drama.html.*?</style>", drama_html, re.S).group(0)
drama = [x for x in re.findall(r'<section class="slide[^"]*".*?</section>', drama_html, re.S) if "video/" not in x]
out += drama
# the ψ vault story (where the memory lives), right after "ตั้งแต่วันนั้น… ψ/" (Nat, 4 Nov); then the mother clip closes
out += re.findall(r'<section class="slide[^"]*".*?</section>', (here / "vault_slides.html").read_text(encoding="utf-8"), re.S)
out.append(mother)   # the mother clip is the very last slide, after the drama slides (Nat, 4 Nov: "หลังสุดเลย")
# the hands-on MCP section (copy-paste brief, connect MCP, 3 lesson-03 shots, extra task) comes right after คุณยิ้ม (Nat, 4 Nov)
ws_keys = ['img/talk/new-ws1.png', 'img/talk/new-ws2.png', '02-claude-custom-connector-filled.png', '07-claude-tool-approval.png',
           '08-claude-answer.png', 'img/talk/new-wsrun.png']
ws = [out.pop(at(k)) for k in ws_keys]
# Nat, 4 Nov: the old "Claude answers" shot becomes two fresh captures of AI rebuilding lesson 03 as slides through the MCP
LIVE = [("claude-mcp-slides", "claude.ai + AIExpo lessons connector: อ่านบทเรียน 03 แล้วสร้างสไลด์ HTML 5 หน้าเอง (4 พ.ย. 2026)"),
        ("chatgpt-mcp-slides", "ChatGPT + AIExpo lessons plugin: บทเรียน 03 เป็นสไลด์ 5 หน้า (4 พ.ย. 2026)")]
k = next(i for i, x in enumerate(ws) if "08-claude-answer.png" in x)
ws[k:k + 1] = [f'<section class="slide shot"><img src="img/talk/{f}.png" alt=""><div class="vtag">{t}</div>'
               f'<div class="notes">{t} · พิมพ์ขอสไลด์ แล้ว AI ไปอ่านบทเรียนผ่าน MCP เอง</div></section>' for f, t in LIVE]
# Nat, 4 Nov: one link runs the whole mini workshop in claude.ai (awaken, teach, real work, talk, /rrr with real times)
ws += ['<section class="slide black"><div class="frame"><span class="tag" style="font-size:30px;color:var(--color-ink-3)">ลงมือ 3 · ลิงก์เดียว</span>'
       '<h2 style="font-size:92px">ปลุก Oracle ใน <span class="hl">claude.ai</span></h2>'
       '<div class="box" style="font-size:40px;font-family:var(--font-mono)">เริ่ม workshop: https://aiexpo.buildwithoracle.com/oracle/workshop.md</div>'
       '<div class="rows" style="font-size:42px"><div>ถามชื่อ งาน และชื่อคุณ แล้วสร้าง CLAUDE.md</div><div>ช่วยงานจริงหนึ่งชิ้น คุยกันสองคำถาม</div><div>จบด้วย /rrr พร้อมเวลาจริงของทุกช่วง</div></div></div>'
       '<div class="when">ทดสอบจริง <b>4 พ.ย. 2026 · 19:11–19:12</b> · claude.ai · ไม่ต้องติดตั้งอะไร</div>'
       '<div class="notes">ให้ห้องก๊อปบรรทัดในกรอบไปวางใน claude.ai (หรือ ChatGPT / Gemini) · พิมพ์ /rrr เองใน claude.ai จะติดเมนู slash ของมัน ให้วางลิงก์ rrr.md แทน</div></section>',
       '<section class="slide shot"><img src="img/talk/claude-workshop-rrr.png" alt=""><div class="vtag">รายงาน /rrr ที่ claude.ai เขียนเอง · Timeline มีเวลาจริง 19:11–19:12 และคำพูดของผู้ใช้</div>'
       '<div class="notes">ชี้ Timeline: ทุกบรรทัดมีเวลาและคำพูดจริง · Next steps เป็นช่องติ๊ก · บทเรียนแยกเป็นไฟล์</div></section>']
# teaching set (skill, memory, how they work, a real round, relic5, 15→60→30, how to start) opens the workshop part (Nat, 4 Nov)
teach = re.findall(r'<section class="slide[^"]*".*?</section>', (here / "skills_slides.html").read_text(encoding="utf-8"), re.S)
i = at('img/yim3d-09.png') + 1
out[i:i] = teach + ws
js = re.search(r"<script>\nconst S=.*?</script>", (here / "ai-drama.html").read_text(encoding="utf-8"), re.S).group(0)  # same keys + video play/pause
page = (head.replace("<title>", "<title>Talk 6 Nov · ").rstrip() + "\n" + CSS + "\n" + DRAMA_CSS + "\n</head>\n<body>\n<div id=\"stage\">\n\n"
        + "\n\n".join(out) + "\n\n</div>\n<div id=\"count\"></div>\n" + js + "\n</body>\n</html>\n")
(here / "talk.html").write_text(page, encoding="utf-8")
print(f"talk.html: {len(out)} slides, {sum('data-video' in s for s in out)} videos")
