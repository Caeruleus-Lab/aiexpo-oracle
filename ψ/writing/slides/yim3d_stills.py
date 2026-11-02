"""Render คุณยิ้ม's 3D deck (yim-3d/deck.html) to 1920x1080 stills: img/yim3d-NN.png, one per slide, plus notes.

The live deck stays the one to present (3D moves); the stills put the same design into deck.html and deck.pdf.
Usage: uv run --with playwright python yim3d_stills.py
"""
import json, pathlib
from playwright.sync_api import sync_playwright

here = pathlib.Path(__file__).resolve().parent
out = here / "img"; out.mkdir(exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto((here / "yim-3d" / "deck.html").as_uri())
    pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2500)
    n = pg.locator(".slide").count()
    world = pg.evaluate("() => window.__world")
    notes = pg.evaluate("() => [...document.querySelectorAll('.slide')].map(s => s.querySelector('.notes')?.innerText.trim() || '')")
    pg.keyboard.press("Home"); pg.wait_for_timeout(1800)
    for k in range(n):
        if k: pg.keyboard.press("ArrowRight"); pg.wait_for_timeout(2200)  # 850 ms camera move + riso print settle
        pg.screenshot(path=str(out / f"yim3d-{k+1:02d}.png"))
    b.close()
(here / "img" / "yim3d-notes.json").write_text(json.dumps(notes, ensure_ascii=False, indent=1))
print(f"slides: {n}, webgl world: {world}, stills -> img/yim3d-01..{n:02d}.png")
