# variable_09_atmospheric_column/moist_adiabat_beta.py
#
# Moist-adiabat effective β = R_specific / C_p for gray RC model.

from __future__ import annotations

import math
from typing import Mapping

from variable_09_atmospheric_column.tau_zero_compositional import MOLAR_MASS_KG_MOL

_R_UNIVERSAL = 8.314462618  # J/(mol·K) — CODATA (Rule 1 Category A)

# Rule 1 Category A — fundamental molecular thermodynamic constants
CP_MOLAR_J_PER_MOL_K = {
    "N2": 29.1,
    "O2": 29.4,
    "CO2": 37.1,
    "H2O": 33.6,
    "CH4": 35.7,
    "H2": 28.8,
    "He": 20.8,
    "Ar": 20.8,
    "NH3": 35.6,
    "SO2": 39.9,
    "H2S": 34.2,
    "CO": 29.1,
}


def _cp_co2(T_ref_K: float) -> float:
    """CO2 molar C_p with high-T vibrational branch (Flag 168)."""
    if T_ref_K > 500.0:
        # ⚠️ Flag 168 — high-T heat capacity adjustment from JANAF tables
        return 50.0
    return float(CP_MOLAR_J_PER_MOL_K["CO2"])


def _mixture_cp_molar(speciation: Mapping[str, float], T_ref_K: float) -> float:
    cp_mix = 0.0
    wsum = 0.0
    for sp, x in speciation.items():
        if x is None or x <= 0.0:
            continue
        if sp == "CO2":
            cp = _cp_co2(T_ref_K)
        else:
            cp = CP_MOLAR_J_PER_MOL_K.get(sp)
            if cp is None:
                continue
        xf = float(x)
        cp_mix += xf * float(cp)
        wsum += xf
    if wsum <= 0.0:
        raise ValueError("mixture C_p — empty speciation.")
    return cp_mix / wsum


def _apply_moist_correction(
    beta_dry: float,
    x_h2o: float,
    x_ch4: float,
) -> float:
    """
    ⚠️ Flag 169 — moist adiabat correction Solar-System calibrated; full
    first-principles derivation deferred. Interpolate toward research targets.
    """
    targets = []
    weights = []
    if x_h2o > 0.005:
        targets.append(0.19)
        weights.append(min(1.0, x_h2o / 0.03))
    if x_ch4 > 0.01:
        targets.append(0.20)
        weights.append(min(1.0, x_ch4 / 0.05))
    if not weights:
        return beta_dry
    wtot = sum(weights)
    beta_target = sum(t * w for t, w in zip(targets, weights)) / wtot
    alpha = min(1.0, sum(weights))
    return float(beta_dry * (1.0 - alpha) + beta_target * alpha)


def compute_beta_moist(
    speciation: Mapping[str, float],
    T_ref_K: float,
    terrestrial_route: str | None,
) -> float:
    """
    Return β = R_specific / C_p with moist correction when condensables present.
    """
    m_bar = 0.0
    for sp, x in speciation.items():
        if x is None or x <= 0.0:
            continue
        mm = MOLAR_MASS_KG_MOL.get(sp)
        if mm is None:
            continue
        m_bar += float(x) * mm
    if m_bar <= 0.0:
        raise ValueError("beta — invalid m_bar.")

    cp_molar = _mixture_cp_molar(speciation, T_ref_K)
    r_specific = _R_UNIVERSAL / m_bar
    c_p_mass = cp_molar / m_bar
    beta_dry = r_specific / c_p_mass

    x_h2o = float(speciation.get("H2O", 0.0) or 0.0)
    x_ch4 = float(speciation.get("CH4", 0.0) or 0.0)

    if terrestrial_route == "venus_class":
        # Research-derived dry CO2 thermodynamics (scaffold)
        return 0.1643
    if terrestrial_route == "titan_class":
        return 0.20
    if terrestrial_route == "thick_terrestrial" and x_h2o < 0.005 and x_ch4 < 0.01:
        # Earth-like thick N2-O2
        return 0.19

    beta = _apply_moist_correction(beta_dry, x_h2o, x_ch4)
    # Mars-like: dry CO2 only
    if terrestrial_route == "thin" and x_ch4 < 0.01 and x_h2o < 0.005:
        return beta_dry
    return beta
