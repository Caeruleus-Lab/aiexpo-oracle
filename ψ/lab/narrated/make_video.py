"""Narrated lesson -> one MP4 (1920x1080): the player page itself, one frame per subtitle cue, over the slide MP3s.

What you see in the video is exactly what player.html shows (slide, image, subtitle, progress), rendered by Chromium;
the sound is the same per-slide MP3s, joined, and the audio is encoded once (QuickTime silence bug with copied AAC).
Usage: uv run --with playwright python make_video.py skills-mcp     -> out/<lesson>/<lesson>.mp4 (+ .jpg poster)
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import functools, http.server, json, pathlib, subprocess, sys, threading

HERE = pathlib.Path(__file__).resolve().parent
LESSON = sys.argv[1]
OUT = HERE / "out" / LESSON
TMP = OUT / "video-frames"; TMP.mkdir(exist_ok=True)


def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True).stdout


def main():
    talk = json.loads((OUT / "talk.json").read_text(encoding="utf-8"))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(HERE)))
    srv.RequestHandlerClass.log_message = lambda *a: None
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/player.html?l={LESSON}"
    from playwright.sync_api import sync_playwright
    frames, before = [], 0.0
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto(url); pg.wait_for_function("typeof talk !== 'undefined' && talk && talk.slides")
        pg.evaluate("document.getElementById('start')?.remove(); audio.muted = true")
        for k, s in enumerate(talk["slides"]):
            pg.evaluate(f"go({k}, false)"); pg.wait_for_timeout(500)
            pg.evaluate("Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => i.onload = i.onerror = r)))")
            # one frame per stretch: before the first cue, each cue until the next one starts, to the slide's end
            marks = [(0.0, "")] if s["cues"] and s["cues"][0]["start"] > 0.05 else []
            marks += [(c["start"], c["text"]) for c in s["cues"]]
            for j, (t0, text) in enumerate(marks):
                t1 = marks[j + 1][0] if j + 1 < len(marks) else s["duration"]
                done = before + t0
                pg.evaluate("""([text, pct, clock]) => { document.getElementById('cctext').textContent = text;
                    document.getElementById('prog').firstElementChild.style.width = pct + '%';
                    document.getElementById('time').textContent = clock; document.getElementById('play').textContent = '❚❚'; }""",
                            [text, 100 * done / talk["duration"], f"{int(done // 60)}:{int(done % 60):02d} / {int(talk['duration'] // 60)}:{int(talk['duration'] % 60):02d}"])
                f = TMP / f"s{k:02d}-{j:02d}.png"; pg.screenshot(path=str(f)); frames.append((f, t1 - t0))
            before += s["duration"]
        b.close()
    srv.shutdown()
    (TMP / "frames.txt").write_text("".join(f"file '{f}'\nduration {d:.3f}\n" for f, d in frames) + f"file '{frames[-1][0]}'\n")
    (TMP / "audio.txt").write_text("".join(f"file '{OUT / s['audio']}'\n" for s in talk["slides"]))
    mp4 = OUT / f"{LESSON}.mp4"
    sh("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(TMP / "frames.txt"),
       "-f", "concat", "-safe", "0", "-i", str(TMP / "audio.txt"),
       "-vf", "fps=30,scale=1280:720,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-tune", "stillimage",
       "-af", "aresample=async=1:first_pts=0", "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "128k",
       "-shortest", "-movflags", "+faststart", str(mp4))
    sh("ffmpeg", "-y", "-loglevel", "error", "-i", str(frames[0][0]), "-vf", "scale=1280:720", "-q:v", "4", str(OUT / f"{LESSON}.jpg"))
    dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)))
    print(f"{len(frames)} frames, {dur:.1f}s (talk {talk['duration']:.1f}s), {mp4.stat().st_size / 1e6:.1f} MB -> {mp4}")


if __name__ == "__main__":
    main()
