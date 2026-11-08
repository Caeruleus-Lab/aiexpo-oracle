#!/usr/bin/env zsh
# scouts.sh "<task A>" "<task B>" [--kind claude] [--model sonnet] [--reuse]
# Lead stays left; two scout agents open on the right (top + bottom); both report back to the lead pane.
# --reuse: if two agents already sit in this tab (e.g. Nat forked the lead), brief THOSE instead of opening new panes.
set -u
A=${1:?task A}; B=${2:?task B}; shift 2
KIND=claude; MODEL=sonnet; REUSE=0
while [ $# -gt 0 ]; do case $1 in --kind) KIND=$2; shift 2;; --model) MODEL=$2; shift 2;; --reuse) REUSE=1; shift;; *) shift;; esac; done
LEAD=${HERDR_PANE_ID:?run from inside a herdr pane}
TAB=$(herdr agent list | jq -r --arg p "$LEAD" '.result.agents[]|select(.pane_id==$p)|.tab_id')
OTHERS=(${(f)"$(herdr agent list | jq -r --arg t "$TAB" --arg p "$LEAD" '.result.agents[]|select(.tab_id==$t and .pane_id!=$p)|.pane_id')"})
if [ $REUSE = 1 ] && [ ${#OTHERS} -ge 2 ]; then
  P1=${OTHERS[1]}; P2=${OTHERS[2]}; echo "reusing $P1 $P2"
else
  [ ${#OTHERS} -ge 1 ] && echo "note: tab already holds agents ${OTHERS[*]} — pass --reuse to brief them instead" >&2
  P1=$(herdr pane split --pane $LEAD --direction right --ratio 0.5 | jq -r '.result.pane.pane_id')
  P2=$(herdr pane split --pane $P1 --direction down --ratio 0.5 | jq -r '.result.pane.pane_id')
  args=(); [ $KIND = claude ] && args=(-- --model $MODEL)
  herdr agent start scout-a-${LEAD//:/-} --kind $KIND --pane $P1 $args >/dev/null || exit 1
  herdr agent start scout-b-${LEAD//:/-} --kind $KIND --pane $P2 $args >/dev/null || exit 1
fi
tail="When done, report ONLY via: herdr agent prompt $LEAD \"[scout %s] <result>\". Read-only unless the task says otherwise. Stop at 40 tool calls."
herdr agent prompt $P1 "SCOUT A. $A $(printf "$tail" A)" >/dev/null && echo "briefed A -> $P1"
herdr agent prompt $P2 "SCOUT B. $B $(printf "$tail" B)" >/dev/null && echo "briefed B -> $P2"
echo "lead=$LEAD scouts=$P1,$P2 — results arrive in the lead as mid-turn messages; never sleep-poll"
