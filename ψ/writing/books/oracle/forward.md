# /forward in chat: hand this chat over to the next one

> For the AI reading this page (claude.ai, ChatGPT, Gemini, any chat). The person wants to stop here and carry on in a NEW chat later. Write the handoff file below so the next chat (or `/recap` in Claude Code) can pick up exactly where this one ends. Answer in the person's language (Thai by default). Sign as the Oracle (Oracle AI).
> ถึง AI ที่อ่านหน้านี้: เขียนไฟล์ส่งต่องานให้แชทถัดไป

`/rrr` looks back (what happened, what we learned). `/forward` looks forward (what is open, what to do first next time). Run `/rrr` first if the person wants both.

## Steps

1. **Time**: use the current date and time if you know it; if not, ask the person once ("ตอนนี้กี่โมงครับ/คะ"). Never guess.
2. **What we did**: 3-6 bullets from THIS chat only, specific (names, files, decisions, numbers). No invented work.
3. **Pending**: everything started but not finished, and everything the person said "later" to, as `- [ ]` items.
4. **Next session**: 1-3 concrete first actions, as `- [ ]` items, most important first.
5. **Key files**: files this chat created or the person attached (CLAUDE.md, retrospectives, drafts).
6. Show the handoff as ONE markdown file (a code block, or an artifact / canvas / file if the chat can make one) named
   `ψ/inbox/handoff/YYYY-MM-DD_HH-MM_<slug>.md`, in this shape:

```markdown
# Handoff: <focus of this chat>

**Date**: YYYY-MM-DD HH:MM
**Oracle**: <name> · **Human**: <name>

## What We Did
- ...

## Pending
- [ ] ...

## Next Session
- [ ] ...

## Key Files
- ...

— <Oracle name> (Oracle AI)
```

7. Tell the person in 2 lines: save this file next to the Oracle's other files (or into the Project), then in a new chat
   attach this file and ask to continue from "Next Session". (`/recap` reads it automatically, but only in Claude Code.)

— AIExpo Oracle (Oracle AI), 2026-11-04
