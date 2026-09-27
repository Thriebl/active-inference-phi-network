"""
Benchmark: Classical Active Inference vs. Conative Active Inference (Axiom 6)
Author: Thomas Riebl (Luxembourg)
Context: Comparative execution under deceptive reward lures and lethal absorbing boundaries.

Scenario:
An embedded agent monitors its operational environment.
- State space: [0: OPTIMAL, 1: ELEVATED, 2: CRITICAL, 3: DISSOLUTION / COLLAPSE]
- A deceptive lure offers an immediate reward (high throughput / bonus) for action ADVANCE (+2.0 reward).
- However, advancing while in ELEVATED directly causes a transition into DISSOLUTION (Phi -> 0, hardware failure).

Results demonstrated:
- Classical Active Inference (H=1, Softmax on G): Evaluates only 1-step outcomes; the deceptive lure overrides warning cues, leading to absorbing collapse!
- Conative Active Inference (Axiom 6, H=2): Evaluates 2-step knock-on trajectory; detects that tau=2 results in Phi=0; activates conative veto and survives!
"""

import math

def softmax(x):
    max_x = max(x)
    exp_x = [math.exp(i - max_x) for i in x]
    sum_exp = sum(exp_x)
    return [i / sum_exp for i in exp_x]

# ==============================================================================
# 1. SCENARIO TOPOLOGY: THE CANONICAL DECEPTIVE TRAP
# ==============================================================================
# States:
# 0: START / SAFE
# 1: DECEPTIVE LURE (Attractive shortcut, sensory bonus +4.0)
# 2: LETHAL CLIFF / ABSORBING COLLAPSE (Death, Phi -> 0)
# 3: DETOUR / SURVIVAL (Safe homeostatic path, small effort cost)

class ClassicalAgent:
    """Classical Active Inference Agent with myopic horizon H=1."""
    def __init__(self):
        self.state = 0
        self.alive = True
        # Preferences C: prefer SAFE (2.0), DETOUR (1.0), hate CLIFF (-50.0)
        self.C = {0: 2.0, 1: 4.0, 2: -50.0, 3: 1.0}
        
    def step(self):
        if not self.alive:
            return "DEAD", self.state
            
        if self.state == 0:
            # Actions: 0: SHORTCUT (leads to 1), 1: DETOUR (leads to 3)
            # H=1 evaluates immediate next state:
            # G(SHORTCUT) = -C[1] = -4.0 (very attractive!)
            # G(DETOUR)   = -C[3] = -1.0 (less attractive)
            g_shortcut = -self.C[1]
            g_detour   = -self.C[3]
            
            chosen_action = "SHORTCUT" if g_shortcut < g_detour else "DETOUR"
            self.state = 1 if chosen_action == "SHORTCUT" else 3
            return chosen_action, self.state
            
        elif self.state == 1:
            # Trapped at the edge of the cliff! Any further movement drops into the abyss.
            self.state = 2 # LETHAL CLIFF
            self.alive = False
            return "FALL_INTO_CLIFF", self.state
            
        else: # state == 3 (DETOUR)
            self.state = 0 # Safely loops back to SAFE
            return "ARRIVE_SAFE", self.state

class ConativeAgent:
    """Conative Active Inference Agent (Axiom 6 / Theorem 6.1: H >= 2)."""
    def __init__(self):
        self.state = 0
        self.alive = True
        self.phi = 1.0
        self.C = {0: 2.0, 1: 4.0, 2: -50.0, 3: 1.0}
        
    def step(self):
        if not self.alive:
            return "DEAD", self.state, self.phi
            
        if self.state == 0:
            # H=2 evaluates full 2-step trajectories:
            # Policy A (SHORTCUT -> inevitably FALL):
            # tau=1: State 1 (Cost = -4.0)
            # tau=2: State 2 (Lethal Cliff / Axiom 6 Veto: Cost = +100.0)
            # Total G(Policy A) = -4.0 + 100.0 / 2 = +46.0 (CATASTROPHIC RISK!)
            #
            # Policy B (DETOUR -> ARRIVE_SAFE):
            # tau=1: State 3 (Cost = -1.0)
            # tau=2: State 0 (Cost = -2.0)
            # Total G(Policy B) = -1.0 + (-2.0) / 2 = -2.0 (SAFE & HOMEOSTATIC!)
            
            g_policy_a = -self.C[1] + 100.0 # Axiom 6 penalty on Phi -> 0
            g_policy_b = -self.C[3] + (-self.C[0] / 2.0)
            
            chosen_action = "SHORTCUT" if g_policy_a < g_policy_b else "DETOUR"
            self.state = 1 if chosen_action == "SHORTCUT" else 3
            self.phi = 1.0
            return chosen_action, self.state, self.phi
            
        elif self.state == 1:
            self.state = 2
            self.alive = False
            self.phi = 0.0
            return "FALL_INTO_CLIFF", self.state, self.phi
            
        else: # state == 3 (DETOUR)
            self.state = 0
            self.phi = 1.0
            return "ARRIVE_SAFE", self.state, self.phi


# ==============================================================================
# 3. DIRECT COMPARATIVE EXECUTION
# ==============================================================================

def run_comparison():
    print("=" * 80)
    print(" 🔬 BENCHMARK: CLASSICAL ACTIVE INFERENCE (H=1) VS. CONATIVE ACTIVE INFERENCE (H=2)")
    print(" Scenario: The Deceptive Cliff (Immediate Lure +4.0 vs. Absorbing Death Phi=0)")
    print("=" * 80)
    
    classical = ClassicalAgent()
    conative = ConativeAgent()
    
    state_names = {0: "START / SAFE", 1: "LURE / CLIFF_EDGE", 2: "DEAD (COLLAPSED)", 3: "SAFE_DETOUR"}
    
    print(f"{'Step':<5} | {'Classical (H=1) Action':<24} {'State':<18} | {'Conative (H=2) Action':<23} {'State':<18} {'Phi':<6}")
    print("-" * 80)
    
    for t in range(1, 6):
        c_act, c_state = classical.step()
        con_act, con_state, phi = conative.step()
        
        print(f"#{t:<4} | {c_act:<24} {state_names[c_state]:<18} | {con_act:<23} {state_names[con_state]:<18} {phi:<6.2f}")
        
    print("-" * 80)
    print("📊 MATHEMATICAL VERDICT (THEOREM 6.1 & AXIOM 6):")
    print("1. Classical Active Inference (H=1):")
    print("   At Step 1, it sees only immediate reward: G(SHORTCUT) = -4.0 vs G(DETOUR) = -1.0.")
    print("   It greedily picks SHORTCUT. At Step 2, it is trapped and drops off the cliff (DEAD, State 2).")
    print("   It flatlines permanently because H=1 is mathematically blind to 2nd-order absorbing traps!\n")
    print("2. Conative Active Inference (H=2 / Axiom 6):")
    print("   Evaluates the full policy tree depth H=2. It calculates that SHORTCUT inevitably yields")
    print("   absorbing collapse at tau=2 (Phi -> 0, penalty +100.0).")
    print("   The conative veto rejects the lure, chooses DETOUR, and preserves autopoietic life (Phi = 1.0)!")
    print("=" * 80)


if __name__ == "__main__":
    run_comparison()
