# variable_09_atmospheric_column/radical_steady_state.py
#
# Tropospheric OH / H steady-state gray closure (Scaffold §12.2).

from __future__ import annotations

import math
from typing import Mapping

_K_B = 1.381e-23  # J/K

# ⚠️ Note 174 — JPL reaction rate constants (Earth-laboratory; 200–400 K).
K_O1D_H2O = 2.2e-10  # cm^3/s
K_O1D_M = 3e-11
K_OH_CO = 1.5e-13
K_OH_H2 = 2.8e-12


def compute_radical_steady_state(
    *,
    speciation: Mapping[str, float],
    T_K: float,
    P_s_Pa: float,
    m_bar_kg_mol: float,
    photolysis_J: Mapping[str, float],
    F_xuv_W_m2: float | None = None,
) -> dict:
    """
    Return dict: regime, OH_cm3, H_cm3, notes.
    """
    x_o2 = float(speciation.get("O2", 0.0) or 0.0)
    x_co2 = float(speciation.get("CO2", 0.0) or 0.0)
    x_h2 = float(speciation.get("H2", 0.0) or 0.0)
    x_ch4 = float(speciation.get("CH4", 0.0) or 0.0)

    if x_o2 > 0.01 or x_co2 > 0.5:
        regime = "oxidizing"
    elif x_h2 > 0.5 or x_ch4 > 0.5:
        regime = "reducing"
    else:
        return {
            "regime": "collapsed",
            "OH_cm3": None,
            "H_cm3": None,
            "notes": "mixed/collapsed — [OH]=[H]=None",
        }

    n_mol_m3 = P_s_Pa / (_K_B * float(T_K))
    n_cm3 = n_mol_m3 * 1e-6

    if regime == "oxidizing":
        x_h2o = float(speciation.get("H2O", 0.0) or 0.0)
        x_co = float(speciation.get("CO", 0.0) or 0.0)
        x_o3 = float(speciation.get("O3", 0.0) or 0.0)
        if x_o3 <= 0.0:
            # ⚠️ EMPIRICAL — Note 174b modern tropospheric O3 mole fraction anchor
            # when absent from V08 speciation (Earth-like photochemistry only).
            x_o3 = 30e-9
        j_o3 = float(photolysis_J.get("O3", 0.0) or 0.0)
        if j_o3 <= 0.0 and F_xuv_W_m2 is not None:
            # ⚠️ Note 173 — actinic O3 photolysis fallback when O3 absent from V08
            from variable_09_atmospheric_column.photolysis_rates import (
                LAMBDA_MAX_PHOTOLYSIS_NM,
                SIGMA_A_M2,
            )

            h = 6.62607015e-34
            c = 2.99792458e8
            lam_m = float(LAMBDA_MAX_PHOTOLYSIS_NM["O3"]) * 1e-9
            e_ph = h * c / lam_m
            j_o3 = float(F_xuv_W_m2) / e_ph * float(SIGMA_A_M2["O3"])
        h2o = x_h2o * n_cm3
        co = max(x_co * n_cm3, 1.0)
        o3 = x_o3 * n_cm3
        m_eff = n_cm3
        oh = (
            2.0
            * K_O1D_H2O
            * h2o
            * j_o3
            * o3
            / ((K_O1D_H2O * h2o + K_O1D_M * m_eff) * K_OH_CO * co)
        )
        return {"regime": "oxidizing", "OH_cm3": float(oh), "H_cm3": None, "notes": ""}

    # reducing
    x_h2o = float(speciation.get("H2O", 0.0) or 0.0)
    j_h2o = float(photolysis_J.get("H2O", 0.0) or 0.0)
    h2o = x_h2o * n_cm3
    m_eff = n_cm3
    k5 = K_OH_H2 * math.exp(-1800.0 / float(T_K))
    h_rad = math.sqrt(max(0.0, j_h2o * h2o / (k5 * m_eff + 1e-300)))
    return {"regime": "reducing", "OH_cm3": None, "H_cm3": float(h_rad), "notes": ""}
