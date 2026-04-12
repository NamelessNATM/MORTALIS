# variable_06_tectonics/radiogenic_heating.py
#
# FORMULA:
#   H_rad(t) = M_mantle * sum_i( C_i * h_i * exp(-t / tau_i) )
#
# ISOTOPES: 40K, 232Th, 235U, 238U
#
# SOURCE: V06 Follow-Up B, Question B3.
#   h_i, tau_i: immutable nuclear physics constants — UNIVERSAL.
#   C_i: bulk silicate Earth initial concentrations — EARTH FALLBACK (Flag 55).
#
# CONSTANTS (per isotope):
#   C_i  [kg/kg]     — initial mass concentration in bulk silicate Earth
#   h_i  [W/kg]      — specific heat production per unit isotope mass
#   tau_i [Gyr → s]  — mean lifetime = half-life / ln(2)
#
# ⚠️ EARTH FALLBACK on C_i — BSE-calibrated concentrations. Galactic chemical
# evolution controls r-process abundances (U, Th). Planets orbiting stars with
# different nucleosynthetic histories will have different budgets. Flag 55.
#
# EARTH CALIBRATION:
#   M_mantle ≈ 4.03e24 kg, t = 4.5 Gyr → H_rad ≈ 19.8 TW (target 20–24 TW) ✓

import math

# [C_i kg/kg, h_i W/kg, tau_i Gyr]
# ⚠️ C_i values are EARTH FALLBACK — Flag 55
_ISOTOPES = [
    {"name": "40K", "C": 355e-9, "h": 29.2e-6, "tau_Gyr": 1.80},
    {"name": "232Th", "C": 100e-9, "h": 26.4e-6, "tau_Gyr": 20.20},
    {"name": "235U", "C": 11.8e-9, "h": 569.0e-6, "tau_Gyr": 1.015},
    {"name": "238U", "C": 39.8e-9, "h": 94.6e-6, "tau_Gyr": 6.45},
]


def compute_radiogenic_heating(M_mantle: float, t_Gyr: float) -> float:
    """
    Compute current radiogenic heat production in the silicate mantle.

    Parameters
    ----------
    M_mantle : float — mantle mass [kg]
    t_Gyr    : float — system age [Gyr]

    Returns
    -------
    H_rad : float — radiogenic heat production [W]
    """
    H_rad = 0.0
    for iso in _ISOTOPES:
        H_rad += (
            M_mantle
            * iso["C"]
            * iso["h"]
            * math.exp(-t_Gyr / iso["tau_Gyr"])
        )
    return H_rad
