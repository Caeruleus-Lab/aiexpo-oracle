#!/usr/bin/env bash
# ship.sh — finish a worktree from the CLI: sign its merged PR, write the tombstone, remove the worktree, delete the
# local branch. A plan until --go. The oracle apps' Work page is meant to run this (oracle-app-kit issue #115).
#
#   ship.sh done <worktree>... [--idle-agents] [--go]
#
# Per worktree, stopping at the first thing that is not true:
#   clean → PR merged (or HEAD already in the default branch) → no working agent → signed with the landed sha
#   → tombstone → fleet clean (its own guards) → git branch -d.
# Never: git add -A, push, merge, git branch -D, rm -rf. The remote branch is kept.
# Signing is asked of the worktree's OWN session (ticket.sh continue) and is asynchronous, so the row stops at
# "signing requested"; run the same command again once the comment exists. No sleep, no polling.
set -uo pipefail
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
tomb="$HOME/.claude/skills/herdr-clean-up-sync/tombstone.py"

row_ok() { printf '  ok  %s\n' "$*"; }
row_no() { printf '  XX  %s\n' "$1"; shift; for c in "$@"; do printf '      %s\n' "$c"; done; }
usage() { sed -n '2,13p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

cmd=${1:-}; [ $# -gt 0 ] && shift
case "$cmd" in done) ;; -h|--help|help|"") usage; exit 0 ;; *) usage >&2; exit 2 ;; esac
GO=0 IDLE=0 WTS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --go) GO=1; shift ;;
    --idle-agents) IDLE=1; shift ;;
    -*) printf '✗ unknown flag %s\n  bash %s --help\n' "$1" "$here/ship.sh" >&2; exit 2 ;;
    *) WTS+=("$1"); shift ;;
  esac
done
[ ${#WTS[@]} -gt 0 ] || { printf '✗ done needs a worktree path\n  bash %s done /path/to/worktree\n' "$here/ship.sh" >&2; exit 2; }
for t in git gh herdr jq python3 fleet; do command -v "$t" >/dev/null || { printf '✗ %s is not on PATH\n  command -v %s\n' "$t" "$t" >&2; exit 2; }; done

live_in() { # $1 = worktree → "<herdr-session> <pane> <status>" per agent whose cwd is inside it, across every running server
  local s
  for s in $(herdr session list 2>/dev/null | awk 'NR > 1 && $2 == "running" { print $1 }'); do
    herdr --session "$s" agent list 2>/dev/null | jq -r --arg s "$s" --arg d "$1" \
      '.result.agents[]? | select((.cwd // "") == $d or ((.cwd // "") | startswith($d + "/"))) | "\($s) \(.pane_id) \(.agent_status)"'
  done
}

done_one() {
  local wt gcd repo branch head slug dflt dirty pr n state pr_head merge landed live ls lp lst reason bodies out
  wt=$(cd "$1" 2>/dev/null && pwd -P) || { printf '%s\n' "$1"; row_no "no such folder" "git worktree prune"; return 1; }
  printf '%s\n' "$wt"
  gcd=$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || { row_no "not a git worktree"; return 1; }
  repo=$(dirname "$gcd")
  [ "$wt" = "$(cd "$repo" && pwd -P)" ] && { row_no "this is the main checkout, not a worktree"; return 1; }
  branch=$(git -C "$wt" branch --show-current); head=$(git -C "$wt" rev-parse HEAD)
  [ -n "$branch" ] || { row_no "detached HEAD: no branch to finish" "git -C $wt log --oneline -3"; return 1; }
  slug=$(git -C "$repo" remote get-url origin 2>/dev/null | sed -E 's#^.*github\.com[:/]##; s#\.git$##')
  [ -n "$slug" ] || { row_no "$repo has no origin remote" "git -C $repo remote -v"; return 1; }
  git -C "$repo" fetch -q origin 2>/dev/null || printf '      (fetch failed: judging by the last fetch)\n'
  dflt=$(git -C "$repo" symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)

  dirty=$(git -C "$wt" status --porcelain | grep -Ev ' (\.envrc|\.DS_Store)$' || true)
  if [ -n "$dirty" ]; then row_no "uncommitted: $(printf '%s\n' "$dirty" | wc -l | tr -d ' ') files" "git -C $wt status --short"; return 1; fi
  row_ok "clean"

  pr=$(gh pr list -R "$slug" --head "$branch" --state all --limit 1 --json number,state,headRefOid,mergeCommit --jq '.[0] // empty' 2>/dev/null || true)
  n=$(jq -r '.number // empty' <<<"${pr:-{\}}"); state=$(jq -r '.state // empty' <<<"${pr:-{\}}")
  pr_head=$(jq -r '.headRefOid // empty' <<<"${pr:-{\}}"); merge=$(jq -r '.mergeCommit.oid // empty' <<<"${pr:-{\}}")
  if [ "$state" = MERGED ]; then
    if [ "$pr_head" != "$head" ] && ! git -C "$repo" merge-base --is-ancestor "$head" "$dflt" 2>/dev/null; then
      row_no "commits landed after PR #$n merged and are not in $dflt" "gh pr create -R $slug --head $branch   # ship them first"; return 1
    fi
    row_ok "PR #$n merged"; reason="merged PR #$n"
  elif git -C "$repo" merge-base --is-ancestor "$head" "$dflt" 2>/dev/null; then
    row_ok "HEAD is already in $dflt"; state=INMAIN; reason="commits are in $dflt"
  else
    row_no "not merged (${state:-no PR})" "gh pr create -R $slug --head $branch"; return 1
  fi

  live=$(live_in "$wt")
  if [ -n "$live" ]; then
    read -r ls lp lst <<<"$(printf '%s\n' "$live" | head -1)"
    case "$lst" in working|blocked) row_no "agent $lst in $ls:$lp" "herdr --session $ls pane read $lp --source recent-unwrapped --lines 30"; return 1 ;; esac
    if [ "$IDLE" = 0 ]; then
      row_no "agent $lst in $ls:$lp: read it first, it may be waiting on a question" \
        "herdr --session $ls pane read $lp --source recent-unwrapped --lines 40 | tail -12" "bash $here/ship.sh done $wt --idle-agents"; return 1
    fi
    row_ok "agent $lst in $ls:$lp will be quit by fleet clean"
  else row_ok "no agent"; fi

  if [ "$state" = MERGED ]; then
    landed=${merge:0:7}   # herdr-sign prints 7-char shas
    bodies=$(gh api "repos/$slug/issues/$n/comments" --paginate --jq '.[].body' 2>/dev/null || true)
    # a signature must cite a commit that is on the default branch: the landed merge sha, or (for a plain merge commit,
    # where the PR's own commits survive) the PR head sha
    cites=""
    if printf '%s' "$bodies" | grep -q 'herdr:'; then
      [ -n "$landed" ] && printf '%s' "$bodies" | grep -q "$landed" && cites=$landed
      [ -z "$cites" ] && [ -n "$pr_head" ] && git -C "$repo" merge-base --is-ancestor "$pr_head" "$dflt" 2>/dev/null \
        && printf '%s' "$bodies" | grep -q "${pr_head:0:7}" && cites=${pr_head:0:7}
    fi
    if [ -n "$cites" ]; then
      row_ok "signed, citing $cites (on $dflt)"
    elif [ "$GO" = 1 ]; then
      out=$(bash "$here/ticket.sh" continue "$wt" --repo "$repo" "/herdr-pr: sign PR #$n of $slug now. It merged as $merge, so sign with --ref $merge. Reply when the comment is posted." 2>&1) \
        && { row_no "signing requested of the worktree's own session; run this again once the comment exists" "bash $here/ship.sh done $wt$([ "$IDLE" = 1 ] && echo " --idle-agents") --go"; return 1; } \
        || { row_no "could not ask the session to sign: $(printf '%s' "$out" | tail -1)" "herdr-sign.sh <model-id> --work $wt --ref $merge | gh pr comment $n -R $slug --body-file -"; return 1; }
    else
      row_no "PR #$n has no signature citing $landed" "would ask the worktree's own session: ticket.sh continue $wt \"/herdr-pr …\""; return 1
    fi
  fi

  out=$(cd "$repo" && fleet clean --repo "$slug" --pick "$wt" $([ "$IDLE" = 1 ] && echo --idle-agents) 2>&1 | grep -F "$wt" | grep -v 'not picked' | head -2)
  case "$out" in
    *would*) printf '      fleet: %s\n' "$(printf '%s' "$out" | head -1 | sed 's/  */ /g')" ;;
    *) row_no "fleet would keep it: gitignored data over its 50 MB cap, a lock, or an agent it will not quit" \
         "cd $repo && fleet audit --repo $slug --pick $wt --no-fetch" "du -sh $wt/.tmp/*   # move what you want out, then run this again"; return 1 ;;
  esac
  if [ "$GO" = 0 ]; then row_ok "PLAN  tombstone → fleet clean → git branch -d $branch   (add --go)"; return 0; fi
  python3 -I "$tomb" "$wt" --write --reason "$reason" >/dev/null 2>&1 || { row_no "tombstone failed" "python3 $tomb $wt"; return 1; }
  row_ok "tombstone written"
  out=$(cd "$repo" && fleet clean --repo "$slug" --pick "$wt" $([ "$IDLE" = 1 ] && echo --idle-agents) --go 2>&1 | tail -3)
  case "$out" in *"removed 1"*"failed 0"*) row_ok "worktree removed" ;; *) row_no "fleet did not remove it: $(printf '%s' "$out" | tail -1)" "cd $repo && fleet clean --repo $slug --pick $wt"; return 1 ;; esac
  if git -C "$repo" branch -d "$branch" >/dev/null 2>&1; then row_ok "local branch $branch deleted (origin keeps it)"
  else row_no "kept local branch $branch: git does not call it merged into its upstream" \
        "git -C $repo branch -D $branch   # only if origin/$branch is $head"; fi
  return 0
}

bad=0
for w in "${WTS[@]}"; do done_one "$w" || bad=$((bad + 1)); echo; done
[ "$GO" = 0 ] && echo "plan only: nothing changed. add --go to act."
exit $((bad > 0))
