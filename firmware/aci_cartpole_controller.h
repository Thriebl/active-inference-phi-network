/**
 * ============================================================================
 * CONATIVE SYSTEMS - DETERMINISTIC EMBEDDED CYBERNETICS
 * ============================================================================
 * File:        aci_cartpole_controller.h
 * Author:      Thomas Riebl (Conative Systems)
 * Target:      Freestanding ANSI C99 / ARM Cortex-M33 (RP2350 / Raspberry Pi Pico)
 * Architecture: Zero-Heap, Deterministic Active Conative Inference Controller
 *
 * Description:
 * Freestanding, allocation-free ANSI C99 controller synthesized from
 * Conative Studio. Implements deep counterfactual active inference rollouts
 * (Horizon H = 10) combined with an autopoietic Conative Veto Gate (Axiom 6)
 * and an empirical Systemic Vitality metric Phi(s).
 *
 * Dual-Target Compilation:
 * - Bare-Metal MCU: Compile directly with arm-none-eabi-gcc for RP2350.
 * - Host SIL (Software-in-the-Loop): Compile with gcc/clang -shared -fPIC
 *   to verify identical control behaviour against continuous physics in Python.
 * ============================================================================
 */

#ifndef ACI_CARTPOLE_CONTROLLER_H
#define ACI_CARTPOLE_CONTROLLER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

#define ACI_NUM_ACTIONS         5
#define ACI_HORIZON_DEFAULT     10
#define ACI_DT_DEFAULT          0.02f

/**
 * Cart-Pole 4D State Vector:
 * s = [x, x_dot, theta, theta_dot]
 */
typedef struct {
    float x;          /* Cart position on rail (m) */
    float x_dot;      /* Cart velocity (m/s) */
    float theta;      /* Pole angle from upright vertical (rad) */
    float theta_dot;  /* Pole angular velocity (rad/s) */
} aci_state_t;

/**
 * Controller Configuration & Tuning Parameters
 */
typedef struct {
    float dt;                  /* Discrete control time-step (s), default 0.02 */
    int   horizon;             /* Deep temporal rollout depth H, default 10 */
    float lambda_phi;          /* Vitality prioritization weight, default 4.0 */
    float veto_threshold;      /* Minimum acceptable vitality Phi, default 0.25 */
    float rail_limit_m;        /* Physical rail margin (m), default 1.8 */
    float angle_limit_rad;     /* Emergency tilt threshold (rad), default 20 deg (0.349 rad) */
} aci_config_t;

/**
 * Runtime Telemetry & Diagnostic Inspection
 */
typedef struct {
    float selected_force;                  /* Force applied to cart (N) */
    int   selected_action_idx;             /* Index in discrete action dictionary [0..4] */
    float min_projected_vitality;          /* Minimum anticipated vitality Phi along chosen path */
    float expected_free_energy;            /* Minimized G*(a) value */
    bool  conative_veto_active;            /* True if supervisory conative gate intervened */
    float g_star_profile[ACI_NUM_ACTIONS]; /* Expected Free Energy evaluated across all actions */
    float vitality_profile[ACI_NUM_ACTIONS];/* Minimum anticipated vitality across all actions */
    bool  veto_profile[ACI_NUM_ACTIONS];   /* Veto trip mask across all candidate actions */
} aci_telemetry_t;

/**
 * Initializes controller with specified configuration (or NULL for defaults).
 */
void aci_cartpole_init(const aci_config_t* cfg);

/**
 * Executes a single deterministic Active Conative Inference control cycle.
 * Computes counterfactual rollouts across all candidate actions, evaluates
 * Expected Free Energy G*(a), checks the Conative Veto Gate, and outputs
 * the optimal motor command and detailed telemetry.
 *
 * Execution profile: Bounded, allocation-free, < 15 microseconds.
 *
 * @param state_in   Pointer to current 4D state vector [x, x_dot, theta, theta_dot]
 * @param force_out  Pointer receiving selected horizontal motor force (N)
 * @param telem_out  Pointer receiving diagnostic telemetry (may be NULL)
 */
void aci_cartpole_step(const float state_in[4], float* force_out, aci_telemetry_t* telem_out);

/**
 * Evaluates the instantaneous Systemic Vitality metric Phi(s).
 * Quantifies the agent's structural self-integrity (1.0 = optimal upright equilibrium,
 * decaying to 0.0 near physical collapse).
 */
float aci_cartpole_compute_vitality(const float state[4]);

#ifdef __cplusplus
}
#endif

#endif /* ACI_CARTPOLE_CONTROLLER_H */
