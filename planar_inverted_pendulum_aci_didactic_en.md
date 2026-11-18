<img src="conative_systems_logo.svg" align="right" width="125" style="float: right; margin-left: 20px; margin-bottom: 15px;" alt="Conative Systems Logo" />

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
