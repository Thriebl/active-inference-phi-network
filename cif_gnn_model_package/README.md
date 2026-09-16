# The Conative-Integrative Framework (CIF): GNN Model Package

**Author:** Thomas Riebl  
**Context:** Research on Deep Temporal Active Inference, Integrated Information Theory (IIT 4.0), and the 6th Axiom of Autopoietic Persistence  
**Specification Standard:** Active Inference Institute — Generalized Notation Notation (GNN v1.1)

---

## Overview

This directory contains the self-contained model specification, test scripts, rendered backend runners, and simulation outputs for the **Conative-Integrative Framework (CIF)** deep temporal POMDP agent.

The model formalizes the **Temporal Depth Condition for Consciousness (Theorem 6.1)** and empirically tests the **6th Axiom of Autopoietic Causal Persistence**:

$$\mathbb{E}_{\pi^*}\left[\Phi(t+1)\right] \ge \Phi(t) > 0$$

In this architecture, an agent's policy selection under Expected Free Energy ($\mathbf{G}$) must actively preserve its internal cause-effect power ($\Phi$) to avert cognitive and physical collapse in deceptive environments.

---

## Directory Contents

```
cif_gnn_model_package/
├── README.md                                  # This documentation
├── cif_deep_temporal_agent.gnn.md             # Canonical GNN v1.1 model specification
├── scripts/
│   ├── run_cif_pymdp_agent.py                 # Empirical Monte Carlo simulation across planning horizons H ∈ {0, 1, 2, 4}
│   ├── CIF_Deep_Temporal_Agent_H2_pymdp.py    # GNN Step 11 rendered standalone PyMDP runner
│   └── CIF_Deep_Temporal_Agent_H2_rxinfer.jl  # GNN Step 11 rendered reactive Julia / RxInfer.jl runner
└── results/
    ├── simulation_results.json                # Execution trace data (25 timesteps)
    ├── pymdp_cif_simulation_run.png           # Monte Carlo phase transition plot (H=0 vs H>=1 survival & Phi)
    ├── cif_deep_temporal_agent.gnn_combined_analysis.png  # GNN matrix distributions & parameter heatmap
    ├── cif_deep_temporal_agent.gnn_pymdp_vfe_vs_efe.png   # Step 16 VFE vs. EFE dynamic trajectory plot
    └── cif_deep_temporal_agent.gnn_network_interactive.html # Interactive HTML bipartite network graph
```

---

## 1. The Generative Model

* **6 Hidden States:** Start ($s_0$), Cue ($s_1$), Trap ($s_2$), Safe Path ($s_3$), Goal ($s_4$), Death ($s_5$).
* **5 Sensory Observations:** Neutral ($o_0$), Ambiguous ($o_1$), Safe ($o_2$), Sweet Temptation ($o_3$), Lethal Collapse ($o_4$).
* **4 Controllable Actions:** Stay ($u_0$), Visit Cue ($u_1$), Go to Trap ($u_2$), Go to Safe Path ($u_3$).
* **Tensors:**
  * **$A$ (Likelihood, $5 \times 6$):** Sensory mapping with high epistemic ambiguity at the start.
  * **$B$ (Transition Tensor, $6 \times 6 \times 4$):** Row-stochastic transition dynamics where the Trap ($s_2$) collapser deterministically to Death ($s_5$).
  * **$C$ (Preferences, $5 \times 1$):** Prior attractors with a deceptive positive valence for the sweet cue ($+2.0$), strong reward for the goal ($+4.5$), and massive penalty for death ($-10.0$).
  * **$D$ (Prior, $6 \times 1$):** Deterministic initialization at the Start state ($s_0$).

---

## 2. Compilation via the GNN Pipeline

To validate and transpile this model using the official [ActiveInferenceInstitute/GeneralizedNotationNotation](https://github.com/ActiveInferenceInstitute/GeneralizedNotationNotation) toolchain:

```bash
# 1. Copy the model specification to GNN input
cp cif_deep_temporal_agent.gnn.md path/to/GeneralizedNotationNotation/input/gnn_files/

# 2. Run GNN Steps: Render, Execute, and Analyze
cd path/to/GeneralizedNotationNotation
uv run python src/gnn/8_visualization.py --target-dir input/gnn_files --output-dir output
uv run python src/gnn/11_render.py --target-dir input/gnn_files --output-dir output
uv run python src/gnn/12_execute.py --target-dir input/gnn_files --output-dir output
uv run python src/gnn/16_analysis.py --target-dir input/gnn_files --output-dir output
```

The pipeline automatically compiles the model into 22 target representations, including PyMDP, RxInfer.jl, JAX, NumPyro, PyTorch, Stan, and DisCoPy.

---

## 3. Running the Empirical Test Scripts

### A. Monte Carlo Horizon Comparison (PyMDP)
To reproduce the empirical phase transition comparing reflex agents ($H=0$) to deep temporal agents ($H \ge 1$):

```bash
python scripts/run_cif_pymdp_agent.py
```
* **Findings:** 
  * Reflex agents ($H=0$) fall for the immediate sweet temptation ($s_2$) with a 60% mortality rate; $\Phi$ collapses to noise ($\approx 0.01$).
  * Deep temporal agents ($H \ge 1$) project counterfactual outcomes under Expected Free Energy, take the epistemic detour to the Cue ($s_1$), achieve 100% survival, and sustain $\Phi \ge 1.45$.

### B. Julia / RxInfer.jl Execution
To run the reactive message-passing simulation:

```bash
julia scripts/CIF_Deep_Temporal_Agent_H2_rxinfer.jl
```

---

## Supporting Artifacts

* **Interactive Browser Graph:** Open `results/cif_deep_temporal_agent.gnn_network_interactive.html` in any browser to explore the bipartite state-observation topology.
* **Methodology Proposals:** See [`../docs/gnn_methodology_proposals.md`](../docs/gnn_methodology_proposals.md) for proposals regarding native $\Phi$ integration in Step 16 and multi-agent Markov blanket coupling.
