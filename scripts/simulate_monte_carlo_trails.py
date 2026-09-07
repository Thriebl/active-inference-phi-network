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
    'font.sans-serif': ['Inter', 'DejaVu Sans', 'Arial'],
    'axes.edgecolor': '#cbd5e1',
    'axes.linewidth': 1.2,
    'grid.color': '#f1f5f9',
    'grid.linestyle': '--'
})

# Parameters for Monte Carlo Trails
N_TRAILS = 60         # Number of Monte Carlo trails (Pfadfinder)
HORIZON = 25          # Temporal depth (H = 25 time steps into the counterfactual future)
TARGET_STATE = 0.0    # Desired homeostatic equilibrium (Attractor)
START_STATE = 3.5     # Perturbed current state at t=0
NOISE_STD = 0.35      # Environmental stochasticity
GAMMA = 2.5           # Precision (inverse temperature parameter)

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
        # Next state transition
        state = state + action + noise
        trail_states.append(state)
        # Expected Free Energy accumulation (quadratic divergence from preferred state)
        trail_cost += (state - TARGET_STATE)**2
        
    trails[i, :] = trail_states
    free_energies[i] = trail_cost

# Softmax weighting over Expected Free Energy: P(pi) ~ exp(-gamma * G)
# Invert cost so lower G has higher probability
weights = np.exp(-GAMMA * (free_energies - np.min(free_energies)) / (np.max(free_energies) - np.min(free_energies) + 1e-6))
weights /= np.sum(weights)

# Select the winning trail (the one with highest precision-weighted likelihood)
best_trail_idx = np.argmin(free_energies)
best_trail = trails[best_trail_idx, :]

# CREATE FIGURE
fig = plt.figure(figsize=(14, 7), dpi=300)
gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1], height_ratios=[1, 1], hspace=0.35, wspace=0.25)

# --- PANEL 1: THE MONTE CARLO TRAIL BUNDLE (PHASENRAUM-TRAJEKTORIEN) ---
ax1 = fig.add_subplot(gs[:, 0])

# Time axis
time_steps = np.arange(HORIZON)

# Plot all candidate trails with transparency
for i in range(N_TRAILS):
    ax1.plot(time_steps, trails[i, :], color='#94a3b8', alpha=0.35, linewidth=1.0, zorder=1)

# Plot Mean trajectory and confidence interval ribbon (mean +/- std)
mean_traj = np.mean(trails, axis=0)
std_traj = np.std(trails, axis=0)
ax1.fill_between(time_steps, mean_traj - std_traj, mean_traj + std_traj, color='#38bdf8', alpha=0.2, label='68% Ensemble-Band (Trials)', zorder=2)

# Plot Target Attractor (Homeostasis)
ax1.axhline(TARGET_STATE, color='#10b981', linestyle='--', linewidth=2.0, label='Homöostatisches Ziel s* (Attraktor)', zorder=3)

# Plot Best/Selected Trail (Optimal Policy)
ax1.plot(time_steps, best_trail, color='#2563eb', linewidth=3.0, label='Selektierter Trail π* (Minimale Freie Energie)', zorder=4)

# Start node
ax1.scatter([0], [START_STATE], color='#ef4444', s=120, zorder=5, label='Gegenwärtiger Zustand s₀ (t=0 im Jetzt)')

ax1.set_title('A: Die Schar der Monte-Carlo-Trails im Jetzt (t = 0)', fontsize=13, fontweight='bold', pad=12, color='#0f172a')
ax1.set_xlabel('Counterfactualer Zeithorizont τ (Inferenz-Schritte in die Zukunft)', fontsize=10, labelpad=8)
ax1.set_ylabel('Systemzustand s(τ) (Phasenraum-Koordinate)', fontsize=10, labelpad=8)
ax1.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9)
ax1.set_xlim(-0.5, HORIZON - 0.5)

# --- PANEL 2: DISTRIBUTION OF EXPECTED FREE ENERGY G(π) ---
ax2 = fig.add_subplot(gs[0, 1])
sns.histplot(free_energies, kde=True, color='#6366f1', ax=ax2, bins=15, alpha=0.6, edgecolor='white')
ax2.axvline(free_energies[best_trail_idx], color='#2563eb', linestyle='--', linewidth=2.0, label=f'Bestes G = {free_energies[best_trail_idx]:.2f}')
ax2.set_title('B: Verteilung der Erwarteten Freien Energie G(π)', fontsize=11, fontweight='bold', pad=8, color='#0f172a')
ax2.set_xlabel('Erwartete Freie Energie G (niedriger = besser)', fontsize=9)
ax2.set_ylabel('Dichte / Häufigkeit der Trails', fontsize=9)
ax2.legend(loc='upper right', fontsize=8.5)

# --- PANEL 3: SOFTMAX-SELECTION PROBABILITIES ---
ax3 = fig.add_subplot(gs[1, 1])
sorted_indices = np.argsort(free_energies)
top_n = 15
sorted_weights = weights[sorted_indices][:top_n]
bar_colors = ['#2563eb'] + ['#94a3b8'] * (top_n - 1)

ax3.bar(range(top_n), sorted_weights, color=bar_colors, edgecolor='none', width=0.7)
ax3.set_title('C: Softmax-Wahrscheinlichkeiten P(π) ~ σ(-γG)', fontsize=11, fontweight='bold', pad=8, color='#0f172a')
ax3.set_xlabel('Rangfolge der Top-15 Trails (geordnet nach Güte)', fontsize=9)
ax3.set_ylabel('Auswahl-Wahrscheinlichkeit P(π)', fontsize=9)
ax3.set_xticks(range(top_n))
ax3.set_xticklabels([f'#{i+1}' for i in range(top_n)], fontsize=8)

# Figure Title & Annotations
fig.suptitle('Monte Carlo Trails & Active Inference: Zukunfts-Exploration im ewigen Jetzt', fontsize=15, fontweight='bold', y=0.98, color='#0f172a')

# Save paths
out_dir = '/home/thr/Documents/active-inference-phi-network/images'
os.makedirs(out_dir, exist_ok=True)
out_png = os.path.join(out_dir, 'monte_carlo_trails_simulation.png')
vault_dir = '/home/thr/Documents/ThRNotes/Alle_Braindumps_PDF'
vault_png = os.path.join(vault_dir, 'monte_carlo_trails_simulation.png')

plt.savefig(out_png, dpi=300, bbox_inches='tight')
plt.savefig(vault_png, dpi=300, bbox_inches='tight')
plt.close()

print(f"SUCCESS: Plot generated and saved to:\n  - {out_png}\n  - {vault_png}")
