#!/usr/bin/env zsh
# Every command of the herdr-room lesson, run for real in a throwaway herdr session `roomlab`
# on a throwaway git repo /tmp/roomlab/team (main + 2 worktrees). Output: NN-slug.txt here.
# The home folder is printed as ~ so no local user path reaches the public page.
setopt pipefail
C=${0:A:h}; S=roomlab; T=/private/tmp/roomlab/team
run() { local nn=$1 slug=$2 disp=$3 cmd=$4 f=$C/$1-$2.txt
  print -r -- "$ $disp" > $f
  zsh -c "$cmd" 2>&1 | sed "s#$HOME#~#g" >> $f; local rc=${pipestatus[1]}
  print -r -- "(exit $rc)" >> $f; printf '%s %-16s exit %d\n' $nn $slug $rc; }
pane() { herdr --session $S agent list | jq -r --arg n "$1" '.result.agents[]|select(.name==$n)|.pane_id'; }
export S T; typeset -f pane > $C/.lib.zsh; export LIB=$C/.lib.zsh

# reset
for w in $(herdr --session $S workspace list | jq -r '.result.workspaces[]|select(.label!="roomlab")|.workspace_id'); do herdr --session $S workspace close $w --group >/dev/null 2>&1 || herdr --session $S workspace close $w >/dev/null 2>&1; done
rm -f ~/.local/state/herdr-room/${S}__team.json

run 01 repo      "git -C /tmp/roomlab/team worktree list" "git -C $T worktree list"
run 02 help      "herdr-room --help | head -8" "herdr-room --help | head -8"
run 03 spaces    "herdr --session roomlab workspace create --cwd team --label desk; herdr worktree open (x2)" \
 "herdr --session $S workspace create --cwd $T --label desk --no-focus | jq -c '.result|{space:.workspace.workspace_id,pane:.root_pane.pane_id}'
  for m in member-a member-b; do herdr --session $S worktree open --cwd $T --path $T/wt/\$m --label \$m --no-focus | jq -c '.result|{space:.workspace.workspace_id,label:.workspace.label,linked:.workspace.worktree.is_linked_worktree}'; done"
run 04 agents    "herdr pane report-agent <pane> --agent claude --state idle; herdr agent rename <pane> <name>" \
 "for w in \$(herdr --session $S workspace list | jq -r '.result.workspaces[]|select(.label!=\"roomlab\")|.workspace_id'); do
    p=\$(herdr --session $S workspace get \$w | jq -r '.result.workspace.active_tab_id' | sed 's/:t.*//'):p1; l=\$(herdr --session $S workspace get \$w | jq -r .result.workspace.label)
    herdr --session $S pane report-agent \$p --source lesson --agent claude --state idle >/dev/null; herdr --session $S agent rename \$p \$l >/dev/null; done
  herdr --session $S agent list | jq -r '.result.agents[]|[.pane_id,.name,.agent_status,(.cwd|sub(\"/private/tmp/roomlab/\";\"\"))]|@tsv'"
run 05 in-dry    "herdr-room in team desk member-a member-b --layout fib --session roomlab --dry" \
 "herdr-room in team desk member-a member-b --layout fib --session $S --dry"
run 06 in        "herdr-room in team desk member-a member-b --layout fib --session roomlab" \
 "herdr-room in team desk member-a member-b --layout fib --session $S"
run 07 state     "herdr-room list | rg roomlab; jq '.members' ~/.local/state/herdr-room/roomlab__team.json" \
 "herdr-room list | rg '^roomlab'; jq -c '.layout, (.members[]|[.pane,.name])' ~/.local/state/herdr-room/${S}__team.json"
run 08 out-dry   "herdr-room out team --session roomlab --dry" "herdr-room out team --session $S --dry"
run 09 out       "herdr-room out team --session roomlab" "herdr-room out team --session $S"
run 10 nested    "herdr --session roomlab workspace list | jq '[space, label, linked worktree]'" \
 "herdr --session $S workspace list | jq -r '.result.workspaces[]|[.workspace_id,.label,(.worktree.is_linked_worktree//false)]|@tsv'"
run 11 rebuild   "herdr-room in team --session roomlab      # no members: rebuild from the saved state" \
 "herdr-room in team --session $S | rg -v '^  run'"
# the trap: a new body for member-a starts while the old one is still inside the room
run 12 newbody   "herdr pane split <member-a> --direction down --cwd team/wt/member-a; report-agent; rename member-a-new" \
 "source \$LIB; o=\$(pane member-a); n=\$(herdr --session $S pane split \$o --direction down --cwd $T/wt/member-a --no-focus | jq -r .result.pane.pane_id)
  herdr --session $S pane report-agent \$n --source lesson --agent claude --state idle >/dev/null; herdr --session $S agent rename \$n member-a-new >/dev/null; echo old=\$o new=\$n"
run 13 trap      "herdr-room in team desk member-a-new member-b --layout fib --session roomlab   # old body still inside" \
 "herdr-room in team desk member-a-new member-b --layout fib --session $S | rg -v '^  run'"
run 14 fix       "herdr pane close <old member-a>; then herdr-room in team desk member-a-new member-b ..." \
 "source \$LIB; herdr --session $S pane close \$(pane member-a) | jq -r .result.type
  herdr-room in team desk member-a-new member-b --layout fib --session $S | rg -v '^  run'"
run 15 manual    "herdr pane move <pane> --tab <room tab> --target-pane <desk> --split right --ratio 0.5   # what in does, by hand" \
 "source \$LIB; herdr-room out team member-b --session $S >/dev/null; b=\$(pane member-b); d=\$(pane desk); t=\$(herdr --session $S pane get \$d | jq -r .result.pane.tab_id)
  herdr --session $S pane move \$b --tab \$t --target-pane \$d --split right --ratio 0.5 --no-focus | jq -c '.result|{type, changed}'
  herdr --session $S agent list | jq -r '.result.agents[]|[.pane_id,.name]|@tsv'"
