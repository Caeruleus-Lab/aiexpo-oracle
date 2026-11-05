# Narrated lessons (Thai voice + subtitles) — 2026-11-02

8 lessons, 76 slides, 270 subtitles, 27.7 min, 14 MB. Voice: Edge TTS `th-TH-NiwatNeural` (AI voice, male: ผม/ครับ).

| File | Does |
|---|---|
| `scripts/NN-<lesson>.json` | narration: slides (title, bullets, code, image) + lines (`text` = subtitle, `say` = spoken form) |
| `lexicon.json` + `scripts/*.lex.json` | English → Thai karaoke spelling; Niwat cannot read English. Build stops if any English word has no spelling |
| `build.py` | `--check` (no TTS) or build: one clip per line (cached), measured cue times, one MP3 per slide, `out/<lesson>/talk.json` |
| `manifest.py` | `out/lessons.json` for the index |
| `index.html`, `player.html` | lesson list; player with auto-advance, CC (C), Space, ←/→, progress bar, "next lesson" at the end |
| `BRIEF.md` | the rules the script writers followed (lessons 02–08 drafted by Sonnet, one agent per lesson, checked here) |

Run: `python3 build.py scripts/0*-[a-z]*[a-z].json && python3 manifest.py && python3 -m http.server 8766 --bind 127.0.0.1`

Checked: all 8 play in ego-browser (subtitle + clock moving), every audio/image file exists, every cue inside its slide audio.

— AIExpo Oracle (Oracle AI)
