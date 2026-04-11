# coordinate_system/grid_builder.py
#
# PURPOSE: Construct the planetary surface grid.
#
# Grid geometry: equirectangular projection.
#   GRID_WIDTH  = 4096 cells (longitude axis, 0° to 360°)
#   GRID_HEIGHT = 2048 cells (latitude axis, -90° to +90°)
#   Each cell spans 360/4096 ≈ 0.0879° longitude
#                  180/2048 ≈ 0.0879° latitude
#
# Cell size in metres (at equator):
#   cell_size_m = 2 * pi * R_m / GRID_WIDTH
#
# Derivation: circumference of a sphere = 2 * pi * R. Divided by the number
# of cells along the equator. Rule 1 Category B derived quantity.
# No Earth fallback — R_m is supplied from Variable 02.
#
# Grid layers initialised here (all zero):
#   'regime_id'     : int8  [H x W] — compositional regime (0=dwarf,1=rocky,
#                     2=sub_neptune,3=gas_giant,4=brown_dwarf)
#   'R_m'           : float32 [H x W] — planetary radius [m] (uniform at this stage)
#   'rho_mean'      : float32 [H x W] — mean density [kg/m^3] (uniform)
#   'g'             : float32 [H x W] — surface gravity [m/s^2] (uniform)
#   'v_e'           : float32 [H x W] — escape velocity [m/s] (uniform)
#   'P_c'           : float32 [H x W] — central pressure [Pa] (uniform)
#
# Future variables append new layers to this dict. No layer is ever removed.

import math

import numpy as np

GRID_WIDTH = 4096
GRID_HEIGHT = 2048

REGIME_IDS = {
    "dwarf": 0,
    "rocky": 1,
    "sub_neptune": 2,
    "gas_giant": 3,
    "brown_dwarf": 4,
}


def build_grid(v02: dict) -> tuple:
    """
    Construct the initial planetary grid populated with Variable 02 outputs.

    Parameters
    ----------
    v02 : dict — output of variable_02_composition.run()

    Returns
    -------
    grid : dict of numpy arrays, all shape (GRID_HEIGHT, GRID_WIDTH)
    meta : dict of scalar metadata
    """
    H, W = GRID_HEIGHT, GRID_WIDTH

    regime_id = REGIME_IDS.get(v02["regime"], -1)
    R_m = v02["R_m"] if v02["R_m"] is not None else 0.0
    rho_mean = v02["rho_mean_kg_m3"] if v02["rho_mean_kg_m3"] is not None else 0.0
    g = v02["g_m_s2"] if v02["g_m_s2"] is not None else 0.0
    v_e = v02["v_e_m_s"] if v02["v_e_m_s"] is not None else 0.0
    P_c = v02["P_c_Pa"] if v02["P_c_Pa"] is not None else 0.0

    # Cell size at the equator [m]
    cell_size_m = (2.0 * math.pi * R_m / W) if R_m > 0.0 else 0.0

    grid = {
        "regime_id": np.full((H, W), regime_id, dtype=np.int8),
        "R_m": np.full((H, W), R_m, dtype=np.float32),
        "rho_mean": np.full((H, W), rho_mean, dtype=np.float32),
        "g": np.full((H, W), g, dtype=np.float32),
        "v_e": np.full((H, W), v_e, dtype=np.float32),
        "P_c": np.full((H, W), P_c, dtype=np.float32),
    }

    meta = {
        "regime": v02["regime"],
        "regime_id": regime_id,
        "cell_size_m": cell_size_m,
        "grid_width": W,
        "grid_height": H,
    }

    return grid, meta
