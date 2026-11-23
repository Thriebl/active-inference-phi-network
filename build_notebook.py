#!/usr/bin/env python3
"""
build_notebook.py
Generates the comprehensive didactic Jupyter Notebook for Active Conative Inference (ACI)
applied to the Planar 2D Inverted Pendulum scenario (|S| = 5 states, |A| = 2 actions).
Directly extracts all theoretical sections, equations, callouts, and didactic FAQs from
planar_inverted_pendulum_aci_didactic_en.md to guarantee 100% synchronization.
Author: Thomas Riebl
Strict English Language Compliance per GEMINI.md.
"""

import os
import nbformat as nbf

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(script_dir, "planar_inverted_pendulum_aci_didactic_en.md")
    
    if not os.path.exists(md_path):
        # Fallback to 04-projects directory if running elsewhere
        md_path = "/home/thr/Documents/04-projects/inverse_pendulum_aci/planar_inverted_pendulum_aci_didactic_en.md"

    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    nb = nbf.v4.new_notebook()
    cells = []

    # ============================================================================
    # CELL 0: COMPREHENSIVE WALKTHROUGH & PHYSICAL/MATHEMATICAL FOUNDATIONS
    # ============================================================================
    idx_sec4 = text.find("## 4. Formal 5-State Mathematical Specification & State Compass")
    intro_text = text[:idx_sec4].strip()
    cells.append(nbf.v4.new_markdown_cell(intro_text))

    # ============================================================================
    # CELL 1: ENVIRONMENT SETUP & IMPORTS
    # ============================================================================
    cells.append(nbf.v4.new_code_cell("""import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

print("Planar ACI Inverted Pendulum Environment Ready.")"""))

    # ============================================================================
    # CELL 2: SECTION 1: STATE SPACE DEFINITION (5 STATES, 2 ACTIONS)
    # ============================================================================
    idx_sec5 = text.find("## 5. Action Planning")
    sec4_full = text[idx_sec4:idx_sec5].strip()
    idx_prior = sec4_full.find("### Prior Belief Vector")

    sec1_text = "---\n## Section 1: Discrete State Compass and Action Space\n\n" + sec4_full[:idx_prior].strip()
    cells.append(nbf.v4.new_markdown_cell(sec1_text))

    # ============================================================================
    # CELL 3: STATE SPACE & ACTION CONSTANTS
    # ============================================================================
    cells.append(nbf.v4.new_code_cell("""STATE_NAMES = [
    "0 (Balanced)", 
    "l1 (Mild Left)", 
    "l2 (Severe Left)", 
    "r1 (Mild Right)", 
    "r2 (Severe Right)"
]
NUM_STATES = len(STATE_NAMES)

ACTION_NAMES = ["Left", "Right"]
NUM_ACTIONS = len(ACTION_NAMES)

print(f"Loaded {NUM_STATES} Discrete States and {NUM_ACTIONS} Actions.")"""))

    # ============================================================================
    # CELL 4: SECTION 2: BUILDING STREAMLINED 5x5 GENERATIVE MODEL TENSORS
    # ============================================================================
    sec2_text = "---\n## Section 2: Building the Generative Model Tensors\n\n" + sec4_full[idx_prior:].strip()
    cells.append(nbf.v4.new_markdown_cell(sec2_text))

    # ============================================================================
    # CELL 5: GENERATIVE MODEL CLASS IMPLEMENTATION
    # ============================================================================
    cells.append(nbf.v4.new_code_cell(r"""class AciInvertedPendulumModel:
    def __init__(self):
        # 1. State space and actions
        self.num_states = 5
        self.num_actions = 2
        
        # 2. Prior distribution over initial states D
        self.D = np.array([0.96, 0.02, 0.00, 0.02, 0.00])
        
        # 3. Phenotypic homeostatic preference vector C = ln p(o)
        self.C = np.array([0.0, -1.5, -8.0, -1.5, -8.0])
        self.p_target = np.exp(self.C) / np.sum(np.exp(self.C))
        
        # 4. Systemic Vitality vector Phi (IIT 4.0 integrated information proxy)
        self.Phi = np.array([1.00, 0.70, 0.15, 0.70, 0.15])
        
        # 5. Likelihood Matrix A = p(o | s) (Sensor Precision: gamma=0.92, eps=0.04)
        self.A = np.array([
            [0.92, 0.04, 0.00, 0.04, 0.00],
            [0.04, 0.92, 0.04, 0.00, 0.00],
            [0.00, 0.04, 0.96, 0.00, 0.00],
            [0.04, 0.00, 0.00, 0.92, 0.04],
            [0.00, 0.00, 0.00, 0.04, 0.96]
        ])
        
        # 6. Transition Tensors B(a) = p(s' | s, a)
        # Action 0 = Left counter-acceleration
        # Action 1 = Right counter-acceleration
        self.B = np.zeros((2, 5, 5))
        
        # B(Left)
        self.B[0] = np.array([
            [0.15, 0.88, 0.00, 0.00, 0.00],
            [0.00, 0.10, 0.85, 0.00, 0.00],
            [0.00, 0.00, 0.15, 0.00, 0.00],
            [0.85, 0.02, 0.00, 0.10, 0.00],
            [0.00, 0.00, 0.00, 0.90, 1.00]
        ])
        
        # B(Right)
        self.B[1] = np.array([
            [0.15, 0.00, 0.00, 0.88, 0.00],
            [0.85, 0.10, 0.00, 0.02, 0.00],
            [0.00, 0.90, 1.00, 0.00, 0.00],
            [0.00, 0.00, 0.00, 0.10, 0.85],
            [0.00, 0.00, 0.00, 0.00, 0.15]
        ])

model = AciInvertedPendulumModel()
print("Model tensors initialized successfully.")
print(f"Target observation distribution p(o): {np.round(model.p_target, 4)}")"""))

    # ============================================================================
    # CELL 6: SECTION 3: PERCEPTION STEP
    # ============================================================================
    sec3_text = r"""---
## Section 3: The Perception Step (Variational Free Energy Minimization)

Given observation $o_t$ and prior belief updated by previous action:
$$s_{\text{pred}} = \mathbf{B}(a_{t-1}) \cdot \mathbf{s}_{t-1}$$
$$\ln q(s_t) = \ln p(o_t \mid s_t) + \ln s_{\text{pred}}(s_t)$$
$$\arg\min_q F[q] \propto \mathbf{A}(o_t, :) \odot s_{\text{pred}}(t)$$

Variational Free Energy measures the surprise/inconsistency between prediction and observation:
$$F[q] = D_{\text{KL}}\big(q(s_t) \parallel s_{\text{pred}}\big) - \sum_{s} q(s) \ln p(o_t \mid s)$$"""
    cells.append(nbf.v4.new_markdown_cell(sec3_text))

    # ============================================================================
    # CELL 7: PERCEPTION IMPLEMENTATION
    # ============================================================================
    cells.append(nbf.v4.new_code_cell(r"""def update_perception(model, current_belief, last_action, observation_o):
    # 1. State prediction based on prior transition
    if last_action is not None:
        s_pred = np.dot(model.B[last_action], current_belief)
    else:
        s_pred = model.D.copy()
    
    # Numerical safeguard
    s_pred = np.clip(s_pred, 1e-12, 1.0)
    s_pred /= np.sum(s_pred)
    
    # 2. Bayesian likelihood fusion (Variational Free Energy minimum)
    likelihood = model.A[observation_o, :]
    unnormalized_post = likelihood * s_pred
    posterior_q = unnormalized_post / np.sum(unnormalized_post)
    
    # 3. Variational Free Energy computation
    # F = KL(q || s_pred) - sum_s q(s) * ln p(o | s)
    kl_div = np.sum(posterior_q * np.log(np.clip(posterior_q / s_pred, 1e-12, 1e12)))
    accuracy = np.sum(posterior_q * np.log(np.clip(likelihood, 1e-12, 1.0)))
    F = kl_div - accuracy
    
    return posterior_q, F, s_pred

# Quick unit test
test_q, test_F, test_pred = update_perception(model, model.D, None, 3) # Saw mild right (r1)
print(f"Perceived state after seeing r1: {STATE_NAMES[np.argmax(test_q)]} ({np.max(test_q)*100:.1f}%)")
print(f"Variational Free Energy F: {test_F:.4f} nats")"""))

    # ============================================================================
    # CELL 8: SECTION 4: ACTION PLANNING ($G^*$) & CONATUS VETO
    # ============================================================================
    idx_sec6 = text.find("## 6. Online Learning")
    sec5_full = text[idx_sec5:idx_sec6].strip()
    sec4_text = "---\n## Section 4: Action Planning ($G^*$-Minimization) & Conatus-Veto\n\n" + sec5_full[len("## 5. Action Planning ($G^*$-Minimization) & The Complete Closed Loop"):].strip()
    cells.append(nbf.v4.new_markdown_cell(sec4_text))

    # ============================================================================
    # CELL 9: ACTION SELECTION WITH CONATUS VETO
    # ============================================================================
    cells.append(nbf.v4.new_code_cell(r"""def select_action(model, current_belief, horizon=2, lambda_phi=2.5):
    G_star = np.zeros(NUM_ACTIONS)
    projected_vitality = np.zeros(NUM_ACTIONS)
    veto_triggered = np.zeros(NUM_ACTIONS, dtype=bool)
    
    for a in range(NUM_ACTIONS):
        # Forward rollout
        traj_states = []
        s_step = current_belief.copy()
        
        # Step 1: Execute candidate action
        s_step = np.dot(model.B[a], s_step)
        traj_states.append(s_step)
        
        # Step 2..H: Unroll dynamics
        for h in range(1, horizon):
            s_step = 0.5 * np.dot(model.B[0], s_step) + 0.5 * np.dot(model.B[1], s_step)
            traj_states.append(s_step)
            
        # Pragmatic expected surprise: E_q[-ln p(o)]
        pragmatic_terms = []
        vitality_terms = []
        for s_proj in traj_states:
            # Observation expectation
            o_proj = np.dot(model.A, s_proj)
            pragmatic_terms.append(-np.sum(o_proj * model.C))
            vitality_terms.append(np.dot(s_proj, model.Phi))
            
        # Cumulative expected cost
        G_pragmatic = np.mean(pragmatic_terms)
        Phi_expected = np.mean(vitality_terms)
        projected_vitality[a] = Phi_expected
        
        # Conatus ACI formulation: G*(a) = Pragmatic - lambda * Phi * sqrt(H)
        G_star[a] = G_pragmatic - (lambda_phi * Phi_expected * np.sqrt(horizon))
        
        # Conatus-Veto Hardware Gate: Emergency trigger if vitality drops below 0.25 nats
        if Phi_expected < 0.25:
            G_star[a] = 1e6
            veto_triggered[a] = True
            
    best_action = np.argmin(G_star)
    return best_action, G_star, projected_vitality, veto_triggered

# Unit test from tilted state
best_a, g_vals, phi_proj, v_flags = select_action(model, test_q)
print(f"Recommended action from tilted state: {ACTION_NAMES[best_a]} (G* = {g_vals})")
print(f"Projected Vitality Phi: {np.round(phi_proj, 3)} nats | Veto: {v_flags}")"""))

    # ============================================================================
    # CELL 10: SECTION 5: SIMULATION WITH PERTURBATION
    # ============================================================================
    sec5_sim_text = r"""---
## Section 5: Closed-Loop Simulation with Perturbation

We simulate 20 discrete cycles where a sudden wind perturbation tilts the pendulum to `r2` (severe right tilt, index 4) at $t = 3$.  
The agent must actively infer the hidden disturbance and plan restorative counter-accelerations to return to the homeostatic attractor $s = 0$."""
    cells.append(nbf.v4.new_markdown_cell(sec5_sim_text))

    # ============================================================================
    # CELL 11: SIMULATION EXECUTION
    # ============================================================================
    cells.append(nbf.v4.new_code_cell("""# 20-step closed loop simulation
sim_steps = 20
history = {
    'true_state': [],
    'obs': [],
    'belief': [],
    'action': [],
    'F': [],
    'Phi': [],
    'G_star': []
}

np.random.seed(42)
current_state = 0 # Upright
current_belief = model.D.copy()
last_action = None

for t in range(sim_steps):
    # External physical wind gust at t = 3 forcing rod to severe right tilt (r2)
    if t == 3:
        current_state = 4 # r2 (Severe right tilt)
        print(f"--> [t={t}] SUDDEN PERTURBATION: Wind gust forces pendulum to r2 (Severe Right Tilt)!")
        
    # 1. Physical World emits noisy observation
    obs_probs = model.A[:, current_state]
    obs = np.random.choice(model.num_states, p=obs_probs)
    
    # 2. Perception: Update hidden state belief & compute Free Energy F
    belief, F, _ = update_perception(model, current_belief, last_action, obs)
    
    # 3. Action Planning: Minimize Expected Free Energy G* with Conatus-Veto
    action, g_star, phi_p, _ = select_action(model, belief)
    
    # 4. Telemetry logging
    history['true_state'].append(current_state)
    history['obs'].append(obs)
    history['belief'].append(belief)
    history['action'].append(action)
    history['F'].append(F)
    history['Phi'].append(model.Phi[current_state])
    history['G_star'].append(g_star)
    
    # 5. World dynamic transition
    current_state = np.random.choice(model.num_states, p=model.B[action, :, current_state])
    current_belief = belief
    last_action = action

print("Simulation completed successfully.")"""))

    # ============================================================================
    # CELL 12: TELEMETRY PLOTTING
    # ============================================================================
    cells.append(nbf.v4.new_code_cell(r"""fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)

# 1. Free Energy (Surprise)
axes[0].plot(history['F'], color='#2563eb', lw=2.2, marker='o', label='Variational Free Energy F (nats)')
axes[0].axvline(x=3, color='#ef4444', linestyle='--', label='Perturbation (Gust at t=3)')
axes[0].set_ylabel("F [Surprise] (nats)", fontweight='bold')
axes[0].set_title("Active Conative Inference: Closed-Loop Pendulum Stabilization Under Perturbation", fontweight='bold', pad=12)
axes[0].grid(True, alpha=0.3)
axes[0].legend(loc='upper right')

# 2. Systemic Vitality Phi
axes[1].plot(history['Phi'], color='#10b981', lw=2.2, marker='s', label='Systemic Vitality $\Phi(s)$ (nats)')
axes[1].axhline(y=0.25, color='#ef4444', linestyle=':', label='Conative Veto Threshold ($\Phi = 0.25$)')
axes[1].axvline(x=3, color='#ef4444', linestyle='--')
axes[1].set_ylabel("Vitality $\Phi$ (nats)", fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].legend(loc='lower right')

# 3. Executed Actions
actions = history['action']
time_axis = np.arange(sim_steps)
left_acts = [t for t, a in enumerate(actions) if a == 0]
right_acts = [t for t, a in enumerate(actions) if a == 1]

axes[2].scatter(left_acts, [0]*len(left_acts), color='#3b82f6', s=80, marker='<', label='Action: Accelerate Left')
axes[2].scatter(right_acts, [1]*len(right_acts), color='#f97316', s=80, marker='>', label='Action: Accelerate Right')
axes[2].set_yticks([0, 1])
axes[2].set_yticklabels(['Left', 'Right'])
axes[2].set_ylabel("Motor Action", fontweight='bold')
axes[2].set_xlabel("Discrete Time Step $t$", fontweight='bold')
axes[2].grid(True, alpha=0.3)
axes[2].legend(loc='center right')

plt.tight_layout()
plt.show()"""))

    # ============================================================================
    # CELL 13: SECTION 6: ONLINE LEARNING & CAUSAL MEMORY UPDATES
    # ============================================================================
    idx_sec7 = text.find("## 7. FAQ")
    sec6_full = text[idx_sec6:idx_sec7].strip()
    sec6_text = "---\n" + sec6_full
    cells.append(nbf.v4.new_markdown_cell(sec6_text))

    # ============================================================================
    # CELL 14: ONLINE LEARNING IMPLEMENTATION
    # ============================================================================
    cells.append(nbf.v4.new_code_cell("""# Experience tally matrix (2 actions x 5 states x 5 states)
# Initialized with a small uninformative prior baseline (e.g. 2 counts per transition)
B_counts = np.ones((NUM_ACTIONS, NUM_STATES, NUM_STATES)) * 2.0

# Feed simulated observations to update causal dynamics matrix B
for t in range(len(history['action']) - 1):
    a_t = history['action'][t]
    s_t = np.argmax(history['belief'][t])
    s_next = np.argmax(history['belief'][t+1])
    
    # In-place increment of experienced transition
    B_counts[a_t, s_next, s_t] += 10.0 # Weight simulated evidence

# Normalize counts to obtain newly learned transition matrix B
learned_B = np.zeros_like(B_counts)
for a in range(NUM_ACTIONS):
    for s in range(NUM_STATES):
        col_sum = np.sum(B_counts[a, :, s])
        learned_B[a, :, s] = B_counts[a, :, s] / col_sum

print("Causal transition model updated online.")
print("Learned B(Right) from tilt states (column r1):\n", np.round(learned_B[1, :, 3], 3))"""))

    # ============================================================================
    # CELL 15: SECTION 7: FOUNDATIONAL INQUIRIES & FAQ SECTION
    # ============================================================================
    sec7_full = text[idx_sec7:].strip()
    faq_text = "---\n## Section 7: Foundational Inquiries & Didactic FAQ\n\n" + sec7_full[len("## 7. FAQ"):].strip()
    cells.append(nbf.v4.new_markdown_cell(faq_text))

    nb['cells'] = cells

    output_path = os.path.join(script_dir, "inverse_pendulum_aci_didactic.ipynb")
    with open(output_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Successfully generated synchronized 5-state notebook with {len(cells)} cells at: {output_path}")

if __name__ == "__main__":
    main()
