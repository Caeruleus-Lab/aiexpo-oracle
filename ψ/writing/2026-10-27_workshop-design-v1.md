# Workshop design v1: new, built from what past workshops taught

Drafted by AIExpo Oracle (AI), 2026-10-27, for Nat and คุณยิ้ม to decide. Draft only, nothing is fixed.
Source material: `2026-10-27_prep-from-relic5.md` (what relic5 holds) and the notes cited below.

Fri 6 Nov 2026, 15:05–16:10 (65 min), Builder Stage. Topic and subtitle as agreed with the organizer:
**ARRA Oracle & Multi-Agent Workflow: AI ที่จำงานของคุณได้ และความจำนั้นเป็นของคุณ**

> ไม่สอนฟีเจอร์ ให้ทุกคนรู้สึกว่า AI ลืม แล้วค้นพบเองว่าความจำที่เป็นไฟล์แก้ได้

## 1. What past workshops taught (and what changes this time)

| Past lesson | Where it came from | What v1 does differently |
|---|---|---|
| Installing ate the room: SIIT gave "Setup & First Chat" 60 of 480 min; PSRU students retried 6 times; Thai `gh issue` failed silently | SIIT Dec 2025 `workshop-flow.md`; PSRU lessons 28 Feb | **No installing in the room.** Install + `/awaken` is the homework, due before the day. That homework is also the e-certificate requirement the organizer already set |
| Teach through necessity: feel the pain, then find the answer | Nat's note 5 Jan 2026 | Open with **the forgetting test**: the room sees a fresh AI forget, then sees their own Oracle remember |
| Parallel birth: the demo and the exercise are the same activity | PSRU lesson 1 | Nat's Oracle and the room do each step **at the same moment**, not demo-then-copy |
| A `/rrr` that is only suggested never happens | PSRU lesson 6 | `/rrr` is a scheduled 3-minute "do it now" slot near the end |
| "Prompt" means a copyable block, not prose | CCC 24 May | Every hands-on step is one copyable prompt on screen **and** in the workbook |
| Lead with the audience, not the speaker's CV | MIdS Apr 2026 | Nat's fleet appears only as "where this grows", 3 minutes, after the room has its own result |
| The live Oracle answering in the room was the moment people remembered | CCC 24 May (Discord replies, voice, federation map) | Keep one live moment: Nat's Oracle team answers in Discord on the big screen |
| Rehearse with a timer; cut anything that runs 1.5× over unless it produces learner output | CCC rehearsal log 20 May | Two timed rehearsals (below) with a cut list ready |
| Verify the claim that matters, not the one next to it | AJ ฝน prep 25 Jul (dead Colab badges found live) | Test every link and command on a **clean** account, the exact path an attendee takes |
| A registry after each wave of births | PSRU lesson 5 | Homework submissions = the room's Oracle registry; show the count on screen at the start |

**What is new (never done in a past workshop):**
1. Attendees arrive **already owning an Oracle**, so the 65 minutes go to memory and teamwork, not setup.
2. The **forgetting test** as the opening, using the attendees' own Oracle from the homework.
3. คุณยิ้ม's SME question ("งานไหนให้คน งานไหนให้ AI") becomes the **design of the agent team**, so the two halves are one story instead of two talks.
   **But that question is the title of คุณยิ้ม's own 11:00 workshop the same day** (Nat, 27 Oct). So 15:08 must not re-teach it: it picks up the morning's result (see §2b).
4. Two tracks in the same room (decision #5): people who installed do it on their laptop; the others do the same steps in the paper/PDF workbook (and claude.ai web if they want).

## 2. Before the day

**Homework (sent to the organizer by ~31 Oct, due on the day, = e-certificate):**
1. Install one agent: Claude Code (Pro, recommended), or Codex (ChatGPT Free) or Antigravity (free).
2. Clone the workshop template repo (to make: one repo with `README` = one-page workbook).
3. Run `/awaken --fast`. Name the Oracle.
4. Do one small real task with it, then `/rrr`.
5. Submit the repo link (form; the sign-up stack from `laris-co/workshop-register` can be reused). Can't install? Submit the workbook page instead; still counts.

**Kit**: one-page install guide (3 tools + the web path), template repo, workbook PDF, slide deck, a fallback video/screenshots of every live step.

## 2b. คุณยิ้ม's 11:00 workshop, the same day

คุณยิ้ม runs "ออกแบบธุรกิจ SME 101: งานไหนให้คน งานไหนให้ AI และอะไรที่ต้องแก้ ต้องสร้าง หรือต้องซื้อ" at 11:00. That changes three things:

- **Don't repeat it.** Part of the 15:05 room was there at 11:00. The 15:08 slot becomes a **bridge**: "this morning we split a job and marked the AI boxes; this afternoon we hand those boxes to an Oracle and its team". About 8–10 minutes, not 17. The time goes to the hands-on.
- **One worksheet across both sessions.** The morning page "job → tasks → person / AI / build / buy" is the input to hands-on 2 in the afternoon. People who attended both bring their own page; the others get the worked example. The morning session can mention the 15:05 session at its close.
- **คุณยิ้ม's load.** Two sessions in one day, and the gap between them (about 12:00–15:00) is the only time to reset the stage laptop. Rehearsal 2 (4 Nov) should run the bridge, not a full second talk, and the morning laptop setup must not be what the afternoon demo relies on.

Questions for คุณยิ้ม: what the morning's worked example job is (the afternoon should reuse it), whether the morning sheet can carry the "AI → team of AI" column, and whether to mention the afternoon session at the end of the morning one.

## 3. The 65 minutes

| Clock | Min | Who | What happens | Room does |
|---|---|---|---|---|
| 15:05 | 3 | Nat | **The forgetting test.** Fresh chat: "เมื่อวานเราทำอะไรกัน" → it doesn't know. Same question to an Oracle → it answers from `ψ/`. Show "N Oracles were born in this room's homework" | Watch, raise a hand if their Oracle exists |
| 15:08 | 17 | คุณยิ้ม | **งานไหนให้คน งานไหนให้ AI.** One SME job (e.g. monthly invoicing). Split it into tasks; mark each: person / one AI / a team of AI. The "team of AI" boxes become today's agents. **Superseded by §2b: a 8–10 min bridge from her 11:00 workshop; the minutes freed go to hands-on 1 and 2** | Fill the workbook page: 1 job → 3–5 tasks → owner of each (or bring the morning page) |
| 15:25 | 7 | Nat | **What an Oracle is**: memory = files you own (`ψ/`, CLAUDE.md); the loop `/recap → work → /rrr`; one slide, the 3 layers | — |
| 15:32 | 13 | Nat + room | **Hands-on 1: the memory loop.** `/recap` → do one task from the workbook page → `/rrr` → **close the window** → reopen → `/recap`: it remembers | Laptop track: run the 4 copyable prompts. Paper track: write the `/rrr` by hand on the template |
| 15:45 | 12 | Nat + room | **Hands-on 2: one agent → a team.** One prompt: the Oracle hires 3 helpers in parallel for the 3 tasks คุณยิ้ม's page marked "team of AI", then merges the results. Show the time difference vs one at a time | Laptop: paste the prompt. Paper: draw who hands what to whom |
| 15:57 | 3 | Nat | **Where it grows**: live on screen, Nat's Oracle team answering in Discord; one search across months of memory (relic5) | Watch |
| 16:00 | 3 | room | **`/rrr` do-it-now** and submit (link or photo of the page) | Everyone |
| 16:03 | 7 | both | Q&A + "ความจำนั้นเป็นของคุณ": delete the chat, the files stay | — |

Cut list if late (in this order): "where it grows" → shorten Q&A → hands-on 2 becomes a demo only. Never cut the forgetting test or the `/rrr` slot.

## 4. Prep calendar (10 days)

| Day | Date | Work |
|---|---|---|
| Tue–Wed | 28–29 Oct | Nat + คุณยิ้ม agree on this outline (or change it). Choose the SME example job |
| Wed–Thu | 29–30 Oct | Build the template repo + one-page workbook + install guide. Write the homework brief |
| Fri | 31 Oct | Homework brief to the organizer (needed for the e-certificate) |
| Sat–Sun | 1–2 Nov | **Rehearsal 1** on clean accounts: Claude Code, Codex Free, Antigravity Free, claude.ai web. Time every step. Record the fallback screenshots |
| Mon | 3 Nov | Slides from the timings; cut what runs 1.5× over |
| Tue | 4 Nov | **Rehearsal 2** with คุณยิ้ม, full 65 minutes with a timer |
| Wed | 5 Nov | Travel; check laptop, adapter, hotspot, offline copies |
| Fri | 6 Nov | 15:05 |

## 5. Decisions for Nat and คุณยิ้ม

1. Is the homework above what the organizer gets (install + `/awaken` + one `/rrr` + link)?
2. Keep the split 20/40, or move to the clock above (คุณยิ้ม 17 + shared opening and Q&A)?
3. Which SME job for the example? Reuse the worked example from คุณยิ้ม's 11:00 workshop, and shrink 15:08 to a bridge (§2b)?
4. The live "where it grows" moment: Discord team, relic5 search, ARRA Memory, or the Oracle app?
5. Hands-on 2 must be tested on Codex and Antigravity: if their sub-agents don't behave the same, that track becomes a demo.
