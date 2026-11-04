"""Publish copy of the talk decks for aiexpo.buildwithoracle.com/talk/ (Nat, 4 Nov 2026: deploy, notes stripped).
Only git-tracked files; speaker notes, HTML comments, briefs, logs, scripts and PDFs are left out. Called by books/deploy.sh.
AIExpo Oracle (Oracle AI)."""
import pathlib, re, shutil, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE
DST = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "books" / "dist" / "talk"
if DST.exists(): shutil.rmtree(DST)
files = subprocess.run(["git", "ls-files"], cwd=SRC, capture_output=True, text=True, check=True).stdout.split("\n")
skip = re.compile(r"(\.md$|\.py$|\.pdf$|\.log$|^yim-3d/briefs/|^yim-3d/checks/|^yim-3d/.*\.(json|txt|sh)$)")
n = 0
for f in filter(None, files):
    if skip.search(f): continue
    out = DST / f; out.parent.mkdir(parents=True, exist_ok=True)
    if f.endswith(".html"):
        s = (SRC / f).read_text(encoding="utf-8")
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)                                   # no internal comments
        s = re.sub(r'<(div|aside) class="notes">.*?</\1>', "", s, flags=re.S)          # no speaker notes
        s = s.replace("../books/2026-10-30_mcp-connect-guide/images/", "img/lesson03/")
        out.write_text(s, encoding="utf-8")
    else:
        shutil.copy2(SRC / f, out)
    n += 1
l3 = DST / "img/lesson03"; l3.mkdir(parents=True, exist_ok=True)
for img in ["02-claude-custom-connector-filled.png", "07-claude-tool-approval.png", "08-claude-answer.png"]:
    shutil.copy2(SRC.parent / "books/2026-10-30_mcp-connect-guide/images" / img, l3 / img)
(DST / "index.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=talk.html"><title>AI Expo 2026 · ARRA Oracle talk</title><a href="talk.html">talk</a>', encoding="utf-8")
print(n, "files")
