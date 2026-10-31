# helpers sourced by every runsh in capture.sh
paneof() { herdr --session $S pane list | jq -r --arg c "$1" '[.result.panes[]|select(.cwd==$c)]|last|.pane_id'; }
fake()   { herdr --session $S pane report-agent $1 --source book-demo --agent claude --state idle >/dev/null; }
