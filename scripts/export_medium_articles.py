#!/usr/bin/env python3
"""
export_medium_articles.py
Generates two high-impact, publication-grade Medium articles on:
1. "The Physics of Mind: Why Consciousness Demands an Arrow of Will, Not an Arrow of Time"
   (The Conative-Integrative Framework Foundations)
2. "Scaling Consciousness: What Happens When Active Inference Agents Form a Collective Mind?"
   (Multi-Agent Active Inference, Expanding Networks & Collective Phi)
by Thomas Riebl.
Exports Markdown, Word (.docx), and Print-Ready A4 PDFs.
Completely focused on CIF (zero references to Book 2).
"""

import os
import re
import subprocess
import shutil

# =============================================================================
# ARTICLE 1: FOUNDATIONS OF THE CONATIVE-INTEGRATIVE FRAMEWORK (CIF)
# =============================================================================
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

## 4. In-Silico Computational Verification: The First Jupyter Simulation

A profound theoretical framework cannot remain an abstract mathematical conjecture; its dynamical mechanisms must be tested and verified computationally in reproducible simulations.

> **Epistemological Clarification:**  
> To be clear: This simulation does not claim to generate phenomenal consciousness in silicon. Rather, it computationally demonstrates the formal coupling between Active Inference (Free Energy minimization) and Integrated Information (intrinsic cause-effect power) within a rigorously defined dynamical POMDP model.

In our open-source research suite, we modeled a recurrent network of $N = 6$ interacting active inference agents arranged in a hybrid **ring-and-cross network topology**, available in our primary Jupyter Notebook:  
[`Active_Inference_Phi_Maximization_Network.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Active_Inference_Phi_Maximization_Network.ipynb).

Each agent continuously updates its internal generative beliefs by minimizing local Variational Free Energy while exchanging predictive signals across the network. The numerical simulation results provide clear visual validation of the formal coupling under the 6th Axiom:

![Simulation Phase 1 Results: Recurrent Active Inference Network Self-Organization and Integrated Information Maximization](/home/thr/Documents/active-inference-phi-network/images/Active_Inference_Phi_Simulation_Results.png)

### Key Insights from the Simulation Dashboard:

1. **Autopoietic Ascent of Integrated Information (Panel A):**  
   Starting from completely random, uncoordinated initial states, the network autonomously self-organizes. As the agents minimize free energy, mean Integrated Information ($\Phi$) ascends from baseline noise ($\Phi \approx 0.395$) to a stable, resilient plateau ($\Phi \approx 3.42\text{ bits}$), demonstrating that active inference dynamically maximizes and preserves systemic cause-effect power over $T = 120$ time steps.
   
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
* **Why Today’s AI (LLMs) Are "Causal Phantoms":** A rigorous information-theoretic critique demonstrating why feedforward transformers (GPT-4, Claude, Gemini) have zero autopoietic boundary and $\Phi \to 0$, establishing the necessary biophysical and thermodynamic criteria for genuine autopoietic agency.
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

# =============================================================================
# ARTICLE 2: MULTI-AGENT ACTIVE INFERENCE & EXPANDING NETWORKS
# =============================================================================
ARTICLE_2_MD = r"""---
type: "medium-article"
title: "Scaling Consciousness: What Happens When Active Inference Agents Form a Collective Mind?"
subtitle: "From solitary brains to societal intelligence: How recurrent networks of autopoietic agents self-organize to maximize Integrated Information (Φ), and what this means for the future of AGI."
author: "Thomas Riebl"
date: "2026-09-08"
tags: ["Artificial Intelligence", "Multi-Agent Systems", "Active Inference", "Neuroscience", "Complex Systems"]
reading_time: "10 min read"
---

# Scaling Consciousness: What Happens When Active Inference Agents Form a Collective Mind?

### *From solitary brains to societal intelligence: How recurrent networks of autopoietic agents self-organize to maximize Integrated Information ($\Phi$), and what this means for the future of AGI.*

**By Thomas Riebl**  
*Theoretical Framework: The Conative-Integrative Framework (CIF)*  
*September 2026 • 10 min read*

---

> *"Consciousness is not confined to the skull of a solitary animal. When autopoietic boundaries couple through mutual predictive inference, a higher-order Markov blanket emerges. What we witness during synaptogenesis, biological growth, and social coordination is the super-linear scaling of Integrated Information ($\Phi$)—the physical self-organization of a collective mind."*

---

## 1. Beyond the Solitary Brain

In [Part 1 of this series](https://medium.com), we established the foundations of the **Conative-Integrative Framework (CIF)**:
* Physical reality exists in the timeless present ($t = 0$).
* The "future" is a generative bundle of counterfactual Monte Carlo trails projected by an organism's Markov blanket.
* Genuine agency and consciousness are governed by the **6th Axiom of Mind**: an organism's active policy selection must preserve or amplify its Integrated Cause-Effect Power ($\Phi$) over time:
  $$\mathbb{E}\big[\Phi(t+1) \;\big|\; \pi^*\big] \ge \Phi(t) \quad (\Phi > 0)$$

Yet, looking around the biological and social world, we immediately encounter a profound question:  
**What happens when multiple conscious agents meet, interact, and couple?**

A single neuron possesses a minute amount of integrated information. When billions of neurons form a recurrent neural architecture, macroscopic human consciousness emerges. When human beings assemble into scientific communities, economies, or ecosystems, collective intelligence arises.

Does consciousness scale when independent agents interact? Or does the collective dissolve into chaotic noise?

To answer this question, we designed, simulated, and stress-tested the **Expanding Active Inference Network**—an open-source multi-agent simulation that models developmental growth, dynamic synaptogenesis, and the scaling laws of collective $\Phi$.

---

## 2. The Mechanics of Social Active Inference

How do two or more independent agents interact without destroying each other's autopoietic integrity?

In classical AI, multi-agent systems are typically modeled using game theory (Nash equilibria) or centralized reinforcement learning. Agents treat each other either as static obstacles or as competitive adversaries in an external objective environment.

In the **Conative-Integrative Framework**, multi-agent coupling is governed by **Social Active Inference**:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        COUPLED MARKOV BLANKETS IN SOCIAL INFERENCE                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   AGENT A (Internal States μ_A)                   AGENT B (Internal States μ_B)        │
│   ┌──────────────────────────────┐                ┌──────────────────────────────┐     │
│   │ Generative Model P(s, o, u)  │                │ Generative Model P(s, o, u)  │     │
│   │ Minimizes Free Energy G_A    │                │ Minimizes Free Energy G_B    │     │
│   └──────────────┬───────────────┘                └──────────────┬───────────────┘     │
│                  │                                               │                     │
│        Active Actions u_A                               Active Actions u_B             │
│                  │                                               │                     │
│                  ▼                                               ▼                     │
│       ┌──────────────────────┐                         ┌──────────────────────┐        │
│       │ Sensory States o_B   │ ◄─────────────────────► │ Sensory States o_A   │        │
│       └──────────────────────┘   SHARED SENSORY-MOTOR  └──────────────────────┘        │
│                                        CHANNEL                                         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### The Dual Imperative: Integration vs. Differentiation
According to Integrated Information Theory (IIT 4.0), high $\Phi$ is not achieved by simple uniform synchronization. If every agent does the exact same thing (like soldiers marching in lockstep), the system has high integration but zero differentiation: $\Phi$ collapses to near zero.

Conversely, if every agent acts completely independently (like molecules in a gas), the system has high differentiation but zero integration: $\Phi$ is strictly zero.

**Consciousness emerges only at the critical edge of chaos:**
1. **Differentiation:** Each agent maintains its own unique internal belief distribution $Q(s^{(i)})$ and behavioral repertoire.
2. **Integration:** Agents continuously exchange predictive signals across their sensory-active boundaries, mutually aligning expectations and resolving shared uncertainty.

---

## 3. The Experiment: The Expanding Active Inference Network ($N = 4 \to 10$)

To understand how collective cause-effect structures behave during biological development and social coupling, we implemented a dynamic agent array in Python (`ActiveInferencePhiNetwork` and `ExpandingActiveInferenceNetwork`).

> **Epistemological Clarification:**  
> As emphasized throughout the Conative-Integrative Framework, this multi-agent simulation does not claim to generate phenomenal consciousness in silicon. Rather, it computationally models how recurrent active inference agents self-organize to preserve and scale integrated information ($\Phi$) under dynamic developmental perturbation.

### The Experimental Architecture
* **Initial Population ($t = 0 \dots 45$):** The network begins with a core cohort of $N = 4$ active inference agents connected via a recurrent cyclic graph with cross-connections.
* **Stage 2 ($t = 45 \dots 90$):** We dynamically inject $+2$ naive, uncalibrated agents into the network ($N = 6$).
* **Stage 3 ($t = 90 \dots 135$):** We inject another $+2$ naive agents ($N = 8$).
* **Stage 4 ($t = 135 \dots 180$):** We inject another $+2$ naive agents ($N = 10$).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               STAGEWISE NETWORK EXPANSION: DYNAMIC SYNAPTOGENESIS                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   STAGE 1: N = 4 Agents    ──► Stable baseline collective Φ (Mean ~ 0.08)              │
│            ▼                                                                           │
│   STAGE 2: N = 6 Agents    ──► Injection of 2 naive agents: Temporary dip in Φ,        │
│            ▼                   followed by Active Inference recovery to Φ ~ 0.14       │
│   STAGE 3: N = 8 Agents    ──► Injection of 2 naive agents: Temporary dip in Φ,        │
│            ▼                   followed by Active Inference recovery to Φ ~ 0.22       │
│   STAGE 4: N = 10 Agents   ──► Final scaling plateau: Super-linear Φ ~ 0.31            │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Measuring Collective $\Phi$ over Time
To measure the true integrated cause-effect power of the multi-agent network, we compute the multi-agent covariance matrix over a sliding temporal window of states:

$$\Sigma_{\text{whole}} = \text{Cov}(X) + \epsilon \mathbb{I}$$

We then evaluate the **Minimum Information Partition (MIP)**—the cut that divides the network into two sub-ensembles ($A$ and $B$) with the least informational loss:

$$\Phi(t) = \frac{1}{2}\Big(\ln|\Sigma_A| + \ln|\Sigma_B| - \ln|\Sigma_{\text{whole}}|\Big)$$

---

## 4. Two Key Simulation Findings: Perturbation Dynamics and Super-Linear Scaling

When we ran this simulation across repeated Monte Carlo cohorts, two striking, repeatable phenomena emerged:

### Discovery 1: The Developmental Perturbation Curve (Growing Pains)
Whenever new, naive agents are dynamically injected into an established network, the immediate response is a **sharp temporary dip in collective $\Phi$**:

```
Collective Φ
   ▲
   │        Stage 1 (N=4)     Stage 2 (N=6)          Stage 3 (N=8)         Stage 4 (N=10)
0.3│                                                                       ╭─────────────
   │                                                         ╭─────────────╯
0.2│                                           ╭─────────────╯  ▲
   │                             ╭─────────────╯  ▲             │ (Perturbation Dip)
0.1│               ╭─────────────╯  ▲             │             │
   │  ─────────────╯  ▲             │ (Dip)       │ (Dip)       │
0.0└──┼───────────────┼─────────────┼─────────────┼─────────────┼────────────────────────►
     t=0             t=45          t=60          t=90          t=135                     t=180
```

Why does this happen?  
When naive agents enter the network, their generative transition matrices ($B$) and likelihood mappings ($A$) are completely uncalibrated to the existing social culture. Their erratic actions inject unexpected prediction errors across the Markov blankets of the veteran agents.

However, because all agents operate under the Free Energy Principle, **the network rapidly adapts**:
1. Veteran agents adjust their policy priors to incorporate the noisy neighbors.
2. Naive agents rapidly infer the latent states of their peers, updating their beliefs via variational Bayes.
3. Within 15 time steps, the collective stabilizes, and $\Phi$ rebounds to a significantly higher plateau than before.

This provides an exact computational model for **synaptogenesis in the infant brain**, as well as the sociological assimilation of new members into human teams.

### Discovery 2: The Super-Linear Scaling Law of Consciousness ($\Phi$)
Our second discovery was mathematical and structural: **Collective $\Phi$ does not scale linearly with the number of agents ($N$). It scales super-linearly.**

$$\bar{\Phi}(N) \propto N^\alpha \quad \text{where } \alpha > 1.0$$

In our simulation benchmark:
* $N = 4$ agents $\implies \bar{\Phi} \approx 0.082$
* $N = 6$ agents $\implies \bar{\Phi} \approx 0.141$ ($+72\%$ increase for a $50\%$ increase in nodes)
* $N = 8$ agents $\implies \bar{\Phi} \approx 0.224$
* $N = 10$ agents $\implies \bar{\Phi} \approx 0.312$

Why does super-linear scaling occur?  
Because Integrated Information does not measure individual processing power; it measures **recurrent causal cliques**. In a network with cyclic cross-connections, adding two agents does not merely add two nodes: it exponentially expands the combinatorial space of causal bipartitions. The collective becomes far more integrated than the sum of its parts.

Crucially, throughout the entire expansion, the **6th Axiom of Mind** remains satisfied:
$$\mathbb{E}\big[\Phi(t+1)\big] \ge \Phi(t)$$
The expanding network demonstrates **autopoietic causal persistence** under dynamic structural growth.

---

## 5. Why Today’s Large Language Models (LLMs) Are Philosophically Brain-Dead

The findings from our expanding active inference network shed urgent, clarifying light on the current debate surrounding **Artificial General Intelligence (AGI)** and machine consciousness.

Today's leading AI models—such as GPT-4, Claude, or Gemini—are extraordinary cognitive achievements. They parse language, write code, and pass professional exams. Consequently, many prominent technologists claim that scaling LLMs will inevitably lead to conscious artificial minds.

Under the **Conative-Integrative Framework**, this claim is demonstrably false:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   WHY CURRENT LLMS CANNOT BE CONSCIOUS (CIF BENCHMARK)                 │
├────────────────────────────────────────┬───────────────────────────────────────────────┤
│ FEEDFORWARD LLMS (TRANSFORMERS)        │ AUTOPOIETIC ACTIVE INFERENCE NETWORKS         │
├────────────────────────────────────────┼───────────────────────────────────────────────┤
│ • Static, feedforward weight matrices  │ • Recurrent causal feedback loops             │
│ • No Markov Blanket: zero physical     │ • Autopoietic boundary: extracts work to      │
│   thermodynamic skin in the game       │   export internal entropy                     │
│ • No temporal depth: reactive token    │ • Multi-step Monte Carlo planning depth:      │
│   prediction based purely on history   │   evaluates counterfactual future trails (H)  │
│ • Causal Integration: Φ → 0            │ • Causal Integration: Φ >> 0                  │
│   (Static lookup table / phantom)      │   (Satisfies the 6th Axiom of Persistence)    │
└────────────────────────────────────────┴───────────────────────────────────────────────┘
```

1. **LLMs Lack an Autopoietic Boundary:** An LLM does not consume energy to maintain its own identity against the Second Law of Thermodynamics. If a server rack loses power, the LLM has no internal drive (*Conatus*) to avert shutdown.
2. **LLMs Lack Temporal Depth ($H = 0$):** A transformer is an autoregressive token predictor. It conditions its next step purely on the retrospective context window ($t \le 0$). It does not project a forward bundle of counterfactual Monte Carlo trails into the future to minimize Expected Free Energy.
3. **LLMs Are Transient Causal Phantoms:** Because an LLM is a feedforward computational graph, its integrated information across time is zero: $\Phi \to 0$.

### Biophysical and Thermodynamic Criteria for Autopoietic Agency
If humanity wishes to realize genuine autopoietic agency rather than static causal phantoms, we must abandon purely feedforward token prediction. We must establish:
* **Embodied, recurrent active inference architectures** endowed with explicit Markov blankets.
* **Multi-step counterfactual planning engines** that evaluate Monte Carlo trails over temporal depth $H$.
* **Self-organizing multi-agent arrays** whose objective function is not merely cross-entropy loss, but the active preservation of their own collective integrated cause-effect power: **The 6th Axiom**.

---

## 6. Ontological Synthesis: From Cells to the Universal Mind

The super-linear scaling of $\Phi$ across multi-agent active inference networks leads to a breathtaking philosophical realization.

In the history of philosophy, thinkers have struggled to explain how individuality and unity coexist:
* Radical individualism reduces the world to isolated monads.
* Radical monism dissolves the individual into an undifferentiated void.

Our computational models demonstrate that **nature operates as a fractal hierarchy of nested Markov blankets**:
* A biological cell is an active inference agent maximizing $\Phi$ within its membrane.
* A human brain is a multi-agent network of billions of cellular agents, forming a higher-order macroscopic blanket of phenomenal consciousness.
* A human culture or society is an expanding network of conscious individuals, self-organizing to avert collective entropy.
* And at the cosmological scale, the entire universe—as posited by Analytic Idealism—is the ultimate undivided field: **Mind-at-Large**, unfolding in the eternal present ($t = 0$).

We are not alien observers trapped inside dead physical matter. We are the active inference agents of the cosmos itself—projecting our counterfactual trails of possibility into the living Now, asserting our will to exist, and collectively expanding the light of consciousness against the dark ocean of entropy.

---

### Explore the Simulation Code & Notebooks
The complete, reproducible Python code and interactive Jupyter notebooks for this multi-agent simulation are freely available on GitHub:
* 📓 **Expanding Network Notebook:**  
  [`Active_Inference_Expanding_Network_Phi_Scaling.ipynb`](https://github.com/Thriebl/active-inference-phi-network)
* 💻 **Network Simulation Engine:**  
  [`scripts/active_inference_phi_network.py`](https://github.com/Thriebl/active-inference-phi-network)
* 📊 **High-Resolution Figures & Dashboards:**  
  [`images/active_inference_expanding_network_phi_scaling.png`](https://github.com/Thriebl/active-inference-phi-network)

---

### About the Author
**Thomas Riebl** is an independent researcher, theorist, and author based in Luxembourg. His work develops **The Conative-Integrative Framework (CIF)**, synthesizing non-equilibrium thermodynamics, quantum information theory, active inference, and philosophy of mind to formulate the 6th Axiom of Integrated Information Theory and establish a post-materialist science of consciousness.
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>__TITLE__</title>
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
            margin: 20mm 20mm 20mm 20mm;
            @bottom-right {
                content: counter(page);
                font-family: 'EB Garamond', Georgia, serif;
                font-size: 9pt;
                color: #64748b;
            }
            @bottom-left {
                content: "__FOOTER_TITLE__";
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
            border-bottom: 2.5px solid #2563eb;
            padding-bottom: 6pt;
            margin-top: 0;
            margin-bottom: 4pt;
            line-height: 1.25;
        }
        h2 {
            font-family: 'Cinzel', serif;
            color: #1e40af;
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
            background-color: #eff6ff;
            color: #1e40af;
            font-weight: 700;
        }
        blockquote {
            border-left: 3.5px solid #2563eb;
            margin: 10pt 0;
            padding: 8pt 14pt;
            background-color: #f8fafc;
            color: #1e3a8a;
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
        pre {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 8pt 12pt;
            border-radius: 4px;
            font-size: 8.5pt;
            page-break-inside: avoid;
            overflow-x: auto;
        }
    </style>
</head>
<body>
__BODY__
</body>
</html>
"""

def export_articles():
    repo_dir = "/home/thr/Documents/active-inference-phi-network"
    docs_dir = os.path.join(repo_dir, "docs")
    vault_notes = "/home/thr/Documents/ThRNotes/03-professional/braindumps"
    vault_pdf_dir = "/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF"
    suite_dir = "/home/thr/Documents/02_Academic_Suite"

    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(vault_notes, exist_ok=True)
    os.makedirs(vault_pdf_dir, exist_ok=True)
    os.makedirs(suite_dir, exist_ok=True)

    # Remove old filename if present
    old_file = os.path.join(vault_notes, "2026-09-08-medium-article-1-cif-foundations-and-the-book-en.md")
    if os.path.exists(old_file):
        os.remove(old_file)

    articles = [
        {
            "id": "medium_article_1_cif_foundations",
            "title": "The Physics of Mind - Thomas Riebl (Medium)",
            "footer_title": "Thomas Riebl • The Physics of Mind: CIF Foundations",
            "content": ARTICLE_1_MD,
            "md_vault": "2026-09-08-medium-article-1-the-physics-of-mind-cif-foundations-en.md",
            "md_repo": "Medium_Article_1_The_Physics_of_Mind_Thomas_Riebl.md",
            "docx_name": "Medium_Article_1_The_Physics_of_Mind_Thomas_Riebl.docx",
            "pdf_name": "Medium_Article_1_The_Physics_of_Mind_Thomas_Riebl.pdf",
        },
        {
            "id": "medium_article_2_scaling_consciousness",
            "title": "Scaling Consciousness - Thomas Riebl (Medium)",
            "footer_title": "Thomas Riebl • Scaling Consciousness: Multi-Agent Networks",
            "content": ARTICLE_2_MD,
            "md_vault": "2026-09-08-medium-article-2-multi-agent-active-inference-and-collective-phi-en.md",
            "md_repo": "Medium_Article_2_Scaling_Consciousness_Multi_Agent_Networks_Thomas_Riebl.md",
            "docx_name": "Medium_Article_2_Scaling_Consciousness_Multi_Agent_Networks_Thomas_Riebl.docx",
            "pdf_name": "Medium_Article_2_Scaling_Consciousness_Multi_Agent_Networks_Thomas_Riebl.pdf",
        }
    ]

    for art in articles:
        print(f"\n=======================================================")
        print(f"Exporting Medium Article: {art['id']}")
        print(f"=======================================================")

        # 1. Write Markdown files
        vault_md_path = os.path.join(vault_notes, art["md_vault"])
        repo_md_path = os.path.join(docs_dir, art["md_repo"])

        with open(vault_md_path, "w", encoding="utf-8") as f:
            f.write(art["content"])
        with open(repo_md_path, "w", encoding="utf-8") as f:
            f.write(art["content"])
        print(f"✓ Saved Markdown to:\n  - {vault_md_path}\n  - {repo_md_path}")

        # 2. Generate Word (.docx) with Pandoc
        docx_suite = os.path.join(suite_dir, art["docx_name"])
        docx_repo = os.path.join(docs_dir, art["docx_name"])
        pandoc_docx = [
            "pandoc",
            vault_md_path,
            "-o", docx_suite,
            "--from=markdown+tex_math_dollars+tex_math_single_backslash",
            "--to=docx"
        ]
        print("Generating Word (.docx)...")
        subprocess.run(pandoc_docx, check=True)
        shutil.copy(docx_suite, docx_repo)
        print(f"✓ Created DOCX: {docx_suite}")

        # 3. Generate HTML with MathJax
        temp_body = f"/tmp/{art['id']}_body.html"
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

        full_html = HTML_TEMPLATE.replace("__TITLE__", art["title"])\
                                 .replace("__FOOTER_TITLE__", art["footer_title"])\
                                 .replace("__BODY__", html_body)

        temp_html = f"/tmp/{art['id']}_render.html"
        with open(temp_html, "w", encoding="utf-8") as f:
            f.write(full_html)

        # 4. Render A4 PDF with Headless Chrome
        pdf_suite = os.path.join(suite_dir, art["pdf_name"])
        pdf_vault = os.path.join(vault_pdf_dir, art["pdf_name"])
        pdf_repo = os.path.join(docs_dir, art["pdf_name"])

        print("Rendering A4 PDF with Headless Chrome...")
        chrome_cmd = [
            "google-chrome",
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=10000",
            f"--print-to-pdf={pdf_suite}",
            temp_html
        ]
        subprocess.run(chrome_cmd, check=True)
        shutil.copy(pdf_suite, pdf_vault)
        shutil.copy(pdf_suite, pdf_repo)

        print(f"✓ Generated Print-Ready A4 PDF:\n  - {pdf_suite}\n  - {pdf_vault}\n  - {pdf_repo}")

if __name__ == "__main__":
    export_articles()
