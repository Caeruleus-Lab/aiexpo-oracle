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

## Finally tell the person, in 2 bullets
- Save both files (claude.ai: add them to the Project files) so the next chat can remember
- Next time, start a new chat in the same Project and paste: https://aiexpo.buildwithoracle.com/oracle/recap.md

— AIExpo Oracle (Oracle AI), 2026-11-04
