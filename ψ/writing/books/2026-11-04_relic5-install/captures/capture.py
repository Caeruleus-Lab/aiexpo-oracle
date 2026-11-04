"""Every command of lesson 11, run for real on m5 (macOS, arm64) against the relic5 hub on white, 4 Nov 2026.
Each file: the command as typed, then what it printed. Long output is cut and says so.
Usage: python3 captures/capture.py [NN ...]        AIExpo Oracle (Oracle AI), 2026-11-04."""
import json, pathlib, subprocess, sys

C = pathlib.Path(__file__).resolve().parent
R5 = "/opt/Code/github.com/Soul-Brews-Studio/relic5"
HUB = "http://white.follow-rankine.ts.net:8795"
TRY = "/tmp/relic5-try"

def run(cmd, cwd=None, cut=40):
    p = subprocess.run(["zsh", "-c", cmd], cwd=cwd, capture_output=True, text=True, timeout=900)
    out = (p.stdout + p.stderr).rstrip().split("\n")
    if len(out) > cut: out = out[:cut] + [f"... ({len(out) - cut} more lines cut)"]
    return out, p.returncode

def save(nn, slug, shown, lines, rc=None):
    tail = [] if rc in (None, 0) else [f"(exit {rc})"]
    (C / f"{nn}-{slug}.txt").write_text("\n".join([f"$ {shown}"] + lines + tail).rstrip() + "\n", encoding="utf-8")
    print(nn, slug, len(lines), "lines", "rc", rc)

def step(nn, slug, cmd, cwd=None, shown=None, cut=40):
    if only and nn not in only: return
    out, rc = run(cmd, cwd, cut); save(nn, slug, shown or cmd, out, rc)

only = sys.argv[1:]
step("01", "clone", f"rm -rf {TRY} && git clone -q -b alpha https://github.com/Soul-Brews-Studio/relic5 {TRY} && cd {TRY} && git log --oneline -1 && ls",
     shown="git clone -b alpha https://github.com/Soul-Brews-Studio/relic5 && cd relic5 && git log --oneline -1 && ls")
step("02", "uv-sync", "uv sync --no-dev 2>&1 | tail -4 && .venv/bin/relic5 --version", cwd=TRY,
     shown="uv sync --no-dev && .venv/bin/relic5 --version")
step("03", "versions", "relic5 --version; file -b ~/.local/bin/relic5 | cut -c1-60; relic-scan --version; relic-extract --version; uname -sm",
     shown="relic5 --version; file -b ~/.local/bin/relic5; relic-scan --version; relic-extract --version; uname -sm")
step("04", "health", f"curl -s {HUB}/health; echo; curl -s -o /dev/null -w '%{{http_code}}\\n' https://relic5-mcp.buildwithoracle.com/mcp",
     shown=f"curl -s {HUB}/health          # on the tailnet: no token\n$ curl -s -o /dev/null -w '%{{http_code}}' https://relic5-mcp.buildwithoracle.com/mcp   # outside: token or OAuth")
step("05", "mcp-tools", f"""curl -s -X POST {HUB}/mcp -H 'content-type: application/json' -d '{{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{{}}}}' | python3 -c "import json,sys; [print(t['name']) for t in json.load(sys.stdin)['result']['tools']]" """,
     shown=f"curl -s -X POST {HUB}/mcp -H 'content-type: application/json' \\\n    -d '{{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/list\",\"params\":{{}}}}'   # tool names only", cut=60)
step("06", "claude-mcp", "claude mcp get relic5 2>&1 | head -8", shown="claude mcp get relic5")
step("07", "pending", "relic5 pending", cut=30)
step("08", "push-dry-run", f"{R5}/bin/relic5-push -n 2>&1 | tail -14", shown="bin/relic5-push -n      # dry run: what would move, nothing is sent")
