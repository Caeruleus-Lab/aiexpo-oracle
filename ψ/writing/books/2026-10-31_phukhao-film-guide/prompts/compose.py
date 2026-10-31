"""Phukhao 9 months, v3: the 13 GB300 loops as scenes under the same voice, captions and end card.

Each scene is one seamless loop (first half of the x2 file), repeated for as long as its line lasts,
scaled to 1920x1080 and joined to the next with a short crossfade. The line cards from `oraclefilm assets`
fade in over a soft dark band; the end card closes. Output is silent; mix-family adds voice + music.
Usage: python3 compose.py loops.json out.mp4   (loops.json: {"a1": "/path/x2.mp4", ...})
"""
import json, subprocess, sys
here = __file__.rsplit('/', 1)[0]
timed = json.load(open(f'{here}/timed.json'))
fam = json.load(open(f'{here}/family.json'))
loops = json.load(open(sys.argv[1])); out = sys.argv[2]
segs = timed['segments']; X = 0.6                     # crossfade seconds
VEND = segs[-1]['end']; CARD = VEND + 1.8; TOTAL = CARD + 4.6
def dur(f): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f]))
# scene i covers [b_i, b_{i+1}) where b_0 = 0 and b_i = start_i - 0.3; the last runs to the end card
bounds = [0.0] + [max(0.0, s['start'] - 0.3) for s in segs[1:]] + [CARD + 0.6]
args = ['ffmpeg', '-v', 'error', '-y']; f = []; n = len(segs)
for i, m in enumerate(fam):
    src = loops[m['line']]; one = dur(src) / 2
    d = bounds[i + 1] - bounds[i] + (X if i < n - 1 else 0)
    args += ['-stream_loop', '-1', '-t', f'{one:.3f}', '-i', src]
    f.append(f'[{i}:v]trim=0:{one:.3f},setpts=PTS-STARTPTS,loop=loop=-1:size=32767,trim=0:{d:.3f},setpts=PTS-STARTPTS,'
             f'scale=1920:1280:flags=lanczos,crop=1920:1080,fps=24,format=yuv420p[s{i}]')
cur, off = 's0', bounds[1] - bounds[0]
for i in range(1, n):
    f.append(f'[{cur}][s{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[x{i}]'); cur = f'x{i}'
    off += bounds[i + 1] - bounds[i]
k = n
args += ['-loop', '1', '-t', f'{TOTAL:.2f}', '-i', f'{here}/card2.png']; card = k; k += 1
f.append(f'color=black:s=1920x1080:d={TOTAL:.2f},format=rgba,geq=r=0:g=0:b=0:a=\'if(gt(Y,640),(Y-640)/440*170,0)\'[band]')
f.append(f'[{cur}]tpad=stop_mode=clone:stop_duration=6[bg];[bg][band]overlay=0:0[v0]')
cur = 'v0'
for i, s in enumerate(segs):
    args += ['-loop', '1', '-t', f'{TOTAL:.2f}', '-i', f'{here}/line{i}.png']
    a, b = s['start'] - 0.15, s['end'] + 0.35
    f.append(f'[{k}:v]format=rgba,fade=t=in:st={a:.2f}:d=0.35:alpha=1,fade=t=out:st={b:.2f}:d=0.35:alpha=1[l{i}];'
             f'[{cur}][l{i}]overlay=0:0:enable=\'between(t,{a:.2f},{b + 0.4:.2f})\'[v{i + 1}]')
    cur = f'v{i + 1}'; k += 1
f.append(f'[{card}:v]format=rgba,fade=t=in:st={CARD:.2f}:d=1.2:alpha=1[cd];[{cur}][cd]overlay=0:0:enable=\'gte(t,{CARD:.2f})\',trim=0:{TOTAL:.2f}[out]')
args += ['-filter_complex', ';'.join(f), '-map', '[out]', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', '24', out]
subprocess.check_call(args)
print('COMPOSE-DONE', out, f'{dur(out):.2f}s')
