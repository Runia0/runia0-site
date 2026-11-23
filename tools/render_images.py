# -*- coding: utf-8 -*-
"""Render favicon PNGs, logo and the Open Graph image with headless Chromium.

Usage: python3 tools/render_images.py   (needs: pip install playwright)
"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
SVG = open(os.path.join(ASSETS, "favicon.svg"), encoding="utf-8").read()

OG = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;width:1200px;height:630px;background:#050807;color:#e8f2ec;
font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;overflow:hidden;position:relative}
.glow{position:absolute;inset:0;background:radial-gradient(700px 380px at 90% 0%,rgba(31,107,67,.45),transparent 70%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(#0f2219 1px,transparent 1px),linear-gradient(90deg,#0f2219 1px,transparent 1px);background-size:48px 48px;opacity:.45}
.c{position:absolute;left:84px;top:84px;right:84px;bottom:84px;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:22px;font-size:44px;font-weight:700}
.brand svg{width:76px;height:76px}
h1{font-size:82px;line-height:1.04;margin:auto 0 22px;font-weight:750;letter-spacing:-1px;max-width:900px}
h1 span{color:#39ff88}
p{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:25px;color:#a3b8ab;margin:0}
</style></head><body><div class="grid"></div><div class="glow"></div><div class="c">
<div class="brand">%SVG%<span>Runia0</span></div>
<h1>Ideas into things that <span>work.</span></h1>
<p>Software · AI · Games · Digital Products</p></div></body></html>""".replace("%SVG%", SVG)


def icon_html(size, pad=0):
    inner = size - 2 * pad
    svg = SVG.replace("<svg ", '<svg width="%d" height="%d" ' % (inner, inner))
    bg = "#050807" if pad else "transparent"
    return (
        '<html><body style="margin:0;background:transparent">'
        '<div style="width:%dpx;height:%dpx;padding:%dpx;box-sizing:border-box;background:%s">%s</div>'
        "</body></html>" % (size, size, pad, bg, svg)
    )


with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.set_content(OG)
    pg.screenshot(path=os.path.join(ASSETS, "og.png"))
    for name, size, pad in [("favicon-32.png", 32, 0), ("apple-touch-icon.png", 180, 0), ("logo-512.png", 512, 0)]:
        pg = b.new_page(viewport={"width": size, "height": size})
        pg.set_content(icon_html(size, pad))
        pg.screenshot(path=os.path.join(ASSETS, name), omit_background=(size == 32))
    b.close()
print("images rendered")
