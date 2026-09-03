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

BOOK_DIR = "/home/thr/Documents/active-inference-phi-network/book"
MANUSCRIPT_EN_DIR = os.path.join(BOOK_DIR, "manuscript_en")
MANUSCRIPT_DE_DIR = os.path.join(BOOK_DIR, "manuscript_de")
BUILD_DIR = os.path.join(BOOK_DIR, "build")
DOCS_DIR = "/home/thr/Documents/active-inference-phi-network/docs"
VAULT_DIR = "/home/thr/Documents/ThRNotes/03-professional/braindumps"
VAULT_PDF_DIR = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"

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
    
    # 2. HTML to PDF via Chrome
    print("  • Generating HTML & rendering 6x9 Print PDF...")
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
    
    kdp_html = f"""<!DOCTYPE html>
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
                primaryColor: '#e0f2fe',
                primaryTextColor: '#0369a1',
                primaryBorderColor: '#0284c7',
                lineColor: '#0284c7',
                secondaryColor: '#f8fafc',
                tertiaryColor: '#ffffff',
                fontSize: '12px',
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
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
                font-size: 8pt;
                color: #64748b;
            }}
            @top-right {{
                content: "Thomas Riebl";
                font-family: 'EB Garamond', serif;
                font-style: italic;
                font-size: 8pt;
                color: #64748b;
            }}
            @bottom-center {{
                content: counter(page);
                font-family: 'EB Garamond', serif;
                font-size: 9pt;
                color: #334155;
            }}
        }}
        
        body {{
            font-family: 'EB Garamond', Garamond, Georgia, serif;
            color: #0f172a;
            line-height: 1.55;
            font-size: 10.2pt;
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
            padding: 5pt 0 10pt 0;
            box-sizing: border-box;
            page-break-before: avoid;
            page-break-after: always;
            break-after: page;
        }}
        
        .title-top-group {{
            margin-top: 10pt;
            margin-bottom: 8pt;
        }}
        
        .title-main {{
            font-family: 'Cinzel', serif;
            font-size: 16.5pt;
            font-weight: 800;
            letter-spacing: 1.2px;
            color: #0f172a;
            line-height: 1.22;
            margin-bottom: 6pt;
        }}
        
        .title-subtitle {{
            font-family: 'EB Garamond', serif;
            font-style: italic;
            font-size: 10.8pt;
            color: #0369a1;
            line-height: 1.35;
            max-width: 90%;
            margin: 0 auto;
        }}
        
        .title-image-box {{
            margin: 8pt auto;
            max-width: 88%;
            border: 1.2px solid #1e3a8a;
            border-radius: 6pt;
            padding: 8pt;
            background: #0b192c; /* Dunkelblauer Hintergrund */
            box-shadow: 0 3px 10px rgba(11, 25, 44, 0.2);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .title-cover-image {{
            max-height: 150pt;
            width: auto;
            max-width: 100%;
            display: block;
            margin: 0 auto;
            border-radius: 4pt;
            border: 0.8px solid #1e40af;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.35);
        }}
        
        .title-image-caption {{
            font-family: 'EB Garamond', serif;
            font-size: 8.3pt;
            font-style: italic;
            color: #93c5fd; /* Sanftes Hellblau auf dunkelblauem Grund */
            margin-top: 4pt;
            text-align: center;
        }}
        
        .master-equivalence-box {{
            background: #f0fdf4;
            border: 1.2px solid #16a34a;
            border-radius: 5pt;
            padding: 6pt 10pt;
            margin: 8pt auto;
            width: 96%;
            box-sizing: border-box;
        }}
        
        .master-equivalence-box .mjx-chtml {{
            font-size: 102% !important;
            margin: 4pt 0 !important;
        }}
        
        .eq-label {{
            font-family: 'Cinzel', serif;
            font-size: 8pt;
            font-weight: 700;
            letter-spacing: 0.8px;
            color: #166534;
            margin-bottom: 2pt;
        }}
        
        .eq-subtext {{
            font-family: 'EB Garamond', serif;
            font-size: 8pt;
            font-style: italic;
            color: #15803d;
            margin-top: 2pt;
        }}
        
        .title-author-block {{
            margin-top: auto;
            padding-top: 8pt;
            border-top: 0.8px solid #e2e8f0;
            width: 80%;
        }}
        
        .title-author {{
            font-family: 'Cinzel', serif;
            font-size: 12.5pt;
            font-weight: 700;
            letter-spacing: 1.5px;
            color: #0f172a;
        }}
        
        .title-meta {{
            font-family: 'EB Garamond', serif;
            font-size: 8.8pt;
            color: #64748b;
            margin-top: 2pt;
        }}
        
        /* H1 is the ONLY element that triggers a new page (Chapters & Front Matter sections) */
        h1 {{
            font-family: 'Cinzel', serif;
            color: #0f172a;
            font-size: 15.5pt;
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
            margin-top: 32%;
            text-align: center;
            padding: 20pt 15pt;
        }}
        
        .dedication-page h1 {{
            border-bottom: none;
            font-size: 14pt;
            margin-bottom: 25pt;
            letter-spacing: 1px;
            color: #0369a1;
        }}
        
        .dedication-page p {{
            font-style: italic;
            text-align: center;
            font-size: 11pt;
            line-height: 1.7;
            max-width: 90%;
            margin: 0 auto;
            color: #1e293b;
        }}
        
        /* Subheadings must NEVER trigger page breaks and must not be orphaned */
        h2 {{
            font-family: 'EB Garamond', serif;
            color: #0369a1;
            font-size: 12.5pt;
            font-weight: 700;
            margin-top: 18pt;
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
            font-size: 10.8pt;
            font-weight: 600;
            margin-top: 12pt;
            margin-bottom: 4pt;
            page-break-before: auto;
            break-before: auto;
            page-break-after: avoid;
            break-after: avoid;
        }}
        
        p {{
            margin-top: 0;
            margin-bottom: 7pt;
            text-align: justify;
            text-justify: inter-word;
            orphans: 2;
            widows: 2;
        }}
        
        ul, ol {{
            margin-top: 0;
            margin-bottom: 7pt;
            padding-left: 16pt;
        }}
        
        li {{
            margin-bottom: 2.5pt;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
            font-size: 8.2pt;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        th, td {{
            padding: 4.5pt 6pt;
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
            margin: 10pt 0;
            padding: 7pt 12pt;
            background-color: #f0fdf4;
            border-left: 3.5px solid #16a34a;
            color: #166534;
            font-size: 9.3pt;
            border-radius: 0 4px 4px 0;
            font-style: italic;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 10pt 0;
            background: #ffffff;
            padding: 6pt;
            border: 0.8px solid #e2e8f0;
            border-radius: 4pt;
            page-break-inside: avoid;
            break-inside: avoid;
            transform: scale(0.92);
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10pt auto;
            border: 0.8px solid #cbd5e1;
            border-radius: 4pt;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
        
        hr {{
            border: none;
            border-top: 0.8px solid #e2e8f0;
            margin: 10pt 0;
            page-break-before: auto;
            break-before: auto;
            page-break-after: auto;
            break-after: auto;
        }}
        
        code {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 7.8pt;
            background-color: #f1f5f9;
            padding: 1.5px 3.5px;
            border-radius: 3px;
            color: #0f172a;
        }}
        
        pre {{
            background-color: #0f172a;
            color: #f8fafc;
            padding: 8pt;
            border-radius: 4pt;
            font-family: 'JetBrains Mono', monospace;
            font-size: 7.2pt;
            overflow-x: auto;
            page-break-inside: avoid;
            break-inside: avoid;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""
    
    render_file = os.path.join(BUILD_DIR, f"render_{edition_name}.html")
    with open(render_file, "w", encoding="utf-8") as f:
        f.write(kdp_html)
        
    cmd_pdf = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=12000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_out}",
        render_file
    ]
    subprocess.run(cmd_pdf, check=True)
    
    pdf_basename = os.path.basename(pdf_out)
    shutil.copy(pdf_out, os.path.join(DOCS_DIR, pdf_basename))
    shutil.copy(pdf_out, os.path.join(VAULT_PDF_DIR, pdf_basename))
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
