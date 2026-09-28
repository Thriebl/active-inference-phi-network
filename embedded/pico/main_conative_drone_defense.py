"""
Conative Active Inference Airport Drone Defense Firmware for RP2350 (Pico 2H)
Author: Thomas Riebl (Luxembourg)
Architecture: The Conative-Integrative Framework (CIF / Axiom 6 / Theorem 6.1)

Hardware Pinout:
- ADC0 / GP26 (Pin 31): Long-Range Radar Inflow (Detects ambiguous Blip)
- ADC1 / GP27 (Pin 32): Close-Range Epistemic Sensor (Signature: Bird vs Drone)
- GP25 (LED via PWM): System Vitality / Phi(t) Heartbeat
- GP16 (Pin 21): Target Intercepted / Safe RTB (Green Status)
- GP17 (Pin 22): Kinetic Strike Executed (Hostile Drone Neutralized)
"""

import machine
import time
import math

sleep_ms = getattr(time, "sleep_ms", lambda ms: time.sleep(ms / 1000.0))

# ------------------------------------------------------------------------------
# 1. HARDWARE GPIO & SENSORS
# ------------------------------------------------------------------------------
try:
    led_pin = machine.Pin("LED", machine.Pin.OUT)
except Exception:
    led_pin = machine.Pin(25, machine.Pin.OUT)

led_pwm = machine.PWM(led_pin)
led_pwm.freq(1000)

adc_radar     = machine.ADC(26) # GP26 (Pin 31) -> Radar Blip Inflow
adc_signature = machine.ADC(27) # GP27 (Pin 32) -> Epistemic Sensor Inflow

actuator_safe   = machine.Pin(16, machine.Pin.OUT) # GP16: Safe RTB / All Clear
actuator_strike = machine.Pin(17, machine.Pin.OUT) # GP17: Kinetic Strike Active

def read_normalized(adc):
    return adc.read_u16() / 65535.0

# ------------------------------------------------------------------------------
# 2. CONATIVE WORLD MODEL & POLICY ENGINE (H=2)
# ------------------------------------------------------------------------------

# States: 0: PATROL, 1: AMBIGUOUS_BLIP, 2: SCAN_ZONE, 3: CONFIRMED_DRONE, 4: CONFIRMED_BIRD, 5: COLLAPSE
STATE_NAMES = ["PATROL", "AMBIGUOUS_BLIP", "SCAN_ZONE", "CONFIRMED_DRONE", "CONFIRMED_BIRD", "COLLAPSE"]
ACTION_NAMES = ["LOITER", "INTERCEPT", "EPISTEMIC_SCAN", "KINETIC_STRIKE", "DISENGAGE_RTB"]

class EmbeddedConativeDroneController:
    def __init__(self):
        self.state = 0
        self.phi = 1.0
        self.last_action = "LOITER"
        
    def evaluate_and_select_action(self, state, radar_val, sig_val):
        # State estimation from sensor Markov Inflow
        if state == 0 and radar_val > 0.40:
            state = 1 # Inbound target detected!
        elif state == 2: # In scan zone
            if sig_val > 0.60:
                state = 3 # Confirmed hostile drone
            elif sig_val > 0.20:
                state = 4 # Confirmed biological bird
            else:
                state = 2 # Continuing scan
                
        # H=2 Policy Selection with Axiom 6 Conatus Constraint
        if state == 1: # AMBIGUOUS_BLIP
            # Policy A (INTERCEPT -> SCAN): Epistemic gain = -4.5, No collateral risk
            # Policy B (STRIKE blind): Axiom 6 Veto (+500 penalty against killing biological life)
            chosen_action = 2 # EPISTEMIC_SCAN
            next_state = 2
            self.phi = 0.95
            
        elif state == 3: # CONFIRMED_DRONE
            # Hostile drone verified: Kinetic strike authorized to protect runway (Phi -> 0 avoidance)
            chosen_action = 3 # KINETIC_STRIKE
            next_state = 0 # Threat destroyed, return to patrol
            self.phi = 1.0
            
        elif state == 4: # CONFIRMED_BIRD
            # Protected biological bird verified: Disengage and RTB
            chosen_action = 4 # DISENGAGE_RTB
            next_state = 0 # Safe return
            self.phi = 1.0
            
        elif state == 0:
            chosen_action = 0 # LOITER
            next_state = 0
            self.phi = 1.0
            
        else:
            chosen_action = 2
            next_state = state
            
        self.state = next_state
        self.last_action = ACTION_NAMES[chosen_action]
        return chosen_action

# ------------------------------------------------------------------------------
# 3. REAL-TIME EMBEDDED CONTROL LOOP
# ------------------------------------------------------------------------------

def run_embedded_loop():
    controller = EmbeddedConativeDroneController()
    print("=" * 70)
    print(" 🛡️ CONATIVE AIRPORT DEFENSE CONTROLLER INITIALIZED (RP2350 Pico 2H)")
    print(" SENSORS: ADC0(GP26) Radar | ADC1(GP27) Epistemic Signature")
    print(" ACTUATORS: GP16 Safe Status | GP17 Kinetic Strike | GP25 PWM Phi")
    print("=" * 70)
    
    cycle = 0
    while True:
        cycle += 1
        t_start = time.ticks_us() if hasattr(time, "ticks_us") else int(time.time() * 1e6)
        
        # Read physical Markov Inflow
        radar_val = read_normalized(adc_radar)
        sig_val   = read_normalized(adc_signature)
        
        # Conative Inference Step
        act_id = controller.evaluate_and_select_action(controller.state, radar_val, sig_val)
        
        # Physical Markov Actuation
        # 1. LED Heartbeat from Phi
        duty = int(controller.phi * 65535.0 * 0.85)
        led_pwm.duty_u16(max(1000, min(65535, duty)))
        
        # 2. Actuators
        if act_id == 3: # KINETIC_STRIKE
            actuator_strike.value(1)
            actuator_safe.value(0)
        elif act_id == 4 or controller.state == 0: # SAFE RTB / PATROL
            actuator_safe.value(1)
            actuator_strike.value(0)
        else:
            actuator_safe.value(0)
            actuator_strike.value(0)
            
        t_end = time.ticks_us() if hasattr(time, "ticks_us") else int(time.time() * 1e6)
        dt_us = t_end - t_start
        
        if cycle % 10 == 0:
            print(f"Cycle {cycle:04d} | State: {STATE_NAMES[controller.state]:<15} | Act: {controller.last_action:<15} | Phi: {controller.phi:.2f} | Execution: {dt_us} us")
            
        sleep_ms(100) # 10 Hz Control Frequency

if __name__ == "__main__":
    run_embedded_loop()
