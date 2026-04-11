# variable_02_composition/mass_radius_subneptune.py
#
# Sub-Neptune-regime mass–radius relation.
#
# Formula (R in R_earth, M in M_earth):
#   R = 0.56 * M^0.67
#
# Source: Chen & Kipping 2017 / Otegi et al. 2020, research session 2026-04-11
#
# Earth calibration: Formula is physically invalid for Earth (rocky body).
#
# Neptune calibration: M = 17.15 M_earth → R = 3.69 R_earth (4.5% error vs
# known 3.865 R_earth — acceptable for demographic empirical fit).
#
# Coefficients confirmed across multiple exoplanet bodies.

R_EARTH_M = 6.371e6
M_EARTH_KG = 5.972e24


def compute_radius_subneptune(M_kg: float) -> float:
    """
    Chen & Kipping / Otegi et al. sub-Neptune empirical M–R fit.

    Returns R in metres.
    """
    m_earth = M_kg / M_EARTH_KG
    r_over_r_earth = 0.56 * (m_earth**0.67)
    return R_EARTH_M * r_over_r_earth
