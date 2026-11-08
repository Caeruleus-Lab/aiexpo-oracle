#!/usr/bin/env zsh
# Run every command the book will show, for real, and keep what it printed.
# Each capture: captures/NN-slug.txt = "$ <shown command>" + output + "(exit N · T s)".
# The .txt files are the book's evidence: writers quote them, reviewers check against them,
# and cards.py renders them to images/NN-slug.png. Anything the book will claim — a number,
# a source file, a directory listing — gets a capture, or a reviewer will call it invented.
#
# Edit the CONFIG and the COMMANDS section, then run it in a herdr pane (it can be slow):
#   herdr pane run <PANE> "zsh capture.sh; RC=\$?; herdr agent prompt <AGENT> \"captures rc=\$RC\""
setopt pipefail
B=${0:A:h}; C=$B/captures; mkdir -p $C

# ── CONFIG ──────────────────────────────────────────────────────────────────
TOOL=herdr                               # the name printed after "$ " in every capture
TOOLCMD=(herdr)
WORKDIR=/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle
TIMEOUT=180

# run NN slug -- args...          → "$ TOOL args"   (runs TOOLCMD args)
run() {
  local nn=$1 slug=$2; shift 3
  local f=$C/$nn-$slug.txt t0=$(date +%s.%N)
  print -r -- "$ $TOOL $*" > $f
  (cd $WORKDIR && timeout $TIMEOUT $TOOLCMD "$@") >> $f 2>&1; local rc=$?
  printf '(exit %d · %.1f s)\n' $rc $(( $(date +%s.%N) - t0 )) >> $f
  printf '%s %-28s exit %d  %4d lines\n' $nn $slug $rc $(wc -l < $f)
}
# runsh NN slug "shown command" "shell command"   → for pipes, ssh, servers, cat of a source file
runsh() {
  local nn=$1 slug=$2 disp=$3 cmd=$4
  local f=$C/$nn-$slug.txt t0=$(date +%s.%N)
  print -r -- "$ $disp" > $f
  (cd $WORKDIR && timeout $TIMEOUT zsh -c "$cmd") >> $f 2>&1; local rc=$?
  printf '(exit %d · %.1f s)\n' $rc $(( $(date +%s.%N) - t0 )) >> $f
  printf '%s %-28s exit %d  %4d lines\n' $nn $slug $rc $(wc -l < $f)
}

date '+== capture start %H:%M:%S'
$TOOLCMD --help > $C/00-help.txt 2>&1      # the help text: reviewers check every flag against it

# ── COMMANDS (read-only; the 4 skills are never run for real here) ──────────
SK=$HOME/.claude/skills
# ch1 what the four are
run 01 version -- --version
runsh 02 skill-sizes "wc -l ~/.claude/skills/herdr-{wt,bring,pr,dissolve}/SKILL.md" "wc -l $SK/herdr-{wt,bring,pr,dissolve}/SKILL.md | sed 's|$HOME|~|'"
runsh 03 skill-descriptions "rg -m1 '^description:' ~/.claude/skills/herdr-{wt,bring,pr,dissolve}/SKILL.md | cut -c1-300" "for s in wt bring pr dissolve; do printf '%s: ' herdr-\$s; rg -m1 '^description:' $SK/herdr-\$s/SKILL.md | cut -c14-300; done"
runsh 04 worktree-list "git worktree list" "git worktree list"
# ch2 /herdr-wt
runsh 10 wt-naming "sed -n (naming section) ~/.claude/skills/herdr-wt/SKILL.md" "rg -n -i 'slug.*oracle.*date|<slug>-<oracle>-<date>' $SK/herdr-wt/SKILL.md | head -12"
runsh 11 wt-steps "rg '^#+ ' ~/.claude/skills/herdr-wt/SKILL.md" "rg -n '^#+ ' $SK/herdr-wt/SKILL.md | head -40"
runsh 12 issue-129 "gh issue view 129 --repo laris-co/laris-team" "gh issue view 129 --repo laris-co/laris-team | sed -n '1,60p'"
runsh 13 issue-129-comments "gh issue view 129 --repo laris-co/laris-team --comments | tail -40" "gh issue view 129 --repo laris-co/laris-team --comments | tail -40"
runsh 14 aiexpo-wt-branches "git branch -a | rg 'aiexpo|issue|soul'" "git branch -a | rg 'aiexpo|issue|soul|notion'"
# ch3 /herdr-bring
runsh 20 bring-steps "rg '^#+ ' ~/.claude/skills/herdr-bring/SKILL.md" "rg -n '^#+ ' $SK/herdr-bring/SKILL.md | head -40"
runsh 21 maw-locate-neo "maw locate neo" "maw locate neo 2>&1 | head -20"
runsh 22 maw-locate-aiexpo "maw locate aiexpo" "maw locate aiexpo 2>&1 | head -20"
runsh 23 bring-rules "rg -n -i 'kill|resume|never' ~/.claude/skills/herdr-bring/SKILL.md | head -20" "rg -n -i 'kill|resume|never' $SK/herdr-bring/SKILL.md | head -20"
# ch4 /herdr-pr
runsh 30 sign-help "herdr-sign.sh --help" "bash $SK/herdr-pr/herdr-sign.sh --help"
runsh 31 sign-this-pane "herdr-sign.sh claude-opus-5-5 wCM:p1" "bash $SK/herdr-pr/herdr-sign.sh claude-opus-5-5 wCM:p1"
runsh 32 pr-130-built-by "gh pr view 130 --repo laris-co/laris-team --comments | rg -A32 'Built by' | head -40" "gh pr view 130 --repo laris-co/laris-team --comments | rg -A32 'Built by' | head -40"
runsh 33 pr-7-signed "gh pr view 7 --comments | rg -A30 'Built by' | head -36" "gh pr view 7 --repo Caeruleus-Lab/aiexpo-oracle --comments | rg -A30 'Built by' | head -36"
runsh 34 pr-7-times "gh pr view 7 --json createdAt,mergedAt,headRefName,title" "gh pr view 7 --repo Caeruleus-Lab/aiexpo-oracle --json number,title,headRefName,createdAt,mergedAt"
# ch5 /herdr-dissolve
runsh 40 dissolve-modes "rg -n 'self|--sweep|--all-but-me|--sync' ~/.claude/skills/herdr-dissolve/SKILL.md | sed 1d | head -10" "rg -n -e '--sweep' -e '--all-but-me' -e '--sync' -e 'self' $SK/herdr-dissolve/SKILL.md | head -24"
runsh 41 tombstone-help "tombstone.py" "python3 $SK/herdr-dissolve/tombstone.py; true"
runsh 42 tombstone-dry-run "tombstone.py wt/calliope-oracle-soul --reason 'book demo, dry run'" "python3 $SK/herdr-dissolve/tombstone.py wt/calliope-oracle-soul --reason 'book demo, dry run'"
runsh 43 tombstone-issue3 "cat ψ/memory/tombstones/2026-11-08_workshop-for-ai-aiexpo-issue3-30oct-fri2026.md" "cat 'ψ/memory/tombstones/2026-11-08_workshop-for-ai-aiexpo-issue3-30oct-fri2026.md'"
runsh 44 tombstone-demo129 "cat ~/.herdr/tombstones/laris-team/2026-11-03_demo-hello-world-laris-team-issue129-3nov-tue2026.md" "cat $HOME/.herdr/tombstones/laris-team/2026-11-03_demo-hello-world-laris-team-issue129-3nov-tue2026.md 2>&1 | head -40"
runsh 45 tombstones-dir "ls ~/.herdr/tombstones/laris-team | tail -12" "ls $HOME/.herdr/tombstones/laris-team | tail -12; ls $HOME/.herdr/tombstones/laris-team | wc -l"

# ch3 story of 3 Nov (relic5 log saved by the bring/promote lesson)
runsh 24 relic5-neo-3nov "cat ../2026-11-08_herdr-bring-promote/captures/relic5-session-51fdd0de.txt" "cat ψ/writing/books/2026-11-08_herdr-bring-promote/captures/relic5-session-51fdd0de.txt"
runsh 15 relic5-wt-3nov "cat ../2026-11-08_herdr-wt-lifecycle/captures/01-relic5-timeline.txt" "cat ψ/writing/books/2026-11-08_herdr-wt-lifecycle/captures/01-relic5-timeline.txt"
# ch6 inside the scripts
runsh 60 sign-visibility "sed -n 205,222p ~/.claude/skills/herdr-pr/herdr-sign.sh" "sed -n 205,222p $SK/herdr-pr/herdr-sign.sh"
runsh 61 sign-private-fields "sed -n 266,285p ~/.claude/skills/herdr-pr/herdr-sign.sh" "sed -n 266,285p $SK/herdr-pr/herdr-sign.sh"
runsh 62 tombstone-refuse "sed -n 18,40p ~/.claude/skills/herdr-dissolve/tombstone.py" "sed -n 18,40p $SK/herdr-dissolve/tombstone.py"
runsh 63 tombstone-write "rg -n 'write|exists|never' ~/.claude/skills/herdr-dissolve/tombstone.py" "rg -n 'write|exists|never|overwrite' $SK/herdr-dissolve/tombstone.py"
runsh 64 wt-step0 "rg -n -A12 '^## Step 0' ~/.claude/skills/herdr-wt/SKILL.md" "rg -n -A14 '^#+ Step 0' $SK/herdr-wt/SKILL.md | head -30"
runsh 65 dissolve-ask "rg -n -i 'ask|confirm|never close' ~/.claude/skills/herdr-dissolve/SKILL.md | head -16" "rg -n -i 'ask|confirm|never close|plan' $SK/herdr-dissolve/SKILL.md | head -16"
runsh 66 tombstone-refuse-main "tombstone.py . (the main checkout)" "python3 $SK/herdr-dissolve/tombstone.py .; true"
# ch7 traps, evidence
runsh 70 pr-130-merged "gh pr view 130 --repo laris-co/laris-team --json number,mergedAt,mergeCommit,headRefName" "gh pr view 130 --repo laris-co/laris-team --json number,mergedAt,mergeCommit,headRefName"
runsh 71 issue3-dist-tgz "ls -lh ~/.herdr/tombstones/aiexpo-oracle/" "ls -lh $HOME/.herdr/tombstones/aiexpo-oracle/ | sed 's|$HOME|~|'"

date '+== capture end %H:%M:%S'
ls $C | wc -l
