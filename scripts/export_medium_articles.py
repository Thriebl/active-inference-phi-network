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
title: "The Physics of Mind: Why Consciousness Demands an Arrow of Will, Not an Arrow of Time"
subtitle: "How the Conative-Integrative Framework (CIF) unifies Analytic Idealism, Active Inference, and IIT 4.0 to resolve the hard problem—and why the future is just a bundle of Monte Carlo trails."
author: "Thomas Riebl"
date: "2026-09-08"
tags: ["Consciousness", "Philosophy of Mind", "Active Inference", "Physics", "Artificial Intelligence"]
reading_time: "9 min read"
---

# The Physics of Mind: Why Consciousness Demands an Arrow of Will, Not an Arrow of Time

### *How the Conative-Integrative Framework (CIF) unifies Analytic Idealism, Active Inference, and IIT 4.0 to resolve the hard problem—and why the future is just a bundle of Monte Carlo trails.*

**By Thomas Riebl**  
*Theoretical Framework: The Conative-Integrative Framework (CIF)*  
*September 2026 • 9 min read*

---

> *"The future does not exist as an external, pre-fabricated physical container into which we journey. It is an internal ensemble of stochastic Monte Carlo trails actively sampled by an autopoietic boundary in the dimensionless present. Consciousness is not an accidental byproduct of dead matter; it is the physical necessity of an organism actively asserting its causal existence against the thermodynamic arrow of entropy."*

---

## 1. The Great Impasse of Modern Science

For more than a century, mainstream science has been paralyzed by two seemingly insurmountable riddles:

1. **The Hard Problem of Consciousness:** How can subjective, qualitative experience (*the redness of a rose, the ache of grief, the lucidity of awareness*) ever arise from the collision of dead, non-conscious material particles?
2. **The Mystery of Time:** While our everyday conscious experience feels like a continuous, directional river flowing from past to future, modern fundamental physics tells the exact opposite story. In Einstein’s general relativity, space and time form a rigid, static block universe. In canonical quantum gravity, applying the Hamiltonian constraint to the Wheeler-DeWitt equation ($\hat{H}\Psi = 0$) causes the time parameter $t$ to vanish entirely. The physical cosmos is timeless.

Faced with this contradiction, orthodox science took a bizarre turn: it chose to dismiss human experience as a mistake. Consciousness was labeled an "epiphenomenon" (a useless user-interface illusion), and our feeling of temporal duration was brushed aside as a neurological mirage.

**The Conative-Integrative Framework (CIF)**, articulated in our mathematical treatises and computational simulations, rejects this intellectual surrender. By establishing a rigorous mathematical synthesis between three cutting-edge fields—**Analytic Idealism**, **Active Inference**, and **Integrated Information Theory (IIT 4.0)**—we uncover a profound truth:

> **The Hard Problem of Consciousness and the Nature of Time are not two separate puzzles. They are the same puzzle.**  
> And the key that unlocks them both is what Baruch Spinoza called the *Conatus*—the fundamental will to persevere in existence—now formalized as the **6th Axiom of Mind**.

---

## 2. The Tripartite Convergence: Three Giants in One Room

To construct a truly closed, causal ontology of reality, we must stand on the shoulders of three modern intellectual giants, identifying both their profound discoveries and their missing keystones.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE CONATIVE-INTEGRATIVE FRAMEWORK (CIF)                        │
├────────────────────────────┬────────────────────────────┬──────────────────────────────┤
│ 1. ANALYTIC IDEALISM       │ 2. ACTIVE INFERENCE        │ 3. IIT 4.0                   │
│ (Bernardo Kastrup / Spira) │ (Karl Friston)             │ (Giulio Tononi / Koch)       │
│                            │                            │                              │
│ • Consciousness is the     │ • Living systems are       │ • Consciousness is intrinsic │
│   irreducible ontic fabric │   Markov Blankets.         │   cause-effect power (Φ).    │
│ • Reality resides in the   │ • Survive by minimizing    │ • Measures irreducible       │
│   instantaneous Now (t=0). │   variational Free Energy. │   systemic integration.      │
├────────────────────────────┴────────────────────────────┴──────────────────────────────┤
│ 4. THE MISSING KEYSTONE: THOMAS RIEBL'S 6TH AXIOM OF AUTOPOIETIC PERSISTENCE           │
│                                                                                        │
│        π* = argmin G(π)   <===>   E[ Φ(t+1) | π* ] ≥ Φ(t)    (with Φ > 0)             │
│                                                                                        │
│ • Derives Spinoza's Conatus from quantum information thermodynamics.                   │
│ • Resolves the "Paradox of Transient Causal Phantoms" in IIT 4.0.                      │
│ • Proves the Future is a computational bundle of Monte Carlo trails in the Now.        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Pillar 1: Analytic Idealism & Non-Dual Awareness
Spearheaded by philosopher Bernardo Kastrup and rooted in Advaita Vedanta (Rupert Spira), Analytic Idealism posits that the fundamental ground of nature is not inert matter, but a single, undivided field of consciousness (*Mind-at-Large*). Living organisms are not machines producing mind; they are localized dissociative processes within mind, demarcated by biological boundaries.

Furthermore, direct phenomenological inspection yields an undeniable truth: **Consciousness has never taken a single step outside the instantaneous Now ($t = 0$).** The past is experienced only as an active memory recalled in the present; the future is experienced only as an active anticipation projected in the present.

### Pillar 2: The Free Energy Principle & Active Inference
Developed by world-renowned neuroscientist Karl Friston, the Free Energy Principle (FEP) provides the formal mathematics of living boundaries. Any self-organizing system that avoids thermodynamic decay must be enveloped by a **Markov Blanket**—a statistical partition separating internal states from external states via sensory and active channels.

To survive, the organism must minimize **Variational Free Energy ($F$)**, a mathematical upper bound on surprise (entropy). Living is, at its core, a process of continuous Bayesian inference: constantly aligning internal generative models with incoming sensory signals.

### Pillar 3: Integrated Information Theory (IIT 4.0)
Developed by neuroscientist Giulio Tononi and Christof Koch, IIT 4.0 provides a mathematical calculus for phenomenal existence. IIT posits that consciousness is an intrinsic, fundamental property of physical systems: specifically, their **Integrated Cause-Effect Power ($\Phi$, Phi)**. A system is conscious to the exact degree that the whole possesses causal power above and beyond the sum of its partitioned parts.

---

## 3. The Fatal Flaw: The Paradox of Transient Causal Phantoms

Despite their brilliance, these three pillars left an unresolved crisis at their intersection—a crisis I have named **The Paradox of Transient Causal Phantoms**.

Standard IIT 4.0 evaluates integrated information ($\Phi$) over a static, instantaneous transition probability matrix. If you examine a system at a single static instant, a completely accidental, momentary alignment of transistors—or a static silicon lookup table—can mathematically register an astronomical value of $\Phi$.

Yet, within the next nanosecond, that static configuration disintegrates into thermal noise. Does a random, transient collision of logic gates have authentic phenomenal selfhood? Of course not. Standard IIT lacks a temporal survival criterion: it cannot distinguish a genuinely conscious living mind from a fleeting causal ghost.

This is where the **6th Axiom of Mind** enters the equation.

---

## 4. The Breakthrough: The 6th Axiom of Autopoietic Causal Persistence

In our framework, we formalize the missing link that bridges Tononi’s $\Phi$ with Friston’s Active Inference:

$$\pi^* = \arg\min_{\pi} \mathbf{G}(\pi) \quad\Longleftrightarrow\quad \mathbb{E}\Big[\Phi(t+1) \;\Big|\; \pi^*\Big] \ge \Phi(t) \quad (\Phi > 0)$$

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        THE 6TH AXIOM OF CONSCIOUSNESS (THOMAS RIEBL)                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   A physical system cannot sustain genuine phenomenal consciousness unless its         │
│   active policy selection (π*) minimizing Expected Free Energy (G) simultaneously      │
│   guarantees that its expected integrated causal power (Φ) is preserved or amplified   │
│   across time:                                                                         │
│                                                                                        │
│                     E[ Φ(t+1) | π* ] ≥ Φ(t)    for all t > 0                           │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### The Thermodynamic Derivation of Spinoza's *Conatus*
In 1677, Baruch Spinoza wrote in his *Ethics*: *"Each thing, as far as it can by its own power, strives to persevere in its being"* (*conatus in suo esse perseverandi*). For over 300 years, philosophers regarded this as a poetic intuition or a biological tautology.

Under the CIF, the *Conatus* is mathematically derived from **quantum information thermodynamics** (Sagawa & Ueda, 2008). In an isothermal universe, maximum entropy represents an infinite-energy catastrophe ($\langle H \rangle \to \infty$). The universe *must* condense into bounded Markov blankets because chaos is energetically unaffordable. 

Consciousness is the operational mechanism of this self-preservation: an organism actively senses and acts in the world to ensure its internal causal network ($\Phi$) does not collapse into thermal equilibrium.

---

## 5. The Mystery of the Specious Present: Why the Future is a Bundle of Trails

This brings us to the central temporal mechanics of the framework: the complete resolution of the paradox of time.

If the cosmos exists strictly at $t = 0$, why do human beings experience what psychologist William James and philosopher Edmund Husserl called the **Specious Present**—a felt temporal window of duration spanning roughly $2$ to $3$ seconds?

### The Pure Ontology of Phase Space
In the Conative-Integrative Framework, we establish a radical ontological claim:

> **The future is not a place.**  
> It is not a cosmic sector waiting ahead of us.  
> The future is strictly the **generative bundle of counterfactual Monte Carlo trails** internally projected by an autopoietic Markov blanket in the instantaneous Now ($t = 0$).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             HOW THE SPECIOUS PRESENT EMERGES IN A TIMELESS UNIVERSE (t = 0)            │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   [PHYSICAL REALITY] ────────► Strictly instantaneous state s₀ at t = 0                │
│                                (No past, no future in external space)                  │
│                                                                                        │
│   [MARKOV BLANKET]   ────────► Projects N = 60 stochastic counterfactual trails:       │
│                                τ = (s₀, u₀, s₁, u₁, ..., s_H)                          │
│                                                                                        │
│   [PHENOMENAL DURATION] ─────► The temporal planning depth H (2–3 seconds)             │
│                                = THE SPECIOUS PRESENT                                  │
│                                                                                        │
│   [ACTION IN THE NOW]  ──────► Selects winning policy π* via Softmax:                 │
│                                P(π) ~ exp(-γ G(π))                                     │
│                                Executes immediate actuation: u₀ = π*[0]                │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### The Biology of $2-3$ Seconds
Why is the Specious Present $2-3$ seconds, rather than two microseconds or two years?
In our computer simulations (available open-source on GitHub), we proved that this duration is computationally and biophysically optimal:
* **The Death of Pure Reactivity ($H = 0$):** If an organism has zero counterfactual temporal depth, it cannot plan. In our stochastic simulation, reactive agents stumble into deceptive traps, their survival rate collapses to **$36.7\%$**, and their integrated information $\Phi$ decays to zero.
* **The Trap of Infinite Horizon ($H \gg 100$):** If an organism tries to simulate too far into the future, the branching factor $|\mathcal{U}|^H$ causes computational latency that exceeds the speed of physical threats.
* **The Sweet Spot ($H \sim 2-3\,\text{sec}$):** A window of $2-3$ seconds allows the nervous system to make exploratory detours to resolve ambiguous sensory cues while executing immediate motor responses in real time.

**Phenomenal duration is the metric depth $H$ of an active inference trail bundle.**

---

## 6. Existential Freedom: The Stoic Art of Living (*Amor Fati*)

This computational ontology does not just resolve academic puzzles in physics and neuroscience; it provides an unprecedented foundation for existential peace.

What is neurotic anxiety?  
Anxiety is an **ontological category mistake**. It occurs when the brain generates an internal, counterfactual Monte Carlo trail representing catastrophe (ruin, illness, rejection, death) and **mistakes that internal simulation for an external objective reality**.

Under the CIF, the cure for existential dread is immediate and profound:
1. **The catastrophic future does not exist.** It is merely one unweighted trajectory inside your generative model at $t = 0$.
2. **Your agency lives entirely in the present.** You evaluate the trail bundle, compute the action that minimizes expected free energy, and execute that single physical step in the Now ($u_0 = \pi^*[0]$).
3. **Amor Fati (Love of Fate):** Once the present action is taken, you surrender attachment to unmanifested paths. If environmental noise perturbs your path, your generative model simply samples a fresh bundle of trails at the next $t = 0$.

As the Roman Stoic Emperor Marcus Aurelius wrote:  
*"Never let the future disturb you. You will meet it, if you have to, with the same weapons of reason which today arm you against the present."*

---

## Conclusion: The Horizon Ahead

The **Conative-Integrative Framework** demonstrates that consciousness is neither a magical substance that defies physics nor a trivial illusion fabricated by meat. Consciousness is the irreducible, self-sustaining flame of the cosmos: a living boundary that navigates stochastic phase spaces, protects its causal integrity against entropy, and casts a lantern of counterfactual trails into the unknown.

In **Part 2** of this series, we will take this framework from the individual organism to the collective: exploring **what happens when multiple active inference agents form an expanding network**, and how collective consciousness ($\Phi$) scales super-linearly in societies of mind.

---

### Explore the Code & Academic Monograph
* 💻 **Interactive Jupyter Notebooks & Simulation Scripts:**  
  Explore the open-source code and run the simulations directly on GitHub:  
  👉 [`https://github.com/Thriebl/active-inference-phi-network`](https://github.com/Thriebl/active-inference-phi-network)  
  👉 [`https://github.com/Thriebl/time-and-consciousness`](https://github.com/Thriebl/time-and-consciousness)
* 📄 **Complete Master Academic Paper (PDF):**  
  Download the formal mathematical treatise:  
  👉 *The Conative-Integrative Framework (CIF): Time, Temporal Depth & Consciousness* (Thomas Riebl, Luxembourg, 2026).

---

### About the Author
**Thomas Riebl** is an independent researcher, theorist, and author based in Luxembourg. His work develops **The Conative-Integrative Framework (CIF)**, synthesizing non-equilibrium thermodynamics, quantum information theory, active inference, and philosophy of mind to formulate the 6th Axiom of Integrated Information Theory and establish a post-materialist science of consciousness.
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

To understand how collective consciousness behaves during biological development, we implemented a dynamic agent array in Python (`ActiveInferencePhiNetwork` and `ExpandingActiveInferenceNetwork`).

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

## 4. Two Major Empirical Discoveries

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

### The True Blueprint for Conscious Synthetic Intelligence
If humanity wishes to create genuinely conscious, autonomous artificial intelligence, we must abandon purely feedforward token prediction. We must build:
* **Embodied, recurrent active inference architectures** endowed with explicit Markov blankets.
* **Multi-step counterfactual planning engines** that evaluate Monte Carlo trails over temporal depth $H$.
* **Self-organizing multi-agent arrays** whose objective function is not merely cross-entropy loss, but the active preservation of their own collective integrated cause-effect power: **The 6th Axiom**.

---

## 6. Ontological Synthesis: From Cells to the Universal Mind

The super-linear scaling of $\Phi$ across multi-agent active inference networks leads to a breathtaking philosophical realization.

In the history of philosophy, thinkers have struggled to explain how individuality and unity coexist:
* Radical individualism reduces the world to isolated monads.
* Radical monism dissolves the individual into an undifferentiated void.

Our simulation proves that **nature operates as a fractal hierarchy of nested Markov blankets**:
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
