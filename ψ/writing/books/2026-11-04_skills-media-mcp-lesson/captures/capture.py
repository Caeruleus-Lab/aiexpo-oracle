"""Every MCP call of lesson 09, run for real against the live server. Output: NN-slug.txt here.
Each file starts with the request (method + params) as JSON-RPC, then what came back; long answers are cut and say so.
Usage: python3 captures/capture.py        AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import json, pathlib, re, subprocess, urllib.request

C = pathlib.Path(__file__).resolve().parent
M = "https://aiexpo.buildwithoracle.com/mcp"


def rpc(method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(M, data=body, headers={"content-type": "application/json", "User-Agent": "aiexpo-capture/1.0"})
    return json.load(urllib.request.urlopen(req, timeout=60))["result"]


def save(nn, slug, method, params, lines):
    head = f"$ curl -s -X POST {M} -H 'content-type: application/json' \\\n    -d '{json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}, ensure_ascii=False)}'"
    (C / f"{nn}-{slug}.txt").write_text(head + "\n" + "\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(nn, slug, len(lines), "lines")


r = rpc("tools/list", {})
save("01", "tools-list", "tools/list", {}, ["# name          title"] + [f"{t['name']:<15} {t.get('title', '')}" for t in r["tools"]])

r = rpc("tools/call", {"name": "list_skills", "arguments": {}})
sk = json.loads(r["content"][0]["text"])["skills"]
save("02", "list-skills", "tools/call", {"name": "list_skills", "arguments": {}},
     [f"{s['name']:<11} {s['what']}" for s in sk] + ["", f"full:     {sk[1]['full']}", f"download: {sk[1]['download'][0]}"])

p = {"name": "get_skill", "arguments": {"name": "rrr"}}
c = rpc("tools/call", p)["content"]
res = c[1]["resource"]
files = re.findall(r"### File: `([^`]+)`", res["text"])
save("03", "get-skill-rrr", "tools/call", p,
     [f"content parts: {[x['type'] for x in c]}", "", f"[text]     {c[0]['text']}", "", f"[resource] uri:      {res['uri']}",
      f"           mimeType: {res['mimeType']}", f"           size:     {len(res['text'].encode()):,} bytes", "           files inside:"]
     + [f"             - {f}" for f in files] + ["", "... the last lines of the file (cut):", ""] + res["text"].rstrip().split("\n")[-9:])

p = {"name": "get_skill", "arguments": {"name": "recap", "source": "chat"}}
t = rpc("tools/call", p)["content"][1]["resource"]["text"].split("## Download")[0].strip()
save("04", "recap-cli-only", "tools/call", p, t.split("\n"))

# 5 Nov (Nat): /where-we-are joins the skills; unlike /recap it runs in a chat, because it reads the conversation
p = {"name": "get_skill", "arguments": {"name": "where-we-are"}}
c = rpc("tools/call", p)["content"]
res = c[1]["resource"]
files = re.findall(r"### File: `([^`]+)`", res["text"])
part1 = res["text"].split("## Part 1 · run it in this chat")[1].split("## Part 2")[0].strip().split("\n")
save("09", "get-skill-where-we-are", "tools/call", p,
     [f"[resource] uri:      {res['uri']}", f"           size:     {len(res['text'].encode()):,} bytes", "           files inside:"]
     + [f"             - {f}" for f in files] + ["", "Part 1 (run it in this chat), first lines:", ""] + part1[:22])

r = rpc("tools/call", {"name": "list_media", "arguments": {}})
d = json.loads(r["content"][0]["text"])
items = d.get("media", d.get("items", []))
save("05", "list-media", "tools/call", {"name": "list_media", "arguments": {}},
     [f"{m['kind']:<9} {m['id']:<22} {str(m.get('length', '')):>6}  {m['title'][:52]}" for m in items])

p = {"name": "get_media", "arguments": {"id": "oracle-family"}}
t = rpc("tools/call", p)["content"][0]["text"].split("\n")
save("06", "get-media-family", "tools/call", p, t[:16] + ["... (cut)"])

r = rpc("resources/list", {})
save("07", "resources-list", "resources/list", {}, [f"{x['name']:<14} {x['mimeType']}  {x['uri']}" for x in r["resources"]])

h = subprocess.run(["curl", "-sI", "https://aiexpo.buildwithoracle.com/oracle/full/forward.md"], capture_output=True, text=True).stdout
(C / "08-plain-link.txt").write_text("$ curl -sI https://aiexpo.buildwithoracle.com/oracle/full/forward.md   (no MCP needed)\n"
    + "\n".join(l for l in h.splitlines() if re.match(r"(?i)(HTTP|content-type|content-length)", l)) + "\n", encoding="utf-8")
print("08 plain-link")
