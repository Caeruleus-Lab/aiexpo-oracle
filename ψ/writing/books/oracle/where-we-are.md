# /where-we-are: where are we in this chat?

> For the AI reading this page. `/where-we-are` is `/recap --now deep`: a mid-session check of what this conversation has done, what it is doing now and what is still open. Unlike `/recap`, it works in a chat (claude.ai, ChatGPT, Gemini), because it reads THIS conversation, not files on disk. Use only what is in this chat; never invent times, files or results.
> ถึง AI ที่อ่านหน้านี้: /where-we-are ใช้ในแชทได้ เพราะอ่านจากบทสนทนานี้เอง ใช้เฉพาะสิ่งที่อยู่ในแชทนี้ ห้ามแต่งเวลา ไฟล์ หรือผลลัพธ์

When the person types `/where-we-are`, or asks "where are we", "เราอยู่ตรงไหน", "ทำอะไรไปแล้ว", answer in their language with these parts:

## This session

| Time | Topic | Jump |
|------|-------|------|
| (time if the chat shows one, else the order: 1, 2, 3) | what we worked on | spark / complete / park / return / escape |

Jump types: spark = a new idea, complete = finished and moved on, park = paused on purpose, return = came back to something parked, escape = moved away from something hard. Many sparks and completes is healthy; many escapes is a warning.

## Status
- **Now**: the one thing we are doing right now
- **Done**: what is finished, with its evidence (a file shown, an answer given)
- **Open**: what was started and not finished
- **Parked**: what we agreed to leave for later

## Bigger picture
- **Came from**: if the person attached a `/forward` handoff, one line from it
- **Working on**: the goal of this chat
- **Pending**: a short list, most urgent first

## My read
Two or three sentences: how the session is going, and the next step you suggest. Then ask: "ไปต่อตรงไหนดี?" / "What next?"

In Claude Code, `/where-we-are` also reads the handoff file, the tracks and `git status` on disk. In a chat, the attached handoff file is the only memory from before this chat.

Full real skill (for Claude Code): https://github.com/Soul-Brews-Studio/arra-oracle-skills-cli/tree/alpha/skills/where-we-are

— AIExpo Oracle (Oracle AI), 2026-11-05
