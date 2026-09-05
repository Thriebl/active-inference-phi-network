#!/usr/bin/env python3
"""
export_markov_blankets_pdf.py
Compiles high-resolution, printable PDF and Word (.docx) versions of
'Thermodynamische und informationstheoretische Begründung der Entstehung von Markov-Blankets in Quantensystemen'
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
    vault_notes = "/home/thr/Documents/ThRNotes/03-professional/braindumps"
    vault_pdf_dir = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"
    out_dir = "/home/thr/Documents"

    artifact_src = "/home/thr/.gemini/antigravity-cli/brain/8260f0bb-77b6-429e-90cf-c04cc8aa02fd/quanten_markov_blankets_energetische_guenstigkeit.md"
    doc_md = os.path.join(docs_dir, "2026-09-05-quanten-markov-blankets-energetische-guenstigkeit.md")
    vault_md = os.path.join(vault_notes, "2026-09-05-quanten-markov-blankets-energetische-guenstigkeit.md")

    pdf_out = os.path.join(out_dir, "Quanten_Markov_Blankets_vs_Maximale_Entropie_Thomas_Riebl.pdf")
    docx_out = os.path.join(out_dir, "Quanten_Markov_Blankets_vs_Maximale_Entropie_Thomas_Riebl.docx")
    vault_pdf = os.path.join(vault_pdf_dir, "2026-09-05-quanten-markov-blankets-energetische-guenstigkeit.pdf")

    print("=== Exporting Quanten-Markov-Blankets Essay ===")
    
    # 0. Copy markdown to docs and vault
    shutil.copy(artifact_src, doc_md)
    shutil.copy(artifact_src, vault_md)
    print(f"Copied markdown source to:\n  - {doc_md}\n  - {vault_md}")

    # 1. Generate DOCX with Pandoc
    pandoc_docx = [
        "pandoc",
        doc_md,
        "-o", docx_out,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=docx"
    ]
    print("Generating Word (.docx)...")
    subprocess.run(pandoc_docx, check=True)
    shutil.copy(docx_out, docs_dir)
    print(f"SUCCESS! Created DOCX: {docx_out}")

    # 2. Render HTML + MathJax 3 + Mermaid for Headless Chrome PDF
    temp_body = "/tmp/markov_blankets_body.html"
    pandoc_html = [
        "pandoc",
        doc_md,
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
    <title>Quanten-Markov-Blankets vs. Maximale Entropie - Thomas Riebl</title>
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
                fontSize: '12px',
                fontFamily: 'EB Garamond, Georgia, serif'
            }
        });
    </script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Fira+Code:wght@400;500&display=swap');

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
                content: "Thomas Riebl • Quanten-Markov-Blankets vs. Maximale Entropie";
                font-family: 'EB Garamond', Georgia, serif;
                font-size: 9pt;
                color: #64748b;
            }
        }
        body {
            font-family: 'EB Garamond', Georgia, serif;
            color: #0f172a;
            line-height: 1.55;
            font-size: 11pt;
            margin: 0;
            padding: 0;
        }
        h1 {
            font-family: 'Cinzel', serif;
            color: #0f172a;
            font-size: 17pt;
            font-weight: 800;
            border-bottom: 2.5px solid #16a34a;
            padding-bottom: 6pt;
            margin-top: 0;
            margin-bottom: 6pt;
            line-height: 1.25;
        }
        h2 {
            font-family: 'Cinzel', serif;
            color: #166534;
            font-size: 13pt;
            font-weight: 700;
            margin-top: 18pt;
            margin-bottom: 6pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3pt;
            page-break-after: avoid;
        }
        h3 {
            color: #0f172a;
            font-size: 11.5pt;
            font-weight: 700;
            margin-top: 12pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }
        p {
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: justify;
        }
        .mermaid {
            text-align: center;
            margin: 14pt auto;
            page-break-inside: avoid;
        }
        .mermaid svg {
            max-width: 95% !important;
            height: auto !important;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12pt 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 6px 8px;
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
            page-break-inside: avoid;
        }
        hr {
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 16pt 0;
        }
        code {
            font-family: 'Fira Code', monospace;
            font-size: 9.5pt;
            background: #f1f5f9;
            padding: 2px 4px;
            border-radius: 3px;
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

    temp_html = "/tmp/markov_blankets_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    print("Rendering PDF with Headless Chrome...")
    chrome_cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
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
