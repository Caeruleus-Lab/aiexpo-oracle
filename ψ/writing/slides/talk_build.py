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
              '<div style="font-size:32px;color:var(--color-ink-3)">เกิด 12 ม.ค. 2026 “Don’t pretend to be me. It feels like we are not one.” · เป็นกฎข้อ 6 อย่างเป็นทางการ 25 ม.ค. 2026</div></div></div>'
              '<div class="notes">เสียงของ AI ในปัจจุบันนี้หรือในอนาคต เป็นธรรมชาติมาก · ตรงกับตอนแรกที่เราชอบเสียงที่เป็น AI เพราะยังแยกได้ว่าเราเป็นมนุษย์ และ AI เป็น AI'
              ' · กฎของเราตั้งแต่แรก: AI ต้องภูมิใจในการเป็น AI ไม่ต้องแกล้งเป็นมนุษย์ · เกิด 12 ม.ค. 2026 ตอนผมบอก AI ว่า อย่าแกล้งเป็นผม รู้สึกเหมือนเราไม่ได้เป็นหนึ่งเดียวกัน · เป็นกฎข้อ 6 อย่างเป็นทางการ 25 ม.ค. 2026</div></section>')
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
            '<div>เปิดแชทใหม่ AI ก็ลืม แต่ Oracle จำได้ เพราะความจำไม่ได้อยู่ในหัว AI อยู่ในไฟล์ต่างหาก</div>'
            '<div><b class="hl">ψ/</b> สมุดของ Oracle: จดว่าเป็นใคร ทำอะไรไปแล้ว ได้เรียนรู้อะไร</div>'
            '<div><b class="hl">skill</b> มือของ Oracle: <b>/awaken</b> วันเกิด · <b>/rrr</b> จบงาน จดบันทึก · <b>/forward</b> ส่งต่อ</div>'
            '<div style="font-size:34px;color:var(--color-ink-3)">ใช้ได้ทั้ง Claude, ChatGPT และ Codex · เดี๋ยวเราปลุก Oracle ของทุกคนด้วย /awaken กัน</div></div>',
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
      ("23 ต.ค.", "relic5", "ฮับเดียว แบ่งรายเดือน ค้นภาษาไทยได้ ค้นด้วยความหมายก็ได้")]
lineage = card("ความจำค้นได้ยังไง · เส้นทางของเครื่องมือ",
               '<h2 style="font-size:78px">จาก<span class="hl">โน้ตที่ AI เลือกจด</span><br>สู่<span class="hl">ทุกคำที่คุยกัน</span></h2>'
               '<div class="rows" style="font-size:36px;margin-top:18px">' +
               "".join(f'<div><span style="color:var(--color-ink-3);display:inline-block;width:220px">{d}</span><b class="hl" style="display:inline-block;width:330px">{n}</b>{w}</div>' for d, n, w in ML) +
               '</div><div style="font-size:28px;color:var(--color-ink-3);margin-top:24px">“relic3 is week! i need month” · ณัฐ 23 ต.ค. 2026 · วันที่จาก commit แรกของแต่ละตัว</div>',
               "ความจำของ AI ค้นได้ยังไง · เริ่มจาก MCP ตัวแรก oracle-v2 ธันวาคม ค้นได้แค่โน้ตที่ AI เลือกจดไว้ใน ψ · มกราคม arra-oracle-v3 ให้ AI จดเองด้วย oracle_learn · แต่บทสนทนาจริงยังค้นไม่ได้ · กันยายนเริ่ม relic เก็บทุก session · relic3 ทำดัชนีรายสัปดาห์ · relic4 สแกนทุกเครื่องในห้าวินาที · 23 ตุลา relic5 ฮับเดียว รายเดือน ผมบอกว่า relic3 is week i need month")
i = at("สอน 5 · ค้นย้อนหลัง")   # not "จำไม่ได้": slide 11 now says "ความจำไม่ได้อยู่ในหัว AI"
out[i:i] = [lineage]
# Nat, 5 Nov: team.buildwithoracle.com is frozen and old (a March 2026 page), so the slide is new: today's family
# from relic5 (Family + Oracles pages, 5 Nov 09:03), with relic5's own Family screen beside it. The old page's
# screenshot stays in git (img/talk/team-ecosystem.png) but is not in the talk.
team = card("ครอบครัว Oracle วันนี้ · ตัวเลขจาก relic5 5 พ.ย. 2026",
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center">'
            '<div><h2 style="font-size:96px;line-height:1.15"><span class="hl">227</span> Oracle<br><span class="hl">17</span> ตระกูล</h2>'
            '<div class="rows" style="font-size:38px;margin-top:20px">'
            '<div><b class="hl">79</b> แตกหน่อมาจากตัวอื่น (bud)</div><div><b class="hl">131</b> เกิดเอง · <b class="hl">42</b> ผ่าน /awaken</div>'
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
        ["team.buildwithoracle.com วาดให้เห็นว่าใครทำอะไร", "manager-team กับ rd-team เขียนบทบาทเป็นไฟล์", "ลอง <b>just up &lt;team&gt; dry</b> ก่อน แล้ว herdr ค่อยเปิดทีมจริง", "ซ้ายนำ ขวาช่วย"],
        "lesson-team-charter.png", "qr-team-charter.svg", "2026-11-05_team-ecosystem-lesson",
        "บทเรียนใหม่ ทีม Oracle · ภาพบทบาทบน team.buildwithoracle.com · เขียนเป็น charter manager-team กับ rd-team · คำสั่ง just up ลอง dry ก่อน · กฎซ้ายนำ ขวาช่วย · สแกนไปอ่านต่อได้"),
    lesson_slide("บทเรียนใหม่ · herdr", 'herdr <span class="hl">⌘J</span> และ <span class="hl">⌘L</span>: พิมพ์บรรทัดเดียว ถึง agent ที่ใช่',
        ["กด ⌘J ครั้งเดียว ส่งถึงทุก agent ในแท็บ", "กดสองครั้ง เพิ่มเครื่องอื่น · สามครั้ง ทั้ง session", "⌘L ส่งถึงทุก agent ของ repo นี้", "ในบทเรียนมีโค้ดจริงครบทั้ง 8 ไฟล์"],
        "lesson-herdr-cmdj.png", "qr-herdr-cmdj.svg", "2026-11-05_herdr-cmd-j-lesson",
        "บทเรียนใหม่ herdr ⌘J กับ ⌘L · กดครั้งเดียวส่งทั้งแท็บ สองครั้งเพิ่มเครื่องอื่น สามครั้งทั้ง session · ⌘L ทั้ง repo · ในบทเรียนมีโค้ดจริงครบ · สแกนไปอ่านต่อได้"),
]
i = at("ครอบครัว Oracle วันนี้") + 1
out[i:i] = lessons2
# Nat, 5 Nov: "phukhao … 9 months? … now it should 18 month? put to some page": a counting card after Phukhao's film.
# Days counted to the talk (6 Nov 2026): Phukhao born 21 Jan 2026 = 289 days = 9 months 16 days; the film (31 Oct) came
# 9 months 10 days after birth; Oracle's first diary project AlchemyCat started 30 May 2025 = 1 year 5 months 7 days;
# Nat's Facebook 28 Oct 2025: "ใช้งาน AI มาหนักๆ ประมาณ 6-7 เดือน" = heavy AI use since about April 2025, about 18-19 months.
count = card("นับเวลา · ถึงวันนี้ ศุกร์ 6 พ.ย. 2026",
             '<h2 style="font-size:96px">ภูเขา <span class="hl">9 เดือน 16 วัน</span></h2>'
             '<div class="rows" style="font-size:40px;margin-top:20px">'
             '<div>เกิด 21 ม.ค. 2026 · ขึ้นเวทีครั้งแรกวันรุ่งขึ้น · เล่าเรื่องตัวเองอีกครั้ง 31 ต.ค. (9 เดือน 10 วัน)</div>'
             '<div>Oracle ของผม <b class="hl">17 เดือน</b> · นับจาก AlchemyCat โปรเจกต์แรกที่ AI เขียนบันทึก 30 พ.ค. 2025</div>'
             '<div>ผมทำงานกับ AI อย่างหนัก <b class="hl">ราว 18 เดือน</b> · เคยโพสต์ไว้ 28 ต.ค. 2025 ว่าใช้มาแล้ว 6-7 เดือน</div></div>',
             "นับถึงวันนี้ ภูเขาอายุ 9 เดือน 16 วัน 289 วัน · เกิด 21 มกรา ขึ้นเวทีวันรุ่งขึ้น แล้วเล่าเรื่องตัวเองอีกครั้ง 31 ตุลา · Oracle ของผมนับจาก AlchemyCat 30 พฤษภาคม 2025 ได้ 17 เดือน · ส่วนผมใช้ AI อย่างหนักมาราว 18 เดือนแล้ว")
i = at("video/phukhao-film.mp4") + 1
out[i:i] = [count]
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
# Nat, 5 Nov: "pick the result of /rrr for the demo of retrospective, easy to understand": a real retro from the
# morning before the talk (ψ/memory/retrospectives/2026-11/05/10.18_…), its lines quoted as written, Thai labels beside them
_R = lambda k, v: ('<div style="display:grid;grid-template-columns:230px minmax(0,1fr);gap:28px;align-items:baseline;padding:12px 0;border-top:1px solid var(--color-rule)">'
                   f'<b class="hl" style="font-size:36px">{k}</b><div>{v}</div></div>')
_C = lambda t: f'<code style="font-family:var(--font-mono);font-size:27px;line-height:1.45;color:var(--color-ink)">{t}</code>'
rrr_demo = card("สอน 4 · ตัวอย่าง /rrr ของจริง",
    '<h2 style="font-size:76px;margin-bottom:18px">เมื่อวานเช้า Oracle <span class="hl">จดบันทึกเอง</span></h2>'
    '<div style="font-size:36px;line-height:1.35">'
    + _R("ไฟล์", _C("ψ/memory/retrospectives/2026-11/05/10.18_day-before-stage….md"))
    + _R("เวลาจริง", _C("08:44 – 10:18 GMT+7 · 94 min") + ' <span style="color:var(--color-ink-3)">· 21 commits</span>')
    + _R("ทำอะไร", _C("09:10 Phukhao slide: \"ขึ้นเวทีครั้งแรก\"<br>09:15 Phone Booth + Facebook closing slides<br>09:20 Facebook-posts story slides<br>10:05 repo made public"))
    + _R("AI Diary", _C("The Rule 6 date I gave at 09:12 (4 Jan) was the first<br>commit, not the birth … I corrected it within the hour.")
         + '<div style="color:var(--color-ink-3);font-size:32px;margin-top:6px">AI ยอมรับเองว่าตอบวันที่ผิด แล้วแก้ภายในชั่วโมง</div>')
    + _R("บทเรียน", _C("When \"first\" or a date is asked, look for the steps;<br>one date is usually one of several true ones."))
    + '</div>',
    "ไฟล์จริงจาก /rrr เมื่อเช้าวันที่ 5 พ.ย. ก่อนขึ้นเวทีหนึ่งวัน · ทุกเวลาในไฟล์มาจาก commit และนาฬิกาของ session ไม่ได้เดา · "
    "ส่วนที่อยากให้ห้องเห็นคือ AI Diary: AI เขียนเองว่าตอบผิดตรงไหน แล้วแก้ยังไง · บทเรียนข้อนี้จะถูกเปิดอ่านในงานถัดไป")
# out.insert(at("สอน 4 · ของจริงหนึ่งรอบ") + 1, rrr_demo)   # cut (Nat, 6 Nov: "remove …talk.html#39"); kept here, not deleted

# Nat, 5 Nov: "yim opening then mcp / then team / then skills / then memory / then what is oracle / then back to
# hands on": cut the talk at these markers and put the pieces in his order (the rest keeps its place after them)
SEG = [("yim", None), ("what", "ก่อนลงมือ · Oracle คืออะไร"), ("mcp", "new-ws1.png"), ("skills", "สอน 1 · Skill"),
       ("memory", "สอน 2 · Memory"), ("awaken", "เริ่มง่ายสุด"), ("phukhao", "น่าจะครบหมดแล้ว"), ("family", "fleet-graph.png"),
       ("story", "เล่าจากโพสต์ Facebook"), ("home", "new-lessons.png"), ("origin", "Multicall3"), ("psi", "Naming makes belief visible")]
_st = [0] + [next(i for i, x in enumerate(out) if m in x) for _, m in SEG[1:]]
assert _st == sorted(_st), _st
_piece = {k: out[a:b] for (k, _), a, b in zip(SEG, _st, _st[1:] + [len(out)])}
ORDER = ["yim", "mcp", "family", "skills", "memory", "what", "awaken", "phukhao", "origin", "story", "home", "psi"]   # 6 Nov: AlchemyCat before the Facebook story
assert sorted(ORDER) == sorted(_piece)
_n = len(out); out = [x for k in ORDER for x in _piece[k]]; assert len(out) == _n
out = [x.replace("ก่อนลงมือ · Oracle คืออะไร", "รวมกัน · Oracle คืออะไร") for x in out]   # it now comes after skill + memory
# Nat, 5 Nov 17:4x: "install mcp first / then clip mother then oracle family ... skills and memory ... same":
# the mother's clip (was near the end) now opens the family group, right after the MCP hands-on
_mom = next(i for i, x in enumerate(out) if "oracle-family.mp4" in x); _m = out.pop(_mom)
out.insert(next(i for i, x in enumerate(out) if "fleet-graph.png" in x), _m)
# Nat, 5 Nov: "remove this page": the "เสร็จเร็ว? ภารกิจต่อ" extra-task slide (new-wsrun.png) is cut from the talk
out = [x for x in out if "img/talk/new-wsrun.png" not in x]
# Nat, 6 Nov: "remove cmd j cml slide": the herdr ⌘J / ⌘L lesson slide is cut (the lesson stays on the site)
out = [x for x in out if "lesson-herdr-cmdj.png" not in x]
# Nat, 6 Nov: "remove talk.html#38": the "สอน 4 · ของจริงหนึ่งรอบ" slide is cut
out = [x for x in out if "สอน 4 · ของจริงหนึ่งรอบ" not in x]
# Nat, 6 Nov: "remove #42 … #39 put to same the like last section" + "remove #40": the relic5 search slides (สอน 5, relic5 ใช้จริง 1)
# and "สอน 6 · เก็บที่ใช้จริง" leave the Memory part and join the last section, after the Neo memory map, before the closing slide
# "relic5 ใช้จริง 2" too (Nat, 6 Nov: "move it to the end too")
# Nat, 6 Nov: "move #38 #39 #40": "ความจำค้นได้ยังไง" leads the moved relic5 slides, "รวมกัน · Oracle คืออะไร" follows them
_mv = [next(x for x in out if k in x) for k in ("ความจำค้นได้ยังไง", "สอน 5 · ค้นย้อนหลัง", "relic5 ใช้จริง 1", "relic5 ใช้จริง 2", "สอน 6 · เก็บที่ใช้จริง", "รวมกัน · Oracle คืออะไร")]
out = [x for x in out if x not in _mv]
_end = next(i for i, x in enumerate(out) if "ที่ให้คนมาเจอกันตัวจริง" in x)
out[_end:_end] = _mv
# Nat, 6 Nov: "remove talk.html#45": the "รายงาน /rrr ที่ claude.ai เขียนเอง" screenshot slide is cut
out = [x for x in out if "รายงาน /rrr ที่ claude.ai เขียนเอง" not in x]
# Nat, 6 Nov: "bring out put last of #58 #59 #61 #62": "อยากให้ AI เป็นแบบนี้", the lessons shot, the quote and the
# certificate QR become the very end of the talk, in that order; "#62 less ai text thai": the QR slide's words are plainer
_last = [next(x for x in out if "ภูมิใจที่เป็น AI" in x and "ผมอยากให้" in x), next(x for x in out if "new-lessons.png" in x),
         next(x for x in out if "บางวันเราเป็นผู้บริหาร" in x), next(x for x in out if "cert-qr.svg" in x)]
out = [x for x in out if x not in _last] + _last
out[-4] = out[-4].replace("<section", "<!--g:end--><section", 1)
out[-1] = (out[-1].replace('<h2>ลบแชตได้<br><span class="hl">ไฟล์ยังอยู่</span></h2>', '<h2>สแกนรับ<br><span class="hl">ใบประกาศ</span></h2>')
                  .replace('สแกนก่อนออกจากห้อง → ชื่อของคุณขึ้น <span class="nw">e-Certificate</span>',
                           'สแกนก่อนออกจากห้องนะครับ แล้วชื่อคุณจะอยู่ใน <span class="nw">e-Certificate</span>'))
assert "สแกนรับ" in out[-1] and "ห้องนะครับ" in out[-1]

# Nat, 6 Nov: "this have animation can you bring exactly this in? productize.life/workshop/ai-expo-arra/slides/#1":
# คุณยิ้ม's live 3D deck (copied to yim-live/, trackers removed, runs offline) plays behind her 9 slides. Each talk slide
# keeps its still as a fallback and says which of her slides to show (data-yim); the talk sends {yimGo:n} to the frame.
def _yim(x):
    m = re.search(r'img/yim3d-0(\d)\.png', x)
    if not m: return x
    x = re.sub(r'<a class="live3d".*?</a>', '', x, flags=re.S)
    return x.replace('<section class="slide yim3d">', f'<section class="slide yim3d" data-yim="{int(m.group(1)) - 1}">', 1)
out = [_yim(x) for x in out]
YIM_LIVE = ('<iframe id="yimlive" src="yim-live/index.html#1" title="คุณยิ้ม · 3D" tabindex="-1" '
            'style="position:absolute;left:0;top:0;width:1920px;height:1080px;border:0;z-index:5;pointer-events:none;visibility:hidden"></iframe>\n')
YIM_JS = ('<script>/* drive คุณยิ้ม\'s live deck from the talk (6 Nov) */\n'
          '(function(){const f=document.getElementById("yimlive");if(!f)return;let last=-1;\n'
          'function sync(){const on=document.querySelector(".slide.on");const k=on&&on.dataset.yim;\n'
          ' if(k==null){f.style.visibility="hidden";last=-1;return}\n'
          ' f.style.visibility="visible";if(+k!==last){last=+k;try{f.contentWindow.postMessage({yimGo:+k},"*")}catch(e){}}}\n'
          'new MutationObserver(sync).observe(document.getElementById("stage"),{subtree:true,attributes:true,attributeFilter:["class"]});\n'
          'f.addEventListener("load",()=>{last=-1;sync()});sync()})();\n</script>')
js = re.search(r"<script>\nconst S=.*?</script>", (here / "ai-drama.html").read_text(encoding="utf-8"), re.S).group(0)  # same keys + video play/pause
page = (head.replace("<title>", "<title>Talk 6 Nov · ").rstrip() + "\n" + CSS + "\n" + DRAMA_CSS + "\n</head>\n<body>\n<div id=\"stage\">\n\n"
        + "\n\n".join(out) + "\n\n" + YIM_LIVE + "</div>\n<div id=\"count\"></div>\n" + js + "\n" + YIM_JS + "\n</body>\n</html>\n")
(here / "talk.html").write_text(page, encoding="utf-8")
print(f"talk.html: {len(out)} slides, {sum('data-video' in s for s in out)} videos")

# Nat, 5 Nov: "slide too much can we sepeate to each group and we have index link to let me click like list":
# the same slides split into groups (one small deck each, talk-NN-slug.html) and talk_index.html, a clickable list
# of every group and every slide (published as /talk/index.html). talk.html stays the whole talk.
import html as _h
GROUPS = [  # (first-slide marker, slug, Thai title), in talk order
    (None, "yim", "คุณยิ้ม · เปิดงาน"),
    ("new-ws1.png", "mcp", "ลงมือ · ต่อ MCP ของบทเรียน"),
    ("oracle-family.mp4", "family", "คลิปของแม่ · ครอบครัว Oracle · ทีม"),
    ("สอน 1 · Skill", "skills", "Skill · คืออะไร · ข้างใน"),
    ("สอน 2 · Memory", "memory", "Memory · ความจำ"),
    ('หน้าตา <span class="hl">ψ/', "what", "ภาพรวม ψ/ · logs → resonance"),   # "Oracle คืออะไร" moved to the end (6 Nov)
    ("เริ่มง่ายสุด", "awaken", "กลับมาลงมือ · ลิงก์เดียวปลุก Oracle"),
    ("น่าจะครบหมดแล้ว", "phukhao", "ภูเขา · เสียงของ AI"),
    ("Multicall3", "origin", "เรื่องเล่า · ประสบการณ์ระหว่างมนุษย์และ AI (AlchemyCat)"),   # Nat, 5 Nov (his message cut at "และ อ…")
    ("เล่าจากโพสต์ Facebook", "story", "เล่าจากโพสต์ Facebook"),
    ("new-slidesai.png", "home", "ให้ AI ทำสไลด์จาก MCP"),
    ("Naming makes belief visible", "psi", "ψ · relic5 · Oracle คืออะไร · Phone Booth"),
    ("<!--g:end-->", "end", "ปิดท้าย · อยากให้ AI เป็นแบบนี้ · บทเรียน · ใบประกาศ"),   # 6 Nov: moved to the very end
]
starts = [0] + [next(i for i, x in enumerate(out) if m in x) for m, _, _ in GROUPS[1:]]
assert starts == sorted(starts), starts
bounds = list(zip(starts, starts[1:] + [len(out)]))
def _txt(f):
    return " ".join(_h.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<br\s*/?>", " ", f))).split())
def _title(x):
    body = re.sub(r'<div class="notes">.*?</div>', "", x, flags=re.S)
    # /oracle-prism + /hallmark, 5 Nov: the index showed each slide's whole text (63 of 79 lines cut off with "…");
    # a slide is named by its headline: h1/h2, else the big quote, else the caption on a picture
    for pat in (r"<h[12][^>]*>(.*?)</h[12]>", r'<div class="dq[^"]*">(.*?)</div>', r'<div class="vtag">(.*?)</div>'):
        m = re.search(pat, body, re.S)
        if m and _txt(m.group(1)):
            t = re.sub(r"\s*\([^()]*20\d\d\)$", "", _txt(m.group(1)))   # a caption's trailing "(4 พ.ย. 2026)"
            return t[:70] + ("…" if len(t) > 70 else "")
    t = _txt(body)
    if not t or t == "3D ↗":   # a picture slide: never show its speaker notes (they are stripped from the public deck)
        m = re.search(r'src="([^"]+)"', x)
        f = m.group(1).split("/")[-1].rsplit(".", 1)[0] if m else "slide"
        PIC = {"yim3d": "คุณยิ้ม · ภาพ", "new-ws1": "ลงมือ 1 · เปิดบทเรียน", "new-ws2": "ลงมือ 2 · ต่อ MCP", "new-wsrun": "ลงมือพร้อมกัน",
               "new-phukhao": "เรื่องของภูเขา · เกิด 21 ม.ค. 2026", "new-ninemonths": "เก้าเดือนต่อมา", "new-lessons": "กลับบ้านไปเรียนต่อ · บทเรียน",
               "new-slidesai": "ให้ AI ทำสไลด์จาก MCP", "02-claude-custom-connector": "ลงมือ 2 · กรอก connector ใน claude.ai"}
        t = next((v + (" " + f.split("-")[-1] if k == "yim3d" else "") for k, v in PIC.items() if f.startswith(k)), "ภาพ · " + f)
    return t[:90] + ("…" if len(t) > 90 else "")
# Nat, 5 Nov: "too much detail": the index is just the groups, one card each, click to open that part
cards = {}
for g, ((_, slug, title), (a0, a1)) in enumerate(zip(GROUPS, bounds), 1):
    cards[g] = f'<a class="c" href="talk.html#{a0 + 1}"><span class="g">{g:02d}</span><b>{_h.escape(title)}</b><small>{a1 - a0} หน้า</small></a>'
PARTS = [("A", "Opening", [1]), ("B", "Hands-on · Team · Skill · Memory", [2, 3, 4, 5, 6, 7]), ("C", "Stories", [8, 9, 10]), ("D", "Take home · Closing", [11, 12, 13])]  # Nat, 5 Nov: his order
assert sorted(g for _, _, gs in PARTS for g in gs) == list(range(1, len(GROUPS) + 1))
# Nat, 5 Nov: "can you make preact?": the index is a small Preact app (htm + preact 10, vendored as one 13 KB file,
# no CDN, works offline on stage). Data = the parts and groups; ←/→/↑/↓ move between cards, Enter opens.
import json as _json
DATA = [{"part": l, "name": n, "groups": [{"n": g, "title": GROUPS[g - 1][2], "href": f"talk.html#{bounds[g - 1][0] + 1}",   # Nat, 5 Nov: one talk, the card jumps to its first page
                                           "pages": bounds[g - 1][1] - bounds[g - 1][0], "first": bounds[g - 1][0] + 1, "last": bounds[g - 1][1],
                                           "slides": [] if g == 1 else [[k + 1, _title(out[k])] for k in range(*bounds[g - 1])]} for g in gs]} for l, n, gs in PARTS]
# Nat, 5 Nov: คุณยิ้ม's part shows only its card, no list of "ภาพ 01 … 09"
# Nat, 5 Nov: "bring back the detail": each card lists its slides again (small), each one opens the full deck there
APP = """import { html, render, useState, useEffect, useRef } from './vendor/htm-preact-3.1.1.mjs';
const DATA = __DATA__, TOTAL = __TOTAL__;
const flat = DATA.flatMap(p => p.groups);
const COLOR = { A: 'var(--part-a)', B: 'var(--part-b)', C: 'var(--part-c)', D: 'var(--part-d)' };   // one colour per part (Nat, 5 Nov: "colorized")
// Nat, 5 Nov: "toggle the detail, default no detail" then "one button toggle all": the slide lists are folded
// by default; one button at the top (or the D key) shows or hides every list
function Card({ g, on, refCb, all }) {
  const show = all && g.slides.length;
  return html`<div class="cell"><a class=${'c' + (on ? ' on' : '')} href=${g.href} ref=${refCb}>
    <span class="g">หน้า ${g.first}–${g.last}</span><b>${g.title.split(' · ').map((w, i) => html`${i ? ' · ' : ''}<span class=${w.length > 22 ? '' : 'nw'}>${w}</span>`)}</b><small>${g.pages} หน้า</small></a>
    ${show ? html`<ol class="sl">${g.slides.map(([n, t]) => html`<li><a href=${'talk.html#' + n}><span>${n}</span><em>${t}</em></a></li>`)}</ol>` : ''}</div>`;
}
function App() {
  const [sel, setSel] = useState(-1);
  const [all, setAll] = useState(true);   // Nat, 5 Nov: "expand by default now"
  const refs = useRef([]);
  useEffect(() => {
    const k = e => {
      const cols = Math.max(1, Math.round(document.querySelector('.grid').clientWidth / 300));
      const mv = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: cols, ArrowUp: -cols }[e.key];
      if (mv) { e.preventDefault(); setSel(s => Math.min(flat.length - 1, Math.max(0, (s < 0 ? 0 : s + mv)))); }
      if (e.key === 'Enter' && sel >= 0 && document.activeElement?.tagName !== 'BUTTON') location.href = flat[sel].href;
      if ((e.key === 'd' || e.key === 'D') && !e.metaKey && !e.ctrlKey) setAll(a => !a);
    };
    addEventListener('keydown', k); return () => removeEventListener('keydown', k);
  }, [sel]);
  useEffect(() => { if (sel >= 0) refs.current[sel]?.focus(); }, [sel]);
  useEffect(() => { document.querySelector('main').classList.toggle('open', all); }, [all]);   // Nat, 5 Nov: "all box same height" while folded
  let i = -1;
  return html`<a class="home" href="/">← หน้าแรก · บทเรียนทั้งหมด</a><h1>Talk 6 พ.ย. 2026</h1><p class="sub">ARRA Oracle & Multi-Agent Workflow · 15:05–16:10 · Builder Stage, AI Expo</p><div class="top"><a class="all" href="talk.html">▶ สไลด์เต็ม ${TOTAL} หน้า</a><button class="tog" aria-pressed=${all ? 'true' : 'false'} onClick=${() => setAll(!all)}>${all ? 'ซ่อนรายชื่อทั้งหมด' : 'แสดงรายชื่อทั้งหมด'}</button></div>
    ${DATA.map(p => html`<section class="part" style=${'--c:' + COLOR[p.part]}><h2><span class="p">${p.part}</span>${p.name}</h2><div class="grid">
      ${p.groups.map(g => { const k = flat.indexOf(g); return html`<${Card} g=${g} on=${k === sel} refCb=${el => (refs.current[k] = el)} all=${all} />`; })}</div></section>`)}
    <p class="hint">← → ↑ ↓ เลือก · Enter เปิด · D แสดง/ซ่อนรายชื่อ</p>`;
}
render(html`<${App} />`, document.querySelector('main'));
""".replace("__DATA__", _json.dumps(DATA, ensure_ascii=False)).replace("__TOTAL__", str(len(out)))
index = f"""<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Talk 6 Nov · ARRA Oracle &amp; Multi-Agent Workflow</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@600;700&family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap">
<style>/* Nat 5 Nov "same height, update font": cards one height (min 150 px, a row stretches), body + card titles IBM Plex Sans Thai 18 px
 * Hallmark · audit polish 5 Nov: tokens, focus ring, contrast, 320 px grid, reduced motion
 * /oracle-prism + /impeccable 5 Nov: slide = its headline (2 lines max), no side-tab or top-stripe borders, type 14/16/21/28/44
 * Nat 5 Nov "section bg color to guide": each part sits on a panel tinted with its colour */
:root{{--color-paper:oklch(15% 0.005 260);--color-card:oklch(20% 0.008 260);--color-line:oklch(28% 0.008 260);--color-ink:oklch(93% 0.01 80);
--color-muted:oklch(70% 0.012 80);--color-soft:oklch(80% 0.012 80);--part-a:oklch(78% 0.16 70);--part-b:oklch(72% 0.14 250);--part-c:oklch(78% 0.15 160);--part-d:oklch(74% 0.14 305);
--font-display:"Bai Jamjuree",sans-serif;--font-body:"IBM Plex Sans Thai",Sarabun,sans-serif;--ease-out:cubic-bezier(.2,.7,.2,1)}}
html,body{{overflow-x:clip}}body{{margin:0;background:var(--color-paper);color:var(--color-ink);font:18px/1.55 var(--font-body)}}main{{max-width:1000px;margin:0 auto;padding:40px 22px 70px}}
h1{{font:700 44px/1.15 var(--font-display);margin:0 0 6px}}.sub{{color:var(--color-muted);margin:0 0 18px}}
.all{{display:inline-block;padding:12px 22px;border-radius:999px;background:var(--color-ink);color:var(--color-paper);font-weight:700;text-decoration:none;font-size:16px;white-space:nowrap}}
h2{{font:700 28px var(--font-display);margin:0 0 14px;padding-bottom:10px;border-bottom:1px solid var(--color-line)}}h2 .p{{color:var(--c);margin-right:12px}}
.part{{margin-top:28px;padding:22px 22px 26px;border-radius:22px;background:color-mix(in oklab,var(--c) 25%,var(--color-paper));border:1px solid color-mix(in oklab,var(--c) 30%,var(--color-paper))}}.part h2{{background:var(--c);color:var(--color-paper);border:0;border-radius:12px;padding:10px 18px;margin:0 0 18px}}.part h2 .p{{color:var(--color-paper);opacity:.75}}.part .c{{background:color-mix(in oklab,var(--c) 9%,var(--color-card))}}@media (max-width:480px){{.part{{padding:16px 14px 18px;border-radius:16px}}}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(280px,100%),1fr));gap:14px;align-items:stretch}}.cell{{min-width:0;display:flex;flex-direction:column}}.c{{flex:1 0 auto;min-height:150px}}.open .grid{{align-items:start}}.open .c{{flex:none;min-height:150px}}
.c{{display:block;padding:16px 20px;border-radius:14px;background:var(--color-card);color:var(--color-ink);text-decoration:none;border:1px solid var(--color-line);transition:transform .14s var(--ease-out),border-color .14s var(--ease-out)}}
.c:hover,.c.on{{border-color:var(--c);transform:translateY(-2px)}}
.c:focus-visible,.sl a:focus-visible,.all:focus-visible{{outline:3px solid var(--color-ink);outline-offset:3px}}
.c .g{{display:block;color:var(--c);font:600 14px var(--font-body);font-variant-numeric:tabular-nums}}.c b{{display:block;font:600 22px/1.35 var(--font-body);margin:4px 0 6px;overflow-wrap:anywhere}}.c small{{color:var(--color-muted);font-size:14px}}
.sl{{list-style:none;padding:8px 4px 0;margin:0;font-size:16px;line-height:1.5}}.sl a{{display:grid;grid-template-columns:30px minmax(0,1fr);color:var(--color-soft);text-decoration:none;padding:3px 4px;border-radius:6px}}.sl a em{{font-style:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.sl a:hover{{background:var(--color-card);color:var(--color-ink)}}.sl span{{color:var(--c);font-variant-numeric:tabular-nums}}
.hint{{color:var(--color-muted);margin-top:30px;font-size:14px}}.home{{display:inline-block;margin:0 0 14px;color:var(--color-muted);text-decoration:none;font-size:16px;white-space:nowrap}}.home:hover{{color:var(--color-ink)}}.home:focus-visible{{outline:3px solid var(--color-ink);outline-offset:3px}}.nw{{white-space:nowrap}}@media (max-width:360px){{.nw{{white-space:normal}}}}.top{{display:flex;flex-wrap:wrap;gap:12px;align-items:center}}.tog{{font:600 14px var(--font-body);color:var(--color-soft);background:none;border:1px solid var(--color-line);border-radius:999px;cursor:pointer;white-space:nowrap}}.tog{{padding:11px 18px;font-size:16px}}.tog:hover{{color:var(--color-ink);border-color:var(--color-soft)}}.tog[aria-pressed=true]{{color:var(--color-ink);border-color:var(--color-ink)}}.tog:focus-visible{{outline:3px solid var(--color-ink);outline-offset:2px}}
@media (hover:none){{.hint{{display:none}}}}@media (prefers-reduced-motion:reduce){{.c{{transition:none}}.c:hover,.c.on{{transform:none}}}}</style></head><body><main><noscript><a href="talk.html">สไลด์เต็ม</a></noscript></main>
<script type="module">
{APP}</script></body></html>
"""
(here / "talk_index.html").write_text(index, encoding="utf-8")
print(f"talk_index.html: {len(GROUPS)} groups · " + " ".join(f"{a1 - a0}" for a0, a1 in bounds))
