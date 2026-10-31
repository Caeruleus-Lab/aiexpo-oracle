# Skills inventory — m5 and white, 31 Oct 2026

Written by AIExpo Oracle (Oracle AI) for Nat, session `bfe79650`. Nat asked: "/dig --deep all, find about skills, list all and compare, and relic5 too", then "relic5 semantics".

## Counts

| Where | Skills |
|---|---|
| m5, `~/.claude/skills` (beta) | 301 (258 folders, 43 symlinks; plus `herdr-skills.zip` and `VERSION.md`, not skills) |
| m5, Nat's account `~/.claude/skills` | 126 |
| m5, `~/.codex/skills` | 82 (34 exist only here: the omx set — ralph, ralplan, autopilot, ultrawork, deep-interview, team, wiki …) |
| m5, `~/.agents/skills` | 72 |
| m5, plugin skills | 37 (caveman 26, claude-plugins-official 7, openai-codex 3, discord-voice-bot 1) |
| white, `~/.claude/skills` | 129 |
| white, `~/.codex/skills` | 56 |
| white, plugin skills | 75 (anthropic-agent-skills 38, oracle-skills 13, thedotmack 10, caveman 7 …) |

## How the count grew (relic5 semantic search over past sessions)

Earlier inventories, found with relic5 `semantic: true`:

| Date | Count | What was done |
|---|---|---|
| 16 Jan | 60+ | first full search of the skills in a repo |
| 10 Feb | 26 | grouped into "core, keep visible" and the rest (oracle-skills-cli) |
| 13 Mar | 31 | duplicate audit of oracle-skills-cli |
| 5 Apr | 24 | split into tiers (standard: recap, rrr, forward, standup, trace, learn, go …) |
| 14 Apr | 47 | "skill genome" by use on oracle-world: mawjs 19,720, incubate 3,573, learn 3,564 |
| 15 Apr | 44 | three profiles: standard 18, full 25, lab 44 |
| 27 Apr | 95 used | 1,306 calls to 95 skills over 71 days |
| 12 Jun | — | Nat asked the same thing: "list all and compare and list all skills" |
| 22 Aug | 22 | shelf skills; 18 of 22 had no anti-pattern section |
| **31 Oct** | **301** | this file |

Links: `relic5://2026-04/45f3188e6ceee42258682690d66daad4` (genome), `relic5://2026-03/c9f3b5e2761d9a12ff36ff8f81627fb8` (31-skill audit), `relic5://2026-04/d58cee0f00824b1be0823df14bfe805d` (profiles), `relic5://2026-04/f07988eceaebfb309eb6c81a3e3bee59` (usage report), `relic5://2026-08/060fa4af57f7a23ca217a75b2c0f3fb4` (shelf).

Limit found: semantic search does not reach the config layer (SKILL.md files). With `semantic: true, with: config` relic5 answered from conversation text, so a meaning-based grouping of SKILL.md needs keyword search or the local grouping below.

## All 301 skills on m5, grouped by what they do

Grouped by name pattern, then the leftovers placed by hand.

### 1. herdr: panes, worktrees, teams (72)

`claude-twins`, `fleet-burn`, `fleet-layout`, `go-parallel`, `herdr`, `herdr-ask`, `herdr-blank`, `herdr-bring`, `herdr-bring-beside`, `herdr-buddy`, `herdr-clean-up-sync`, `herdr-dissolve`, `herdr-done`, `herdr-fib-wt`, `herdr-finished`, `herdr-handover`, `herdr-hey`, `herdr-idea`, `herdr-incubate`, `herdr-info`, `herdr-issue`, `herdr-lead-scouts`, `herdr-link`, `herdr-link-check`, `herdr-link-local`, `herdr-link-remote`, `herdr-link-talk`, `herdr-link-teardown`, `herdr-machine-labels`, `herdr-move`, `herdr-neighbors`, `herdr-pane-run`, `herdr-peek`, `herdr-pr`, `herdr-promote`, `herdr-rename`, `herdr-room`, `herdr-roomcast`, `herdr-send`, `herdr-sessioncast`, `herdr-sleep`, `herdr-soulcast`, `herdr-structure`, `herdr-team`, `herdr-team-ctl`, `herdr-ticket`, `herdr-tree`, `herdr-trinity`, `herdr-twin`, `herdr-unpromote`, `herdr-vacation`, `herdr-whoami`, `herdr-work`, `herdr-wt`, `herdr-wt-ship`, `isolate-worktree`, `maw-restart`, `maw-teams`, `maw-wake`, `maw-wrapup`, `noah`, `noah-bring`, `orca-cli`, `orca-per-workspace-env`, `pane-shot`, `parallel-wt-issues`, `portal`, `team-check`, `team-up`, `team-wake`, `tile`, `trio`

### 2. Memory and history (38)

`claude-handoff`, `day-diary`, `day-open`, `dig`, `digger`, `done`, `ferry-delta`, `ferry-ledger`, `find-session`, `forward`, `gather`, `handoff`, `huginn`, `jsonl-truth`, `munin`, `odin-seek`, `oracle-ferry`, `oracle-recap-day`, `oracle-resume-recovery`, `peek-and-nudge-every-10m`, `psi`, `ralph-dig`, `recap`, `recap-voice`, `relic-report`, `relic3`, `relic5`, `resonance`, `retro`, `rrr`, `seek`, `session-recap`, `sleipnir`, `time-travel`, `today-repos`, `trace`, `vault-sync`, `where-we-are`

### 3. Oracle identity and family (25)

`about-oracle`, `awaken`, `bud`, `federation-oss`, `federation-talk`, `feel`, `incubate`, `introduce`, `lab-hatch`, `lab-idea`, `lab-team-kit`, `learn`, `oracle-app`, `oracle-arch-map`, `oracle-doctor`, `oracle-enlighten-me`, `oracle-family-scan`, `oracle-lineage-scan`, `oracle-naming`, `oracle-newborn`, `oracle-team`, `philosophy`, `project`, `soul`, `who-are-you`

### 4. Books, writing, Thai voice (44)

`android-port-book`, `app-guide-book`, `atlas-recap-th`, `build-story`, `checklist`, `cover-and-title`, `duang`, `duanju`, `facebook-dom`, `git-story`, `group-digest`, `group-narrative`, `kien-thai`, `kode-thai`, `measured-doc`, `mine-moments`, `nat-pulse`, `nat-technical-kien-thai`, `nat-thai`, `nat-thai-check`, `nat-voice-technical`, `notebook-qa`, `oracle-book-cover`, `oracle-book-latex`, `oracle-booklet`, `oracle-cheatsheet`, `oracle-prose-rhythm`, `oracle-source-book`, `oracle-title-forge`, `oracle-write-complete-book`, `oracle-write-doc-book`, `oracle-write-endgame`, `oracle-write-mini-book`, `oracle-write-mini-book-v2`, `oracle-write-mini-book-v3`, `oracle-write-proof-book`, `oracle-write-proof-book-v2`, `summarize`, `teach`, `teach-from-a-case`, `writing-beats`, `writing-for-agents`, `writing-fragments`, `writing-shape`

### 5. Browser, web, design (16)

`archify`, `artifact-data-card`, `artifact-first-try`, `artifact-paper-brief`, `ascii-diagram`, `browser-tutorial`, `ego-browser`, `ego-ext-reload`, `fb-subscribers-post`, `hallmark`, `imagegen`, `impeccable`, `return`, `shader-to-art`, `slide-deck-qa`, `watch`

### 6. Research, analysis, code (41)

`adversarial-analysis`, `archaeology`, `ask-codex-dispatch-parallel`, `ask-matt`, `check-that-your-measurement-measures-what-you-think`, `code-review`, `codebase-design`, `deep-research-sonnet`, `diagnosing-bugs`, `domain-modeling`, `find-root-cause`, `git-guardrails-claude-code`, `grill-me`, `grill-with-docs`, `grilling`, `hyperresearch`, `implement`, `implement-spec`, `improve-codebase-architecture`, `oracle-deep-research`, `oracle-find-pattern-ship`, `oracle-plan`, `oracle-prism`, `prototype`, `reimplement`, `research`, `resolving-merge-conflicts`, `reverse-engineer-anything`, `round-table`, `scaffold-exercises`, `setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`, `tdd`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`, `wait-what`, `wayfinder`, `wizard`

### 7. AI agents and models (14)

`agent-reach`, `ai-controls-ai`, `codex-lead`, `codex-team-lessons`, `go`, `go-with-the-best-you-can-and-never-stop-when-your-dream-not-done-go-until-finish-without-anyask-or-wait-me`, `hermes-talkback`, `loop-me`, `orchestrate`, `orchestration`, `sonnet`, `sonnet-scout`, `wf-charting`, `wf-peek`

### 8. Machines, infra, ops (35)

`actions-off`, `admin-manual`, `argus-usage-refresh`, `calver`, `cf-billing`, `cf-tunnel-nginx-fanout`, `cpu-check`, `cpu-kill`, `cpu-ram-doctor`, `create-shortcut`, `deploy-index`, `flash`, `geos-display`, `gh-billing`, `gh-reconcile`, `gods-eyes-refresh`, `google-billing`, `issue-tidy`, `jobs-doctor`, `keychain-unlock`, `live-config-install`, `mba`, `migrate-to-shoehorn`, `mqtt-online`, `physical`, `power-display`, `spin-repo`, `statusline-pace`, `swift-lsp-check`, `teardown`, `test-planmode`, `tooltime`, `white`, `wol`, `wss-tunnel`

### 9. Discord, voice, meetings (13)

`discord-deaf`, `discord-fleet`, `discord-room-guest`, `discord-table`, `pet-analyze-meeting`, `pet-find-in-meeting`, `pet-live-meeting`, `pet-meeting-start`, `pet-summarize-meeting`, `reply`, `voice-map`, `voice-meeting-build`, `voice-pulse`

### 10. Other (3)

`bampenpien`, `find-skills`, `yd-odoo`

## Skills that overlap

- Handing off a session: `forward`, `handoff`, `claude-handoff`
- Where are we: `recap`, `where-we-are`, `session-recap`
- Grilling: `grilling`, `grill-me`, `grill-with-docs`
- Orchestration: `orchestrate`, `orchestration`
- History search: `relic3` (frozen since 15 Oct) is replaced by `relic5`
- Research: `research`, `hyperresearch`, `deep-research-sonnet`, `oracle-deep-research`
- Versions kept side by side: `oracle-write-mini-book` v1/v2/v3, `oracle-write-proof-book` v1/v2

## Use (slash commands typed in m5 transcripts, `~/.claude/projects`)

Counted with `rg '<command-name>/…'` over every transcript. Scheduled runs repeat the same command, so `huginn` and `loop` are inflated. Skills that load without a slash command (relic5 via its MCP tools, herdr-pane-run as a CLAUDE.md pattern) are undercounted.

### Top 40 installed skills

| Skill | Times typed |
|---|---|
| `huginn` | 9522 |
| `recap` | 2961 |
| `trace` | 2515 |
| `oracle-family-scan` | 1610 |
| `rrr` | 1446 |
| `codex-lead` | 1379 |
| `sleipnir` | 1223 |
| `peek-and-nudge-every-10m` | 1220 |
| `dig` | 1190 |
| `forward` | 1068 |
| `awaken` | 892 |
| `odin-seek` | 856 |
| `where-we-are` | 744 |
| `cpu-ram-doctor` | 666 |
| `learn` | 644 |
| `project` | 532 |
| `go` | 430 |
| `trio` | 344 |
| `ralph-dig` | 205 |
| `herdr-wt` | 195 |
| `lab-idea` | 151 |
| `wf-peek` | 147 |
| `watch` | 132 |
| `oracle-cheatsheet` | 128 |
| `psi` | 125 |
| `seek` | 108 |
| `argus-usage-refresh` | 102 |
| `find-root-cause` | 99 |
| `oracle-write-complete-book` | 88 |
| `who-are-you` | 87 |
| `oracle-prism` | 85 |
| `ascii-diagram` | 82 |
| `incubate` | 81 |
| `herdr-bring` | 81 |
| `session-recap` | 71 |
| `return` | 71 |
| `impeccable` | 69 |
| `archaeology` | 68 |
| `herdr-pr` | 56 |
| `ego-browser` | 56 |
### Never typed as a command (175 of 301)

`actions-off`, `admin-manual`, `adversarial-analysis`, `agent-reach`, `ai-controls-ai`, `android-port-book`, `archify`, `artifact-data-card`, `artifact-first-try`, `artifact-paper-brief`, `ask-matt`, `build-story`, `cf-tunnel-nginx-fanout`, `check-that-your-measurement-measures-what-you-think`, `checklist`, `claude-handoff`, `claude-twins`, `code-review`, `codebase-design`, `codex-team-lessons`, `cover-and-title`, `deep-research-sonnet`, `deploy-index`, `diagnosing-bugs`, `digger`, `discord-deaf`, `discord-fleet`, `discord-room-guest`, `discord-table`, `domain-modeling`, `duang`, `duanju`, `ego-ext-reload`, `federation-talk`, `feel`, `ferry-ledger`, `find-session`, `flash`, `fleet-burn`, `fleet-layout`, `gather`, `geos-display`, `gh-billing`, `gh-reconcile`, `git-guardrails-claude-code`, `git-story`, `go-parallel`, `gods-eyes-refresh`, `google-billing`, `grill-with-docs`, `group-digest`, `group-narrative`, `handoff`, `herdr-ask`, `herdr-blank`, `herdr-bring-beside`, `herdr-handover`, `herdr-hey`, `herdr-incubate`, `herdr-issue`, `herdr-lead-scouts`, `herdr-link`, `herdr-link-check`, `herdr-link-local`, `herdr-link-remote`, `herdr-link-talk`, `herdr-link-teardown`, `herdr-machine-labels`, `herdr-move`, `herdr-neighbors`, `herdr-peek`, `herdr-promote`, `herdr-roomcast`, `herdr-send`, `herdr-sessioncast`, `herdr-structure`, `herdr-team`, `herdr-twin`, `herdr-unpromote`, `herdr-whoami`, `herdr-wt-ship`, `hermes-talkback`, `hyperresearch`, `imagegen`, `implement`, `implement-spec`, `improve-codebase-architecture`, `introduce`, `issue-tidy`, `jsonl-truth`, `kode-thai`, `lab-team-kit`, `loop-me`, `maw-teams`, `maw-wake`, `mba`, `measured-doc`, `migrate-to-shoehorn`, `mqtt-online`, `munin`, `nat-technical-kien-thai`, `nat-thai`, `nat-thai-check`, `nat-voice-technical`, `noah`, `noah-bring`, `notebook-qa`, `oracle-app`, `oracle-book-latex`, `oracle-doctor`, `oracle-ferry`, `oracle-find-pattern-ship`, `oracle-lineage-scan`, `oracle-naming`, `oracle-newborn`, `oracle-prose-rhythm`, `oracle-recap-day`, `oracle-source-book`, `oracle-write-doc-book`, `oracle-write-endgame`, `orca-cli`, `orca-per-workspace-env`, `orchestrate`, `orchestration`, `pane-shot`, `parallel-wt-issues`, `pet-analyze-meeting`, `pet-find-in-meeting`, `pet-live-meeting`, `pet-meeting-start`, `pet-summarize-meeting`, `portal`, `power-display`, `prototype`, `recap-voice`, `reimplement`, `relic-report`, `reply`, `research`, `resolving-merge-conflicts`, `reverse-engineer-anything`, `round-table`, `scaffold-exercises`, `setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`, `shader-to-art`, `slide-deck-qa`, `sonnet-scout`, `spin-repo`, `statusline-pace`, `swift-lsp-check`, `tdd`, `teach`, `team-check`, `team-wake`, `test-planmode`, `to-questionnaire`, `to-spec`, `to-tickets`, `today-repos`, `tooltime`, `triage`, `vault-sync`, `voice-map`, `voice-meeting-build`, `wait-what`, `white`, `wizard`, `wol`, `writing-beats`, `writing-for-agents`, `writing-fragments`, `writing-shape`, `wss-tunnel`

## m5 against white (`~/.claude/skills`)

239 skills are only on m5, mostly this month's herdr, relic and book skills. Of the 12 most used on m5, white lacks `huginn`, `codex-lead`, `sleipnir` and `odin-seek`.

On both (62): `about-oracle`, `awaken`, `bampenpien`, `bud`, `calver`, `create-shortcut`, `dig`, `discord-fleet`, `domain-modeling`, `federation-talk`, `feel`, `find-root-cause`, `fleet-layout`, `forward`, `go`, `grill-me`, `grill-with-docs`, `grilling`, `herdr`, `herdr-blank`, `herdr-bring`, `herdr-buddy`, `herdr-done`, `herdr-handover`, `herdr-hey`, `herdr-idea`, `herdr-incubate`, `herdr-neighbors`, `herdr-pane-run`, `herdr-peek`, `herdr-pr`, `herdr-team-ctl`, `herdr-ticket`, `herdr-wt`, `impeccable`, `incubate`, `learn`, `mine-moments`, `nat-voice-technical`, `oracle-booklet`, `oracle-cheatsheet`, `oracle-family-scan`, `oracle-prism`, `oracle-title-forge`, `oracle-write-complete-book`, `pane-shot`, `philosophy`, `portal`, `project`, `recap`, `resonance`, `reverse-engineer-anything`, `rrr`, `seek`, `team-check`, `team-wake`, `time-travel`, `trace`, `vault-sync`, `watch`, `where-we-are`, `who-are-you`

Only on white (67): `VERSION.md`, `add-collab`, `arra-cookbook`, `auto-retrospective`, `bud-index`, `bud-test`, `codex-team`, `coding-to-see-the-truth`, `contacts`, `create-a-plan-and-give-me-full-path-of-the-plan`, `deep-analyse`, `dev-browser`, `discord-timeline`, `do-not-change-the-previous`, `do-not-implement`, `dream`, `evolution`, `find-group`, `fleet`, `fleet-radar`, `forward-lite`, `fyi`, `give-me-full-path-of-the-plan`, `harden`, `hey`, `i-believed`, `i-dont-like-this`, `i-have-new-idea`, `inbox`, `ladder`, `list-group`, `machines`, `mailbox`, `memory`, `mids-update-and-timeline-and-my-works`, `morpheus`, `my-works`, `oracle-combine-blogs`, `oracle-soul-sync-update`, `psi-sync`, `read-group`, `recap-lite`, `release`, `room-wt`, `rrr-lite`, `schedule`, `skills-list`, `standup`, `sunday-workshop`, `talk-to`, `team-agents`, `this-is-the-correct-way`, `this-wrong`, `vault`, `verification-gate-fail-closed`, `very-cool`, `warp`, `what-is-the-current`, `what-you-think`, `what-you-understand`, `whats-next`, `why-you-did-cool-correct-but-the-previous-you-go-with-me-a-lot`, `work-with`, `workshop-bundle`, `worktree`, `wormhole`, `xray`

Nat's account on m5 has 13 that beta's lacks: `codex-team`, `contacts`, `dream`, `fleet-radar`, `fyi`, `hey`, `oracle-combine-blogs`, `oracle-write-complete-book copy` (a folder with a space in its name), `schedule`, `skill-creator`, `talk-to`, `team-agents`, `verification-gate-fail-closed`.

## Made this month (October)

From relic5's git layer (commits since 1 Oct) and the birth time of each SKILL.md. Reinstalls on 3 Oct (`rrr`, `recap`, `forward`, `trace`, `go`, `soul` …) are not counted as new.

- Global, m5 (about 60): about 40 `herdr-*`; `cf-billing`, `gh-billing`, `google-billing`; five `pet-*-meeting`; `relic3`, `jsonl-truth`, `relic-report`, `relic5`; `oracle-write-doc-book`, `oracle-write-proof-book` (+v2), `android-port-book`, `app-guide-book`; `team-wake`, `team-check`, `discord-fleet`, `fleet-layout`, `discord-deaf`; `find-root-cause`, `geos-display`, `gods-eyes-refresh`, `pane-shot`, `portal`, `voice-map`, `isolate-worktree` and others.
- In repos: `herdr-work` (neo, 13 Oct), `dakanda-product-post` (dakanda, 14 Oct), `fm17-deck` (DustBoy-Phd, 15 Oct), `fleet-layout` (laris-co-team, 17 Oct), `geos-display` (oracle-gods-eys-os, 22 Oct), `jsonl-truth` (neo lab, 22 Oct), `pym-docs` (pym-oracle, 27 Oct), `groq-models` and `summarize` (arkkra-team, 29 Oct), `pane-shot` (laris-team, 29 Oct), `ego-lite-install` (aiexpo-oracle, 30 Oct), maw pos skill (pos-oracle, 31 Oct).
- White's own: `impeccable`, `room-wt` (12 Oct), `discord-timeline` (22 Oct).

## Options for Nat

1. Copy the most-used m5 skills that white lacks (`huginn`, `codex-lead`, `sleipnir`, `odin-seek`).
2. Merge or retire the overlapping skills listed above.
3. Move `herdr-skills.zip` and `VERSION.md` out of `~/.claude/skills`.
4. Review the never-typed list before retiring anything; some are used without a slash command.

## Sources

- `/dig --deep` over every `~/.claude/projects*` root on m5: 104,033 sessions (50,512 main), 3 min.
- `ls` of each skills folder on m5 and on white (`nat@white` over tailscale).
- relic5 trace chain `a7407beaa2` (keyword, git and semantic searches, two found notes).
