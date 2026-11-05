"""Write out/lessons.json from every out/<lesson>/talk.json, in lesson order (scripts/NN-*.json)."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
items = []
for sp in sorted((HERE / "scripts").glob("[0-9][0-9]-*.json")):
    if sp.name.endswith(".lex.json"): continue
    s = json.loads(sp.read_text()); t = HERE / "out" / s["lesson"] / "talk.json"
    if not t.exists(): continue
    talk = json.loads(t.read_text())
    items.append({"n": sp.name[:2], "lesson": s["lesson"], "title": talk["title"], "slides": len(talk["slides"]),
                  "duration": talk["duration"], "lines": sum(len(x["cues"]) for x in talk["slides"])})
(HERE / "out" / "lessons.json").write_text(json.dumps(items, ensure_ascii=False, indent=1))
print(f"lessons.json: {len(items)} lessons, {sum(i['duration'] for i in items)/60:.1f} min total")
