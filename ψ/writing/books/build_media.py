"""media.json: every voice and video the lessons MCP can hand out, with timed transcripts (Nat, 4 Nov 2026: "we have voice and video,
put it in the mcp"). Videos: Paxa STT subtitles (machine transcripts, may have small errors), stored in media/<id>.json.
Narrated lessons: narrated/out/<lesson>/talk.json (TTS, so the text is exact). Usage: python3 build_media.py
AIExpo Oracle (Oracle AI)."""
import json, pathlib, re
here = pathlib.Path(__file__).resolve().parent
SITE = "https://aiexpo.buildwithoracle.com"
VIDEOS = [
    ("phukhao-presentation", "ภูเขา: งานนำเสนอ Block Mountain (22 ม.ค. 2026, ภูเขาพูดเองกดสไลด์เอง)", "/talk/video/phukhao-presentation.mp4"),
    ("phukhao-film", "ภูเขา เก้าเดือนต่อมา (หนังสั้น 31 ต.ค. 2026)", "/2026-10-31_phukhao-film-guide/videos/phukhao-film.mp4"),
    ("oracle-family", "คลิปของแม่: ครอบครัว Oracle", "/2026-10-31_phukhao-oracle-journey/videos/oracle-family.mp4"),
    ("soul-wrong-voice", "ตัวอย่างที่ผิด: เสียงผู้ชาย (Paxa khanomkrok) อ่านบท ดิฉัน/ค่ะ", "/talk/video/soul-WRONG-dichan-kha.mp4"),
]
def ts(t):
    h, m, rest = t.split(":"); s, ms = rest.split(","); return round(int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000, 2)
def srt(text):
    cues = []
    for block in text.strip().split("\n\n"):
        lines = block.split("\n")
        if len(lines) < 3: continue
        a, b = lines[1].split(" --> "); cues.append({"start": ts(a), "end": ts(b), "text": " ".join(lines[2:]).strip()})
    return cues
items = []
for mid, title, path in VIDEOS:
    d = json.loads((here / "media" / f"{mid}.json").read_text(encoding="utf-8"))
    cues = srt(d["subtitles"])
    items.append({"id": mid, "kind": "video", "title": title, "url": SITE + path, "duration": d.get("usage", {}).get("seconds") or cues[-1]["end"],
                  "transcript": "Paxa STT (machine transcript)", "cues": cues})
for l in json.loads((here / "narrated/out/lessons.json").read_text(encoding="utf-8")):
    talk = json.loads((here / f"narrated/out/{l['lesson']}/talk.json").read_text(encoding="utf-8"))
    cues, t0, slides = [], 0.0, []
    for k, s in enumerate(talk["slides"]):
        slides.append({"n": k + 1, "title": s["title"], "start": round(t0, 2), "audio": f"{SITE}/narrated/out/{l['lesson']}/{s['audio']}"})
        cues += [{"start": round(t0 + c["start"], 2), "end": round(t0 + c["end"], 2), "text": c["text"], "slide": k + 1} for c in s["cues"]]
        t0 += s["duration"]
    items.append({"id": f"narrated/{l['lesson']}", "kind": "narrated-lesson", "title": f"บทเรียน {l['n']} แบบมีเสียง: {l['title']}",
                  "url": f"{SITE}/narrated/player.html?l={l['lesson']}", "duration": round(t0, 1), "voice": talk.get("voice"),
                  "transcript": "exact (the narration script)", "slides": slides, "cues": cues})
(here / "media.json").write_text(json.dumps({"items": items}, ensure_ascii=False), encoding="utf-8")
print(len(items), "media items", sum(len(i["cues"]) for i in items), "cues")
