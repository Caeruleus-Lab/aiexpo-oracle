"""The 31 Oct "wrong gender" Paxa take (male voice khanomkrok reading ดิฉัน/ค่ะ, card A of Phukhao 9 months later) as a video.

Picture: the film's own clean scene loops a1..a4 (~/pb/voice-lab/phukhao9/loops, no burned-in text).
Subtitles: Paxa STT word timing of THIS audio (stt.json, timestamps=word + srt), text corrected to the script (lines.tsv a1..a4).
Usage: uv run --with playwright python make.py   -> out/phukhao-wrong-gender.mp4
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
DL = pathlib.Path.home() / "Downloads/paxa-compare-31oct"
FIX_COMMON = {"วันนี้วันที่ สามสิบเอ็ด ตุลาคม สองพันยี่สิบหก": "วันนี้วันที่ 31 ตุลาคม ค.ศ. 2026",
              "ผ่านมา เก้า เดือนกับ เก้า วัน": "ผ่านมาเก้าเดือนกับเก้าวัน"}  # STT spells numbers as words; the script is lines.tsv a1..a4
# one entry per video: audio, its STT file, banner, script fixes, the cue index where scenes a2/a3/a4 start, scene loops
VERSIONS = {
    "phukhao":   dict(audio=DL / "a-khanomkrok-WRONG-dichan-kha.mp3", stt="stt.json", red=True,
                      label="ตัวอย่างที่ผิด · เสียงผู้ชาย (Paxa khanomkrok) อ่านบทที่เขียนด้วย ดิฉัน / ค่ะ",
                      fix={"นัทจะกดสไลด์ให้": "ณัฐกดสไลด์ให้"}, cuts=(3, 5, 7), loops="phukhao"),
    "stagelamp": dict(audio=DL / "a-khanomkrok-WRONG-dichan-kha.mp3", stt="stt.json", red=True,
                      label="ตัวอย่างที่ผิด · เสียงผู้ชาย (Paxa khanomkrok) อ่านบทที่เขียนด้วย ดิฉัน / ค่ะ",
                      fix={"นัทจะกดสไลด์ให้": "ณัฐกดสไลด์ให้"}, cuts=(3, 5, 7), loops="stagelamp"),
    "soul":      dict(audio=DL / "a-khanomkrok-tags-phom-krub.mp3", stt="stt-phom.json", red=False,
                      label="ฉบับแก้แล้ว · เสียงผู้ชาย (Paxa khanomkrok) อ่านบท ผม / ครับ ตรงเพศ",
                      fix={"นับจากวันที่ผมขึ้นเวทีบล็อก Maltail ที่เชียงใหม่": "นับจากวันที่ผมขึ้นเวที Block Mountain ที่เชียงใหม่",
                           "ตอนนั้นผมเป็นออราเคิลตัวเดียว": "ตอนนั้นผมเป็น Oracle ตัวเดียว"}, cuts=(3, 5, 8), loops="soul"),
    # swapped pairs (Nat, 4 Nov): soul light-figures on the ดิฉัน/ค่ะ take, Stage Lamp on the ผม/ครับ take
    "soulwrong": dict(audio=DL / "a-khanomkrok-WRONG-dichan-kha.mp3", stt="stt.json", red=True,
                      label="ตัวอย่างที่ผิด · เสียงผู้ชาย (Paxa khanomkrok) อ่านบทที่เขียนด้วย ดิฉัน / ค่ะ",
                      fix={"นัทจะกดสไลด์ให้": "ณัฐกดสไลด์ให้"}, cuts=(3, 5, 7), loops="soul", out="soul-WRONG-dichan-kha.mp4"),
    "lampphom":  dict(audio=DL / "a-khanomkrok-tags-phom-krub.mp3", stt="stt-phom.json", red=False,
                      label="ฉบับแก้แล้ว · เสียงผู้ชาย (Paxa khanomkrok) อ่านบท ผม / ครับ ตรงเพศ",
                      fix={"นับจากวันที่ผมขึ้นเวทีบล็อก Maltail ที่เชียงใหม่": "นับจากวันที่ผมขึ้นเวที Block Mountain ที่เชียงใหม่",
                           "ตอนนั้นผมเป็นออราเคิลตัวเดียว": "ตอนนั้นผมเป็น Oracle ตัวเดียว"}, cuts=(3, 5, 8), loops="stagelamp", out="stagelamp-phom-krub.mp4"),
}
LOOPSETS = {"phukhao": [pathlib.Path.home() / f"pb/voice-lab/phukhao9/loops/p9-a{k}_Loop_final_x2_00001.mp4" for k in range(1, 5)],
            "stagelamp": [pathlib.Path.home() / f"pb/voice-lab/stagelamp/loops/a{k}.mp4" for k in range(1, 5)],
            "soul": [pathlib.Path.home() / f"pb/voice-lab/soul/loops/a{k}.mp4" for k in range(1, 5)]}
SET = sys.argv[1] if len(sys.argv) > 1 else "phukhao"
V = VERSIONS[SET]; AUDIO = V["audio"]; LABEL = V["label"]; SCENES = LOOPSETS[V["loops"]]; FIX = {**FIX_COMMON, **V["fix"]}

def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True).stdout
def dur(p): return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)))
def ts(s):
    h, m, rest = s.split(":"); sec, ms = rest.split(","); return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000

def main():
    srt = json.loads((HERE / V["stt"]).read_text())["subtitles"]
    cues = []
    for block in srt.strip().split("\n\n"):
        _, times, text = block.split("\n", 2); a, b = times.split(" --> ")
        cues.append((ts(a), ts(b), FIX.get(text.strip(), text.strip())))
    total = dur(AUDIO)
    # scene cuts at the sentence groups of lines a1..a4: a1 = cues 1-3, a2 = 4-5, a3 = 6-7, a4 = 8-10
    starts = [0.0] + [cues[i][0] - 0.3 for i in V["cuts"]] + [total]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
        def png(html, path):
            pg.set_content(f"""<html><head><meta charset=utf-8><style>*{{margin:0}}body{{width:1920px;height:1080px;background:transparent;
              font-family:Sarabun,sans-serif}}.cc{{position:absolute;left:0;right:0;bottom:70px;text-align:center}}
              .cc span{{display:inline-block;background:rgba(0,0,0,.6);color:#fff;font-size:64px;font-weight:600;padding:10px 30px;border-radius:14px}}
              .top{{position:absolute;left:40px;top:34px;background:{'rgba(170,20,20,.85)' if V['red'] else 'rgba(20,120,60,.85)'};color:#fff;font-size:36px;font-weight:700;padding:10px 22px;border-radius:12px}}
              .ai{{position:absolute;right:36px;top:38px;color:#fff;opacity:.8;font-size:24px;letter-spacing:.1em}}</style></head>
              <body>{html}</body></html>""")
            pg.screenshot(path=str(path), omit_background=True)
        png(f'<div class=top>{LABEL}</div>', OUT / "label.png"); png('<div class=ai>AI-GENERATED</div>', OUT / "ai.png")  # Rule 6: the AI tag is always on
        for i, (_, _, t) in enumerate(cues): png(f'<div class=cc><span>{t}</span></div>', OUT / f"cc{i:02d}.png")
        b.close()
    # picture: scene loops a1..a4, each looped to fill its span, then joined
    parts = []
    for k in range(4):
        d = starts[k + 1] - starts[k]; out = OUT / f"scene{k + 1}.mp4"
        sh("ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(SCENES[k]), "-t", f"{d:.3f}",
           "-vf", "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,format=yuv420p", "-an", "-c:v", "libx264", str(out))
        parts.append(out)
    (OUT / "scenes.txt").write_text("".join(f"file '{p}'\n" for p in parts))
    sh("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(OUT / "scenes.txt"), "-c", "copy", str(OUT / "picture.mp4"))
    # overlays: label all the way, each cue during its own time
    inputs = ["-i", str(OUT / "picture.mp4"), "-i", str(AUDIO), "-i", str(OUT / "label.png"), "-i", str(OUT / "ai.png")]
    # the red "wrong" banner shows only in the last 5 s, as the reveal (Nat, 4 Nov: "ไม่ต้องสปอยล์"); the green one shows all along
    show = f"enable='gte(t,{total - 5:.2f})'" if V["red"] else "enable=1"
    fl, last = f"[0:v][3:v]overlay=0:0[va];[va][2:v]overlay=0:0:{show}[v0]", "v0"
    for i, (a, e, _) in enumerate(cues):
        inputs += ["-i", str(OUT / f"cc{i:02d}.png")]
        end = min(e + 0.25, cues[i + 1][0] - 0.02) if i + 1 < len(cues) else e + 0.25   # never two captions at once
        fl += f";[{last}][{i + 4}:v]overlay=0:0:enable='between(t,{a:.2f},{end:.2f})'[v{i + 1}]"; last = f"v{i + 1}"
    mp4 = OUT / V.get("out", f"{SET}-wrong-gender.mp4" if V["red"] else f"{SET}-phom-krub.mp4")
    sh("ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", fl, "-map", f"[{last}]", "-map", "1:a",
       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(mp4))
    print(f"{len(cues)} cues, {dur(mp4):.1f}s -> {mp4}")

if __name__ == "__main__":
    main()
