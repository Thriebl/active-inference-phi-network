#!/usr/bin/env python3
"""
Build Documentation and Printable PDFs for Planar Inverted Pendulum ACI Didactic.
Generates:
1. planar_inverted_pendulum_aci_didactic_en.md (English Obsidian Note)
2. planar_inverted_pendulum_aci_didactic_de.md (German Obsidian Note)
3. planar_inverted_pendulum_aci_didactic_en.pdf (English A4 Printable PDF with page numbers)
4. planar_inverted_pendulum_aci_didactic_de.pdf (German A4 Printable PDF with page numbers)
Copies all outputs to Obsidian (/home/thr/Documents/ThRNotes/04-projects/inverse_pendulum_aci/)
and project directories (/home/thr/Documents/04-projects/inverse_pendulum_aci/).
"""

import os
import shutil
import subprocess

def get_markdown_en():
    md = r"""<img src="conative_systems_logo.svg" align="right" width="125" style="float: right; margin-left: 20px; margin-bottom: 15px;" alt="Conative Systems Logo" />

# Active Conative Inference (ACI): The Planar Inverted Pendulum
### A Didactic First-Principles Walkthrough of Perception, Action, Vitality, and Online Learning in a Planar 2D System

**Author:** Thomas Riebl  
**Organization:** Conative Systems S.à r.l.  
**Theoretical Basis:** Active Conative Inference (ACI), Free Energy Principle (FEP), Integrated Information Theory ($\Phi$ / IIT 4.0, Giulio Tononi), Spinozan Conatus, Patent 01 & 11  
**Target Architecture:** Freestanding ANSI C99 Edge Microcontrollers (Zero Dynamic Heap)

---

## 1. Physical Intuition: The Palm-Balancing Paradox & Planar Architecture

Before formalizing any mathematics or probability matrices, let us anchor the system in everyday physical intuition.

Imagine balancing a long broomstick vertically on the open palm of your hand:
* When the top of the stick begins tilting to the **right**, what must your hand do?
* Human instinct might mistakenly tempt you to pull your hand away to the left. But classical Newton-Euler physics dictates the exact opposite: your hand must dart quickly to the **RIGHT**, positioning the base pivot directly underneath the falling Center of Mass (CoM).
* The resulting inertial reaction torque swings the rod back toward vertical balance ($0^\circ$).

In this planar 2D system, motion is strictly constrained to a single vertical plane: the base cart moves along the horizontal $x$-axis, and the pendulum tilts strictly **Left** ($l$) or **Right** ($r$). Out-of-plane forward/rear degrees of freedom are mechanically constrained.

---

### 1.1 Physical Kinematic Diagram (Step 1: The Intuitive Cart-Pole)

The following vector graphic illustrates the fundamental physical setup before introducing discrete probability bins or matrix mathematics:

![1. Physical System: The Planar Inverted Pendulum](inverted_pendulum_step1_physics.svg)

#### Visual Elements of the Physical Stage:
1. **The Mobile Base Cart (Mass $M$):** Constrained to move strictly along the horizontal $x$-axis on the linear floor track (Left ↔ Right). There are no out-of-plane forward/rear degrees of freedom.
2. **The Rigid Balancing Rod (Length $L$, Mass $m$):** Attached to the cart at a low-friction pivot pin $(x, 0)$, tilting freely at continuous angle $\theta$.
3. **Vertical Equilibrium ($\theta = 0^\circ$, Green Dashed Line):** The unstable mechanical equilibrium stance where the Center of Mass (CoM) is positioned vertically above the pivot.
4. **The Palm-Balancing Paradox:** If the rod tips to the right ($+\theta$), the cart must accelerate rapidly to the **RIGHT** to position the pivot underneath the falling mass and swing the rod back upright.

---

## 2. The Agent's Mind: Bayes' Theorem & Foundational Probability

Now that the physical pendulum and its balance mechanics are visually and intuitively grounded, we turn to the controller: **How does the agent infer what is happening in the real world?**

In classical textbook control theory, controllers often assume instantaneous, perfect knowledge of the true angle $\theta$. In reality, physical sensors are noisy, encoders have quantization jitter, and air currents disturb the rod. The agent never has direct, omniscient access to the outside world; it must continually infer what is happening through its sensory boundary (the **Markov blanket**).

### Core Notational Elements: $s, o, a, p, P, q$

* **$s$ (Hidden State):** The true, unobservable physical condition of the external world (e.g., the actual tilt angle of the rod $\theta \in \mathcal{S}$). The agent can never touch $s$ directly.
* **$o$ (Observation):** The noisy sensory measurement registered by the agent's sensors at the boundary (e.g., optical encoder reading or proprioceptive sensor $o \in \mathcal{O}$).
* **$a$ (Action):** The physical intervention or motor command emitted by the agent into the environment (e.g., base cart acceleration $a \in \mathcal{A}$).
* **$p(\cdot)$ (Probability Distribution):** The mathematical function or probability vector spanning across the entire state or observation space (e.g., prior distribution $p(s)$, likelihood distribution $p(o \mid s)$, transition dynamics $p(s' \mid s, a)$).
* **$P(\cdot)$ (Specific Probability Scalar):** The concrete numerical value assigned to an individual outcome or discrete event, strictly bounded in the unit interval ($P \in [0, 1]$). For instance, $P(s = 0) = 0.92$ or $P(\text{Rain}) = 0.20$.
* **$q(s)$ (Recognition Density):** The agent's internal, approximate belief distribution over hidden states $s$, continually optimized to minimize Variational Free Energy $F$.
* **The Conditioning Bar ($\mid$):** Read as **"given"**. For instance, $p(s \mid o)$ is read as *"the probability distribution over hidden states $s$ **given** sensory observation $o$"*.

---

### Bayes' Theorem in Perception

Bayes' Theorem provides the exact mathematical law for updating an internal distribution in light of incoming noisy sensory evidence:

$$p(s \mid o) = \frac{p(o \mid s) \cdot p(s)}{p(o)} = \frac{p(o \mid s) \cdot p(s)}{\sum_{s'} p(o \mid s') \cdot p(s')}$$

---

#### Intuitive Everyday Example: The Wet Street Paradox ($s = \text{Rain}$, $o = \text{Street is Wet}$)

To make the interaction of these probabilistic terms and the indispensable role of the denominator $P(o)$ immediately graspable before formalizing matrices, consider an everyday scenario:

* **Hidden World State $s$ (Unobserved weather outside):**
  * $s_1 = \text{Rain}$ (Prior belief: $P(\text{Rain}) = 0.20$ or $20\%$)
  * $s_2 = \text{No Rain}$ (Prior belief: $P(\text{No Rain}) = 0.80$ or $80\%$)
* **Sensory Observation $o$ (Looking out the window):**
  * $o = \text{The street is wet}$

**Why could the street be wet? (Two competing causal pathways):**
1. **Path 1 (True Rain):** If it rains, the street is almost certainly wet: $P(\text{Wet} \mid \text{Rain}) = 0.99$ ($99\%$).
2. **Path 2 (Sensor Ambiguity / External Factor):** There is no rain, but a street cleaning truck passed by or a neighbor ran the garden sprinkler: $P(\text{Wet} \mid \text{No Rain}) = 0.05$ ($5\%$).

**Calculating Marginal Evidence $P(o)$ (Total Probability of Seeing a Wet Street):**

$$\begin{aligned}
P(\text{Wet}) &= \underbrace{P(\text{Wet} \mid \text{Rain}) \cdot P(\text{Rain})}_{\text{Wet via Rain } (0.99 \cdot 0.20 = 0.198)} + \underbrace{P(\text{Wet} \mid \text{No Rain}) \cdot P(\text{No Rain})}_{\text{Wet via Sprinkler } (0.05 \cdot 0.80 = 0.040)} \\
&= 0.198 + 0.040 = \mathbf{0.238} \; (23.8\%)
\end{aligned}$$

**Applying Bayes' Theorem (Is it really raining?):**  
When you look out the window and observe that the street is wet ($o$), your updated posterior belief that it is actually raining becomes:

$$P(\text{Rain} \mid \text{Wet}) = \frac{P(\text{Wet} \mid \text{Rain}) \cdot P(\text{Rain})}{P(\text{Wet})} = \frac{0.198}{0.238} \approx \mathbf{83.2\%}$$

* The denominator $P(o) = 0.238$ normalizes the evidence.
* Seeing the wet street dramatically increases your belief in rain from $20\%$ to $83.2\%$—but not to $100\%$, because Bayes' Theorem fairly accounts for the alternative causal pathway (the garden sprinkler)!
* In our inverted pendulum, $P(o)$ serves this exact mathematical role: it dynamically balances prior physical momentum against noisy sensor-encoder readings.

---

## 3. Mapping the Physical World to Active Inference: Four Intuitive Objects

By constraining the system to a single plane (Left/Right), our generative model simplifies down to just **5 states** and **2 actions**:

1. **Where do we need to be? $\to \mathbf{C}$ (Phenotypic Preference):**  
   The biological/autopoietic desire of the system. Upright equilibrium ($s_0$) is homeostatic bliss ($C_0 = 0.0$). Mild tilts carry small surprise penalty ($C = -1.5$). Catastrophic tipping is existential disaster ($C = -8.0$).
2. **Where do we believe we start? $\to \mathbf{D}$ (Prior Belief):**  
   The initial hypothesis before taking the first measurement ($92\%$ certainty of standing upright at $t = 0$).
3. **How clearly do we see the rod? $\to \mathbf{A}$ (Likelihood Matrix):**  
   A transparent $5 \times 5$ matrix capturing sensor fidelity ($92\%$ diagonal precision, with $4\%$ blur into directly adjacent tilt states).
4. **What happens when we move the cart? $\to \mathbf{B}(a)$ (Causal Transition Tensors):**  
   Two intuitive $5 \times 5$ matrices ($\mathbf{B}(l)$ and $\mathbf{B}(r)$) encoding the laws of Newton-Euler physics: accelerating right ($a = r$) when tilted right ($r_1$) restores vertical balance ($0$) with $88\%$ probability.

---

### The Four Core Components of Bayes' Theorem (Formal Matrix Mapping)

With the intuitive objects ($\mathbf{C}, \mathbf{D}, \mathbf{A}, \mathbf{B}$) and the wet street paradox established, we can formalize how Bayes' Theorem operates inside the agent:

1. **Prior Distribution $p(s)$ (What we expect before sensing $\to \mathbf{D}$):**  
   What the agent believes about the world **before** looking at the new sensory reading. In our pendulum, this is either the initial upright stance vector $\mathbf{D} = p(s_0)$ or the forward prediction generated by the transition model:
   $$s_{\text{pred}} = \mathbf{B}(a_{t-1}) \cdot s_{t-1}$$
   *(In the rain example: $P(\text{Rain}) = 20\%$.)*
2. **Likelihood Distribution $p(o \mid s)$ (Sensor Precision $\to \mathbf{A}$):**  
   The generative mapping: *"If the rod were genuinely in physical state $s$, how probable is it that our sensor reports observation $o$?"*  
   This captures the fidelity and precision of the sensory apparatus, including sensor noise $\varepsilon$ and diagonal precision $\gamma_s$.  
   *(In the rain example: $P(\text{Wet} \mid \text{Rain}) = 99\%$ vs. $P(\text{Wet} \mid \text{No Rain}) = 5\%$.)*
3. **Posterior Distribution $p(s \mid o)$ (Read: "$s$ given $o$" $\to$ Recognition Density $q(s)$):**  
   The updated, optimal belief distribution about the hidden state $s$ **after** assimilating observation $o$. Perception in Active Inference is nothing other than minimizing the discrepancy (Variational Free Energy $F$) between this Bayesian posterior $p(s \mid o)$ and the agent's internal recognition density $q(s)$.  
   *(In the rain example: $P(\text{Rain} \mid \text{Wet}) = 83.2\%$.)*
4. **Marginal Evidence Distribution $p(o)$ (Normalization & Phenotypic Preference $\to \mathbf{C}$):**  
   The total probability distribution over observation states. Its logarithm $\ln p(o)$ forms the homeostatic phenotype preference vector $\mathbf{C}$.  
   *(In the rain example: $P(\text{Wet}) = 23.8\%$.)*

---

## 4. Formal 5-State Mathematical Specification & State Compass

### 1.2 State Space Architecture (Step 2: Discretization & Conatus Horizons)

To build a computable generative model, we discretize the continuous angle $\theta$ into **5 conative states** ($\mathcal{S}$) and define the **Conatus survival limit**:

![2. Discrete State Space & Conatus Survival Barrier](inverted_pendulum_step2_states.svg)

#### The 5 Discrete States & Physical Thresholds:
* **State $s_0 = 0$ (Green):** Vertical upright equilibrium stance ($|\theta| \le 3^\circ$). Homeostatic attractor ($C_0 = 0.0$, $\Phi = 1.00$).
* **States $s_1 = l_1, s_3 = r_1$ (Amber):** Mild tilt left or right ($3^\circ < |\theta| \le 15^\circ$). Easily stabilized with standard counter-steering ($C = -1.5$, $\Phi = 0.70$).
* **States $s_2 = l_2, s_4 = r_2$ (Red):** Severe tipping left or right ($15^\circ < |\theta| < 35^\circ$). Strong restorative torque needed ($C = -8.0$, $\Phi = 0.15$).
* **Conatus VETO Limit (Red Dashed Line at $\pm 35^\circ$):** Point of No Return. Excursions beyond $\pm 35^\circ$ cannot be recovered by motor torque; any policy leading here triggers an emergency Conatus-Veto ($G^* \to +\infty$).

### Discrete State Space ($|\mathcal{S}| = 5$) and Action Space ($|\mathcal{A}| = 2$)

* **States:** $\mathcal{S} = \{0, l_1, l_2, r_1, r_2\}$
  * $s_0 = 0$: Upright Stance (Balanced / Homeostatic Attractor)
  * $s_1 = l_1$: Slight Tilt Left ($\theta \approx -12^\circ$)
  * $s_2 = l_2$: Severe Fall Left ($\theta \approx -26^\circ$)
  * $s_3 = r_1$: Slight Tilt Right ($\theta \approx +12^\circ$)
  * $s_4 = r_2$: Severe Fall Right ($\theta \approx +26^\circ$)
* **Actions:** $\mathcal{A} = \{l, r\}$
  * $a = 0$ ($l$): Accelerate Base LEFT ⬅
  * $a = 1$ ($r$): Accelerate Base RIGHT ➔

---

### Prior Belief Vector $\mathbf{D}$ (Initial State Prior & Predictive Recurrence)

How does the agent form a prior prediction $s_{\text{pred}}$ about the hidden world state before processing the next sensor observation?

1. **Continuous Operation ($t \ge 1$):**  
   Once in motion, the agent projects its belief forward using the causal transition tensor $\mathbf{B}$ and the last emitted motor action $a_{t-1}$:
   $$s_{\text{pred}}(t) = \mathbf{B}(a_{t-1}) \cdot s_{t-1}$$
2. **System Initialization ($t = 0$):**  
   At the very first time step when the controller powers on, no previous action $a_{-1}$ and no previous state $s_{-1}$ exist.  
   **Vector $\mathbf{D}$ serves as the essential initial condition for this predictive recurrence:**
   $$s_{\text{pred}}(t=0) = \mathbf{D} = p(s_0) = \begin{pmatrix} 0.92 \\ 0.04 \\ 0.00 \\ 0.04 \\ 0.00 \end{pmatrix} \begin{matrix} (0: \text{Upright balanced}) \\ (l_1: \text{Slight tilt left}) \\ (l_2: \text{Severe fall left}) \\ (r_1: \text{Slight tilt right}) \\ (r_2: \text{Severe fall right}) \end{matrix}$$

* $P(s_0 = 0) = 0.92$: The agent powers on with high confidence that it starts in the upright balanced stance.
* $P(s_0 = l_1) = P(s_0 = r_1) = 0.04$: Minor residual uncertainty ($4\%$) ensures perceptual flexibility and avoids numerical zero-probability traps.
* $P(s_0 = l_2) = P(s_0 = r_2) = 0.00$: Zero initial probability for severe collapse.
* **Strict Probability Conservation:** $\sum_{i=0}^4 D_i = 0.92 + 0.04 + 0.00 + 0.04 + 0.00 = \mathbf{1.00}$ ($\mathbf{100\%}$).

---

### Preference Vector $\mathbf{C}$ & Target Distribution $p(o)$ (The 3-Step Derivation)

In Active Inference, an agent's goals are not framed as arbitrary rewards, but as **phenotypic prior expectations**: the agent actively acts to observe what it expects to see in order to maintain its structural integrity.

#### Step 1: Definition of the Target Observation Probabilities $p(o)$
We define what observation angles the inverted pendulum expects to measure:
* **$P(o_0 : \text{Upright balanced}, |\theta| \le 3^\circ) \approx 69.1\,\%$:** The ideal operational regime.
* **$P(o_{l1}, o_{r1} : \text{Slight tilt}, 3^\circ < |\theta| \le 15^\circ) \approx 15.4\,\%$ each:** Tolerable everyday perturbations.
* **$P(o_{l2}, o_{r2} : \text{Catastrophic fall}, |\theta| > 15^\circ) \approx 0.023\,\%$ each:** Dangerous tipping boundaries that the agent expects practically never to observe.

As a normalized probability vector $p(o) \in [0, 1]^5$:
$$p(o) = \begin{pmatrix} 
0.6911 \\ 
0.1542 \\ 
0.00023 \\ 
0.1542 \\ 
0.00023 
\end{pmatrix} 
\begin{matrix} 
(o_0: \text{Upright balanced} \approx \mathbf{69.1\,\%}) \\ 
(o_{l1}: \text{Slight tilt left} \approx \mathbf{15.4\,\%}) \\ 
(o_{l2}: \text{Catastrophic fall left} \approx \mathbf{0.02\,\%}) \\ 
(o_{r1}: \text{Slight tilt right} \approx \mathbf{15.4\,\%}) \\ 
(o_{r2}: \text{Catastrophic fall right} \approx \mathbf{0.02\,\%}) 
\end{matrix}$$

* **Strict Probability Conservation:** All entries are strictly positive and sum exactly to $1.0$ ($100\,\%$):  
  $\sum_{i=1}^5 P(o_i) = 0.6911 + 0.1542 + 0.00023 + 0.1542 + 0.00023 = \mathbf{1.0000}$.

#### Step 2: Deriving the Preference Vector $\mathbf{C} = \ln p(o)$
Active Inference algorithms evaluate Expected Free Energy in logarithmic information space (nats). Taking the natural logarithm of the defined probabilities yields:
* $\ln(0.6911) = \mathbf{-0.369}$
* $\ln(0.1542) = \mathbf{-1.869} = -0.369 - 1.5$
* $\ln(0.00023) = \mathbf{-8.369} = -0.369 - 8.0$

Subtracting the baseline offset $-0.369$ (zero-calibration) produces the clean **Preference Vector $\mathbf{C}$**:
$$\mathbf{C} = \ln p(o) - \max(\ln p(o)) = \begin{pmatrix} 0.0 \\ -1.5 \\ -8.0 \\ -1.5 \\ -8.0 \end{pmatrix} \begin{matrix} (o_0: \text{Upright}) \\ (o_{l1}: \text{Slight left}) \\ (o_{l2}: \text{Fall left}) \\ (o_{r1}: \text{Slight right}) \\ (o_{r2}: \text{Fall right}) \end{matrix}$$

* $\mathbf{C}_0 = 0.0$: Maximum preference (zero surprise / minimum Free Energy in equilibrium).
* $\mathbf{C}_{\text{Level 1}} = -1.5$: Mild aversion against minor tilts (drives corrective counter-steering).
* $\mathbf{C}_{\text{Level 2}} = -8.0$: Catastrophically negative score (repulsive potential against tipping).

#### Step 3: The Softmax Bridge in Code ($p(o) = \operatorname{softmax}(\mathbf{C})$)
In software implementations, engineers directly configure $\mathbf{C}$. The **Softmax operator** (Boltzmann-Gibbs distribution) maps these log-preferences back to the exact physical probability distribution:
$$P(o_i) = \sigma(\mathbf{C})_i = \frac{e^{C_i}}{\sum_{j=1}^5 e^{C_j}} \implies p(o) = \operatorname{softmax}(\mathbf{C})$$
With partition sum $Z = \sum_{j=1}^5 e^{C_j} = e^{0.0} + 2 e^{-1.5} + 2 e^{-8.0} \approx 1.4469$, $\operatorname{softmax}(\mathbf{C})$ recovers precisely the $69.1\,\%, 15.4\,\%, 0.02\,\%$ target distribution!

#### 💡 Summary:
* **The Probability Space ($\mathbf{A}, \mathbf{B}, \mathbf{D}, p(o)$):** All values are true probabilities ($P \in [0, 1]$), strictly positive, summing to $1.0$.
* **The Log-Preference Space ($\mathbf{C}$ in nats):** Working space for Free Energy calculations ($\mathbf{C} = \ln p(o)$), where improbable events have large negative scores that penalize dangerous actions.
* **The Softmax Bridge:** Links both spaces: $p(o) = \operatorname{softmax}(\mathbf{C}) \iff \mathbf{C} \cong \ln p(o)$.

---

### Likelihood Matrix $\mathbf{A}$ (Sensor Precision)

The matrix $\mathbf{A} \in \mathbb{R}^{5 \times 5}$ maps the hidden physical world state $s$ to sensory observations $o$ across the Markov blanket: $p(o \mid s)$.

For optical or proprioceptive sensing with precision $\gamma_s = 0.92$ and neighboring perceptual noise $\varepsilon = 0.04$:

$$\mathbf{A} = p(o \mid s) = \begin{pmatrix}
0.92 & 0.04 & 0.00 & 0.04 & 0.00 \\
0.04 & 0.92 & 0.04 & 0.00 & 0.00 \\
0.00 & 0.04 & 0.96 & 0.00 & 0.00 \\
0.04 & 0.00 & 0.00 & 0.92 & 0.04 \\
0.00 & 0.00 & 0.00 & 0.04 & 0.96
\end{pmatrix}$$

* The main diagonal dominates: The actual motion of the pendulum is registered with over 92% reliability.
* Perceptual leakage occurs strictly into directly adjacent tilt stages ($4\%$).

---

### Transition Tensors $\mathbf{B}(a)$ (Causal Dynamics)

For each of the 2 discrete actions $a \in \{l, r\}$, an explicit transition matrix $\mathbf{B}(a) \in \mathbb{R}^{5 \times 5}$ specifies $p(s_{t+1} \mid s_t, a)$.

#### Action $a = r$ (Base Accelerates Right)

$$\mathbf{B}(r) = p(s' \mid s, a = r) = \begin{pmatrix}
0.15 & 0.00 & 0.00 & 0.88 & 0.00 \\
0.85 & 0.10 & 0.00 & 0.02 & 0.00 \\
0.00 & 0.90 & 1.00 & 0.00 & 0.00 \\
0.00 & 0.00 & 0.00 & 0.10 & 0.85 \\
0.00 & 0.00 & 0.00 & 0.00 & 0.15
\end{pmatrix}$$

* From $s = r_1$ (slight right tilt): Rightward jerk $\to$ restores balance to $0$ with $P = 0.88$, lingers in $r_1$ with $P = 0.10$, overshoots to $l_1$ with $P = 0.02$.
* From $s = r_2$ (severe right tilt): Rescues the system from $r_2$ back to $r_1$ with $P = 0.85$.
* From $s = 0$ (balanced): Unnecessary rightward jerk tilts the pendulum leftward ($l_1$) with $P = 0.85$.
* From $s = l_1$ (already tilted left): Rightward jerk accelerates collapse to the left ($l_2$) with $P = 0.90$.

#### Action $a = l$ (Base Accelerates Left — Symmetrically Inverted)

$$\mathbf{B}(l) = p(s' \mid s, a = l) = \begin{pmatrix}
0.15 & 0.88 & 0.00 & 0.00 & 0.00 \\
0.00 & 0.10 & 0.85 & 0.00 & 0.00 \\
0.00 & 0.00 & 0.15 & 0.00 & 0.00 \\
0.85 & 0.02 & 0.00 & 0.10 & 0.00 \\
0.00 & 0.00 & 0.00 & 0.90 & 1.00
\end{pmatrix}$$

---

### 5. The Conative ACI Distinction (Thomas Riebl)

In myopic classical Active Inference ($H = 1$), the agent greedily selects the action that maximizes $\mathbf{C}$ at the immediate next step.

Under Active Conative Inference:
* **Temporal Horizon $H \ge 2$:** The agent anticipates overshoot. Accelerating too aggressively to the right at $r_1$ induces an uncontrollable $l_2$ at $t + 2$.
* **Systemic Vitality Monitoring $\Phi(s)$ (Integrated Information Theory / IIT 4.0, Giulio Tononi):**
  * $\Phi(0) = 1.00\text{ nats}$ (Maximum systemic coherence and autopoietic health)
  * $\Phi(l_1, r_1) = 0.70\text{ nats}$ (Mild perturbation)
  * $\Phi(l_2, r_2) = 0.15\text{ nats}$ (Critical boundary hazard)
* **Conatus-Veto:** When projected vitality falls below $\Phi < 0.25\text{ nats}$ or actuator stress poses structural hazards, the Conatus-Veto immediately blocks the destructive trajectory and enforces stabilizing damping.

---

## 5. Action Planning ($G^*$-Minimization) & Complete Closed-Loop System

### 1.3 Complete Closed-Loop System (Step 3: Torques, Actions & Generative Matrices)

Having established the physical cart-pole (Step 1) and the discrete state compass (Step 2), we now integrate the active forces, corrective motor policies, and the complete $5 \times 5$ generative model:

![3. Complete Planar ACI System: Kinematics, Forces & 5x5 Tensors](inverted_pendulum_step3_complete.svg)

#### Closed-Loop Dynamic Elements:
* **Overturning Torque $\tau_{\text{grav}} = m g L \sin\theta$:** Whenever tilted (e.g. state $s_4 = r_2$), gravity pulls the Center of Mass downward ($\vec{F}_g$).
* **Restoring Counter-Steering $\vec{a}_{\text{base}}$:** The agent emits motor action $a = r$ (Accelerate Base Right ➔), thrusting the pivot beneath the Center of Mass to reverse torque.
* **Expected Free Energy Minimization ($G^*$):** Action selection minimizes anticipated surprise while defending systemic vitality $\Phi$ over temporal horizon $H \ge 2$:

$$G^*(a) = G_{\text{pragmatic}}(a) - \lambda_\Phi \cdot \Phi(a, H) \cdot \sqrt{H} + \Omega_{\text{conatus\_veto}}$$

* **Pragmatic Term:** $-\mathbb{E}_{q(s_{t+1})}[\mathbf{C}]$ (distance from phenotypic attractor $s_0$).
* **Conative Vitality Term:** Projected systemic health $\Phi$ weighted by temporal depth $\sqrt{H}$.
* **Conatus-Veto:** If projected vitality drops below critical threshold ($\Phi < 0.25\text{ nats}$), $G^* \to +\infty$, triggering an emergency damping policy.

---

## 6. Online Learning — Experience Counting (Causal Memory Updating)

### How the Agent Learns Cause and Effect: The Tally Counter Principle

Traditional deep neural networks and Reinforcement Learning algorithms require millions of trial-and-error training iterations, opaque weight matrices, and GPU clusters, and they constantly suffer from **"catastrophic forgetting"** (learning a new behavior can unpredictably erase previously mastered skills).

In Active Inference, learning how the physical world behaves is as transparent and intuitive as keeping an **experience tally chart (an empirical counter for each cause-and-effect transition)**:

1. **The Experience Bucket $\beta$:**  
   For every possible combination of current state $s$, motor action $a$, and resulting next state $s'$, the agent maintains a simple event counter $\beta_{s', s, a}$.
2. **Real-Time Increment:**  
   Every time the agent finds itself in state $s$ (e.g. tilted right), executes action $a$ (accelerates right), and observes that the pendulum transitioned to state $s'$ (upright balance), it simply adds to that counter:
   $$\beta_{s', s, a} \leftarrow \beta_{s', s, a} + 1$$
3. **From Counters to Probabilities:**  
   To predict future transitions with matrix $\mathbf{B}(a)$, the agent merely calculates the fraction of times this specific outcome occurred:
   $$\mathbf{B}_{s', s, a} = p(s' \mid s, a) = \frac{\text{Empirical count of }(s \xrightarrow{a} s')}{\text{Total experiences in state } s \text{ with action } a} = \frac{\beta_{s', s, a}}{\sum_{s''} \beta_{s'', s, a}}$$

#### Why This is Revolutionary for Embedded & Industrial Edge Control:
* **Single-Trial Instant Learning:** No backpropagation or gradient descent is required. The moment an unexpected perturbation or mechanical change occurs, the corresponding counter increments in constant time $O(1)$.
* **Zero Catastrophic Forgetting:** Prior empirical experiences are safely preserved in their respective state-action buckets.
* **Deterministic & Microcontroller-Ready:** In production C99, this is pure integer or floating-point addition—no dynamic heap allocation (`malloc`), no matrix inversions, and zero runtime jitter.

*(In formal Bayesian statistics, this natural tally-counter process is known as a **Dirichlet-Categorical conjugate update** — but physically and operationally, it is straightforward empirical experience counting.)*

---

## 7. Foundational Inquiries & Didactic FAQ

### FAQ 1: What makes this system "Intelligent"?
Intelligence in this framework is **neither passive statistical pattern matching (LLMs) nor ungrounded reward hunting (Reinforcement Learning)**.  
Intelligence is **active homeostasis and predictive autopoiesis under sensory noise and physical perturbation**:
* **Inference over Reflex:** Rather than reacting blindly to raw sensor readings (like a classical PID controller), the ACI agent maintains an internal generative hypothesis. It recognizes that sensory data is corrupted by noise, reconstructs the hidden physical state $s$, and anticipates future states over a deep temporal horizon ($H \ge 2$).
* **Autopoietic Self-Preservation (Conatus):** The agent does not optimize an external human-designed reward score. Its drive originates directly from its mandate to defend its structural and operational integrity ($\Phi$) against thermodynamic entropy and physical collapse.

---

### FAQ 2: What does the agent "learn"?
The agent learns the **true causal transition dynamics of its physical embodiment and environment**:
* It updates the conditional probability distribution tensor $\mathbf{B}(s' \mid s, a) = p(s' \mid s, a)$: *"When I am at state $s$ and execute action $a$, what is the exact probability distribution over landing in state $s'$?"*
* If environmental friction increases, motor voltage drops, or rod inertia changes, the agent does not retrain weights via backpropagation; it simply updates its transition beliefs online.

---

### FAQ 3: How does the agent learn?
Learning operates via **exact Bayesian Dirichlet count updates (experience tallying)** rather than stochastic gradient descent:
* The agent maintains count matrices (pseudo-counts $\beta_{s', s, a}$).
* Every observed transition incrementing state-action-successor counters directly refines transition matrix $\mathbf{B}$.
* **Key advantage:** Learning is instantaneous, online, numerically exact, and exhibits zero catastrophic forgetting.

---

### FAQ 4: What is the World Model in this example?
The **World Model** is the agent's internal generative representation of the physical environment, consisting of:
* **Hidden State Compass $\mathcal{S}$:** $\{0, l_1, l_2, r_1, r_2\}$ representing true rod deflection.
* **Sensor Likelihood Mapping $\mathbf{A}$:** The physical sensor model capturing noise and observation fidelity ($p(o \mid s)$).
* **Causal Dynamics $\mathbf{B}(a)$:** The transition tensor mapping actions to state shifts ($p(s' \mid s, a)$).

---

### FAQ 5: What is the Generative Model in this example?
The **Generative Model** is the complete joint probability distribution over observations, states, actions, and preferences:
$$p(o, s, a) = p(o \mid s) \cdot p(s \mid s_{t-1}, a) \cdot p(s_0) \cdot p_{\text{prior}}(a)$$
augmented with the phenotypic preference vector $\mathbf{C} = \ln p(o)$ and systemic vitality metric $\Phi(s)$. It enables the agent to evaluate the Expected Free Energy $G^*$ of counterfactual futures before committing physical torque.

---

### FAQ 6: Classical PID vs. Active Conative Inference (ACI) — Differences, Weaknesses, and Advantages

#### 1. What Classical PID Is and How It Operates
* **Proportional (P):** Corrective force proportional to current tracking error $e(t) = \theta_{\text{target}} - \theta_{\text{actual}}$.
* **Integral (I):** Corrective force accumulating past steady-state errors $\int e(\tau) d\tau$.
* **Derivative (D):** Corrective force dampening rate of change $\frac{de(t)}{dt}$.

#### 2. Weaknesses and Limitations of Classical PID
* **No World Model:** PID has zero understanding of cause and effect. It cannot predict what will happen 2 steps into the future.
* **Sensitivity to Noise (D-Term Amplification):** The derivative term violently amplifies high-frequency encoder noise, causing actuator chatter.
* **Integral Windup:** During strong disturbances, the I-term accumulates massive error, causing violent overshoot once the system recovers.
* **Zero Self-Protection:** PID blindly commands full motor current even if the rod has crossed the point of no return, burning out motors or snapping mechanical gears.

#### 3. Advantages of Classical PID
* Computationally negligible (requires ~10 floating-point operations).
* Extremely mature, intuitive tuning for simple linear regimes.

#### 4. Advantages of Active Conative Inference (ACI)
* **Optimal Kalman-Bayesian Filtering:** Naturally separates sensor noise from physical reality via matrix $\mathbf{A}$.
* **Deep Horizon Anticipation ($H \ge 2$):** Predicts and prevents overshoots before they physically manifest.
* **Autonomous Conatus Protection:** Conatus-Veto prevents motor burnout and structural self-destruction.
* **Instant Online Adaptation:** Adjusts to changing payload or friction without manual retuning.

#### 5. Trade-Offs / Costs of ACI
* Requires evaluating probability tensors ($5 \times 5$ matrices).
* Demands explicit definition of state ontologies and likelihood mappings.

---

### FAQ 7: How Exactly Does the Conatus-Veto Operate in This Inverted Pendulum Scenario?

#### 1. The Physical Problem: Inertia & The Whiplash Trap
When an inverted pendulum is recovering from an excursion, an aggressive counter-steering action creates enormous kinetic momentum. A myopic controller ($H = 1$) drives the rod back toward vertical ($0^\circ$) at high velocity, resulting in an uncontrollable opposite-side collapse (whiplash effect).

#### 2. The Conative Invariant: Vitality Mapping $\Phi(s)$
Under Spinoza's Conatus principle, an autopoietic system's primary imperative is the preservation of its organizational and physical integrity.
We operationalize this through Integrated Information Theory ($\Phi$ / IIT 4.0, Giulio Tononi):
* When upright ($s_0$), the system exhibits maximum structural vitality $\Phi = 1.00\text{ nats}$.
* At mild tilts ($l_1, r_1$), vitality dips safely to $\Phi = 0.70\text{ nats}$.
* At severe angles ($l_2, r_2$), vitality drops precipitously to $\Phi = 0.15\text{ nats}$.

#### 3. The Operation of the Conatus-Veto
The Conatus principle states that the preservation of life and structural integrity supersedes all task performance commands.
* Before executing action $a$, the agent computes expected vitality over horizon $H = 2$:
$$\Phi_{\text{projected}}(a) = \frac{1}{H} \sum_{\tau=1}^H \mathbb{E}_{q(s_\tau \mid a)}[\Phi(s_\tau)]$$
* If $\Phi_{\text{projected}}(a) < 0.25\text{ nats}$ (indicating that the policy risks driving the rod past $\pm 35^\circ$), the **Conatus-Veto** fires:
$$G^*(a) \to +\infty$$
* The proposed destructive policy is strictly vetoed. The system immediately substitutes an emergency damping action.

---

### FAQ 8: Python (and MicroPython) is Not Hard Real-Time Capable — How is This Resolved for Industrial Edge Hardware?

#### 1. Python as the Didactic Prototype vs. Native C99 Production
This documentation and its companion Jupyter notebook serve strictly as a **didactic reference architecture** designed for human inspection and mathematical clarity.

In commercial robotics, automation, and industrial deployment (patented by Conative Systems S.à r.l.):
* **Zero Python in Production:** The production inference engine contains zero Python, zero PyTorch, and zero external numerical libraries.
* **Pure Native C99 Core:** The entire ACI generative model, belief updater, and Expected Free Energy engine are written in **freestanding, ANSI C99**.

#### 2. Architectural Pillars of the Native C99 ACI Engine
* **Zero Dynamic Heap Allocation (`malloc` / `free` Forbidden):**
  All tensors, state vectors, Dirichlet accumulators ($\beta$), and working scratchpads are allocated as fixed, static structures at compile time. This eliminates memory fragmentation and unpredictable heap latency.
* **Deterministic Sub-Millisecond Execution:**
  Without garbage collection jitter, belief propagation and action selection execute within a strictly bounded time budget ($< 50\,\mu\text{s}$ on modern industrial microcontrollers), fitting into $1\,\text{kHz}$ or $10\,\text{kHz}$ control loops.
* **Bare-Metal & RTOS Portability:**
  Compiles cleanly with any standard C compiler (`gcc`, `clang`, `arm-none-eabi-gcc`). Runs directly on bare-metal microcontrollers (ARM Cortex-M4/M7, STM32, ESP32, RISC-V) as well as real-time operating systems (FreeRTOS, Zephyr, VxWorks) and industrial PLCs via CANopen, EtherCAT, or SPI/PWM drivers.
* **Safety & Industrial Certification (MISRA-C Compliance):**
  Static allocation and pointer-safe C99 architectures allow formal verification and alignment with functional safety standards (ISO 26262 for automotive, IEC 61508 for industrial robotics).

---

### FAQ 9: The Mathematical Formalism Appears Highly Complex — How Does One Develop High-Quality Edge Software Without Hand-Coding Tensors?

#### The Solution: The Conative Studio IDE

To bridge the gap between high-level theoretical neuro-cybernetics and deterministic low-level industrial deployment, Conative Systems S.à r.l. engineered the **Conative Studio IDE** — a specialized graphical engineering environment and compiler suite tailored specifically for Active Conative Inference.

#### 1. Visual Generative Model Specification & Ontology Modeling
* Engineers define discrete state spaces $\mathcal{S}$, sensory observation spaces $\mathcal{O}$, and action repertoires $\mathcal{A}$ via visual ontologies and graph-based transition diagrams.
* Sensor precision ($\mathbf{A}$) and causal dynamics ($\mathbf{B}$) are configured through visual matrix editors with automatic stochastic normalization.
* Homeostatic preference attractors ($\mathbf{C}$), empirical experience-learning priors ($\beta$), and structural vitality functions ($\Phi(s)$) are mapped graphically.

#### 2. Formal Verification & Mathematical Integrity Checks
* **Ergodicity & Reachability Analysis:** Verifies that no absorbing dead-end states trap the agent.
* **Conservation & Normalization Checks:** Formally guarantees numerical stability and absence of divide-by-zero risks in logarithmic free energy evaluations.
* **Veto Circuit Validation:** Mathematically verifies that the Conatus-Veto triggers reliably under all boundary conditions where $\Phi(s) < \Phi_{\text{crit}}$.

#### 3. Automated Zero-Allocation C99 Code Generation
* Compiles verified models into optimized, freestanding C99 (`aci_core.h`, `aci_core.c`) with zero external dependencies.
* Employs compile-time static memory layouts conforming directly to MISRA-C and ISO 26262.

#### 4. Hardware-in-the-Loop (HIL) Simulation & Live Telemetry
* Enables engineers to simulate and stress-test the ACI model against physical digital twins prior to burning firmware onto silicon.
* Provides live streaming introspection: engineers observe hidden beliefs $P(s)$, Expected Free Energy landscapes $G^*(a)$, and vitality dynamics $\Phi(t)$ side-by-side with real motor telemetry.

---

### FAQ 10: Can the Classic 'Dark Room Problem' Occur in This Inverted Pendulum Setup Without Conatus?

#### 1. What is the 'Dark Room' of an Inverted Pendulum?
In theoretical cognitive science, the **Dark Room Problem** is a classic critique of the Free Energy Principle:  
*“If an agent merely minimizes surprise (Free Energy), why shouldn’t it simply seek out a dark, empty room where nothing happens, shut its eyes, and remain completely still to experience zero sensory surprise?”*

In the context of an inverted pendulum, the equivalent "Dark Room" is **letting the rod fall flat onto the ground table and leaving the motor turned off**:
* Once the rod is resting flat against the ground, it never moves.
* Sensor readings become completely static, predictable, and devoid of surprises ($F \approx 0$).
* A naive, unconstrained algorithm that merely seeks sensory predictability would naturally settle into this stationary dead state.

#### 2. Why Pure Surprise Minimization (Without Conatus) Leads to Inaction
If an agent only has an ungrounded mathematical prior without a physical self-preservation imperative:
* Balancing upright is dynamic, noisy, and requires constant effort.
* Resting horizontally on the floor is stable and predictable.
* Without an active conative drive, the agent has no intrinsic motivation to spend electrical energy fighting gravity.

#### 3. How Conatus and Integrated Vitality $\Phi(s)$ Solve the Dark Room Problem
Active Conative Inference completely eradicates the Dark Room Problem through two interlocking principles:
1. **Phenotypic Preference ($\mathbf{C}$):**  
   The agent does not seek arbitrary predictability; it seeks **phenotype-congruent predictability**. Resting horizontally on the floor is assigned a catastrophic surprise penalty ($\mathbf{C} = -8.0$).
2. **Vitality Maximization ($\Phi$):**  
   Lying dead on the floor corresponds to $\Phi \approx 0.0\text{ nats}$ (complete loss of functional organization and informational integration).
   Because the action selection objective $G^*$ actively rewards higher vitality ($-\lambda_\Phi \Phi \sqrt{H}$), the agent is biologically compelled to keep the rod upright.
3. **The Conatus Imperative (Spinoza):**  
   An autopoietic agent's very existence is defined by its continual struggle against thermodynamic entropy. Standing upright against gravity is the ultimate mechanical expression of this living struggle.
"""
    return md

def get_markdown_de():
    md = r"""<img src="conative_systems_logo.svg" align="right" width="125" style="float: right; margin-left: 20px; margin-bottom: 15px;" alt="Conative Systems Logo" />

# Active Conative Inference (ACI): Das Planare Invertierte Pendel
### Ein didaktischer Leitfaden zu Wahrnehmung, Handlung, Vitalität und Online-Lernen in einem planaren 2D-System

**Autor:** Thomas Riebl  
**Organisation:** Conative Systems S.à r.l.  
**Theoretische Grundlagen:** Active Conative Inference (ACI), Free Energy Principle (FEP), Integrated Information Theory ($\Phi$ / IIT 4.0, Giulio Tononi), Spinozas Conatus, Patent 01 & 11  
**Zielarchitektur:** Freistehendes ANSI C99 für Edge-Mikrocontroller (Zero Dynamic Heap)

---

## 1. Physikalische Anschauung: Das Besenstiel-Paradoxon & Planare Architektur

Bevor wir mathematische Formalismen oder Wahrscheinlichkeitsmatrizen definieren, verankern wir das System in der alltäglichen physikalischen Anschauung.

Stellen wir uns vor, einen langen Besenstiel senkrecht auf der offenen Handfläche zu balancieren:
* Wenn die Spitze des Stiels nach **rechts** kippt: Was muss die Hand tun?
* Die menschliche Intuition verleitet oft zu dem fatalen Reflex, die Hand nach links wegzuziehen. Die klassische Newton-Euler-Mechanik verlangt jedoch das genaue Gegenteil: Die Hand muss blitzschnell nach **RECHTS** schnellen, um den Drehpunkt direkt unter den fallenden Schwerpunkt (Center of Mass, CoM) zu schieben.
* Das resultierende Trägheitsmoment richtet den Stab wieder in die senkrechte Ruhelage ($0^\circ$) auf.

In diesem planaren 2D-System ist die Bewegung streng auf eine einzige vertikale Ebene beschränkt: Der Translationswagen fährt entlang der horizontalen $x$-Achse, und das Pendel kippt ausschließlich nach **Links** ($l$) oder **Rechts** ($r$). Vorne/Hinten-Freiheitsgrade sind mechanisch gesperrt.

---

### 1.1 Physikalisches Kinematik-Diagramm (Stufe 1: Das intuitive Cart-Pole)

Die folgende Vektorgrafik veranschaulicht den physikalischen Grundaufbau vor der Einführung diskreter Wahrscheinlichkeitsfächer oder Matrizen:

![1. Physikalisches System: Das Planare Invertierte Pendel](inverted_pendulum_step1_physics.svg)

#### Visuelle Elemente der physikalischen Bühne:
1. **Der mobile Translationswagen (Masse $M$):** Fährt streng linear entlang der horizontalen Schiene (Links ↔ Rechts). Keine Vorne/Hinten-Bewegungen.
2. **Der starre Balancestab (Länge $L$, Masse $m$):** Gelagert am reibungsarmen Drehpunkt $(x, 0)$ des Wagens, frei kippend um den Winkel $\theta$.
3. **Vertikale Soll-Lage ($\theta = 0^\circ$, grün gestrichelte Linie):** Die instabile Gleichgewichtslage, in welcher der Schwerpunkt exakt senkrecht über dem Drehpunkt steht.
4. **Das Besenstiel-Paradoxon:** Kippt der Stab nach rechts ($+\theta$), muss der Wagen blitzschnell nach **RECHTS** beschleunigen, um den Drehpunkt unter die fallende Masse zu schieben.

---

## 2. Der Geist des Reglers: Bayes' Theorem & Grundlegende Wahrscheinlichkeiten

Nachdem die Mechanik des Pendels greifbar vor Augen steht, wenden wir uns der Steuerung zu: **Wie nimmt der Agent wahr, was in der realen Welt geschieht?**

In klassischen Regelungstheorien wird oft angenommen, dass der exakte Winkel $\theta$ verzögerungsfrei und perfekt messbar sei. In der Realität sind Sensoren verrauscht, Encoder haben Quantisierungsrauschen und Luftzüge stören das System. Der Agent hat niemals direkten, allwissenden Zugriff auf den verborgenen Zustand der Außenwelt; er muss ihn kontinuierlich durch seine sensorische Grenze (das **Markov-Blanket**) hindurch erschließen.

### Grundlegende Notation: $s, o, a, p, P, q$

* **$s$ (Verborgener Zustand / Hidden State):** Der wahre, unberührbare physikalische Zustand der Welt (z. B. der tatsächliche Kippwinkel $\theta \in \mathcal{S}$).
* **$o$ (Beobachtung / Observation):** Der verrauschte Messwert, den die Sensoren am Markov-Blanket registrieren ($o \in \mathcal{O}$).
* **$a$ (Handlung / Action):** Die physikalische Intervention oder der Steuerbefehl an die Motoren (z. B. Wagenbeschleunigung $a \in \mathcal{A}$).
* **$p(\cdot)$ (Wahrscheinlichkeitsverteilung):** Die mathematische Funktion oder der Verteilungsvektor über den gesamten Zustands- oder Beobachtungsraum (z. B. Prior-Verteilung $p(s)$, Likelihood-Verteilung $p(o \mid s)$, Dynamiktensor $p(s' \mid s, a)$).
* **$P(\cdot)$ (Konkrete Wahrscheinlichkeit / Skalar):** Der exakte numerische Wert für die Eintreffwahrscheinlichkeit eines bestimmten Einzelergebnisses, strikt beschränkt auf das Einheitsintervall ($P \in [0, 1]$). Beispielsweise $P(s = 0) = 0{,}92$ oder $P(\text{Regen}) = 0{,}20$.
* **$q(s)$ (Recognition Density / Interner Glaube):** Die interne Überzeugungsverteilung des Agenten über die Weltzustände $s$, die kontinuierlich optimiert wird, um die Freie Energie $F$ zu minimieren.
* **Der Bedingungsstrich ($\mid$):** Gelesen als **„gegeben“**. Beispielsweise liest sich $p(s \mid o)$ als: *„Die Wahrscheinlichkeitsverteilung über Zustände $s$, **gegeben** die Beobachtung $o$“*.

---

### Bayes' Theorem in der Wahrnehmung

Das Theorem von Bayes liefert das mathematische Gesetz, wie eine interne Wahrscheinlichkeitsverteilung unter Einbeziehung neuer sensorischer Evidenz optimal aktualisiert wird:

$$p(s \mid o) = \frac{p(o \mid s) \cdot p(s)}{p(o)} = \frac{p(o \mid s) \cdot p(s)}{\sum_{s'} p(o \mid s') \cdot p(s')}$$

---

#### Anschauliches Alltagsbeispiel: Das Regen-Paradoxon ($s = \text{Regen}$, $o = \text{Straße nass}$)

Um das Zusammenspiel dieser probabilistischen Terme und die unverzichtbare Rolle des Nenners $P(o)$ vorab intuitiv zu begreifen, hilft ein einfaches Alltagsszenario:

* **Verborgener Weltzustand $s$ (Das Wetter draußen):**
  * $s_1 = \text{Regen}$ (Vorab-Glaube / Prior: $P(\text{Regen}) = 0{,}20$ bzw. $20\,\%$)
  * $s_2 = \text{Ohne Regen}$ (Vorab-Glaube / Prior: $P(\text{ohne Regen}) = 0{,}80$ bzw. $80\,\%$)
* **Sensorische Beobachtung $o$ (Blick aus dem Fenster):**
  * $o = \text{Die Straße ist nass}$

**Warum kann die Straße nass sein? (Zwei konkurrierende Kausalpfade):**
1. **Pfad 1 (Echter Regen):** Wenn es regnet, ist die Straße fast garantiert nass: $P(\text{nass} \mid \text{Regen}) = 0{,}99$ ($99\,\%$).
2. **Pfad 2 (Sensor-Mehrdeutigkeit / Falscher Alarm):** Es herrscht kein Regen, aber ein Straßenreinigungsfahrzeug fuhr vorbei oder der Rasensprenger des Nachbarn lief: $P(\text{nass} \mid \text{ohne Regen}) = 0{,}05$ ($5\,\%$).

**Berechnung der marginalen Evidenz $P(o)$ (Gesamtwahrscheinlichkeit einer nassen Straße):**

$$\begin{aligned}
P(\text{nass}) &= \underbrace{P(\text{nass} \mid \text{Regen}) \cdot P(\text{Regen})}_{\text{Nass durch Regen } (0{,}99 \cdot 0{,}20 = 0{,}198)} + \underbrace{P(\text{nass} \mid \text{ohne Regen}) \cdot P(\text{ohne Regen})}_{\text{Nass durch Rasensprenger } (0{,}05 \cdot 0{,}80 = 0{,}040)} \\
&= 0{,}198 + 0{,}040 = \mathbf{0{,}238} \; (23{,}8\,\%)
\end{aligned}$$

**Anwendung des Bayes-Theorems (Regnet es wirklich da draußen?):**  
Sobald du aus dem Fenster blickst und siehst, dass die Straße nass ist ($o$), aktualisiert sich dein Glaube:

$$P(\text{Regen} \mid \text{nass}) = \frac{P(\text{nass} \mid \text{Regen}) \cdot P(\text{Regen})}{P(\text{nass})} = \frac{0{,}198}{0{,}238} \approx \mathbf{83{,}2\,\%}$$

* Der Nenner $P(o) = 0{,}238$ normiert das Ergebnis.
* Die Beobachtung der nassen Straße lässt die Regenwahrscheinlichkeit von zuvor $20\,\%$ auf $83{,}2\,\%$ steigen – aber eben nicht auf $100\,\%$, weil Bayes den alternativen Kausalpfad (Rasensprenger) mathematisch exakt mit einrechnet!
* In Theons Invertiertem Pendel erfüllt $P(o)$ exakt dieselbe mathematische Funktion: Es gewichtet Vorab-Erwartungen dynamisch gegen verrauschte Sensor-Encoder.

---

## 3. Abbildung der physikalischen Welt auf Active Inference: Vier intuitive Objekte

Durch die Beschränkung auf die Ebene vereinfacht sich unser generatives Modell auf exakt **5 Zustände** und **2 Aktionen**:

1. **Wo müssen wir sein? $\to \mathbf{C}$ (Phänotypische Präferenz):**  
   Das autopoietische Verlangen des Systems. Die aufrechte Ruhelage ($s_0$) bedeutet minimale Überraschung ($C_0 = 0.0$). Leichte Neigungen tragen kleine Strafen ($C = -1.5$). Katastrophales Kippen bedeutet existenzielle Bedrohung ($C = -8.0$).
2. **Wo glauben wir zu starten? $\to \mathbf{D}$ (Prior-Glaube):**  
   Die Ausgangshypothese vor der ersten Messung ($92\%$ Gewissheit für aufrechte Balance bei $t = 0$).
3. **Wie präzise sehen wir den Stab? $\to \mathbf{A}$ (Likelihood-Matrix):**  
   Eine transparente $5 \times 5$-Matrix für die Sensorzuverlässigkeit ($92\%$ Diagonalschärfe, $4\%$ Nachbarstreuung).
4. **Was bewirkt die Wagenbewegung? $\to \mathbf{B}(a)$ (Kausale Übergangstensoren):**  
   Zwei intuitive $5 \times 5$-Matrizen ($\mathbf{B}(l)$ und $\mathbf{B}(r)$), welche die Newton-Euler-Physik kodieren: Bei Schräglage rechts ($r_1$) stellt ein Rechtsruck ($a = r$) die Ruhelage ($s_0$) mit $88\%$ Wahrscheinlichkeit wieder her.

---

### Die vier Kernkomponenten von Bayes' Theorem (Formale Matrizen-Zuordnung)

Mit den vier intuitiven Objekten ($\mathbf{C}, \mathbf{D}, \mathbf{A}, \mathbf{B}$) und dem Regen-Paradoxon lässt sich nun formal beschreiben, wie Bayes' Theorem im Regler rechnet:

1. **Prior-Verteilung $p(s)$ (A-priori-Erwartung vor der Messung $\to \mathbf{D}$):**  
   Die Wahrscheinlichkeitsverteilung über alle Zustände vor der Messung: $\mathbf{D} = p(s_0)$. Vorhersage über den Übergangstensor:
   $$s_{\text{pred}} = \mathbf{B}(a_{t-1}) \cdot s_{t-1}$$
   *(Im Regen-Beispiel: Vorab-Wahrscheinlichkeit $P(\text{Regen}) = 20\,\%$.)*
2. **Likelihood-Verteilung $p(o \mid s)$ (Matrix $\mathbf{A}$ — Sensorpräzision):**  
   Die generative Abbildung: *„Wenn der Stab tatsächlich im Zustand $s$ stünde: Wie wahrscheinlich ist es dann, dass unser Sensor die Beobachtung $o$ meldet?“*  
   $$\mathbf{A} = p(o \mid s)$$
   *(Im Regen-Beispiel: $P(\text{nass} \mid \text{Regen}) = 99\,\%$ vs. $P(\text{nass} \mid \text{ohne Regen}) = 5\,\%$.)*
3. **Posterior-Verteilung $p(s \mid o)$ (A-posteriori-Zustand $\to$ Interne Dichte $q(s)$):**  
   Die aktualisierte, optimale Wahrscheinlichkeitsverteilung über den Weltzustand $s$ **nach** Verarbeitung der Beobachtung $o$. Wahrnehmung in Active Inference ist die Minimierung der Diskrepanz (Variational Free Energy $F$) zwischen diesem Posterior $p(s \mid o)$ und der internen Dichte $q(s)$.  
   *(Im Regen-Beispiel: $P(\text{Regen} \mid \text{nass}) = 83{,}2\,\%$.)*
4. **Marginale Evidenz-Verteilung $p(o)$ (Normierung & Phänotypische Präferenz $\to \mathbf{C}$):**  
   Die Gesamtwahrscheinlichkeitsverteilung über alle denkbaren Beobachtungen. Ihr Logarithmus $\ln p(o)$ bildet den phänotypischen Präferenzvektor $\mathbf{C}$.  
   *(Im Regen-Beispiel: $P(\text{nass}) = 23{,}8\,\%$.)*

---

## 4. Formale mathematische 5-Zustände-Spezifikation & Zustands-Kompass

### 1.2 Architektur des Zustandsraums (Stufe 2: Diskretisierung & Conatus-Grenze)

Zur Konstruktion eines berechenbaren Modells diskretisieren wir den kontinuierlichen Winkel $\theta$ in **5 conative Zustände** ($\mathcal{S}$) und definieren die **Conatus-Überlebensgrenze**:

![2. Diskreter Zustandsraum & Conatus-Überlebensbarriere](inverted_pendulum_step2_states.svg)

#### Die 5 diskreten Zustände & physikalischen Schwellenwerte:
* **Zustand $s_0 = 0$ (Grün):** Aufrechte Gleichgewichtslage ($|\theta| \le 3^\circ$). Homeostatischer Attraktor ($C_0 = 0.0$, $\Phi = 1.00$).
* **Zustände $s_1 = l_1, s_3 = r_1$ (Bernstein):** Leichte Neigung links oder rechts ($3^\circ < |\theta| \le 15^\circ$). Mühelos stabilisierbar ($C = -1.5$, $\Phi = 0.70$).
* **Zustände $s_2 = l_2, s_4 = r_2$ (Rot):** Kritisches Kippen links oder rechts ($15^\circ < |\theta| < 35^\circ$). Starkes Gegensteuern erforderlich ($C = -8.0$, $\Phi = 0.15$).
* **Conatus-VETO-Grenze (Rot gestrichelt bei $\pm 35^\circ$):** Point of No Return. Exkursionen über $\pm 35^\circ$ können vom Motor nicht mehr abgefangen werden; jede dahin führende Politik löst ein sofortiges Conatus-Veto aus ($G^* \to +\infty$).

### Diskreter Zustandsraum ($|\mathcal{S}| = 5$) und Aktionsraum ($|\mathcal{A}| = 2$)

* **Zustände:** $\mathcal{S} = \{0, l_1, l_2, r_1, r_2\}$
  * $s_0 = 0$: Aufrechte Soll-Lage (Balanciert / Attraktor)
  * $s_1 = l_1$: Leichte Linksauslenkung ($\theta \approx -12^\circ$)
  * $s_2 = l_2$: Starker Sturz nach Links ($\theta \approx -26^\circ$)
  * $s_3 = r_1$: Leichte Rechtsauslenkung ($\theta \approx +12^\circ$)
  * $s_4 = r_2$: Starker Sturz nach Rechts ($\theta \approx +26^\circ$)
* **Aktionen:** $\mathcal{A} = \{l, r\}$
  * $a = 0$ ($l$): Wagen beschleunigt nach LINKS ⬅
  * $a = 1$ ($r$): Wagen beschleunigt nach RECHTS ➔

---

### Prior-Vektor $\mathbf{D}$ (Startzustand & Prädiktive Kausalkette)

Wie bildet der Agent eine A-priori-Vorhersage $s_{\text{pred}}$ über den verborgenen Weltzustand, bevor er die nächste Sensormessung verarbeitet?

1. **Im laufenden Betrieb ($t \ge 1$):**  
   Sobald das System in Bewegung ist, projiziert der Agent seine Erwartung über den Kausal-Tensor $\mathbf{B}$ und die zuletzt ausgeführte Aktion $a_{t-1}$ voraus:
   $$s_{\text{pred}}(t) = \mathbf{B}(a_{t-1}) \cdot s_{t-1}$$
2. **Beim Systemstart ($t = 0$):**  
   Im allerersten Zeitschritt beim Einschalten existieren noch keine vorherige Aktion $a_{-1}$ und kein Vorzustand $s_{-1}$.  
   **Der Vektor $\mathbf{D}$ dient als zwingender Startwert für diese prädiktive Kausalkette:**
   $$s_{\text{pred}}(t=0) = \mathbf{D} = p(s_0) = \begin{pmatrix} 0.92 \\ 0.04 \\ 0.00 \\ 0.04 \\ 0.00 \end{pmatrix} \begin{matrix} (0: \text{Aufrecht balanciert}) \\ (l_1: \text{Leichte Neigung links}) \\ (l_2: \text{Starker Sturz links}) \\ (r_1: \text{Leichte Neigung rechts}) \\ (r_2: \text{Starker Sturz rechts}) \end{matrix}$$

* $P(s_0 = 0) = 0.92$: Das System startet mit hoher A-priori-Gewissheit, dass es aufrecht balanciert steht.
* $P(s_0 = l_1) = P(s_0 = r_1) = 0.04$: Geringe Restunsicherheit ($4\%$) verhindert numerische Nullfallen und sorgt für sensorische Flexibilität.
* $P(s_0 = l_2) = P(s_0 = r_2) = 0.00$: Null Wahrscheinlichkeit für einen sofortigen Absturz beim Einschalten.
* **Strikte Wahrscheinlichkeitserhaltung:** $\sum_{i=0}^4 D_i = 0.92 + 0.04 + 0.00 + 0.04 + 0.00 = \mathbf{1.00}$ ($\mathbf{100\,\%}$).

---

### Präferenzvektor $\mathbf{C}$ & Zielverteilung $p(o)$ (Die 3-Schritte-Herleitung)

In Active Inference werden Handlungsziele nicht als willkürliche Belohnungen formuliert, sondern als **phänotypische Erwartungen**: Der Agent handelt aktiv so, dass er genau das beobachtet, was er zu sehen erwartet, um stabil im Gleichgewicht zu bleiben.

#### Schritt 1: Definition der Beobachtungswahrscheinlichkeiten $p(o)$
Wir als Entwickler definieren vorab, welche Winkel das inverse Pendel zu beobachten erwartet:
* **$P(o_0 : \text{Aufrecht balanciert}, |\theta| \le 3^\circ) \approx 69{,}1\,\%$:** Der gewünschte Idealzustand.
* **$P(o_{l1}, o_{r1} : \text{Leichte Neigung}, 3^\circ < |\theta| \le 15^\circ) \approx 15{,}4\,\%$ je Seite:** Alltägliche, noch tolerierbare Schwankungen.
* **$P(o_{l2}, o_{r2} : \text{Katastrophaler Sturz}, |\theta| > 15^\circ) \approx 0{,}023\,\%$ je Seite:** Gefahrenzonen, die das System praktisch niemals zu sehen erwartet.

Als normierter Wahrscheinlichkeitsvektor $p(o) \in [0, 1]^5$:
$$p(o) = \begin{pmatrix} 
0{,}6911 \\ 
0{,}1542 \\ 
0{,}00023 \\ 
0{,}1542 \\ 
0{,}00023 
\end{pmatrix} 
\begin{matrix} 
(o_0: \text{Aufrecht balanciert} \approx \mathbf{69{,}1\,\%}) \\ 
(o_{l1}: \text{Leichte Neigung links} \approx \mathbf{15{,}4\,\%}) \\ 
(o_{l2}: \text{Katastrophaler Sturz links} \approx \mathbf{0{,}02\,\%}) \\ 
(o_{r1}: \text{Leichte Neigung rechts} \approx \mathbf{15{,}4\,\%}) \\ 
(o_{r2}: \text{Katastrophaler Sturz rechts} \approx \mathbf{0{,}02\,\%}) 
\end{matrix}$$

* **Strikte Wahrscheinlichkeitserhaltung:** Alle Werte sind positiv und summieren sich exakt zu $1{,}0$ ($100\,\%$):  
  $\sum_{i=1}^5 P(o_i) = 0{,}6911 + 0{,}1542 + 0{,}00023 + 0{,}1542 + 0{,}00023 = \mathbf{1{,}0000}$.

#### Schritt 2: Ableitung des Präferenzvektors $\mathbf{C} = \ln p(o)$
Active-Inference-Algorithmen berechnen die erwartete freie Energie im logarithmischen Informationsraum (Nats). Das Ziehen des natürlichen Logarithmus liefert:
* $\ln(0{,}6911) = \mathbf{-0{,}369}$
* $\ln(0{,}1542) = \mathbf{-1{,}869} = -0{,}369 - 1{,}5$
* $\ln(0{,}00023) = \mathbf{-8{,}369} = -0{,}369 - 8{,}0$

Zieht man den Basis-Offset $-0{,}369$ ab (Nullpunkt-Eichung), entsteht der saubere **Präferenzvektor $\mathbf{C}$**:
$$\mathbf{C} = \ln p(o) - \max(\ln p(o)) = \begin{pmatrix} 0{,}0 \\ -1{,}5 \\ -8{,}0 \\ -1{,}5 \\ -8{,}0 \end{pmatrix} \begin{matrix} (o_0: \text{Aufrecht}) \\ (o_{l1}: \text{Leicht links}) \\ (o_{l2}: \text{Sturz links}) \\ (o_{r1}: \text{Leicht rechts}) \\ (o_{r2}: \text{Sturz rechts}) \end{matrix}$$

* $\mathbf{C}_0 = 0{,}0$: Maximale Präferenz (minimale Freie Energie / Null Überraschung in stabiler Balance).
* $\mathbf{C}_{\text{Stufe 1}} = -1{,}5$: Leichte Aversion gegen Schräglagen (erzeugt korrigierenden Regelantrieb).
* $\mathbf{C}_{\text{Stufe 2}} = -8{,}0$: Katastrophal negativer Wert (abstoßendes Strafpotenzial gegen Kippen).

#### Schritt 3: Die Softmax-Brücke im Code ($p(o) = \operatorname{softmax}(\mathbf{C})$)
In der Implementierung konfigurieren Entwickler direkt den Vektor $\mathbf{C}$. Der **Softmax-Operator** (Boltzmann-/Gibbs-Verteilung) überführt diese Log-Präferenzen wieder exakt in die ursprüngliche Wahrscheinlichkeitsverteilung:
$$P(o_i) = \sigma(\mathbf{C})_i = \frac{e^{C_i}}{\sum_{j=1}^5 e^{C_j}} \implies p(o) = \operatorname{softmax}(\mathbf{C})$$
Mit der Zustandssumme $Z = \sum_{j=1}^5 e^{C_j} = e^{0{,}0} + 2 e^{-1{,}5} + 2 e^{-8{,}0} \approx 1{,}4469$ stellt $\operatorname{softmax}(\mathbf{C})$ exakt die Zielverteilung $69{,}1\,\%, 15{,}4\,\%, 0{,}02\,\%$ wieder her!

#### 💡 Zusammenfassung:
* **Der Wahrscheinlichkeits-Raum ($\mathbf{A}, \mathbf{B}, \mathbf{D}, p(o)$):** Alle Werte sind echte Wahrscheinlichkeiten ($P \in [0, 1]$), strikt positiv, Summe $= 1{,}0$.
* **Der Log-Präferenz-Raum ($\mathbf{C}$ in Nats):** Arbeitsraum für Freie-Energie-Berechnungen ($\mathbf{C} = \ln p(o)$), in dem gefährliche Zustände große negative Strafwerte besitzen.
* **Die Softmax-Brücke:** Verbindet beide Welten eineindeutig: $p(o) = \operatorname{softmax}(\mathbf{C}) \iff \mathbf{C} \cong \ln p(o)$.

---

### Beobachtungsmatrix $\mathbf{A}$ (Sensorpräzision)

Die Matrix $\mathbf{A} \in \mathbb{R}^{5 \times 5}$ bildet den Weltzustand $s$ auf die Beobachtungen $o$ ab: $p(o \mid s)$.

Bei Sensorschärfe $\gamma_s = 0.92$ und Nachbarstreuung $\varepsilon = 0.04$:

$$\mathbf{A} = p(o \mid s) = \begin{pmatrix}
0.92 & 0.04 & 0.00 & 0.04 & 0.00 \\
0.04 & 0.92 & 0.04 & 0.00 & 0.00 \\
0.00 & 0.04 & 0.96 & 0.00 & 0.00 \\
0.04 & 0.00 & 0.00 & 0.92 & 0.04 \\
0.00 & 0.00 & 0.00 & 0.04 & 0.96
\end{pmatrix}$$

* Die Hauptdiagonale dominiert mit über $92\%$ Zuverlässigkeit.
* Sensorungenauigkeiten treten nur in direkt benachbarte Neigungsstufen auf ($4\%$).

---

### Übergangstensoren $\mathbf{B}(a)$ (Kausaldynamik)

Für die beiden Aktionen $a \in \{l, r\}$ beschreibt $\mathbf{B}(a) \in \mathbb{R}^{5 \times 5}$ die Übergänge $p(s_{t+1} \mid s_t, a)$.

#### Aktion $a = r$ (Wagen beschleunigt nach rechts)

$$\mathbf{B}(r) = p(s' \mid s, a = r) = \begin{pmatrix}
0.15 & 0.00 & 0.00 & 0.88 & 0.00 \\
0.85 & 0.10 & 0.00 & 0.02 & 0.00 \\
0.00 & 0.90 & 1.00 & 0.00 & 0.00 \\
0.00 & 0.00 & 0.00 & 0.10 & 0.85 \\
0.00 & 0.00 & 0.00 & 0.00 & 0.15
\end{pmatrix}$$

* Aus $s = r_1$ (leichte Neigung rechts): Rechtsruck $\to$ stellt Ruhelage $0$ mit $P = 0.88$ wieder her.
* Aus $s = r_2$ (starker Sturz rechts): Rettet das System von $r_2$ zurück nach $r_1$ mit $P = 0.85$.
* Aus $s = 0$ (bereits balanciert): Überflüssiger Rechtsruck kippt das Pendel nach links ($l_1$, $P = 0.85$).
* Aus $s = l_1$ (bereits nach links gekippt): Rechtsruck beschleunigt den Absturz nach links ($l_2$, $P = 0.90$).

#### Aktion $a = l$ (Wagen beschleunigt nach links – symmetrisch invertiert)

$$\mathbf{B}(l) = p(s' \mid s, a = l) = \begin{pmatrix}
0.15 & 0.88 & 0.00 & 0.00 & 0.00 \\
0.00 & 0.10 & 0.85 & 0.00 & 0.00 \\
0.00 & 0.00 & 0.15 & 0.00 & 0.00 \\
0.85 & 0.02 & 0.00 & 0.10 & 0.00 \\
0.00 & 0.00 & 0.00 & 0.90 & 1.00
\end{pmatrix}$$

---

### 5. Die conative ACI-Differenzierung (Thomas Riebl)

Klassisches Active Inference ($H = 1$) handelt kurzsichtig und optimiert lediglich den nächsten Zeitschritt.

Unter Active Conative Inference gilt:
* **Temporale Tiefe $H \ge 2$:** Der Agent antizipiert Überschwingen. Zu starkes Gegensteuern bei $r_1$ erzeugt bei $t+2$ einen unkontrollierbaren Gegenschwung nach $l_2$.
* **Systemische Vitalitätsüberwachung $\Phi(s)$ (Integrated Information Theory / IIT 4.0, Giulio Tononi):**
  * $\Phi(0) = 1.00\text{ nats}$ (Maximale systemische Kohärenz und autopoietische Gesundheit)
  * $\Phi(l_1, r_1) = 0.70\text{ nats}$ (Leichte Auslenkung)
  * $\Phi(l_2, r_2) = 0.15\text{ nats}$ (Kritische Gefahrenzone)
* **Conatus-VETO:** Fällt die prognostizierte Vitalität unter $\Phi < 0.25\text{ nats}$, sperrt das Conatus-Veto den schädlichen Steuerbefehl sofort und erzwingt stabilisierende Dämpfung.

---

## 5. Handlungsplanung ($G^*$-Minimierung) & Der Gesamte Regelkreis

### 1.3 Der vollständige geschlossene Regelkreis (Stufe 3: Kräfte, Handlungen & Tensoren)

Aus der Synthese von Cart-Pole-Mechanik (Stufe 1) und diskretem Zustands-Kompass (Stufe 2) entsteht die vollständige geschlossene Architektur:

![3. Vollständiges Planares ACI-System: Kinematik, Kräfte & 5x5-Tensoren](inverted_pendulum_step3_complete.svg)

#### Dynamische Elemente des Regelkreises:
* **Kippmoment $\tau_{\text{grav}} = m g L \sin\theta$:** Bei Auslenkung zieht die Schwerkraft $\vec{F}_g$ den Schwerpunkt abwärts.
* **Wiederherstellende Beschleunigung $\vec{a}_{\text{base}}$:** Der Agent setzt die Aktion $a = r$ (Rechtsbeschleunigung), um den Drehpunkt unter die Masse zu fahren.
* **Erwartete Freie Energie ($G^*$):** Die Aktionsauswahl minimiert künftige Überraschung und schützt die systemische Vitalität $\Phi$ über den Zeithorizont $H \ge 2$:

$$G^*(a) = G_{\text{pragmatisch}}(a) - \lambda_\Phi \cdot \Phi(a, H) \cdot \sqrt{H} + \Omega_{\text{conatus\_veto}}$$

* **Pragmatischer Term:** $-\mathbb{E}_{q(s_{t+1})}[\mathbf{C}]$ (Abstand zum phänotypischen Attraktor $s_0$).
* **Conativer Vitalitätsterm:** Prognostizierte Integrität $\Phi$, gewichtet mit Zeittiefe $\sqrt{H}$.
* **Conatus-Veto:** Sinkt die Vitalität unter $\Phi < 0.25\text{ nats}$, springt $G^* \to +\infty$ und blockiert gefährliche Steuerimpulse.

---

## 6. Online-Lernen — Erfahrungszähler (Kausales Gedächtnis)

### Wie der Agent Ursache und Wirkung lernt: Das Strichlisten-Prinzip

Traditionelle neuronale Netze und Reinforcement Learning benötigen Millionen Trainingsschritte, GPU-Cluster und leiden unter katastrophalem Vergessen („Catastrophic Forgetting“).

In Active Inference lernt das System physikalische Kausalgesetze so transparent wie das Führen einer **Erfahrungs-Strichliste**:

1. **Das Erfahrungsfach $\beta$:**  
   Für jede Kombination aus Ausgangszustand $s$, Aktion $a$ und Folgezustand $s'$ besitzt der Agent einen einfachen Zähler $\beta_{s', s, a}$.
2. **Echtzeit-Inkrementierung:**  
   Befindet sich das Pendel in Zustand $s$ (z. B. $r_1$), setzt der Wagen Aktion $a = r$ und landet das Pendel in $s'$ (Ruhelage $s_0$), erhält dieses Fach sofort einen Zählerpunkt:
   $$\beta_{s', s, a} \leftarrow \beta_{s', s, a} + 1$$
3. **Von Zählern zu Wahrscheinlichkeiten:**  
   Zur Vorhersage künftiger Übergänge $\mathbf{B}(a)$ berechnet der Agent schlicht den relativen Anteil:
   $$\mathbf{B}_{s', s, a} = p(s' \mid s, a) = \frac{\text{Beobachtete Häufigkeit von }(s \xrightarrow{a} s')}{\text{Gesamte Erfahrungen in Zustand } s \text{ mit Aktion } a} = \frac{\beta_{s', s, a}}{\sum_{s''} \beta_{s'', s, a}}$$

#### Industrielle Vorteile für Edge- und Mikrocontroller-Steuerungen:
* **Sofortiges Lernen in einem Schritt ($O(1)$):** Keine Gradientenabstiegsschleifen oder Backpropagation; sofortige Aktualisierung bei mechanischen Veränderungen.
* **Kein katastrophales Vergessen:** Frühere physikalische Erfahrungen bleiben in ihren Zählfächern sicher konserviert.
* **Deterministisch & C99-bereit:** Reines Hochzählen von Ganz- oder Gleitkommazahlen ohne Speicherallokation (`malloc`).

*(In der mathematischen Statistik wird dieses Zählverfahren als Dirichlet-Verteilung formalisiert – physikalisch ist es schlicht empirische Erfahrungsspeicherung.)*

---

## 7. Grundsatzfragen & Didaktische FAQ

### FAQ 1: Was macht dieses System „intelligent“?
Intelligenz ist in diesem Framework **weder passive statistische Textvorhersage (LLMs) noch blinde Belohnungsjagd (Reinforcement Learning)**.  
Intelligenz ist **aktive Homeostase und vorausschauende Autopoiese unter Rauschen und Störungen**:
* **Inferenz statt Reflex:** Statt wie ein PID-Regler blind auf Messfehler zu reagieren, pflegt der Agent eine interne generative Hypothese. Er filtert Rauschen heraus, rekonstruiert den wahren Zustand $s$ und plant über Zeithorizonte $H \ge 2$ voraus.
* **Autopoietischer Selbsterhalt (Conatus):** Der Regler jagt keinen von Menschen vorgegebenen Punktestand; sein Antrieb entspringt dem fundamentalen Schutz der eigenen Existenz und Systemvitalität ($\Phi$).

---

### FAQ 2: Was lernt der Agent?
Der Agent lernt die **wahren Kausalgesetze seiner Mechanik und Umwelt**:
* Er verfeinert den Dynamiktensor $\mathbf{B}(s' \mid s, a) = p(s' \mid s, a)$: *„Wenn ich im Zustand $s$ bin und Aktion $a$ ausführe: Mit welcher Wahrscheinlichkeit lande ich in $s'$?“*
* Ändert sich die Schienenreibung oder die Stablänge, passt sich das Kausalmodell im Betrieb sofort an.

---

### FAQ 3: Wie lernt der Agent?
Über **exakte Bayes'sche Zähler-Updates (Erfahrungs-Strichlisten)** statt über Gradientenabstiege:
* Der Agent führt Pseudocount-Matrizen $\beta_{s', s, a}$.
* Jede reale Beobachtung verfeinert die Übergangsmatrix $\mathbf{B}$ unmittelbar.
* **Vorteil:** Numerisch exakt, sofort wirksam und ohne Speicherüberlauf.

---

### FAQ 4: Was ist das Weltmodell in diesem Beispiel?
Das **Weltmodell** ist die generative Repräsentation der Umwelt im Agenten:
* **Zustandskompass $\mathcal{S}$:** $\{0, l_1, l_2, r_1, r_2\}$ für die wahre Auslenkung.
* **Sensormodell $\mathbf{A}$:** Abbildung von realem Zustand auf verrauschte Messung ($p(o \mid s)$).
* **Kausaldynamik $\mathbf{B}(a)$:** Übergangstensor für die Wirkung der Motorbeschleunigung ($p(s' \mid s, a)$).

---

### FAQ 5: Was ist das Generative Modell in diesem Beispiel?
Die vollständige Verbundwahrscheinlichkeitsverteilung über Beobachtungen, Zustände, Handlungen und Präferenzen:
$$p(o, s, a) = p(o \mid s) \cdot p(s \mid s_{t-1}, a) \cdot p(s_0) \cdot p_{\text{prior}}(a)$$
ergänzt um den conativen Phänotypvektor $\mathbf{C} = \ln p(o)$ und die systemische Vitalität $\Phi(s)$. Es gestattet das geistige Durchspielen alternativer Zukünfte vor dem Auslösen von Motorströmen.

---

### FAQ 6: Klassischer PID vs. Active Conative Inference (ACI) — Unterschiede, Schwächen und Vorteile

#### 1. Was klassischer PID ist und wie er arbeitet
* **Proportional (P):** Stellkraft proportional zum aktuellen Regelfehler $e(t) = \theta_{\text{soll}} - \theta_{\text{ist}}$.
* **Integral (I):** Summiert vergangene Abweichungen auf $\int e(\tau) d\tau$.
* **Derivative (D):** Dämpft die Änderungsgeschwindigkeit $\frac{de(t)}{dt}$.

#### 2. Schwächen klassischer PID-Regler
* **Kein Kausalmodell:** PID weiß nichts über Ursache und Wirkung; er kann nicht zwei Schritte in die Zukunft blicken.
* **Rauschempfindlichkeit (D-Term-Verstärkung):** Das Differenzieren verstärkt Sensorrauschen extrem und führt zu Motorflattern.
* **Integral-Windup:** Bei starken Störungen läuft der I-Speicher voll und verursacht extremes Überschwingen.
* **Kein Selbsterhalt:** PID steuert selbst dann mit Vollgas weiter, wenn das System mechanisch bricht.

#### 3. Vorteile klassischer PID-Regler
* Minimaler Rechenaufwand (~10 Fließkommaoperationen).
* Bewährt und intuitiv für einfache lineare Arbeitspunkte.

#### 4. Vorteile von Active Conative Inference (ACI)
* **Optimales Bayes-Filtern:** Trennt Sensorrauschen von physikalischer Realität über Matrix $\mathbf{A}$.
* **Vorausschauende Planung ($H \ge 2$):** Verhindert Überschwingen, bevor es entsteht.
* **Autonomer Conatus-Schutz:** Conatus-Veto verhindert Motorschäden und Getriebebrüche.
* **Echtzeit-Adaption:** Passt sich veränderten Reibungswerten im Betrieb ohne manuelles Nachtrimmen an.

---

### FAQ 7: Wie arbeitet das Conatus-Veto am Invertierten Pendel konkret?

#### 1. Das Problem: Peitscheneffekt (Whiplash)
Beim schnellen Aufrichten aus starker Neigung erzeugt die Massenträgheit hohe kinetische Energie. Ein kurzsichtiger Regler ($H = 1$) reißt den Wagen zurück, wodurch der Stab auf die Gegenseite durchschlägt und abstürzt.

#### 2. Die conative Invariante: Vitalitätsabbildung $\Phi(s)$
Nach Spinozas Conatus-Prinzip strebt jedes autopoietische System nach Selbsterhalt. Über IIT 4.0 (Giulio Tononi) wird dies messbar:
* Aufrecht ($s_0$): Maximale Systemvitalität $\Phi = 1.00\text{ nats}$.
* Leichte Neigung ($l_1, r_1$): Stabiler Vitalitätsbereich $\Phi = 0.70\text{ nats}$.
* Gefahrenzone ($l_2, r_2$): Starker Vitalitätsabfall auf $\Phi = 0.15\text{ nats}$.

#### 3. Auslösen des Conatus-Vetos
Das Conatus-Prinzip besagt, dass der Schutz des Systems und der Erhalt der physischen Integrität absoluten Vorrang vor Aufgabenanforderungen haben.
* Vor jedem Steuerimpuls prüft der Agent die prognostizierte Vitalität über $H = 2$:
$$\Phi_{\text{prognose}}(a) < 0.25\text{ nats} \implies G^*(a) \to +\infty$$
* Der zerstörerische Befehl wird verworfen; stattdessen greift eine stabilisierende Notdämpfung.

---

### FAQ 8: Warum kein Python in harter Echtzeit — und wie löst ACI dies auf Edge-Hardware?

#### 1. Python als didaktischer Prototyp vs. natives C99 in Produktion
Dieses Dokument und das begleitende Jupyter-Notebook sind ein didaktischer Simulator für Übersicht und mathematische Klarheit.

In der industriellen Robotik (patentiert durch Conative Systems S.à r.l.):
* **Kein Python im Feld:** Null Python, null PyTorch, keine externen Bibliotheken.
* **Reiner ANSI-C99-Kern:** Der gesamte Inferenz- und Planungskern läuft in freistehendem C99.

#### 2. Die Pfeiler der nativen C99-ACI-Engine
* **Kein dynamischer Heap (`malloc`/`free` verboten):** Alle Tensoren, Vektoren und Arbeitsbereiche liegen fest im statischen Speicher. Keine Fragmentierung, keine Latenzsprünge.
* **Deterministische Ausführung unter $50\,\mu\text{s}$:** Garantiert feste Rechenzeiten, passend für $1\,\text{kHz}$- oder $10\,\text{kHz}$-Regeltakte.
* **Bare-Metal-Portabilität:** Kompiliert auf ARM Cortex-M4/M7, STM32, ESP32, RISC-V sowie Industrie-SPS via CANopen oder EtherCAT.
* **Funktionale Sicherheit (MISRA-C-Konformität):** Vollständig verifizierbar nach ISO 26262 und IEC 61508.

---

### FAQ 9: Wie beherrscht man die Mathematik ohne händisches Coden von Tensoren?

#### Die Lösung: Die Conative Studio IDE
Zur Überbrückung der Hürde zwischen theoretischer Neuro-Kybernetik und deterministischem Embedded-Code entwickelte Conative Systems die **Conative Studio IDE**:
* **Visuelle Modellierung:** Zustandsräume, Beobachtungen und Kausaltensoren werden grafisch definiert.
* **Formale Verifikation:** Automatische Prüfung auf Ergodizität, Normalisierung und zuverlässiges Greifen des Conatus-Vetos vor Code-Generierung.
* **1-Klick-C99-Codegenerierung:** Erzeugt optimierte, freistehende Quelldateien (`aci_core.h`, `aci_core.c`) ohne externe Abhängigkeiten.
* **Hardware-in-the-Loop-Simulation:** Echtzeit-Testlauf gegen digitale Zwillinge vor dem Aufspielen auf die Zielhardware.

---

### FAQ 10: Tritt das „Dark Room Problem“ beim Invertierten Pendel auf?

#### 1. Was ist das „Dark Room Problem“?
In der Kognitionswissenschaft lautet eine klassische Kritik am Free Energy Principle:  
*„Wenn ein System nur sensorische Überraschung minimiert: Warum setzt es sich nicht einfach in einen dunklen, leeren Raum, schließt die Augen und bleibt regungslos stehen?“*

Am Invertierten Pendel entspräche der „Dark Room“ dem **Umkippen auf den Tisch und Abschalten des Motors**:
* Liegt der Stab flach am Boden, bewegt sich nichts mehr.
* Die Messwerte sind absolut vorhersehbar und frei von Überraschungen ($F \approx 0$).
* Ein naiver Algorithmus ohne Conatus würde diesen Zustand anstreben.

#### 2. Wie Conatus und Systemvitalität $\Phi(s)$ das Problem lösen
Active Conative Inference schließt dieses Fehlverhalten kategorisch aus:
1. **Phänotypische Präferenz ($\mathbf{C}$):** Flach auf dem Boden zu liegen ist mit katastrophaler Aversion belegt ($\mathbf{C} = -8.0$).
2. **Vitalitätsmaximierung ($\Phi$):** Regungslos am Boden zu liegen bedeutet $\Phi \approx 0.0\text{ nats}$ (Verlust der systemischen Integration).
3. **Der Conatus-Imperativ:** Das System existiert, um aktiv gegen die Entropie anzukämpfen. Das Aufrechtstehen gegen die Schwerkraft ist der physische Beweis dieser Lebendigkeit.
"""
    return md

def build_html_wrapper(title, lang, body_html, logo_base64=None):
    footer_page_text = "Page " if lang == "en" else "Seite "
    footer_of_text = " of " if lang == "en" else " von "
    
    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <!-- MathJax for rendering LaTeX formulas cleanly -->
    <script>
    window.MathJax = {{
      tex: {{
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
        processEscapes: true
      }},
      svg: {{
        fontCache: 'global'
      }}
    }};
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        @page {{
            size: A4 portrait;
            margin: 18mm 16mm 18mm 16mm;
            @bottom-left {{
                content: "Conative Systems S.à r.l. • Active Conative Inference (ACI)";
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 8.5pt;
                font-weight: 500;
                color: #64748b;
            }}
            @bottom-right {{
                content: "{footer_page_text}" counter(page) "{footer_of_text}" counter(pages);
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 8.5pt;
                font-weight: 600;
                color: #0284c7;
            }}
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.45;
            color: #1e293b;
            background-color: #ffffff;
            margin: 0;
            padding: 0;
        }}

        /* Header & Titles */
        h1 {{
            font-size: 19pt;
            font-weight: 800;
            line-height: 1.2;
            color: #0f172a;
            margin-top: 0;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }}

        h2 {{
            font-size: 14pt;
            font-weight: 700;
            color: #0f172a;
            border-left: 4px solid #0284c7;
            padding-left: 8px;
            margin-top: 18pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }}

        h3 {{
            font-size: 12pt;
            font-weight: 600;
            color: #0369a1;
            margin-top: 14pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }}

        h4 {{
            font-size: 11pt;
            font-weight: 700;
            color: #334155;
            margin-top: 10pt;
            margin-bottom: 3pt;
            page-break-after: avoid;
        }}

        p {{
            margin-top: 0;
            margin-bottom: 7pt;
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

        /* Clean Toner-Friendly Code & Formulas */
        pre, code {{
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }}

        code {{
            font-size: 9pt;
            background-color: #f1f5f9;
            padding: 1.5px 4px;
            border-radius: 3px;
            color: #0f172a;
        }}

        pre {{
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 4px solid #0284c7;
            padding: 8pt 10pt;
            border-radius: 4px;
            font-size: 8.5pt;
            line-height: 1.35;
            color: #0f172a;
            overflow-x: auto;
            page-break-inside: avoid;
            margin: 8pt 0;
        }}

        /* Images and SVGs */
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10pt auto;
            border-radius: 6px;
            page-break-inside: avoid;
        }}

        /* Math formula display */
        mjx-container[display="true"] {{
            margin: 8pt 0 !important;
            font-size: 102% !important;
            overflow-x: auto;
            page-break-inside: avoid;
        }}

        hr {{
            border: none;
            border-top: 1px solid #e2e8f0;
            margin: 14pt 0;
        }}

        blockquote {{
            border-left: 4px solid #0284c7;
            margin: 8pt 0;
            padding: 6pt 10pt;
            background-color: #f0f9ff;
            color: #0369a1;
            border-radius: 0 4px 4px 0;
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>
{body_html}
</body>
</html>"""
    return html

def convert_md_to_html(md_path, html_path, title, lang):
    cmd = [
        "pandoc",
        md_path,
        "-o", html_path,
        "--from=markdown+tex_math_dollars+tex_math_single_backslash",
        "--to=html5",
        "--mathjax"
    ]
    subprocess.run(cmd, check=True)
    with open(html_path, "r", encoding="utf-8") as f:
        body_content = f.read()
    
    full_html = build_html_wrapper(title, lang, body_content)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def render_pdf(html_path, pdf_path):
    cmd = [
        "google-chrome",
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--virtual-time-budget=12000",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)

def main():
    import sys
    proj_dir = "/home/thr/Documents/04-projects/inverse_pendulum_aci"
    obsidian_dir = "/home/thr/Documents/ThRNotes/04-projects/inverse_pendulum_aci"
    vault_projects_dir = "/home/thr/Documents/ThRNotes/04-projects"
    general_projects_dir = "/home/thr/Documents/04-projects"
    
    os.makedirs(proj_dir, exist_ok=True)
    os.makedirs(obsidian_dir, exist_ok=True)

    # 1. Write English and German Markdown
    en_md_path = os.path.join(proj_dir, "planar_inverted_pendulum_aci_didactic_en.md")
    de_md_path = os.path.join(proj_dir, "planar_inverted_pendulum_aci_didactic_de.md")

    print("Writing English Markdown documentation...")
    with open(en_md_path, "w", encoding="utf-8") as f:
        f.write(get_markdown_en())

    print("Writing German Markdown documentation...")
    with open(de_md_path, "w", encoding="utf-8") as f:
        f.write(get_markdown_de())

    # Copy markdown files to Obsidian
    shutil.copy(en_md_path, os.path.join(obsidian_dir, "planar_inverted_pendulum_aci_didactic_en.md"))
    shutil.copy(de_md_path, os.path.join(obsidian_dir, "planar_inverted_pendulum_aci_didactic_de.md"))
    print(f"Copied markdown files to {obsidian_dir}")

    # Render PDFs ONLY when explicitly requested with --pdf
    if "--pdf" in sys.argv:
        en_html = os.path.join(proj_dir, "temp_render_en.html")
        de_html = os.path.join(proj_dir, "temp_render_de.html")
        
        print("Converting English MD to HTML...")
        convert_md_to_html(en_md_path, en_html, "Active Conative Inference (ACI): The Planar Inverted Pendulum", "en")

        print("Converting German MD to HTML...")
        convert_md_to_html(de_md_path, de_html, "Active Conative Inference (ACI): Das Planare Invertierte Pendel", "de")

        en_pdf = os.path.join(proj_dir, "planar_inverted_pendulum_aci_didactic_en.pdf")
        de_pdf = os.path.join(proj_dir, "planar_inverted_pendulum_aci_didactic_de.pdf")

        print("Rendering English PDF via Chrome Headless...")
        render_pdf(en_html, en_pdf)

        print("Rendering German PDF via Chrome Headless...")
        render_pdf(de_html, de_pdf)

        for fname, src in [("planar_inverted_pendulum_aci_didactic_en.pdf", en_pdf), ("planar_inverted_pendulum_aci_didactic_de.pdf", de_pdf)]:
            shutil.copy(src, os.path.join(obsidian_dir, fname))
            shutil.copy(src, os.path.join(vault_projects_dir, fname))
            shutil.copy(src, os.path.join(general_projects_dir, fname))
            print(f"Mirrored {fname} to {obsidian_dir}, {vault_projects_dir}, and {general_projects_dir}")

        if os.path.exists(en_html): os.remove(en_html)
        if os.path.exists(de_html): os.remove(de_html)

    print("\n✓ Markdown documentation successfully updated (PDFs skipped until explicit request)!")

if __name__ == "__main__":
    main()
