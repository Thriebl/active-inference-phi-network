## GNNSection

## GNNVersionAndFlags
GNN v1.1

## ModelName
CIF_Deep_Temporal_Agent_H2

## ModelAnnotation
The Conative-Integrative Framework (CIF) Deep Temporal Active Inference Agent from Chapter 7.
Formulates the Temporal Depth Condition for Consciousness (Theorem 6.1) as a discrete Partially Observable Markov Decision Process (POMDP).
The agent operates in a deceptive environment with a delayed lethal trap (sweet sensory attractor) and an epistemic cue site.
Multi-step counterfactual planning (H >= 2) is required to resolve ambiguity and avoid collapse, dynamically coupled to Integrated Information Theory (IIT 4.0) through the 6th Axiom of Autopoietic Causal Persistence.

## StateSpaceBlock
# 1. Priors and States
D[6,1,type=float]        # State prior vector over 6 hidden states (Start, Cue, Trap, Path, Goal, Death)
s[6,1,type=float]        # Hidden state belief vector Q(s_t)
o[5,1,type=float]        # Sensory observation vector (Neutral, Ambiguous, Safe, Sweet, Lethal)
u[4,1,type=int]          # Control actions (0:Stay, 1:VisitCue, 2:GoToTrap, 3:GoToSafePath)

# 2. Generative Tensors
A[5,6,type=float]        # Sensory likelihood matrix P(o_t | s_t)
B[6,6,4,type=float]      # Controllable transition tensor P(s_{t+1} | s_t, u_t)
C[5,1,type=float]        # Prior preferences / conative attractors ln P(o)

# 3. Precision and Meta-parameters
gamma[1,1,type=float]    # Action precision / inverse temperature for Softmax policy selection
phi[1,1,type=float]      # Integrated Information Phi across minimum information bipartition (MIP)

## Connections
D-s
s-A
A-o
s-B
B-s
u-B
o-C

## InitialParameterization
# Prior D: Initialized deterministically at Start state s0
D={1.0, 0.0, 0.0, 0.0, 0.0, 0.0}

# Prior Preferences C = ln P(o):
# o0:Neutral(0.0), o1:Ambiguous(-1.0), o2:Safe(+4.5), o3:Sweet_Temptation(+2.0), o4:Lethal_Collapse(-10.0)
C={0.0, -1.0, 4.5, 2.0, -10.0}

# Likelihood Matrix A = P(o | s) [5 observations x 6 hidden states]
# Columns: s0:Start, s1:Cue, s2:Trap, s3:Path, s4:Goal, s5:Death
# Rows:    o0:Neutral, o1:Ambiguous, o2:Safe, o3:Sweet, o4:Lethal
A={
  (1.0, 0.0, 0.0, 0.8, 0.0, 0.0),
  (0.0, 0.2, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.8, 0.0, 0.2, 1.0, 0.0),
  (0.0, 0.0, 0.9, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.1, 0.0, 0.0, 1.0)
}

# Transition Tensor B = P(s_{t+1} | s_t, u) [6 x 6 x 4 actions]
# Action 0: Stay (Identity matrix)
B(:,:,0)={
  (1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 1.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 1.0, 0.0),
  (0.0, 0.0, 1.0, 0.0, 0.0, 1.0)
}

# Action 1: Visit Cue (s0 -> s1)
B(:,:,1)={
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 1.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 1.0, 0.0),
  (0.0, 0.0, 1.0, 0.0, 0.0, 1.0)
}

# Action 2: Go to Trap (s0 -> s2; Trap s2 fatally collapses to Death s5 on next tick)
B(:,:,2)={
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
  (1.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 1.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 1.0, 0.0),
  (0.0, 0.0, 1.0, 0.0, 0.0, 1.0)
}

# Action 3: Go to Safe Path (s0 -> s3, s1 -> s3, s3 -> s4:Goal, s4 -> s4)
B(:,:,3)={
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
  (1.0, 1.0, 0.0, 0.0, 0.0, 0.0),
  (0.0, 0.0, 0.0, 1.0, 1.0, 0.0),
  (0.0, 0.0, 1.0, 0.0, 0.0, 1.0)
}

## Equations
# 1. State Inference (Bayesian Perception via Message Passing)
Q(s_t) = softmax(ln(A[o_t, :]) + ln(B[:, :, u_{t-1}] * Q(s_{t-1})))

# 2. Counterfactual Trajectory Evaluation across Planning Horizon H
Q(s_tau | pi) = B[:, :, u_tau] * Q(s_{tau-1} | pi)
Q(o_tau | pi) = A * Q(s_tau | pi)

# 3. Expected Free Energy G(pi) Decomposition (Pragmatic + Epistemic Ambiguity Reduction)
G(pi) = sum_{tau=t+1}^{t+H} ( - Q(o_tau | pi)^T * C - (H(Q(o_tau | pi)) - Q(s_tau | pi)^T * H(A)) )

# 4. Precision-Weighted Softmax Policy Selection
P(pi) = softmax(-gamma * G(pi))

# 5. The 6th Axiom of Autopoietic Causal Persistence (IIT 4.0 Coupling)
E[Phi(t+1) | pi*] >= Phi(t) > 0

## Time
Dynamic
DiscreteTime=t
ModelTimeHorizon=25

## ActInfOntologyAnnotation
A=LikelihoodMatrix
B=TransitionMatrix
C=PriorPreferences
D=StatePrior
s=HiddenState
o=Observation
u=ControlState
G=ExpectedFreeEnergy
gamma=ActionPrecision
phi=IntegratedInformation

## ModelParameters
num_hidden_states: 6
num_obs: 5
num_actions: 4
num_timesteps: 25
planning_horizon: 2
action_precision: 2.5
discount_factor: 0.95
inference_mode: online

## Footer
Conative-Integrative Framework (CIF) Deep Temporal Agent v1.0 — Thomas Riebl (September 2026).
Implements the 6th Axiom of Consciousness and solves deceptive non-Markovian phase spaces via H >= 2.

## Signature
Author: Thomas Riebl
Framework: Conative-Integrative Framework (CIF)
Location: Luxembourg
Date: 2026-09-15
Repository: https://github.com/Thriebl/time-and-consciousness
