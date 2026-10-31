#!/bin/bash
# Seam check for Perfect Looper x2 files: the loop point is the middle of the file (frame N/2-1 -> N/2).
# Pass when the PSNR across the loop point is within 6 dB of an ordinary step just before it.
psnr(){ ffmpeg -i "$1" -i "$2" -lavfi psnr -f null - 2>&1 | rg -o 'average:[0-9.]+' | cut -d: -f2; }
T=$(mktemp -d)
for F in "$@"; do
  N=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 "$F"); H=$((N/2))
  for n in $((H-2)) $((H-1)) $H; do ffmpeg -v error -y -i "$F" -vf "select='eq(n\,$n)'" -fps_mode passthrough "$T/$n.png"; done
  a=$(psnr "$T/$((H-2)).png" "$T/$((H-1)).png"); s=$(psnr "$T/$((H-1)).png" "$T/$H.png")
  v=$(python3 -c "print('PASS' if $s >= $a - 6 else 'FAIL')")
  printf '%s %s step=%.1f seam=%.1f %s\n' "$v" "$(basename "$F")" "$a" "$s" "$N"
done
rm -r "$T"
