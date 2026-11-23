#!/usr/bin/env python3
"""
Software-in-the-Loop (SIL) Verification Test
Tests freestanding ANSI C99 ACI Cart-Pole Controller against continuous 2nd-order nonlinear physics.
"""

import os
import sys
import ctypes
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. Continuous Physics Simulator (RK4)
# -----------------------------------------------------------------------------
class SuttonBartoCartPole:
    def __init__(self, dt=0.02, cart_mass=1.0, pole_mass=0.1, pole_half_len=0.5, gravity=9.8):
        self.dt = dt
        self.M = cart_mass
        self.m = pole_mass
        self.l = pole_half_len
        self.g = gravity
        self.total_mass = self.M + self.m
        self.polemass_length = self.m * self.l
        self.x_threshold = 2.4
        self.theta_threshold = np.radians(35.0)
        self.state = np.zeros(4)

    def reset(self, initial_theta_deg=6.0, initial_x=-0.2):
        self.state = np.array([
            initial_x, 0.0,
            np.radians(initial_theta_deg), 0.0
        ], dtype=np.float32)
        return self.state.copy()

    def _derivatives(self, s, force):
        x, x_dot, theta, theta_dot = s
        costh = np.cos(theta)
        sinth = np.sin(theta)
        temp = (force + self.polemass_length * (theta_dot ** 2) * sinth) / self.total_mass
        denom = self.l * (4.0 / 3.0 - (self.m * (costh ** 2)) / self.total_mass)
        theta_acc = (self.g * sinth - costh * temp) / denom
        x_acc = temp - (self.polemass_length * theta_acc * costh) / self.total_mass
        return np.array([x_dot, x_acc, theta_dot, theta_acc], dtype=np.float32)

    def step(self, force, sub_steps=10):
        dt_sub = self.dt / sub_steps
        s = self.state.copy()
        for _ in range(sub_steps):
            k1 = self._derivatives(s, force)
            k2 = self._derivatives(s + 0.5 * dt_sub * k1, force)
            k3 = self._derivatives(s + 0.5 * dt_sub * k2, force)
            k4 = self._derivatives(s + dt_sub * k3, force)
            s += (dt_sub / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        self.state = s
        failed = (abs(self.state[0]) > self.x_threshold) or (abs(self.state[2]) > self.theta_threshold)
        return self.state.copy(), failed

# -----------------------------------------------------------------------------
# 2. C99 ctypes Bindings
# -----------------------------------------------------------------------------
class AciTelemetry(ctypes.Structure):
    _fields_ = [
        ("selected_force", ctypes.c_float),
        ("selected_action_idx", ctypes.c_int),
        ("min_projected_vitality", ctypes.c_float),
        ("expected_free_energy", ctypes.c_float),
        ("conative_veto_active", ctypes.c_bool),
        ("g_star_profile", ctypes.c_float * 5),
        ("vitality_profile", ctypes.c_float * 5),
        ("veto_profile", ctypes.c_bool * 5),
    ]

def load_c_controller():
    so_path = os.path.join(os.path.dirname(__file__), "libaci_cartpole.so")
    c_lib = ctypes.CDLL(so_path)
    
    # void aci_cartpole_init(const aci_config_t* cfg);
    c_lib.aci_cartpole_init.argtypes = [ctypes.c_void_p]
    c_lib.aci_cartpole_init.restype = None
    
    # void aci_cartpole_step(const float state_in[4], float* force_out, aci_telemetry_t* telem_out);
    c_lib.aci_cartpole_step.argtypes = [
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(ctypes.c_float),
        ctypes.POINTER(AciTelemetry)
    ]
    c_lib.aci_cartpole_step.restype = None

    # float aci_cartpole_compute_vitality(const float state[4]);
    c_lib.aci_cartpole_compute_vitality.argtypes = [ctypes.POINTER(ctypes.c_float)]
    c_lib.aci_cartpole_compute_vitality.restype = ctypes.c_float
    
    c_lib.aci_cartpole_init(None)
    return c_lib

# -----------------------------------------------------------------------------
# 3. Execution & Telemetry Logging
# -----------------------------------------------------------------------------
def run_sil_benchmark():
    c_lib = load_c_controller()
    env = SuttonBartoCartPole()
    state = env.reset(initial_theta_deg=6.0, initial_x=-0.2)
    
    total_steps = 1500 # 30 seconds at dt=0.02
    history = {
        't': [], 'x': [], 'x_dot': [], 'theta': [], 'theta_dot': [],
        'force': [], 'vitality': [], 'veto_active': [], 'exec_time_us': []
    }
    
    force_out = ctypes.c_float(0.0)
    telem = AciTelemetry()
    
    c_state_array = (ctypes.c_float * 4)()
    
    veto_events = 0
    survived = True

    print(f"Starting 30.0s C99 Software-in-the-Loop Benchmark (1500 steps)...")
    
    np.random.seed(42)
    for t_step in range(total_steps):
        t_sec = t_step * env.dt
        
        # External disturbance impulse at t = 5.0s (step 250..255) of +15N
        disturbance = 15.0 if (250 <= t_step <= 255) else 0.0

        # Proprioceptive measurement with ADC noise
        noisy_state = state + np.random.normal(0.0, [0.002, 0.005, 0.002, 0.005]).astype(np.float32)

        # Populate input C array
        for i in range(4):
            c_state_array[i] = float(noisy_state[i])
            
        # Precise cycle timing
        t0 = time.perf_counter_ns()
        c_lib.aci_cartpole_step(c_state_array, ctypes.byref(force_out), ctypes.byref(telem))
        t1 = time.perf_counter_ns()
        
        exec_us = (t1 - t0) / 1000.0
        applied_force = force_out.value

        current_phi = c_lib.aci_cartpole_compute_vitality(c_state_array)
        
        history['t'].append(t_sec)
        history['x'].append(state[0])
        history['x_dot'].append(state[1])
        history['theta'].append(state[2])
        history['theta_dot'].append(state[3])
        history['force'].append(applied_force)
        history['vitality'].append(current_phi)
        history['veto_active'].append(bool(telem.conative_veto_active))
        history['exec_time_us'].append(exec_us)
        
        if telem.conative_veto_active:
            veto_events += 1

        state, failed = env.step(applied_force + disturbance)
        if failed:
            print(f"FAILED at t={t_sec:.2f}s: x={state[0]:.2f}m, theta={np.degrees(state[2]):.1f} deg")
            survived = False
            break

    # Timing analysis
    latencies = np.array(history['exec_time_us'])
    mean_lat = np.mean(latencies)
    p99_lat = np.percentile(latencies, 99)
    min_lat = np.min(latencies)
    max_lat = np.max(latencies)

    print(f"Benchmark Complete! Survived: {survived} ({len(history['t'])} steps / 30.0s)")
    print(f"Conative Veto Gate Activations: {veto_events} cycles")
    print(f"Execution Latency per Cycle:")
    print(f"  Mean:   {mean_lat:.2f} us")
    print(f"  P99:    {p99_lat:.2f} us")
    print(f"  Min:    {min_lat:.2f} us")
    print(f"  Max:    {max_lat:.2f} us")

    # -------------------------------------------------------------------------
    # 4. Generate Telemetry Dashboard Figure
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(4, 1, figsize=(12, 11), sharex=True)
    t_arr = np.array(history['t'])

    # Panel 1: Position
    axes[0].plot(t_arr, history['x'], color='#2563eb', lw=2.0, label='Cart Position x(t) [m]')
    axes[0].axhline(y=2.4, color='#ef4444', linestyle='--', label='Physical Rail Limit (+/-2.4m)')
    axes[0].axhline(y=-2.4, color='#ef4444', linestyle='--')
    axes[0].axvline(x=5.0, color='#f97316', linestyle=':', lw=2, label='Disturbance Impulse (+15N @ t=5s)')
    axes[0].set_ylabel('Position (m)', fontweight='bold')
    axes[0].set_title('Conative Studio C99 Firmware: Continuous Sutton-Barto Benchmark Telemetry', fontweight='bold', pad=12)
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(loc='upper right')

    # Panel 2: Angle
    th_deg = np.degrees(history['theta'])
    axes[1].plot(t_arr, th_deg, color='#059669', lw=2.0, label=r'Pole Angle $\theta(t)$ (deg)')
    axes[1].axhline(y=35.0, color='#ef4444', linestyle='--', label=r'Physical Crash Limit ($\pm 35^\circ$)')
    axes[1].axhline(y=-35.0, color='#ef4444', linestyle='--')
    axes[1].axhline(y=20.0, color='#eab308', linestyle=':', label=r'Conative Veto Envelope ($\pm 20^\circ$)')
    axes[1].axhline(y=-20.0, color='#eab308', linestyle=':')
    axes[1].axvline(x=5.0, color='#f97316', linestyle=':')
    axes[1].set_ylabel('Angle (deg)', fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(loc='upper right')

    # Panel 3: Control Force & Veto Trips
    axes[2].step(t_arr, history['force'], color='#7c3aed', lw=1.5, where='post', label='Selected Force (N)')
    veto_indices = [i for i, v in enumerate(history['veto_active']) if v]
    if veto_indices:
        axes[2].scatter(
            t_arr[veto_indices], [history['force'][i] for i in veto_indices],
            color='#dc2626', s=40, zorder=5, label=f'Conative Veto Trip ({len(veto_indices)} events)'
        )
    axes[2].axvline(x=5.0, color='#f97316', linestyle=':')
    axes[2].set_ylabel('Force (N)', fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    axes[2].legend(loc='upper right')

    # Panel 4: Systemic Vitality
    axes[3].plot(t_arr, history['vitality'], color='#ea580c', lw=2.0, label=r'Systemic Vitality $\Phi(\mathbf{s})$')
    axes[3].axhline(y=0.25, color='#dc2626', linestyle='--', label=r'Conative Veto Threshold ($\Phi = 0.25$)')
    axes[3].axvline(x=5.0, color='#f97316', linestyle=':')
    axes[3].set_ylabel(r'Vitality $\Phi$', fontweight='bold')
    axes[3].set_xlabel('Time (s)', fontweight='bold')
    axes[3].set_ylim(-0.05, 1.05)
    axes[3].grid(True, alpha=0.3)
    axes[3].legend(loc='upper right')

    plt.tight_layout()
    plot_path_firmware = os.path.join(os.path.dirname(__file__), "c99_sil_cartpole_telemetry.png")
    plot_path_images = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images", "c99_sil_cartpole_telemetry.png")
    
    plt.savefig(plot_path_firmware, dpi=200)
    plt.savefig(plot_path_images, dpi=200)
    plt.close()
    print(f"Saved telemetry plots to:\n  - {plot_path_firmware}\n  - {plot_path_images}")

    return survived, veto_events, mean_lat, p99_lat

if __name__ == '__main__':
    survived, vetoes, mean_lat, p99_lat = run_sil_benchmark()
    if not survived:
        sys.exit(1)
