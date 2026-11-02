#!/usr/bin/env zsh
# Every agy command of lesson 08, run for real on m5 (agy 1.4.12, signed in). Output: NN-slug.txt here.
# The home folder is shown as ~; lines about other MCP servers on this machine are left out (rg -v).
setopt pipefail
C=${0:A:h}
run() { local nn=$1 slug=$2 disp=$3 cmd=$4 f=$C/$1-$2.txt
  print -r -- "$ $disp" > $f
  zsh -c "$cmd" 2>&1 | sed "s#$HOME#~#g" | rg -v '@gmail|@googlemail' >> $f; local rc=${pipestatus[1]}
  print -r -- "(exit $rc)" >> $f; printf '%s %-12s exit %d\n' $nn $slug $rc; }
OTHERS='^(rea) '
export OTHERS
cd /tmp

run 01 version  "agy --version" "agy --version"
run 02 mcp-help "agy mcp --help" "agy mcp --help"
run 03 add-help "agy mcp add --help" "agy mcp add --help"
run 04 add      "agy mcp add aiexpo https://aiexpo.buildwithoracle.com/mcp; agy mcp add aiexpo-github npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp" \
 "agy mcp add aiexpo https://aiexpo.buildwithoracle.com/mcp && agy mcp add aiexpo-github npx -y github:Caeruleus-Lab/aiexpo-lessons-mcp"
run 05 list     "agy mcp list" "agy mcp list | rg -v \"\$OTHERS\""
run 06 trap-flag "agy mcp add try-x https://example.com/mcp --header 'X-Test: 1'   # flag after the name" \
 "agy mcp add try-x https://example.com/mcp --header 'X-Test: 1'; rc=\$?; agy mcp list | rg -q '^try-x ' && agy mcp remove try-x >/dev/null; exit \$rc"
run 07 toggle   "agy mcp disable aiexpo-github; agy mcp list; agy mcp enable aiexpo-github" \
 "agy mcp disable aiexpo-github && agy mcp list | rg -v \"\$OTHERS\" && agy mcp enable aiexpo-github && agy mcp list | rg '^aiexpo-github'"
run 08 hosted   "agy --sandbox --dangerously-skip-permissions --print-timeout 240s -p \"Use ONLY the MCP server aiexpo ... how do I build my own MCP server?\"" \
 "agy --sandbox --dangerously-skip-permissions --print-timeout 240s -p 'Use ONLY the MCP server named aiexpo (tools search and fetch). Search the lessons for: how do I build my own MCP server? Answer in 3 short bullets, give the lesson URL you used, and name each MCP tool you called.'"
run 09 github   "agy --sandbox --dangerously-skip-permissions --print-timeout 240s -p \"Use ONLY the MCP server aiexpo-github ... list_lessons, then search\"" \
 "agy --sandbox --dangerously-skip-permissions --print-timeout 240s -p 'Use ONLY the MCP server named aiexpo-github. Call list_lessons, then search for: build your own MCP. Reply with the lesson count, the title of lesson 7, the top hit id, and the tool names you called.'"
