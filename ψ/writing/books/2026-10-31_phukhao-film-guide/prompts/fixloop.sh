#!/bin/bash
# Make a loop seamless by hand when the model's bridge drifted: take one loop (first half of the x2 file),
# drop its first X seconds, and crossfade its last X seconds into those first X seconds. The output ends
# exactly where it begins. Written as x2 again (played twice) so compose.py treats it like any loop.
# Usage: fixloop.sh IN_x2.mp4 OUT_x2.mp4 [X=1.2]
set -euo pipefail
IN=$1; OUT=$2; X=${3:-1.2}
T=$(python3 -c "print($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")/2)")
TMP=$(mktemp -d)
ffmpeg -v error -y -i "$IN" -filter_complex "[0:v]trim=0:$T,setpts=PTS-STARTPTS,split[a][b];[a]trim=$X:$T,setpts=PTS-STARTPTS[tail];[b]trim=0:$X,setpts=PTS-STARTPTS[head];[tail][head]xfade=transition=fade:duration=$X:offset=$(python3 -c "print($T-2*$X)")[v]" -map "[v]" -an -c:v libx264 -crf 16 -pix_fmt yuv420p "$TMP/one.mp4"
ffmpeg -v error -y -stream_loop 1 -i "$TMP/one.mp4" -c copy "$OUT"
rm -r "$TMP"; echo "FIXED $OUT"
