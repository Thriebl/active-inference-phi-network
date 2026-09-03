#!/usr/bin/env python3
"""
export_kdp_book_pdf_epub.py
Compiles English, German, and Bilingual Amazon KDP-ready 6x9 inch Academic Monograph Editions (PDF & DOCX).
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
            merged_content.append(ch.read())
    full_text = "\n\n\\newpage\n\n".join(merged_content)
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
        "--table-of-contents",
        "--toc-depth=2"
    ]
    subprocess.run(cmd_docx, check=False)
    
    # Copy DOCX to docs
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
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(cmd_pandoc, check=True)
    
    with open(temp_html_body, "r", encoding="utf-8") as f:
        html_body = f.read()
        
    html_body = re.sub(r'<pre class="mermaid"><code>(.*?)</code></pre>', r'<div class="mermaid">\1</div>', html_body, flags=re.DOTALL)
    html_body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', r'<div class="mermaid">\1</div>', html_body, flags=re.DOTALL)
    html_body = html_body.replace('../images/', '/home/thr/Documents/active-inference-phi-network/images/')
    
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
            page-break-before: always;
            page-break-after: always;
            break-before: page;
            break-after: page;
            display: block;
            margin-top: 35%;
            text-align: center;
            padding: 20pt 15pt;
        }}
        
        .dedication-page h1 {{
            border-bottom: none;
            page-break-before: avoid;
            break-before: avoid;
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
        
        h2 {{
            font-family: 'EB Garamond', serif;
            color: #0369a1;
            font-size: 12.5pt;
            font-weight: 700;
            margin-top: 18pt;
            margin-bottom: 6pt;
            border-bottom: 0.5px solid #e2e8f0;
            padding-bottom: 2pt;
        }}
        
        h3 {{
            font-family: 'EB Garamond', serif;
            color: #0284c7;
            font-size: 10.8pt;
            font-weight: 600;
            margin-top: 12pt;
            margin-bottom: 4pt;
        }}
        
        p {{
            margin-top: 0;
            margin-bottom: 7pt;
            text-align: justify;
            text-justify: inter-word;
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
        }}
        
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 12pt 0;
            background: #ffffff;
            padding: 6pt;
            border: 0.8px solid #e2e8f0;
            border-radius: 4pt;
            page-break-inside: avoid;
            transform: scale(0.92);
        }}
        
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 12pt auto;
            border: 0.8px solid #cbd5e1;
            border-radius: 4pt;
        }}
        
        hr {{
            border: none;
            border-top: 0.8px solid #e2e8f0;
            margin: 12pt 0;
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
    # 1. English Edition
    en_md = os.path.join(BUILD_DIR, "CIF_Monograph_EN.md")
    en_text = merge_chapters(MANUSCRIPT_EN_DIR, en_md)
    en_pdf = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_EN_6x9.pdf")
    en_docx = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_EN_6x9.docx")
    build_edition("EN", en_md, "The Conative-Integrative Framework", en_pdf, en_docx)
    
    # 2. German Edition
    de_md = os.path.join(BUILD_DIR, "CIF_Monograph_DE.md")
    de_text = merge_chapters(MANUSCRIPT_DE_DIR, de_md)
    de_pdf = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_DE_6x9.pdf")
    de_docx = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_DE_6x9.docx")
    build_edition("DE", de_md, "Das Konativ-Integrative Framework", de_pdf, de_docx)
    
    # 3. Bilingual Master Edition
    bilingual_md = os.path.join(BUILD_DIR, "CIF_Monograph_Bilingual_EN_DE.md")
    bilingual_header = """---
title: "The Conative-Integrative Framework (CIF) / Das Konativ-Integrative Framework"
subtitle: "Bilingual Complete Edition / Zweisprachige Gesamtausgabe (English & Deutsch)"
author: "Thomas Riebl"
date: "2026"
geometry: "paperwidth=6in,paperheight=9in,margin=0.75in,bindingoffset=0.25in"
fontsize: "10.5pt"
linestretch: "1.18"
documentclass: "book"
toc: true
toc-depth: 2
---

# Bilingual Edition Note / Zweisprachige Edition {-}

*This volume contains the complete unabridged monograph in both English and German.*  
*Dieser Band enthält die vollständige, ungekürzte Monographie in englischer und deutscher Sprache.*

---

# Part I: English Edition {-}

"""
    with open(bilingual_md, "w", encoding="utf-8") as f:
        f.write(bilingual_header + "\n\n" + en_text + "\n\n\\newpage\n\n# Part II: Deutsche Ausgabe {-}\n\n" + de_text)
        
    bilingual_pdf = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Bilingual_Edition_Thomas_Riebl_6x9.pdf")
    bilingual_docx = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Bilingual_Edition_Thomas_Riebl_6x9.docx")
    build_edition("Bilingual", bilingual_md, "The Conative-Integrative Framework (Bilingual)", bilingual_pdf, bilingual_docx)
    
    print("\n🎉 ALL THREE EDITIONS SUCCESSFULLY COMPILED!")

if __name__ == "__main__":
    main()
