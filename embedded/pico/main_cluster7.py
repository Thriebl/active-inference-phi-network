"""
7-Agent Conative Active Inference Cluster for Raspberry Pi Pico 2 / 2H (RP2350)
Author: Thomas Riebl (Luxembourg)
Architecture:
- 7 Networked Conative Agents running in parallel on bare-metal RP2350
- Dual External ADC Sensor Inflow:
    * ADC(0) / GP26 (Pin 31): External Sensor Alpha (e.g. Threat / Light / Perturbation)
    * ADC(1) / GP27 (Pin 32): External Sensor Beta  (e.g. Gradient / Pressure / Proximity)
- Communication Topology: Ring lattice with cross-chord hubs (Chordal Ring graph)
- Collective Information Integration: Computes local Phi_i and collective Phi_net
- Physical Markov Blanket Actuation:
    * Onboard LED (GP25 via PWM): Modulates with Collective Phi_net heartbeat
    * GP16: Cluster Consensus / Stability Indicator
    * GP17: Collective Hazard / Emergency Evasion Drive
"""

import machine
import time
import math

# Cross-platform compatibility (MicroPython & Desktop CPython)
sleep_ms = getattr(time, "sleep_ms", lambda ms: time.sleep(ms / 1000.0))

# ==============================================================================
# 1. HARDWARE GPIO & DUAL EXTERNAL ADC SETUP
# ==============================================================================

# Onboard LED (Collective Vitality & Pulse Display)
try:
    led_pin = machine.Pin("LED", machine.Pin.OUT)
except Exception:
    led_pin = machine.Pin(25, machine.Pin.OUT)

led_pwm = machine.PWM(led_pin)
led_pwm.freq(1000)

# Dual External ADC Sensors (Markov Blanket Inflow)
adc_alpha = machine.ADC(26)  # GP26 (Pin 31) -> External Sensor Alpha
adc_beta  = machine.ADC(27)  # GP27 (Pin 32) -> External Sensor Beta

# Internal Core Temp as background reference
try:
    temp_sensor = machine.ADC(4)
except Exception:
    temp_sensor = None

# External Actuators (Markov Blanket Outflow)
actuator_consensus = machine.Pin(16, machine.Pin.OUT) # GP16: High when Cluster is in Homeostatic Harmony
actuator_hazard    = machine.Pin(17, machine.Pin.OUT) # GP17: High when Cluster detects Collective Danger

def read_adc_normalized(adc):
    """Reads 16-bit ADC and returns normalized float [0.0, 1.0]."""
    raw = adc.read_u16()
    return round(raw / 65535.0, 3)

def read_temperature_celsius():
    if not temp_sensor:
        return 25.0
    raw = temp_sensor.read_u16()
    voltage = raw * 3.3 / 65535.0
    return round(27.0 - (voltage - 0.706) / 0.001721, 1)

# ==============================================================================
# 2. 7-AGENT NETWORK TOPOLOGY & CONATIVE ENGINE
# ==============================================================================

# 7-Node Chordal Ring Topology:
# Node 0: Boundary Node Alpha (directly senses ADC0)
# Node 6: Boundary Node Beta  (directly senses ADC1)
# Nodes 1, 2, 3, 4, 5: Mediating & Integrating Network Nodes
NEIGHBORS = {
    0: [1, 6],       # Coupled to Node 1 and Node 6
    1: [0, 2, 4],    # Cross-link to Node 4
    2: [1, 3],
    3: [2, 4],       # Central Pacemaker / Median node
    4: [1, 3, 5],    # Cross-link to Node 1
    5: [4, 6],
    6: [5, 0]        # Coupled to Node 5 and Node 0
}

class ClusterConativeAgent:
    """Individual Active Conative Agent within the 7-node cluster."""
    def __init__(self, node_id, temporal_depth=2):
        self.id = node_id
        self.H = temporal_depth
        
        # State: 0: OPTIMAL, 1: STRESSED, 2: CRITICAL, 3: DISSOLVED
        self.state = 0
        self.phi_local = 1.0
        
        # Actions: 0: REST/STABILIZE, 1: ACTIVE_COMM, 2: EVADE/DEFEND
        self.action = 0
        self.action_names = ["REST", "COMM", "EVADE"]
        
        # Prior Preferences C = ln P(s*)
        self.C = [2.5, 0.0, -3.0, -20.0]

    def transition(self, s, a, neighbor_distress):
        """Transition dynamic B(a) incorporating physical and social distress."""
        if s == 3: return 3 # Absorbing trap
        
        # Base transition from action
        if a == 0:   # REST cools down / recovers
            next_s = max(0, s - 1)
        elif a == 1: # COMM consumes energy / maintains sync
            next_s = s
        else:        # EVADE retreats from hazard
            next_s = max(0, s - 1)
            
        # Social contagion / peer effect: if neighbors are stressed, state elevates
        if neighbor_distress > 0.6 and next_s < 2:
            next_s = min(2, next_s + 1)
            
        return next_s

    def evaluate_expected_free_energy(self, policy, neighbor_distress):
        curr_s = self.state
        total_G = 0.0
        
        for step, a in enumerate(policy):
            next_s = self.transition(curr_s, a, neighbor_distress)
            pragmatic_cost = -self.C[next_s]
            
            # Axiom 6 Autopoietic Veto: Dissolution carries massive penalty
            if next_s == 3:
                pragmatic_cost += 80.0
                
            total_G += pragmatic_cost / (step + 1)
            curr_s = next_s
            
        return total_G

    def step(self, physical_signal, neighbor_distress):
        """
        Updates belief and selects conative action using H=2 lookahead.
        """
        # 1. Update state based on local sensor input and neighbor messages
        if physical_signal > 0.85:
            self.state = 2 # CRITICAL
            self.phi_local = max(0.1, self.phi_local - 0.25)
        elif physical_signal > 0.65 or neighbor_distress > 0.5:
            self.state = 1 # STRESSED
            self.phi_local = max(0.4, self.phi_local - 0.08)
        else:
            self.state = 0 # OPTIMAL
            self.phi_local = min(1.0, self.phi_local + 0.05)

        # 2. Conative Policy Selection (H=2 planning)
        best_a = 0
        min_G = float("inf")
        
        # Evaluate 2-step policies (3^2 = 9 policies)
        for a1 in [0, 1, 2]:
            for a2 in [0, 1, 2]:
                g = self.evaluate_expected_free_energy([a1, a2], neighbor_distress)
                if g < min_G:
                    min_G = g
                    best_a = a1

        self.action = best_a
        return self.state, self.action, self.phi_local

# ==============================================================================
# 3. COLLECTIVE NETWORK CLUSTER MANAGER
# ==============================================================================

class ConativeCluster7:
    """Manages the 7-agent cluster, topological coupling, and Collective Phi."""
    def __init__(self):
        self.agents = [ClusterConativeAgent(i, temporal_depth=2) for i in range(7)]
        self.phi_collective = 1.0

    def compute_collective_phi(self):
        """
        Computes the Integrated Information (Phi_net) across the 7-node network.
        Approximated as the minimum information bipartition integration:
        High when all nodes are coordinated; drops if nodes desynchronize or collapse.
        """
        local_phis = [a.phi_local for a in self.agents]
        mean_phi = sum(local_phis) / 7.0
        
        # Variance of states measures network discord / fragmentation
        states = [a.state for a in self.agents]
        state_variance = sum((s - (sum(states)/7.0))**2 for s in states) / 7.0
        
        # Coherence term: high when agents are in synchrony, penalizes fragmentation
        coherence = math.exp(-state_variance * 0.8)
        self.phi_collective = round(mean_phi * coherence, 3)
        return self.phi_collective

    def cycle(self, val_alpha, val_beta):
        """Executes one synchronized active inference cycle across all 7 agents."""
        # 1. Distribute physical ADC inputs:
        # Node 0 receives direct ADC Alpha (GP26)
        # Node 6 receives direct ADC Beta (GP27)
        # Internal nodes (1-5) experience baseline ambient sensor field
        sensor_inputs = [
            val_alpha,                    # Node 0
            val_alpha * 0.5,              # Node 1
            0.1,                          # Node 2
            0.1,                          # Node 3 (Central Pacemaker)
            0.1,                          # Node 4
            val_beta * 0.5,               # Node 5
            val_beta                      # Node 6
        ]

        # 2. Gather neighbor distress signals from previous step
        prev_states = [a.state for a in self.agents]
        
        # 3. Synchronous inference step for all 7 agents
        for i in range(7):
            neighbors = NEIGHBORS[i]
            neighbor_distress = sum(1.0 for n in neighbors if prev_states[n] >= 1) / len(neighbors)
            self.agents[i].step(sensor_inputs[i], neighbor_distress)

        # 4. Compute global network Phi
        self.compute_collective_phi()
        return self.phi_collective

# ==============================================================================
# 4. PHYSICAL ACTUATION & VITALITY DISPLAY
# ==============================================================================

def update_hardware_actuators(cluster, phi_net):
    # Actuator 1 (GP16): Consensus / Harmony (Active when Phi_net >= 0.70)
    if phi_net >= 0.70:
        actuator_consensus.value(1)
    else:
        actuator_consensus.value(0)
        
    # Actuator 2 (GP17): Emergency / Collective Hazard (Active if any node is CRITICAL)
    hazard_active = any(a.state == 2 for a in cluster.agents)
    actuator_hazard.value(1 if hazard_active else 0)

def pulse_collective_led(phi_net, step_count):
    """Modulates onboard LED PWM with collective network vitality."""
    if phi_net <= 0.05:
        led_pwm.duty_u16(0)
        return
        
    freq_factor = 0.04 + (1.0 - phi_net) * 0.16
    sine_val = (math.sin(step_count * freq_factor) + 1.0) / 2.0
    duty = int(sine_val * phi_net * 65535)
    duty = max(0, min(65535, duty))
    led_pwm.duty_u16(duty)

# ==============================================================================
# 5. MAIN EMBEDDED CLUSTER RUNTIME
# ==============================================================================

def run_pico_7_cluster():
    print("=" * 76)
    print(" 🌐 7-AGENT CONATIVE ACTIVE INFERENCE CLUSTER — RASPBERRY PI PICO 2H")
    print(" Architecture: Dual-ADC Boundary Sensing & 7-Node Chordal Ring Topology")
    print(" Target: RP2350 (Dual Cortex-M33 @ 150 MHz, MicroPython)")
    print("=" * 76)
    print(" Inputs : ADC(0) / GP26 (Sensor Alpha) | ADC(1) / GP27 (Sensor Beta)")
    print(" Outputs: GP25 (Pulse LED Phi_net) | GP16 (Harmony) | GP17 (Hazard Alarm)")
    print("-" * 76)

    cluster = ConativeCluster7()
    step = 0

    try:
        while True:
            step += 1
            
            # 1. Read Dual Physical ADCs
            val_alpha = read_adc_normalized(adc_alpha)
            val_beta  = read_adc_normalized(adc_beta)
            core_temp = read_temperature_celsius()
            
            # 2. Run Synchronous Multi-Agent Conative Inferenz (7 Agents)
            phi_net = cluster.cycle(val_alpha, val_beta)
            
            # 3. Actuate Physical Pins & Pulse Vitality Heartbeat
            update_hardware_actuators(cluster, phi_net)
            pulse_collective_led(phi_net, step)
            
            # 4. Real-time Cluster Telemetry Line
            # Node state symbols: '.' = OPTIMAL, '!' = STRESSED, 'X' = CRITICAL
            symbols = [".", "!", "X", "#"]
            cluster_graph = "".join(f"[N{i}:{symbols[cluster.agents[i].state]}]" for i in range(7))
            
            bar_len = int(phi_net * 10)
            phi_bar = "[" + "#" * bar_len + "-" * (10 - bar_len) + "]"
            
            print("Step {:04d} | ADC0(α): {:4.2f} | ADC1(β): {:4.2f} | {} | Φ_net: {:4.2f} {} | T: {:4.1f}°C".format(
                step, val_alpha, val_beta, cluster_graph, phi_net, phi_bar, core_temp
            ))
            
            # Loop rate: 10 Hz (100 ms cycle)
            sleep_ms(100)

    except KeyboardInterrupt:
        print("\n[STOP] Cluster halted by user. Safing GPIO pins...")
        actuator_consensus.value(0)
        actuator_hazard.value(0)
        led_pwm.duty_u16(0)
        print("[SAFE] Hardware safe.")

if __name__ == "__main__":
    run_pico_7_cluster()
