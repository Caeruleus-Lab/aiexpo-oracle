"""Build the Open Graph / Facebook share cards: og/index.png and og/<lesson>.png, 1200x630.

Each card is drawn with Pillow in the deck palette (tokens.css, dark): an amber lamp bar, the lesson number,
the Thai title in Bai Jamjuree, the English title, the lesson's real cover screenshot, the URL small at the
bottom. Pillow lays out Thai with libraqm, so marks stack correctly. A card is redrawn only when its inputs
change (hash kept in og/cards.json).

Drawn with Pillow since 2026-10-31 (issue #6): the earlier ego-browser render came out zoomed 2x and cropped,
whatever the viewport override said, so the cards no longer depend on a browser window.

Usage: python3 build_og.py   (after build_index.py; needs Pillow with raqm, the macOS Bai Jamjuree and Sarabun
fonts; then commit og/ and ./deploy.sh)
"""
import hashlib
import json
import pathlib

from PIL import Image, ImageDraw, ImageFont, ImageOps, features

here = pathlib.Path(__file__).resolve().parent
OG = here / "og"
SITE = "aiexpo.buildwithoracle.com"
VERSION = "pillow-1"  # bump to redraw every card after a layout change

W, H = 1200, 630
PAPER, PAPER_2, RULE = (14, 18, 23), (25, 29, 36), (56, 61, 70)
INK, INK_2, INK_3 = (243, 242, 237), (172, 177, 186), (123, 129, 137)
ACCENT, ACCENT_INK = (245, 174, 57), (32, 22, 8)

FONT_DIR = pathlib.Path("/System/Library/AssetsV2")
FACES = {}


def find_font(file_name):
    hits = sorted(FONT_DIR.glob(f"com_apple_MobileAsset_Font*/*/AssetData/{file_name}"))
    if not hits:
        raise SystemExit(f"font {file_name} not found under {FONT_DIR}: download it in Font Book (Bai Jamjuree, Sarabun)")
    return hits[0]


def font(family, style, size):
    """family 'display' = Bai Jamjuree, 'body' = Sarabun (as tokens.css); style is the face name, e.g. 'Bold'."""
    key = (family, style, size)
    if key not in FACES:
        path = find_font("Baijam.ttc" if family == "display" else "Sarabun.ttc")
        for i in range(16):
            f = ImageFont.truetype(str(path), size, index=i, layout_engine=ImageFont.Layout.RAQM)
            if f.getname()[1] == style:
                FACES[key] = f
                break
        else:
            raise SystemExit(f"no {style} face in {path.name}")
    return FACES[key]


THAI_MARKS = set("ัิีึืฺุู็่้๊๋์ํ๎")
THAI_LEADING = set("เแโใไ")  # vowels written before their consonant


def split_long(draw, word, f, width):
    """A Thai run with no space can be wider than the column: cut it between characters, never before a
    combining mark and never right after a leading vowel."""
    parts, cur = [], ""
    for ch in word:
        if cur and draw.textlength(cur + ch, font=f) > width and ch not in THAI_MARKS and cur[-1] not in THAI_LEADING:
            parts.append(cur)
            cur = ""
        cur += ch
    return parts + [cur]


def thai_words(run):
    """Thai has no spaces between words: segment a run with pythainlp when it is installed, so a line never
    breaks inside a word (ครอบครัว stays whole). Without it the run stays one piece and split_long cuts it."""
    try:
        from pythainlp.tokenize import word_tokenize
    except ImportError:
        return [run]
    return [w for w in word_tokenize(run, engine="newmm", keep_whitespace=False) if w]


def wrap(draw, text, f, width):
    """Greedy wrap: at spaces, then at Thai word boundaries; a piece still wider than the column is cut."""
    words = []  # (piece, glue): glue " " after a space, "" inside a segmented Thai run
    for w in text.split(" "):
        pieces = thai_words(w) if draw.textlength(w, font=f) > width else [w]
        for k, p in enumerate(pieces):
            for q in (split_long(draw, p, f, width) if draw.textlength(p, font=f) > width else [p]):
                words.append((q, "" if k else " "))
    lines, cur = [], ""
    for word, glue in words:
        test = (cur + glue + word).strip() if cur else word
        if draw.textlength(test, font=f) <= width or not cur:
            cur = test
        else:
            lines.append(cur)
            cur = word
    return lines + ([cur] if cur else [])


def foot(draw, left_bold, left_rest):
    f_b, f = font("body", "Bold", 22), font("body", "SemiBold", 22)
    y = H - 40 - 30
    draw.text((72, y), left_bold, font=f_b, fill=INK_2)
    draw.text((72 + draw.textlength(left_bold, font=f_b), y), left_rest, font=f, fill=INK_3)
    draw.text((W - 72 - draw.textlength(SITE, font=f), y), SITE, font=f, fill=INK_3)


def lesson_card(i, l, out):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 11, H], fill=ACCENT)  # the lamp
    text_w = W - 72 - 72 - 56 - 430
    h1, num, en = font("display", "Bold", 60), font("display", "Bold", 44), font("body", "Medium", 26)
    title = wrap(d, l["th"], h1, text_w)[:4]
    sub = wrap(d, l["en"], en, text_w)[:3]
    y = (H - (44 + 22 + len(title) * 71 + 20 + len(sub) * 35)) // 2 - 10
    d.text((72, y), f"{i:02d}", font=num, fill=ACCENT)
    y += 44 + 22
    for line in title:
        d.text((72, y), line, font=h1, fill=INK)
        y += 71
    y += 20
    for line in sub:
        d.text((72, y), line, font=en, fill=INK_2)
        y += 35
    # the cover: 430x430, object-fit cover from the top left, rounded, with a hairline border
    shot = ImageOps.fit(Image.open(here / l["dir"] / l["cover"]).convert("RGB"), (430, 430), centering=(0, 0))
    x0, y0 = W - 72 - 430, (H - 430) // 2
    mask = Image.new("L", (430, 430), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, 429, 429], radius=14, fill=255)
    d.rounded_rectangle([x0 - 1, y0 - 1, x0 + 430, y0 + 430], radius=15, fill=PAPER_2, outline=RULE)
    im.paste(shot, (x0, y0), mask)
    foot(d, "AIExpo Oracle", " · AI Expo · 6 พ.ย. 2026")
    im.save(out, optimize=True)


def index_card(lessons, out):
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 11, H], fill=ACCENT)
    h1, en = font("display", "Bold", 60), font("body", "Medium", 26)
    d.text((72, 150), "บทเรียน workshop", font=h1, fill=INK)
    d.text((72, 221), "ARRA Oracle", font=h1, fill=ACCENT)
    y = 312
    for line in wrap(d, "ARRA Oracle & Multi-Agent Workflow · AI Expo · Fri 6 Nov 2026", en, W - 72 - 56 - 520 - 72):
        d.text((72, y), line, font=en, fill=INK_2)
        y += 35
    # the list, right column 520 px: amber number discs and titles
    item, num = font("display", "SemiBold", 25), font("display", "Bold", 22)
    x0, gap = W - 72 - 520, 14
    rows = [wrap(d, l["th"], item, 520 - 64)[:2] for l in lessons]
    total = sum(max(48, len(r) * 32) for r in rows) + gap * (len(rows) - 1)
    y = (H - 60 - total) // 2
    for i, r in enumerate(rows):
        hgt = max(48, len(r) * 32)
        cy = y + hgt // 2
        d.ellipse([x0, cy - 24, x0 + 48, cy + 24], fill=ACCENT)
        label = f"{i + 1:02d}"
        d.text((x0 + 24 - d.textlength(label, font=num) / 2, cy - 15), label, font=num, fill=ACCENT_INK)
        ty = cy - len(r) * 32 // 2 - 4
        for line in r:
            d.text((x0 + 64, ty), line, font=item, fill=INK)
            ty += 32
        y += hgt + gap
    foot(d, "AIExpo Oracle", f" · {len(lessons)} บทเรียน")
    im.save(out, optimize=True)


def main():
    if not features.check("raqm"):
        raise SystemExit("this Pillow has no libraqm, so Thai marks would not stack: run it with the system python3")
    lessons = json.loads((here / "lessons.json").read_text(encoding="utf-8"))
    OG.mkdir(exist_ok=True)
    state_path = OG / "cards.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {}

    def digest(*parts):
        h = hashlib.sha256(VERSION.encode())
        for p in parts:
            h.update(p if isinstance(p, bytes) else str(p).encode())
        return h.hexdigest()[:16]

    jobs = {"index": (digest(json.dumps([l["th"] for l in lessons], ensure_ascii=False)), lambda out: index_card(lessons, out))}
    for i, l in enumerate(lessons):
        cover = (here / l["dir"] / l["cover"]).read_bytes()
        jobs[l["key"]] = (digest(i + 1, l["th"], l["en"], cover), lambda out, i=i, l=l: lesson_card(i + 1, l, out))
    drawn = 0
    for key, (h, draw) in jobs.items():
        png = OG / f"{key}.png"
        if state.get(key) != h or not png.exists():
            draw(png)
            state[key] = h
            drawn += 1
            print(f"ok   {png}")
    state_path.write_text(json.dumps(state, indent=2) + "\n")
    print(f"og cards: {len(jobs)} total, {drawn} drawn now")


main()
