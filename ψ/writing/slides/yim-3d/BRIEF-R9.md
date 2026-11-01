# Brief round 9 for Osaa: put the Fleet's 14 faces into Yim's deck

From Dobby, 2026-11-01. Yim, verbatim: "เอาส่วน agent 14 ตัวที่เพิ่งทำ เอาไปใส่ slide ที่พูดให้คุณนัทด้วยได้ไหม"
"ส่วน agent 14 ตัวที่เพิ่งทำ" = the contact sheet of 14 agent portraits built today for the productize.life home redesign
(branch feat/home-workbench, `components/sections/showcase.jsx`, screenshot /Users/yim/hello-oracle/ψ/writing/productize-home-redesign/build-b/1920-full.png).
Portraits are already copied to `vendor/fleet/<name>.webp` here (aida daruma dobby fude hako jizo kensa koe kokoro kura mamori osaa ryo sora).
Roles (one short Thai word each; derive from /Users/yim/oracle-products/productize-web-b/lib/agents.js `role`, e.g. dobby ประสานงาน, osaa ภาพ, fude เขียน, koe การตลาด, kensa ตรวจ, mamori ระบบ, kura บัญชี, hako สต็อก, ryo ตลาด, sora อุปกรณ์, daruma product, jizo รับรู้, aida service design, kokoro ปรัชญา).

Do:
- Put the 14 faces where they tell the story best with the least time cost (the talk stays ~9:00). Preferred: on slide 3 "Fleet ของยิ้ม ทำงานกันยังไง" as a contact-sheet strip, each face with its name + one-word role, replacing the top-row 3D formation if needed; or a short dedicated slide right after slide 3 (~30 s) if slide 3 gets crowded. Your call; say why in REPORT.md.
- Fit the Riso look: portraits printed through the riso inks (duotone/dot screen) or framed so colour photos don't fight the paper. Per Yim's rule, faces are a graphic so a screen is allowed; names/roles are text, solid.
- On screen say "สิบกว่าตัว" only if a number appears; 14 faces are fine to show.
- Keep everything else: offline vendor, notes (add a SAY line), no `[—–]`, no "ด่าน", spacing (3D/images clear of rule lines).
Acceptance: checks/r5/shot.py → all slides `[]` at 1920x1080 and 1280x720 (b?.png are gitignored now); look at the slide you changed. REPORT.md in your voice. Don't commit.
