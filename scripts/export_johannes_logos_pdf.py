#!/usr/bin/env python3
"""
export_johannes_logos_pdf.py
Compiles high-resolution PDF and Word (.docx) versions of
'Johannes 1,1–1,5: Griechischer Originaltext, Interlinearübersetzung & Die Ontologie des Logos'
by Thomas Riebl.
"""

import os
import sys
import re
import subprocess
import shutil

def export_paper():
    repo_dir = "/home/thr/Documents/active-inference-phi-network"
    docs_dir = os.path.join(repo_dir, "docs")
    out_dir = "/home/thr/Documents"
    md_source = os.path.join(docs_dir, "2026-09-05-johannes-1-1-5-logos-interlinear-und-philosophie.md")

    pdf_out = os.path.join(out_dir, "Johannes_1_1-5_Logos_Interlinear_und_Philosophie_Thomas_Riebl.pdf")
    docx_out = os.path.join(out_dir, "Johannes_1_1-5_Logos_Interlinear_und_Philosophie_Thomas_Riebl.docx")
    vault_pdf = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF/2026-09-05-johannes-1-1-5-logos-interlinear-und-philosophie.pdf"

    print("=== Exporting Johannes 1:1-5 Logos Essay ===")
    
    # 1. Generate DOCX with Pandoc
    pandoc_docx = [
        "pandoc",
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
    temp_body = "/tmp/johannes_logos_body.html"
    pandoc_html = [
        "pandoc",
        md_source,
        "-o", temp_body,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(pandoc_html, check=True)

    with open(temp_body, "r", encoding="utf-8") as f:
        html_body = f.read()

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

    template_head = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Johannes 1,1–1,5 & Der Logos - Thomas Riebl</title>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
                processEscapes: true,
                processEnvironments: true
            },
            svg: { fontCache: 'global' },
            startup: { typeset: true }
        };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'base',
            themeVariables: {
                primaryColor: '#f0fdf4',
                primaryTextColor: '#166534',
                primaryBorderColor: '#16a34a',
                lineColor: '#16a34a',
                secondaryColor: '#f8fafc',
                tertiaryColor: '#ffffff',
                fontSize: '14px',
                fontFamily: 'EB Garamond, Georgia, serif'
            }
        });
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap');

        @page {
            size: A4 portrait;
            margin: 20mm 20mm 20mm 20mm;
            @bottom-right {
                content: counter(page);
                font-family: 'EB Garamond', Georgia, serif;
                font-size: 9pt;
                color: #64748b;
            }
            @bottom-left {
                content: "Thomas Riebl • Johannes 1,1–1,5: Die Ontologie des Logos";
                font-family: 'EB Garamond', Georgia, serif;
                font-size: 9pt;
                color: #64748b;
            }
        }
        body {
            font-family: 'EB Garamond', Georgia, serif;
            color: #0f172a;
            line-height: 1.6;
            font-size: 11pt;
            margin: 0;
            padding: 0;
        }
        h1 {
            font-family: 'Cinzel', serif;
            color: #0f172a;
            font-size: 18pt;
            font-weight: 800;
            border-bottom: 2px solid #16a34a;
            padding-bottom: 6pt;
            margin-top: 0;
            margin-bottom: 10pt;
            line-height: 1.3;
        }
        h2 {
            font-family: 'Cinzel', serif;
            color: #166534;
            font-size: 13pt;
            font-weight: 700;
            margin-top: 16pt;
            margin-bottom: 6pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3pt;
        }
        h3 {
            color: #0f172a;
            font-size: 11.5pt;
            font-weight: 700;
            margin-top: 12pt;
            margin-bottom: 4pt;
        }
        p {
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: justify;
        }
        .mermaid {
            text-align: center;
            margin: 12pt auto;
            page-break-inside: avoid;
        }
        .mermaid svg {
            max-height: 280px !important;
            height: auto !important;
            max-width: 100% !important;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
            font-size: 9.5pt;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 6px 10px;
            text-align: left;
        }
        th {
            background-color: #f0fdf4;
            color: #166534;
            font-weight: 700;
        }
        blockquote {
            border-left: 3.5px solid #16a34a;
            margin: 10pt 0;
            padding: 8pt 14pt;
            background-color: #f0fdf4;
            color: #166534;
            font-style: italic;
            border-radius: 0 6px 6px 0;
        }
        hr {
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 16pt 0;
        }
    </style>
</head>
<body>
"""
    template_foot = """
</body>
</html>
"""
    full_html = template_head + html_body + template_foot

    temp_html = "/tmp/johannes_logos_render.html"
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
