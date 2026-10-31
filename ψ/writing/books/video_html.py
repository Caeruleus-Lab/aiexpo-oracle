"""The "watch" section a lesson puts first: one or more videos with a poster frame, on the th / en / AI pages.

Each video is a 720p web copy (H.264 + AAC, +faststart) kept under the Workers 25 MiB per-file cap; the full
1080p masters stay in ~/pb/voice-lab. The README is not touched, so the signed editions stay valid.
"""
import html as H

CSS = """.watch video{width:100%;display:block;border-radius:var(--r);border:1px solid var(--rule);background:#000}
.watch figure.tall video{width:auto;max-width:100%;max-height:82vh;margin:0 auto}
.watch .alt{margin:-14px 0 24px;color:var(--ink-3);font-size:.95em}"""

TITLE = {"th": "ดูวิดีโอ", "en": "Watch", "b64": "Watch"}


def watch_section(lang, videos):
    """videos: dicts with src, poster, caption {th, en}, optional tall=True and alt=(href, {th, en}) for a second cut."""
    t = "th" if lang == "th" else "en"
    out = [f'<h2 id="watch-h">{TITLE[lang]}</h2>']
    for v in videos:
        cap = H.escape(v["caption"][t])
        out.append(f'<figure class="{"tall" if v.get("tall") else ""}"><video controls preload="metadata" playsinline '
                   f'poster="{v["poster"]}" src="{v["src"]}" aria-label="{cap}"></video><figcaption>{cap}</figcaption></figure>')
        if v.get("alt"):
            href, label = v["alt"]
            out.append(f'<p class="alt"><a href="{href}">{H.escape(label[t])}</a></p>')
    return f'<div class="watch">{"".join(out)}</div>'
