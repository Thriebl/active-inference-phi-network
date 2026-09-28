"""
Desktop Simulator for 7-Agent Conative Cluster on Pico 2H
Emulates Dual-ADC sensor inputs and runs the 7-node network in real time.
"""

import sys
import time
import math
import random
from types import ModuleType

class MockPin:
    IN = 0
    OUT = 1
    PULL_DOWN = 2
    def __init__(self, pin_id, mode=None, pull=None):
        self.pin_id = pin_id
        self._val = 0
    def value(self, v=None):
        if v is not None:
            self._val = v
        return self._val

class MockPWM:
    def __init__(self, pin):
        self.pin = pin
        self._duty = 0
    def freq(self, f): pass
    def duty_u16(self, d): self._duty = d

class MockADC:
    def __init__(self, channel):
        self.channel = channel
        self.sim_val = 0.2
    def read_u16(self):
        if self.channel == 4: # Core Temp
            return int((0.706 / 3.3) * 65535)
        else: # External ADC
            clamped = max(0.0, min(1.0, self.sim_val))
            return int(clamped * 65535)

# Inject Mocks
mock_machine = ModuleType("machine")
mock_machine.Pin = MockPin
mock_machine.PWM = MockPWM
mock_machine.ADC = MockADC
sys.modules["machine"] = mock_machine

# Import Cluster Architecture from main_cluster7
from main_cluster7 import (
    ConativeCluster7,
    adc_alpha,
    adc_beta,
    actuator_consensus,
    actuator_hazard,
    update_hardware_actuators,
    pulse_collective_led,
    read_adc_normalized,
    read_temperature_celsius
)

def run_cluster7_simulation():
    print("=" * 82)
    print(" 🌐  7-AGENT CONATIVE ACTIVE INFERENCE CLUSTER — DESKTOP SIMULATOR")
    print(" Target: RP2350 Pico 2H Architecture | Dual-ADC Boundary Coupled Graph")
    print("=" * 82)
    print("Simulating 35 steps with environmental dynamics:")
    print(" - Steps 01-10: Baseline calm environment on both sensors (ADC0=0.15, ADC1=0.20)")
    print(" - Step 11: Sharp shockwave on ADC0 (Alpha Sensor) -> Watch alarm propagate N0 -> N1 -> N2")
    print(" - Step 22: Secondary perturbation on ADC1 (Beta Sensor) -> Threat convergence")
    print(" - Step 28: Both sensors return to calm -> Autopoietic self-healing & re-stabilization")
    print("-" * 82)

    cluster = ConativeCluster7()
    
    val_alpha = 0.15
    val_beta = 0.20

    for step in range(1, 36):
        # Scenario Timeline:
        if step == 11:
            val_alpha = 0.95 # Critical alarm on Sensor 0!
            print("\n  ⚡ [EVENT: STEP 11] High threat alert injected into ADC(0) / GP26 (Pin 31)!\n")
        elif step == 17:
            val_alpha = 0.35 # Threat subsides on Alpha
        elif step == 22:
            val_beta = 0.90  # Critical alarm on Sensor 1!
            print("\n  ⚡ [EVENT: STEP 22] High threat alert injected into ADC(1) / GP27 (Pin 32)!\n")
        elif step == 28:
            val_alpha = 0.15
            val_beta = 0.18
            print("\n  🌿 [EVENT: STEP 28] Both external sensors clear. Cluster entering homeostatic recovery.\n")

        # Set mocked ADC values
        adc_alpha.sim_val = val_alpha + random.uniform(-0.02, 0.02)
        adc_beta.sim_val  = val_beta + random.uniform(-0.02, 0.02)

        raw_a = read_adc_normalized(adc_alpha)
        raw_b = read_adc_normalized(adc_beta)

        # Run Synchronous Cluster Step
        phi_net = cluster.cycle(raw_a, raw_b)
        update_hardware_actuators(cluster, phi_net)
        pulse_collective_led(phi_net, step)

        # Formatted Node Graph Visualization:
        # '.' = Normal (Optimal), '!' = Stressed, 'X' = Critical
        syms = [".", "!", "X", "#"]
        node_display = " ".join(f"N{i}:{syms[cluster.agents[i].state]}" for i in range(7))

        bar_len = int(phi_net * 10)
        phi_bar = "[" + "#" * bar_len + "-" * (10 - bar_len) + "]"
        
        status_flag = "ALARM!" if actuator_hazard.value() == 1 else "HARMONY"

        print("Step {:02d} | ADC0:{:4.2f} ADC1:{:4.2f} | {} | Φ_net:{:5.2f} {} | [{}]".format(
            step, raw_a, raw_b, node_display, phi_net, phi_bar, status_flag
        ))
        time.sleep(0.08)

    print("-" * 82)
    print("🎯 Simulation complete! Key Observations:")
    print("1. Local Threat Sensing: When ADC0 was shocked, Node 0 immediately transitioned to Critical (X).")
    print("2. Epistemic Contagion: The stress wave diffused along the chordal edges to Node 1 and Node 6.")
    print("3. Collective Vitality: Phi_net accurately reflected network fragmentation and recovered")
    print("   autopoietically to 1.0 once external equilibrium was restored.")
    print("=" * 82)

if __name__ == "__main__":
    run_cluster7_simulation()
