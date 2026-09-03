#!/usr/bin/env python3
"""
export_kdp_book_pdf_epub.py
Compiles all chapter manuscripts into a unified Amazon KDP-ready 6x9 inch Academic Monograph (PDF & DOCX).
"""

import os
import subprocess
import shutil
import re

BOOK_DIR = "/home/thr/Documents/active-inference-phi-network/book"
MANUSCRIPT_DIR = os.path.join(BOOK_DIR, "manuscript")
BUILD_DIR = os.path.join(BOOK_DIR, "build")
DOCS_DIR = "/home/thr/Documents/active-inference-phi-network/docs"
VAULT_DIR = "/home/thr/Documents/ThRNotes/03-professional/braindumps"
VAULT_PDF_DIR = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"

MERGED_MD = os.path.join(BUILD_DIR, "CIF_Monograph_Complete.md")
PDF_OUT = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_6x9.pdf")
DOCX_OUT = os.path.join(BUILD_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_6x9.docx")

def merge_manuscripts():
    print("=== 1. Merging Chapter Manuscripts ===")
    chapter_files = sorted([
        f for f in os.listdir(MANUSCRIPT_DIR) if f.endswith(".md")
    ])
    
    merged_content = []
    for f in chapter_files:
        path = os.path.join(MANUSCRIPT_DIR, f)
        print(f"  • Adding: {f}")
        with open(path, "r", encoding="utf-8") as ch:
            content = ch.read()
            merged_content.append(content)
            
    full_text = "\n\n\\newpage\n\n".join(merged_content)
    
    with open(MERGED_MD, "w", encoding="utf-8") as out:
        out.write(full_text)
        
    # Copy to docs and vault
    shutil.copy(MERGED_MD, os.path.join(DOCS_DIR, "The_Conative_Integrative_Framework_Book_Manuscript_Thomas_Riebl.md"))
    shutil.copy(MERGED_MD, os.path.join(VAULT_DIR, "2026-09-03-the-conative-integrative-framework-complete-book-manuscript-thomas-riebl-en.md"))
    print(f"✓ Created complete merged manuscript: {MERGED_MD}")

def generate_docx():
    print("\n=== 2. Generating Word (.docx) for Amazon KDP / Review ===")
    cmd_docx = [
        "pandoc",
        MERGED_MD,
        "-o", DOCX_OUT,
        "--from=markdown+tex_math_dollars+yaml_metadata_block",
        "--table-of-contents",
        "--toc-depth=2"
    ]
    subprocess.run(cmd_docx, check=False)
    if os.path.exists(DOCX_OUT):
        shutil.copy(DOCX_OUT, os.path.join(DOCS_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_6x9.docx"))
        print(f"✓ Created Word DOCX: {DOCX_OUT}")

def generate_kdp_pdf():
    print("\n=== 3. Rendering Amazon KDP Print-Ready 6x9 inch PDF via Headless Chrome ===")
    html_body_temp = os.path.join(BUILD_DIR, "temp_book_body.html")
    
    cmd_pandoc = [
        "pandoc",
        MERGED_MD,
        "-o", html_body_temp,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(cmd_pandoc, check=True)
    
    with open(html_body_temp, "r", encoding="utf-8") as f:
        html_body = f.read()
        
    # Convert Mermaid code blocks into <div class="mermaid">
    html_body = re.sub(
        r'<pre class="mermaid"><code>(.*?)</code></pre>',
        r'<div class="mermaid">\1</div>',
        html_body,
        flags=re.DOTALL
    )
    html_body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<div class="mermaid">\1</div>',
        html_body,
        flags=re.DOTALL
    )
    
    # Fix relative image links: ../images/ -> /home/thr/Documents/active-inference-phi-network/images/
    html_body = html_body.replace('../images/', '/home/thr/Documents/active-inference-phi-network/images/')
    
    kdp_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Conative-Integrative Framework - Thomas Riebl</title>
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
                content: "The Conative-Integrative Framework";
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
            font-size: 16pt;
            font-weight: 700;
            text-align: center;
            border-bottom: 1.5px solid #0284c7;
            padding-bottom: 8pt;
            margin-top: 24pt;
            margin-bottom: 14pt;
            page-break-before: always;
            line-height: 1.25;
            letter-spacing: 0.5px;
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
    
    html_render_file = os.path.join(BUILD_DIR, "temp_book_render.html")
    with open(html_render_file, "w", encoding="utf-8") as f:
        f.write(kdp_html)
        
    cmd_pdf = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=12000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_OUT}",
        html_render_file
    ]
    subprocess.run(cmd_pdf, check=True)
    
    if os.path.exists(PDF_OUT):
        shutil.copy(PDF_OUT, os.path.join(DOCS_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_6x9.pdf"))
        shutil.copy(PDF_OUT, os.path.join(VAULT_PDF_DIR, "The_Conative_Integrative_Framework_Book_Thomas_Riebl_6x9.pdf"))
        print(f"✓ SUCCESS! Created Amazon KDP Print PDF (6x9 in):\n  - {PDF_OUT}")

if __name__ == "__main__":
    merge_manuscripts()
    generate_docx()
    generate_kdp_pdf()
