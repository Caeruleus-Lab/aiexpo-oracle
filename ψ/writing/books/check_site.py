"""Live check of everything aiexpo.buildwithoracle.com serves: the MCP (every tool, skill, media item, resource, prompt)
and every page with every local link and image on it. Prints one line per failure and a summary; exit 1 on any failure.

Usage: python3 check_site.py [base]     (default https://aiexpo.buildwithoracle.com)
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import concurrent.futures as cf, json, re, sys, urllib.error, urllib.parse, urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://aiexpo.buildwithoracle.com").rstrip("/")
UA = {"User-Agent": "aiexpo-check/1.0", "content-type": "application/json"}
FAIL, OK = [], []


def bad(what, why): FAIL.append(f"FAIL {what}: {why}")
def good(what): OK.append(what)


def http(url, method="GET", body=None, headers=None):
    req = urllib.request.Request(url, data=body, method=method, headers={**UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.headers, (r.read() if method != "HEAD" else b"")
    except urllib.error.HTTPError as e:
        return e.code, e.headers, b""
    except Exception as e:  # noqa: BLE001 - report every network error as a failure line
        return 0, {}, str(e).encode()


def rpc(method, params=None, n=[0]):
    n[0] += 1
    st, _, b = http(BASE + "/mcp", "POST", json.dumps({"jsonrpc": "2.0", "id": n[0], "method": method, "params": params or {}}).encode())
    if st != 200: return None, f"HTTP {st}"
    d = json.loads(b)
    return (d.get("result"), None) if "result" in d else (None, d.get("error"))


def tool(name, args):
    res, err = rpc("tools/call", {"name": name, "arguments": args})
    if err or res is None: return None, err
    if res.get("isError"): return None, res["content"][0].get("text", "")[:120]
    return res["content"], None


def text_of(content):
    return "\n".join(c.get("text") or c.get("resource", {}).get("text", "") for c in content)


def check_mcp():
    res, err = rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "check", "version": "1"}})
    if err: return bad("initialize", err)
    caps = res["capabilities"]
    for c in ("tools", "prompts", "resources"):
        (good if c in caps else lambda w: bad(w, "missing"))(f"capability {c}")
    tools = [t["name"] for t in rpc("tools/list")[0]["tools"]]
    want = ["search", "fetch", "get_image", "list_lessons", "list_skills", "get_skill", "list_media", "get_media"]
    (good("tools/list 8") if sorted(tools) == sorted(want) else bad("tools/list", tools))
    # lessons
    c, e = tool("list_lessons", {})
    lessons = json.loads(text_of(c))["lessons"] if c else []
    (good(f"list_lessons {len(lessons)}") if len(lessons) == 9 else bad("list_lessons", e or len(lessons)))
    for q, lang in (("ติดตั้ง Claude Code", "th"), ("connect claude.ai to MCP", "en"), ("herdr room", None)):
        c, e = tool("search", {"query": q, **({"lang": lang} if lang else {})})
        hits = re.findall(r'"id":\s*"([^"]+)"', text_of(c)) if c else []
        if not hits: bad(f"search '{q}'", e or "no hits"); continue
        good(f"search '{q}' {len(hits)}")
        c, e = tool("fetch", {"id": hits[0]})
        if not c: bad(f"fetch {hits[0]}", e); continue
        good(f"fetch {hits[0]}")
    for l in lessons:  # every lesson can be fetched whole, and its first image handed over
        lid = l.get("id")
        c, e = tool("fetch", {"id": f"{lid}/th"})
        if not c: bad(f"fetch {lid}/th", e); continue
        imgs = re.findall(r"image id[^\n]*?'([^']+\.png)'|\b([\w.-]+\.png)\b", text_of(c))
        img = next((a or b for a, b in imgs), None)
        good(f"fetch {lid}/th")
        if img:
            img = f"{lid}/{img}"   # image ids are <lesson>/<file>.png
            c, e = tool("get_image", {"id": img})
            (good(f"get_image {img}") if c and any(x["type"] == "image" for x in c) else bad(f"get_image {img}", e or "no image part"))
    # skills: tool, resource and prompt for each; full must carry every file and the download links
    c, e = tool("list_skills", {})
    skills = json.loads(text_of(c))["skills"] if c else []
    names = [s["name"] for s in skills]
    (good(f"list_skills {names}") if len(names) == 6 and "forward" in names else bad("list_skills", e or names))
    for s in skills:
        for src in ("full", "chat") + (("github",) if s.get("github") else ()):
            c, e = tool("get_skill", {"name": s["name"], "source": src})
            if not c: bad(f"get_skill {s['name']} {src}", e); continue
            r = next((x["resource"] for x in c if x["type"] == "resource"), None)
            if not r or r.get("mimeType") != "text/markdown": bad(f"get_skill {s['name']} {src}", "no text/markdown resource"); continue
            t = r["text"]
            if src == "full" and ("### File: `skills/" not in t or ".zip" not in t): bad(f"get_skill {s['name']} full", "missing skill files or zip links"); continue
            good(f"get_skill {s['name']} {src} {len(t)}B")
        for z in s.get("download", []):
            st, _, _ = http(z, "HEAD")
            (good(f"zip {z.rsplit('/', 1)[1]}") if st == 200 else bad(f"zip {z}", st))
    rl, e = rpc("resources/list")
    rs = rl["resources"] if rl else []
    (good(f"resources/list {len(rs)}") if len(rs) == 6 else bad("resources/list", e or len(rs)))
    for r in rs:
        rr, e = rpc("resources/read", {"uri": r["uri"]})
        (good(f"resources/read {r['name']}") if rr and rr["contents"][0]["mimeType"] == "text/markdown" else bad(f"resources/read {r['uri']}", e))
    pl, e = rpc("prompts/list")
    for p in (pl or {}).get("prompts", []):
        pg, e = rpc("prompts/get", {"name": p["name"]})
        (good(f"prompts/get {p['name']}") if pg and pg["messages"] else bad(f"prompts/get {p['name']}", e))
    # media: every item has a timed transcript and a link that answers
    c, e = tool("list_media", {})
    items = json.loads(text_of(c)).get("media", json.loads(text_of(c)).get("items", [])) if c else []
    (good(f"list_media {len(items)}") if len(items) == 13 else bad("list_media", e or len(items)))
    for m in items:
        c, e = tool("get_media", {"id": m["id"]})
        t = text_of(c) if c else ""
        (good(f"get_media {m['id']}") if re.search(r"\[\d+:\d\d\]", t) else bad(f"get_media {m['id']}", e or "no [m:ss] lines"))
        url = m.get("url")
        if url:
            st, h, _ = http(url, "GET", headers={"Range": "bytes=0-99"}) if url.endswith(".mp4") else http(url, "HEAD")
            (good(f"media url {m['id']} {st}") if st in (200, 206) else bad(f"media url {url}", st))


def pages():
    out = [BASE + "/", BASE + "/ai.md", BASE + "/llms.txt", BASE + "/talk/talk.html", BASE + "/narrated/", BASE + "/media.json"]
    lj = json.loads(http(BASE + "/lessons.json")[2] or b"{}")
    for l in (lj if isinstance(lj, list) else lj.get("lessons", [])):
        d = l.get("dir") or l.get("path", "").strip("/")
        for f in ("", "th.html", "en.html", "llms.txt", "README.md", "README.en.md"):
            out.append(f"{BASE}/{d}/{f}")
    for k in ("claude-chatgpt", "ego-lite", "mcp-connect", "phukhao-film", "phukhao-journey", "herdr-room", "build-mcp", "agy-mcp", "skills-mcp"):
        out.append(f"{BASE}/narrated/player.html?l={k}")
    for s in ("awaken", "rrr", "forward", "recap", "workshop", "awaken-app"):
        out += [f"{BASE}/oracle/{s}.md", f"{BASE}/oracle/full/{s}.md"]
    return out


def check_pages():
    links = set()
    def one(u):
        st, h, b = http(u)
        return u, st, (h.get("content-type", "") if h else ""), b
    with cf.ThreadPoolExecutor(12) as ex:
        for u, st, ct, b in ex.map(one, pages()):
            if st != 200: bad(f"page {u}", st); continue
            good(f"page {u}")
            if "html" in ct:
                for ref in re.findall(r'(?:src|href)="([^"#]+)"', b.decode("utf-8", "replace")):
                    if ref.startswith(("mailto:", "data:", "javascript:", "tel:")) or "${" in ref: continue   # JS template, not a link
                    full = urllib.parse.urljoin(u, ref)
                    if full.startswith(BASE): links.add(full.split("#")[0])
    def head(u):
        st, _, _ = http(u, "GET", headers={"Range": "bytes=0-0"})
        return u, st
    with cf.ThreadPoolExecutor(16) as ex:
        for u, st in ex.map(head, sorted(links)):
            (good(f"link {u}") if st in (200, 206) else bad(f"link {u}", st))
    return len(links)


if __name__ == "__main__":
    check_mcp()
    n = check_pages()
    for f in FAIL: print(f)
    print(f"\n{len(OK)} ok · {len(FAIL)} failed · {n} local links on the pages · {BASE}")
    sys.exit(1 if FAIL else 0)
