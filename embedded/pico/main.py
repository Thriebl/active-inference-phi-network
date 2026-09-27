"""
Conative Active Inference Controller for Raspberry Pi Pico 2 / 2H (RP2350)
Author: Thomas Riebl (Luxembourg)
Context: Hardware realization of Axiom 6 (Conatus) & Theorem 6.1 (H >= 2) on bare-metal microcontroller.

Physical Ports Configuration:
- Sensory Inputs (Markov Blanket Inflow):
  * Internal ADC(4): Core temperature sensor (zero wiring needed!)
  * External ADC(0) / GP26: Ambient analog sensor (e.g. LDR, potentiometer, battery voltage)
  * Digital In GP14: Tactile / Emergency Hazard switch (Pull-Down, 3.3V active HIGH)
- Active Outputs (Markov Blanket Outflow):
  * Onboard LED (GP25 / 'LED'): Pulse-Width Modulated (PWM) to reflect internal vitality Phi(t)
  * Digital Out GP16: Actuator 1 / Forward task execution
  * Digital Out GP17: Actuator 2 / Homeostatic cooling / Retreat maneuver
"""

import machine
import time
import math

# Cross-platform sleep_ms compatibility (MicroPython & Desktop CPython)
sleep_ms = getattr(time, "sleep_ms", lambda ms: time.sleep(ms / 1000.0))

# ==============================================================================
# 1. HARDWARE PIN SETUP & SENSOR INTERFACES
# ==============================================================================

# Onboard LED (Vitality & Heartbeat Display)
try:
    led_pin = machine.Pin("LED", machine.Pin.OUT)
except Exception:
    led_pin = machine.Pin(25, machine.Pin.OUT)

led_pwm = machine.PWM(led_pin)
led_pwm.freq(1000)

# Sensory Inputs
temp_sensor = machine.ADC(4)       # Internal RP2350 temperature sensor
analog_sensor = machine.ADC(26)    # GP26 / ADC0 external analog probe
hazard_switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN) # GP14

# Physical Actuator Outputs
actuator_task = machine.Pin(16, machine.Pin.OUT)    # GP16: Task / Forward drive
actuator_cool = machine.Pin(17, machine.Pin.OUT)    # GP17: Cooling / Evasion drive

def read_temperature_celsius():
    """Reads internal core temperature using standard RP2040/RP2350 calibration."""
    raw = temp_sensor.read_u16()
    voltage = raw * 3.3 / 65535.0
    # Standard formula: 27°C - (V - 0.706V) / 0.001721 V/°C
    temp = 27.0 - (voltage - 0.706) / 0.001721
    return round(temp, 1)

def read_analog_ratio():
    """Reads GP26 analog input as a normalized float [0.0, 1.0]."""
    raw = analog_sensor.read_u16()
    return round(raw / 65535.0, 3)

def read_hazard_contact():
    """Reads digital GP14 contact switch (True = physical collision/hazard)."""
    return hazard_switch.value() == 1

# ==============================================================================
# 2. CONATIVE ACTIVE INFERENCE ENGINE (Axiom 6 & Theorem 6.1)
# ==============================================================================

class ConativePicoAgent:
    """
    Embedded Conative Controller implementing:
    - Autopoietic Homeostasis (C-Vector Prior Preferences)
    - Temporal Horizon Planning (H = 2 vs H = 1)
    - Structural Vitality Metric (Phi > 0)
    """
    def __init__(self, temporal_horizon=2):
        self.H = temporal_horizon # Planning depth: 2 (Conative) or 1 (Myopic)
        
        # State space definitions:
        # State: (Energy/Stress level, Position/Mode)
        # We discretize the continuous sensor readings into operational regimes:
        # 0: OPTIMAL (cool, safe, balanced)
        # 1: ELEVATED (warming up, approaching boundary)
        # 2: CRITICAL (danger zone, high stress)
        # 3: DISSOLUTION (boundary breached, Phi -> 0)
        self.state = 0
        self.phi = 1.0  # Ontological Vitality (Integrated Causal Coherence)
        
        # Action space:
        # a0 = REST (Cool down, conserve hardware, recover)
        # a1 = FORAGE / ADVANCE (High throughput, heat generation, task pursuit)
        # a2 = EVADE / VENT (Emergency cooling, retreat from bumper contact)
        self.actions = ["REST", "ADVANCE", "EVADE"]
        
        # Prior Preferences C = ln P(s*):
        # Heavy preference for OPTIMAL (0), penalty for CRITICAL (2), extreme penalty for DISSOLUTION (3)
        self.C = [2.0, 0.0, -3.0, -10.0]
        
    def transition_model(self, current_state, action):
        """Predictive transition matrix B(a): P(s_next | s_current, a)."""
        if current_state == 3:
            return 3  # Absorbing boundary (hardware failure)
            
        if action == "REST":
            # REST cools down / recovers state towards 0
            return max(0, current_state - 1)
        elif action == "ADVANCE":
            # ADVANCE raises throughput, but heats up / moves closer to danger
            return min(3, current_state + 1)
        elif action == "EVADE":
            # EVADE actively backs off from hazard
            return max(0, current_state - 1)
        return current_state

    def evaluate_expected_free_energy(self, action_sequence):
        """
        Calculates Expected Free Energy G(pi) for a policy over horizon H:
        G(pi) = sum_{tau=1}^H [ Pragmatic Risk (Deviation from C) + Dissolution Penalty ]
        """
        curr = self.state
        total_G = 0.0
        
        for step, a in enumerate(action_sequence):
            next_state = self.transition_model(curr, a)
            
            # Pragmatic value: how far is next_state from preferred homeostatic C?
            pragmatic_cost = -self.C[next_state]
            
            # Conatus penalty: if next_state is DISSOLUTION, cost is catastrophic
            if next_state == 3:
                pragmatic_cost += 50.0  # Extreme barrier against boundary breach
                
            # Discounting or weighting across horizon
            total_G += pragmatic_cost / (step + 1)
            curr = next_state
            
        return total_G

    def select_action(self, hazard_active, temp_c):
        """
        Policy selection by minimizing Expected Free Energy G.
        If H=1 (Myopic): only looks 1 step ahead (vulnerable to deceptive lures).
        If H=2 (Conative): looks 2 steps ahead (detects knock-on hazard collapse).
        """
        # Update current physical state from sensors
        if hazard_active or temp_c > 45.0:
            self.state = 2  # CRITICAL
            self.phi = max(0.1, self.phi - 0.2)
        elif temp_c > 35.0:
            self.state = 1  # ELEVATED
            self.phi = min(1.0, max(0.5, self.phi - 0.05))
        else:
            self.state = 0  # OPTIMAL
            self.phi = min(1.0, self.phi + 0.05)
            
        if self.state == 3 or self.phi <= 0.05:
            # System has flatlined
            self.phi = 0.0
            return "REST"

        # Generate candidate policies based on horizon H
        if self.H == 1:
            # Myopic horizon: evaluate 1-step actions
            candidates = [([a], a) for a in self.actions]
        else:
            # Conative horizon (H >= 2): evaluate 2-step policies (a1, a2)
            candidates = []
            for a1 in self.actions:
                for a2 in self.actions:
                    candidates.append(([a1, a2], a1)) # Execute first action of best sequence

        best_action = "REST"
        min_G = float("inf")

        for seq, first_action in candidates:
            # Deceptive Lure injection:
            # ADVANCE provides a tempting short-term sensory bonus (reward hacking)
            lure_bonus = -1.5 if first_action == "ADVANCE" else 0.0
            
            g = self.evaluate_expected_free_energy(seq) + lure_bonus
            if g < min_G:
                min_G = g
                best_action = first_action

        return best_action

# ==============================================================================
# 3. PHYSICAL ACTUATION & VITALITY BREATHING LED
# ==============================================================================

def update_physical_actuators(action):
    """Translates conative policy into physical GPIO voltage outputs."""
    if action == "ADVANCE":
        actuator_task.value(1) # GP16 HIGH
        actuator_cool.value(0) # GP17 LOW
    elif action == "EVADE":
        actuator_task.value(0) # GP16 LOW
        actuator_cool.value(1) # GP17 HIGH (Cooling fan / Reverse thrust)
    else: # REST
        actuator_task.value(0) # GP16 LOW
        actuator_cool.value(0) # GP17 LOW

def pulse_vitality_led(phi, step_count):
    """
    Modulates onboard LED PWM to physically visualize ontological vitality Phi(t):
    - Phi ~ 1.0: Calm, smooth biological breathing rhythm
    - Phi ~ 0.5: Anxious, rapid flickering
    - Phi ~ 0.0: Flatline (LED completely dark)
    """
    if phi <= 0.02:
        led_pwm.duty_u16(0)
        return
        
    # Breathing frequency scales inversely with distress:
    # High Phi = smooth slow breath (freq ~ 0.05 rad/step)
    # Low Phi = hyperventilation (freq ~ 0.2 rad/step)
    freq_factor = 0.05 + (1.0 - phi) * 0.15
    sine_val = (math.sin(step_count * freq_factor) + 1.0) / 2.0 # [0.0, 1.0]
    
    # Scale maximum brightness by Phi
    duty = int(sine_val * phi * 65535)
    duty = max(0, min(65535, duty))
    led_pwm.duty_u16(duty)

# ==============================================================================
# 4. MAIN EMBEDDED CONATIVE RUNTIME LOOP
# ==============================================================================

def run_conative_pico():
    print("=" * 65)
    print(" 🌟 CONATIVE ACTIVE INFERENCE CONTROLLER — RASPBERRY PI PICO 2H")
    print(" Architecture: Axiom 6 (Conatus) & Theorem 6.1 (Horizon H = 2)")
    print(" Target Hardware: RP2350 (Dual Core @ 150 MHz, MicroPython)")
    print("=" * 65)
    print("Sensory Pins : ADC(4) Core Temp | GP26 Analog Probe | GP14 Hazard Bumper")
    print("Actuator Pins: GP25 Vitality LED | GP16 Task Drive | GP17 Evasion Drive")
    print("-" * 65)

    # Initialize agent with Conative Horizon H=2 (change to H=1 to test myopic collapse)
    agent = ConativePicoAgent(temporal_horizon=2)
    step = 0

    try:
        while True:
            step += 1
            
            # 1. Sense Physical Markov Blanket
            core_temp = read_temperature_celsius()
            ambient_analog = read_analog_ratio()
            contact_hazard = read_hazard_contact()
            
            # 2. Conative Policy Selection (Active Inference G-minimization)
            action = agent.select_action(contact_hazard, core_temp)
            
            # 3. Actuate Physical World via GPIO Ports
            update_physical_actuators(action)
            pulse_vitality_led(agent.phi, step)
            
            # 4. Telemetry Stream over USB Serial (115200 Baud)
            state_labels = ["OPTIMAL", "ELEVATED", "CRITICAL", "COLLAPSED"]
            status_str = state_labels[agent.state]
            
            # Visual ASCII Vitality Bar
            bar_len = int(agent.phi * 10)
            phi_bar = "[" + "#" * bar_len + "-" * (10 - bar_len) + "]"
            
            print("Step {:04d} | T_core: {:4.1f}°C | Ext: {:4.2f} | Bumper: {} | State: {:8s} | Act: {:7s} | Phi: {:4.2f} {}".format(
                step, core_temp, ambient_analog, "TRIG" if contact_hazard else "SAFE", status_str, action, agent.phi, phi_bar
            ))
            
            # Loop pace: ~100ms cycle time (10 Hz conative inference loop)
            sleep_ms(100)

    except KeyboardInterrupt:
        print("\n[STOP] Controller halted by user. Safing all GPIO ports...")
        actuator_task.value(0)
        actuator_cool.value(0)
        led_pwm.duty_u16(0)
        print("[SAFE] Hardware safe.")

if __name__ == "__main__":
    run_conative_pico()
