# variable_08_volatile_inventory/late_veneer.py
#
# Late accretion veneer mass and mantle volatile dilution.
#
# Formula: M_LV = M_kg × 10^(−2.3 + 0.3 × N(seed)); 80% EH3 / 20% CI mixing
# Source: Monte Carlo N-body simulations; Ru isotopic constraints for NC/CC ratio
# Earth calibration: M_LV/M_kg = 0.005 (geometric mean); X_mantle,H2O addition ~272−7 = 265 ppm
# Flag 115: log-normal μ=−2.3, σ=0.3 — N-body Monte Carlo calibration. Solar System calibration.
# Flag 116: 80/20 NC/CC mixing ratio — Ru isotopic anomaly constraint. Solar System specific.
# Flag 117: CI chondrite fractions — Wasson & Kallemeyn (1988), Lodders (2003). Multi-meteorite.
#
# Flag 133 — N post-veneer overshoot. 80/20 mixing ratio delivers ~6 ppm N vs 1–2 ppm MORB-source
# target. Atmosphere will be slightly N₂-richer than modern Earth. Model limitation — not patched.

import numpy as np

MU_LV = -2.3  # log10 mean late veneer fraction — Flag 115
SIGMA_LV = 0.3  # log10 std dev — Flag 115
F_CC = 0.20  # CC (CI) fraction — Flag 116
F_NC = 0.80  # NC (EH3) fraction — Flag 116

# CI chondrite elemental fractions — Flag 117
F_CI = {"H": 0.020, "C": 0.03220, "N": 0.00310, "S": 0.05410}

# EH3 fractions (dry, same as elemental_partitioning.py F_DRY)
F_EH3 = {"H": 8.0e-6, "C": 67.0e-6, "N": 8.0e-6, "S": 916.0e-6}

# Mixed veneer composition
F_LV = {el: F_CC * F_CI[el] + F_NC * F_EH3[el] for el in F_CI}


def compute_late_veneer(seed: int, M_kg: float, CMF: float, X_mantle: dict) -> dict:
    """Apply late veneer mass mixing; Ar unchanged (negligible veneer Ar)."""
    rng = np.random.default_rng(seed + 8_000_000)
    n = float(rng.standard_normal())
    m_lv = M_kg * 10.0 ** (MU_LV + SIGMA_LV * n)
    m_mantle = M_kg * (1.0 - CMF)
    ratio = m_lv / m_mantle if m_mantle > 0.0 else 0.0

    out = dict(X_mantle)
    out["X_mantle_H_ppm"] = out.get("X_mantle_H_ppm", 0.0) + F_LV["H"] * ratio * 1e6
    out["X_mantle_C_ppm"] = out.get("X_mantle_C_ppm", 0.0) + F_LV["C"] * ratio * 1e6
    out["X_mantle_N_ppm"] = out.get("X_mantle_N_ppm", 0.0) + F_LV["N"] * ratio * 1e6
    out["X_mantle_S_ppm"] = out.get("X_mantle_S_ppm", 0.0) + F_LV["S"] * ratio * 1e6
    # Ar: late veneer delivers negligible Ar; carry X_mantle_Ar unchanged
    out["M_LV_kg"] = m_lv
    return out
