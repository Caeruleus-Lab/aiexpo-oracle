---
name: herdr-rename
description: Rename the current herdr worktree's branch (the sidebar label) to a meaningful name the AI picks from the session's actual work. With no name given, the AI renames to its best pick first, then shows a popup so the human can keep it or choose another, but only when the human is waiting on the rename. Inside a ticket or wt brief it renames without asking and lists the runner-ups in the final report, so the work and the push never wait on a popup. Default is branch-only (`git branch -m`), which is instant and keeps the session alive. Use when the user says "rename", "rename this branch", "name this worktree", "give it a meaningful name", or the sidebar shows a random name like green-meadow-782b. Do NOT use to create a worktree (use /herdr-wt) or to move the directory (only on explicit ask, see below).
---

# /herdr-rename — AI picks a meaningful branch name

The herdr sidebar row shows the **branch name**. Renaming the branch relabels the row
immediately; the directory and the running session are untouched.

## Steps

1. **Gather evidence** (patterns over intentions — name what the work IS, not what was planned):

   ```bash
   TZ=Asia/Bangkok date '+%-d%b-%a%Y' | tr 'A-Z' 'a-z'      # e.g. 3oct-sat2026
   git branch --show-current
   git log --oneline main..HEAD | head -10
   git status --short | head -10
   ```

   Also use the conversation so far: the topic the user and I actually worked on.

   **Fresh worktree** (right-click → New worktree gives a random name like `green-meadow-782b`,
   no commits, clean tree, no conversation yet): the evidence is the user's task. Use their
   args (`/herdr-rename fix relic fts`) or first prompt as the topic; if there is neither,
   ask "what is this worktree for?" in one line. This is the only case where you ask
   before renaming: with no evidence at all, any name would be a guess.

2. **Draft 3 names** (best first), shape `<topic>-<owner>[-issue<N>]-<d><mon>-<dow><year>` —
   **slug first** (Nat, 2026-10-03; the /herdr-wt rule since 2026-09-20), e.g.
   `office-town-neo-3oct-sat2026`, `register-free-cloud-homelab-issue23-28sep-mon2026`. Rules:
   - `<topic>` 1-3 words, lowercase, hyphens, no slashes (a `/` hides the label prefix).
   - Name the work, not the tool used to do it.
   - `<owner>` comes AFTER the topic: the repo's basename without `-oracle` (`neo` for
     neo-oracle, `homelab` for homelab). Compute it from the MAIN checkout, never from the
     worktree folder or from CLAUDE.md:
     `basename "$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")" | sed 's/-oracle$//'`.
     Measured 2026-10-08: `--show-toplevel` gave `worktree-calm-meadow-eea9` here, and an
     agent in a scratch repo `here-test` wrote `neo` because it read the parent CLAUDE.md. The sidebar groups spaces under their repo and
     truncates from the right, so a leading `neo-` repeats the parent row on every line —
     /herdr-wt measured 3 collisions at 14 visible characters owner-first, 0 slug-first.
   - `-issue<N>` only when a GitHub issue is the brief for this worktree.
   - Check no collision: `git branch --list '<name>'` must be empty. If a draft is taken,
     replace it with another draft. Never reuse a taken name and never add `-2` to it.
   - Older siblings named owner-first (`neo-herdr-14sep-mon2026`) predate the rule; leave
     them unless asked — a branch with an open PR must not be renamed without asking.

   If the user already gave a name, skip the proposal and use it verbatim.

   **No name given: pick one yourself and rename first, then ask** (Nat, 2026-10-08).
   Do not open with a question. Choose the best candidate and apply it right away (step 3),
   so the sidebar gets a real name even if the human ignores the prompt. The name should
   be meaningful AND memorable: a vivid, specific topic (`fts-stopword-purge`,
   `kong-cutover`) beats a generic one (`fix-bug`, `update-stuff`), but never trade
   accuracy for flair. The name must still say what the work is.

3. **Rename**:

   ```bash
   old=$(git branch --show-current)
   git branch -m "$old" <new-name> || { echo "branch rename failed; label left alone"; exit 1; }
   git branch --show-current
   # a /herdr-wt --here pane is labelled with the branch name; keep the label in step.
   # Only reached when the branch rename succeeded.
   P=$(herdr pane current | python3 -c "import json,sys;print(json.load(sys.stdin)['result']['pane']['pane_id'])")
   L=$(herdr pane get "$P" | python3 -c "import json,sys;print(json.load(sys.stdin)['result']['pane'].get('label') or '')")
   if [ "$L" = "$old" ]; then herdr pane rename "$P" <new-name> >/dev/null && echo "label: $old -> <new-name>"
   else echo "label '${L:-none}' is not the old branch name; left alone"; fi
   # the SPACE has its own label, set once at creation (the folder name for a right-click
   # worktree). Apps that list spaces (oracle-app-kit hub, `maw herdr ls` .label) read it,
   # not the branch. Rename it when it is still automatic: old branch or folder name.
   W=$(herdr pane get "$P" | python3 -c "import json,sys;print(json.load(sys.stdin)['result']['pane']['workspace_id'])")
   WL=$(herdr workspace list | python3 -c "import json,sys;w=[x for x in json.load(sys.stdin)['result']['workspaces'] if x['workspace_id']==sys.argv[1]][0];print(w['label'] if (w.get('worktree') or {}).get('is_linked_worktree') else '')" "$W")
   dir=$(basename "$(git rev-parse --show-toplevel)")
   if [ -n "$WL" ] && { [ "$WL" = "$old" ] || [ "$WL" = "$dir" ]; }; then herdr workspace rename "$W" <new-name> >/dev/null && echo "space: $WL -> <new-name>"
   else echo "space label '${WL:-main checkout}' is custom or not a worktree; left alone"; fi
   ```

   Why the space label too: measured 2026-10-09 on `w3M`, after `git branch -m` the herdr
   sidebar showed `neo-understanding` but `herdr workspace list` still had label
   `worktree-lucky-valley-12bc`, and the Neo app showed that. `herdr workspace rename w3M
   neo-understanding` fixed it, with the agent still running. (oracle-app-kit#114 made the
   app's Work row read the branch; its hub space views still read the label.)

   Run this **in the pane of the worktree being renamed**. `--show-current` reads the
   pane's own cwd, so running it from a sibling pane renames the sibling's branch.
   The folder keeps its old name. The lock reason (`tool|who|when|slug[|#issue]`) keeps the
   SLUG that was current at lock time, not the branch name. Both are expected; see
   *Directory rename* below to move the folder.

4. **Let the human veto it — with a popup only when they are waiting on this rename.**

   **Unattended: no popup.** If the rename is one step of a longer job — a `/herdr-ticket`
   or `/herdr-wt` brief, or any flow with more work after it (commits, push, PR) — do NOT
   call AskUserQuestion. A popup there parks finished work unpushed until someone answers
   (Nat, 2026-10-09, issue #157: *"go implement work first then can rename again"*). Rename
   and keep working. In the final report, list the runner-ups as runnable lines so the
   veto costs one command, after the work is done:

   ```
   renamed: <old> -> <new>
   other names: /herdr-rename <runner-up-1>   ·   /herdr-rename <runner-up-2>
   ```

   Briefs say "before your first push" so the remote gets the good name. That still
   holds, but the popup never comes before the push. Renaming again after a push is
   allowed when the human asks for it: push the new branch with `-u`, then repoint the PR
   (`gh pr edit` cannot change the head, so open a new draft PR from the new branch and
   close the old one only with the human's OK). Never delete the old remote branch.

   **Interactive: popup.** When the human typed `/herdr-rename` with no name and nothing
   else is queued after it, call AskUserQuestion once right after the rename:
   - question: `Renamed to <new-name>. Keep it?`
   - option 1: `Keep <new-name> (Recommended)`
   - options 2-3: the two runner-up names, each with a one-line reason in `description`
   - the built-in "Other" lets the human type their own name

   If they pick a runner-up or type a name, rename again (step 3) and run the collision
   check again. Do not ask a second time: the human's choice is final. One exception: if
   the name they TYPED already exists as a branch, say so and ask once more, because
   `git branch -m` refuses it and there is no choice to apply. Skip the popup
   when the human supplied the name.

5. **Report** in one line: old → new, that the sidebar follows the branch, and whether the
   space label was renamed too.

## Directory rename (only if asked)

Moving the dir kills this session's cwd. Say so, then print the exact commands with real paths:

```bash
git -C <main-repo> worktree move <current-dir> <main-repo>/wt/<new-name>
claude --resume   # from the new path
```

## Never

- `git push --force`, `git commit --amend` — rename touches no commits.
- Rename `main` or any branch that has an open PR without asking: the PR is tied to the old
  branch name; renaming the local branch leaves the remote one behind.
