#!/bin/zsh
# Covers v2 (Nat, 8 Nov: "make cover to let it easy to scan make it differnce!"): v1 (gen.sh) gave all 14 the same dark room
# and amber lamp, so the cards blurred together. v2 keeps each lesson's subject but gives each landing GROUP its own colour
# world, so a reader can see the group at a glance. Then covers/title.py v2 sets the title plus a group tag in the group colour.
# Codex image_gen, 7 at a time, output /tmp/covers2/notext-<key>.jpg
STYLE='Editorial illustration for a lesson card, 3:2 landscape, calm flat-painterly style with clean bold shapes and strong colour. The left 45% of the frame is calm, plain, low-detail space in the darkest tone of the palette (a title will be set there later); the subject sits in the right half, large and easy to read at thumbnail size. No text, letters or numbers anywhere. No logos, no real faces. '
typeset -A PAL
PAL[start]='Palette: deep teal-to-petrol background, bright cyan and mint light, white highlights. No amber, no orange lamp.'
PAL[build]='Palette: deep forest green background, fresh lime and leaf-green light, cream highlights. No amber, no orange lamp.'
PAL[memory]='Palette: deep indigo-violet night background, lavender and soft purple glow, silver highlights. No amber, no orange lamp.'
PAL[team]='Palette: deep wine-red background, coral and warm pink light, cream highlights. No amber, no orange lamp.'
PAL[story]='Palette: dawn sky, deep navy at the top fading to warm peach and rose gold at the horizon, golden sunrise light.'
gen() { # key group subject
  codex exec --skip-git-repo-check -C /tmp/covers2 "Generate ONE image. ${STYLE}${PAL[$2]} Subject on the right side: $3. Reply with only the absolute path of the generated PNG." > /tmp/covers2/notext-$1.log 2>&1
  echo "$1 done rc=$?"
}
L=(
"skills-mcp|start|one glowing hub handing out a paper scroll, a microphone and a film reel"
"mcp-connect|start|a power plug joining a chat speech bubble to a neat stack of books"
"agy-mcp|start|a terminal window floating weightless, small objects drifting up around it"
"ego-lite|start|a small friendly robot hand resting on a browser window"
"claude-chatgpt|start|two glowing app windows opening like small doors"
"build-mcp|build|an open toolbox where books turn into tools"
"signature|build|a document with a glowing wax-style seal made of tiny hexagons"
"relic5-install|memory|several laptops sending streams of light into one round hub"
"relic5-ui|memory|a quiet archive hall with rows of softly glowing cards on shelves"
"team-charter|team|a pencil sketch of boxes on paper turning into desks with small figures"
"herdr-room|team|many small desks gathered in one cozy room, seen from above"
"herdr-cmd-j|team|two keyboard keys sending a thin line of light to several small terminal windows"
"phukhao-journey|story|a small lantern climbing a mountain path toward a lit stage"
"phukhao-film|story|a film strip curving around a calm mountain silhouette"
)
i=0
for row in $L; do
  IFS='|' read -r k g s <<< "$row"
  gen "$k" "$g" "$s" &
  (( ++i % 7 == 0 )) && wait
done
wait
ok=0
for row in $L; do
  k=${row%%|*}
  p=$(grep -oE '/Users/[^ ]+/generated_images/[^ ]+\.png' /tmp/covers2/notext-$k.log | tail -1)
  if [[ -f "$p" ]]; then sips -s format jpeg -s formatOptions 80 -Z 1200 "$p" --out "/tmp/covers2/notext-$k.jpg" >/dev/null && ((ok++)) && echo "$k ok"; else echo "$k MISSING"; fi
done
echo "covers ok=$ok/14"
