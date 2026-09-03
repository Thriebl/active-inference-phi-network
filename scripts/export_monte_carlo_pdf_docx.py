#!/usr/bin/env python3
"""
export_monte_carlo_pdf_docx.py
Exports the Monte Carlo methodology document to publication-grade A4 Portrait PDF and Word (.docx).
"""

import os
import subprocess
import shutil
import re

DOC_MD = "/home/thr/Documents/time-and-consciousness/docs/2026-09-03-monte-carlo-methodology-in-active-inference-and-consciousness-en.md"
VAULT_MD = "/home/thr/Documents/ThRNotes/03-professional/braindumps/2026-09-03-monte-carlo-methodology-in-active-inference-and-consciousness-en.md"

DOCX_OUT = "/home/thr/Documents/time-and-consciousness/docs/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.docx"
DOCX_MAIN = "/home/thr/Documents/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.docx"

PDF_OUT = "/home/thr/Documents/time-and-consciousness/docs/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.pdf"
PDF_MAIN = "/home/thr/Documents/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.pdf"
PDF_VAULT = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF/2026-09-03-monte-carlo-methodology-in-active-inference-and-consciousness-en.pdf"

def main():
    print("=== Exporting Monte Carlo Methodology Document (A4 Portrait) ===")
    
    # 1. Copy to Vault
    shutil.copy(DOC_MD, VAULT_MD)
    print(f"✓ Copied Markdown to Vault: {VAULT_MD}")
    
    # 2. Generate DOCX via pandoc
    print("Generating Word (.docx)...")
    cmd_docx = [
        "pandoc",
        DOC_MD,
        "-o", DOCX_MAIN,
        "--from=markdown+tex_math_dollars+yaml_metadata_block",
        "--table-of-contents",
        "--toc-depth=2"
    ]
    subprocess.run(cmd_docx, check=False)
    if os.path.exists(DOCX_MAIN):
        shutil.copy(DOCX_MAIN, DOCX_OUT)
        print(f"✓ Created DOCX: {DOCX_MAIN} and {DOCX_OUT}")
        
    # 3. Generate HTML body with pandoc
    print("Generating HTML body...")
    html_body_temp = "/tmp/monte_carlo_body.html"
    cmd_pandoc_html = [
        "pandoc",
        DOC_MD,
        "-o", html_body_temp,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(cmd_pandoc_html, check=True)
    
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
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Monte Carlo Methodology in Active Inference - Thomas Riebl</title>
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
                fontSize: '14px',
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
                content: "Thomas Riebl • Monte Carlo Methodology in Active Inference [CIF]";
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                font-size: 8.5pt;
                color: #64748b;
            }}
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #0f172a;
            line-height: 1.55;
            font-size: 9.8pt;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }}
        h1 {{
            color: #0f172a;
            font-size: 19pt;
            font-weight: 800;
            border-bottom: 2.5px solid #0284c7;
            padding-bottom: 5pt;
            margin-top: 0;
            margin-bottom: 6pt;
            line-height: 1.25;
        }}
        h2 {{
            color: #0369a1;
            font-size: 13pt;
            font-weight: 700;
            margin-top: 16pt;
            margin-bottom: 6pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3pt;
        }}
        h3 {{
            color: #0284c7;
            font-size: 10.8pt;
            font-weight: 600;
            margin-top: 12pt;
            margin-bottom: 4pt;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 8pt;
            text-align: justify;
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
            font-size: 8.8pt;
        }}
        th, td {{
            padding: 6pt 8pt;
            border: 1px solid #cbd5e1;
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
            padding: 8pt 12pt;
            background-color: #f0fdf4;
            border-left: 4px solid #16a34a;
            color: #166534;
            font-size: 9.3pt;
            border-radius: 0 6px 6px 0;
        }}
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 14pt 0;
            background: #ffffff;
            padding: 8pt;
            border: 1px solid #e2e8f0;
            border-radius: 6pt;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 14pt 0;
        }}
        code {{
            font-family: 'JetBrains Mono', 'Courier New', monospace;
            font-size: 8.5pt;
            background-color: #f1f5f9;
            padding: 2px 4px;
            border-radius: 3px;
            color: #0f172a;
        }}
    </style>
</head>
<body>
{html_body}
</body>
</html>
"""
    
    html_render_file = "/tmp/monte_carlo_render.html"
    with open(html_render_file, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print("Rendering high-quality A4 Portrait PDF via Chrome...")
    cmd_pdf = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--virtual-time-budget=8000",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_MAIN}",
        html_render_file
    ]
    subprocess.run(cmd_pdf, check=True)
    
    if os.path.exists(PDF_MAIN):
        shutil.copy(PDF_MAIN, PDF_OUT)
        shutil.copy(PDF_MAIN, PDF_VAULT)
        print(f"✓ SUCCESS! Exported A4 Portrait PDF to:\n  - {PDF_MAIN}\n  - {PDF_OUT}\n  - {PDF_VAULT}")

if __name__ == "__main__":
    main()
