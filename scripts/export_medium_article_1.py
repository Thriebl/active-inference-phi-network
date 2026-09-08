#!/usr/bin/env python3
"""
export_medium_article_1.py
Compacts and exports Medium Article 1:
"The Conative-Integrative Framework: How Active Inference and IIT 4.0 Solve the Hard Problem of Consciousness"
by Thomas Riebl.

Features:
- Compact summary of the First Part of the Conative-Integrative Framework (CIF).
- Prominently embeds the First Jupyter Simulation graphic (Active_Inference_Phi_Simulation_Results.png).
- High-converting, elegant Call-to-Action (CTA) encouraging purchase of the book on Amazon with front cover.
- 100% English. Completely excludes Book 2.
- Exports to Markdown (Vault & Repo), Word (.docx), and Print-Ready A4 PDF (via Headless Chrome).
"""

import os
import subprocess
import shutil

# Paths
REPO_DIR = "/home/thr/Documents/active-inference-phi-network"
DOCS_DIR = os.path.join(REPO_DIR, "docs")
VAULT_NOTES = "/home/thr/Documents/ThRNotes/03-professional/braindumps"
VAULT_PDF_DIR = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"
SUITE_DIR = "/home/thr/Documents/02_Academic_Suite"

SIMULATION_IMG = os.path.join(REPO_DIR, "images", "Active_Inference_Phi_Simulation_Results.png")
COVER_IMG = os.path.join(REPO_DIR, "book", "cover", "The_Conative_Integrative_Framework_Front_Cover.jpg")
PORTRAIT_IMG = os.path.join(REPO_DIR, "images", "img_9795.jpg")

ARTICLE_1_MD = r"""---
type: "medium-article"
title: "The Conative-Integrative Framework: How Active Inference and IIT 4.0 Solve the Hard Problem of Consciousness"
subtitle: "Why subjective awareness demands an autopoietic arrow of will, how self-organizing networks maximize integrated information at the edge of chaos—and why you need the book."
author: "Thomas Riebl"
date: "2026-09-08"
tags: ["Consciousness", "Active Inference", "Integrated Information Theory", "Neuroscience", "Philosophy of Mind", "Amazon Books"]
reading_time: "7 min read"
---

# The Conative-Integrative Framework: How Active Inference and IIT 4.0 Solve the Hard Problem of Consciousness

### *Why subjective awareness demands an autopoietic arrow of will, how self-organizing networks maximize integrated information at the edge of chaos—and why you need the book.*

**By Thomas Riebl**  
*Theoretical Neuroscience & Philosophy of Mind • September 2026 • 7 min read*

---

> *"Consciousness is not an incidental, decorative byproduct of dead physical matter. It is the thermodynamic necessity of an autopoietic boundary actively asserting its causal existence against the entropic arrow of dissolution. To be conscious is to possess an Arrow of Will."*

---

## 1. The Great Impasse: The Explanatory Chasm

For more than three centuries, orthodox science has operated under the dogma of reductive physicalism: the assumption that reality is fundamentally composed of cold, inanimate particles, and that subjective qualitative experience (*the fiery red of a sunset, the ache of heartbreak, the silent lucidity of being*) somehow "emerges" from complex biological wiring.

Yet, as philosopher David Chalmers famously crystallized, physicalism faces an impenetrable brick wall: **The Hard Problem of Consciousness**. Cognitive neuroscience can map the brain's "easy problems"—optical processing, motor reflexes, language parsing, and memory retrieval—with exquisite precision. But no matter how detailed our map of ion channels and synaptic spikes becomes, Joseph Levine’s **Explanatory Gap** remains absolute:

$$\text{Mechanical Spikes } (\text{Action Potentials, Ion Flux}) \quad\xrightarrow{\;\text{Explanatory Gap}\;}\quad \text{Phenomenal Qualia } (\text{Subjective Experience})$$

Why should any neural computation *feel* like anything from the inside? Why are we not philosophical zombies, carrying out identical cognitive tasks in total inner darkness?

Faced with this crisis, mainstream physicalism made an absurd intellectual concession: it claimed that subjective consciousness is merely an "epiphenomenon"—a useless, illusory user interface. 

**The Conative-Integrative Framework (CIF)** rejects this surrender. By establishing a rigorous mathematical bridge between three intellectual revolutions—**Analytic Idealism**, **Active Inference**, and **Integrated Information Theory (IIT 4.0)**—we demonstrate that the Hard Problem is not solved by reducing mind to matter, but by understanding how the universal ground of reality partitions itself into living, self-sustaining agents.

---

## 2. The Tripartite Synthesis: Three Giants in One Room

To construct a mathematically closed ontology of mind, we synthesize the foundational discoveries of three modern pioneers:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE CONATIVE-INTEGRATIVE FRAMEWORK (CIF)                        │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. ANALYTIC IDEALISM       │ 2. ACTIVE INFERENCE        │ 3. IIT 4.0                   │
│ (Bernardo Kastrup / Spira) │ (Karl Friston)             │ (Giulio Tononi / Koch)       │
│                            │                            │                              │
│ • Consciousness is the     │ • Living systems are       │ • Consciousness is intrinsic │
│   irreducible ontic fabric │   Markov Blankets.         │   cause-effect power (Φ).    │
│   of nature (Mind-at-Large)│ • Survive by minimizing    │ • Measures irreducible       │
│ • Organisms are alters.    │   variational Free Energy. │   causal wholeness.          │
├────────────────────────────┴────────────────────────────┴──────────────────────────────┤
│ 4. THE MISSING KEYSTONE: THOMAS RIEBL'S 6TH AXIOM OF AUTOPOIETIC PERSISTENCE           │
│                                                                                        │
│        π* = argmin G(π)   <===>   E[ Φ(t+1) | π* ] ≥ Φ(t)    (with Φ > 0)             │
│                                                                                        │
│ • Derives Spinoza's Conatus from quantum information thermodynamics.                   │
│ • Resolves the "Paradox of Transient Causal Phantoms" in IIT 4.0.                      │
│ • Dynamically self-organizes at the Edge of Chaos (Criticality).                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Pillar 1: Analytic Idealism & Non-Dual Ontology
Spearheaded by philosopher Bernardo Kastrup and rooted in Advaita Vedanta, Analytic Idealism posits that reality is fundamentally a single, undivided experiential field: **Mind-at-Large**. Living organisms are not biological machines manufacturing experience out of dead meat; rather, they are **dissociated alters** within Mind-at-Large. The biological body and brain are what an alter's internal experiential processes *look like* when observed across a boundary.

### Pillar 2: The Free Energy Principle & Markov Blankets
Formulated by world-renowned theoretical neuroscientist Karl Friston, the Free Energy Principle (FEP) provides the mathematical physics of living boundaries. A living agent survives in an unpredictable world by maintaining a **Markov Blanket** ($\mathcal{B} = \{s, a\}$) separating internal cognitive states ($\mu$) from external ambient states ($\eta$):

$$\mu \perp\!\!\!\perp \eta \mid \mathcal{B}$$

To avoid thermodynamic dispersion, the agent must constantly minimize **Variational Free Energy ($F$)**, bounding its informational entropy, and act to minimize **Expected Free Energy ($G$)** over future policies.

### Pillar 3: Integrated Information Theory (IIT 4.0)
Developed by neuroscientist Giulio Tononi and Christof Koch, IIT 4.0 formalizes consciousness from the inside out: consciousness is **intrinsic cause-effect power ($\Phi$, Phi)**. A system has phenomenal experience to the exact degree that its internal structure forms an irreducible, unified causal whole above and beyond any possible partition of its parts.

---

## 3. The Fatal Flaw & The Discovery: The 6th Axiom of Mind

Despite their individual genius, these frameworks left an existential blind spot at their junction—a problem I uncovered and termed **The Paradox of Transient Causal Phantoms**.

Standard IIT 4.0 evaluates integrated information ($\Phi$) on static, instantaneous transition probability matrices. Mathematically, a completely accidental, momentary physical configuration—or an inanimate silicon lookup table—could register an astronomical value of $\Phi$ for a fraction of a millisecond, only to immediately dissolve into thermal noise. 

Does a fleeting, random collision of transistors possess authentic phenomenal selfhood? No. Standard IIT lacks a temporal survival drive: it cannot distinguish a living, conscious agent from a transient causal ghost.

### The Breakthrough: The 6th Axiom of Consciousness
The Conative-Integrative Framework resolves this impasse by introducing the **6th Axiom of Consciousness (*Autopoietic Causal Persistence*)**:

$$\pi^* = \arg\min_{\pi} \mathbf{G}(\pi) \quad\Longleftrightarrow\quad \mathbb{E}\Big[\Phi(t+1) \;\Big|\; \pi^*\Big] \ge \Phi(t) \quad (\Phi > 0)$$

> **The 6th Axiom (Thomas Riebl):**  
> *A physical substrate cannot sustain genuine phenomenal consciousness unless its active policy selection ($\pi^*$) minimizing Expected Free Energy ($G$) simultaneously guarantees that its expected integrated cause-effect power ($\Phi$) is preserved or amplified across time.*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   THE THERMODYNAMIC DERIVATION OF SPINOZA'S CONATUS                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ In 1677, Baruch Spinoza wrote in his Ethics:                                           │
│ "Each thing, as far as it can by its own power, strives to persevere in its being."    │
│                                                                                        │
│ Under the CIF, Spinoza's Conatus is formally derived from quantum information           │
│ thermodynamics: In an isothermal universe, maximum entropy is an infinite-energy      │
│ catastrophe. Living boundaries must condense and actively self-assert their causal     │
│ wholeness. Consciousness is the operational engine of this autopoietic struggle.       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. In-Silico Empirical Proof: The First Jupyter Simulation

A profound theoretical framework cannot remain an abstract mathematical equation. It must be demonstrated computationally in reproducible simulations.

In our open-source research suite, we modeled a recurrent network of $N = 6$ interacting active inference agents arranged in a hybrid **ring-and-cross network topology**, available in our primary Jupyter Notebook:  
[`Active_Inference_Phi_Maximization_Network.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Active_Inference_Phi_Maximization_Network.ipynb).

Each agent continuously updates its internal generative beliefs by minimizing local Variational Free Energy while exchanging predictive signals across the network. The empirical results provide indisputable visual confirmation of the 6th Axiom:

![Simulation Phase 1 Results: Recurrent Active Inference Network Self-Organization and Integrated Information Maximization](/home/thr/Documents/active-inference-phi-network/images/Active_Inference_Phi_Simulation_Results.png)

### Key Insights from the Simulation Dashboard:

1. **Autopoietic Ascent of Integrated Information (Panel A):**  
   Starting from completely random, uncoordinated initial states, the network autonomously self-organizes. As the agents minimize free energy, mean Integrated Information ($\Phi$) ascends from baseline noise ($\Phi \approx 0.395$) to a stable, resilient plateau ($\Phi \approx 3.42\text{ bits}$), proving that active inference dynamically maximizes and preserves systemic cause-effect power over $T = 120$ time steps.
   
2. **Phase-Locked Coherent State Dynamics (Panel B):**  
   The state raster confirms that the agents settle into coordinated, rhythmic state transitions without collapsing into pathological hypersynchrony (epileptic locking) or dispersing into incoherent thermal noise.
   
3. **Self-Organized Criticality at the Edge of Chaos (Panels C & D):**  
   Analysis of the adjacency coupling matrix $W$ and the maximal Lyapunov exponent ($\lambda_1 \approx 0^+$) reveals that the network self-tunes precisely to the **Edge of Chaos**. Subcritical networks ($\lambda_1 < 0$) freeze into rigid, low-$\Phi$ attractors, while supercritical networks ($\lambda_1 \gg 0$) dissolve into chaotic turbulence. Maximum integrated cause-effect power emerges strictly at the critical boundary!

---

## 5. Want the Full Theory? Get the Book on Amazon

This article provides only an introductory glimpse into the foundations of the Conative-Integrative Framework. The complete, rigorous mathematical, neurobiological, and metaphysical architecture is published in the comprehensive master monograph:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              NOW AVAILABLE ON AMAZON                                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│                     THE CONATIVE-INTEGRATIVE FRAMEWORK                                 │
│        Active Inference, Integrated Information, and the Autopoietic Arrow of Mind     │
│                                                                                        │
│                                 By Thomas Riebl                                        │
│                                                                                        │
│    "The definitive mathematical synthesis resolving the Hard Problem of Consciousness, │
│     the illusion of time, and the boundary between machine computation and mind."     │
│                                                                                        │
│    Available worldwide on Amazon in Kindle eBook, Paperback, and Hardcover editions.   │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

![The Conative-Integrative Framework Front Cover](/home/thr/Documents/active-inference-phi-network/book/cover/The_Conative_Integrative_Framework_Front_Cover.jpg)

### What You Will Discover in the Complete Book:

* **The 6-Layer Ontogeny of the Soul ($100\%$):** How Mind-at-Large ($25\%$), Genetics ($15\%$), Embryological Chance & Necessity ($15\%$), Transgenerational Epigenetics ($10\%$), Biographical Learning ($25\%$), and the Phenomenal Self-Model / Ego Tunnel ($10\%$) assemble an individual conscious mind.
* **The Theorem of Minimum Temporal Depth ($H > 1$):** A formal mathematical proof that consciousness cannot exist in a static dimensionless instant, resolving William James’s *Specious Present* and proving why purely reactive automata ($H = 0$) suffer inevitable causal death.
* **Why Today’s AI (LLMs) Are "Causal Phantoms":** A rigorous information-theoretic critique demonstrating why feedforward transformers (GPT-4, Claude, Gemini) have zero autopoietic boundary and $\Phi \to 0$, providing the true engineering blueprint for synthetic consciousness.
* **Multi-Agent Scaling Laws ($\Phi(N)$):** How collective consciousness scales super-linearly across societies of communicating active inference agents.
* **Existential & Spiritual Horizons:** The neuroscience of dying with dignity, the dissolution of trauma, and the ultimate synthesis of Stoic *Amor Fati* with quantum thermodynamics.

👉 **Order Your Copy on Amazon Today:**  
Search for **"The Conative-Integrative Framework by Thomas Riebl"** on your local Amazon store ([Amazon.com](https://www.amazon.com), [Amazon.de](https://www.amazon.de), [Amazon.co.uk](https://www.amazon.co.uk)) to get the Kindle eBook or the collector’s Paperback/Hardcover edition.

---

## 6. Open-Source Code & Reproducibility

True science demands transparency. The complete Python implementation, simulation scripts, and Jupyter notebooks used to produce the figures in this article and throughout the book are open-source and freely accessible on GitHub:

* 💻 **Primary Simulation Repository:**  
  [`https://github.com/Thriebl/active-inference-phi-network`](https://github.com/Thriebl/active-inference-phi-network)
* 📓 **Interactive Jupyter Notebooks:**  
  [`Active_Inference_Phi_Maximization_Network.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Active_Inference_Phi_Maximization_Network.ipynb)  
  [`Deep_Temporal_Active_Inference_Simulation.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Deep_Temporal_Active_Inference_Simulation.ipynb)  
  [`Active_Inference_Expanding_Network_Phi_Scaling.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Active_Inference_Expanding_Network_Phi_Scaling.ipynb)

---

## About the Author

![Thomas Riebl](/home/thr/Documents/active-inference-phi-network/images/img_9795.jpg)

**Thomas Riebl** is an independent researcher, systems architect, and author based in Luxembourg. Born in 1960 in Western Germany, he spent over three decades in enterprise information technology as an independent IT consultant, systems architect, and senior IT manager at a premier global banking institution. 

Driven by a lifelong passion for foundational physics, cybernetics, and non-dual philosophy, he developed **The Conative-Integrative Framework (CIF)**, formulated the **6th Axiom of Consciousness**, and proved the **Theorem of Minimum Temporal Depth**, providing the first mathematically closed bridge between 3rd-person cybernetic self-organization and 1st-person phenomenal causality.
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Conative-Integrative Framework - Thomas Riebl (Medium)</title>
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
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=EB+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Fira+Code:wght@400;500&display=swap');

        @page {
            size: A4 portrait;
            margin: 18mm 18mm 18mm 18mm;
            @bottom-right {
                content: counter(page);
                font-family: 'EB Garamond', Georgia, serif;
                font-size: 8.5pt;
                color: #64748b;
            }
            @bottom-left {
                content: "Thomas Riebl • The Conative-Integrative Framework (CIF)";
                font-family: 'EB Garamond', Georgia, serif;
                font-size: 8.5pt;
                color: #64748b;
            }
        }
        body {
            font-family: 'EB Garamond', Georgia, serif;
            color: #0f172a;
            line-height: 1.55;
            font-size: 10.5pt;
            margin: 0;
            padding: 0;
        }
        h1 {
            font-family: 'Cinzel', serif;
            color: #0f172a;
            font-size: 17pt;
            font-weight: 800;
            border-bottom: 2.5px solid #1e40af;
            padding-bottom: 5pt;
            margin-top: 0;
            margin-bottom: 4pt;
            line-height: 1.25;
        }
        h2 {
            font-family: 'Cinzel', serif;
            color: #1e40af;
            font-size: 12.5pt;
            font-weight: 700;
            margin-top: 16pt;
            margin-bottom: 5pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 3pt;
            page-break-after: avoid;
        }
        h3 {
            color: #0f172a;
            font-size: 11pt;
            font-weight: 700;
            margin-top: 10pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }
        p {
            margin-top: 0;
            margin-bottom: 7pt;
            text-align: justify;
        }
        img {
            max-width: 95%;
            height: auto;
            display: block;
            margin: 10pt auto;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        img[alt*="Front Cover"] {
            max-width: 50%;
            margin: 12pt auto;
            box-shadow: 0 6px 18px rgba(0,0,0,0.25);
            border: 1px solid #cbd5e1;
        }
        img[alt*="Thomas Riebl"] {
            max-width: 30%;
            margin: 10pt auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
            font-size: 8.5pt;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #cbd5e1;
            padding: 5px 8px;
            text-align: left;
        }
        th {
            background-color: #eff6ff;
            color: #1e40af;
            font-weight: 700;
        }
        blockquote {
            border-left: 3.5px solid #1e40af;
            margin: 8pt 0;
            padding: 6pt 12pt;
            background-color: #f8fafc;
            color: #1e3a8a;
            font-style: italic;
            border-radius: 0 5px 5px 0;
            page-break-inside: avoid;
        }
        hr {
            border: 0;
            height: 1px;
            background: #e2e8f0;
            margin: 12pt 0;
        }
        code {
            font-family: 'Fira Code', monospace;
            font-size: 9pt;
            background: #f1f5f9;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 6pt 10pt;
            border-radius: 4px;
            font-size: 8pt;
            page-break-inside: avoid;
            overflow-x: auto;
        }
        a {
            color: #1e40af;
            text-decoration: none;
            font-weight: 600;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
__BODY__
</body>
</html>
"""

def run():
    print("==================================================================")
    print("Exporting Medium Article 1: CIF Foundations & Amazon Book CTA")
    print("==================================================================")

    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(VAULT_NOTES, exist_ok=True)
    os.makedirs(VAULT_PDF_DIR, exist_ok=True)
    os.makedirs(SUITE_DIR, exist_ok=True)

    # 1. Write Markdown files
    md_vault_filename = "2026-09-08-medium-article-1-the-conative-integrative-framework-foundations-amazon-en.md"
    md_repo_filename = "Medium_Article_1_The_Conative_Integrative_Framework_Foundations_Amazon.md"

    vault_md_path = os.path.join(VAULT_NOTES, md_vault_filename)
    repo_md_path = os.path.join(DOCS_DIR, md_repo_filename)

    with open(vault_md_path, "w", encoding="utf-8") as f:
        f.write(ARTICLE_1_MD)
    with open(repo_md_path, "w", encoding="utf-8") as f:
        f.write(ARTICLE_1_MD)

    # Also update the legacy name to keep links functional
    alt_vault_path = os.path.join(VAULT_NOTES, "2026-09-08-medium-article-1-the-physics-of-mind-cif-foundations-en.md")
    with open(alt_vault_path, "w", encoding="utf-8") as f:
        f.write(ARTICLE_1_MD)

    print(f"✓ Saved Markdown files to:\n  - {vault_md_path}\n  - {repo_md_path}\n  - {alt_vault_path}")

    # 2. Generate Word (.docx) with Pandoc
    docx_suite = os.path.join(SUITE_DIR, "Medium_Article_1_The_Conative_Integrative_Framework_Foundations_Thomas_Riebl.docx")
    docx_repo = os.path.join(DOCS_DIR, "Medium_Article_1_The_Conative_Integrative_Framework_Foundations_Thomas_Riebl.docx")

    pandoc_docx = [
        "pandoc",
        vault_md_path,
        "-o", docx_suite,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=docx"
    ]
    print("\nGenerating Word (.docx) with Pandoc...")
    subprocess.run(pandoc_docx, check=True)
    shutil.copy(docx_suite, docx_repo)
    print(f"✓ Created DOCX:\n  - {docx_suite}\n  - {docx_repo}")

    # 3. Generate HTML with Pandoc & MathJax
    temp_body = "/tmp/medium_article_1_cif_body.html"
    pandoc_html = [
        "pandoc",
        vault_md_path,
        "-o", temp_body,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(pandoc_html, check=True)

    with open(temp_body, "r", encoding="utf-8") as f:
        html_body = f.read()

    full_html = HTML_TEMPLATE.replace("__BODY__", html_body)

    temp_html = "/tmp/medium_article_1_cif_render.html"
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    # 4. Render Print-Ready A4 PDF with Headless Chrome
    pdf_suite = os.path.join(SUITE_DIR, "Medium_Article_1_The_Conative_Integrative_Framework_Foundations_Thomas_Riebl.pdf")
    pdf_vault = os.path.join(VAULT_PDF_DIR, "Medium_Article_1_The_Conative_Integrative_Framework_Foundations_Thomas_Riebl.pdf")
    pdf_repo = os.path.join(DOCS_DIR, "Medium_Article_1_The_Conative_Integrative_Framework_Foundations_Thomas_Riebl.pdf")

    print("\nRendering Print-Ready A4 PDF with Headless Google Chrome...")
    chrome_cmd = [
        "google-chrome",
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--allow-file-access-from-files",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=10000",
        f"--print-to-pdf={pdf_suite}",
        temp_html
    ]
    subprocess.run(chrome_cmd, check=True)
    shutil.copy(pdf_suite, pdf_vault)
    shutil.copy(pdf_suite, pdf_repo)

    print(f"✓ Generated Print-Ready A4 PDF:\n  - {pdf_suite}\n  - {pdf_vault}\n  - {pdf_repo}")
    print("\nAll deliverables compiled successfully!")

if __name__ == "__main__":
    run()
