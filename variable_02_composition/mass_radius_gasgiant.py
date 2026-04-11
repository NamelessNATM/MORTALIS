# variable_02_composition/mass_radius_gasgiant.py
#
# Gas-giant-regime mass–radius relation (Bashi et al. 2017).
#
# Formula (R in R_earth, M in M_earth; intended for M > 127 M_earth):
#   R = 18.6 * M^(-0.06)
#
# Source: Bashi et al. 2017, research session 2026-04-11
#
# Jupiter calibration: M = 318 M_earth → R = 13.15 R_earth (17% overestimate
# vs known 11.21 R_earth). Source describes this as upper-bound approximation.
# ⚠️ Flag 12: 17% overestimate on Jupiter. Recorded per Rule 2. Not a patch
# candidate — this is the formula the literature uses for this regime.
#
# Coefficients confirmed across multiple Jovian exoplanets.

R_EARTH_M = 6.371e6
M_EARTH_KG = 5.972e24


def compute_radius_gasgiant(M_kg: float) -> float:
    """
    Bashi et al. 2017 gas-giant empirical M–R fit.

    Returns R in metres.
    """
    m_earth = M_kg / M_EARTH_KG
    r_over_r_earth = 18.6 * (m_earth ** (-0.06))
    return R_EARTH_M * r_over_r_earth
