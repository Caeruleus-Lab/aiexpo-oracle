"""Fix links on the built pages that only work inside the git repo, not on a website.

The READMEs are signed, so they keep their repo-relative links (they work when the markdown is read on GitHub).
On the web pages a folder link like captures/ has no index page, and ../../../../.mcp.json points outside the
site. Folder links go to the public copy on GitHub (Caeruleus-Lab/aiexpo-lessons) instead, ../worker.js to the
MCP source there, and links to files that are not public (repo root, deploy.sh) become plain code.
"""
import re

REPO = "https://github.com/Caeruleus-Lab/aiexpo-lessons"
FOLDERS = ("captures/", "prompts/")
MOVED = {"../worker.js": f"{REPO}/blob/main/mcp/worker.js"}


def fix_links(html, lesson_dir):
    def one(m):
        href, inner = m.group(1), m.group(2)
        if href in FOLDERS:
            return f'<a href="{REPO}/tree/main/{lesson_dir}/{href}">{inner}</a>'
        if href in MOVED:
            return f'<a href="{MOVED[href]}">{inner}</a>'
        if href.startswith("../../../../") or href == "../deploy.sh":
            return inner if inner.startswith("<code>") else f"<code>{inner}</code>"
        return m.group(0)
    return re.sub(r'<a href="([^"#:]+)">(.*?)</a>', one, html)
