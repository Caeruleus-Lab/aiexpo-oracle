"""The "watch" section a lesson puts first: one or more videos with a poster frame, on the th / en / AI pages.

Each video is a 720p web copy (H.264 + AAC, +faststart) kept under the Workers 25 MiB per-file cap; the full
1080p masters stay in ~/pb/voice-lab. The README is not touched, so the signed editions stay valid.
"""
import html as H

CSS = """.watch video{width:100%;display:block;border-radius:var(--r);border:1px solid var(--rule);background:#000}
.watch figure.tall video{width:auto;max-width:100%;max-height:82vh;margin:0 auto}
.watch .alt{margin:-14px 0 24px;color:var(--ink-3);font-size:.95em}
.watch iframe{width:100%;aspect-ratio:16/9;display:block;border-radius:var(--r);border:1px solid var(--rule);background:#000}"""

TITLE = {"th": "ดูวิดีโอ", "en": "Watch", "b64": "Watch"}


def watch_section(lang, videos):
    """videos: dicts with src, poster, caption {th, en}, optional tall=True and alt=(href, {th, en}), or a list of them, for other cuts; or iframe=url + caption for a live page."""
    t = "th" if lang == "th" else "en"
    out = [f'<h2 id="watch-h">{TITLE[lang]}</h2>']
    for v in videos:
        cap = H.escape(v["caption"][t])
        if v.get("iframe"):  # a live page from another site (a slide deck), played in place
            out.append(f'<figure><iframe src="{v["iframe"]}" title="{cap}" loading="lazy" allow="fullscreen" '
                       f'allowfullscreen referrerpolicy="no-referrer"></iframe><figcaption>{cap}</figcaption></figure>')
        else:
            out.append(f'<figure class="{"tall" if v.get("tall") else ""}"><video controls preload="metadata" playsinline '
                       f'poster="{v["poster"]}" src="{v["src"]}" aria-label="{cap}"></video><figcaption>{cap}</figcaption></figure>')
        if v.get("alt"):
            alts = v["alt"] if isinstance(v["alt"], list) else [v["alt"]]
            links = " · ".join(f'<a href="{href}">{H.escape(label[t])}</a>' for href, label in alts)
            out.append(f'<p class="alt">{links}</p>')
    return f'<div class="watch">{"".join(out)}</div>'
