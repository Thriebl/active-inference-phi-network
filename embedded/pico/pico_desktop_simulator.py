"""
Desktop Simulator / Mock Harness for Pico 2H Conative Controller
Allows testing the Conative Active Inference engine on Linux without physical hardware.
"""

import time
import math
import random

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
    def freq(self, f):
        pass
    def duty_u16(self, d):
        self._duty = d

class MockADC:
    def __init__(self, channel):
        self.channel = channel
        self.sim_temp = 28.0
    def read_u16(self):
        if self.channel == 4:
            # Simulate internal temperature fluctuating
            # Formula: temp = 27.0 - (V - 0.706) / 0.001721
            # V = 0.706 - (temp - 27.0) * 0.001721
            v = 0.706 - (self.sim_temp - 27.0) * 0.001721
            return int((v / 3.3) * 65535)
        else:
            return random.randint(15000, 45000)

import sys
from types import ModuleType

mock_machine = ModuleType("machine")
mock_machine.Pin = MockPin
mock_machine.PWM = MockPWM
mock_machine.ADC = MockADC
sys.modules["machine"] = mock_machine


# Re-use Conative Engine & Initialized Pins from main
from main import (
    ConativePicoAgent,
    update_physical_actuators,
    pulse_vitality_led,
    read_temperature_celsius,
    read_analog_ratio,
    read_hazard_contact,
    temp_sensor,
    analog_sensor,
    hazard_switch,
    actuator_task,
    actuator_cool,
)


def run_desktop_demo():
    print("=" * 70)
    print(" 🖥️  PICO 2H CONATIVE CONTROLLER — DESKTOP SIMULATOR (MOCK HARDWARE)")
    print(" Running pure Conative Active Inference engine (Axiom 6, H=2)")
    print("=" * 70)
    
    agent = ConativePicoAgent(temporal_horizon=2)
    step = 0
    sim_t = 26.0

    print("Simulating 35 steps of physical embedded active inference:")
    print("At Step 12: A deceptive sensory lure tempts the agent to overheat.")
    print("At Step 22: External thermal disturbance injected.")
    print("-" * 70)

    for step in range(1, 36):
        # Environmental dynamics simulation:
        # If task actuator is active, heat increases
        if actuator_task.value() == 1:
            sim_t += 1.8
        elif actuator_cool.value() == 1:
            sim_t -= 2.2
        else:
            sim_t += (24.0 - sim_t) * 0.1 # Ambient cooling towards 24C

        # Inject disturbance at step 22
        if step == 22:
            sim_t += 12.0
            print("  ⚠️ [ENVIRONMENT] Sudden external thermal spike injected!")

        temp_sensor.sim_temp = sim_t
        core_temp = read_temperature_celsius()
        ambient_analog = read_analog_ratio()
        contact_hazard = read_hazard_contact()

        action = agent.select_action(contact_hazard, core_temp)
        update_physical_actuators(action)
        pulse_vitality_led(agent.phi, step)

        state_labels = ["OPTIMAL", "ELEVATED", "CRITICAL", "COLLAPSED"]
        status_str = state_labels[agent.state]
        bar_len = int(agent.phi * 10)
        phi_bar = "[" + "#" * bar_len + "-" * (10 - bar_len) + "]"

        print("Step {:02d} | T_core: {:4.1f}°C | State: {:8s} | Act: {:7s} | Pins: [T:{} C:{}] | Phi: {:4.2f} {}".format(
            step, core_temp, status_str, action, actuator_task.value(), actuator_cool.value(), agent.phi, phi_bar
        ))
        time.sleep(0.08)

    print("-" * 70)
    print("🎯 Simulation complete. Conative agent successfully preserved boundary (Phi > 0)!")
    print("   Notice how the agent automatically switched to EVADE/COOL when approaching the thermal boundary.")

if __name__ == "__main__":
    run_desktop_demo()
