# variable_02_composition/mass_radius_rocky.py
#
# Rocky-regime mass–radius relation (Zeng et al. 2016).
#
# Formula (all dimensionless ratios unless noted):
#   R/R_earth = (1.07 - 0.21 * CMF) * (M/M_earth)^(1/3.7)
#   R — planetary radius [m]
#   M — planetary mass (input M_kg) [kg]
#   CMF — Core Mass Fraction, dimensionless in [0, 1]; valid range for fit ~0–0.4
#
# Coefficients 1.07, 0.21, and exponent 1/3.7 are empirical, calibrated to Earth
# interior models (PREM seismic data) only — Rule 3.
#
# Source: Zeng et al. 2016, research session 2026-04-11
#
# Earth calibration: M = 1 M_earth, CMF = 0.325 → R = 1.00175 R_earth
# (0.17% error vs 1 R_earth).
#
# ⚠️ EARTH FALLBACK — coefficients derived from PREM (Earth seismic data only).
# Universal applicability not confirmed. Flag 09.
#
# ⚠️ Flag 07: CMF defaults to 0.325 (Earth value). No disk chemistry variable
# yet in cascade. Deferred.

R_EARTH_M = 6.371e6
M_EARTH_KG = 5.972e24
DEFAULT_CMF = 0.325


def compute_radius_rocky(M_kg: float, CMF: float = DEFAULT_CMF) -> float:
    """
    Zeng et al. 2016 rocky mass–radius relation.

    Returns R in metres.
    """
    m_ratio = M_kg / M_EARTH_KG
    factor = (1.07 - 0.21 * CMF) * (m_ratio ** (1.0 / 3.7))
    return R_EARTH_M * factor
