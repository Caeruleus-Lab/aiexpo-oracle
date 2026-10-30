# Rehearsal checklist: ARRA Oracle & Multi-Agent Workflow

Fri 6 Nov 2026, 15:05–16:10, Builder Stage, Challenger Hall. Nat + คุณยิ้ม.
Drafted by AIExpo Oracle (Oracle AI), 2026-10-30, for Nat and คุณยิ้ม to change.
Sources: `ψ/writing/slides/deck.html` (block clocks), `ψ/writing/2026-10-27_workshop-design-v1.md` (run of show and rehearsal dates),
`ψ/memory/learnings/2026-10-30_line-masterclass-facts.md` (organizer asks), `ψ/memory/learnings/2026-10-30_full-agenda.md` (the day's stage).

> No changeover: AI Vibe Coding 101 ends at 15:05 on the same stage. Everything below "before 15:05" has to be done before then.

## 1. Laptop and cables

- [ ] Nat's own laptop (organizer agreed 29 Oct), charged, charger in the bag
- [ ] USB-C → HDMI adapter, plus a spare. TODO: ask the organizer which input the stage has (HDMI only?)
- [ ] Display set to mirror. Test at 1920×1080. The deck scales to any window, but check it fills the screen
- [ ] Notifications off (Focus mode). Hide LINE, Discord and mail windows. No personal chats on the big screen
- [ ] Terminal font size large enough to read from the back row. Check from the back during the stage test
- [ ] Battery saver and auto-lock off for the 65 minutes

## 2. Network

- [ ] Venue wifi: TODO, get the SSID and password from the organizer
- [ ] Phone hotspot as the fallback, tested with Claude Code before the day
- [ ] Offline copies on the laptop: `deck.html` + `speakers-crop.jpg` (the deck has no other network dependency), `deck.pdf`, the demo clip (29 Oct recording, 0:45–1:45 for the room view)

## 3. Accounts

- [ ] Claude Code logged in on the stage laptop. Run one prompt the morning of the event to prove the token is live
- [ ] A **clean** account or folder for the live demo, so the room sees what a newcomer sees (lesson: test the exact path an attendee takes)
- [ ] One Oracle that already has `ψ/` memory from earlier days, for the forgetting test's "it remembers" window
- [ ] Codex and Antigravity checked for hands-on 2 (design decision #5). If their sub-agents don't behave the same, that track watches the demo

## 4. Demo path (in deck order)

| Clock | Slide | What runs on screen | Ready before 15:05 |
|---|---|---|---|
| 15:05 | 1–3 | Forgetting test: a fresh chat vs the Oracle, same question "เมื่อวานเราทำอะไรกัน" | both windows open, side by side |
| 15:07 | 4 | Count of Oracles born in the homework | TODO: replace N with the real count from submissions, or ask for hands |
| 15:08 | 5 | Bridge from คุณยิ้ม's 11:00 workshop | the morning's example job (still to be chosen by คุณยิ้ม) |
| 15:18 | 6–7 | What an Oracle is · the loop | — |
| 15:25 | 8–9 | Hands-on 1: `/recap` → one task → `/rrr` → close → reopen → `/recap` | a terminal in the clean folder |
| 15:38 | 10 | Hands-on 2: the 3-helper prompt | the 3 "team of AI" tasks from the worksheet |
| 15:50 | 11–12 | Where it grows: the herdr room, each agent's own app | room already built, or the clip queued |
| 15:53 | 14 | `/rrr` do-it-now (never cut) | — |
| 15:56 | 15 | Homework: how and when to submit | TODO: the submission link or QR |
| 15:58 | 16 | Close | — |
| 15:59–16:10 | 17 | E-certificate QR on screen during Q&A (organizer ask) | TODO: the real svg saved and swapped in |

Cut order if late (from the deck notes): "where it grows" → shorter Q&A → hands-on 2 becomes a demo. Never cut the forgetting test, the `/rrr` slot or the QR slide.

## 5. Timing rehearsals

- [ ] **Rehearsal 1** (planned 1–2 Nov): clean accounts on Claude Code, Codex Free, Antigravity Free and claude.ai web. Time every step and record fallback screenshots
- [ ] **Rehearsal 2** (planned Tue 4 Nov): with คุณยิ้ม, the full 65 minutes on a timer
- [ ] Write the measured minutes per block next to the clock column above. Cut any block that runs 1.5× over unless it produces something the attendee keeps (CCC rehearsal lesson)
- [ ] Final slide file to the organizer by **Mon 2 Nov** (the PDF from 30 Oct was the first file)

## 6. If Claude Code is down

| Symptom | Fallback |
|---|---|
| Claude Code won't start or log in on stage | Switch to the hotspot and retry once. Otherwise run the same prompts in Codex, or play the recorded clip and screenshots |
| The model answers slowly | Keep talking over it, then move to the next slide; the paper track keeps the room busy |
| The whole room's wifi is down | Paper track for everyone: write the `/rrr` by hand on the handout and draw the team for hands-on 2. Homework is still submitted within the day |
| Sub-agents don't run (hands-on 2) | Show the result from rehearsal as a demo, as the cut list already plans |
| The deck won't open | Open `deck.pdf` |

## 7. Day of, stage test (Builder Stage lunch gap 12:40–13:30)

- [ ] Plug in, mirror, deck on slide 1, notes off (`N`)
- [ ] Run the forgetting test once on stage wifi
- [ ] Sound: if the room has a mic for the laptop, check the demo clip's audio
- [ ] Leave the laptop asleep on slide 1, both windows open, so 15:05 starts with no setup
- [ ] Handout copies or a QR to the handout (TODO: how attendees get it, print or link)

---
— AIExpo Oracle (Oracle AI)
