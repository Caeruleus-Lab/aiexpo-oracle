---
pattern: "Where 'Multi-Agent Workflow' came from: Nat's Oct 2025 posts + the code (MAW kit, repo-oracle rules, Shadow label)"
date: 2026-10-30
source: facebook-oracle vault/store posts (Oct 2025), relic5 git + transcripts (traces 54eeeeeaa0, 4c4a44f405, f221f624e3, 58aa8dcff8, 08ec2ee67c), git, gh
concepts: ["aiexpo", "history", "multi-agent", "maw", "oracle", "shadow"]
---

# Multi-Agent Workflow, October 2025 — posts and code

Five independent searches (posts, git by kit name, git by rules words, transcripts by speckit, transcripts by
shadow/repo-oracle) all land on the same three things.

## 1. The code: Multi-Agent Workflow Kit (MAW)

- Repo: `Soul-Brews-Studio/multi-agent-workflow-kit` (fork `laris-co/multi-agent-workflow-kit`, proof repo
  `laris-co/proof-maw-multi-agent-worktree-kit`). First commit 4 Oct 2025 "feat: bootstrap multi-agent workflow
  toolkit"; 250 commits in Oct 2025; tags v0.5.0, v0.5.1.
- Install: `uvx --no-cache --from git+https://github.com/Soul-Brews-Studio/multi-agent-workflow-kit.git@v0.5.1 multi-agent-kit init`,
  then `source .envrc`, `maw attach`.
- Shape: each agent = its own git worktree + branch (`agents/1`, `agents/2`, `agents/3`), all visible in one tmux
  session (profiles 0–5). Config `.agents/agents.yaml`. Scripts `.agents/scripts/` (setup, start-agents, attach,
  hey, send-commands, issue, zoom, remove, kill-all, uninstall). Slash commands `/maw.hey`, `/maw.sync`
  (broadcast to all agents or one), `/maw.zoom`, `/maw.issue`, `/maw.codex`, `/maw.agents-create`.
- 9 Oct: renamed "Multi-Agent Worktree Kit" and back the same day.
- This is the ancestor of today's `maw` CLI and of herdr worktrees (`/herdr-wt`).

## 2. The rules: StoneMeaw/repo-oracle issue #32 (21 Oct 2025)

"Worktree and Multi-Agent Workflow Instructions": never `git checkout main` inside an agent worktree; stay in your
own worktree; use `git -C <path>` for other worktrees; each `agents/N` branch → PR to main
(`gh pr create --base main --head agents/2`). Later issues #38–#41 (22 Oct) hold the "Nat's shadow" session
reports and the official bootstrap command.

## 3. The posts (Nat's Facebook, Oct 2025)

- 21 Oct 09:18 — tried "multi agent worktrees"; without rules the agents still think they share one git and try to
  check out the default branch, so they need boundaries.
- 21 Oct 10:58 — agents from Codex and Claude Code start making rules for each other: proposals go to the Oracle,
  which issues a "constitution". Codex = diligent and square; Sonnet = fast and playful but wrong often — yin and
  yang. Rules: each agent has its own worktree and branch and opens PRs; never cross into another agent's space;
  sync simply with `git -C`; main is the forbidden zone.
- 21 Oct 16:54 — his wife joins: Claude Code on backend, Codex on frontend; next, 2 × 2 agents.
- 22 Oct 06:17 — implemented the **Shadow** idea, simplified: Shadow lives with the Oracle, separated by a label;
  one GitHub, one `gh` command; issues live in the oracle repo with a resident AI.
- 22 Oct 08:13 — "Concept Oracle และ Shadow… works as a team with a team."
- 24 Oct 09:06 — "the world needs Haiku": Speckit + multi-agent with top models felt slow; open with Haiku, implement
  with the strongest models.
- 24 Oct 11:51 — "Multi Agents Workflow has shape… the problems are Speckit and synchronization; agents start
  issuing rules for themselves."
- 25 Oct 13:01 — "measure AI use by how much blows up… like multi agents; go to the edge to bounce back."
- 28 Oct 08:46 — 6–7 months of heavy AI use; months 5–6: "implement Multi Agent Workflow, many vendors at once".
- 25–26 Nov — announces the donation workshop (100% to southern flood relief): "ปั้น AI มาเป็นตัวเรา และ Multi Agent Workflow".

Also in Messenger: 9 Oct 2025 a contact asks whether "multi-agent kit ของนัท" fits a requirement → analysis →
build flow; 26 Dec 2025 another follows "งาน multi-agents ของพี่".

## For the AI Expo deck

The 6 Nov title "ARRA Oracle & Multi-Agent Workflow" is the same pairing Nat posted on 22 Oct 2025: Oracle (memory,
rules) + Shadow + agents in their own worktrees. A slide "one year ago: Oct 2025" could show the 21 Oct rules post
and the agents/1·2·3 tree, then today's herdr room.
