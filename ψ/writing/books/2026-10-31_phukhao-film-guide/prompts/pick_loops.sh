#!/bin/bash
# For each scene take the model's loop if its seam passes; otherwise crossfade-fix it. Writes loops.json + loops-report.txt.
cd "$(dirname "$0")"; mkdir -p loops/fixed; : > loops-report.txt; echo '{' > loops.json; first=1
for s in a1 a2 a3 a4 b1 b2 b3 c1 c2 c3 d1 d2 d3; do
  f=$(ls loops/p9-$s"_Loop_final_x2_"*-audio.mp4 | tail -1)
  r=$(./seamcheck.sh "$f")
  if [[ $r == PASS* ]]; then use="$f"; how=model; else ./fixloop.sh "$f" "loops/fixed/$s.mp4" >/dev/null; use="loops/fixed/$s.mp4"; how="fixed: $(./seamcheck.sh "$use")"; fi
  echo "$s  $r  ->  $how" | tee -a loops-report.txt
  [ $first -eq 1 ] || echo ',' >> loops.json; first=0; printf '"%s": "%s"' "$s" "$PWD/$use" >> loops.json
done; echo '}' >> loops.json; python3 -c "import json;print(len(json.load(open('loops.json'))),'scenes in loops.json')"
