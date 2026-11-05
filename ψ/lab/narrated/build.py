"""Narrated lesson builder: script JSON -> one MP3 per slide + talk.json (slides + timed subtitle cues).

Every subtitle line is synthesized on its own (edge-tts), so each cue's start and end are measured, not guessed.
Lines are joined per slide with a short pause. Clips are cached by hash of voice + rate + spoken text.

Usage: uv run python build.py scripts/01-claude-chatgpt.json   (needs ffmpeg; edge-tts runs through uvx)
"""
import hashlib, json, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
BOOKS = HERE.parent.parent / "writing" / "books"
GAP = 0.35  # seconds of silence between lines
RATE = "+0%"

def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True).stdout

def duration(p): return float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)))

LEX, LEX_RE = {}, None

def load_lexicon(script_path=None):
    """lexicon.json (shared) + scripts/<name>.lex.json (that lesson's own words; it wins on a clash)."""
    global LEX, LEX_RE
    files = [HERE / "lexicon.json"]
    if script_path:
        own = pathlib.Path(script_path).with_suffix(".lex.json")
        if own.exists(): files.append(own)
    LEX = {}
    for f in files:
        LEX.update({k.lower(): v for k, v in json.loads(f.read_text()).items() if not k.startswith("_")})
    # whole words only (a single letter "A" must not eat the "a" of "Claude"); case-blind
    LEX_RE = re.compile(r"(?<![A-Za-z0-9.])(" + "|".join(re.escape(k) for k in sorted(LEX, key=len, reverse=True)) + r")(?![A-Za-z0-9])", re.I)

load_lexicon()

def karaoke(text):
    """Spoken form: every English word becomes Thai karaoke spelling; any Latin left over is an error."""
    out = LEX_RE.sub(lambda m: LEX[m.group(0).lower()], text)
    left = re.findall(r"[A-Za-z][A-Za-z0-9._-]*", out)
    if left: raise SystemExit(f"no Thai spelling for {sorted(set(left))} in: {text}\n  add them to lexicon.json")
    return out

def clip(text, voice):
    h = hashlib.sha256(f"{voice}|{RATE}|{text}".encode()).hexdigest()[:16]
    p = HERE / ".cache" / f"{h}.mp3"
    if not p.exists():
        p.parent.mkdir(exist_ok=True)
        sh("uvx", "edge-tts", "--voice", voice, f"--rate={RATE}", "--text", text, "--write-media", str(p))
    return p

def check(script_path):
    """No TTS: validate the script and list every English word that has no Thai spelling yet."""
    load_lexicon(script_path)
    s = json.loads(pathlib.Path(script_path).read_text()); errs, miss = [], set()
    for k in ("lesson", "dir", "title", "voice", "slides"):
        if k not in s: errs.append(f"missing key {k}")
    for n, sl in enumerate(s.get("slides", []), 1):
        if not sl.get("title") or not sl.get("lines"): errs.append(f"slide {n}: needs title and lines")
        if "image" in sl and not (BOOKS / s["dir"] / sl["image"]).exists(): errs.append(f"slide {n}: no such image {sl['image']}")
        for line in sl.get("lines", []):
            spoken = LEX_RE.sub(lambda m: LEX[m.group(0).lower()], line.get("say", line["text"]))
            miss |= set(re.findall(r"[A-Za-z][A-Za-z0-9._-]*", spoken))
            if len(line["text"]) > 140: errs.append(f"slide {n}: subtitle over 140 chars: {line['text'][:40]}...")
    lines = sum(len(sl.get("lines", [])) for sl in s.get("slides", []))
    print(f"{s.get('lesson')}: {len(s.get('slides', []))} slides, {lines} lines")
    for e in errs: print("ERROR", e)
    if miss: print("NO THAI SPELLING:", ", ".join(sorted(miss)))
    print("OK" if not errs and not miss else "FIX THE ABOVE")
    return not errs and not miss

def main(script_path):
    load_lexicon(script_path)
    s = json.loads(pathlib.Path(script_path).read_text())
    out = HERE / "out" / s["lesson"]; out.mkdir(parents=True, exist_ok=True)
    silence = HERE / ".cache" / "gap.mp3"
    if not silence.exists():
        (HERE / ".cache").mkdir(exist_ok=True)
        sh("ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), "-q:a", "9", "-acodec", "libmp3lame", str(silence))
    talk = {k: s[k] for k in ("lesson", "dir", "title", "voice")}; talk["slides"] = []; total = 0.0
    for n, sl in enumerate(s["slides"], 1):
        parts, cues, t = [], [], 0.0
        for line in sl["lines"]:
            c = clip(karaoke(line.get("say", line["text"])), s["voice"]); d = duration(c)
            cues.append({"start": round(t, 3), "end": round(t + d, 3), "text": line["text"]})
            parts += [c, silence]; t += d + GAP
        lst = out / "concat.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
        mp3 = out / f"slide-{n:02d}.mp3"
        sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(mp3)); lst.unlink()
        slide = {k: sl[k] for k in ("title", "sub", "bullets", "code") if k in sl}
        if "image" in sl:
            src = BOOKS / s["dir"] / sl["image"]; dst = out / "img" / src.name
            dst.parent.mkdir(exist_ok=True); shutil.copy2(src, dst); slide["image"] = f"img/{src.name}"
        slide.update(audio=mp3.name, duration=round(duration(mp3), 3), cues=cues)
        talk["slides"].append(slide); total += slide["duration"]
        print(f"slide {n:02d}  {slide['duration']:6.1f}s  {len(cues)} cues  {sl['title']}")
    talk["duration"] = round(total, 1)
    (out / "talk.json").write_text(json.dumps(talk, ensure_ascii=False, indent=1))
    print(f"{s['lesson']}: {len(talk['slides'])} slides, {total/60:.1f} min -> {out}/talk.json")

if __name__ == "__main__":
    if sys.argv[1] == "--check":
        sys.exit(0 if all([check(p) for p in sys.argv[2:]]) else 1)
    for p in sys.argv[1:]:
        main(p)
