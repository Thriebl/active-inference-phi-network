# ⚡ Conative Active Inference Firmware for Raspberry Pi Pico 2 / 2H (RP2350)

**Hardware-Level Implementation of Axiom 6 (Conatus) & Theorem 6.1 ($H \ge 2$)**  
*Author:* Thomas Riebl (Luxembourg)  
*Architecture:* RP2350 (Dual-Core ARM Cortex-M33 / Hazard3 RISC-V @ 150 MHz, MicroPython)

---

## 🎯 Overview

This embedded firmware runs an autonomous **Conative Active Inference agent directly on bare metal** using the physical GPIO ports of the **Raspberry Pi Pico 2 / Pico 2H**.

Unlike classic reactive or deep reinforcement learning controllers that suffer from myopic collapse ($H=1$), this controller implements **conative temporal horizon planning ($H=2$)**. It continuously evaluates:
$$G(\pi) = \sum_{\tau=1}^2 \Big( D_{\mathrm{KL}}\big(q(s_\tau \mid \pi) \parallel P(s^*)\big) + \mathcal{H}\big(q(o_\tau \mid s_\tau)\big) \Big)$$

It ensures that **internal ontological vitality ($\Phi(t) > 0$)** is never sacrificed for short-term reward lures.

---

## 🔌 Hardware Port Pinout (Markov Blanket Mapping)

The Raspberry Pi Pico 2H comes with pre-soldered pin headers:

```
                          ┌─────── USB ───────┐
            GP0 (UART0 TX)│ 1              40 │VBUS (5V USB in)
            GP1 (UART0 RX)│ 2              39 │VSYS (System voltage)
                       GND│ 3              38 │GND
                       GP2│ 4              37 │3V3_EN
                       GP3│ 5              36 │3V3(OUT)
                       GP4│ 6              35 │ADC_VREF
                       GP5│ 7              34 │GP28 / ADC2
                       GND│ 8              33 │GND
                       GP6│ 9              32 │GP27 / ADC1
                       GP7│ 10             31 │GP26 / ADC0 <--- [Sensory Analog Probe]
                       GP8│ 11             30 │RUN
                       GP9│ 12             29 │GP22
                       GND│ 13             28 │GND
                      GP10│ 14             27 │GP21
                      GP11│ 15             26 │GP20
                      GP12│ 16             25 │GP19
                      GP13│ 17             24 │GP18
[Hazard Bumper] --->  GP14│ 18             23 │GND
                      GP15│ 19             22 │GP17        <--- [Actuator 2: Evasion / Cooling]
                       GND│ 20             21 │GP16        <--- [Actuator 1: Task / Forward]
                          └───────────────────┘
               Internal: ADC(4) = RP2350 Core Temperature Sensor (Zero wiring needed!)
               Internal: GP25 / 'LED' = Onboard Pulse-Width Modulated Vitality Heartbeat
```

### 1. Inflow (Sensory Markov Blanket $s$):
* **Internal Core Temp (ADC 4):** Measures chip temperature in real-time. Works out of the box with zero external wiring.
* **External Analog Probe (GP26 / Pin 31):** Connect a potentiometer, photoresistor (LDR), or battery voltage divider.
* **Tactile Hazard Bumper (GP14 / Pin 18):** Emergency limit switch (pull-down, active HIGH 3.3V).

### 2. Outflow (Active Markov Blanket $a$):
* **Onboard Breathing LED (GP25 / PWM):** The physical heartbeat of $\Phi(t)$.
  * $\Phi \approx 1.0$: Smooth biological breathing rhythm (calm life).
  * $\Phi \approx 0.5$: Anxious rapid flickering (elevated distress).
  * $\Phi \le 0.05$: Flatline (LED off, system shutdown).
* **Actuator 1 — Task / Forward (GP16 / Pin 21):** 3.3V logic high during productive forward action.
* **Actuator 2 — Evasion / Cooling (GP17 / Pin 22):** 3.3V logic high during retreat or fan activation.

---

## 🚀 How to Flash & Run on Pico 2H

### Step 1: Flash MicroPython on Pico 2
1. Hold down the **BOOTSEL** white button on your Pico 2H.
2. Plug the USB cable into your PC. The Pico will mount as a USB flash drive named `RP2350`.
3. Download the official **Raspberry Pi Pico 2 MicroPython `.uf2` firmware** from [micropython.org](https://micropython.org/download/RPI_PICO2/).
4. Drag and drop the `.uf2` file onto the `RP2350` drive. The Pico will reboot automatically into MicroPython.

### Step 2: Copy `main.py` to the Pico
Using **Thonny IDE** (recommended) or `mpremote`:
```bash
# Optional command-line install:
pip install mpremote
mpremote cp main.py :main.py
mpremote repl
```
Or simply open **Thonny**, open `main.py`, select interpreter *"MicroPython (Raspberry Pi Pico)"*, and click **File -> Save As -> Raspberry Pi Pico -> `main.py`**.

### Step 3: Run Without PC (Standalone)
Once `main.py` is saved on the Pico, you can unplug it from the PC and power it with any USB phone charger or battery pack: the conative agent will immediately start its inference loop on boot!

---

## 🖥️ Desktop Simulation (Test Without Hardware)

You can run the conative controller directly on your Linux desktop:
```bash
python3 embedded/pico/pico_desktop_simulator.py
```
This mocks all hardware registers and simulates 35 steps of environmental perturbation, showing how $H=2$ detects the thermal trap and protects the Markov boundary!
