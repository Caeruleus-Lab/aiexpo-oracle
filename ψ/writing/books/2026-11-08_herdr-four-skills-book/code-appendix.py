#!/usr/bin/env python3
"""Write 09-code.md: the four herdr skills and their two scripts, verbatim, one fenced block each.
    python3 code-appendix.py        (from the book dir)
Source: ~/.claude/skills on m5, read on the day the book is built."""
import pathlib, datetime
SK = pathlib.Path.home() / ".claude/skills"
FILES = [
    ("herdr-wt/SKILL.md", "markdown", "/herdr-wt: ตัด worktree เปิด issue สร้าง space ปลุก agent แล้ว brief"),
    ("herdr-bring/SKILL.md", "markdown", "/herdr-bring: หา oracle ด้วย maw locate แล้วเปิด space ของมันใน herdr"),
    ("herdr-pr/SKILL.md", "markdown", "/herdr-pr: เซ็น PR issue หรือคอมเมนต์ด้วยบล็อก Built by"),
    ("herdr-pr/herdr-sign.sh", "bash", "สคริปต์ที่พิมพ์บล็อก Built by (ตัดข้อมูลส่วนตัวเมื่อ repo เป็น public)"),
    ("herdr-dissolve/SKILL.md", "markdown", "/herdr-dissolve: เก็บงาน เขียน tombstone แล้วปิด worktree"),
    ("herdr-dissolve/tombstone.py", "python", "สคริปต์ที่เขียน tombstone ก่อนลบ worktree (dry run ถ้าไม่ใส่ --write)"),
]
out = ["# ภาคผนวก: โค้ดเต็มทั้ง 4 สกิล", "",
       f"ทุกไฟล์ด้านล่างพิมพ์ตามจริงทุกบรรทัด อ่านจาก `~/.claude/skills/` บนเครื่อง m5 วันที่ {datetime.date.today()} "
       "ไม่ย่อ ไม่แก้ให้สวย คัดลอกโฟลเดอร์สกิลไปไว้ที่ `~/.claude/skills/` ของคุณแล้วใช้ได้เลย", "",
       "สกิล herdr ทั้ง 52 ตัวแบบเต็มอยู่ในบทเรียน herdr ทุกสกิล ฉบับเต็ม: "
       "https://aiexpo.buildwithoracle.com/2026-11-08_herdr-skills-full/", ""]
total = 0
for rel, lang, what in FILES:
    text = (SK / rel).read_text(encoding="utf-8").rstrip("\n")
    n = text.count("\n") + 1; total += n
    fence = "`" * (max([3] + [len(r) + 1 for r in __import__("re").findall(r"`{3,}", text)]))
    out += [f"## {rel}", "", f"{what} · {n} บรรทัด", "", f"{fence}{lang}", text, fence, ""]
pathlib.Path("09-code.md").write_text("\n".join(out), encoding="utf-8")
print(f"09-code.md: {len(FILES)} files, {total} lines")
