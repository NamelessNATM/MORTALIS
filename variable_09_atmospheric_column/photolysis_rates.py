# variable_09_atmospheric_column/photolysis_rates.py
#
# Gray-band photolysis rates at top of atmosphere (Scaffold §12.1).

from __future__ import annotations

import math
from typing import Mapping

# ⚠️ Flag 171 — wavelength cutoffs (JPL DE 2020).
LAMBDA_MAX_PHOTOLYSIS_NM = {
    "N2": 127,
    "CH4": 145,
    "CO2": 227,
    "NH3": 230,
    "H2O": 240,
    "O2": 242,
    "H2S": 260,
    "SO2": 390,
    "O3": 1100,
}

# ⚠️ Flag 172 — effective broadband cross-sections (gray approximation).
SIGMA_A_M2 = {
    "H2O": 5e-22,
    "CO2": 1e-23,
    "SO2": 1e-22,
    "H2S": 5e-22,
    "CH4": 2e-21,
    "NH3": 5e-21,
    "N2": 1e-25,
    "O2": 1e-23,
    "O3": 1e-21,
}


def compute_photolysis_rates_toa(
    speciation: Mapping[str, float],
    F_xuv_W_m2: float,
    tau_uv_top: float = 0.0,
) -> dict[str, float]:
    """
    J_i ≈ (F_XUV / hν_avg) · σ_a · exp(-τ_uv) at TOA.

    ⚠️ Flag 173 — gray photolysis approximation.
    """
    h = 6.62607015e-34
    c = 2.99792458e8
    out: dict[str, float] = {}
    for sp, x in speciation.items():
        if x is None or x <= 0.0:
            continue
        lam_nm = LAMBDA_MAX_PHOTOLYSIS_NM.get(sp)
        sig = SIGMA_A_M2.get(sp)
        if lam_nm is None or sig is None:
            continue
        lam_m = float(lam_nm) * 1e-9
        e_ph = h * c / lam_m
        j = float(F_xuv_W_m2) / e_ph * float(sig) * math.exp(-float(tau_uv_top))
        out[sp] = j
    return out
