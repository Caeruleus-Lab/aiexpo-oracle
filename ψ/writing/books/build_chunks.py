"""Build chunks.json: every lesson split into sections (Thai and English separately), tagged, with a prebuilt vector.

The MCP Worker (worker.js) searches these chunks: keyword match plus cosine against the query's vector.
Both sides use the SAME model, Workers AI @cf/baai/bge-m3 (multilingual, Thai OK, 1024 dims):
the chunks here at build time, the query in the Worker at request time.

A chunk is re-embedded only when its text hash changes, so rebuilding is cheap.
Needs the wrangler login on this machine (its OAuth token calls the Workers AI REST API); the token is never printed.

It also writes images.json: every screenshot a chunk shows, resized to at most 1280 px wide, JPEG quality 80,
as base64 keyed by '<lesson>/<file>', so the Worker can return MCP image content blocks. Re-encoded only when the file changes.

Usage: uv run --with pillow python build_chunks.py   (after build_index.py; then commit and ./deploy.sh)
"""
import base64
import hashlib
import io
import json
import os
import pathlib
import re
import subprocess
import tomllib
import urllib.request

here = pathlib.Path(__file__).resolve().parent
SITE = "https://aiexpo.buildwithoracle.com"
ACCOUNT = "a5eabdc2b11aae9bd5af46bd6a88179e"
MODEL = "@cf/baai/bge-m3"
LANGS = {"en": ("README.en.md", "en"), "th": ("README.md", "th")}

# topic and audience tags: a rule matches when any of its words is in the section title or text (lowercased)
TOPICS = {
    "install": ["install", "ติดตั้ง", "download", "ดาวน์โหลด", "dmg", "install.sh", "brew", "winget"],
    "account": ["account", "บัญชี", "login", "ล็อกอิน", "sign in", "pro ", "free", "ฟรี", "plan", "แผน"],
    "skill": ["skill", "สกิล", "plugin", "skill.md", "/awaken", "awaken"],
    "browser": ["browser", "เบราว์เซอร์", "ego-browser", "ego(lite)", "chromium", "space"],
    "memory": ["memory", "ความจำ", "ψ/", "/rrr", "/recap", "sandbox"],
    "web": ["claude.ai", "chatgpt.com", "บนเว็บ", "on the web", "web "],
    "verify": ["signature", "ลายเซ็น", "sha256", "codesign", "spctl", "notarized", "verify", "ตรวจ"],
    "troubleshooting": ["trap", "กับดัก", "troubleshoot", "แก้ปัญหา", "error", "not found", "ไม่ขึ้น", "symptom", "อาการ"],
}
AUDIENCE = {
    "attendee": ["workshop", "install", "ติดตั้ง", "download", "ดาวน์โหลด"],
    "agent": ["agent", "llms.txt", "skill.md", "base64", "codex exec", "claude -p"],
    "presenter": ["ในห้อง", "in the room", "on screen", "บนจอ", "fallback", "ทางสำรอง"],
}


def split(md):
    """Sections at '## ' lines OUTSIDE code fences (``` or ~~~~): a lesson that embeds a whole SKILL.md
    must not turn the skill's own '## ' headings into sections of the lesson."""
    body = md.split("\n---\n", 1)[1] if "\n---\n" in md else md
    parts, cur, fence = [], [], None
    for line in body.split("\n"):
        m = re.match(r"\s*(`{3,}|~{3,})", line)
        if m and (fence is None or m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)):
            fence = None if fence else m.group(1)
        if fence is None and line.startswith("## "):
            parts.append("\n".join(cur)); cur = []
        cur.append(line)
    parts.append("\n".join(cur))
    parts = [p.strip() for p in parts]
    return [(p.split("\n", 1)[0][3:].strip(), p) for p in parts if p.startswith("## ")]


def tags_for(rules, text):
    t = text.lower()
    return [k for k, words in rules.items() if any(w in t for w in words)]


def token():
    subprocess.run(["npx", "-y", "wrangler@4", "whoami"], capture_output=True)  # refreshes the OAuth token if it expired
    cfg = pathlib.Path(os.path.expanduser("~/Library/Preferences/.wrangler/config/default.toml"))
    return tomllib.loads(cfg.read_text())["oauth_token"]


def embed(texts, tok):
    out = []
    for i in range(0, len(texts), 16):
        req = urllib.request.Request(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/{MODEL}",
            data=json.dumps({"text": texts[i:i + 16]}).encode(),
            headers={"Authorization": "Bearer " + tok, "content-type": "application/json"})
        res = json.load(urllib.request.urlopen(req))
        if not res.get("success"):
            raise SystemExit(f"embedding failed: {res.get('errors')}")
        out += res["result"]["data"]
    return out


IMG_RE = re.compile(r"!\[([^\]]*)\]\((images/[^)\s]+)\)")
KEYLIKE = re.compile(r"AKID[0-9a-zA-Z]{32}|AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{36}|sk-[A-Za-z0-9]{32,}|xox[baprs]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}")


def build_images(lessons):
    from PIL import Image
    path = here / "images.json"
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    out, made = {}, 0
    for l in lessons:
        for f in sorted((here / l["dir"] / "images").glob("*.png")):
            raw = f.read_bytes()
            key = f'{l["key"]}/{f.name}'
            h = hashlib.sha256(b"1280/jpeg80\n" + raw).hexdigest()[:16]
            if key in old and old[key]["hash"] == h and not KEYLIKE.search(old[key]["data"]):
                out[key] = old[key]
                continue
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            if im.width > 1280:
                im = im.resize((1280, round(im.height * 1280 / im.width)), Image.LANCZOS)
            # GitHub push protection reads base64 image bytes as key-shaped strings (a Tencent "AKID…" id in
            # relic5-install/00-pipeline.png, 4 Nov 2026) and refuses the Pages push: step the quality down until none match
            for q in range(80, 70, -1):
                buf = io.BytesIO()
                im.save(buf, "JPEG", quality=q, optimize=True)
                if not KEYLIKE.search(base64.b64encode(buf.getvalue()).decode()):
                    break
            out[key] = dict(url=f'{SITE}/{l["dir"]}/images/{f.name}', mimeType="image/jpeg", width=im.width, height=im.height,
                            bytes=buf.tell(), hash=h, data=base64.b64encode(buf.getvalue()).decode())
            made += 1
    path.write_text(json.dumps(out, separators=(",", ":")) + "\n", encoding="utf-8")
    big = max(v["bytes"] for v in out.values())
    print(f"images.json: {len(out)} images, {made} encoded now, largest {big // 1024} KB, total {path.stat().st_size // 1024} KB")
    return out


def main():
    lessons = json.loads((here / "lessons.json").read_text(encoding="utf-8"))
    images = build_images(lessons)
    old_path = here / "chunks.json"
    old = {c["hash"]: c["vec"] for c in json.loads(old_path.read_text(encoding="utf-8"))["chunks"]} if old_path.exists() else {}
    chunks = []
    for l in lessons:
        for lang, (file, page) in LANGS.items():
            for n, (title, text) in enumerate(split((here / l["dir"] / file).read_text(encoding="utf-8")), 1):
                head = l["th"] if lang == "th" else l["en"]
                embed_text = f"{head}\n{title}\n\n{text}"[:6000]
                chunks.append(dict(
                    id=f'{l["key"]}/{lang}/{n}', lesson=l["key"], lang=lang, section=n, title=title,
                    label=f"{head} · {title}", url=f'{SITE}/{l["dir"]}/{page}#s{n + 1}',  # page builder: cover s1, first ## s2
                    tags=dict(lesson=l["key"], lang=lang, section=n,
                              topic=tags_for(TOPICS, title + "\n" + text), audience=tags_for(AUDIENCE, title + "\n" + text) or ["attendee"]),
                    images=[dict(key=f'{l["key"]}/{p.split("/")[-1]}', alt=a) for a, p in IMG_RE.findall(text) if f'{l["key"]}/{p.split("/")[-1]}' in images],
                    text=text, hash=hashlib.sha256((MODEL + "\n" + embed_text).encode()).hexdigest()[:16], _embed=embed_text))
    todo = [c for c in chunks if c["hash"] not in old]
    if todo:
        vecs = embed([c["_embed"] for c in todo], token())
        for c, v in zip(todo, vecs):
            old[c["hash"]] = [round(x, 5) for x in v]
    for c in chunks:
        c["vec"] = old[c["hash"]]
        del c["_embed"]
    out = dict(model=MODEL, dims=len(chunks[0]["vec"]), count=len(chunks), chunks=chunks)
    old_path.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"chunks.json: {len(chunks)} chunks, {out['dims']} dims, {len(todo)} embedded now, {len(chunks) - len(todo)} reused")


main()
