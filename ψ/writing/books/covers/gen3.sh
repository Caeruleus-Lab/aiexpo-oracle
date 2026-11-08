#!/bin/zsh
# Covers for the 6-lesson herdr skills series (8 Nov 2026): same style as gen2.sh, one new group colour (deep blue / sky).
STYLE='Editorial illustration for a lesson card, 3:2 landscape, calm flat-painterly style with clean bold shapes and strong colour. The left 45% of the frame is calm, plain, low-detail space in the darkest tone of the palette (a title will be set there later); the subject sits in the right half, large and easy to read at thumbnail size. No text, letters or numbers anywhere. No logos, no real faces. '
PAL='Palette: deep navy-blue background, bright sky-blue and ice-blue light, white highlights. No amber, no orange lamp.'
gen() { codex exec --skip-git-repo-check -C /tmp/covers3 "Generate ONE image. ${STYLE}${PAL} Subject on the right side: $2. Reply with only the absolute path of the generated PNG." > /tmp/covers3/notext-$1.log 2>&1; echo "$1 done rc=$?"; }
L=(
"herdr-map|a big wall map with seven glowing clusters of small terminal windows joined by thin lines"
"herdr-wt-life|a small sprout growing from a tree branch, a sealed envelope and a neatly closed box, in a row along a path"
"herdr-sleep|small terminal windows sleeping under a crescent moon, one of them waking up next to an alarm clock"
"herdr-bring|a hand carrying a glowing terminal window from one room into another through an open doorway"
"herdr-machines|a laptop and a server tower joined by a glowing tunnel of light"
"herdr-full|an open thick reference book with many coloured tab markers and pages of tiny lines"
)
for row in $L; do IFS='|' read -r k s <<< "$row"; gen "$k" "$s" & done; wait
ok=0
for row in $L; do k=${row%%|*}
  p=$(grep -oE '/Users/[^ ]+/generated_images/[^ ]+\.png' /tmp/covers3/notext-$k.log | tail -1)
  [[ -f "$p" ]] || p=$(ls -t $(dirname "$p" 2>/dev/null)/*.png 2>/dev/null | head -1)
  if [[ -f "$p" ]]; then sips -s format jpeg -s formatOptions 80 -Z 1200 "$p" --out "/tmp/covers3/notext-$k.jpg" >/dev/null && ((ok++)) && echo "$k ok"; else echo "$k MISSING"; fi
done
echo "covers ok=$ok/6"
