#!/usr/bin/env bash
# fast-remove.sh <worktree-path>... — remove worktrees whose work is already merged AND signed.
# Same steps as herdr-ticket/ship.sh (tombstone -> fleet clean -> git branch -d) but:
#   - fleet clean is scoped with --repo, so it scans ONE repo, not all 1,321 (7 min -> seconds)
#   - a /herdr-pr signature in the PR BODY counts, not only in a comment (ship.sh reads comments only)
#   - a tracked-but-modified .envrc (the token label `maw token use` rewrites) is saved as a patch and restored
#   - ignored data over 50 MB is refused up front with the mv command (fleet clean skips it with no message)
#   - closes the worktree's herdr space(s): agents quit with ctrl-c (transcripts stay), panes closed
#   - `fast-remove.sh --close-spaces <old-path>...` closes the spaces of a worktree that is already gone
# Never: push, merge, force, git branch -D, rm -rf. The remote branch is kept.
set -u

# spaces_of <path>: "<session> <workspace>" for every herdr workspace with a pane whose cwd is inside <path>
spaces_of() {
  local path="$1" s
  for s in $(herdr session list 2>/dev/null | awk 'NR>1 && $2=="running"{print $1}'); do
    herdr --session "$s" pane list 2>/dev/null | python3 -c '
import json,sys
path,s=sys.argv[1],sys.argv[2]; seen=set()
try: panes=json.load(sys.stdin)["result"]["panes"]
except Exception: panes=[]
for p in panes:
    for c in (p.get("cwd"),p.get("foreground_cwd")):
        if c and (c==path or c.startswith(path+"/")) and p["workspace_id"] not in seen:
            seen.add(p["workspace_id"]); print(s,p["workspace_id"])' "$path" "$s"
  done
}
# close_spaces <path>: quit every agent in those spaces (transcripts stay on disk), then close the space
close_spaces() {
  local path="$1" s ws
  spaces_of "$path" | while read -r s ws; do
    herdr --session "$s" pane list 2>/dev/null | python3 -c '
import json,sys
ws=sys.argv[1]
for p in json.load(sys.stdin)["result"]["panes"]:
    if p["workspace_id"]==ws and p.get("agent"): print(p["pane_id"])' "$ws" | while read -r pane; do
      herdr --session "$s" pane send-keys "$pane" C-c >/dev/null 2>&1; sleep 0.3; herdr --session "$s" pane send-keys "$pane" C-c >/dev/null 2>&1
    done
    herdr --session "$s" workspace close "$ws" >/dev/null 2>&1 && echo "ok  closed space $ws (session $s): agents quit, panes closed"
  done
}
tomb="$HOME/.claude/skills/herdr-clean-up-sync/tombstone.py"
T="$HOME/.herdr/tombstones"
rc=0
if [ "${1:-}" = "--close-spaces" ]; then shift; for d in "$@"; do close_spaces "$d"; done; exit 0; fi
for wt in "$@"; do
  wt=$(cd "$wt" 2>/dev/null && pwd -P) || { echo "XX  no such folder: $1"; rc=1; continue; }
  echo "== $wt"
  common=$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir) || { echo "XX  not a git worktree"; rc=1; continue; }
  repo=$(dirname "$common"); name=$(basename "$repo")
  slug=$(git -C "$repo" remote get-url origin | sed -E 's#(git@github.com:|https://github.com/|ssh://git@github.com/)##; s#\.git$##')
  branch=$(git -C "$wt" branch --show-current)
  [ -n "$branch" ] || { echo "XX  detached HEAD"; rc=1; continue; }

  # 1. clean (only .envrc may differ)
  dirty=$(git -C "$wt" status --porcelain -uall | grep -v ' \.envrc$')
  if [ -n "$dirty" ]; then
    echo "XX  uncommitted work:"; echo "$dirty" | head -5 | sed 's/^/      /'
    echo "    commit it, or mv it aside:  mkdir -p $T/$name && mv <file> $T/$name/"; rc=1; continue
  fi
  if git -C "$wt" status --porcelain | grep -q ' \.envrc$'; then
    mkdir -p "$T/$name"; git -C "$wt" diff .envrc > "$T/$name/$(basename "$wt").envrc.patch" 2>/dev/null
    git -C "$wt" checkout -- .envrc && echo "ok  .envrc token label restored (patch in $T/$name/)"
  fi

  # 2. PR merged
  pr=$(gh pr list -R "$slug" --head "$branch" --state all --json number,state,body,headRefOid,comments -q '.[0]' 2>/dev/null)
  if [ -z "$pr" ]; then
    # no PR: fine only when the branch holds nothing main lacks (HEAD already in origin/<default>)
    dflt=$(git -C "$repo" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/main)
    if git -C "$repo" merge-base --is-ancestor "$(git -C "$wt" rev-parse HEAD)" "$dflt" 2>/dev/null; then
      echo "ok  no PR needed: HEAD is already in $dflt (no unique commits)"; n=""; nopr=1
    else echo "XX  no PR for $branch and it has commits $dflt lacks"; echo "    gh pr create -R $slug --head $branch"; rc=1; continue; fi
  else nopr=0
  n=$(printf '%s' "$pr" | python3 -c 'import json,sys;print(json.load(sys.stdin)["number"])')
  state=$(printf '%s' "$pr" | python3 -c 'import json,sys;print(json.load(sys.stdin)["state"])')
  [ "$state" = MERGED ] || { echo "XX  PR #$n is $state, not merged"; rc=1; continue; }
  echo "ok  PR #$n merged"

  # 3. signed: 'herdr:' stanza in the body or any comment
  signed=$(printf '%s' "$pr" | python3 -c '
import json,sys
p=json.load(sys.stdin); t=[p["body"] or ""]+[c["body"] for c in p["comments"]]
print(any("herdr:" in x and "Built by" in x for x in t))')
  [ "$signed" = True ] || { echo "XX  PR #$n has no /herdr-pr signature"
    echo "    ~/.claude/skills/herdr-pr/herdr-sign.sh <model-id> <pane> --work $wt --ref ${branch} | gh pr comment $n -R $slug --body-file -"; rc=1; continue; }
  echo "ok  PR #$n signed"
  fi

  # 4. ignored data over 50 MB would be skipped silently by fleet clean
  big=$(git -C "$wt" status --porcelain --ignored -uall 2>/dev/null | awk '/^!! /{print substr($0,4)}' | while read -r f; do du -sk "$wt/$f" 2>/dev/null; done | awk '$1>51200{print $2" ("int($1/1024)" MB)"}' | head -3)
  if [ -n "$big" ]; then echo "XX  ignored data over 50 MB: $big"
    echo "    mkdir -p $T/$name && mv <path> $T/$name/   (rebuildable? only then rm; log it in $T/RETIRED.md)"; rc=1; continue; fi

  # 5. tombstone -> fleet clean (one repo) -> branch -d
  spaces=$(spaces_of "$wt")
  python3 -I "$tomb" "$wt" --write --reason "${n:+PR #$n merged and signed; }trinity fast path" >/dev/null 2>&1 || { echo "XX  tombstone failed"; rc=1; continue; }
  echo "ok  tombstone written"
  [ -n "$spaces" ] && close_spaces "$wt"   # quit agents + close space FIRST: fleet clean skips a worktree whose agent it cannot quit (omp/codex)
  out=$(cd "$repo" && fleet clean --repo "$slug" --pick "$(basename "$wt")" --tier B,C,D --idle-agents --min-age 0 --go 2>&1 | grep -v '^\[' | tail -3)
  case "$out" in *"removed 1"*"failed 0"*) echo "ok  worktree removed" ;;
    *) echo "XX  fleet did not remove it: $(printf '%s' "$out" | tail -1)"; echo "    cd $repo && fleet clean --repo $slug --pick $(basename "$wt")"; rc=1; continue ;; esac
  git -C "$repo" branch -d "$branch" >/dev/null 2>&1 && echo "ok  local branch $branch deleted (origin keeps it)" \
    || echo "--  branch $branch kept (not merged into its upstream)"
done
exit $rc
