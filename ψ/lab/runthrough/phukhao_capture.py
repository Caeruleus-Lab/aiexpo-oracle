"""Phukhao's self-playing Block Mountain presentation -> out/phukhao-presentation.mp4 (Nat, 2026-11-04: "1st phukhao should
from https://phukhao.buildwithoracle.com/presentation/").

Rebuilds what the page does, deterministically instead of screen-recording it:
  intro screen + intro.mp3 (subtitle = the page's own introCC text, in 3 pages like the page),
  then 4 beats: beat audio, Reveal slides startSlide.. spread evenly (slide j at j*dur/(slides-1), same as the page),
  then the end screen. Audio and slides come from the live site; nothing is re-voiced.
Usage: uv run --with playwright python phukhao_capture.py
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import json, pathlib, re
import build as B  # frame(), enc(), sh, duration

SITE = "https://phukhao.buildwithoracle.com"
OUT = B.OUT / "phukhao"; OUT.mkdir(parents=True, exist_ok=True)
TAG = "15:15 · ภูเขา · งานนำเสนอจริงของภูเขา Block Mountain 22 ม.ค. 2026 (เสียง AI ของภูเขา)"

def get(url, path):
    # curl, not urllib: the site's Cloudflare answers 403 to Python's default client (2026-11-04)
    if not path.exists(): B.sh("curl", "-fsSL", "-o", str(path), url)
    return path

def main():
    html = B.sh("curl", "-fsSL", SITE + "/presentation/")
    intro_cc = re.search(r'const introCC = "(.*?)";', html).group(1)
    beats = json.loads(re.search(r"const beats = (\[.*?\]);", html).group(1))
    audio = [get(SITE + "/audio/presentation/intro.mp3", OUT / "intro.mp3")]
    audio += [get(SITE + b["audio"], OUT / pathlib.Path(b["audio"]).name) for b in beats]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(SITE + "/presentation/"); pg.wait_for_load_state("networkidle")
        pg.evaluate("""() => { for (const id of ['start-screen','demo-phase','end-phase']) document.getElementById(id)?.classList.add('hidden');
            document.getElementById('presentation').classList.remove('hidden');
            document.getElementById('intro-phase').classList.remove('hidden');
            document.getElementById('controls')?.classList.add('hidden'); }""")
        # the subtitle goes INSIDE the page, in the page's own CC box, like the live presentation (Nat, 2026-11-04)
        pages, cur = [], ""
        for w in intro_cc.split(" "):
            if cur and len(cur) + 1 + len(w) > 90: pages.append(cur); cur = w
            else: cur = f"{cur} {w}".strip()
        pages.append(cur)
        for k, t in enumerate(pages):
            pg.evaluate("t => { const e = document.getElementById('intro-cc-text'); e.classList.remove('opacity-0'); e.textContent = t; e.style.fontSize = '44px'; e.style.lineHeight = '1.35'; }", t)
            pg.wait_for_timeout(400); pg.screenshot(path=str(OUT / f"intro-{k}.png"))
        pg.evaluate("""() => { document.getElementById('intro-phase').classList.add('hidden');
            document.getElementById('end-phase').classList.remove('hidden'); }""")
        pg.wait_for_timeout(800); pg.screenshot(path=str(OUT / "end.png"))
        pg.goto(SITE + "/slides/oracle-block-mountain-2026"); pg.wait_for_load_state("networkidle")
        pg.wait_for_function("window.Reveal && Reveal.isReady()")
        n = pg.evaluate("Reveal.getTotalSlides()")
        for i in range(n):
            pg.evaluate(f"Reveal.slide({i})"); pg.wait_for_timeout(700)
            pg.screenshot(path=str(OUT / f"slide-{i:02d}.png"))
        # compose frames (slide at 84% + subtitle band, same look as the run-through)
        fr = pg  # reuse the page for frame rendering
        parts = []
        d = B.duration(audio[0]); total = sum(map(len, pages)); seg = []
        for k, t in enumerate(pages):
            f = OUT / f"f-intro-{k}.png"; B.frame(fr, OUT / f"intro-{k}.png", TAG, "", f, full=True); seg.append((f, d * len(t) / total))
        parts.append((seg, audio[0]))
        for b, a in zip(beats, audio[1:]):
            d = B.duration(a); step = d / (b["slides"] - 1); seg = []
            for j in range(b["slides"] - 1):
                s = b["startSlide"] + j; f = OUT / f"f-{s:02d}.png"
                B.frame(fr, OUT / f"slide-{s:02d}.png", f'{TAG} · {b["title"]}', "", f, full=True); seg.append((f, step))
            parts.append((seg, a))
        f = OUT / "f-end.png"; B.frame(fr, OUT / "end.png", TAG, "", f, full=True); parts.append(([(f, 3.0)], None))
        br.close()
    clips = []
    for k, (seg, a) in enumerate(parts):
        vl = OUT / "v.txt"; vl.write_text("".join(f"file '{f}'\nduration {d:.3f}\n" for f, d in seg) + f"file '{seg[-1][0]}'\n")
        out = OUT / f"part-{k}.mp4"
        src = ["-i", str(a)] if a else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "3"]
        B.enc(["-f", "concat", "-safe", "0", "-i", str(vl), *src, "-shortest"], out); clips.append(out)
    lst = OUT / "parts.txt"; lst.write_text("".join(f"file '{c}'\n" for c in clips))
    mp4 = B.OUT / "phukhao-presentation.mp4"
    B.sh("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-map", "0:v", "-map", "0:a",
         "-c:v", "copy", "-af", "aresample=async=1:first_pts=0", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "160k", str(mp4))
    print(f"{n} slides, {len(beats)} beats -> {mp4} ({B.duration(mp4):.1f}s)")

if __name__ == "__main__":
    main()
