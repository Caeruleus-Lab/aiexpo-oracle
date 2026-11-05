# Paxa TTS docs digest (read 2026-10-31)

Source: https://paxalabs.com/llms-full.txt (948 KB, 132 pages). Read in full: the TTS pages and TTS guides
(generate speech, directions, pauses, temperature, timestamps, designed voices, Flash v2 launch, choosing a
Thai voice, writing a Thai script, judging a Thai voice, Thai subtitles from timestamps, YouTube and
audiobook guides). Skimmed by index only: STT, OCR, extraction, translation, integrations, live socket, latency.

## Request (POST /v1/tts)
- `model: paxa-tts-flash-v2` (nickname Pixie). 50 voices, each speaks Thai, English, Mandarin. 26 F / 24 M.
- `format`: mp3 on v2 is 44.1 kHz 128 kbps (good enough for web); wav/pcm 24 kHz unless `sample_rate` (8k–48k).
- `speed` 0.5–1.5, a multiplier on the voice's own designed pace. Same price.
- `temperature` 0–2 (default 0.5): how much pacing, pauses, breaths, melody vary between takes. Low for a line
  replayed many times; high to get several takes to choose from.
- `language`: auto | th | en | zh — only how digits, codes, symbols read.
- `timestamps`: word | sentence | utterance → JSON with base64 `audio` + `timing.spans[{text,start,end}]`;
  Thai is segmented by the model; tags take no span. Bills 1.25x.
- Max 5,000 characters per request. 10 credits per 1,000 chars ($10 per million). Tags bill as characters.

## Direction tags (v2, every voice)
- Any words in `[...]`, in Thai, English or Chinese, set the delivery until the next tag: `[อบอุ่น พูดช้า ๆ]`,
  `[ค่อย ๆ ตื่นเต้นขึ้น]`, `[product advertisement, punchy and upbeat]`. `[neutral]` resets.
- Weights and blends: `[excited:2]`, `[sad:50%]`, `[happy:0.7+sad:0.3]`.
- Sounds: `[laughs] [chuckles] [sighs] [gasps] [inhales deeply] [giggles] [sobs] [yawns] [clears throat] [scoffs]`.
- Hesitations `[um] [hmm] [เอ่อ]` are spoken. Spans: `<emph>…</emph>`, `<whisper>…</whisper>`.
- Pauses: `[short pause]` 130 ms, `[pause]` 180 ms, `[long pause]` 460 ms in Thai; `[pause 300ms]` max 500 ms.
- Refused (400 tag_invalid, no charge): accents, a different voice (`[เสียงเด็ก]`), singing, sound effects,
  languages, sounds off the list (`[coughs]`). Only tags → 422 unspeakable_text.

## Writing a Thai script for a voice
1. A space is a pause (a breath). Put one where a reader breathes; never inside a word.
2. End every sentence with a full stop or question mark; prose Thai omits them, a voice needs them.
3. Western year: write ค.ศ. before it, or 2026 reads like an old Buddhist year.
4. Keep English words in Latin script (AI Expo, Builder Stage, relic5). Respelling in Thai reads worse.
   Acronyms read letter by letter; acronyms said as words (NASA) go in Thai script.
5. Space phone digits into groups; write ambiguous numbers (fractions, house numbers) as words.
6. Particles set register and gender: female ดิฉัน/ค่ะ (statement) / คะ (question, after นะ); male ผม/ครับ.
7. Narration reads best as paragraphs of 3–5 sentences; ads as one clause per line.

## Choosing a voice
Order: job → register of the text → gender → direction tags → language last.
- Long reads: foithong (F narrator), khanomkrok (M lead), matum (F documentary), panang (M stage actor).
- Lessons: chuchi (M), baitoey (F), kaprao (M). Announcements: thongek (M), massaman (M), todmun (F host), saku (F).
- Ads: nomyen (F lead), mooping (M), tomyum (F), kaengphet (M trailer).
- One voice per brand surface; a second voice only for a second character.

## Designed voice and licence
- `POST /v1/voices/design` from a 1–2 sentence description (who, how it sounds, how they speak, where heard,
  language); refine one change at a time; 5 credits per design or change; speech in it costs 1.25x.
- Paxa clones no voice from audio.
- Free credits alone: personal use only. Any purchase makes all the account's audio commercial.

## Subtitles from word spans
Cut a cue at a gap over ~0.5 s, at ~35 chars per line (2 lines max), or at ~6 s on screen.
