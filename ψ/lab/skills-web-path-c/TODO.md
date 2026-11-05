# skills-web-path-c: todo

Status as of 2026-10-31. `[x]` means verified by running it, not by assuming.
Tracking: TODO.md only.

## Done — verified

- [x] 28 ZIPs pass claude.ai preview. Verified: ego-browser loop, `captures/13-claude-ai-preview-28.txt` → 28/28 names shown.
- [x] Deps measured per skill. Verified: rg counts on m5 (table in SPEC).
- [x] skills.json manifest + build_skills.py. Verified: ran twice, second run printed same `ok 6, partial 13, local 9`, no further diff.
      Surprise: a deps formula could not reproduce the judged verdicts; verdict moved to a hand column (SPEC edited).
- [x] Start-here box + web column (th/en). Verified: `rg -c '\| ✗ \|' README.md` → 9; box lists awaken, rrr, recap.
- [x] Heatmap on th/en pages. Verified: ego-browser screenshots dark + light (/tmp/skillmap-*.png); filter "web OK" → 6 rows
      (where-we-are, who-are-you, philosophy, oracle-prism, bampenpien, oracle-title-forge).
      Surprise: light mode green #22e06b too faint; added --heat #0b8f43 for light.
- [x] Re-sign, rebuild, deploy, ping. Verified: verify.mjs VALID; commit 8da22df; live en page has id="skillmap" and 9 data-web="local".

## Deferred — decided, not scheduled

- [ ] Real upload of oracle-prism + recap. Blocked on Nat's yes. Revisit when he says go.
- [ ] Upstream issue: web-mode flag in SKILL.md. Revisit after the workshop (6 Nov).

## Sprint Retro

| # | Task | Hypothesis | Matched? | Surprise |
|---|---|---|---|---|
| 1 | manifest + builder | one script regenerates | yes | verdict needs a hand column |
| 2 | start-here + web column | 3 match deck, 9 ✗ | yes | none |
| 3 | heatmap | renders both themes | after fix | light green too faint |
| 4 | ship | VALID + live | yes | none |

- Matched 4/4 (one after a fix). Lesson: a measured column is evidence, not a verdict; keep the judgment explicit.
