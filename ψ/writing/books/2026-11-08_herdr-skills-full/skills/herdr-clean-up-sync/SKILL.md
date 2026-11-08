---
name: herdr-clean-up-sync
description: "Old name: merged into /herdr-dissolve on 2026-10-29. Use /herdr-dissolve --sweep (whole-machine cleanup) or /herdr-dissolve --sync (fast-forward checkouts that are behind); this entry only redirects."
---

# /herdr-clean-up-sync: merged into /herdr-dissolve

On 2026-10-29 Nat asked to merge this skill and `/herdr-dissolve` into one. Read
`~/.claude/skills/herdr-dissolve/SKILL.md` and use:

- `/herdr-dissolve --sweep [--host H]` for what this skill did: audit the whole machine, show
  the plan, ask, remove finished worktrees and close ✓ agents, then the sync plan.
- `/herdr-dissolve --sync [--all]` for fast-forwards alone.

The same `fleet audit / clean / sync` commands, tiers, tombstones and traps are all in the
merged skill. `tombstone.py` moved to `../herdr-dissolve/tombstone.py`; the symlink here
keeps old paths working. Nothing was deleted: the previous text of this skill is in
`SKILL.md.bak-20261029-merged-into-dissolve`.
