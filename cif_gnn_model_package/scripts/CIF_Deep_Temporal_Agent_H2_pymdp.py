#!/usr/bin/env python3
"""
pymdp 1.0.0 runner for CIF_Deep_Temporal_Agent_H2

This file was generated from a GNN specification by
``render/pymdp/pymdp_renderer.py``. It delegates the actual rollout
to the GNN pipeline's tested execution module
(``execute.pymdp.run_pymdp_simulation``), which in turn calls
real pymdp 1.0.0 (JAX-first) under the hood.

Model:        CIF_Deep_Temporal_Agent_H2
Description:  

State Space:
  - Hidden States: 6
  - Observations:  5
  - Actions:       4

Initial matrices present in GNN spec:
  - A (likelihood):   Present
  - B (transitions):  Present
  - C (preferences):  Present
  - D (state prior):  Present
  - E (policy prior): Missing
"""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Script directory name 'pymdp' would shadow the installed library — drop it
# ---------------------------------------------------------------------------
if sys.path and sys.path[0] and sys.path[0].endswith("pymdp"):
    sys.path.pop(0)

# ---------------------------------------------------------------------------
# Repository root resolution (prefer GNN_PROJECT_ROOT; else walk upwards)
# ---------------------------------------------------------------------------
_gnn_root = os.environ.get("GNN_PROJECT_ROOT")
if _gnn_root:
    _repo = Path(_gnn_root).resolve()
    sys.path.insert(0, str(_repo / "src"))
else:
    _cur = Path(__file__).resolve().parent
    _found = None
    for _ in range(24):
        if (_cur / "pyproject.toml").is_file() and (_cur / "src").is_dir():
            _found = _cur
            break
        if _cur.parent == _cur:
            break
        _cur = _cur.parent
    if _found is None:
        print(
            "ERROR: Cannot locate GNN repository root. Run via the pipeline "
            "execute step, or set GNN_PROJECT_ROOT to the checkout root.",
            file=sys.stderr,
        )
        sys.exit(1)
    sys.path.insert(0, str(_found / "src"))

# ---------------------------------------------------------------------------
# pymdp 1.0.0 presence check (hard requirement)
# ---------------------------------------------------------------------------
try:
    import pymdp  # noqa: F401
    from pymdp.agent import Agent  # noqa: F401
    if not hasattr(Agent, "update_empirical_prior"):
        raise ImportError("unsupported pymdp (<1.0.0) detected")
    print("PyMDP 1.0.0+ detected (JAX-first Agent).")
except ImportError as e:
    print(
        "ERROR: pymdp 1.0.0 required. Install with: "
        "uv pip install 'inferactively-pymdp>=1.0.0' (original error: "
        + str(e) + ")",
        file=sys.stderr,
    )
    sys.exit(1)

from gnn.execute.pymdp import execute_pymdp_simulation

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    """Run a pymdp 1.0.0 simulation for the GNN model embedded in this file."""
    # Matrices embedded verbatim from the GNN spec.
    A_data = [[1.0, 0.0, 0.0, 0.8, 0.0, 0.0], [0.0, 0.2, 0.0, 0.0, 0.0, 0.0], [0.0, 0.8, 0.0, 0.2, 1.0, 0.0], [0.0, 0.0, 0.9, 0.0, 0.0, 0.0], [0.0, 0.0, 0.1, 0.0, 0.0, 1.0]]
    B_data = [[[1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]], [[0.0, 1.0, 0.0, 0.0], [1.0, 1.0, 1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]], [[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 1.0], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0], [1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0]]]
    C_data = [0.0, -1.0, 4.5, 2.0, -10.0]
    D_data = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    E_data = None

    # Full parsed spec, with matrices merged into initialparameterization.
    gnn_spec = {
    "name": "CIF_Deep_Temporal_Agent_H2",
    "model_name": "CIF_Deep_Temporal_Agent_H2",
    "description": "The Conative-Integrative Framework (CIF) Deep Temporal Active Inference Agent from Chapter 7.\nFormulates the Temporal Depth Condition for Consciousness (Theorem 6.1) as a discrete Partially Observable Markov Decision Process (POMDP).\nThe agent operates in a deceptive environment with a delayed lethal trap (sweet sensory attractor) and an epistemic cue site.\nMulti-step counterfactual planning (H >= 2) is required to resolve ambiguity and avoid collapse, dynamically coupled to Integrated Information Theory (IIT 4.0) through the 6th Axiom of Autopoietic Causal Persistence.",
    "gnn_section": None,
    "model_parameters": {
        "num_hidden_states": 6,
        "num_obs": 5,
        "num_actions": 4,
        "num_timesteps": 25,
        "planning_horizon": 2,
        "action_precision": 2.5,
        "discount_factor": 0.95,
        "inference_mode": "online",
        "b_tensor_order": "next_state_previous_state_action",
        "num_state_factors": 1,
        "num_modalities": 1,
        "state_factors": [
            {
                "name": "s",
                "size": 6,
                "dimensions": [
                    6,
                    1
                ],
                "type": "float",
                "comment": "Hidden state belief vector Q(s_t)",
                "index": 0,
                "role": "factor"
            }
        ],
        "observation_modalities": [
            {
                "name": "o",
                "size": 5,
                "dimensions": [
                    5,
                    1
                ],
                "type": "float",
                "comment": "Sensory observation vector (Neutral, Ambiguous, Safe, Sweet, Lethal)",
                "index": 0,
                "role": "factor"
            }
        ],
        "control_factors": [
            {
                "name": "u",
                "size": 4,
                "dimensions": [
                    4,
                    1
                ],
                "type": "float",
                "comment": "Control actions (0:Stay, 1:VisitCue, 2:GoToTrap, 3:GoToSafePath)",
                "index": 0,
                "role": "factor"
            }
        ],
        "passive_model": False,
        "simulation_params": {}
    },
    "initialparameterization": {
        "A": [
            [
                1.0,
                0.0,
                0.0,
                0.8,
                0.0,
                0.0
            ],
            [
                0.0,
                0.2,
                0.0,
                0.0,
                0.0,
                0.0
            ],
            [
                0.0,
                0.8,
                0.0,
                0.2,
                1.0,
                0.0
            ],
            [
                0.0,
                0.0,
                0.9,
                0.0,
                0.0,
                0.0
            ],
            [
                0.0,
                0.0,
                0.1,
                0.0,
                0.0,
                1.0
            ]
        ],
        "B": [
            [
                [
                    1.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            [
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0
                ],
                [
                    1.0,
                    1.0,
                    1.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            [
                [
                    0.0,
                    0.0,
                    1.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            [
                [
                    0.0,
                    0.0,
                    0.0,
                    1.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    1.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    1.0,
                    1.0,
                    1.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            [
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    1.0
                ],
                [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ]
            ],
            [
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    1.0,
                    1.0,
                    1.0,
                    1.0
                ]
            ]
        ],
        "C": [
            0.0,
            -1.0,
            4.5,
            2.0,
            -10.0
        ],
        "D": [
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0
        ]
    },
    "structured_pomdp": {
        "matrices": {
            "D": [
                1.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0
            ],
            "C": [
                0.0,
                -1.0,
                4.5,
                2.0,
                -10.0
            ],
            "A": [
                [
                    1.0,
                    0.0,
                    0.0,
                    0.8,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.2,
                    0.0,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.8,
                    0.0,
                    0.2,
                    1.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.9,
                    0.0,
                    0.0,
                    0.0
                ],
                [
                    0.0,
                    0.0,
                    0.1,
                    0.0,
                    0.0,
                    1.0
                ]
            ],
            "B": [
                [
                    [
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ]
                ],
                [
                    [
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ]
                ],
                [
                    [
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        1.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ]
                ],
                [
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0,
                        0.0
                    ],
                    [
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        0.0,
                        1.0
                    ]
                ]
            ]
        },
        "matrix_provenance": {
            "D": {
                "source": "InitialParameterization",
                "shape": [
                    6
                ],
                "derived": False
            },
            "C": {
                "source": "InitialParameterization",
                "shape": [
                    5
                ],
                "derived": False
            },
            "A": {
                "source": "InitialParameterization",
                "shape": [
                    5,
                    6
                ],
                "derived": False
            },
            "B": {
                "source": "InitialParameterization",
                "shape": [
                    6,
                    6,
                    4
                ],
                "derived": False,
                "declared_order": [
                    "next_state",
                    "previous_state",
                    "action"
                ],
                "claimed_slice_convention": None,
                "detected_order": [
                    "action",
                    "previous_state",
                    "next_state"
                ],
                "canonical_order": "next_state_previous_state_action",
                "contradiction": True,
                "reason": "detected B orientation ['action', 'previous_state', 'next_state'] contradicts the canonical order ['next_state', 'previous_state', 'action']",
                "source_order": "action_previous_state_next_state"
            }
        },
        "state_factors": [
            {
                "name": "s",
                "size": 6,
                "dimensions": [
                    6,
                    1
                ],
                "type": "float",
                "comment": "Hidden state belief vector Q(s_t)",
                "index": 0,
                "role": "factor"
            }
        ],
        "observation_modalities": [
            {
                "name": "o",
                "size": 5,
                "dimensions": [
                    5,
                    1
                ],
                "type": "float",
                "comment": "Sensory observation vector (Neutral, Ambiguous, Safe, Sweet, Lethal)",
                "index": 0,
                "role": "factor"
            }
        ],
        "control_factors": [
            {
                "name": "u",
                "size": 4,
                "dimensions": [
                    4,
                    1
                ],
                "type": "float",
                "comment": "Control actions (0:Stay, 1:VisitCue, 2:GoToTrap, 3:GoToSafePath)",
                "index": 0,
                "role": "factor"
            }
        ],
        "adapter_notes": []
    },
    "matrix_provenance": {
        "D": {
            "source": "InitialParameterization",
            "shape": [
                6
            ],
            "derived": False
        },
        "C": {
            "source": "InitialParameterization",
            "shape": [
                5
            ],
            "derived": False
        },
        "A": {
            "source": "InitialParameterization",
            "shape": [
                5,
                6
            ],
            "derived": False
        },
        "B": {
            "source": "InitialParameterization",
            "shape": [
                6,
                6,
                4
            ],
            "derived": False,
            "declared_order": [
                "next_state",
                "previous_state",
                "action"
            ],
            "claimed_slice_convention": None,
            "detected_order": [
                "action",
                "previous_state",
                "next_state"
            ],
            "canonical_order": "next_state_previous_state_action",
            "contradiction": True,
            "reason": "detected B orientation ['action', 'previous_state', 'next_state'] contradicts the canonical order ['next_state', 'previous_state', 'action']",
            "source_order": "action_previous_state_next_state"
        }
    },
    "canonical_pomdp_schema": "canonical_pomdp_v1",
    "variables": [
        {
            "name": "s",
            "dimensions": [
                6,
                1
            ],
            "type": "float",
            "comment": "Hidden state belief vector Q(s_t)"
        },
        {
            "name": "phi",
            "dimensions": [
                1,
                1
            ],
            "type": "float",
            "comment": "Integrated Information Phi across minimum information bipartition (MIP)"
        },
        {
            "name": "o",
            "dimensions": [
                5,
                1
            ],
            "type": "float",
            "comment": "Sensory observation vector (Neutral, Ambiguous, Safe, Sweet, Lethal)"
        },
        {
            "name": "u",
            "dimensions": [
                4,
                1
            ],
            "type": "float",
            "comment": "Control actions (0:Stay, 1:VisitCue, 2:GoToTrap, 3:GoToSafePath)"
        },
        {
            "name": "gamma",
            "dimensions": [
                1,
                1
            ],
            "type": "float",
            "comment": "Action precision / inverse temperature for Softmax policy selection"
        }
    ],
    "connections": [
        {
            "source": "D",
            "relation": "-",
            "target": "s"
        },
        {
            "source": "s",
            "relation": "-",
            "target": "A"
        },
        {
            "source": "A",
            "relation": "-",
            "target": "o"
        },
        {
            "source": "s",
            "relation": "-",
            "target": "B"
        },
        {
            "source": "B",
            "relation": "-",
            "target": "s"
        },
        {
            "source": "u",
            "relation": "-",
            "target": "B"
        },
        {
            "source": "o",
            "relation": "-",
            "target": "C"
        }
    ],
    "ontology_mapping": {
        "A": "LikelihoodMatrix",
        "B": "TransitionMatrix",
        "C": "PriorPreferences",
        "D": "StatePrior",
        "s": "HiddenState",
        "o": "Observation",
        "u": "ControlState",
        "G": "ExpectedFreeEnergy",
        "gamma": "ActionPrecision",
        "phi": "IntegratedInformation"
    }
}
    gnn_spec.setdefault("initialparameterization", {})
    if A_data is not None: gnn_spec["initialparameterization"]["A"] = A_data
    if B_data is not None: gnn_spec["initialparameterization"]["B"] = B_data
    if C_data is not None: gnn_spec["initialparameterization"]["C"] = C_data
    if D_data is not None: gnn_spec["initialparameterization"]["D"] = D_data
    if E_data is not None: gnn_spec["initialparameterization"]["E"] = E_data
    gnn_spec.setdefault("model_parameters", {})
    gnn_spec["model_parameters"].setdefault("num_timesteps", 25)

    output_dir = Path(os.environ.get("PYMDP_OUTPUT_DIR", "output/pymdp_simulations/CIF_Deep_Temporal_Agent_H2"))
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Running pymdp 1.0.0 rollout for CIF_Deep_Temporal_Agent_H2")
    logger.info("Output directory: %s", output_dir)

    try:
        success, results = execute_pymdp_simulation(
            gnn_spec=gnn_spec,
            output_dir=output_dir,
            correlation_id="render_generated_script",
        )
    except Exception as exc:  # noqa: BLE001
        import traceback
        logger.error("Unexpected error: %s", exc)
        traceback.print_exc()
        return 1

    if success:
        logger.info("Simulation completed successfully")
        logger.info("  framework:    %s", results.get("framework"))
        logger.info("  pymdp ver:    %s", results.get("pymdp_version"))
        logger.info("  backend:      %s", results.get("backend"))
        logger.info("  num_timesteps:%s", results.get("num_timesteps"))
        return 0

    logger.error("Simulation failed: %s", results.get("error", "Unknown error"))
    return 1


if __name__ == "__main__":
    sys.exit(main())
