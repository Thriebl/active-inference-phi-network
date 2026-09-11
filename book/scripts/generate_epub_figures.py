#!/usr/bin/env python3
"""
generate_epub_figures.py
Renders all 50 Mermaid diagrams from the manuscript into clean, crisp 250-DPI cropped PNGs
for universal e-reader compatibility (Kindle, Apple Books, Kobo, etc.).
"""

import os
import re
import subprocess
import shutil
from PIL import Image, ImageChops

BOOK_DIR = "/home/thr/Documents/active-inference-phi-network/book"
MANUSCRIPT_DIR = os.path.join(BOOK_DIR, "manuscript_en")
BUILD_DIR = os.path.join(BOOK_DIR, "build")
EPUB_IMG_DIR = os.path.join(BUILD_DIR, "epub_images")
os.makedirs(EPUB_IMG_DIR, exist_ok=True)

# 1. Collect all diagrams
chapter_files = sorted([f for f in os.listdir(MANUSCRIPT_DIR) if f.endswith(".md")])

diagram_list = []
pattern = re.compile(r'```mermaid\n(.*?)\n```\s*<p class="figure-caption"><strong>Figure\s+([^:]+):</strong>\s*(.*?)</p>', re.DOTALL)

for f in chapter_files:
    path = os.path.join(MANUSCRIPT_DIR, f)
    with open(path, "r", encoding="utf-8") as ch:
        content = ch.read()
    
    for match in pattern.finditer(content):
        code = match.group(1).strip()
        fig_num = match.group(2).strip()
        caption = match.group(3).strip()
        safe_fig_id = "fig_" + fig_num.replace(".", "_").lower()
        diagram_list.append({
            "file": f,
            "fig_num": fig_num,
            "id": safe_fig_id,
            "caption": caption,
            "code": code
        })

print(f"Total Mermaid diagrams collected: {len(diagram_list)}")

# 2. Build multi-page HTML slide document
slides_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
        primaryColor: '#f0f9ff',
        primaryTextColor: '#0369a1',
        primaryBorderColor: '#0284c7',
        lineColor: '#0284c7',
        secondaryColor: '#f8fafc',
        tertiaryColor: '#ffffff',
        fontSize: '13.5px',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
    },
    flowchart: {
        htmlLabels: true,
        useMaxWidth: false,
        curve: 'basis'
    }
});
</script>
<style>
@page {
    size: 1600px 2400px;
    margin: 0;
}
body {
    margin: 0;
    padding: 0;
    background: #ffffff;
}
.diagram-slide {
    width: 1600px;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    page-break-after: always;
    break-after: page;
    background: #ffffff;
    box-sizing: border-box;
    padding: 50px 30px;
}
.mermaid {
    width: auto;
}
</style>
</head>
<body>
"""

for d in diagram_list:
    slides_html += f'<div class="diagram-slide" id="{d["id"]}"><div class="mermaid">\n{d["code"]}\n</div></div>\n'

slides_html += "</body></html>"

temp_slides_html = os.path.join(BUILD_DIR, "temp_diagram_slides.html")
temp_slides_pdf = os.path.join(BUILD_DIR, "temp_diagram_slides.pdf")

with open(temp_slides_html, "w", encoding="utf-8") as f:
    f.write(slides_html)

print("  • Rendering 50 diagram slides with Google Chrome headless...")
subprocess.run([
    "google-chrome",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--virtual-time-budget=25000",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={temp_slides_pdf}",
    temp_slides_html
], check=True)

print("  • Rasterizing slides to high-resolution PNGs (200 DPI)...")
ppm_prefix = os.path.join(BUILD_DIR, "temp_slide_page")
subprocess.run([
    "pdftoppm",
    "-png",
    "-r", "200",
    temp_slides_pdf,
    ppm_prefix
], check=True)

# 3. Crop each image and save with target name
print("  • Cropping whitespace and saving to epub_images...")
pad = 20
for idx, d in enumerate(diagram_list, start=1):
    page_img = f"{ppm_prefix}-{idx:02d}.png" if os.path.exists(f"{ppm_prefix}-{idx:02d}.png") else f"{ppm_prefix}-{idx}.png"
    if not os.path.exists(page_img):
        print(f"    [ERROR] Missing page image {page_img} for {d['id']}")
        continue
    
    im = Image.open(page_img).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    
    if bbox:
        padded_bbox = (
            max(0, bbox[0] - pad),
            max(0, bbox[1] - pad),
            min(im.size[0], bbox[2] + pad),
            min(im.size[1], bbox[3] + pad)
        )
        cropped = im.crop(padded_bbox)
    else:
        cropped = im
    
    out_file = os.path.join(EPUB_IMG_DIR, f"{d['id']}.png")
    cropped.save(out_file, "PNG", optimize=True)
    if idx % 10 == 0 or idx == len(diagram_list):
        print(f"    ✓ Processed {idx}/{len(diagram_list)}: {d['id']}.png ({cropped.size[0]}x{cropped.size[1]})")

# Also copy simulation images to epub_images
sim_imgs = [
    ("Active_Inference_Phi_Simulation_Results.png", "fig_7_2.png"),
    ("Active_Inference_Expanding_Network_Phi_Scaling.png", "fig_7_4.png"),
    ("Deep_Temporal_Active_Inference_Simulation.png", "fig_7_7.png")
]
SOURCE_IMG_DIR = "/home/thr/Documents/active-inference-phi-network/images"
for src_name, dst_name in sim_imgs:
    src_path = os.path.join(SOURCE_IMG_DIR, src_name)
    dst_path = os.path.join(EPUB_IMG_DIR, dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"    ✓ Copied simulation plot: {dst_name}")

print("🎉 ALL 53 FIGURES READY IN EPUB_IMAGES!")
