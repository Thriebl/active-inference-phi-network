#!/usr/bin/env python3
"""
export_time_and_consciousness_pdf_docx.py
Compiles high-resolution PDF and Word (.docx) versions of
'Time and Consciousness: The Temporal Mechanics of the Conscious Mind' by Thomas Riebl.
"""

import os
import sys
import re
import subprocess
import shutil

def export_paper():
    repo_dir = "/home/thr/Documents/time-and-consciousness"
    docs_dir = os.path.join(repo_dir, "docs")
    out_dir = "/home/thr/Documents"
    md_source = os.path.join(docs_dir, "2026-09-02-time-and-consciousness-the-temporal-mechanics-of-the-conscious-mind-en.md")

    pdf_out = os.path.join(out_dir, "The_Temporal_Mechanics_of_Consciousness_Thomas_Riebl.pdf")
    docx_out = os.path.join(out_dir, "The_Temporal_Mechanics_of_Consciousness_Thomas_Riebl.docx")
    vault_pdf = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF/2026-09-02-time-and-consciousness-the-temporal-mechanics-of-the-conscious-mind-en.pdf"

    print("=== Exporting Time and Consciousness Paper ===")
    
    # 1. Generate DOCX with Pandoc
    pandoc_docx = [
        "/home/thr/anaconda3/bin/pandoc",
        md_source,
        "-o", docx_out,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=docx"
    ]
    print("Generating Word (.docx)...")
    subprocess.run(pandoc_docx, check=True)
    shutil.copy(docx_out, docs_dir)
    print(f"SUCCESS! Created DOCX: {docx_out}")

    # 2. Render HTML + MathJax 3 + Mermaid for Headless Chrome PDF
    pandoc_html = [
        "/home/thr/anaconda3/bin/pandoc",
        md_source,
        "-o", "/tmp/time_consciousness_body.html",
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(pandoc_html, check=True)

    with open("/tmp/time_consciousness_body.html", "r", encoding="utf-8") as f:
        html_body = f.read()

    # Convert ```mermaid code blocks into <pre class="mermaid">
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

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Time and Consciousness - Thomas Riebl</title>
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
                secondaryColor: '#f1f5f9',
                tertiaryColor: '#ffffff',
                fontSize: '15px',
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
            }}
        }});
    </script>
    <style>
        @page {{
            size: A4 portrait;
            margin: 18mm 18mm 18mm 18mm;
            @bottom-right {{
                content: counter(page);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                font-size: 8.5pt;
                color: #64748b;
            }}
            @bottom-left {{
                content: "Thomas Riebl • Time and Consciousness [CIF]";
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                font-size: 8.5pt;
                color: #64748b;
            }}
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #0f172a;
            line-height: 1.55;
            font-size: 10pt;
            margin: 0;
            padding: 0;
        }}
        h1 {{
            color: #0f172a;
            font-size: 20pt;
            font-weight: 800;
            border-bottom: 2.5px solid #0284c7;
            padding-bottom: 5pt;
            margin-top: 0;
            margin-bottom: 6pt;
        }}
        h2 {{
            color: #0369a1;
            font-size: 13pt;
            font-weight: 700;
            margin-top: 14pt;
            margin-bottom: 6pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3pt;
        }}
        h3 {{
            color: #0f172a;
            font-size: 11pt;
            font-weight: 700;
            margin-top: 10pt;
            margin-bottom: 4pt;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 7pt;
            text-align: justify;
        }}
        .mermaid {{
            text-align: center;
            margin: 10pt auto;
            page-break-inside: avoid;
        }}
        .mermaid svg {{
            max-height: 280px !important;
            height: auto !important;
            max-width: 100% !important;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8pt 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
            text-align: left;
        }}
        th {{
            background-color: #f1f5f9;
            color: #0f172a;
            font-weight: 700;
        }}
        blockquote {{
            border-left: 4px solid #0284c7;
            margin: 8pt 0;
            padding: 6pt 10pt;
            background-color: #f0f9ff;
            color: #0369a1;
            font-style: normal;
            border-radius: 0 6px 6px 0;
        }}
        code {{
            font-family: ui-monospace, Menlo, Monaco, Consolas, monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            padding: 2px 4px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""

    temp_html = "/tmp/time_consciousness_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("Rendering PDF with Headless Chrome...")
    chrome_cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf_out}",
        temp_html
    ]
    subprocess.run(chrome_cmd, check=True)
    shutil.copy(pdf_out, docs_dir)
    shutil.copy(pdf_out, vault_pdf)
    print(f"SUCCESS! Exported PDF to:\n  - {pdf_out}\n  - {os.path.join(docs_dir, os.path.basename(pdf_out))}\n  - {vault_pdf}")

if __name__ == "__main__":
    export_paper()
