"""Talk run-through builder: script.json -> runthrough.mp4 (slides + AI voices + burned-in Thai subtitles + the two clips).

Reuses the narrated-lesson TTS (edge-tts, one clip per subtitle line, karaoke spelling for English) from ../narrated/build.py.
Every frame (slide + subtitle + top tag) is drawn by Chromium, so Thai marks render correctly without libass.

Usage: uv run --with playwright python build.py [--check]
Outputs in out/: runthrough.mp4, runthrough.mp3, runthrough.srt, timing.md
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import base64, importlib.util, json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
PSI = HERE.parent.parent
SLIDES = PSI / "writing" / "slides"
LESSON03 = PSI / "writing" / "books" / "2026-10-30_mcp-connect-guide" / "images"
OUT = HERE / "out"; FR = OUT / "frames"; SEG = OUT / "seg"
FPS = 30
SPEAKER = {"yim": "เสียง AI (Paxa) อ่านแทนคุณยิ้ม (ซ้อม)", "nat": "เสียง AI อ่านแทนคุณนัท (ซ้อม)"}

spec = importlib.util.spec_from_file_location("narr", HERE.parent / "narrated" / "build.py")
narr = importlib.util.module_from_spec(spec); spec.loader.exec_module(narr)
sh, duration = narr.sh, narr.duration

PAXA_STYLE = "[neutral] "  # plain read, no breathy/emotional delivery (Nat, 2026-11-04)

def paxa(text, voice):
    """Paxa Flash v2, cached like edge-tts. English stays in Latin script (Paxa reads it; Thai respelling reads worse).
    The key comes from pass at call time and is never printed."""
    import hashlib, urllib.request
    text = text if text.rstrip()[-1:] in ".?!" else text + "."
    h = hashlib.sha256(f"paxa|{voice}|{PAXA_STYLE}|{text}".encode()).hexdigest()[:16]
    p = narr.HERE / ".cache" / f"paxa-{h}.mp3"
    if p.exists() and p.stat().st_size > 1000: return p
    key = subprocess.run(["pass", "show", "paxa/arkkra-voicepb"], capture_output=True, text=True, check=True).stdout.split("\n")[0]
    body = json.dumps({"model": "paxa-tts-flash-v2", "voice": voice, "text": PAXA_STYLE + text, "format": "mp3",
                       "temperature": 0.3, "speed": 1.0}).encode()
    req = urllib.request.Request("https://api.paxalabs.com/v1/tts", body, {"Authorization": f"Bearer {key}",
          "content-type": "application/json", "user-agent": "aiexpo-runthrough/1"})
    p.write_bytes(urllib.request.urlopen(req, timeout=120).read()); duration(p); return p

def tts(text, voice, tries=4):
    """edge-tts drops a request now and then (seen 2026-11-04) and can leave a broken cache file: check it, retry."""
    import hashlib, time
    h = hashlib.sha256(f"{voice}|{narr.RATE}|{text}".encode()).hexdigest()[:16]
    cached = narr.HERE / ".cache" / f"{h}.mp3"
    for n in range(tries):
        try:
            c = narr.clip(text, voice); duration(c); return c
        except subprocess.CalledProcessError:
            if cached.exists(): cached.rename(cached.with_suffix(".bad"))  # keep it, but never reuse it
            if n == tries - 1: raise
            time.sleep(2 * (n + 1))

def check(script):
    narr.load_lexicon(HERE / "script.json")
    miss = set()
    for g in script["segments"]:
        for sl in g["slides"]:
            for ln in sl.get("lines", []):
                spoken = narr.LEX_RE.sub(lambda m: narr.LEX[m.group(0).lower()], ln.get("say", ln["text"]))
                miss |= set(narr.re.findall(r"[A-Za-z][A-Za-z0-9._-]*", spoken))
    print("NO THAI SPELLING:", sorted(miss) if miss else "none"); return not miss

def b64(p): return "data:image/png;base64," + base64.b64encode(pathlib.Path(p).read_bytes()).decode()

def base_images(script, page):
    """One 1920x1080 PNG per distinct src (deck page, Yim still, lesson 03 shot, new slide)."""
    srcs = {sl["src"] for g in script["segments"] for sl in g["slides"] if "src" in sl}
    base = OUT / "base"; base.mkdir(parents=True, exist_ok=True); m = {}
    deck = sorted({int(s.split(":")[1]) for s in srcs if s.startswith("deck:")})
    for n in deck:
        sh("pdftoppm", "-png", "-f", str(n), "-l", str(n), "-scale-to-x", "1920", "-scale-to-y", "1080", "-singlefile",
           str(SLIDES / "deck.pdf"), str(base / f"deck-{n:02d}"))
        m[f"deck:{n}"] = base / f"deck-{n:02d}.png"
    page.goto((HERE / "slides.html").as_uri()); page.wait_for_load_state("networkidle")
    for s in sorted(srcs):
        kind, _, v = s.partition(":")
        if kind == "yim": m[s] = SLIDES / "img" / f"yim3d-{int(v):02d}.png"
        elif kind == "lesson03": m[s] = LESSON03 / v
        elif kind == "book": m[s] = PSI / "writing" / "books" / v   # any lesson image, e.g. book:<lesson dir>/images/<file>
        elif kind == "new":
            p = base / f"new-{v}.png"; page.locator(f'section[data-id="{v}"]').screenshot(path=str(p)); m[s] = p
    return m

FRAME = """<html><head><meta charset=utf-8><style>
*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;background:#0e0f12;overflow:hidden;font-family:Sarabun,sans-serif}
/* slide at 84% on top, subtitle band below: the caption never covers slide text (QA 2026-11-04) */
.bg{position:absolute;left:192px;top:12px;width:1536px;height:864px;object-fit:contain;border-radius:10px}
.band{position:absolute;left:0;right:0;top:880px;bottom:24px;display:flex;align-items:center;justify-content:center}
.band p{max-width:1840px;color:#fff;font-size:60px;font-weight:600;line-height:1.25;text-align:center}  /* big subtitles (Nat, 2026-11-04) */
.tag{position:absolute;left:18px;bottom:10px;color:#f2b544;font-size:20px;opacity:.85}
</style></head><body><img class=bg src="{IMG}"><div class=band>{CC}</div><div class=tag>{TAG}</div></body></html>"""

FULL = """<html><head><meta charset=utf-8><style>
*{margin:0;padding:0}body{width:1920px;height:1080px;background:#0e0f12;overflow:hidden;font-family:Sarabun,sans-serif}
.bg{position:absolute;inset:0;width:1920px;height:1080px;object-fit:contain}
.tag{position:absolute;left:14px;bottom:8px;color:#f2b544;font-size:18px;opacity:.7;background:rgba(0,0,0,.55);padding:2px 8px;border-radius:6px}
</style></head><body><img class=bg src="{IMG}"><div class=tag>{TAG}</div></body></html>"""

def frame(page, img, tag, text, path, full=False):
    """Subtitled frames: slide at 84% + caption band. full=True (a section with no subtitles, e.g. Phukhao's own slides):
    the real slide fills the whole frame, only a small label in the corner (Nat, 2026-11-04)."""
    cc = f'<p>{text}</p>' if text else ""
    tpl = FULL if full else FRAME
    page.set_content(tpl.replace("{IMG}", b64(img)).replace("{TAG}", tag).replace("{CC}", cc))
    page.wait_for_function("document.images[0].complete")
    page.screenshot(path=str(path))

def enc(args, out):
    sh("ffmpeg", "-y", "-loglevel", "error", *args, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", str(out))

def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main():
    script = json.loads((HERE / "script.json").read_text())
    if not check(script): sys.exit("fix the lexicon first")
    if "--check" in sys.argv: return
    from playwright.sync_api import sync_playwright
    for d in (FR, SEG): d.mkdir(parents=True, exist_ok=True)
    narr.load_lexicon(HERE / "script.json")
    silence = OUT / "gap.wav"
    sh("ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(narr.GAP), str(silence))
    parts, srt, timing, t0, k = [], [], [], 0.0, 0
    with sync_playwright() as p:
        b = p.chromium.launch(); page = b.new_page(viewport={"width": 1920, "height": 1080})
        base = base_images(script, page)
        for g in script["segments"]:
            voice = script["voices"][g["speaker"]]; seg_start = t0
            for sl in g["slides"]:
                k += 1; tag = f'{g["clock"]} · {g["seg"]}'
                if "video" in sl:
                    src = (HERE / sl["video"]).resolve(); out = SEG / f"{k:03d}.mp4"
                    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1"
                    enc(["-i", str(src), "-vf", vf, "-af", f"volume={sl.get('gain', '-4dB')}"], out)  # clips were ~4 dB louder than the voice (QA)
                    d = duration(out); parts.append(out)
                    srt.append((t0, t0 + 3, f'[{sl["label"]}]')); t0 += d
                    print(f"{k:03d} video {d:6.1f}s {sl['label']}"); continue
                tag2 = f'{tag} · {SPEAKER[g["speaker"]]}'
                clips, cues, t = [], [], 0.0
                for ln in sl["lines"]:
                    c = paxa(ln["text"], voice[5:]) if voice.startswith("paxa:") else tts(narr.karaoke(ln.get("say", ln["text"])), voice); d = duration(c)
                    cues.append((t, t + d, ln["text"])); clips += [c, silence]; t += d + narr.GAP
                t += 0.6  # breath before the next slide
                lst = OUT / "a.txt"; lst.write_text("".join(f"file '{c}'\n" for c in clips))
                wav = OUT / f"a{k:03d}.wav"
                sh("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-af", ("volume=4dB," if voice.startswith("paxa:") else "") + "apad", "-t", f"{t:.3f}", "-ar", "48000", "-ac", "2", str(wav))  # Paxa ran ~4 dB under Niwat
                # frames: one per cue; each cue holds until the next cue starts
                vl = OUT / "v.txt"; lines = []
                for i, (s, e, txt) in enumerate(cues):
                    f = FR / f"{k:03d}-{i:02d}.png"; frame(page, base[sl["src"]], tag2, txt, f)
                    end = cues[i + 1][0] if i + 1 < len(cues) else t
                    lines += [f"file '{f}'", f"duration {end - s:.3f}"]
                    srt.append((t0 + s, t0 + e, txt))
                lines.append(f"file '{f}'"); vl.write_text("\n".join(lines) + "\n")
                out = SEG / f"{k:03d}.mp4"
                enc(["-f", "concat", "-safe", "0", "-i", str(vl), "-i", str(wav), "-shortest"], out)
                parts.append(out); t0 += duration(out); wav.unlink()
                print(f"{k:03d} slide {t:6.1f}s {len(cues)} cues {sl['src']}")
            timing.append((g["clock"], g["seg"], seg_start, t0 - seg_start))
        b.close()
    lst = OUT / "parts.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    mp4 = OUT / "runthrough.mp4"
    # Video can be stream-copied, but copying 30 AAC segments leaves per-segment priming/edit lists that made
    # QuickTime go silent after ~39 s (Nat, 2026-11-04). So decode all audio and encode it ONCE as one track.
    sh("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
       "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", "aresample=async=1:first_pts=0",
       "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", "-movflags", "+faststart", str(mp4))
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vn", "-c:a", "libmp3lame", "-q:a", "4", str(OUT / "runthrough.mp3"))
    (OUT / "runthrough.srt").write_text("".join(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{x}\n\n" for i, (s, e, x) in enumerate(srt, 1)))
    total = duration(mp4)
    md = ["# Run-through timing", "", "| แผน | ช่วง | เริ่มในวิดีโอ | ยาว |", "|---|---|---|---|"]
    md += [f"| {c} | {n} | {int(s//60)}:{int(s%60):02d} | {d/60:.1f} นาที |" for c, n, s, d in timing]
    md += ["", f"รวม {total/60:.1f} นาที (ไม่รวมเวลาลงมือในห้อง ~25 นาที) · เสียง AI อ่านแทนผู้พูด เพื่อซ้อมเท่านั้น", "", "— AIExpo Oracle (Oracle AI)"]
    (OUT / "timing.md").write_text("\n".join(md) + "\n")
    print("\n".join(md)); print(mp4)

if __name__ == "__main__":
    main()
