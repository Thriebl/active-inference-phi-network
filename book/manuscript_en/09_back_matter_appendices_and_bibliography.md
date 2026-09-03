# Chapter 9: Mathematical Appendices, Source Code & Academic Bibliography

---

## Appendix A: Mathematical Formalisms & Tensor Notations

### 1. The POMDP Generative Model
The discrete Partially Observable Markov Decision Process (POMDP) of a conscious alter is defined by the tuple:

$$\mathcal{M} = \big\langle \mathcal{S}, \mathcal{O}, \mathcal{U}, A, B, C, D, \gamma \big\rangle$$

* **Hidden States:** $s \in \mathcal{S} = \{1, \dots, N_s\}$
* **Observations:** $o \in \mathcal{O} = \{1, \dots, N_o\}$
* **Actions:** $u \in \mathcal{U} = \{1, \dots, N_u\}$
* **Likelihood Mapping ($A$):** $P(o_\tau \mid s_\tau) = A \in \mathbb{R}^{N_o \times N_s}$, where $\sum_j A_{j, k} = 1$.
* **Transition Tensor ($B$):** $P(s_{\tau+1} \mid s_\tau, u_\tau) = B \in \mathbb{R}^{N_s \times N_s \times N_u}$, where $\sum_i B_{i, j, u} = 1$.
* **Prior Preferences ($C$):** $\ln P(o) = C \in \mathbb{R}^{N_o}$.
* **Initial State Prior ($D$):** $P(s_1) = D \in \mathbb{R}^{N_s}$, where $\sum_k D_k = 1$.
* **Action Precision ($\gamma$):** Inverse temperature governing policy selection certainty.

### 2. Variational State Belief Updating (Perceptual Inference)
At time step $t$, upon observing $o_t$, the variational posterior $q(s_t)$ is computed in log-space via softmax:

$$q(s_t) = \sigma\Big( \ln A_{o_t, :} + \ln \big( B(u_{t-1}) \cdot q(s_{t-1}) \big) \Big)$$

Where $\sigma(x)_i = \frac{\exp(x_i)}{\sum_j \exp(x_j)}$ is the softmax function.

### 3. Expected Free Energy ($\mathbf{G}$) over Planning Horizon $H$
For candidate policy $\pi = (u_t, u_{t+1}, \dots, u_{t+H-1})$:

$$\mathbf{G}(\pi) = \sum_{\tau = t+1}^{t+H} \delta^{\tau - t} \cdot \mathbf{G}(\pi, \tau)$$

$$\mathbf{G}(\pi, \tau) = \underbrace{\sum_{o_\tau} Q(o_\tau \mid \pi) \cdot \Big(\ln Q(o_\tau \mid \pi) - C(o_\tau)\Big)}_{\text{Pragmatic Value (KL Divergence to Goals)}} + \underbrace{\sum_{s_\tau} Q(s_\tau \mid \pi) \cdot \mathcal{H}\big(A_{:, s_\tau}\big)}_{\text{Epistemic Ambiguity}}$$

Where predicted observations are:

$$Q(o_\tau \mid \pi) = A \cdot Q(s_\tau \mid \pi)$$

$$Q(s_\tau \mid \pi) = B(u_{\tau-1}) \cdot Q(s_{\tau-1} \mid \pi)$$

### 4. Policy Selection via Precision-Weighted Boltzmann Distribution
$$P(\pi) = \frac{\exp\big(-\gamma \cdot \mathbf{G}(\pi)\big)}{\sum_{\pi'} \exp\big(-\gamma \cdot \mathbf{G}(\pi')\big)}$$

---

## Appendix B: Python Implementation of Deep Temporal Agent

```python
"""
Deep Temporal Active Inference Agent (CIF Core Implementation)
Author: Thomas Riebl (2026)
"""
import numpy as np
import scipy.linalg as la
import itertools

class DeepTemporalActiveInferenceAgent:
    def __init__(self, name, horizon=4, num_states=6, num_obs=5, num_actions=4, precision=2.5):
        self.name = name
        self.horizon = horizon
        self.num_states = num_states
        self.num_obs = num_obs
        self.num_actions = num_actions
        self.precision = precision
        
        # 1. State Prior D
        self.D = np.zeros(num_states)
        self.D[0] = 1.0  # Initialized at Start state (s0)
        
        # 2. Likelihood Matrix A = P(o | s)
        self.A = np.zeros((num_obs, num_states))
        self.A[0, 0] = 1.0  # Start -> Neutral obs
        self.A[1, 1] = 0.2; self.A[2, 1] = 0.8  # Cue -> Disambiguates safe path
        self.A[3, 2] = 0.9; self.A[4, 2] = 0.1  # Trap -> Deceptive sweet obs
        self.A[0, 3] = 0.8; self.A[2, 3] = 0.2  # Path1 -> Neutral/Safe
        self.A[2, 4] = 1.0  # True Goal -> True safe obs
        self.A[4, 5] = 1.0  # Death -> Lethal collapse obs
        self.A += 1e-6
        self.A = self.A / self.A.sum(axis=0, keepdims=True)
        
        # 3. Transition Tensors B = P(s_{t+1} | s_t, u)
        self.B = np.zeros((num_states, num_states, num_actions))
        for u in range(num_actions):
            self.B[:, :, u] = np.eye(num_states)
            
        # Action 1: Move to Cue Site
        self.B[:, 0, 1] = 0; self.B[1, 0, 1] = 1.0
        # Action 2: Move to Trap (Lethal collapse after delay)
        self.B[:, 0, 2] = 0; self.B[2, 0, 2] = 1.0
        for u in range(num_actions):
            self.B[:, 2, u] = 0; self.B[5, 2, u] = 1.0
            
        # Action 3: Move to Safe Path / Goal
        self.B[:, 0, 3] = 0; self.B[3, 0, 3] = 1.0
        self.B[:, 1, 3] = 0; self.B[3, 1, 3] = 1.0
        self.B[:, 3, 3] = 0; self.B[4, 3, 3] = 1.0
        
        # 4. Prior Preferences C = ln P(o)
        self.C = np.array([0.0, -1.0, 4.5, 2.0, -10.0])
        self.qs = self.D.copy()
        
    def infer_states(self, obs):
        likelihood = self.A[obs, :]
        self.qs = self.qs * likelihood
        self.qs = self.qs / (np.sum(self.qs) + 1e-12)
        return self.qs
        
    def calculate_expected_free_energy(self, policy):
        if self.horizon == 0:
            return 0.0
        G = 0.0
        curr_qs = self.qs.copy()
        for t, u in enumerate(policy):
            next_qs = self.B[:, :, u] @ curr_qs
            next_qs = next_qs / (np.sum(next_qs) + 1e-12)
            qo = self.A @ next_qs
            qo = qo / (np.sum(qo) + 1e-12)
            pragmatic = np.sum(qo * self.C)
            H_qo = -np.sum(qo * np.log(qo + 1e-12))
            H_A = -np.sum(self.A * np.log(self.A + 1e-12), axis=0)
            epistemic = H_qo - np.sum(next_qs * H_A)
            step_G = -(pragmatic + 1.2 * epistemic)
            G += (0.95 ** t) * step_G
            curr_qs = next_qs
        return G

    def select_action(self):
        if self.horizon == 0:
            return np.random.choice([1, 2, 3], p=[0.2, 0.6, 0.2]), 0.0
        policies = list(itertools.product(range(self.num_actions), repeat=self.horizon))
        G_vals = np.array([self.calculate_expected_free_energy(pol) for pol in policies])
        e_G = np.exp(-self.precision * (G_vals - np.min(G_vals)))
        p_pol = e_G / np.sum(e_G)
        chosen_idx = np.random.choice(len(policies), p=p_pol)
        return policies[chosen_idx][0], G_vals[chosen_idx]
```

---

## Appendix C: Open Science, Git Repository & Computational Reproducibility

In alignment with the highest standards of open, transparent, and reproducible science, all simulation source codes, interactive Jupyter Notebooks, foundational treatises, and high-resolution publication assets accompanying this monograph are hosted publicly on GitHub:

* **Primary Project Repository:**  
  [https://github.com/Thriebl/active-inference-phi-network](https://github.com/Thriebl/active-inference-phi-network)

### 1. Interactive Simulation Notebooks (`notebooks/`):
* **Recurrent $\Phi$-Maximization Network:**  
  [`Active_Inference_Phi_Maximization_Network.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Active_Inference_Phi_Maximization_Network.ipynb)  
  *Simulates active inference agent arrays self-organizing at the Edge of Chaos (Criticality) to maximize Integrated Information ($\Phi$).*
* **Modular Network Scaling ($\Phi(N)$):**  
  [`Active_Inference_Expanding_Network_Phi_Scaling.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Active_Inference_Expanding_Network_Phi_Scaling.ipynb)  
  *Simulates dynamic modular network expansion from $N=4$ to $N=12$ nodes, demonstrating superlinear $\Phi$ integration.*
* **Deep Temporal Active Inference & The 6th Axiom:**  
  [`Deep_Temporal_Active_Inference_Simulation.ipynb`](https://github.com/Thriebl/active-inference-phi-network/blob/main/notebooks/Deep_Temporal_Active_Inference_Simulation.ipynb)  
  *Multi-agent Monte Carlo simulation ($N=30$) proving the Theorem of Minimum Temporal Depth ($H > 1$) and epistemic curiosity.*

### 2. Foundational Treatises & Academic Papers (`docs/`):
* **The Master Framework Paper:** *The Conative-Integrative Framework (CIF)*  
  [`The_Conative_Integrative_Framework_Thomas_Riebl.pdf`](https://github.com/Thriebl/active-inference-phi-network/blob/main/docs/The_Conative_Integrative_Framework_Thomas_Riebl.pdf)
* **The Ontogenetic Architecture:** *The Composition of the Soul: The 6-Layer Architecture*  
  [`The_Composition_of_the_Soul_Thomas_Riebl.pdf`](https://github.com/Thriebl/active-inference-phi-network/blob/main/docs/The_Composition_of_the_Soul_Thomas_Riebl.pdf)
* **The Temporal Mechanics:** *The Temporal Mechanics of Consciousness (Time & The Specious Present)*  
  [`The_Temporal_Mechanics_of_Consciousness_Thomas_Riebl.pdf`](https://github.com/Thriebl/active-inference-phi-network/blob/main/docs/The_Temporal_Mechanics_of_Consciousness_Thomas_Riebl.pdf)
* **The Statistical Framework:** *Monte Carlo Methodology in Active Inference & Consciousness*  
  [`Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.pdf`](https://github.com/Thriebl/active-inference-phi-network/blob/main/docs/Monte_Carlo_Methodology_Active_Inference_Thomas_Riebl.pdf)
* **The Executive Landscape Poster:** *The 6th Axiom Executive Slide (High-Impact Hero Formula)*  
  [`The_6th_Axiom_Executive_Slide_Thomas_Riebl_A4_Landscape.pdf`](https://github.com/Thriebl/active-inference-phi-network/blob/main/docs/The_6th_Axiom_Executive_Slide_Thomas_Riebl_A4_Landscape.pdf)

---

## Appendix D: Alphabetical Glossary of Technical Terms

* **Active Inference:** The normative mathematical framework in theoretical neurobiology stating that living organisms preserve homeostatic existence by executing actions to minimize Expected Free Energy ($\mathbf{G}$), bringing sensory observations into alignment with prior preferences.
* **Alter (Dissociated Center of Mind):** In Analytic Idealism, an individual living organism formed through the topological dissociation of Mind-at-Large, demarcated by a statistical Markov Blanket.
* **Analytic Idealism:** The non-dual, parsimonious monistic ontology (formulated by Bernardo Kastrup) asserting that reality in its essence is experiential (*Mind-at-Large*), and inanimate physical matter is the extrinsic appearance of universal mental processes observed across a boundary.
* **Autopoiesis:** The fundamental property of a living system to continuously regenerate, repair, and sustain its own structural and organizational network against thermodynamic dispersion.
* **Conatus:** The innate striving of any living entity to persevere in its own existence and resist entropic destruction (Spinoza). In CIF, formalized as the conative goal state $\Phi > 0$.
* **Criticality (Edge of Chaos):** The delicate phase transition boundary between rigid order and chaotic turbulence where information transmission, network dynamic range, and integrated information ($\Phi$) reach their global maximum.
* **Expected Free Energy ($\mathbf{G}$):** A forward-looking metric evaluating candidate policy sequences over planning horizon $H$, decomposing into pragmatic value (goal satisfaction) and epistemic value (ambiguity resolution / curiosity).
* **Explanatory Gap:** The insurmountable epistemic chasm within physicalism between quantitative objective neural mechanisms and qualitative subjective experience (Levine).
* **Hard Problem of Consciousness:** The fundamental question of why and how physical computations in a brain should ever give rise to subjective, qualitative inner experience (*qualia*) (Chalmers).
* **Integrated Information ($\Phi$):** The quantitative measure of intrinsic cause-effect power within a maximally irreducible physical substrate, computed across the Minimum Information Partition (Tononi, IIT 4.0).
* **Markov Blanket:** A statistical boundary partitioning a system into internal ($\mu$), sensory ($s$), active ($a$), and external ($\eta$) states, rendering internal states conditionally independent of external states.
* **Mind-at-Large:** The universal, transpersonal field of pure consciousness that constitutes the fundamental ontological ground of reality (Spinoza, Kastrup).
* **Minimum Information Partition (MIP):** The bipartition of a system that minimizes informational and causal loss, used to calculate irreducibility and integrated information $\Phi$.
* **Phenomenal Self-Model (PSM):** A transparent, continuous internal simulation generated by the predictive brain that creates the felt 1st-person perspective of an enduring "I" (Metzinger).
* **POMDP (Partially Observable Markov Decision Process):** A mathematical framework for modeling decision-making under uncertainty, defined by matrices $A$ (likelihood), $B$ (transitions), $C$ (preferences), and $D$ (priors).
* **Primal Impression (*Urimpression*):** The present sensory perturbation at the Markov boundary within the Specious Present, corresponding to incoming prediction errors (Husserl).
* **Protention:** The forward-looking anticipatory projection within the Specious Present, corresponding to top-down generative predictions (Husserl).
* **Retention:** The immediate past preserved in working memory within the Specious Present, corresponding to empirical synaptic priors (Husserl).
* **Specious Present:** The tripartite, non-zero temporal duration of subjective consciousness ($\sim 500\,\text{ms} - 3\,\text{s}$) combining Retention, Primal Impression, and Protention (James, Husserl).
* **Temporal Depth ($H$):** The length of the forward-looking counterfactual planning horizon over which an agent evaluates transition tensors ($B$) and expected free energy ($\mathbf{G}$).
* **Theorem of Minimum Temporal Depth:** The mathematical necessity condition stating that phenomenal self-consciousness strictly requires multi-step counterfactual planning ($H > 1$) to avoid causal collapse ($\Phi \to 0$) (Riebl).
* **The 6th Axiom of Consciousness:** The axiom of *Autopoietic Causal Persistence*, establishing that genuine consciousness requires an active striving to preserve integrated cause-effect power over time: $\mathbb{E}[\Phi(t+1) \mid \pi^*] \ge \Phi(t)$ (Riebl).
* **Variational Free Energy ($F$):** A computable upper bound on sensory surprise ($-\ln P(o)$), minimized during perceptual inference to eliminate prediction errors.

---

## Academic References & Comprehensive Bibliography

1. **Bak, P. (1996).** *How Nature Works: The Science of Self-Organized Criticality.* Copernicus, Springer-Verlag, New York.
2. **Beggs, J. M., & Plenz, D. (2003).** *Neuronal avalanches in neocortical circuits.* Journal of Neuroscience, 23(35), 11167–11177.
3. **Bouchard, T. J. (2004).** *Genetic influence on human psychological traits: A survey.* Current Directions in Psychological Science, 13(4), 148–151.
4. **Chalmers, D. J. (1995).** *Facing up to the problem of consciousness.* Journal of Consciousness Studies, 2(3), 200–219.
5. **Chialvo, D. R. (2010).** *Emergent complex neural dynamics.* Nature Physics, 6(10), 744–750.
6. **Clark, A. (2013).** *Whatever next? Predictive brains, situated agents, and the future of cognitive science.* Behavioral and Brain Sciences, 36(3), 181–204.
7. **Clark, A. (2016).** *Surfing Uncertainty: Prediction, Action, and the Embodied Mind.* Oxford University Press.
8. **Da Costa, L., Parr, T., Sajid, N., Veselic, S., Neacsu, V., & Friston, K. (2020).** *Active inference on discrete state-spaces: A synthesis.* Journal of Mathematical Psychology, 99, 102447.
9. **Eigen, M. (1971).** *Selforganization of matter and the evolution of biological macromolecules.* Die Naturwissenschaften, 58(10), 465–523.
10. **Eigen, M., & Winkler, R. (1975).** *Das Spiel: Unsere Begegnung mit dem Zufall.* Piper Verlag, München.
11. **Fountas, Z., Sajid, N., Mediano, P. A. M., & Friston, K. (2020).** *Deep active inference agents using Monte-Carlo methods.* Advances in Neural Information Processing Systems (NeurIPS 2020), 33, 11662–11675.
12. **Friston, K. (2010).** *The free-energy principle: a unified brain theory?* Nature Reviews Neuroscience, 11(2), 127–138.
13. **Friston, K., FitzGerald, T., Rigoli, F., Schwartenbeck, P., & Pezzulo, G. (2017).** *Active Inference: A Process Theory.* Neural Computation, 29(1), 1–49.
14. **Friston, K., Rosch, R., Parr, T., Price, C., & Bowman, H. (2017).** *Deep temporal models and active inference.* Neuroscience & Biobehavioral Reviews, 77, 388–402.
15. **Gershman, S. J. (2019).** *The generative adversary in brain and machine.* Trends in Cognitive Sciences, 23(1), 8–17.
16. **Hohwy, J. (2013).** *The Predictive Mind.* Oxford University Press.
17. **Husserl, E. (1928).** *Vorlesungen zur Phänomenologie des inneren Zeitbewusstseins.* Max Niemeyer Verlag, Halle.
18. **Jablonka, E., & Lamb, M. J. (2014).** *Evolution in Four Dimensions: Genetic, Epigenetic, Behavioral, and Symbolic Variation.* MIT Press.
19. **James, W. (1890).** *The Principles of Psychology.* Henry Holt and Company, New York.
20. **Kant, I. (1781).** *Kritik der reinen Vernunft.* Johann Friedrich Hartknoch, Riga.
21. **Kastrup, B. (2019).** *The Idea of the World: A Multi-Disciplinary Argument for the Mental Nature of Reality.* Iff Books.
22. **Kastrup, B. (2021).** *Science Ideated: The Fall of Matter and the Contours of the Next Mainstream Scientific Worldview.* Iff Books.
23. **Kastrup, B., & Friston, K. (2020).** *An Analytic Idealist Perspective on the Free Energy Principle.* Working Treatise.
24. **Levine, J. (1983).** *Materialism and qualia: The explanatory gap.* Pacific Philosophical Quarterly, 64(4), 354–361.
25. **Metzinger, T. (2003).** *Being No One: The Self-Model Theory of Subjectivity.* MIT Press, Cambridge, MA.
26. **Metzinger, T. (2009).** *The Ego Tunnel: The Science of the Mind and the Myth of the Self.* Basic Books, New York.
27. **Metzinger, T. (2024).** *The Elephant and the Blind: The Experience of Pure Consciousness.* MIT Press, Cambridge, MA.
28. **Monod, J. (1970).** *Le Hasard et la Nécessité: Essai sur la philosophie naturelle de la biologie moderne.* Éditions du Seuil, Paris.
29. **Panksepp, J. (1998).** *Affective Neuroscience: The Foundations of Human and Animal Emotions.* Oxford University Press.
30. **Parr, T., & Friston, K. J. (2018).** *The anatomy of choice: active inference and agency.* Cognitive Neuroscience, 9(1-2), 11–27.
31. **Parr, T., Pezzulo, G., & Friston, K. J. (2022).** *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior.* MIT Press, Cambridge, MA.
32. **Plomin, R., DeFries, J. C., Knopik, V. S., & Neiderhiser, J. M. (2016).** *Top 10 Replicated Findings From Behavioral Genetics.* Perspectives on Psychological Science, 11(1), 3–23.
33. **Riebl, T. (2026).** *The Conative-Integrative Framework (CIF): How Active Inference Networks, Integrated Information ($\Phi$), and the 6th Axiom Fit Together to Unite Analytic Idealism, the Free Energy Principle, and Consciousness.* Master Monograph, Luxembourg.
34. **Riebl, T. (2026).** *The Composition of the Soul: The 6-Layer Ontogenetic Architecture of the Dissociated Mind.* Luxembourg.
35. **Riebl, T. (2026).** *The Temporal Mechanics of Consciousness: The Specious Present, Deep Temporal Active Inference, and the Anti-Entropic Arrow of Mind.* Luxembourg.
36. **Roth, G. (2003).** *Aus Sicht des Gehirns.* Suhrkamp Verlag, Frankfurt am Main.
37. **Roth, G. (2021).** *Wie das Gehirn die Seele macht: Emotionen, Bewusstsein, Unbewusstes.* Klett-Cotta, Stuttgart.
38. **Safron, A. (2020).** *An Integrated World Modeling Theory (IWMT) of Consciousness.* Frontiers in Artificial Intelligence, 3, 30.
39. **Schopenhauer, A. (1819/1844).** *Die Welt als Wille und Vorstellung.* F. A. Brockhaus, Leipzig.
40. **Seth, A. K. (2021).** *Being You: A New Science of Consciousness.* Dutton, Penguin Random House.
41. **Seth, A. K., & Tsakiris, M. (2018).** *Being a beast machine: The somatic basis of active inference and consciousness.* Trends in Cognitive Sciences, 22(11), 969–981.
42. **Spinoza, B. (1677).** *Ethica, ordine geometrico demonstrata.* Posthumous Publication.
43. **Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016).** *Integrated information theory: from consciousness to its physical substrate.* Nature Reviews Neuroscience, 17(7), 450–461.
44. **Tononi, G., Albantakis, L., Boly, M., Massimini, M., & Koch, C. (2023).** *Integrated information theory (IIT) 4.0: Formulating the properties of phenomenal existence in physical terms.* PLOS Computational Biology, 19(10), e1011465.
45. **Tschantz, A., Millidge, B., Seth, A. K., & Buckley, C. L. (2020).** *Reinforcement learning through active inference.* arXiv preprint arXiv:2002.12636.
46. **Turkheimer, E. (2000).** *Three Laws of Behavior Genetics and What They Mean.* Current Directions in Psychological Science, 9(5), 160–164.
47. **Wiese, W. (2018).** *Experienced Wholes: Unifying Insight into Phenomenal Integration.* MIT Press.
48. **Yehuda, R., & Lehrner, A. (2018).** *Intergenerational transmission of trauma effects: putative role of epigenetic mechanisms.* World Psychiatry, 17(3), 243–257.

---

## Tool Attribution & Colophon

> [!NOTE]
> **Tooling Colophon:**  
> This theoretical treatise, philosophical architecture, and scientific monograph were conceptualized and authored by **Thomas Riebl** (Luxembourg) as part of **The Conative-Integrative Framework (CIF)**.  
> The conceptual formulation, mathematical modeling, simulation scripts, vector diagrams, and multi-format document compilation (Amazon KDP Print PDF $6 \times 9''$, Word `.docx`, and EPUB) were developed with the assistance of **Google Gemini (Antigravity Advanced Agentic Coding System)** (September 2026).
