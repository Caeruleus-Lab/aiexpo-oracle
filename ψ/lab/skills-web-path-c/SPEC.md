# skills-web-path-c: spec

Lesson 01, section 6 (claude.ai path C) offers the 28 Oracle skill ZIPs; the source is
`ψ/writing/books/2026-10-30_claude-chatgpt-install-guide/` on branch `ego-lite-guide-aiexpo-30oct-fri2026`.

## Why it exists

Measured on m5, 2026-10-31:

| Fact | Number |
|---|---|
| ZIPs shipped | 28, all pass claude.ai Upload preview (`captures/13-claude-ai-preview-28.txt`) |
| ZIPs really uploaded + run in a chat | 0 of 27 new (only `awaken`, 23 Aug) |
| Skills with zero local deps (claude/bun/maw/gh/git/py/jsonl/ψ refs in SKILL.md) | 2: oracle-prism, where-we-are |
| Heaviest | incubate git 123 · ψ 71; bud maw 21; oracle-family-scan bun 19 |
| Skills the workshop deck uses | 3: /awaken, /rrr, /recap (deck.html lines 199-346) |

**A beginner on path C sees 28 rows with no "works on web" marker, can upload `dig` or `bud`, and
gets a skill that fails in the sandbox** (no `~/.claude/projects`, no `maw`). Root: the upstream
SKILL.md files assume a local agent host; ZIPping copies that assumption. So web compatibility is a
first-class column driven by measured deps, not a footnote.

## Non-goals

- **Not patching SKILL.md text.** Upstream arra-oracle-skills owns it; a web mode belongs there.
- **Not uploading to Nat's account without his yes.** Preview only, until he says go.
- **Not touching deck.html.** The left pane owns the deck; we only align wording.

## Decisions

**Start-here box with 3 skills (awaken, rrr, recap)**: matches the deck demo exactly.
Consequence: `forward` drops out of the box though it has 867 uses; it stays in the beginner tier.

**One manifest `skills/skills.json` drives ZIPs, README tables and the web matrix** with tier, th/en
text, uses, measured deps, web = ok | partial | local.
Consequence: README section 6 skills block is generated between markers; hand edits there get overwritten.

**The cool part: a dependency heatmap on the web page** (Nat 31 Oct "bring the cool in!" on the
terminal matrix): skills × deps grid, cell brightness = count, web badge, tier filter.
GitHub README keeps a plain table with ✓ ◐ ✗.

**Web verdict is set by hand in build_skills.py, with the measured deps beside it as evidence.**
A formula failed: `awaken` has 1 `.jsonl` ref yet runs on the web (memory lost next chat).
Result: ok 6, partial 13, local 9.
Consequence: `awaken` reads partial (ψ lost next chat), correct, not a bug. Counts in skills.json use
re.findall (occurrences), so incubate git = 137, not the 123 from `rg -c` (lines). Both are right.

## Deferred: real upload test

Plausible that scripts block the security scan. **Test**: upload `oracle-prism` (ok) and `recap`
(partial), run each once, then delete. Needs Nat's yes.

---
DNA lenses: root-cause + prism (design preset: User, Maintainer, Breaker, Simplifier, Integrator) · ⚠️ DEGRADED: single-context, --quick from prior analysis · 2026-10-31
