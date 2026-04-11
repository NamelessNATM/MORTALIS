# variable_05_kinematics/orbital_period.py
#
# PURPOSE: Compute orbital period from Kepler's third law.
#
# Formula: T = 2*pi * sqrt(a^3 / (mu_star + mu_planet))
#
# Derivation: Equating Newtonian gravitational force to centripetal
# acceleration for a two-body system, then extending to elliptical
# orbits via the vis-viva equation and conservation of angular momentum.
# The exact two-body form uses mu_star + mu_planet. For M_star >> M,
# this simplifies to mu_star alone, but the exact form is used here.
# Source: Newton (Principia, 1687); universal physical law.
#
# Earth calibration:
#   a = 1.496e11 m, mu_star = 1.327e20 m^3/s^2, mu_planet = 3.986e14 m^3/s^2
#   T = 2*pi * sqrt((1.496e11)^3 / (1.327e20 + 3.986e14))
#     = 2*pi * sqrt(3.348e33 / 1.327e20)
#     = 2*pi * 5.022e6 = 3.156e7 s = 365.3 days ✓

import math

PI = math.pi


def compute_orbital_period(a_m: float, mu_star: float,
                            mu_planet: float) -> float:
    """
    Orbital period T [s].

    Parameters
    ----------
    a_m       : semimajor axis [m]
    mu_star   : stellar gravitational parameter [m^3/s^2] from Variable 03
    mu_planet : planetary gravitational parameter [m^3/s^2] from Variable 01

    Returns
    -------
    T [s]
    """
    return 2.0 * PI * math.sqrt(a_m ** 3 / (mu_star + mu_planet))
