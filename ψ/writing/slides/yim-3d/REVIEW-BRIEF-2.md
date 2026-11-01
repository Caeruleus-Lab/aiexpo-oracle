Independent review of deck.html (8-slide Thai stage deck, Three.js, for AI Expo 6 Nov 2026, speaker = Yim, a non-engineer PM).
You did not build it. Review as a skeptical reviewer, read-only except for writing REVIEW-CODEX-2.md in this folder.

Check:
1. Stage risk: does it run offline / on a weak projector laptop? What happens if the CDN or WebGL fails? Any console errors? Keyboard nav, N notes.
2. Claims on screen: list every number or factual claim and whether this folder or its sources back it (BRIEF.md, BRIEF-R2.md, ~/hello-oracle/ψ/writing/expo-2026-10/2026-11-01_fleet-facts-for-talk.md). Flag anything unbacked.
3. Readability from the back of a hall: text size, contrast over the 3D, Thai line breaks. Use the screenshots b1.png..b8.png.
4. Story: does each slide support the arc (memory -> bottleneck -> team + ARRA way of working -> fleet -> shift cycle -> results -> "ถ้ายิ้มทำได้ คุณก็ทำได้")? Anything a non-technical audience would not follow?
5. Bugs in the JS (navigation, morph timing, resize, memory leaks over a 10-minute talk).

Output REVIEW-CODEX-2.md: findings ranked by severity, each with slide number, evidence, and a concrete fix. End with a one-line verdict: ship / ship after fixes / not ready.
Acceptance: REVIEW-CODEX-2.md exists and ends with a line starting "Verdict:".

This is a second review after a full restyle (Riso direction, Rikyu type, 8 slides). The first review is REVIEW-CODEX.md; check which of its findings are now fixed and which remain, then new issues. Offline vendor files are in vendor/.
