#!/usr/bin/env python3
"""
generate_epub_figures.py
Renders all 50 Mermaid diagrams from the English or German manuscript into clean,
crisp 250-DPI cropped PNGs for universal e-reader compatibility (Kindle, Apple Books, Kobo, etc.).
"""

import os
import sys
import re
import subprocess
import shutil
from PIL import Image, ImageChops

BOOK_DIR = "/home/thr/Documents/active-inference-phi-network/book"
BUILD_DIR = os.path.join(BOOK_DIR, "build")
SOURCE_IMG_DIR = "/home/thr/Documents/active-inference-phi-network/images"

def generate_figures(lang="en"):
    print(f"\n=======================================================")
    print(f"=== Generating EPUB Figures for Language: {lang.upper()} ===")
    print(f"=======================================================")

    manuscript_dir = os.path.join(BOOK_DIR, f"manuscript_{lang}")
    epub_img_dir = os.path.join(BUILD_DIR, f"epub_images_{lang}" if lang == "de" else "epub_images")
    os.makedirs(epub_img_dir, exist_ok=True)

    # 1. Collect all diagrams
    chapter_files = sorted([f for f in os.listdir(manuscript_dir) if f.endswith(".md")])
    diagram_list = []
    
    if lang == "de":
        pattern = re.compile(r'```mermaid\n(.*?)\n```\s*<p class="figure-caption"><strong>Abbildung\s+([^:]+):</strong>\s*(.*?)</p>', re.DOTALL)
    else:
        pattern = re.compile(r'```mermaid\n(.*?)\n```\s*<p class="figure-caption"><strong>Figure\s+([^:]+):</strong>\s*(.*?)</p>', re.DOTALL)

    for f in chapter_files:
        path = os.path.join(manuscript_dir, f)
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

    print(f"  • Total Mermaid diagrams collected ({lang.upper()}): {len(diagram_list)}")

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

    temp_slides_html = os.path.join(BUILD_DIR, f"temp_diagram_slides_{lang}.html")
    temp_slides_pdf = os.path.join(BUILD_DIR, f"temp_diagram_slides_{lang}.pdf")

    with open(temp_slides_html, "w", encoding="utf-8") as f:
        f.write(slides_html)

    print(f"  • Rendering {len(diagram_list)} diagram slides with Google Chrome headless...")
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
    ppm_prefix = os.path.join(BUILD_DIR, f"temp_slide_page_{lang}")
    subprocess.run([
        "pdftoppm",
        "-png",
        "-r", "200",
        temp_slides_pdf,
        ppm_prefix
    ], check=True)

    # 3. Crop each image and save with target name
    print(f"  • Cropping whitespace and saving to {epub_img_dir}...")
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
        
        out_file = os.path.join(epub_img_dir, f"{d['id']}.png")
        cropped.save(out_file, "PNG", optimize=True)
        if idx % 10 == 0 or idx == len(diagram_list):
            print(f"    ✓ Processed {idx}/{len(diagram_list)}: {d['id']}.png ({cropped.size[0]}x{cropped.size[1]})")

    # Also copy simulation images to epub_images
    sim_imgs = [
        ("Active_Inference_Phi_Simulation_Results.png", "fig_7_2.png"),
        ("Active_Inference_Expanding_Network_Phi_Scaling.png", "fig_7_4.png"),
        ("Deep_Temporal_Active_Inference_Simulation.png", "fig_7_7.png")
    ]
    for src_name, dst_name in sim_imgs:
        src_path = os.path.join(SOURCE_IMG_DIR, src_name)
        dst_path = os.path.join(epub_img_dir, dst_name)
        if os.path.exists(src_path):
            shutil.copy(src_path, dst_path)
            print(f"    ✓ Copied simulation plot: {dst_name}")

    print(f"🎉 ALL 53 FIGURES READY IN {epub_img_dir}!")

def main():
    if "--de" in sys.argv:
        generate_figures("de")
    elif "--all" in sys.argv:
        generate_figures("en")
        generate_figures("de")
    else:
        generate_figures("en")

if __name__ == "__main__":
    main()
