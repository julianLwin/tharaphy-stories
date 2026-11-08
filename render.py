"""Render each slide of a story HTML file to a 1080x1920 PNG.

Usage: python render.py <story.html> <out_dir> <name1> <name2> ...
Slide N (id="sN") is saved as <out_dir>/NN-<nameN>.png.
Needs: pip install playwright && python -m playwright install --with-deps chromium
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

html = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2])
names = sys.argv[3:]
out.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1920})
    for i, name in enumerate(names, 1):
        page.goto(f"{html.as_uri()}?s={i}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready.then(() => true)")
        path = out / f"{i:02d}-{name}.png"
        page.screenshot(path=str(path))
        print(path)
    browser.close()
