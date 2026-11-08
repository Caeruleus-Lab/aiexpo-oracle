# Nat, 5 Nov: "eng ok, but balance check": one English title on every cover, set by us (not drawn by the model) so every
# card has the same face, size, position and two lines; Bai Jamjuree Bold, the site's display face
import sys, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = sorted(pathlib.Path("/System/Library/AssetsV2").glob("com_apple_MobileAsset_Font*/*/AssetData/Baijam.ttc"))[0]
def face(size):
    for i in range(16):
        f = ImageFont.truetype(str(P), size, index=i, layout_engine=ImageFont.Layout.RAQM)
        if f.getname()[1] == "Bold": return f
# v3 (Nat, 8 Nov: "the title can we use like sumarize from the content"): each cover says what the lesson gives you,
# taken from its content, not its name (v1/v2 names are in git history)
T = {"claude-chatgpt": "Install your AI,|load the skills", "ego-lite": "Your agent gets|its own browser",
     "mcp-connect": "Your chat AI|reads the lessons", "phukhao-film": "An Oracle films|its own story",
     "phukhao-journey": "From its birth|to the stage", "herdr-room": "Many agents,|one page",
     "build-mcp": "Turn lessons|into AI tools", "agy-mcp": "Google's agy|reads the lessons",
     "skills-mcp": "One MCP: skills,|voice and video", "relic5-ui": "Every session,|searchable",
     "team-charter": "Sketch a team,|watch it work", "herdr-cmd-j": "One line to the|right agents",
     "relic5-install": "Every machine's|history, one hub", "signature": "Change one word,|the seal breaks"}
# v2 (Nat, 8 Nov: "make cover easy to scan, make it different"): each landing group has its own colour world (gen2.sh)
# and a small group tag above the title in that colour; the scrim behind the title takes the picture's own dark tone
GROUP = {"skills-mcp": "start", "mcp-connect": "start", "agy-mcp": "start", "ego-lite": "start", "claude-chatgpt": "start",
         "build-mcp": "build", "signature": "build", "relic5-install": "memory", "relic5-ui": "memory",
         "team-charter": "team", "herdr-room": "team", "herdr-cmd-j": "team", "phukhao-journey": "story", "phukhao-film": "story"}
TAG = {"start": ("START · CONNECT", (110, 231, 222)), "build": ("BUILD", (178, 236, 120)), "memory": ("MEMORY", (196, 176, 255)),
       "team": ("AGENT TEAMS", (255, 150, 140)), "story": ("STORIES", (255, 200, 130))}
# Thai covers (Nat, 8 Nov: "thai cover a"): same picture, Thai summary title and Thai group tag; COVER_LANG=th
T_TH = {"claude-chatgpt": "ติดตั้ง AI|ลงสกิลให้พร้อม", "ego-lite": "ให้ agent มี|เบราว์เซอร์ของตัวเอง",
        "mcp-connect": "AI ในแชท|อ่านบทเรียนเองได้", "phukhao-film": "Oracle เล่าเรื่อง|ตัวเองเป็นหนัง",
        "phukhao-journey": "จากวันเกิด|ถึงเวที AI Expo", "herdr-room": "หลาย agent|อยู่ในหน้าเดียว",
        "build-mcp": "เปลี่ยนบทเรียน|เป็นเครื่องมือให้ AI", "agy-mcp": "agy ของ Google|อ่านบทเรียนได้",
        "skills-mcp": "สกิล เสียง วิดีโอ|ใน MCP เดียว", "relic5-ui": "ค้นได้ทุก session|จากทุกเครื่อง",
        "team-charter": "วาดทีมบนเว็บ|แล้วทีมทำงานจริง", "herdr-cmd-j": "พิมพ์บรรทัดเดียว|ถึง agent ที่ใช่",
        "relic5-install": "ประวัติทุกเครื่อง|รวมที่ฮับเดียว", "signature": "แก้คำเดียว|ลายเซ็นก็พัง"}
TAG_TH = {"start": "เริ่มต้น · ต่อ AI", "build": "สร้างเอง", "memory": "ความจำ", "team": "ทีม agent", "story": "เรื่องเล่า"}
import os
TH = os.environ.get("COVER_LANG") == "th"
if TH:
    T = T_TH
    TAG = {g: (TAG_TH[g], c) for g, (_, c) in TAG.items()}
W, H, X, Y, MAXW = 1200, 800, 64, 60, 0.56
d0 = ImageDraw.Draw(Image.new("RGB", (W, H)))
SIZE = 96   # one size for all: the largest at which the widest line of any title fits in the left half
while max(d0.textlength(l, font=face(SIZE)) for t in T.values() for l in t.split("|")) > W * MAXW: SIZE -= 2
F, LH = face(SIZE), int(SIZE * (1.32 if TH else 1.12))   # Thai needs room for vowels above and below
TF, TH = face(34), 58   # group tag: size and the space it takes above the title
def run(src_tpl, dst_dir, keys):
    for k in keys:
        im = Image.open(src_tpl.format(k)).convert("RGB").resize((W, H))
        tag, col = TAG[GROUP[k]]
        dark = tuple(int(c * 0.45) for c in im.crop((0, 0, int(W * 0.4), int(H * 0.4))).resize((1, 1), Image.Resampling.BOX).getpixel((0, 0)))
        sc = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sc).rectangle([0, 0, int(W * 0.62), Y + TH + 2 * LH + 40], fill=215)
        im = Image.composite(Image.new("RGB", (W, H), dark), im, sc.filter(ImageFilter.GaussianBlur(70)))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([X, Y, X + 10, Y + 34], radius=3, fill=col)
        d.text((X + 22, Y - 4), tag, font=TF, fill=col)
        sh = Image.new("L", (W, H), 0)   # soft shadow under the title, so a bright picture behind it never wins
        for n, line in enumerate(T[k].split("|")):
            ImageDraw.Draw(sh).text((X, Y + TH + n * LH), line, font=F, fill=200)
        im = Image.composite(Image.new("RGB", (W, H), dark), im, sh.filter(ImageFilter.GaussianBlur(14)))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([X, Y, X + 10, Y + 34], radius=3, fill=col)
        d.text((X + 22, Y - 4), tag, font=TF, fill=col)
        for n, line in enumerate(T[k].split("|")):
            d.text((X, Y + TH + n * LH), line, font=F, fill=(246, 244, 238))
        im.save(f"{dst_dir}/{k}.jpg", quality=80, optimize=True)
    print("size", SIZE, "keys", len(keys))
if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3:] or list(T))
