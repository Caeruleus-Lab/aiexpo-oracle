"""Re-take the landing screenshots used by slides.html (live site, light theme, 1920x1080 viewport).
Usage: uv run --with playwright python shots_capture.py      AIExpo Oracle (Oracle AI), 2026-11-04."""
import pathlib
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent; S = HERE / "shots"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.add_init_script("localStorage.setItem('aiexpo-theme','light');localStorage.setItem('aiexpo-lang','th')")
    pg.goto("https://aiexpo.buildwithoracle.com/"); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
    pg.evaluate("document.querySelector('[data-set=th]')?.click()"); pg.wait_for_timeout(300)
    pg.screenshot(path=str(S / "landing.png"))
    for name, sel in [("copybox", "#brief"), ("lessons", "#all")]:
        pg.evaluate(f"window.scrollTo(0, document.querySelector('{sel}').getBoundingClientRect().top + scrollY - 40)")
        pg.wait_for_timeout(700); pg.screenshot(path=str(S / f"{name}.png"))
    b.close()
print("ok")
