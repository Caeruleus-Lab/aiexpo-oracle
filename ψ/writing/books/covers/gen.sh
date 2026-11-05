#!/bin/zsh
# How the lesson covers were made (Nat, 5 Nov): Codex image_gen draws each picture with no text (this script), then
# covers/title.py sets the English title. Output collected to /tmp/covers, then copied to <lesson>/images/cover-ai.jpg.
# one Codex image per lesson, 7 at a time; one log per key; then collect + jpeg into the lesson dir
BOOKS='/opt/Code/github.com/Caeruleus-Lab/aiexpo-oracle/ψ/writing/books'
STYLE='Editorial illustration for a lesson card, 3:2 landscape. Dark charcoal background, one warm amber stage-lamp glow, a few cool blue accents, calm painterly-flat style with clean shapes, the left 45% of the frame is calm empty dark space (a title will be set there later), the subject sits in the right half. No text, letters or numbers anywhere in the image. '
gen() { # key title subject
  codex exec --skip-git-repo-check -C /tmp/covers "Generate ONE image. ${STYLE} Subject on the right side: $3. No logos, no real people's faces, no extra words or letters. Reply with only the absolute path of the generated PNG." > /tmp/covers/notext-$1.log 2>&1
  echo "$1 done rc=$?"
}
L=(
"claude-chatgpt|Install Claude & ChatGPT|two glowing app windows on a wooden desk opening like small doors"
"ego-lite|A Browser for Your Agent|a small friendly robot hand resting on a browser window"
"mcp-connect|Connect the Lessons MCP|a power plug joining a chat speech bubble to a neat stack of books"
"phukhao-film|An Oracle Films Its Story|a film strip curving around a calm mountain silhouette"
"phukhao-journey|Phukhao's Journey|a small lantern climbing a mountain path toward a lit stage"
"herdr-room|One Room, Many Agents|many small lamp-lit desks gathered in one cozy room, seen from above"
"build-mcp|Build Your Own MCP|an open toolbox where books turn into tools"
"agy-mcp|Antigravity CLI + MCP|a terminal window floating weightless above a desk, small objects drifting up"
"skills-mcp|Skills, Voice and Video|one glowing hub handing out a paper scroll, a microphone and a film reel"
"relic5-ui|A Tour of relic5|a quiet archive hall with rows of softly glowing cards on shelves"
"team-charter|From Picture to Team|a pencil sketch of boxes on paper turning into lamp-lit desks with small figures"
"herdr-cmd-j|Cmd J and Cmd L|two keyboard keys sending a thin line of light to several small terminal windows"
"relic5-install|Every Machine, One Hub|several laptops sending streams of light into one round hub"
"signature|The Lessons' Signature|a document with a glowing wax-style seal made of tiny hexadecimal digits"
)
i=0
for row in $L; do
  IFS='|' read -r k t s <<< "$row"
  gen "$k" "$t" "$s" &
  (( ++i % 7 == 0 )) && wait
done
wait
ok=0
for row in $L; do
  k=${row%%|*}
  p=$(grep -oE '^/Users/[^ ]+/generated_images/[^ ]+\.png$' /tmp/covers/notext-$k.log | tail -1)
  if [[ -f "$p" ]]; then sips -s format jpeg -s formatOptions 72 -Z 1200 "$p" --out "/tmp/covers/notext-$k.jpg" >/dev/null && ((ok++)) && echo "$k ok"; else echo "$k MISSING"; fi
done
echo "covers ok=$ok/14"
