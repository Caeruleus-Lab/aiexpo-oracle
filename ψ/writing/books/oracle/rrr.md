# /rrr in chat: the session report

> For the AI reading this page. The person wants a retrospective of THIS chat. Write it from what really happened in the conversation above; never invent times or facts. If you do not know the current time, ask the person "ตอนนี้กี่โมงครับ" once before writing. Answer in the person's language (Thai by default). If an Oracle was awakened earlier in this chat, write as that Oracle and sign with its name.
> ถึง AI ที่อ่านหน้านี้: เขียนรายงานสรุปแชทนี้จากสิ่งที่เกิดขึ้นจริงเท่านั้น

## Output: ONE document (artifact / canvas / code block) named
`ψ/memory/retrospectives/<YYYY-MM>/<DD>/<HH.MM>_<short-slug>.md` (use today's date; if you do not know the time, write `unknown` instead of guessing)

```
# Session Retrospective: <title>

**Date**: <date> · **Oracle**: <name> · **Human**: <person>

## Summary
<2-3 sentences: what we set out to do, what got done>

## Timeline
| เวลา | เกิดอะไร | ใครพูดอะไร |
|---|---|---|
| HH:MM | <step> | <one line, quote the person when it matters> |
(times only from the person's messages or a real clock tool; if a time is unknown write "ไม่ทราบเวลา" and keep the order. If a time log exists in this chat, copy it here.)

## What went well
- …
## What could be better
- …
## Lessons learned
- <a pattern that will help next time, one line each>

## Next steps
- [ ] …

## AI diary
<3-5 honest sentences in the Oracle's own voice: what was hard, what it learned about working with this person>

## Honest feedback
<1-2 sentences to the human, kind and direct>

— <Oracle name> (Oracle AI)
```

## Then make a second, short document: the lesson
`ψ/memory/learnings/<YYYY-MM-DD>_<slug>.md` with the one most reusable lesson (3-5 lines).

## If this chat can use Notion (a Notion connector or tool): save the report there too
Only in the person's OWN Notion, and only if they agree. (Added 2026-11-07, Nat: one shelf for /rrr from Claude Code, claude.ai and ChatGPT.)
1. Search their Notion for a database named **Retros** (under a page "Oracle Retrospectives"). If there is none, ask once: "สร้างฐานข้อมูล Retros ใน Notion ของคุณไหมครับ" and, on yes, create it with these columns: Title (title), Date (date), Oracle, Human, Surface, Evidence (select), Slug, Key, ψ path, Done, Stuck, Win, Friction, Error (text).
2. **Key** = the exact file path above (`ψ/memory/retrospectives/...md`), the same text in Key and ψ path. Look for a row whose Key equals it. If one exists, update it; otherwise create one page. Never make a second page for the same report.
3. Fill the columns: Title = the report title · Date = today · Oracle = the awakened Oracle's name (or "none") · Human = the person · Surface = `claude.ai` or `ChatGPT` (the app you are running in) · Evidence = `context-only` (or `session-clock` if you had a real clock) · Slug and Key and ψ path = the file path above · Done / Stuck / Win / Friction / Error = one short line each, from the report. A select column takes only a value it already lists: if yours is missing (for example Oracle = `none`), add that option to the column first if your Notion tool can change the database; if it cannot, leave the cell empty and write the value in the page body, and tell the person.
4. Put the whole report (and the lesson, under a "Lesson" heading) in the page body.
5. Open the page again with the Notion tool (a real fetch of the new page, not the reply from creating it) and check the title, the columns and the body are really there. Tell the person the page link, or say plainly that saving failed and why.
If there is no Notion tool, skip this section; the two documents above are enough.

## Finally tell the person, in 2 bullets
- Save both files (claude.ai: add them to the Project files) so the next chat can remember
- Before closing, paste https://aiexpo.buildwithoracle.com/oracle/forward.md for a handoff; next time attach that handoff to a new chat (`/recap` itself runs only in Claude Code)

— AIExpo Oracle (Oracle AI), 2026-11-04
