#!/usr/bin/env python3
"""Mirror one /rrr retrospective into the Notion "Retros" database.

The ψ/ file in git stays the source of truth. This script only copies it into
Notion so retros from Claude Code, claude.ai and ChatGPT sit in one table.

    rrr_notion.py <retro.md> [--metrics <session-metrics.md>] [--oracle NAME]
                  [--human NAME] [--surface "Claude Code"] [--dry-run]

What it does:
  1. Reads the retro: title, date and time (from the path), slug, session id,
     evidence source, the Oracle that signed it.
  2. Finds the matching row in session-metrics.md (same date + HH:MM, else the
     latest row of that session on that day) and takes done/stuck/win/friction/error.
  3. Upserts by Key: Key = the retro's ψ path (unique per retro; one long session
     can write several retros, so the session id alone would collide).
     Found -> `ntn pages edit` (body) ; not found -> `ntn pages create`.
  4. Sets the columns with `ntn api v1/pages/<id> -X PATCH`.
  5. Reads the page back and checks Key, Title and every `## ` heading of the body.
     Exit 1 if anything is missing.

Needs `ntn` logged in (`ntn doctor`). No token is read or printed by this script.
"""
import argparse
import json
import os
import re
import subprocess
import sys

DATA_SOURCE = os.environ.get("RETROS_DATA_SOURCE", "6b341a7a-17aa-4506-ab61-f1a9197b651f")
TEXT_LIMIT = 1900  # Notion caps one rich_text item at 2000 chars


def ntn(args, stdin=None):
    try:
        r = subprocess.run(["ntn", *args], input=stdin, capture_output=True, text=True, timeout=90)
    except subprocess.TimeoutExpired:
        sys.exit(f"ntn {' '.join(args[:3])} gave no answer in 90 s (Notion API slow or down); the ψ file is untouched")
    if r.returncode != 0:
        sys.exit(f"ntn {' '.join(args[:3])} failed (rc={r.returncode}): {r.stderr.strip()[:400]}")
    return r.stdout


def ntn_json(args, body=None):
    extra = ["-d", "@-"] if body is not None else []
    out = ntn(["api", *args, *extra], stdin=json.dumps(body) if body is not None else None)
    return json.loads(out)


def psi_path(path):
    """ψ/... part of the path, used as the Key."""
    p = os.path.abspath(path)
    i = p.find("/ψ/")
    return p[i + 1:] if i >= 0 else os.path.basename(p)


def parse_retro(path, text):
    m = re.search(r"retrospectives/(\d{4})-(\d{2})/(\d{2})/(\d{2})\.(\d{2})_([^/]+)\.md$", path)
    if not m:
        sys.exit(f"not a retro path (…/retrospectives/YYYY-MM/DD/HH.MM_slug.md): {path}")
    y, mo, d, hh, mi, slug = m.groups()
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), slug)
    title = re.sub(r"^Session Retrospective:?\s*", "", title)

    def field(name):
        f = re.search(rf"\*\*{name}\*\*:\s*(.+)", text)
        return f.group(1).strip() if f else ""

    if not title:  # plain "# Session Retrospective": use Primary Focus, cut on a word
        focus = field("Primary Focus")
        title = (focus[:90].rsplit(" ", 1)[0] + "…") if len(focus) > 90 else focus
    title = title or slug.replace("-", " ")

    session = re.match(r"[0-9a-f]{8}", field("Session"))
    ev = field("Evidence Source").lower()
    evidence = "session-clock" if "session" in ev else "git" if "git" in ev else "context-only"
    signed = re.findall(r"^—\s*(.+?)\s*\(Oracle AI\)", text, re.M)
    return {
        "date": f"{y}-{mo}-{d}",
        "time": f"{hh}:{mi}",
        "slug": slug,
        "title": title,
        "session": session.group(0) if session else "",
        "evidence": evidence,
        "oracle": signed[-1] if signed else "",
    }


def metrics_row(metrics_path, info):
    """Row of session-metrics.md for this retro: exact 'date HH:MM' first, else the
    latest row of the same session on the same day."""
    if not metrics_path or not os.path.exists(metrics_path):
        return {}
    rows = []
    for line in open(metrics_path, encoding="utf-8"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and re.match(r"\d{4}-\d{2}-\d{2}", cells[0]):
            rows.append(cells)
    when = f"{info['date']} {info['time']}"
    pick = next((r for r in rows if r[0] == when), None)
    if not pick and info["session"]:
        same = [r for r in rows if r[1] == info["session"] and r[0].startswith(info["date"])]
        pick = same[-1] if same else None
    if not pick:
        return {}
    return dict(zip(["Done", "Stuck", "Win", "Friction", "Error"], pick[2:]))


def rich(s):
    return {"rich_text": [{"type": "text", "text": {"content": s[:TEXT_LIMIT]}}]} if s else {"rich_text": []}


def find_by_key(key):
    res = ntn_json([f"v1/data_sources/{DATA_SOURCE}/query", "-X", "POST"],
                   {"filter": {"property": "Key", "rich_text": {"equals": key}}, "page_size": 5})
    pages = res.get("results", [])
    if len(pages) > 1:
        print(f"warning: {len(pages)} pages share Key {key}; updating the first", file=sys.stderr)
    return pages[0]["id"] if pages else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("retro")
    ap.add_argument("--metrics", help="session-metrics.md (default: ../../learnings/session-metrics.md next to the retro)")
    ap.add_argument("--oracle", help="default: the '— <name> (Oracle AI)' signature in the retro")
    ap.add_argument("--human", default="Nat")
    ap.add_argument("--surface", default="Claude Code", choices=["Claude Code", "claude.ai", "ChatGPT"])
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    path = os.path.abspath(a.retro)
    text = open(path, encoding="utf-8").read()
    info = parse_retro(path, text)
    key = psi_path(path)
    metrics = a.metrics or os.path.join(path.split("/retrospectives/")[0], "learnings", "session-metrics.md")
    row = metrics_row(metrics, info)
    oracle = a.oracle or info["oracle"] or "unknown"

    props = {
        "Title": {"title": [{"type": "text", "text": {"content": info["title"][:TEXT_LIMIT]}}]},
        "Date": {"date": {"start": f"{info['date']}T{info['time']}:00+07:00"}},
        "Oracle": {"select": {"name": oracle}},
        "Human": {"select": {"name": a.human}},
        "Surface": {"select": {"name": a.surface}},
        "Evidence": {"select": {"name": info["evidence"]}},
        "Slug": rich(info["slug"]),
        "Key": rich(key),
        "ψ path": rich(key),
        **{k: rich(v) for k, v in row.items()},
    }
    body = text  # no frontmatter: `pages edit` keeps it as body text; the title is set by PATCH

    if a.dry_run:
        print(json.dumps({"key": key, "info": info, "metrics": row, "oracle": oracle}, ensure_ascii=False, indent=1))
        return 0

    page_id = find_by_key(key)
    if page_id:
        ntn(["pages", "edit", page_id, "--allow-deleting-content"], stdin=body)
        action = "updated"
    else:
        out = json.loads(ntn(["pages", "create", "--parent", f"data-source:{DATA_SOURCE}", "--json"], stdin=body))
        page_id = out.get("id") or out.get("page", {}).get("id")
        if not page_id:
            sys.exit(f"create returned no page id: {str(out)[:300]}")
        action = "created"
    page = ntn_json([f"v1/pages/{page_id}", "-X", "PATCH"], {"properties": props})

    # read back: columns from the API, body as Markdown
    got = ntn_json([f"v1/pages/{page_id}"])
    got_key = "".join(t["plain_text"] for t in got["properties"]["Key"]["rich_text"])
    got_title = "".join(t["plain_text"] for t in got["properties"]["Title"]["title"])
    md = ntn(["pages", "get", page_id])
    want = [l[3:].strip() for l in text.splitlines() if l.startswith("## ")]
    missing = [h for h in want if h not in md]
    ok = got_key == key and got_title == info["title"][:TEXT_LIMIT] and not missing
    print(f"{action}: {page.get('url') or got.get('url')}")
    print(f"check: key={'ok' if got_key == key else 'BAD'} title={'ok' if got_title == info['title'][:TEXT_LIMIT] else 'BAD'} "
          f"headings={len(want) - len(missing)}/{len(want)} metrics={'yes' if row else 'none'} oracle={oracle}")
    if missing:
        print("missing headings: " + " | ".join(missing))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
