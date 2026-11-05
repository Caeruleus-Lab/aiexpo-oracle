#!/usr/bin/env python3
"""Count skill use per month from Claude Code transcripts (read-only).

stdin: JSONL lines pre-filtered by rg (lines holding <command-name> or a Skill tool call).
Two kinds are counted apart:
  typed  - a human typed /name (user message carrying <command-name>/name</command-name>)
  model  - the agent called the Skill tool itself
Each message uuid is counted once (resumed sessions repeat lines across files).
Output: ψ/lab/skill-usage/usage.json + a short table on stdout.
"""
import json, re, sys, collections, pathlib

CMD = re.compile(r"<command-name>/?([A-Za-z0-9:_.-]+)</command-name>")
BUILTIN = {"clear", "compact", "exit", "model", "login", "logout", "config", "help", "resume",
           "mcp", "status", "cost", "init", "memory", "permissions", "plugin", "plugins",
           "context", "usage", "doctor", "hooks", "agents", "ide", "fast", "add-dir",
           "rewind", "export", "vim", "terminal-setup", "theme", "upgrade", "bug", "feedback",
           "release-notes", "statusline", "output-style", "privacy-settings", "todos", "bashes",
           "install-github-app", "pr-comments", "review", "migrate-installer", "effort", "btw",
           "copy", "tasks", "workflows", "sandbox", "skills", "remote-control", "rename", "branch"}

seen = set()
typed = collections.defaultdict(collections.Counter)
model = collections.defaultdict(collections.Counter)
first = {}

for line in sys.stdin:
    try:
        d = json.loads(line)
    except Exception:
        continue
    uid = d.get("uuid")
    if not uid or uid in seen:
        continue
    seen.add(uid)
    month = (d.get("timestamp") or "")[:7]
    if len(month) != 7:
        continue
    msg = d.get("message") or {}
    content = msg.get("content")
    if d.get("type") == "user" and not d.get("isMeta"):
        text = content if isinstance(content, str) else " ".join(
            c.get("text", "") for c in content or [] if isinstance(c, dict) and c.get("type") == "text")
        m = CMD.search(text or "")
        if m and m.group(1) not in BUILTIN:
            typed[month][m.group(1)] += 1
            first.setdefault(m.group(1), month)
    elif d.get("type") == "assistant" and isinstance(content, list):
        for c in content:
            if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") == "Skill":
                s = (c.get("input") or {}).get("skill")
                if s:
                    model[month][s] += 1
                    first.setdefault(s, month)

out = pathlib.Path(__file__).with_name("usage.json")
months = sorted(set(typed) | set(model))
out.write_text(json.dumps({"typed": typed, "model": model, "first_seen": first}, ensure_ascii=False, indent=1))
tot = collections.Counter()
for mo in months:
    tot.update(typed[mo]); tot.update(model[mo])
    top = (typed[mo] + model[mo]).most_common(8)
    print(mo, " ".join(f"{k}:{v}" for k, v in top))
print("TOP", " ".join(f"{k}:{v}" for k, v in tot.most_common(25)))
print("wrote", out)
