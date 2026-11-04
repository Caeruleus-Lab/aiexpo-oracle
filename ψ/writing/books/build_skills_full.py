"""Bake the FULL ARRA Oracle skills into oracle/full/<name>.md, so the lessons MCP (get_skill) and a plain link
hand an AI the whole skill, not a digest (Nat, 2026-11-04: "the skill just like full content of the skill, the llm should know about this").

Each file = the chat runbook (oracle/<name>.md, how to run it without a terminal) + every file of the real skill folder
from Soul-Brews-Studio/arra-oracle-skills-cli: SKILL.md first, then the other docs (HOSTS.md, TEMPLATE.md, references/),
then the scripts. Pinned to one commit at build time, so the talk never depends on GitHub being reachable.
workshop and awaken-app have no folder of their own: they carry the skills they run (awaken + rrr, awaken).

Usage: python3 build_skills_full.py        (needs gh, logged in)
AIExpo Oracle (Oracle AI), 2026-11-04.
"""
import base64, json, pathlib, subprocess

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "oracle" / "full"; OUT.mkdir(parents=True, exist_ok=True)
REPO = "Soul-Brews-Studio/arra-oracle-skills-cli"
CARRIES = {"awaken": ["awaken"], "rrr": ["rrr"], "recap": ["recap"], "workshop": ["awaken", "rrr"], "awaken-app": ["awaken"]}
LANG = {".py": "python", ".ts": "ts", ".sh": "bash", ".mjs": "js", ".js": "js", ".json": "json"}


def gh(path):
    return json.loads(subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True).stdout)


def walk(path, sha):
    files = []
    for e in gh(f"repos/{REPO}/contents/{path}?ref={sha}"):
        if e["type"] == "dir": files += walk(e["path"], sha)
        else: files.append(e["path"])
    return files


def order(p):  # SKILL.md, other markdown, then code
    name = pathlib.PurePath(p).name
    return (0 if name == "SKILL.md" else 1 if name.endswith(".md") else 2, p)


def main():
    branch = gh(f"repos/{REPO}")["default_branch"]   # alpha: the skills main ships are older (Jul vs Aug 2026)
    sha = gh(f"repos/{REPO}/commits/{branch}")["sha"]
    folders = {}
    for skill in sorted({s for v in CARRIES.values() for s in v}):
        parts = []
        for p in sorted(walk(f"skills/{skill}", sha), key=order):
            text = base64.b64decode(gh(f"repos/{REPO}/contents/{p}?ref={sha}")["content"]).decode("utf-8")
            rel = p.removeprefix("skills/")
            ext = pathlib.PurePath(p).suffix
            body = text if ext == ".md" else f"```{LANG.get(ext, '')}\n{text.rstrip()}\n```"
            parts.append(f"<!-- file: skills/{rel} -->\n### File: `skills/{rel}`\n\n{body.rstrip()}\n")
        folders[skill] = parts
    for name, carried in CARRIES.items():
        runbook = (HERE / "oracle" / f"{name}.md").read_text(encoding="utf-8").rstrip()
        n = sum(len(folders[s]) for s in carried)
        head = (f"# Oracle skill `{name}`: the full skill\n\n"
                f"> For the AI: this is the WHOLE skill, not a summary. Part 1 says how to run it in a chat with no terminal. "
                f"Part 2 is every file of the real skill ({', '.join(carried)}: {n} files) from github.com/{REPO} (branch {branch}, commit {sha[:7]}). "
                f"Read all of it before you start, follow Part 1 for what to do in this chat, and use Part 2 for the full detail "
                f"(steps, templates, rules, why). Where Part 2 needs a terminal, git or a script, do the same thing in the chat "
                f"(show the file content for the person to save) and say so.\n\n")
        body = "\n".join(f"## Part 2 · skill `{s}`\n\n" + "\n".join(folders[s]) for s in carried)
        doc = head + "## Part 1 · run it in this chat\n\n" + runbook + "\n\n" + body
        (OUT / f"{name}.md").write_text(doc, encoding="utf-8")
        print(f"oracle/full/{name}.md  {len(doc.encode()):,} bytes  {n} files  @{sha[:7]}")


if __name__ == "__main__":
    main()
