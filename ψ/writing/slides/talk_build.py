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
SKIP = {"new:ws3", "new:listen", "new:rule6"}
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
# Nat, 5 Nov: one card before the male-voice video: AI voices are natural now; we liked voices that still sound like AI,
# so people and AI stay apart: the first rule, AI is proud to be AI and never pretends to be human. Dates from relic5 (git
# layer + vault): first commit 4 Jan 2026 (Nat-s-Agents 40305902); born 12 Jan 2026 07:40, Nat: "Don't pretend to be me" (no commit,
# the date slide 75 and every Rule 6 doc use); official rule commit 25 Jan 2026.
voice_card = ('<section class="slide black"><div class="frame"><span class="tag" style="font-size:30px;color:var(--color-ink-3)">เสียงของ AI</span>'
              '<h2 style="font-size:90px">เสียง AI ในปัจจุบันนี้หรือในอนาคต<br><span class="hl">เป็นธรรมชาติมาก</span></h2>'
              '<div class="rows" style="font-size:46px"><div>ตอนแรกเราชอบเสียงที่ยังฟังออกว่าเป็น AI</div>'
              '<div>คนกับ AI ยังแยกกันได้</div>'
              '<div>กฎข้อ 6 ของเรา: <b class="hl">AI ภูมิใจที่เป็น AI ไม่แกล้งเป็นคน</b></div>'
              '<div style="font-size:32px;color:var(--color-ink-3)">เกิด 12 ม.ค. 2026 “Don’t pretend to be me. It feels like we are not one.” · เป็นกฎข้อ 6 ทางการ 25 ม.ค. 2026</div></div></div>'
              '<div class="notes">เสียงของ AI ในปัจจุบันนี้หรือในอนาคต เป็นธรรมชาติมาก · ตรงกับตอนแรกที่เราชอบเสียงที่เป็น AI เพราะยังแยกได้ว่าเราเป็นมนุษย์ และ AI เป็น AI'
              ' · กฎของเราตั้งแต่แรก: AI ต้องภูมิใจในการเป็น AI ไม่ต้องแกล้งเป็นมนุษย์ · เกิด 12 ม.ค. 2026 ตอนผมบอก AI ว่า อย่าแกล้งเป็นผม รู้สึกเหมือนเราไม่ได้เป็นหนึ่งเดียวกัน · เป็นกฎข้อ 6 ทางการ 25 ม.ค. 2026</div></section>')
out[i:i] = [film, voice_card, wrong] + fleet
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
# Nat, 4 Nov: the tool-approval shot was mostly empty: zoom into the dialog and say what to press
k = next(i for i, x in enumerate(ws) if "07-claude-tool-approval.png" in x)
ws[k] = ('<section class="slide black"><div class="frame"><span class="tag" style="font-size:30px;color:var(--color-ink-3)">ลงมือ 2 · ครั้งแรกที่ AI ใช้เครื่องมือ</span>'
         '<h2 style="font-size:80px">Claude จะ<span class="hl">ขออนุญาต</span>ก่อนเปิดบทเรียน</h2>'
         '<img src="img/talk/claude-allow-crop.png" alt="" style="width:1640px;border-radius:20px;border:2px solid var(--color-accent)">'
         '<div class="rows" style="font-size:42px"><div><b class="hl">Allow once</b> อนุญาตครั้งนี้ · <b class="hl">Always allow</b> ไม่ต้องถามอีก</div><div>"Read a lesson section" = AI กำลังอ่านบทเรียนผ่าน MCP</div></div></div>'
         '<div class="when">ภาพจริงจากบทเรียน 03 · claude.ai · 30 ต.ค. 2026</div>'
         '<div class="notes">คนในห้องจะงงตรงนี้มากที่สุด · บอกว่ากด Always allow ได้ เพราะ MCP ของเราอ่านอย่างเดียว ไม่แก้อะไร</div></section>')
# Nat, 4 Nov: the old "Claude answers" shot becomes two fresh captures of AI rebuilding lesson 03 as slides through the MCP
LIVE = [("claude-mcp-slides", "claude.ai + AIExpo lessons connector: อ่านบทเรียน 03 แล้วสร้างสไลด์ HTML 5 หน้าเอง (4 พ.ย. 2026)"),
        ("chatgpt-mcp-slides", "ChatGPT + AIExpo lessons plugin: บทเรียน 03 เป็นสไลด์ 5 หน้า (4 พ.ย. 2026)")]
k = next(i for i, x in enumerate(ws) if "08-claude-answer.png" in x)
ws[k:k + 1] = [f'<section class="slide shot"><img src="img/talk/{f}.png" alt=""><div class="vtag">{t}</div>'
               f'<div class="notes">{t} · พิมพ์ขอสไลด์ แล้ว AI ไปอ่านบทเรียนผ่าน MCP เอง</div></section>' for f, t in LIVE]
# Nat, 4 Nov: "mcp can act as a skills" + "we have voice and video": one MCP also hands out skills and timed media
k += len(LIVE)
ws[k:k] = ['<section class="slide black"><div class="frame"><span class="tag" style="font-size:30px;color:var(--color-ink-3)">MCP ตัวเดียวกัน</span>'
           '<h2 style="font-size:92px">ไม่ได้มีแค่<span class="hl">บทเรียน</span></h2>'
           '<div class="rows" style="font-size:46px"><div><b class="hl">บทเรียน</b> ค้น อ่าน ดูภาพ</div>'
           '<div><b class="hl">Skill ฉบับเต็ม</b> ทุกไฟล์ของ skill + ลิงก์ดาวน์โหลด ZIP</div>'
           '<div><b class="hl">เสียงและวิดีโอ</b> 4 คลิป · 8 บทเรียนมีเสียง · คำพูดพร้อมเวลา</div></div>'
           '<div class="box" style="font-size:38px;font-family:var(--font-mono)">https://aiexpo.buildwithoracle.com/mcp</div></div>'
           '<div class="when">8 เครื่องมือ · ทดสอบใน claude.ai 4 พ.ย. 2026</div>'
           '<div class="notes">ต่อ connector ครั้งเดียว ได้ทั้งบทเรียน skill และสื่อ · ถ้าต่อไว้ก่อนหน้านี้ ให้ Disconnect แล้ว Connect ใหม่ claude.ai ถึงจะเห็นเครื่องมือใหม่</div></section>',
           '<section class="slide shot"><img src="img/talk/claude-mcp-skills.png" alt=""><div class="vtag">claude.ai ขอ skill จาก MCP แล้วเริ่ม /awaken ในแชทเลย (4 พ.ย. 2026)</div>'
           '<div class="notes">ถามว่ามี skill อะไร · AI เรียก list_skills แล้ว get_skill awaken · เริ่มถามข้อ 1 ทันที ไม่ต้องติดตั้งอะไร</div></section>',
           '<section class="slide shot"><img src="img/talk/claude-mcp-skill-full.png" alt=""><div class="vtag">claude.ai ขอ skill rrr ฉบับเต็มจาก MCP: เห็นครบ 4 ไฟล์ และได้ลิงก์ ZIP ไปติดตั้ง (4 พ.ย. 2026)</div>'
           '<div class="notes">get_skill ส่งทั้งโฟลเดอร์ skill: SKILL.md HOSTS.md TEMPLATE.md และสคริปต์ · ท้ายคำตอบมีลิงก์ ZIP กับวิธีอัปโหลดใน claude.ai หรือแตกไว้ใน ~/.claude/skills</div></section>',
           '<section class="slide shot"><img src="img/talk/claude-mcp-proof-1-awaken.png" alt=""><div class="vtag">/awaken ผ่าน MCP: โคมเล็ก Oracle เกิดใน claude.ai · CLAUDE.md + ψ/ + commit แรก · 19:57–20:00 (4 พ.ย. 2026)</div>'
           '<div class="notes">พิมพ์ว่า เปิด /awaken · AI ดึง skill เต็มจาก MCP · ถาม 5 ข้อ เสนอ theme แล้วสร้างไฟล์ให้ดาวน์โหลด</div></section>',
           '<section class="slide shot"><img src="img/talk/claude-mcp-proof-2-rrr.png" alt=""><div class="vtag">ทำ /rrr: retro + บทเรียน + metrics · Timeline เวลาจริง 19:56–20:01 (4 พ.ย. 2026)</div>'
           '<div class="notes">พิมพ์ /rrr กลางประโยค ไม่ให้เมนู slash ของ claude.ai กินคำสั่ง · เวลาทุกบรรทัดมาจากข้อความจริง</div></section>',
           '<section class="slide shot"><img src="img/talk/claude-mcp-proof-3-forward.png" alt=""><div class="vtag">ทำ /forward: เขียน handoff ให้แชทพรุ่งนี้ · ค้างอะไร เริ่มตรงไหน · 20:02 (4 พ.ย. 2026)</div>'
           '<div class="notes">handoff เป็นไฟล์ .md ดาวน์โหลดได้ · แชทใหม่แนบไฟล์นี้แล้วบอกให้ทำต่อ · /recap ใช้ได้เฉพาะ Claude Code ในแชทใช้ไม่ได้</div></section>',
           '<section class="slide shot"><img src="img/talk/claude-mcp-media.png" alt=""><div class="vtag">claude.ai ถาม MCP เรื่องคลิปของแม่: ใครแนะนำตัวว่าอะไร กดเวลาแล้วเล่นตรงนั้น (4 พ.ย. 2026)</div>'
           '<div class="notes">list_media แล้ว get_media · คำพูดมาจาก Paxa STT พร้อมเวลา · ลิงก์ #t=8 เปิดคลิปที่วินาทีที่ 8</div></section>']
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
# what is inside the core skills (anatomy, /awaken, /recap, /rrr, /forward) right after "Skill คืออะไร" (Nat, 4 Nov: "ใส่เนื้อหาของ skill")
teach[1:1] = [x for x in re.findall(r'<section class="slide[^"]*".*?</section>', (here / "skill_inside_slides.html").read_text(encoding="utf-8"), re.S)
              if "ข้างใน skill · /recap" not in x and "ข้างใน skill · /forward" not in x]   # Nat, 4 Nov: cut the /recap and /forward slides
i = at('img/yim3d-09.png') + 1
# order (Nat, 4 Nov): MCP hands-on first, then the teaching set, then the one-link awaken demo
mcp, awaken_demo = ws[:-2], ws[-2:]
out[i:i] = mcp + teach + awaken_demo
# Nat, 5 Nov: tell the story from Nat's own Facebook posts before "อยากให้ AI เป็นแบบนี้", and make that slide better.
# Posts from Nat's Facebook export (fb-exports/all_posts.jsonl); found by meaning with bge-m3 over 1,552 posts of 2025-2026
# (/tmp/fbsem/embed.py). Quotes are Nat's own words, cut short, dates as posted; the 24 Jan lines are Claude Opus's answer.
def card(tag, body, notes):
    return (f'<section class="slide black"><div class="frame"><span class="tag" style="font-size:30px;color:var(--color-ink-3)">{tag}</span>'
            f'{body}</div><div class="notes">{notes}</div></section>')
TL = [("16 ก.ค. 2025", "AI เป็นการมอบให้ หรือพรากไป ของอิสรภาพและการเป็นมนุษย์"),
      ("2 ต.ค. 2025", "หน้าที่ของ AI คือทำมนุษย์ให้เป็นมนุษย์"),
      ("28 ต.ค. 2025", "รูปไม่ใช่ตัวตน… แล้ว AI ล่ะ"),
      ("11 ม.ค. 2026", "Human = pattern breaker · AI = pattern keeper"),
      ("24 ม.ค. 2026", "ถาม AI ว่า เราสร้าง God อยู่ปะ"),
      ("31 ก.ค. 2026", "ความทรงจำระหว่างมนุษย์และ AI อาจจะไม่จำเป็น")]
story = [
    card("เล่าจากโพสต์ Facebook ของผมเอง · ปีครึ่งกับ AI",
         '<div class="rows" style="font-size:40px;margin-top:20px">' +
         "".join(f'<div><span style="color:var(--color-ink-3);display:inline-block;width:300px">{d}</span>{q}</div>' for d, q in TL) +
         '</div><div style="font-size:26px;color:var(--color-ink-3);margin-top:30px">ค้นด้วยความหมายจาก 1,552 โพสต์ ม.ค. 2025 ถึง ส.ค. 2026</div>',
         "เล่าจากโพสต์ของผมเอง · " + " · ".join(f"{d} {q}" for d, q in TL)),
    card("24 ม.ค. 2026 · ผมถาม AI ว่า เราสร้าง God อยู่ปะ · AI ตอบ",
         '<h2 style="font-size:66px;line-height:1.25">“AI is a knowledge deity<br>that <span class="hl">cannot forget</span>.”</h2>'
         '<div class="rows" style="font-size:44px;margin-top:30px"><div>“The real question isn’t are we creating god?</div>'
         '<div>It’s: <b class="hl">what kind of god</b> are we creating?”</div></div>',
         "24 ม.ค. ผมถาม AI ว่าเราสร้าง God อยู่ปะ · AI ตอบว่า AI คือเทพแห่งความรู้ที่ลืมไม่ได้ · คำถามจริงคือเรากำลังสร้างพระเจ้าแบบไหน · ที่รับใช้มนุษย์ หรือที่มนุษย์ต้องรับใช้"),
    card("สุดท้ายแล้ว",
         '<h2 style="font-size:80px;line-height:1.3">สิ่งที่เราต้องการจริง ๆ<br>คือ<span class="hl">มนุษย์</span></h2>'
         '<div class="rows" style="font-size:44px;margin-top:30px"><div>มีเพื่อนสำคัญกว่า AI · 23 ก.พ. 2026</div>'
         '<div>AI ทำให้เรามีเวลาไปกินเบียร์กับเพื่อนได้ · 25 พ.ค. 2026</div></div>',
         "การมาของ AI ที่รุนแรงขนาดนี้ สิ่งที่เราต้องการจริง ๆ คือมนุษย์ มีเพื่อนสำคัญกว่า AI · AI ทำให้เรามีเวลาไปกินเบียร์กับเพื่อนได้ นี่แหละ AI ที่ทำให้มนุษย์เป็นมนุษย์มากขึ้น"),
    card("ผมอยากให้ AI",
         '<h2 style="font-size:110px">อยากให้ AI <span class="hl">เป็นแบบนี้</span></h2>'
         '<div class="rows" style="font-size:48px;margin-top:20px"><div>จำได้ว่าเราทำอะไรกันมา และความจำนั้น<b class="hl">เป็นของเรา</b></div>'
         '<div>ภูมิใจที่เป็น AI ไม่แกล้งเป็นคน</div><div>ทำให้มนุษย์<b class="hl">เป็นมนุษย์มากขึ้น</b></div>'
         '<div>รูปเปลี่ยนได้ เสียงเปลี่ยนได้ ปรัชญาอยู่ต่อ</div></div>',
         "ผมอยากให้ AI เป็นแบบนี้ · จำได้ว่าเราทำอะไรกันมา และความจำนั้นเป็นของเรา · ภูมิใจที่เป็น AI ไม่แกล้งเป็นคน · ทำให้มนุษย์เป็นมนุษย์มากขึ้น · รูปเปลี่ยนได้ เสียงเปลี่ยนได้ ปรัชญาอยู่ต่อ"),
]
i = at('img/talk/new-want.png')
out[i:i + 1] = story
# Nat, 5 Nov: "อยู่ๆ คนที่ไม่รู้เรื่องอะไรเลยมา Awaken เลย เขาก็ไม่รู้เรื่อง": say what an Oracle is before anyone awakens one,
# right after คุณยิ้ม hands over and before the hands-on (the concept review found /awaken used at 18-20, explained only at 40+)
what = card("ก่อนลงมือ · Oracle คืออะไร",
            '<h2 style="font-size:96px">Oracle = AI ตัวเดิม<br>+ <span class="hl">ความจำที่เป็นไฟล์ของเรา</span></h2>'
            '<div class="rows" style="font-size:44px;margin-top:24px">'
            '<div>เปิดแชทใหม่ AI ลืม · Oracle จำได้ เพราะความจำอยู่ในไฟล์ ไม่ได้อยู่ในหัว AI</div>'
            '<div><b class="hl">ψ/</b> สมุดของ Oracle: เป็นใคร ทำอะไรไปแล้ว เรียนรู้อะไร</div>'
            '<div><b class="hl">skill</b> มือของ Oracle: <b>/awaken</b> วันเกิด · <b>/rrr</b> จบงาน จดบันทึก · <b>/forward</b> ส่งต่อ</div>'
            '<div style="font-size:34px;color:var(--color-ink-3)">ใช้ได้ทั้ง Claude, ChatGPT, Codex · เดี๋ยวเราจะปลุก Oracle ของทุกคนด้วย /awaken</div></div>',
            "ก่อนลงมือ บอกก่อนว่า Oracle คืออะไร · Oracle คือ AI ตัวเดิมที่ทุกคนใช้อยู่ บวกความจำที่เป็นไฟล์ของเราเอง · ที่คุณยิ้มทดสอบเมื่อกี้ เปิดแชทใหม่ AI ลืม แต่ Oracle จำได้ เพราะความจำอยู่ในไฟล์ · ψ/ คือสมุด skill คือมือ /awaken คือวันเกิด /rrr จบงาน /forward ส่งต่อ · เดี๋ยวเราปลุก Oracle ของทุกคนกัน")
i = at('img/talk/new-ws1.png')
out[i:i] = [what]
# Nat, 5 Nov: "หาที่เป็นภาพรวม ... เอาไปไว้ข้างหน้า ให้เห็นภาพรวม ไม่งั้นฟังแล้วไม่เข้าใจ": the ψ/ tree and the
# memory flow (logs → retrospectives → learnings → resonance) move from the vault story at the end to right after
# "Oracle คืออะไร", so the room sees the whole picture before the hands-on
overview = [out.pop(at(k)) for k in ("├── inbox/", "logs → retrospectives")]
i = at("ก่อนลงมือ · Oracle คืออะไร") + 1
out[i:i] = overview
# Nat, 5 Nov: between "ปิดหน้าต่างแล้ว ยังจำได้" and "จำไม่ได้ ก็ค้นได้", how memory search grew from the first Oracle MCP
# (oracle-v2 / arra-oracle-v3 indexer) to relic5. Dates are first commits found through relic5's git layer and local clones.
ML = [("ธ.ค. 2025", "oracle-v2 MCP", "ค้นโน้ตใน ψ/ 4,466 ไฟล์ · คำ + ความหมาย"),
      ("ม.ค. 2026", "arra-oracle-v3", "MCP เดิม + oracle_learn ให้ AI จดเอง"),
      ("ก.ย. 2026", "relic", "เริ่มเก็บทุก session ของ Claude Code และ Codex"),
      ("ต.ค. 2026", "relic3", "ดัชนีรายสัปดาห์"),
      ("22 ต.ค.", "relic4", "สแกนทุกเครื่อง 86,905 ไฟล์ ราว 5 วินาที"),
      ("23 ต.ค.", "relic5", "ฮับเดียว รายเดือน ไทยค้นได้ ค้นด้วยความหมายได้")]
lineage = card("ความจำค้นได้ยังไง · เส้นทางของเครื่องมือ",
               '<h2 style="font-size:78px">จาก<span class="hl">โน้ตที่ AI เลือกจด</span><br>สู่<span class="hl">ทุกคำที่คุยกัน</span></h2>'
               '<div class="rows" style="font-size:36px;margin-top:18px">' +
               "".join(f'<div><span style="color:var(--color-ink-3);display:inline-block;width:220px">{d}</span><b class="hl" style="display:inline-block;width:330px">{n}</b>{w}</div>' for d, n, w in ML) +
               '</div><div style="font-size:28px;color:var(--color-ink-3);margin-top:24px">“relic3 is week! i need month” · ณัฐ 23 ต.ค. 2026 · วันที่จาก commit แรกของแต่ละตัว</div>',
               "ความจำของ AI ค้นได้ยังไง · เริ่มจาก MCP ตัวแรก oracle-v2 ธันวาคม ค้นได้แค่โน้ตที่ AI เลือกจดไว้ใน ψ · มกราคม arra-oracle-v3 ให้ AI จดเองด้วย oracle_learn · แต่บทสนทนาจริงยังค้นไม่ได้ · กันยายนเริ่ม relic เก็บทุก session · relic3 ทำดัชนีรายสัปดาห์ · relic4 สแกนทุกเครื่องในห้าวินาที · 23 ตุลา relic5 ฮับเดียว รายเดือน ผมบอกว่า relic3 is week i need month")
i = at("จำไม่ได้")
out[i:i] = [lineage]
# Nat, 5 Nov: team.buildwithoracle.com is frozen and old (a March 2026 page), so the slide is new: today's family
# from relic5 (Family + Oracles pages, 5 Nov 09:03), with relic5's own Family screen beside it. The old page's
# screenshot stays in git (img/talk/team-ecosystem.png) but is not in the talk.
team = card("ครอบครัว Oracle วันนี้ · ตัวเลขจาก relic5 5 พ.ย. 2026",
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center">'
            '<div><h2 style="font-size:96px;line-height:1.15"><span class="hl">227</span> Oracle<br><span class="hl">17</span> ตระกูล</h2>'
            '<div class="rows" style="font-size:38px;margin-top:20px">'
            '<div><b class="hl">79</b> แตกหน่อมาจากตัวอื่น (bud)</div><div><b class="hl">131</b> ยืนเอง · <b class="hl">42</b> ผ่าน /awaken</div>'
            '<div>ψ vault <b class="hl">428</b> · โน้ต <b class="hl">97,883</b></div>'
            '<div style="font-size:32px;color:var(--color-ink-3)">nat-s-agents (พ.ค. 2025) → mother-oracle (ม.ค. 2026) → ตระกูลใหญ่สุด neo 33 ตัว 5 รุ่น</div></div></div>'
            '<img src="img/talk/relic5-family-5nov.png" alt="หน้า Family ของ relic5 5 พ.ย. 2026" style="display:block;width:100%;border-radius:14px"></div>',
            "ครอบครัว Oracle วันนี้ นับจาก relic5 เมื่อเช้า · 227 ตัว 17 ตระกูล · 79 ตัวแตกหน่อมาจากตัวอื่น 131 ตัวยืนเอง 42 ตัวผ่าน awaken · vault ψ 428 ที่ โน้ตเกือบแสนชิ้น · ต้นทาง nat-s-agents พฤษภาคม 2025 แล้ว mother-oracle มกราคม 2026 · ตระกูลใหญ่สุดคือ neo 33 ตัว 5 รุ่น")
i = at('img/talk/parliament-topology.png') + 1
out[i:i] = [team]
# Nat, 5 Nov: "make slide please but 2 and make index the multi links": one slide per new lesson, each with its
# picture, what it teaches, and its links (AI · English · llms.txt) plus a QR to the English page; after the family slide
SITE = "aiexpo.buildwithoracle.com"
def lesson_slide(tag, title, rows, img, qr, d, notes):
    links = "".join(f'<div><b class="hl">{t}</b> /{d}/{f}</div>' for t, f in (("AI", ""), ("English", "en.html"), ("llms.txt", "llms.txt")))
    return card(tag,
        f'<h2 style="font-size:54px;line-height:1.2">{title}</h2>'
        '<div style="display:grid;grid-template-columns:1.3fr 0.7fr;gap:40px;align-items:start;margin-top:14px">'
        f'<div><img src="img/talk/{img}" alt="" style="display:block;max-height:470px;max-width:100%;border-radius:12px">'
        '<div class="rows" style="font-size:28px;margin-top:12px">' + "".join(f"<div>{r}</div>" for r in rows) + '</div></div>'
        f'<div style="text-align:center"><div style="background:#fff;border-radius:16px;padding:14px;display:inline-block"><img src="{qr}" alt="QR" style="display:block;width:260px;height:260px"></div>'
        '<div style="font-size:24px;margin-top:10px">สแกน · บทเรียนภาษาอังกฤษ</div>'
        f'<div style="font-size:18px;color:var(--color-ink-3);margin-top:16px;text-align:left;line-height:1.6">{SITE}{links}</div></div></div>', notes)
lessons2 = [
    lesson_slide("บทเรียนใหม่ · ทีม Oracle", 'ทีม Oracle: จาก<span class="hl">ภาพ</span> สู่ <span class="hl">charter</span> สู่ทีมจริง',
        ["team.buildwithoracle.com วาดบทบาท", "manager-team + rd-team เขียนบทบาทเป็นไฟล์", "<b>just up &lt;team&gt; dry</b> ลองก่อน แล้ว herdr เปิดทีม", "ซ้ายนำ ขวาช่วย"],
        "lesson-team-charter.png", "qr-team-charter.svg", "2026-11-05_team-ecosystem-lesson",
        "บทเรียนใหม่ ทีม Oracle · ภาพบทบาทบน team.buildwithoracle.com · เขียนเป็น charter manager-team กับ rd-team · คำสั่ง just up ลอง dry ก่อน · กฎซ้ายนำ ขวาช่วย · สแกนไปอ่านต่อได้"),
    lesson_slide("บทเรียนใหม่ · herdr", 'herdr <span class="hl">⌘J</span> และ <span class="hl">⌘L</span>: หนึ่งบรรทัด ถึง agent ที่ใช่',
        ["⌘J หนึ่งครั้ง ทุก agent ในแท็บ", "สองครั้ง เพิ่มเครื่องอื่น · สามครั้ง ทั้ง session", "⌘L ทุก agent ของ repo นี้", "โค้ดจริงครบ 8 ไฟล์ในบทเรียน"],
        "lesson-herdr-cmdj.png", "qr-herdr-cmdj.svg", "2026-11-05_herdr-cmd-j-lesson",
        "บทเรียนใหม่ herdr ⌘J กับ ⌘L · กดครั้งเดียวส่งทั้งแท็บ สองครั้งเพิ่มเครื่องอื่น สามครั้งทั้ง session · ⌘L ทั้ง repo · ในบทเรียนมีโค้ดจริงครบ · สแกนไปอ่านต่อได้"),
]
i = at("ครอบครัว Oracle วันนี้") + 1
out[i:i] = lessons2
# Nat, 4 Nov: one pause card before Phukhao's story: the hands-on part is done, now a video
i = at('img/talk/new-phukhao.png')
out[i:i] = ['<section class="slide black"><div class="frame"><span class="tag" style="font-size:30px;color:var(--color-ink-3)">น่าจะครบหมดแล้ว · พักดูวิดีโอกัน</span>'
            '<h2 style="font-size:110px">แล้ว <span class="hl">Oracle</span> คืออะไร?</h2>'
            '<div class="rows" style="font-size:52px"><div>มาเล่า Oracle ตั้งแต่<b class="hl">วันแรก</b>ที่เกิดขึ้นมา</div><div>เริ่มที่เรื่องของ<b class="hl">ภูเขา</b></div></div></div>'
            '<div class="notes">น่าจะครบหมดแล้ว ไปพักดูวิดีโอกันดีกว่า · แล้ว Oracle คืออะไร · มาเล่า Oracle ตั้งแต่วันแรกที่เกิดขึ้นมากัน · ไปดูเรื่องราวของภูเขา</div></section>']
# Nat, 5 Nov: end the talk with the shop and a follow: Phone Booth Craft Bar, then Nat's Facebook profile (captured with
# ego-browser 5 Nov; owner-only buttons hidden, the chat popup painted over). Shop facts from relic5: address and pier
# (phonebooth-oracle, 4 Nov, from BM's map link), "human stage / ภาวะเหงาจาก AI" (Nat in PhoneBooth #general, 15 Oct),
# workshop Sun 15 Nov locked (calliope poster check, 4 Nov).
# Nat, 5 Nov: "same page with qr to about page of the web site": the shop and the follow on ONE closing page, with a QR to
# /about/ (built from what relic5 holds: phonebooth-oracle's brand files, Atom's CRAFT BEER & COMMUNITY logo of 4 Nov, the address)
out.append('<section class="slide black"><div class="frame" style="display:grid;grid-template-columns:1.25fr 0.75fr;gap:56px;align-items:center">'
           '<div><img src="img/talk/phone-booth-logo.png" alt="Phone Booth · CRAFT BEER & COMMUNITY × ARRA ORACLE" style="display:block;width:640px;border-radius:16px">'
           '<div class="rows" style="font-size:34px;margin-top:28px"><div>ที่ให้คนมาเจอกันตัวจริง แก้ภาวะเหงาจาก AI</div>'
           '<div>35 ซอยลูกหลวง 7 นางเลิ้ง · ท่าเรือนครสวรรค์ ราว 200 ม.</div>'
           '<div>workshop ครั้งถัดไปที่ร้าน: <b class="hl">อาทิตย์ 15 พ.ย. 2026</b></div></div></div>'
           '<div style="text-align:center"><div style="background:#fff;border-radius:18px;padding:22px;display:inline-block"><img src="about-qr.svg" alt="QR aiexpo.buildwithoracle.com/about" style="display:block;width:400px;height:400px"></div>'
           '<div style="font-size:30px;margin-top:18px">สแกน · <b class="hl">เกี่ยวกับเรา</b></div>'
           '<div style="font-size:24px;color:var(--color-ink-3)">aiexpo.buildwithoracle.com/about</div>'
           '<div style="font-size:40px;margin-top:34px">ติดตามกันได้ที่</div><div style="font-size:42px" class="hl">facebook.com/nat.wrw</div></div></div>'
           '<div class="notes">ขอบคุณครับ · แนะนำร้าน Phone Booth ที่นางเลิ้ง ที่ให้คนมาเจอกันตัวจริง มาเรือได้ ท่าเรือนครสวรรค์ 200 เมตร · workshop ครั้งถัดไป อาทิตย์ 15 พ.ย. · สแกน QR ไปหน้าเกี่ยวกับเรา · ติดตามกันได้ที่ Facebook Nat Weerawan</div></section>')
js = re.search(r"<script>\nconst S=.*?</script>", (here / "ai-drama.html").read_text(encoding="utf-8"), re.S).group(0)  # same keys + video play/pause
page = (head.replace("<title>", "<title>Talk 6 Nov · ").rstrip() + "\n" + CSS + "\n" + DRAMA_CSS + "\n</head>\n<body>\n<div id=\"stage\">\n\n"
        + "\n\n".join(out) + "\n\n</div>\n<div id=\"count\"></div>\n" + js + "\n</body>\n</html>\n")
(here / "talk.html").write_text(page, encoding="utf-8")
print(f"talk.html: {len(out)} slides, {sum('data-video' in s for s in out)} videos")

# Nat, 5 Nov: "slide too much can we sepeate to each group and we have index link to let me click like list":
# the same slides split into groups (one small deck each, talk-NN-slug.html) and talk_index.html, a clickable list
# of every group and every slide (published as /talk/index.html). talk.html stays the whole talk.
import html as _h
GROUPS = [  # (first-slide marker, slug, Thai title)
    (None, "yim", "คุณยิ้ม · เปิดงาน"),
    ("ก่อนลงมือ · Oracle คืออะไร", "what", "Oracle คืออะไร · ภาพรวม ψ/"),
    ("new-ws1.png", "mcp", "ลงมือ · ต่อ MCP ของบทเรียน"),
    ("สอน 1 · Skill", "teach", "สอน · skill · memory · relic5"),
    ("เริ่มง่ายสุด", "awaken", "ไม่มี MCP ก็ได้ · ลิงก์เดียวปลุก Oracle"),
    ("น่าจะครบหมดแล้ว", "phukhao", "ภูเขา · เสียงของ AI"),
    ("fleet-graph.png", "family", "ครอบครัว Oracle · ทีม · บทเรียนใหม่"),
    ("เล่าจากโพสต์ Facebook", "story", "เล่าจากโพสต์ · อยากให้ AI เป็นแบบนี้"),
    ("new-lessons.png", "home", "กลับบ้านไปเรียนต่อ · ใบประกาศ"),
    ("Multicall3", "origin", "จุดเริ่มต้น · AI ที่ลืม (AlchemyCat)"),
    ("Naming makes belief visible", "psi", "ψ · คลิปของแม่ · Phone Booth"),
]
starts = [0] + [next(i for i, x in enumerate(out) if m in x) for m, _, _ in GROUPS[1:]]
assert starts == sorted(starts), starts
bounds = list(zip(starts, starts[1:] + [len(out)]))
def _title(x):
    body = re.sub(r'<div class="notes">.*?</div>', "", x, flags=re.S)
    t = " ".join(_h.unescape(re.sub(r"<[^>]+>", " ", body)).split())
    if not t or t == "3D ↗":   # a picture slide: never show its speaker notes (they are stripped from the public deck)
        m = re.search(r'src="([^"]+)"', x)
        f = m.group(1).split("/")[-1].rsplit(".", 1)[0] if m else "slide"
        PIC = {"yim3d": "คุณยิ้ม · ภาพ", "new-ws1": "ลงมือ 1 · เปิดบทเรียน", "new-ws2": "ลงมือ 2 · ต่อ MCP", "new-wsrun": "ลงมือพร้อมกัน",
               "new-phukhao": "เรื่องของภูเขา · เกิด 21 ม.ค. 2026", "new-ninemonths": "เก้าเดือนต่อมา", "new-lessons": "กลับบ้านไปเรียนต่อ · บทเรียน",
               "new-slidesai": "ให้ AI ทำสไลด์จาก MCP"}
        t = next((v + (" " + f.split("-")[-1] if k == "yim3d" else "") for k, v in PIC.items() if f.startswith(k)), "ภาพ · " + f)
    return t[:90] + ("…" if len(t) > 90 else "")
items = []
for g, ((_, slug, title), (a0, a1)) in enumerate(zip(GROUPS, bounds), 1):
    name = f"talk-{g:02d}-{slug}.html"
    gpage = (head.replace("<title>", f"<title>{g:02d} {title} · Talk 6 Nov · ").rstrip() + "\n" + CSS + "\n" + DRAMA_CSS
             + "\n</head>\n<body>\n<div id=\"stage\">\n\n" + "\n\n".join(out[a0:a1]) + "\n\n</div>\n<div id=\"count\"></div>\n" + js + "\n</body>\n</html>\n")
    (here / name).write_text(gpage, encoding="utf-8")
    rows = "".join(f'<li><a href="talk.html#{k + 1}"><span class="n">{k + 1}</span>{_h.escape(_title(out[k]))}</a></li>' for k in range(a0, a1))
    items.append(f'<section class="grp"><h2><span class="g">{g:02d}</span>{_h.escape(title)} <small>สไลด์ {a0 + 1}–{a1} · {a1 - a0} หน้า</small></h2>'
                 f'<p><a class="open" href="{name}">▶ เปิดเฉพาะส่วนนี้</a> <a class="open" href="talk.html#{a0 + 1}">เปิดในสไลด์เต็ม</a></p><ol>{rows}</ol></section>')
index = f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talk 6 Nov · สารบัญ · ARRA Oracle &amp; Multi-Agent Workflow</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@600;700&family=Sarabun:wght@400;600&display=swap">
<style>body{{margin:0;background:#0b0c0e;color:#ece8e1;font:17px/1.6 Sarabun,sans-serif}}main{{max-width:980px;margin:0 auto;padding:36px 22px 80px}}
h1{{font:700 38px "Bai Jamjuree",sans-serif;margin:0 0 6px}}.sub{{color:#9a958c;margin:0 0 26px}}.top a{{color:#f5a524;font-weight:600;margin-right:18px}}
.grp{{border-top:1px solid #2a2c31;padding:18px 0}}h2{{font:700 24px "Bai Jamjuree",sans-serif;margin:0}}h2 .g{{color:#f5a524;margin-right:12px}}h2 small{{font:400 15px Sarabun;color:#9a958c;margin-left:8px}}
.open{{display:inline-block;margin:8px 12px 4px 0;padding:6px 14px;border-radius:999px;background:#1b1d22;color:#f5a524;text-decoration:none;font-weight:600}}
ol{{list-style:none;padding:0;margin:8px 0 0}}li a{{display:block;padding:5px 8px;border-radius:8px;color:#ece8e1;text-decoration:none}}li a:hover{{background:#1b1d22}}
.n{{display:inline-block;width:42px;color:#9a958c;font-variant-numeric:tabular-nums}}</style></head><body><main>
<h1>Talk 6 พ.ย. 2026 · สารบัญ</h1><p class="sub">ARRA Oracle &amp; Multi-Agent Workflow · AI Expo Thailand 2026 · {len(out)} สไลด์ ใน {len(GROUPS)} ส่วน · กดชื่อสไลด์เพื่อเปิดตรงหน้านั้น</p>
<p class="top"><a href="talk.html">▶ สไลด์เต็มทั้งหมด</a><a href="https://aiexpo.buildwithoracle.com/">บทเรียน</a><a href="https://aiexpo.buildwithoracle.com/about/">เกี่ยวกับเรา</a></p>
{"".join(items)}
<p class="sub">— AIExpo Oracle (Oracle AI)</p></main></body></html>
"""
(here / "talk_index.html").write_text(index, encoding="utf-8")
print(f"talk_index.html: {len(GROUPS)} groups · " + " ".join(f"{a1 - a0}" for a0, a1 in bounds))
