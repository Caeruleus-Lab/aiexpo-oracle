#!/usr/bin/env python3
"""Print the herdr moves and pane-to-pane messages of one Claude Code session, in order.

Usage: python3 timeline.py <session.jsonl> [--since HH:MM] [--until HH:MM]
Times are converted from the transcript's UTC to Asia/Bangkok (+07).
Only lines that matter to the body move are kept: herdr-room calls, agent prompts,
pane closes, and messages that arrived from another pane ("[wCC:" / "[right" / "[left").
"""
import json, sys, re
from datetime import datetime, timedelta, timezone

BKK = timezone(timedelta(hours=7))
KEEP_CMD = re.compile(r"herdr-room (in|out)|agent prompt wCC|pane close|jq '\.members")
KEEP_MSG = re.compile(r"^\[(wCC:p\d|right|left)")

path = sys.argv[1]
since = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else "00:00"
until = sys.argv[sys.argv.index("--until") + 1] if "--until" in sys.argv else "99:99"

def when(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(BKK).strftime("%H:%M:%S")

def short(s, n=86):
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 2] + " …"

seen = set()
for line in open(path, encoding="utf-8"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    ts = d.get("timestamp")
    if not ts or not (since <= when(ts)[:5] < until):
        continue
    msg = d.get("message") or {}
    content = msg.get("content")
    if d.get("type") == "assistant" and isinstance(content, list):
        for c in content:
            if c.get("type") == "tool_use" and c.get("name") == "Bash":
                cmd = c["input"].get("command", "")
                for part in re.split(r";|&&|\n", cmd):
                    if KEEP_CMD.search(part) and "─" not in part:
                        print(f"{when(ts)}  run   {short(part.strip())}")
    if d.get("type") == "queue-operation" and isinstance(d.get("content"), str):
        content = d["content"]
    if d.get("type") in ("user", "queue-operation") and d.get("operation", "enqueue") == "enqueue":
        texts = [content] if isinstance(content, str) else [
            c.get("text", "") for c in (content or []) if isinstance(c, dict) and c.get("type") == "text"]
        for t in texts:
            for l in t.splitlines():
                if KEEP_MSG.match(l.strip()) and l.strip() not in seen:
                    seen.add(l.strip())
                    print(f"{when(ts)}  msg   {short(l.strip())}")
