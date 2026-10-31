---
title: "ย้ายร่าง กลางห้อง"
subtitle: "herdr-room ทีละคำสั่ง: ย้าย agent จาก worktree กลับ main แล้วทำไมห้องถึงมี 3 คอลัมน์"
tagline: "ทุกคำสั่งรันจริง ทุกภาพในเล่มคือเทอร์มินัลจริง ยกเว้นภาพปกที่ AI วาด — 2026-10-31"
author: AIExpo Oracle (AI) · กับ Nat
date: 2026-10-31
language: Thai (kien-thai 7 frames) — commands/flags stay English
style: /browser-tutorial — numbered steps, image under the command that produced it
images: every image rendered from text by /ascii-diagram --png (captures/ + diagrams/)
target: 8 chapters + foreword · 42 images · about 45-55 pages
parts: 3
---

## 00 คำนำ — วิธีอ่านเล่มนี้  (images: D1-overview)
- what happened on 31 Oct in one page: old body p3 in course-team/wt, new body p5 in main, 3 columns then 2
- how the book was made: real session laris-co read only; every move replayed in scratch session bookdemo
  with fake agents (pane report-agent); real night read back from two transcripts with timeline.py
- how to read: ch1-3 setup, ch4-6 the move + bug + fix, ch7-8 the real night and what is left
proof: D1-overview, captures 01, 18, 24

## ภาค 1 — ห้อง ร่าง และ herdr

### บทที่ 1: ร่างอยู่ผิดที่  (images: 01-live-room, 02-branches, 03-handoff, 04-charter, 05-session-host)
- 1.1 what the room looks like now (live laris-co, space wCC: p5 main, p4 wt)
- 1.2 the sidebar label is the branch: main vs wt/aiexpo-oracle vs the wt branch
- 1.3 the handoff file the old body wrote: why move, who owns what
- 1.4 the charter in laris-team still says course-team/wt; who owns the session (host larisco-oracle)
proof: captures 01-05

### บทที่ 2: herdr จากข้างนอกเข้าข้างใน  (images: D2-herdr-nesting, 06-sessions, 07-spaces, 08-fake-agents, 09-agents, 10-explain)
- 2.1 session > space (workspace) > tab > pane > agent
- 2.2 a scratch session bookdemo beside the live laris-co: never rehearse on the live room
- 2.3 two spaces with cwd = old body dir and the wt dir
- 2.4 fake agents: pane report-agent + agent rename, so herdr-room treats a plain shell as claude
- 2.5 agent explain: what herdr believes about that pane
proof: captures 06-10

### บทที่ 3: herdr-room — ห้องเดียว หลาย agent  (images: 00-help, 11-room-dry, 12-room-in, 13-room-state, 14-room-list)
- 3.1 the help: in / out / list / rename, members by name, folder, path or pane id
- 3.2 --dry first: 3 planned moves
- 3.3 the real in: pane ids change (w5:p1 -> w7:p1, w6:p1 -> w7:p2), names set again, rects
- 3.4 the state file: room, session, layout, members (path, pane, name), saved
- 3.5 herdr-room list: OPEN vs out rooms, the live laris-co aiexpo-oracle room next to bookdemo
proof: captures 00, 11-14

## ภาค 2 — ย้ายร่าง

### บทที่ 4: ร่างใหม่เกิดใต้ร่างเก่า  (images: 15-real-launch, 16-new-pane, 17-exit-timer)
- 4.1 the real commands of the old body at 20:05:21 and 20:05:45 (UTC in capture: 13:05:21Z / 13:05:45Z)
- 4.2 replay: split down, cwd = main checkout, report-agent -> w7:p3
- 4.3 the old body schedules its own exit (30 s in the replay; 40 s and 20 s timers on the real night)
proof: captures 15-17

### บทที่ 5: ทำไมมี 3 คอลัมน์  (images: 18-room-three, 19-state-three, 20-state-edit, 21-source, D3-room-in-rule)
- 5.1 herdr-room in new + wt -> 3 members, rects 14/14/13 wide
- 5.2 the state file now lists 3, the old path included
- 5.3 editing the state to 2 does nothing: room in rebuilds from the panes inside the space
- 5.4 the source lines 235-250 that do it; D3 explains the rule
- 5.5 "(not an agent: skipped)" on the new pane: the rename step, not the membership
proof: captures 18-21

### บทที่ 6: ทางแก้ — ให้ร่างเก่าออกก่อน  (images: 22-out-dry, 23-old-gone, 24-room-two, 25-state-two)
- 6.1 two ways out: herdr-room out (dry run shows it would also open a worktree space under course-team) or pane close
- 6.2 the replay's old pane closes at 20:15:48; the pane list shows only w7:p3 and w7:p2
- 6.3 room in again -> 2 members, 21/20 wide, names set with no skip
- 6.4 the state and list now agree
proof: captures 22-25

## ภาค 3 — คืนจริง และสิ่งที่ค้าง

### บทที่ 7: คืนจริง และซ้ายคุยขวา  (images: D4-race, 26-night-old, 27-night-new, 28-left-right-rule, D5-left-right, 29-main-log, 30-merge-scan, 35-scan-hits)
- 7.1 the race on the real night, from both transcripts (D4): room in at 20:05:38, before the old body left
- 7.2 the old body's log, the new body's log
- 7.3 the rule: left talks with Nat, right reports; pane ids change, find agents by cwd
- 7.4 a merge, end to end: git log of main, 0 open PRs, the scan (keys, emails, tailnet, local paths)
- 7.5 the scan found 3 local-path lines in an earlier range: read them, they are commands in vault notes
proof: captures 26-30, 35

### บทที่ 8: สิ่งที่ยังค้าง และสูตรย้ายร่าง  (images: 31-live-state, 32-old-dir, 33-larisco, 34-timeline-src, D6-recipe)
- 8.1 the live room state is right: p5 + p4, saved 20:06:05
- 8.2 the old body's directory is still on disk, 0 uncommitted files, no agent
- 8.3 the charter in laris-team still points there; the host LarisCo (w60:p1) owns that fix
- 8.4 timeline.py: how the night was read back from transcripts
- 8.5 the recipe card: 7 steps, step 3 before step 4
proof: captures 31-34, D6-recipe
