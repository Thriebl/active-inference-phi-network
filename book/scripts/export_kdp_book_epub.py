#!/usr/bin/env python3
"""
export_kdp_book_epub.py
Compiles the complete English Standalone Amazon KDP/Apple Books/EPUB3 Edition
of The Conative-Integrative Framework (CIF).
Integrates all 53 figures (50 rendered diagrams + 3 simulation plots),
MathML mathematical equations, professional typography, cover art, and navigation.
"""

import os
import re
import subprocess
import shutil
import zipfile

BOOK_DIR = "/home/thr/Documents/active-inference-phi-network/book"
MANUSCRIPT_DIR = os.path.join(BOOK_DIR, "manuscript_en")
BUILD_DIR = os.path.join(BOOK_DIR, "build")
EPUB_IMG_DIR = os.path.join(BUILD_DIR, "epub_images")
COVER_PATH = os.path.join(BOOK_DIR, "cover", "The_Conative_Integrative_Framework_Front_Cover.jpg")
CSS_PATH = os.path.join(BUILD_DIR, "epub_style.css")

DOCS_DIR = "/home/thr/Documents/active-inference-phi-network/docs"
VAULT_PDF_DIR = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"
BOOKS_DIR = "/home/thr/Documents/01_Books"

def prepare_epub_markdown(output_file):
    """
    Merges all English manuscript chapters, replacing Mermaid code blocks with
    embedded rasterized high-resolution PNGs and remapping simulation image links.
    """
    chapter_files = sorted([f for f in os.listdir(MANUSCRIPT_DIR) if f.endswith(".md")])
    merged_sections = []

    # Regex to find mermaid block followed by figure caption
    # e.g.: ```mermaid\n...\n```\s*<p class="figure-caption"><strong>Figure 1.1:</strong> ...</p>
    mermaid_pattern = re.compile(
        r'```mermaid\n.*?\n```(?=\s*<p class="figure-caption"><strong>Figure\s+([^:]+):</strong>)',
        re.DOTALL
    )

    for f in chapter_files:
        path = os.path.join(MANUSCRIPT_DIR, f)
        with open(path, "r", encoding="utf-8") as ch:
            content = ch.read().strip()
        
        # Replace mermaid blocks with image tag
        def replace_mermaid(match):
            fig_num = match.group(1).strip()
            safe_id = "fig_" + fig_num.replace(".", "_").lower()
            return f"![]({EPUB_IMG_DIR}/{safe_id}.png)"
        
        transformed = mermaid_pattern.sub(replace_mermaid, content)
        
        # Remap simulation images in Chapter 7
        transformed = transformed.replace(
            "../images/Active_Inference_Phi_Simulation_Results.png",
            f"{EPUB_IMG_DIR}/fig_7_2.png"
        )
        transformed = transformed.replace(
            "../images/Active_Inference_Expanding_Network_Phi_Scaling.png",
            f"{EPUB_IMG_DIR}/fig_7_4.png"
        )
        transformed = transformed.replace(
            "../images/Deep_Temporal_Active_Inference_Simulation.png",
            f"{EPUB_IMG_DIR}/fig_7_7.png"
        )
        
        merged_sections.append(transformed)

    full_text = "\n\n".join(merged_sections)
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(full_text)
    
    print(f"  • Prepared merged EPUB markdown: {output_file} ({len(full_text)} chars)")
    return output_file

def build_epub():
    print("\n=======================================================")
    print("=== Compiling EPUB3 Edition: The Conative-Integrative Framework ===")
    print("=======================================================")

    md_file = os.path.join(BUILD_DIR, "CIF_Monograph_EN_epub.md")
    prepare_epub_markdown(md_file)

    epub_out = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_EN.epub")

    cmd = [
        "pandoc",
        md_file,
        "-o", epub_out,
        "--to=epub3",
        "--mathml",
        "--table-of-contents",
        "--toc-depth=2",
        f"--epub-cover-image={COVER_PATH}",
        f"--css={CSS_PATH}",
        "--metadata", "title=The Conative-Integrative Framework",
        "--metadata", "subtitle=Active Inference, Integrated Information Theory, and the Mind at Large",
        "--metadata", "author=Thomas Riebl",
        "--metadata", "language=en",
        "--metadata", "rights=© 2026 Thomas Riebl. All rights reserved.",
        "--metadata", "publisher=Thomas Riebl",
        f"--resource-path={BUILD_DIR}:{EPUB_IMG_DIR}:{BOOK_DIR}/cover"
    ]

    print("  • Running Pandoc EPUB3 compiler with MathML & custom CSS...")
    subprocess.run(cmd, check=True)
    print(f"  ✓ EPUB generated: {epub_out} ({os.path.getsize(epub_out)} bytes)")

    # Validate EPUB structure
    print("  • Validating EPUB container & asset manifests...")
    with zipfile.ZipFile(epub_out, "r") as z:
        namelist = z.namelist()
        images = [n for n in namelist if n.startswith("EPUB/media/") or n.endswith(".png") or n.endswith(".jpg")]
        xhtmls = [n for n in namelist if n.endswith(".xhtml")]
        print(f"    -> Contained {len(namelist)} total files in EPUB")
        print(f"    -> XHTML documents: {len(xhtmls)}")
        print(f"    -> Embedded images: {len(images)} (Target: ≥ 53 figures + cover)")
        has_nav = any("nav.xhtml" in n for n in namelist)
        has_toc = any("toc.ncx" in n for n in namelist)
        has_cover = any("cover" in n.lower() for n in namelist)
        print(f"    -> Navigation Document (nav.xhtml): {'✓ Yes' if has_nav else '✗ Missing'}")
        print(f"    -> NCX Table of Contents: {'✓ Yes' if has_toc else '✗ Missing'}")
        print(f"    -> Cover Image: {'✓ Yes' if has_cover else '✗ Missing'}")

    # Copy to destination directories
    epub_basename = os.path.basename(epub_out)
    for d in [DOCS_DIR, VAULT_PDF_DIR, BOOKS_DIR]:
        if os.path.exists(d):
            dest = os.path.join(d, epub_basename)
            shutil.copy(epub_out, dest)
            print(f"  ✓ Copied to: {dest}")

    print("\n🎉 EPUB3 EDITION COMPILED & DISTRIBUTED SUCCESSFULLY!")
    return epub_out

if __name__ == "__main__":
    build_epub()
