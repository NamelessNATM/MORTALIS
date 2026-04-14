# variable_08_volatile_inventory/bulk_volatile_fraction.py
#
# Bulk silicate volatile fraction from logistic snow-line crossing.
#
# Formula: X_vol = X_dry + Σ X_max,i / (1 + exp(−0.44 × (a_m − R_snow,i) / R_H))
# Source: logistic snow-line model; k=0.44 from 10 R_H oligarchic feeding zone (Kokubo & Ida 1998)
# Earth calibration: a=1 AU inside H2O snow line → X_vol ≈ X_dry = 1e-3
# Flag 101: X_dry = 1e-3 — EH3 enstatite chondrite hydration. Solar System meteoritic. Earth fallback.
# Flag 105: k = 0.44 — oligarchic feeding zone width. Solar System calibrated. Earth fallback.
# Flag 106: X_max values from Lodders (2003) protosolar abundances. Solar-metallicity calibration.

import math

X_DRY = 1.0e-3  # ⚠️ Flag 101 — EH3 chondrite baseline
K_STEEP = 0.44  # ⚠️ Flag 105 — logistic steepness
X_MAX = {  # ⚠️ Flag 106 — Lodders (2003)
    "H2O": 0.45,
    "CO2": 0.10,
    "N2": 0.02,
}


def _logistic(a_m: float, r_snow_m: float, r_h_m: float) -> float:
    if r_h_m <= 0.0:
        return 0.0
    z = -K_STEEP * (a_m - r_snow_m) / r_h_m
    z = min(max(z, -700.0), 700.0)
    return 1.0 / (1.0 + math.exp(z))


def compute_bulk_volatile_fraction(a_m: float, R_H_m: float, snow_lines: dict) -> dict:
    """Bulk volatile mass fraction and per-species ice contributions (logistic terms)."""
    x_ice_h2o = X_MAX["H2O"] * _logistic(a_m, snow_lines["R_snow_H2O_m"], R_H_m)
    x_ice_co2 = X_MAX["CO2"] * _logistic(a_m, snow_lines["R_snow_CO2_m"], R_H_m)
    x_ice_n2 = X_MAX["N2"] * _logistic(a_m, snow_lines["R_snow_N2_m"], R_H_m)
    x_vol = X_DRY + x_ice_h2o + x_ice_co2 + x_ice_n2
    return {
        "X_vol": x_vol,
        "X_ice_H2O": x_ice_h2o,
        "X_ice_CO2": x_ice_co2,
        "X_ice_N2": x_ice_n2,
    }
