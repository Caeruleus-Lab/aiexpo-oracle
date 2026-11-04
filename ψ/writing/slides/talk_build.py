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
out = []
for g in script["segments"]:
    for sl in g["slides"]:
        src = sl.get("src")
        if "video" in sl:
            name = pathlib.Path(sl["video"]).stem
            out.append(video(name, html.escape(sl["label"]), "วิดีโอเล่นเองเมื่อเข้าหน้านี้ · Space หยุด/เล่น · → ไปต่อ")); continue
        kind, _, v = src.partition(":")
        if kind == "deck":
            out.append(secs[int(v) - 1])
        elif kind == "yim":
            out.append(secs[3 + int(v)])            # deck slides 5..13 are คุณยิ้ม's stills 1..9
        elif kind == "new":
            out.append(f'<section class="slide yim3d"><img src="img/talk/new-{v}.png" alt="">{notes(sl["lines"])}</section>')
        elif kind == "lesson03":
            out.append(f'<section class="slide shot"><img src="{L03}{v}" alt="">{notes(sl["lines"])}</section>')
js = re.search(r"<script>\nconst S=.*?</script>", (here / "ai-drama.html").read_text(encoding="utf-8"), re.S).group(0)  # same keys + video play/pause
page = (head.replace("<title>", "<title>Talk 6 Nov · ").rstrip() + "\n" + CSS + "\n</head>\n<body>\n<div id=\"stage\">\n\n"
        + "\n\n".join(out) + "\n\n</div>\n<div id=\"count\"></div>\n" + js + "\n</body>\n</html>\n")
(here / "talk.html").write_text(page, encoding="utf-8")
print(f"talk.html: {len(out)} slides, {sum('data-video' in s for s in out)} videos")
