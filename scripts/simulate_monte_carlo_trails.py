#!/usr/bin/env python3
"""
simulate_monte_carlo_trails.py
Simulates a stochastic ensemble of Monte Carlo trails under Active Inference
in the Specious Present (t = 0), evaluating Expected Free Energy G(pi)
and precision-weighted Softmax selection P(pi).
Authored for Thomas Riebl.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set random seed for reproducibility
np.random.seed(42)

# Styling configuration with seaborn and matplotlib
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Inter', 'DejaVu Sans', 'Arial', 'Helvetica'],
    'axes.edgecolor': '#cbd5e1',
    'axes.linewidth': 1.2,
    'grid.color': '#f1f5f9',
    'grid.linestyle': '--'
})

# Parameters for Monte Carlo Trails
N_TRAILS     = 60         # Number of Monte Carlo trails (pathfinders)
HORIZON      = 25         # Temporal depth (H = 25 time steps into the counterfactual future)
TARGET_STATE = 0.0        # Desired homeostatic equilibrium (Attractor s*)
START_STATE  = 3.5        # Perturbed current state at t=0 (s0)
NOISE_STD    = 0.35       # Environmental stochasticity (sensory/dynamic noise sigma)
GAMMA        = 2.5        # Action precision gamma (inverse temperature parameter)

# Generate stochastic trails
# An active inference agent evaluates actions that pull towards the target, perturbed by noise
trails = np.zeros((N_TRAILS, HORIZON))
free_energies = np.zeros(N_TRAILS)

for i in range(N_TRAILS):
    state = START_STATE
    trail_states = [state]
    trail_cost = 0.0
    
    # Stochastic control strength varies per policy sample
    control_intent = np.random.uniform(0.1, 0.45)
    
    for t in range(1, HORIZON):
        # Action intent (negative gradient towards homeostatic target)
        action = -control_intent * (state - TARGET_STATE)
        # Environmental noise / sensory fluctuation
        noise = np.random.normal(0, NOISE_STD)
        # Next state transition: s_{t+1} = s_t + action + noise
        state = state + action + noise
        trail_states.append(state)
        # Expected Free Energy accumulation (quadratic divergence from preferred target)
        trail_cost += (state - TARGET_STATE)**2
        
    trails[i, :] = trail_states
    free_energies[i] = trail_cost

# Softmax weighting over Expected Free Energy: P(pi) ~ exp(-gamma * G_norm)
norm_g = (free_energies - np.min(free_energies)) / (np.max(free_energies) - np.min(free_energies) + 1e-6)
weights = np.exp(-GAMMA * norm_g)
weights /= np.sum(weights)

# Select the winning trail (the one with highest precision-weighted likelihood / lowest G)
best_trail_idx = np.argmin(free_energies)
best_trail = trails[best_trail_idx, :]

# CREATE FIGURE
fig = plt.figure(figsize=(15, 7.5), dpi=300)
gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1], height_ratios=[1, 1], hspace=0.35, wspace=0.25)

# --- PANEL 1: THE MONTE CARLO TRAIL BUNDLE (PHASE-SPACE TRAJECTORIES) ---
ax1 = fig.add_subplot(gs[:, 0])

# Time axis
time_steps = np.arange(HORIZON)

# Plot all candidate trails with transparency
for i in range(N_TRAILS):
    ax1.plot(time_steps, trails[i, :], color='#94a3b8', alpha=0.35, linewidth=1.0, zorder=1)

# Plot Mean trajectory and confidence interval ribbon (mean +/- std)
mean_traj = np.mean(trails, axis=0)
std_traj = np.std(trails, axis=0)
ax1.fill_between(time_steps, mean_traj - std_traj, mean_traj + std_traj, color='#38bdf8', alpha=0.22, 
                 label='68% Ensemble Confidence Band (Trials)', zorder=2)

# Plot Target Attractor (Homeostasis)
ax1.axhline(TARGET_STATE, color='#10b981', linestyle='--', linewidth=2.0, 
            label='Homeostatic Target s* (Attractor)', zorder=3)

# Plot Best/Selected Trail (Optimal Policy)
ax1.plot(time_steps, best_trail, color='#2563eb', linewidth=3.2, 
         label=f'Selected Trail π* (Min. Expected Free Energy G={free_energies[best_trail_idx]:.2f})', zorder=4)

# Start node
ax1.scatter([0], [START_STATE], color='#ef4444', s=130, zorder=5, 
            label='Current State s₀ (t = 0 in Eternal Present)', edgecolors='white', linewidth=1.5)

ax1.set_title('A: The Monte Carlo Trail Bundle in the Present (t = 0)', fontsize=13, fontweight='bold', pad=12, color='#0f172a')
ax1.set_xlabel('Counterfactual Time Horizon τ (Inference Steps into Future)', fontsize=10.5, labelpad=8)
ax1.set_ylabel('System State s(τ) (Phase-Space Coordinate)', fontsize=10.5, labelpad=8)
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.92, fontsize=9.5)
ax1.set_xlim(-0.5, HORIZON - 0.5)

# --- PANEL 2: DISTRIBUTION OF EXPECTED FREE ENERGY G(π) ---
ax2 = fig.add_subplot(gs[0, 1])
sns.histplot(free_energies, kde=True, color='#6366f1', ax=ax2, bins=14, alpha=0.6, edgecolor='white')
ax2.axvline(free_energies[best_trail_idx], color='#2563eb', linestyle='--', linewidth=2.0, 
            label=f'Optimal G = {free_energies[best_trail_idx]:.2f}')
ax2.set_title('B: Distribution of Expected Free Energy G(π)', fontsize=11.5, fontweight='bold', pad=8, color='#0f172a')
ax2.set_xlabel('Expected Free Energy G (Lower = More Adaptive)', fontsize=9.5)
ax2.set_ylabel('Density / Trail Count', fontsize=9.5)
ax2.legend(loc='upper right', fontsize=9)

# --- PANEL 3: SOFTMAX-SELECTION PROBABILITIES ---
ax3 = fig.add_subplot(gs[1, 1])
sorted_indices = np.argsort(free_energies)
top_n = 12
sorted_weights = weights[sorted_indices][:top_n]
bar_colors = ['#2563eb'] + ['#94a3b8'] * (top_n - 1)

ax3.bar(range(top_n), sorted_weights, color=bar_colors, edgecolor='none', width=0.65)
ax3.set_title('C: Softmax Probabilities P(π) ~ σ(-γG)', fontsize=11.5, fontweight='bold', pad=8, color='#0f172a')
ax3.set_xlabel('Rank of Top-12 Trails (Ordered by Fitness)', fontsize=9.5)
ax3.set_ylabel('Selection Probability P(π)', fontsize=9.5)
ax3.set_xticks(range(top_n))
ax3.set_xticklabels([f'#{i+1}' for i in range(top_n)], fontsize=8.5)

# Figure Title & Annotations
fig.suptitle('Monte Carlo Trails & Active Inference: Exploring Counterfactual Futures in the Eternal Present', 
             fontsize=14.5, fontweight='bold', y=0.98, color='#0f172a')

# Save paths
out_dir = '/home/thr/Documents/active-inference-phi-network/images'
os.makedirs(out_dir, exist_ok=True)
out_png = os.path.join(out_dir, 'monte_carlo_trails_simulation.png')
vault_dir = '/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF'
os.makedirs(vault_dir, exist_ok=True)
vault_png = os.path.join(vault_dir, 'monte_carlo_trails_simulation.png')

plt.savefig(out_png, dpi=300, bbox_inches='tight')
plt.savefig(vault_png, dpi=300, bbox_inches='tight')
plt.close()

print(f"SUCCESS: English publication plot generated and saved to:\n  - {out_png}\n  - {vault_png}")
