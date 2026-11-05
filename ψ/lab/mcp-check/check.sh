#!/usr/bin/env bash
# Live check of the aiexpo-lessons MCP endpoint (read-only).
# Usage: ψ/lab/mcp-check/check.sh [host]
# Resolves the host via 1.1.1.1 so a stale local DNS cache does not fail the check.
set -uo pipefail
H=${1:-aiexpo.buildwithoracle.com}
U="https://$H/mcp"
IP=$(dig +short @1.1.1.1 "$H" | grep -m1 -E '^[0-9.]+$')
[ -n "$IP" ] || { echo "FAIL dns: $H does not resolve via 1.1.1.1"; exit 1; }
OUT=$(mktemp -d)
fails=0
ok()   { echo "ok   $*"; }
bad()  { echo "FAIL $*"; fails=$((fails+1)); }

rpc() {  # rpc <n> <json> -> writes $OUT/<n>.json (SSE "data:" line stripped if present)
  curl -s --max-time 30 --resolve "$H:443:$IP" \
    -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \
    "$U" -d "$2" > "$OUT/$1.raw"
  sed -n 's/^data: //p' "$OUT/$1.raw" > "$OUT/$1.json"
  [ -s "$OUT/$1.json" ] || cp "$OUT/$1.raw" "$OUT/$1.json"
}

rpc init '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"mcp-check","version":"1"}}}'
rpc list '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
rpc s_th '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search","arguments":{"query":"ติดตั้งสกิลใน claude.ai ยังไง"}}}'
rpc s_en '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"search","arguments":{"query":"how do I give my agent its own browser"}}}'

python3 - "$OUT" "$H" <<'PY' || fails=$((fails+1))
import base64, json, re, sys, pathlib, subprocess
out, host = pathlib.Path(sys.argv[1]), sys.argv[2]
fails = 0
def load(n):
    return json.loads((out / f"{n}.json").read_text())
def ok(m): print("ok  ", m)
def bad(m):
    global fails; fails += 1; print("FAIL", m)

init = load("init")["result"]
ok(f"initialize: {init['serverInfo']['name']} {init['serverInfo'].get('version')} proto {init['protocolVersion']}")
tools = [t["name"] for t in load("list")["result"]["tools"]]
ok(f"tools: {', '.join(tools)}")
for need in ("search", "fetch"):
    if need not in tools: bad(f"missing tool {need} (ChatGPT connectors need search + fetch)")

def results(n):
    txt = load(n)["result"]["content"][0]["text"]
    return json.loads(txt)["results"]
ids = []
for n in ("s_th", "s_en"):
    r = results(n)
    ok(f"search {n}: " + " | ".join(x["id"] for x in r[:3]))
    ids += [x["id"] for x in r[:2]]

# fetch top hits and look for image blocks
def call(name, args, tag):
    body = json.dumps({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                       "params": {"name": name, "arguments": args}})
    ip = subprocess.run(["dig", "+short", "@1.1.1.1", host], capture_output=True, text=True).stdout.split()[0]
    raw = subprocess.run(["curl", "-s", "--max-time", "30", "--resolve", f"{host}:443:{ip}",
                          "-H", "content-type: application/json",
                          "-H", "accept: application/json, text/event-stream",
                          f"https://{host}/mcp", "-d", body], capture_output=True).stdout
    (out / f"{tag}.raw").write_bytes(raw)
    s = raw.decode()
    m = re.search(r"^data: (.*)$", s, re.M)
    return len(raw), json.loads(m.group(1) if m else s)

img_seen = 0
for i, cid in enumerate(dict.fromkeys(ids)):
    size, resp = call("fetch", {"id": cid}, f"fetch{i}")
    blocks = resp.get("result", {}).get("content", [])
    kinds = [b["type"] for b in blocks]
    ok(f"fetch {cid}: {size/1024:.0f} KB, blocks {kinds}")
    for b in blocks:
        if b["type"] != "image": continue
        img_seen += 1
        data = base64.b64decode(b["data"])
        magic = "png" if data[:8] == b"\x89PNG\r\n\x1a\n" else "jpeg" if data[:3] == b"\xff\xd8\xff" else "?"
        want = b.get("mimeType", "")
        (ok if magic in want else bad)(f"  image {want} {len(data)/1024:.0f} KB decodes as {magic}")
        if len(data) > 300 * 1024: bad(f"  image over 300 KB")
    texts = " ".join(b.get("text", "") for b in blocks if b["type"] == "text")
    for url in re.findall(r"!\[[^\]]*\]\((https://[^)]+)\)", texts)[:3]:
        ok(f"  markdown image url {url}")
    if re.search(r"!\[[^\]]*\]\(data:", texts): bad("  data: URI inside markdown (chat UIs block these)")
    if size > 1_000_000: bad(f"  response over 1 MB")

if "get_image" in tools:
    ok("get_image present (call it with an id from fetch to test)")
print(f"image blocks seen: {img_seen}" + ("" if img_seen else "  (images not deployed yet?)"))

# secrets sweep over everything we pulled
blob = b"".join(p.read_bytes() for p in out.glob("*.raw"))
pat = rb"(private_key|PRIVATE KEY-----|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|xox[bp]-)"
hits = re.findall(pat, blob)
(bad if hits else ok)(f"secret patterns in responses: {len(hits)}")
sys.exit(1 if fails else 0)
PY
rc=$?
echo "raw responses: $OUT"
[ $rc -eq 0 ] && [ $fails -eq 0 ] && echo "RESULT pass" || { echo "RESULT fail"; exit 1; }
