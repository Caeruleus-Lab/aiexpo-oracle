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
TOOL=herdr
TOOLCMD=(herdr)
WORKDIR=$B
TIMEOUT=120
S=bookdemo                                            # scratch herdr session, never the live one
MAIN=/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle
WT=$MAIN/wt/workshop-for-ai-aiexpo-issue3-30oct-fri2026
OLD=/opt/Code/github.com/laris-co/course-team/wt/aiexpo-oracle
LT=/opt/Code/github.com/laris-co/laris-team
NEWT=~/.claude/projects/-opt-Code-github-com-Caeruleus-Lab-aiexpo-oracle/2969076e-029b-45c8-9507-fb2158763f97.jsonl
OLDT=~/.claude/projects/-opt-Code-github-com-laris-co-course-team-wt-aiexpo-oracle/89a694ad-4de2-434c-a2c5-0f41f75df38e.jsonl
export S MAIN WT OLD LT NEWT OLDT B
source $B/lib.sh                                      # paneof <cwd> · fake <pane>
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
  [[ -n $ONLY && " $ONLY " != *" $nn "* ]] && return 0      # ONLY="31 32" zsh capture.sh: re-run just those
  local f=$C/$nn-$slug.txt t0=$(date +%s.%N)
  print -r -- "$ $disp" > $f
  (cd $WORKDIR && timeout $TIMEOUT zsh -c "source $B/lib.sh; $cmd") >> $f 2>&1; local rc=$?
  printf '(exit %d · %.1f s)\n' $rc $(( $(date +%s.%N) - t0 )) >> $f
  printf '%s %-28s exit %d  %4d lines\n' $nn $slug $rc $(wc -l < $f)
}

date '+== capture start %H:%M:%S'
[[ -n $ONLY ]] || herdr-room --help > $C/00-help.txt 2>&1

[[ -n $ONLY ]] || {
# reset the scratch session: close every space except the desk, forget the saved room
for w in $(herdr --session $S workspace list | jq -r '.result.workspaces[]|select(.label!="desk")|.workspace_id'); do
  herdr --session $S workspace close $w >/dev/null; done
rm -f ~/.local/state/herdr-room/${S}__aiexpo-oracle.json
}

# ── ch1 the problem, on the live session (read only) ─────────────────────────
runsh 01 live-room "herdr --session laris-co agent list | jq (space wCC)" \
  "herdr --session laris-co agent list | jq -r '.result.agents[]|select(.workspace_id==\"wCC\")|[.pane_id,.name,.agent_status,.cwd]|@tsv'"
runsh 02 branches "git -C <dir> branch --show-current  (main · old body · wt)" \
  "for d in \$MAIN \$OLD \$WT; do printf '%-60s %s\n' \${d#/opt/Code/github.com/} \$(git -C \$d branch --show-current); done"
runsh 03 handoff "sed -n 1,12p <handoff>; rg -n -A1 Charter <handoff>; stat -f %Sm <handoff>" \
  "H=\$MAIN/ψ/inbox/handoff/2026-10-31_20-10_body-back-to-main-checkout.md; sed -n 1,12p \$H; echo; rg -n -A1 Charter \$H; echo; echo last written: \$(stat -f '%Sm' -t '%H:%M:%S' \$H)"
runsh 04 charter "rg -n 'body|aiexpo' oracles/aiexpo-oracle/config.yaml teams/course-team.yaml" \
  "cd \$LT && rg -n 'body|aiexpo' oracles/aiexpo-oracle/config.yaml teams/course-team.yaml"
runsh 05 session-host "sed -n 22,23p CLAUDE.md; cat sessions/laris-co.yaml   (laris-team)" \
  "cd \$LT && sed -n 22,23p CLAUDE.md && echo && cat sessions/laris-co.yaml"

# ── ch2 herdr in a scratch session ───────────────────────────────────────────
runsh 06 sessions "herdr session list | rg 'name|laris-co|bookdemo'" \
  "herdr session list | rg 'name|laris-co |bookdemo' | cut -c1-30"
runsh 07 spaces "herdr --session bookdemo workspace create --cwd <dir> --label <name>  (x2)" \
  "herdr --session \$S workspace create --cwd \$OLD --label old-body --no-focus | jq -c '.result|{space:.workspace.workspace_id,pane:.root_pane.pane_id,label:.workspace.label}'
   herdr --session \$S workspace create --cwd \$WT --label aiexpo-wt --no-focus | jq -c '.result|{space:.workspace.workspace_id,pane:.root_pane.pane_id,label:.workspace.label}'"
runsh 08 fake-agents "herdr pane report-agent <pane> --agent claude --state idle; herdr agent rename" \
  "O=\$(paneof \$OLD); W=\$(paneof \$WT); fake \$O; fake \$W
   herdr --session \$S agent rename \$O aiexpo-oracle | jq -r .result.type
   herdr --session \$S agent rename \$W aiexpo-wt | jq -r .result.type"
runsh 09 agents "herdr --session bookdemo agent list | jq '[pane, name, status, cwd]'" \
  "herdr --session \$S agent list | jq -r '.result.agents[]|[.pane_id,.name,.agent_status,(.cwd|sub(\"/opt/Code/github.com/\";\"\"))]|@tsv'"
runsh 10 explain "herdr --session bookdemo agent explain <old body pane>" \
  "herdr --session \$S agent explain \$(paneof \$OLD)"

# ── ch3 herdr-room ──────────────────────────────────────────────────────────
runsh 11 room-dry "herdr-room in aiexpo-oracle <old> <wt> --layout cols --session bookdemo --dry" \
  "herdr-room in aiexpo-oracle \$(paneof \$OLD) \$(paneof \$WT) --layout cols --session \$S --dry"
runsh 12 room-in "herdr-room in aiexpo-oracle <old> <wt> --layout cols --session bookdemo" \
  "herdr-room in aiexpo-oracle \$(paneof \$OLD) \$(paneof \$WT) --layout cols --session \$S"
runsh 13 room-state "jq . ~/.local/state/herdr-room/bookdemo__aiexpo-oracle.json" \
  "jq . ~/.local/state/herdr-room/\${S}__aiexpo-oracle.json"
runsh 14 room-list "herdr-room list | rg 'bookdemo|laris-co'" "herdr-room list | rg 'bookdemo|laris-co' | cut -c1-96"

# ── ch4 the body moves: split down in the main checkout, old body plans its exit ─
runsh 15 real-launch "python3 (read 89a694ad): the commands that started the new body and closed the old" \
  "python3 - \$OLDT <<'PYX'
import json,sys
for l in open(sys.argv[1]):
    d=json.loads(l)
    if d.get('type')!='assistant': continue
    for c in d['message']['content']:
        if c.get('type')=='tool_use' and c['name']=='Bash' and ('BRIEF=' in c['input']['command'] or c['input']['command'].startswith('nohup sh -c')):
            cmd=c['input']['command']
            print(d['timestamp'], 'UTC')
            for x in cmd.split('\\n'):
                if x.startswith('BRIEF='): x='BRIEF=\"You are AIExpo Oracle, body back in ... Report to Nat in 3 lines, then wait.\"'
                print(x)
PYX"
runsh 16 new-pane "herdr pane split <old> --direction down --cwd \$MAIN; report-agent" \
  "O=\$(paneof \$OLD); N=\$(herdr --session \$S pane split \$O --direction down --cwd \$MAIN --no-focus | jq -r .result.pane.pane_id)
   fake \$N; echo new=\$N; herdr --session \$S pane get \$N | jq -r '.result.pane|[.pane_id,.workspace_id,.cwd]|@tsv'"
runsh 17 exit-timer "(sleep 30; herdr pane close <old>) &   # the old body schedules its own exit" \
  "O=\$(paneof \$OLD); (sleep 30; herdr --session \$S pane close \$O >/dev/null) >/dev/null 2>&1 &!
   echo old=\$O closes at \$(date -v+30S +%H:%M:%S); date +now=%H:%M:%S"

# ── ch5 the bug: room in while the old body is still inside ─────────────────
runsh 18 room-three "herdr-room in aiexpo-oracle <new> <wt> --layout cols --session bookdemo" \
  "herdr-room in aiexpo-oracle \$(paneof \$MAIN) \$(paneof \$WT) --layout cols --session \$S | rg -v '^  run'"
runsh 19 state-three "jq -c '.members[]|[.pane,.name,.path]' <state>" \
  "jq -c '.members[]|[.pane,.name,(.path|sub(\"/opt/Code/github.com/\";\"\"))]' ~/.local/state/herdr-room/\${S}__aiexpo-oracle.json"
runsh 20 state-edit "jq 'drop old from .members' > state; herdr-room in ... again" \
  "f=~/.local/state/herdr-room/\${S}__aiexpo-oracle.json; O=\$(paneof \$OLD)
   jq --arg o \$O '.members |= map(select(.pane!=\$o))' \$f > \$f.tmp && mv \$f.tmp \$f
   echo state now: \$(jq '.members|length' \$f) members
   herdr-room in aiexpo-oracle \$(paneof \$MAIN) \$(paneof \$WT) --layout cols --session \$S | rg 'members|rect'"
runsh 21 source "sed -n 235,250p ~/.local/bin/herdr-room" "sed -n 235,250p ~/.local/bin/herdr-room"

# ── ch6 the fix ─────────────────────────────────────────────────────────────
runsh 22 out-dry "herdr-room out aiexpo-oracle <old> --session bookdemo --dry   (the other way)" \
  "herdr-room out aiexpo-oracle \$(paneof \$OLD) --session \$S --dry"
runsh 23 old-gone "wait for the old body's pane to close, then list the room's panes" \
  "O=\$(paneof \$OLD); while [ \"\$(paneof \$OLD)\" != null ]; do sleep 1; done; date +closed=%H:%M:%S
   herdr --session \$S pane list | jq -r '.result.panes[]|[.pane_id,.workspace_id,(.cwd|sub(\"/opt/Code/github.com/\";\"\"))]|@tsv'"
runsh 24 room-two "herdr-room in aiexpo-oracle <new> <wt> --layout cols --session bookdemo" \
  "herdr-room in aiexpo-oracle \$(paneof \$MAIN) \$(paneof \$WT) --layout cols --session \$S | rg -v '^  run'"
runsh 25 state-two "jq -c '.members[]|[.pane,.name,.path]' <state>; herdr-room list" \
  "jq -c '.members[]|[.pane,.name,(.path|sub(\"/opt/Code/github.com/\";\"\"))]' ~/.local/state/herdr-room/\${S}__aiexpo-oracle.json; herdr-room list | rg bookdemo | cut -c1-96"

# ── ch7 the real night + left/right ─────────────────────────────────────────
runsh 26 night-old "python3 timeline.py <89a694ad, old body> --since 19:54 --until 20:06" \
  "python3 \$B/timeline.py \$OLDT --since 19:54 --until 20:06"
runsh 27 night-new "python3 timeline.py <2969076e, new body> --until 20:07" \
  "python3 \$B/timeline.py \$NEWT --until 20:07"
runsh 28 left-right-rule "rg -n 'left pane|Pane ids change' laris-team/CLAUDE.md" \
  "cd \$LT && rg -n 'left pane|Pane ids change' CLAUDE.md"
runsh 29 main-log "git log --oneline -6 main; gh pr list --state open" \
  "cd \$MAIN && git log --oneline -6 main && echo && echo open PRs: \$(gh pr list -R Caeruleus-Lab/aiexpo-oracle --state open --json number | jq length)"
runsh 30 merge-scan "git diff fd279c7..8a61104 | rg -c <keys|emails|tailnet|local paths>" \
  "cd \$MAIN && for pat in 'sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}' '[A-Za-z0-9._%+-]+@gmail\\.com' '\\.ts\\.net|100\\.(6[4-9]|[7-9][0-9]|1[01][0-9]|12[0-7])\\.[0-9]+\\.[0-9]+' '/Users/beta|/opt/Code'; do
     printf '%-62s %s\n' \"\$pat\" \$(git diff fd279c7..8a61104 | rg '^\\+' | rg -c -e \"\$pat\" || echo 0); done"

# ── ch8 what is left ────────────────────────────────────────────────────────
runsh 31 live-state "jq -c '.members[]|[.pane,.name,.path]' <laris-co state>; jq -r .saved <laris-co state>" \
  "jq -c '.members[]|[.pane,.name,(.path|sub(\"/opt/Code/github.com/\";\"\"))]' ~/.local/state/herdr-room/laris-co__aiexpo-oracle.json; jq -r .saved ~/.local/state/herdr-room/laris-co__aiexpo-oracle.json"
runsh 32 old-dir "ls <old body dir>; git -C <old> status --short | wc -l; agents with cwd = <old>" \
  "ls \$OLD | head -12; echo; echo uncommitted: \$(git -C \$OLD status --short | wc -l | tr -d ' ') files; echo unpushed: \$(git -C \$OLD log --oneline @{u}..HEAD 2>&1 | wc -l | tr -d ' ') commits
   echo agents in laris-co with this cwd: \$(herdr --session laris-co agent list | jq --arg c \$OLD '[.result.agents[]|select(.cwd==\$c)]|length')"
runsh 33 larisco "herdr --session laris-co agent list | jq (LarisCo host w60:p1)" \
  "herdr --session laris-co agent list | jq -r '.result.agents[]|select(.pane_id==\"w60:p1\")|[.pane_id,.agent_status,(.cwd|sub(\"/opt/Code/github.com/\";\"\"))]|@tsv'"
runsh 35 scan-hits "git diff fd279c7..8a61104 | rg '^\+' | rg -n '/Users/beta|/opt/Code'" \
  "cd \$MAIN && git diff fd279c7..8a61104 | rg '^\\+' | rg -n '/Users/beta|/opt/Code' | cut -c1-96"
runsh 34 timeline-src "cat timeline.py" "cat \$B/timeline.py"

date '+== capture end %H:%M:%S'
ls $C | wc -l
