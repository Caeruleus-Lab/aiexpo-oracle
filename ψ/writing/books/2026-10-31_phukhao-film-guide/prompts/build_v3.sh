#!/bin/bash
# v3: the 13 GB300 loops under the same voice. compose -> mix -> master (-16 LUFS, -3 dBTP) -> 9:16 cut.
set -e; cd "$(dirname "$0")"; O=~/pb/screenshots/oraclefilm/bin/oraclefilm
python3 compose.py loops.json v3-loops-silent.mp4
$O mix-family -dir "$PWD" -video "$PWD/v3-loops-silent.mp4" -whoosh '' -out out/phukhao-9m-v3-loops-raw.mp4
ffmpeg -v error -y -i out/phukhao-9m-v3-loops-raw.mp4 -c:v copy -af 'loudnorm=I=-16:TP=-3:LRA=11,aresample=48000,alimiter=limit=0.70:level=disabled' -c:a aac -b:a 192k out/phukhao-9m-v3-loops.mp4
rm out/phukhao-9m-v3-loops-raw.mp4
ffmpeg -v error -y -i out/phukhao-9m-v3-loops.mp4 -filter_complex '[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.15[bg];[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2' -c:a copy -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p out/phukhao-9m-v3-loops-vertical.mp4
for f in out/phukhao-9m-v3-*.mp4; do echo "$f $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)s $(du -h $f | cut -f1) $($O loudness $f 2>&1 | rg -o 'true peak [-0-9.]+ dBTP')"; done
