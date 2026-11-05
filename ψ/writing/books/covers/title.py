# Nat, 5 Nov: "eng ok, but balance check": one English title on every cover, set by us (not drawn by the model) so every
# card has the same face, size, position and two lines; Bai Jamjuree Bold, the site's display face
import sys, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont
P = sorted(pathlib.Path("/System/Library/AssetsV2").glob("com_apple_MobileAsset_Font*/*/AssetData/Baijam.ttc"))[0]
def face(size):
    for i in range(16):
        f = ImageFont.truetype(str(P), size, index=i, layout_engine=ImageFont.Layout.RAQM)
        if f.getname()[1] == "Bold": return f
T = {"claude-chatgpt": "Install|Claude & ChatGPT", "ego-lite": "A Browser|for Your Agent", "mcp-connect": "Connect the|Lessons MCP",
     "phukhao-film": "An Oracle Films|Its Own Story", "phukhao-journey": "Phukhao's|Journey", "herdr-room": "One Room,|Many Agents",
     "build-mcp": "Build Your|Own MCP", "agy-mcp": "Antigravity CLI|+ MCP", "skills-mcp": "Skills, Voice|and Video",
     "relic5-ui": "A Tour of|relic5", "team-charter": "From Picture|to Team", "herdr-cmd-j": "Cmd J|and Cmd L",
     "relic5-install": "Every Machine,|One Hub", "signature": "The Lessons'|Signature"}
W, H, X, Y, MAXW = 1200, 800, 64, 60, 0.56
d0 = ImageDraw.Draw(Image.new("RGB", (W, H)))
SIZE = 96   # one size for all: the largest at which the widest line of any title fits in the left half
while max(d0.textlength(l, font=face(SIZE)) for t in T.values() for l in t.split("|")) > W * MAXW: SIZE -= 2
F, LH = face(SIZE), int(SIZE * 1.12)
def run(src_tpl, dst_dir, keys):
    for k in keys:
        im = Image.open(src_tpl.format(k)).convert("RGB").resize((W, H))
        sc = Image.new("L", (W, H), 0)
        ImageDraw.Draw(sc).rectangle([0, 0, int(W * 0.58), Y + 2 * LH + 50], fill=140)
        im = Image.composite(Image.new("RGB", (W, H), (14, 14, 16)), im, sc.filter(ImageFilter.GaussianBlur(70)))
        d = ImageDraw.Draw(im)
        for n, line in enumerate(T[k].split("|")):
            d.text((X, Y + n * LH), line, font=F, fill=(242, 238, 230))
        im.save(f"{dst_dir}/{k}.jpg", quality=80, optimize=True)
    print("size", SIZE, "keys", len(keys))
if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3:] or list(T))
