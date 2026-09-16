# Methodological Proposals for GNN: Causal Integration Metrics and Declarative Agent Coupling

**Author:** Thomas Riebl  
**Context:** Research on Deep Temporal Active Inference, Integrated Information Theory (IIT 4.0), and the Conative-Integrative Framework (CIF)  
**Target:** Generalized Notation Notation (GNN) Pipeline Architecture

---

## Overview

Following the successful validation and multi-framework execution of my **Conative-Integrative Framework (CIF)** deep temporal POMDP agent within the GNN pipeline, Daniel invited me to share ideas for methods that would be useful for my research and could be circulated back into GNN improvements.

In my research, I investigate the formal intersection between **Active Inference / the Free Energy Principle (FEP)**, **temporal horizon depth**, and **Integrated Information Theory (IIT 4.0)**. Specifically, I test what I formulate as the **6th Axiom of Autopoietic Persistence**:

$$\mathbb{E}_{\pi^*}\left[\Phi(t+1)\right] \ge \Phi(t) > 0$$

where an agent's policy selection under Expected Free Energy ($\mathbf{G}$) must actively preserve its internal integrated cause-effect power ($\Phi$) against entropic decay.

To support this work and broaden GNN's capabilities for computational phenomenology, cognitive science, and collective intelligence, I propose two major methodological extensions:

1. **Native Causal Integration & $\Phi$ Metrics in Step 16 (Analysis Pipeline)**
2. **Declarative Markov Blanket Coupling for Multi-Agent Networks**

---

## Proposal 1: Causal Integration & $\Phi$ Metrics in Step 16 (Analysis)

### 1. Motivation in My Research
In my simulations of the CIF agent, I observed a fundamental phase transition governed by the planning horizon $H$:
* **Reflex Agent ($H = 0$):** Lacking counterfactual trajectory projection, the agent falls into immediate sensory traps. Its internal causal integration collapses to baseline noise ($\Phi \to 0$), signifying cognitive dissolution.
* **Temporal Agent ($H \ge 1$):** By projecting counterfactual futures under Expected Free Energy, the agent actively selects epistemic detours, avoids systemic collapse, and sustains $\Phi \ge 1.45$.

Currently, Step 16 (`16_analysis.py`) provides excellent diagnostics for:
* Variational Free Energy (VFE) convergence: $F(s_t, o_t)$
* Expected Free Energy (EFE) profile: $\mathbf{G}(\pi)$
* Belief state entropy: $\mathcal{H}\left(Q(s_t)\right) = - \sum_{s} Q(s_t) \ln Q(s_t)$
* Action frequencies and state traces.

However, to formally track cognitive integrity and subjective structure, I currently have to compute cause-effect integration ($\Phi$) in a separate, disconnected post-processing step.

### 2. Proposed Formulation for GNN
I propose introducing an optional analysis flag (e.g., `--compute-phi` or `--causal-integration`) into Step 16 that computes state-transition integrated information directly from the canonical transition tensor $B$ and likelihood $A$.

For a state distribution $Q(s_t)$ and transition tensor $B(s_{t+1} \mid s_t, u_t)$, the state-dependent cause-effect integration across the Minimum Information Bipartition (MIP) $P = \{M^1, M^2\}$ can be evaluated as:

$$\Phi(t) = D_{\text{KL}}\left( Q(s_{t+1}, s_t \mid u_t) \;\Big\|\; Q(s_{t+1}^{M^1}, s_t^{M^1} \mid u_t) \otimes Q(s_{t+1}^{M^2}, s_t^{M^2} \mid u_t) \right)$$

where:
$$\text{MIP} = \arg\min_{P} \frac{D_{\text{KL}}\left( Q(s_{t+1}, s_t) \,\|\, Q^P(s_{t+1}, s_t) \right)}{\min\left(|M^1|, |M^2|\right)}$$

### 3. Concrete Value for GNN
* **Visualizing the Dual Dynamics:** Step 16 could automatically generate dual-axis plots correlating $F(t)$ (Free Energy minimization) with $\Phi(t)$ (Causal Integration maintenance).
* **World-First Capability:** This would make GNN the first standardized modeling toolchain in existence capable of evaluating the Free Energy Principle and Integrated Information Theory inside the exact same computational artifact.

---

## Proposal 2: Declarative Markov Blanket Coupling for Multi-Agent Networks

### 1. Motivation in My Research
In the second stage of my Conative-Integrative Framework, I explore how conscious agents scale from solitary systems into collective cognitive architectures (collective $\Phi$ and social active inference). 

When two or more Active Inference agents interact, their Markov blankets become recursively interlocked:
* The **action** (active states) of Agent $A$ ($u^{(A)}_t$) modulates the **sensory observation** of Agent $B$ ($o^{(B)}_t$).
* The internal belief updating of Agent $B$ in turn emits actions ($u^{(B)}_t$) that form the sensory inputs to Agent $A$.

Currently, multi-agent implementations require manual environment scripting or ad-hoc wrappers outside the formal `.gnn.md` specification.

### 2. Proposed Formulation for GNN
I propose adding a declarative coupling block to the GNN specification standard (e.g., `## AgentCoupling` or `## NetworkTopology`), allowing modelers to define how discrete agents interface:

```markdown
## NetworkTopology
Agent_A: cif_deep_temporal_agent.gnn
Agent_B: cif_deep_temporal_agent.gnn

## CouplingChannel
# Observation of Agent B is conditioned on Action of Agent A
Agent_A.u -> Channel_AB -> Agent_B.o
Matrix_AB = {
  # Transfer likelihood mapping u_A to o_B
  (1.0, 0.0, 0.0, 0.0),
  (0.0, 1.0, 0.0, 0.0),
  (0.0, 0.0, 1.0, 0.0),
  (0.0, 0.0, 0.0, 1.0)
}
```

Mathematically, the coupled generative dynamics follow:

$$P\left(o^{(B)}_t \mid u^{(A)}_t\right) = \sum_{s} A^{(B)}\left(o^{(B)}_t \mid s^{(B)}_t\right) \cdot \Gamma_{AB}\left(s^{(B)}_t \mid u^{(A)}_t\right)$$

where $\Gamma_{AB}$ represents the shared environmental mediator or communication channel between the two blankets.

### 3. Concrete Value for GNN
* **Automated Multi-Agent Rendering:** Step 11 could automatically emit coupled multi-agent simulation scripts (e.g., native multi-agent loops in PyMDP or reactive graphs in RxInfer.jl).
* **Standardized Collective Inference:** It standardizes social active inference, stigmergic communication, and swarm intelligence within the GNN specification syntax, removing the need for external boilerplate code.

---

## Summary of How This Supports My Ongoing Work

These two extensions would directly empower my upcoming research on the Conative-Integrative Framework:
1. **Empirical Axiom Testing:** It allows me to automate the verification of the 6th Axiom ($\Delta \Phi \ge 0$) across large-scale Monte Carlo batches entirely within the GNN toolchain.
2. **Multi-Agent Scaling:** It provides a reproducible, standardized foundation for my upcoming publications on collective consciousness and multi-agent Active Inference networks.

---

## Model Package, Test Scripts & Supporting Material

To provide a fully reproducible baseline for exploring these ideas, I have published the complete standalone package in a dedicated directory in this repository:

👉 **[Complete CIF GNN Model Package Directory](https://github.com/Thriebl/active-inference-phi-network/tree/main/cif_gnn_model_package)**

### Direct Component Links:
* **Canonical GNN v1.1 Model Specification:**  
  [`cif_deep_temporal_agent.gnn.md`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/cif_deep_temporal_agent.gnn.md)
* **Empirical Monte Carlo Test Script (PyMDP):**  
  [`scripts/run_cif_pymdp_agent.py`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/scripts/run_cif_pymdp_agent.py) *(Runs 20 trials over $H \in \{0, 1, 2, 4\}$ demonstrating the $\Phi$ phase transition)*
* **GNN Rendered Standalone Runners:**  
  * PyMDP 1.0 Runner: [`scripts/CIF_Deep_Temporal_Agent_H2_pymdp.py`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/scripts/CIF_Deep_Temporal_Agent_H2_pymdp.py)  
  * Julia / RxInfer.jl Runner: [`scripts/CIF_Deep_Temporal_Agent_H2_rxinfer.jl`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/scripts/CIF_Deep_Temporal_Agent_H2_rxinfer.jl)  
* **Execution Data & Traces:**  
  * 25-step execution output: [`results/simulation_results.json`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/results/simulation_results.json)  
* **Visual Trajectory & Structural Graphs:**  
  * Monte Carlo Phase Transition Plot: [`results/pymdp_cif_simulation_run.png`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/results/pymdp_cif_simulation_run.png)  
  * Step 8 Matrix Distributions & Heatmaps: [`results/cif_deep_temporal_agent.gnn_combined_analysis.png`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/results/cif_deep_temporal_agent.gnn_combined_analysis.png)  
  * Step 16 VFE vs. EFE Trajectory Dynamics: [`results/cif_deep_temporal_agent.gnn_pymdp_vfe_vs_efe.png`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/results/cif_deep_temporal_agent.gnn_pymdp_vfe_vs_efe.png)  
  * Interactive Bipartite Network Graph: [`results/cif_deep_temporal_agent.gnn_network_interactive.html`](https://github.com/Thriebl/active-inference-phi-network/blob/main/cif_gnn_model_package/results/cif_deep_temporal_agent.gnn_network_interactive.html)  

I would be delighted to provide any further traces or collaborate on testing if these features align with upcoming GNN roadmap cycles!
