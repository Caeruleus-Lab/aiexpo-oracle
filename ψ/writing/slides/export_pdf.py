"""Export deck.html to deck.pdf: one 1920x1080 (16:9) page per slide, speaker notes hidden.

Usage: uv run --with playwright python export_pdf.py
"""
import pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).resolve().parent
css = """
@page { size: 1920px 1080px; margin: 0 }
html, body { width: 1920px; height: auto; overflow: visible; background: #000 }
#stage { position: static; transform: none !important; width: 1920px; height: auto }
.slide { display: block !important; position: relative; width: 1920px; height: 1080px; break-after: page }
.notes, #count { display: none !important }
"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto((here / "deck.html").as_uri())
    pg.wait_for_load_state("networkidle")
    pg.add_style_tag(content=css)
    n = pg.locator(".slide").count()
    pg.pdf(path=str(here / "deck.pdf"), width="1920px", height="1080px", print_background=True, prefer_css_page_size=True)
    b.close()
print(f"slides: {n} -> {here / 'deck.pdf'}")
