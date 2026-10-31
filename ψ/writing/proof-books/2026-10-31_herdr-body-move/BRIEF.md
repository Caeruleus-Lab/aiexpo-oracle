# BRIEF — shared by every chapter writer

Book dir (absolute): `/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle/ψ/writing/proof-books/2026-10-31_herdr-body-move`
Read `OUTLINE.md` there first: title, parts, and YOUR chapter's subtopics and image list.

## What this book is
This book follows one real event on 31 Oct 2026, machine m5: AIExpo Oracle (an AI agent, Claude Code) moved its
"body" (the herdr pane it runs in) from the worktree `laris-co/course-team/wt/aiexpo-oracle` (pane wCC:p3) back to its own
main checkout `Caeruleus-Lab/aiexpo-oracle` (pane wCC:p5), inside herdr session `laris-co`, room/space `wCC`
"aiexpo-oracle", next to its worktree partner `aiexpo-wt` (wCC:p4). The first `herdr-room in` gave 3 columns, not 2.
The live session was only READ. Every move was REPLAYED in a scratch herdr session `bookdemo`, where plain shell panes
were made to look like claude agents with `herdr pane report-agent` (captures 07-25). The real night is read back
from the two Claude Code transcripts with `timeline.py` (captures 15, 26, 27). Outputs are in `captures/NN-slug.txt`
rendered as `images/NN-slug.png`; diagram cards in `diagrams/Dn-*.txt` -> `images/Dn-*.png`. Author: AIExpo Oracle
(an AI) with Nat. Audience: a developer who runs several AI agents in herdr.

## Style = /browser-tutorial, in Thai
- Numbered steps inside each section: `### ขั้นที่ N — <what it does>`, N restarting at 1 per `##`.
  Each step: 1–3 sentences telling the reader what to type and why → the command in a ```bash block
  → the image of the REAL output directly under it → 1–3 sentences reading the output.
- **Prose carries the instruction; the image confirms it.** A reader with no images must still
  follow. Quote the 2–6 most important output lines in a plain ``` block when the point is a number.
- Image: `![<what is IN the shot, Thai ok>](images/NN-slug.png)` — relative path, only names that
  exist in `images/` (list below). Never invent an image name.
- In each step, the ONE key idea in **bold** — one span per step.
- When something fails or surprises, that IS the lesson: keep it, explain the cause, give the fix.
- Diagram cards go where the concept is introduced, with one sentence on what the picture shows
  that prose did not.
- **Pace: every printed page carries 1–2 images (3 when all three are small captures).** In
  practice: no more than ~250 Thai words (or one long code block) between two images. Pair short
  captures in one step. A section that would be prose-only gets the capture behind its main claim,
  or is cut. `make check` fails on a text-only page (`page_images.py`).

## Language — Thai, kien-thai frames
Natural Thai for a developer colleague next to the terminal. Commands, flags, file names, code,
numbers and product names stay in English/ASCII. f1 topic-comment · f2 condition first (พอ...ก็...)
· f3 short clauses · f4 particles where natural · f5 drop pronouns the context carries · f6 ก็ as
rhythm · f7 pivot with a question or แต่. No English sentences in prose. No emoji. No "!!!".

## Hard rules
- **Never invent output, numbers, flags or behaviour.** Every number must appear in a capture file
  or in FACTS below. Open the capture `.txt` files and read them.
- ```bash for commands, untagged for output. Lines ≤ 76 chars (wrap with ` \`, cut output with `…`);
  verbatim source excerpts stay verbatim.
- Paragraphs ≤ ~500 characters.
- File starts `# บทที่ N: <title>` (frontmatter `# คำนำ`). Sections `##`, steps `###`.
- End with a short forward hook — no recap list.
- Read your captures with ONE call: `python3 verify.py --bundle <your-chapter>.md` (prints every capture and
  diagram the OUTLINE lists for you). Never open a PNG. Never run make, typst or pdftoppm: the lead builds.
  Stop at ~60 tool calls. `python3 verify.py` (0.1 s) checks your numbers, ids and times against the captures.
- Write คุณยิ้ม never bare ยิ้ม if she comes up (she should not; this book is about herdr). Pane ids in a
  step must be the ids in that step's capture (ids change on every move: w5:p1 became w7:p1).
- **WRITE THE FILE YOURSELF**. Return ONLY: `wrote NN-slug.md — <words> words, <n> images`.

## Images available (exact names)
D1-overview D2-herdr-nesting D3-room-in-rule D4-race D5-left-right D6-recipe ;
00-help 01-live-room 02-branches 03-handoff 04-charter 05-session-host 06-sessions 07-spaces 08-fake-agents
09-agents 10-explain 11-room-dry 12-room-in 13-room-state 14-room-list 15-real-launch 16-new-pane 17-exit-timer
18-room-three 19-state-three 20-state-edit 21-source 22-out-dry 23-old-gone 24-room-two 25-state-two
26-night-old 27-night-new 28-left-right-rule 29-main-log 30-merge-scan 31-live-state 32-old-dir 33-larisco
34-timeline-src 35-scan-hits
Each image is used ONCE, in the chapter OUTLINE.md assigns it to.

## FACTS measured on 2026-10-31 (use these; do not add others)
- Words: "ร่าง" (body) = the herdr pane + Claude Code session an oracle runs in; "วิญญาณ" (soul) = its repo
  (CLAUDE.md + ψ vault). "ห้อง" (room) = a herdr space whose one tab shows several agents (herdr-room). herdr's CLI
  calls a space a "workspace"; ids look like wCC (space), wCC:t1 (tab), wCC:p5 (pane).
- Session ids: old body 89a694ad (pane wCC:p3), new body 2969076e (pane wCC:p5), aiexpo-wt bfe79650 (pane wCC:p4).
  Source: herdr agent list at session start, and the transcript file names in captures 26/27 commands.
- Nat asked for the move on 31 Oct so the sidebar shows `main`, not `wt/aiexpo-oracle` (handoff file, capture 03).
- Nat's words relayed by the old body at 20:05:37: "keep talk left right" (capture 27, msg line).
- The new body was started BY THE OLD BODY (capture 15): it split its own pane down with cwd = main checkout,
  ran `claude "<brief>"` in the new pane, and scheduled its own `/exit` + `pane close` with two timers
  (sleep 40 at 20:05:21, sleep 20 at 20:05:45, Bangkok time = UTC+7; capture 15 shows UTC).
- The first real `herdr-room in` (20:05:38) saw 3 members. The state file was edited to drop p3 at 20:05:48 and room in
  run again: still 3 (that output is not captured on the real night; the replay shows the same in capture 20).
  At 20:06:04 room in was run again after p3 had closed: 2 members; the saved state says 20:06:05 (capture 31).
- In the replay the old body's timer was 30 s (capture 17), the pane closed at 20:15:48 (capture 23).
- Merges done by the left pane tonight, all fast-forward after a scan: 0dec1a1, 8881cc1, 53c5e38 (capture 29 shows
  0dec1a1 on top; the later two came after the captures). index.b64.txt is base64; the scan decodes it before searching.
- The 3 local-path hits in capture 35 are lines inside vault notes merged earlier by the old body (fd279c7..8a61104);
  the book does not say whether they were reviewed then. Do not call them a leak; they are paths, not secrets.
- The replay ran in session `bookdemo`, started from a pane in laris-co space wCF with `herdr session attach bookdemo`.
  Nothing in the live room wCC was moved for the book.
