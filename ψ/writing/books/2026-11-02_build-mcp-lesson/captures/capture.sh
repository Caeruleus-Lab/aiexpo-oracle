#!/usr/bin/env zsh
# Every command of the build-mcp lesson, run for real. Output: NN-slug.txt here, home folder shown as ~.
setopt pipefail
C=${0:A:h}; L=${C:h}; B=${L:h}; M=https://aiexpo.buildwithoracle.com/mcp
UA='Mozilla/5.0 (lesson capture)'
run() { local nn=$1 slug=$2 disp=$3 cmd=$4 f=$C/$1-$2.txt
  print -r -- "$ $disp" > $f
  zsh -c "$cmd" 2>&1 | sed "s#$HOME#~#g" >> $f; local rc=${pipestatus[1]}
  print -r -- "(exit $rc)" >> $f; printf '%s %-14s exit %d\n' $nn $slug $rc; }
export L B M UA
rpc() { print -r -- "{\"jsonrpc\":\"2.0\",\"id\":$1,\"method\":\"$2\",\"params\":$3}"; }
typeset -f rpc > $C/.lib.zsh; export LIB=$C/.lib.zsh

run 01 pieces   "wc -l worker.js mcp/server.mjs build_chunks.py; jq '.chunks|length' chunks.json" \
 "cd \$B && wc -l worker.js github/mcp/server.mjs build_chunks.py && printf 'chunks: ' && jq '.chunks|length' chunks.json && printf 'model: ' && jq -r .model chunks.json"
run 02 chunk    "jq '.chunks[] | select(.id==\"herdr-room/th/5\") | {id, lesson, lang, title, url, text: .text[0:120], vec: (.vec|length)}' chunks.json" \
 "cd \$B && jq '.chunks[] | select(.id==\"herdr-room/th/5\") | {id, lesson, lang, title, url, text: .text[0:120], vec: (.vec|length)}' chunks.json"
run 03 mini-list "printf initialize + tools/list | node code/mini-mcp.mjs" \
 "source \$LIB; cd \$L && { rpc 1 initialize '{\"protocolVersion\":\"2025-06-18\"}'; print -r -- '{\"jsonrpc\":\"2.0\",\"method\":\"notifications/initialized\"}'; rpc 2 tools/list '{}'; } | node code/mini-mcp.mjs | jq -c ."
run 04 mini-call "printf tools/call search {query: \"session memory\"} | node code/mini-mcp.mjs" \
 "source \$LIB; cd \$L && { rpc 1 tools/call '{\"name\":\"search\",\"arguments\":{\"query\":\"session memory\"}}'; rpc 2 tools/call '{\"name\":\"nope\",\"arguments\":{}}'; rpc 3 bogus '{}'; } | node code/mini-mcp.mjs | jq -c ."
run 05 mini-claude "claude -p --mcp-config mini.json --allowedTools mcp__mini__search \"...\"" \
 "cd \$L/code && print -r -- '{\"mcpServers\":{\"mini\":{\"command\":\"node\",\"args\":[\"mini-mcp.mjs\"]}}}' > /tmp/mini-mcp.json && MAW_CLAUDE_CHANNELS= command claude -p --strict-mcp-config --mcp-config /tmp/mini-mcp.json --allowedTools mcp__mini__search --model claude-haiku-5-5 'Use the mini search tool to find which command writes a retrospective. Answer in one line and name the note id.' </dev/null"
run 06 get      "curl -s https://aiexpo.buildwithoracle.com/mcp | jq ." \
 "curl -sA \"\$UA\" \$M | jq ."
run 07 init     "curl -s -X POST \$M -H 'content-type: application/json' -d '{initialize}' | jq '.result | {protocolVersion, serverInfo}'" \
 "source \$LIB; curl -sA \"\$UA\" -X POST \$M -H 'content-type: application/json' -d \"\$(rpc 1 initialize '{\"protocolVersion\":\"2025-06-18\"}')\" | jq '.result | {protocolVersion, serverInfo, capabilities}'"
run 08 tools    "curl ... -d '{tools/list}' | jq -r '.result.tools[] | .name + \": \" + .description[0:70]'" \
 "source \$LIB; curl -sA \"\$UA\" -X POST \$M -H 'content-type: application/json' -d \"\$(rpc 2 tools/list '{}')\" | jq -r '.result.tools[] | .name + \": \" + .description[0:70]'"
run 09 search   "curl ... -d '{tools/call search {query: \"ห้องเดียว หลาย agent\", lang: th}}' | jq -r '.result.content[0].text | fromjson | .results[] | .id + \"  \" + .title' | head -3" \
 "source \$LIB; curl -sA \"\$UA\" -X POST \$M -H 'content-type: application/json' -d \"\$(rpc 3 tools/call '{\"name\":\"search\",\"arguments\":{\"query\":\"ห้องเดียว หลาย agent\",\"lang\":\"th\"}}')\" | jq -r '.result.content[0].text | fromjson | .results[] | .id + \"  \" + .title' | head -3"
run 10 fetch    "curl ... -d '{tools/call fetch {id: \"mcp-connect/en/2\"}}' | jq -r '.result.content[0].text | fromjson | .text' | head -8" \
 "source \$LIB; curl -sA \"\$UA\" -X POST \$M -H 'content-type: application/json' -d \"\$(rpc 4 tools/call '{\"name\":\"fetch\",\"arguments\":{\"id\":\"mcp-connect/en/2\"}}')\" | jq -r '.result.content[0].text | fromjson | .text' | head -8"
run 11 npx      "printf initialize + tools/call search {query: \"herdr room out\"} | npx -y github:Caeruleus-Lab/aiexpo-lessons" \
 "source \$LIB; { rpc 1 initialize '{\"protocolVersion\":\"2025-06-18\"}'; print -r -- '{\"jsonrpc\":\"2.0\",\"method\":\"notifications/initialized\"}'; rpc 2 tools/call '{\"name\":\"search\",\"arguments\":{\"query\":\"herdr room out\"}}'; sleep 8; } | npx -y github:Caeruleus-Lab/aiexpo-lessons | jq -c '.result | if .serverInfo then {serverInfo} else (.content[0].text | fromjson | .results[0:3][] | {id, title}) end'"
run 12 config   "cat wrangler.jsonc" "cd \$B && cat wrangler.jsonc"
run 13 trap-ua  "curl -s -o /dev/null -w '%{http_code}' -A 'Python-urllib/3.12' \$M   # Cloudflare bot rule" \
 "printf 'Python-urllib UA: '; curl -s -o /dev/null -w '%{http_code}\n' -A 'Python-urllib/3.12' -X POST \$M -H 'content-type: application/json' -d '{}'; printf 'browser UA:       '; curl -s -o /dev/null -w '%{http_code}\n' -A \"\$UA\" -X POST \$M -H 'content-type: application/json' -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"ping\"}'"
run 14 test     "node code/test-both.mjs     # the same 7 calls on the npx copy and the hosted copy" \
 "cd \$L && node code/test-both.mjs"
rm -f $C/.lib.zsh
