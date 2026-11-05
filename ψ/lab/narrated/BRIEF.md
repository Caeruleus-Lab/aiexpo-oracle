# Brief: write one narrated-lesson script (Thai voice + subtitles)

You turn ONE lesson README into a narration script: `scripts/NN-<lesson>.json` (+ `scripts/NN-<lesson>.lex.json`).
Model to copy: `scripts/01-claude-chatgpt.json` (read it first, all of it). Shared dictionary: `lexicon.json`.

## Voice and style
- Voice `th-TH-NiwatNeural` (male). Narrator = AIExpo Oracle, an AI. Use ผม / ครับ (never ดิฉัน / ค่ะ).
  End only some lines with ครับ (about one per slide), not every line.
- "Explain like what happened": tell what WE actually did and saw, with the real date/numbers from the README
  ("วันที่ 31 ตุลาคม เรารัน ... แล้วเห็นว่า ..."). Never invent a fact, number, command or result that is not in the README.
- Plain spoken Thai, like a calm teacher in an online course. Short sentences. No em-dash, no "ไม่ใช่ X แต่เป็น Y" slogans.
- Always write "คุณยิ้ม" and "คุณนัท" (never bare ยิ้ม/นัท).
- Length: 6–10 slides, 2–5 lines per slide, about 2–4 minutes total (~25–40 lines). First slide = title + one-line promise.
  Last slide = the one thing to remember + a short close. Skip the README's "sources" and "signature" sections.

## Slide schema (exactly these keys)
```
{ "title": "...", "sub": "optional", "bullets": ["optional", "..."], "code": "optional one short command",
  "image": "images/<file>.png (optional, must exist in the lesson dir)", "lines": [ {"text": "...", "say": "optional"} ] }
```
- Top level: `lesson` (id below), `dir` (lesson dir below), `title` (the lesson's Thai title), `voice` "th-TH-NiwatNeural", `slides`.
- `text` = the subtitle shown on screen (real spelling: `Claude Code`, `/awaken`, `--dry`). Max 140 characters per line.
- The voice CANNOT read English. Every English word / command / number-with-dots is spoken from Thai karaoke spelling:
  1. If a phrase needs a natural spoken form (a slash command, a flag, a URL, a file path), give that line a `say`
     written in Thai, e.g. `"say": "พิมพ์ สแลช อะเวคเคน ฟาสต์"`, `"say": "แฟล็ก ดราย"`, `"say": "คล้อด ดอท เอไอ"`.
  2. Plain English words left in `text`/`say` are replaced automatically from `lexicon.json` + your own `.lex.json`.
     Put every word the check reports into `scripts/NN-<lesson>.lex.json` as `{"English": "ไทยคาราโอเกะ"}` —
     spell it the way Thai people say it (คล้อด โค้ด, แชทจีพีที, เทอร์มินัล, เฮิร์ดเดอร์, เอ็มซีพี). Do NOT edit lexicon.json.
  3. Digits are fine as Thai digits (30 ตุลาคม). Versions/IDs like 1.4.12 or w5:p1 need a `say` in Thai.
- Use only images that exist: `ls <lesson dir>/images`. Prefer real screenshots and captures; one image per slide at most.

## Check, fix, repeat (no TTS, 0.1 s)
`python3 build.py --check scripts/NN-<lesson>.json` must print `OK`. Never run build.py without --check
(the lead builds the audio). Never touch other lessons' files. Stop at ~40 tool calls.
Return only: `wrote NN-<lesson>.json — <slides> slides, <lines> lines, <n> lex words, check OK`.
