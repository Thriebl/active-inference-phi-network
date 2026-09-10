#!/usr/bin/env python3
"""
export_kdp_book_pdf_epub.py
Compiles English and German standalone Amazon KDP-ready 6x9 inch Academic Monograph Editions (PDF & DOCX).
Guarantees clean chapter-level page breaks with zero mid-chapter artificial page breaks.
"""

import os
import subprocess
import shutil
import re
from bs4 import BeautifulSoup

BOOK_DIR = "/home/thr/Documents/active-inference-phi-network/book"
MANUSCRIPT_EN_DIR = os.path.join(BOOK_DIR, "manuscript_en")
MANUSCRIPT_DE_DIR = os.path.join(BOOK_DIR, "manuscript_de")
BUILD_DIR = os.path.join(BOOK_DIR, "build")
DOCS_DIR = "/home/thr/Documents/active-inference-phi-network/docs"
VAULT_DIR = "/home/thr/Documents/ThRNotes/03-professional/braindumps"
VAULT_PDF_DIR = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"
BOOKS_DIR = "/home/thr/Documents/01_Books"

def merge_chapters(source_dir, output_file):
    chapter_files = sorted([f for f in os.listdir(source_dir) if f.endswith(".md")])
    merged_content = []
    for f in chapter_files:
        path = os.path.join(source_dir, f)
        with open(path, "r", encoding="utf-8") as ch:
            merged_content.append(ch.read().strip())
    # Join with standard double newline - page breaks handled exclusively by h1 in CSS
    full_text = "\n\n".join(merged_content)
    with open(output_file, "w", encoding="utf-8") as out:
        out.write(full_text)
    return full_text

def generate_toc_html(md_file, edition_name):
    """
    Generates a structured, styled HTML Table of Contents with placeholder page numbers (--)
    and returns the HTML along with the ordered list of entries.
    """
    temp_toc_file = os.path.join(BUILD_DIR, f"temp_{edition_name}_toc_raw.html")
    cmd = [
        "pandoc",
        md_file,
        "-s",
        "--table-of-contents",
        "--toc-depth=2",
        "-o", temp_toc_file
    ]
    subprocess.run(cmd, check=True)

    with open(temp_toc_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    nav = soup.find("nav", id="TOC")
    if not nav:
        return "", []

    main_title = "Table of Contents" if edition_name == "EN" else "Inhaltsverzeichnis"
    lines = []
    lines.append('<section class="toc-wrapper">')
    lines.append(f'<h1 class="toc-main-title">{main_title}</h1>')
    lines.append('<div class="toc-tree">')

    top_ul = nav.find("ul", recursive=False) or nav.ul
    entries = []

    for top_li in top_ul.find_all("li", recursive=False):
        top_a = top_li.find("a", recursive=False)
        if not top_a:
            continue
        href = top_a.get("href", "")
        target_id = href.lstrip("#")
        title_text = " ".join(top_a.text.split())

        # Skip Dedication / Widmung in TOC
        if target_id in ["dedication", "widmung"]:
            continue

        is_chapter = "chapter" in target_id or "kapitel" in target_id
        cls = "toc-h1" + (" toc-chapter" if is_chapter else "")

        lines.append(f'<div class="toc-entry {cls}">')
        lines.append(f'  <a href="{href}">')
        lines.append(f'    <span class="toc-text">{title_text}</span>')
        lines.append('    <span class="toc-dots"></span>')
        lines.append(f'    <span class="toc-pg" id="pg-{target_id}">--</span>')
        lines.append('  </a>')
        lines.append('</div>')
        entries.append((target_id, title_text, href))

        sub_ul = top_li.find("ul", recursive=False)
        if sub_ul:
            lines.append('<div class="toc-sub-group">')
            for sub_li in sub_ul.find_all("li", recursive=False):
                sub_a = sub_li.find("a", recursive=False)
                if not sub_a:
                    continue
                sub_href = sub_a.get("href", "")
                sub_id = sub_href.lstrip("#")
                sub_text = " ".join(sub_a.text.split())
                lines.append('  <div class="toc-entry toc-h2">')
                lines.append(f'    <a href="{sub_href}">')
                lines.append(f'      <span class="toc-text">{sub_text}</span>')
                lines.append('      <span class="toc-dots"></span>')
                lines.append(f'      <span class="toc-pg" id="pg-{sub_id}">--</span>')
                lines.append('    </a>')
                lines.append('  </div>')
                entries.append((sub_id, sub_text, sub_href))
            lines.append('</div>')

    lines.append('</div>')
    lines.append('</section>')
    return "\n".join(lines), entries

def resolve_toc_pages(pdf_path, entries):
    """
    Extracts text per page from the pass 1 PDF and maps each TOC entry to its exact page number.
    """
    res = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True, check=True)
    pages = res.stdout.split("\x0c")

    # Detect contiguous TOC pages starting from the TOC title page
    toc_start = 1
    for idx, p in enumerate(pages, start=1):
        if "Table of Contents" in p or "Inhaltsverzeichnis" in p:
            toc_start = idx
            break

    toc_end = toc_start
    while toc_end <= len(pages):
        p = pages[toc_end - 1]
        toc_lines = len(re.findall(r'--\s*$', p, re.MULTILINE))
        if toc_lines >= 3 or "Table of Contents" in p or "Inhaltsverzeichnis" in p:
            toc_end += 1
        else:
            break

    last_toc_page = toc_end - 1
    start_page = last_toc_page + 1
    current_search_page = start_page
    page_mapping = {}

    for target_id, raw_title, href in entries:
        norm_title = " ".join(re.sub(r'[^a-zA-Z0-9äöüÄÖÜß ]', ' ', raw_title).split())
        words = norm_title.split()
        search_snip = " ".join(words[:4]).lower() if len(words) >= 4 else norm_title.lower()

        found_page = None
        # Search forward from current page
        for p_idx in range(current_search_page, len(pages) + 1):
            p_text = pages[p_idx - 1]
            norm_p = " ".join(re.sub(r'[^a-zA-Z0-9äöüÄÖÜß ]', ' ', p_text).split()).lower()
            if search_snip in norm_p:
                found_page = p_idx
                break

        # Fallback: search anywhere in non-toc pages if not found forward
        if not found_page:
            for p_idx in range(start_page, len(pages) + 1):
                p_text = pages[p_idx - 1]
                norm_p = " ".join(re.sub(r'[^a-zA-Z0-9äöüÄÖÜß ]', ' ', p_text).split()).lower()
                if search_snip in norm_p:
                    found_page = p_idx
                    break

        if found_page:
            page_mapping[target_id] = found_page
            current_search_page = found_page
        else:
            print(f"    [WARN] Heading not matched in PDF: {raw_title} (id: {target_id})")

    return page_mapping

def make_kdp_html(title_header, body_content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title_header} - Thomas Riebl</title>
    <script>
        window.MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            }},
            svg: {{ fontCache: 'global' }},
            startup: {{ typeset: true }}
        }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'base',
            themeVariables: {{
                primaryColor: '#f0f9ff',
                primaryTextColor: '#0369a1',
                primaryBorderColor: '#0284c7',
                lineColor: '#0284c7',
                secondaryColor: '#f8fafc',
                tertiaryColor: '#ffffff',
                fontSize: '14px',
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            }},
            flowchart: {{
                htmlLabels: true,
                useMaxWidth: true,
                curve: 'basis'
            }}
        }});
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=JetBrains+Mono:wght@400;500&display=swap');
        
        @page {{
            size: 6in 9in; /* Standard Amazon KDP Trade Paperback Trim Size */
            margin-top: 18mm;
            margin-bottom: 18mm;
            margin-left: 19mm;
            margin-right: 15mm;
            @top-left {{
                content: "{title_header}";
                font-family: 'EB Garamond', serif;
                font-style: italic;
                font-size: 8.8pt;
                color: #64748b;
            }}
            @top-right {{
                content: "Thomas Riebl";
                font-family: 'EB Garamond', serif;
                font-style: italic;
                font-size: 8.8pt;
                color: #64748b;
            }}
            @bottom-center {{
                content: counter(page);
                font-family: 'EB Garamond', serif;
                font-size: 10pt;
                color: #334155;
            }}
        }}
        
        body {{
            font-family: 'EB Garamond', Garamond, Georgia, serif;
            color: #0f172a;
            line-height: 1.58;
            font-size: 12.5pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
            text-rendering: optimizeLegibility;
        }}
        
        /* Title Page Layout */
        .book-title-page {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            min-height: 86vh;
            padding: 25pt 10pt 20pt 10pt;
            box-sizing: border-box;
            page-break-before: avoid;
            page-break-after: always;
            break-after: page;
        }}
        
        .title-top-group {{
            margin-top: 25pt;
            margin-bottom: 15pt;
        }}
        
        .title-main {{
            font-family: 'Cinzel', serif;
            font-size: 20pt;
            font-weight: 800;
            letter-spacing: 1.5px;
            color: #0f172a;
            line-height: 1.25;
            margin-bottom: 8pt;
        }}
        
        .title-subtitle {{
            font-family: 'EB Garamond', serif;
            font-style: italic;
            font-size: 13pt;
            color: #0369a1;
            line-height: 1.4;
            max-width: 90%;
            margin: 0 auto;
        }}
        
        .master-equivalence-box {{
            background: #f0fdf4;
            border: 1.4px solid #16a34a;
            border-radius: 6pt;
            padding: 16pt 14pt;
            margin: 25pt auto;
            width: 96%;
            box-sizing: border-box;
            box-shadow: 0 2px 8px rgba(22, 163, 74, 0.08);
        }}
        
        .master-equivalence-box .MathJax {{
            font-size: 12.5pt !important;
            margin: 6pt 0 !important;
        }}
        
        .eq-label {{
            font-family: 'Cinzel', serif;
            font-size: 9.5pt;
            font-weight: 700;
            letter-spacing: 1px;
            color: #166534;
            margin-bottom: 4pt;
        }}
        
        .eq-subtext {{
            font-family: 'EB Garamond', serif;
            font-size: 10pt;
            font-style: italic;
            color: #15803d;
            margin-top: 5pt;
        }}
        
        .title-author-block {{
            margin-top: auto;
            padding-top: 16pt;
            border-top: 0.8px solid #cbd5e1;
            width: 80%;
            margin-bottom: 15pt;
        }}
        
        .title-author {{
            font-family: 'Cinzel', serif;
            font-size: 15pt;
            font-weight: 700;
            letter-spacing: 2px;
            color: #0f172a;
        }}
        
        .title-meta {{
            font-family: 'EB Garamond', serif;
            font-size: 10pt;
            color: #64748b;
            margin-top: 3pt;
        }}
        
        /* H1 is the ONLY element that triggers a new page (Chapters & Front Matter sections) */
        h1 {{
            font-family: 'Cinzel', serif;
            color: #0f172a;
            font-size: 18pt;
            font-weight: 700;
            text-align: center;
            border-bottom: 1.5px solid #0284c7;
            padding-bottom: 8pt;
            margin-top: 24pt;
            margin-bottom: 14pt;
            page-break-before: always;
            break-before: page;
            line-height: 1.25;
            letter-spacing: 0.5px;
        }}
        
        .dedication-page {{
            display: block;
            margin-top: 30%;
            text-align: center;
            padding: 20pt 15pt;
        }}
        
        .dedication-page h1 {{
            border-bottom: none;
            font-size: 16pt;
            margin-bottom: 25pt;
            letter-spacing: 1px;
            color: #0369a1;
        }}
        
        .dedication-page p {{
            font-style: italic;
            text-align: center;
            font-size: 13pt;
            line-height: 1.7;
            max-width: 90%;
            margin: 0 auto;
            color: #1e293b;
        }}

        /* Table of Contents Styling */
        .toc-wrapper {{
            page-break-before: always;
            break-before: page;
            page-break-after: always;
            break-after: page;
            padding-top: 10pt;
        }}

        .toc-main-title {{
            font-family: 'Cinzel', serif;
            font-size: 18pt;
            font-weight: 700;
            text-align: center;
            color: #0f172a;
            border-bottom: 1.5px solid #0284c7;
            padding-bottom: 8pt;
            margin-top: 20pt;
            margin-bottom: 20pt;
            letter-spacing: 1px;
            page-break-before: avoid;
            break-before: avoid;
        }}

        .toc-tree {{
            width: 100%;
        }}

        .toc-entry {{
            line-height: 1.38;
            page-break-inside: avoid;
            break-inside: avoid;
        }}

        .toc-entry a {{
            display: flex;
            align-items: baseline;
            text-decoration: none;
            color: inherit;
            width: 100%;
        }}

        .toc-h1 {{
            margin-top: 8pt;
            margin-bottom: 2.5pt;
            font-family: 'EB Garamond', serif;
            font-size: 11pt;
            font-weight: 700;
            color: #0f172a;
        }}

        .toc-h1.toc-chapter a .toc-text {{
            color: #0369a1;
            font-family: 'Cinzel', serif;
            font-size: 9.8pt;
            font-weight: 700;
            letter-spacing: 0.2px;
        }}

        .toc-sub-group {{
            margin-bottom: 5pt;
        }}

        .toc-h2 {{
            margin-left: 14pt;
            margin-top: 2pt;
            margin-bottom: 2pt;
            font-family: 'EB Garamond', serif;
            font-size: 9.5pt;
            font-weight: 400;
            color: #334155;
        }}

        .toc-text {{
            flex: 0 1 auto;
            max-width: 82%;
        }}

        .toc-dots {{
            flex: 1 1 auto;
            border-bottom: 1px dotted #94a3b8;
            margin: 0 5pt;
            min-width: 12pt;
            position: relative;
            top: -3px;
        }}

        .toc-pg {{
            flex: 0 0 auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 9pt;
            color: #475569;
            font-weight: 500;
            text-align: right;
            min-width: 18pt;
        }}
        
        /* Subheadings must NEVER trigger page breaks and must not be orphaned */
        h2 {{
            font-family: 'EB Garamond', serif;
            color: #0369a1;
            font-size: 15pt;
            font-weight: 700;
            margin-top: 20pt;
            margin-bottom: 6pt;
            border-bottom: 0.5px solid #e2e8f0;
            padding-bottom: 2pt;
            page-break-before: auto;
            break-before: auto;
            page-break-after: avoid;
            break-after: avoid;
        }}
        
        h3 {{
            font-family: 'EB Garamond', serif;
            color: #0284c7;
            font-size: 13pt;
            font-weight: 600;
            margin-top: 14pt;
            margin-bottom: 4pt;
            page-break-before: auto;
            break-before: auto;
            page-break-after: avoid;
            break-after: avoid;
        }}
        
        p {{
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: justify;
            text-justify: inter-word;
            orphans: 2;
            widows: 2;
        }}
        
        ul, ol {{
            margin-top: 0;
            margin-bottom: 8pt;
            padding-left: 18pt;
        }}
        
        li {{
            margin-bottom: 3pt;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            font-size: 9.8pt;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        th, td {{
            padding: 5pt 7pt;
            border: 0.8px solid #cbd5e1;
            text-align: left;
        }}
        
        th {{
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        
        blockquote {{
            margin: 12pt 0;
            padding: 8pt 14pt;
            background-color: #f0fdf4;
            border-left: 3.5px solid #16a34a;
            color: #166534;
            font-size: 11.2pt;
            border-radius: 0 4px 4px 0;
            font-style: italic;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        .mermaid {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 14pt auto;
            background: #ffffff;
            padding: 10pt 8pt;
            border: 0.8px solid #cbd5e1;
            border-radius: 6pt;
            page-break-inside: avoid;
            break-inside: avoid;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .mermaid svg {{
            max-width: 100% !important;
            height: auto !important;
        }}
        
        .mermaid svg text,
        .mermaid svg .nodeLabel,
        .mermaid svg .label {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            line-height: 1.35 !important;
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 12pt auto;
            border: 0.8px solid #cbd5e1;
            border-radius: 4pt;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        hr {{
            border: none;
            border-top: 0.8px solid #e2e8f0;
            margin: 12pt 0;
            page-break-before: auto;
            break-before: auto;
            page-break-after: auto;
            break-after: auto;
        }}
        
        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 9.2pt;
            background-color: #f1f5f9;
            padding: 1.5px 4px;
            border-radius: 3px;
            color: #0f172a;
        }}
        
        pre {{
            background-color: #0f172a;
            color: #f8fafc;
            padding: 10pt;
            border-radius: 4pt;
            font-family: 'JetBrains Mono', monospace;
            font-size: 8.6pt;
            overflow-x: auto;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
    </style>
</head>
<body>
{body_content}
</body>
</html>
"""

def build_edition(edition_name, md_file, title_header, pdf_out, docx_out):
    print(f"\n=======================================================")
    print(f"=== Compiling Edition: {edition_name} ===")
    print(f"=======================================================")
    
    # 1. Word DOCX
    print("  • Generating DOCX...")
    cmd_docx = [
        "pandoc",
        md_file,
        "-o", docx_out,
        "--from=markdown+tex_math_dollars+yaml_metadata_block",
        "--resource-path=/home/thr/Documents/active-inference-phi-network/images:/home/thr/Documents/active-inference-phi-network",
        "--table-of-contents",
        "--toc-depth=2"
    ]
    subprocess.run(cmd_docx, check=False)
    
    docx_basename = os.path.basename(docx_out)
    shutil.copy(docx_out, os.path.join(DOCS_DIR, docx_basename))
    
    # 2. HTML to PDF via Chrome (2-Pass Table of Contents Engine)
    print("  • Generating HTML & Table of Contents...")
    temp_html_body = os.path.join(BUILD_DIR, f"temp_{edition_name}_body.html")
    cmd_pandoc = [
        "pandoc",
        md_file,
        "-o", temp_html_body,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--resource-path=/home/thr/Documents/active-inference-phi-network/images:/home/thr/Documents/active-inference-phi-network",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(cmd_pandoc, check=True)
    
    with open(temp_html_body, "r", encoding="utf-8") as f:
        html_body = f.read()
        
    html_body = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>', r'<div class="mermaid">\1</div>', html_body, flags=re.DOTALL)
    html_body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<div class="mermaid">\1</div>', html_body, flags=re.DOTALL)
    html_body = html_body.replace('../images/', '/home/thr/Documents/active-inference-phi-network/images/')
    html_body = html_body.replace('src="images/', 'src="/home/thr/Documents/active-inference-phi-network/images/')

    toc_html, entries = generate_toc_html(md_file, edition_name)

    m = re.search(r'(<section\s+[^>]*class="[^"]*dedication-page[^"]*"[^>]*>.*?</section>)', html_body, re.DOTALL)
    if m:
        dedication_block = m.group(1)
        html_body_with_toc = html_body.replace(dedication_block, dedication_block + "\n" + toc_html)
    else:
        html_body_with_toc = toc_html + "\n" + html_body

    # Pass 1: Render intermediate PDF to determine exact page numbers
    print("  • Rendering Pass 1 PDF to calculate exact page numbers...")
    pass1_html = make_kdp_html(title_header, html_body_with_toc)
    temp_pass1_html = os.path.join(BUILD_DIR, f"temp_{edition_name}_pass1.html")
    temp_pass1_pdf = os.path.join(BUILD_DIR, f"temp_{edition_name}_pass1.pdf")
    with open(temp_pass1_html, "w", encoding="utf-8") as f:
        f.write(pass1_html)

    cmd_pdf_pass1 = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=12000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={temp_pass1_pdf}",
        temp_pass1_html
    ]
    subprocess.run(cmd_pdf_pass1, check=True)

    # Map exact pages
    print("  • Mapping TOC entries to exact printed page numbers...")
    page_map = resolve_toc_pages(temp_pass1_pdf, entries)
    print(f"    -> Successfully mapped {len(page_map)} / {len(entries)} entries")

    # Pass 2: Inject exact page numbers into final HTML and render final PDF
    html_body_final = html_body_with_toc
    for target_id, page_num in page_map.items():
        old_span = f'<span class="toc-pg" id="pg-{target_id}">--</span>'
        new_span = f'<span class="toc-pg" id="pg-{target_id}">{page_num}</span>'
        html_body_final = html_body_final.replace(old_span, new_span)

    print("  • Rendering Pass 2 (Final Print-Ready PDF with verified TOC)...")
    final_html = make_kdp_html(title_header, html_body_final)
    render_file = os.path.join(BUILD_DIR, f"render_{edition_name}.html")
    with open(render_file, "w", encoding="utf-8") as f:
        f.write(final_html)

    cmd_pdf_final = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=12000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_out}",
        render_file
    ]
    subprocess.run(cmd_pdf_final, check=True)

    pdf_basename = os.path.basename(pdf_out)
    shutil.copy(pdf_out, os.path.join(DOCS_DIR, pdf_basename))
    shutil.copy(pdf_out, os.path.join(VAULT_PDF_DIR, pdf_basename))
    if os.path.exists(BOOKS_DIR):
        shutil.copy(pdf_out, os.path.join(BOOKS_DIR, pdf_basename))
    print(f"✓ Created PDF: {pdf_out}")

def main():
    # 1. English Standalone Edition
    en_md = os.path.join(BUILD_DIR, "CIF_Monograph_EN.md")
    merge_chapters(MANUSCRIPT_EN_DIR, en_md)
    en_pdf = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_EN_6x9.pdf")
    en_docx = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_EN_6x9.docx")
    build_edition("EN", en_md, "The Conative-Integrative Framework", en_pdf, en_docx)
    
    # 2. German Standalone Edition
    de_md = os.path.join(BUILD_DIR, "CIF_Monograph_DE.md")
    merge_chapters(MANUSCRIPT_DE_DIR, de_md)
    de_pdf = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_DE_6x9.pdf")
    de_docx = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_DE_6x9.docx")
    build_edition("DE", de_md, "Das Konativ-Integrative Framework", de_pdf, de_docx)
    
    print("\n🎉 STANDALONE EN AND DE MONOGRAPH EDITIONS COMPILED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
