# variable_05_kinematics/roche_limit.py
#
# PURPOSE: Compute the fluid Roche limit — the inner boundary of stable orbits.
#
# Formula: a_Roche = 2.44 * R_star * (rho_star / rho_planet)^(1/3)
#
# Derivation: From fluid mechanics, tidal forces overcome self-gravity at the
# radius where the Roche lobe equals the body's physical radius. The coefficient
# 2.44 is derived from the fluid (not rigid) body Roche limit and applies to
# all planetary bodies. Source: Roche (1849); confirmed universally across
# planetary bodies and binary star systems.
#
# Stellar density rho_star = M_star / ((4/3) pi R_star^3) — Rule 1 Category B.
#
# Earth/Sun calibration:
#   R_star = 6.957e8 m, M_star = 1.989e30 kg -> rho_star = 1409 kg/m^3
#   rho_planet = 5514 kg/m^3 (Earth mean density)
#   a_Roche = 2.44 * 6.957e8 * (1409/5514)^(1/3)
#            = 1.697e9 * 0.6349 = 1.077e9 m = 0.0072 AU
#   Earth orbit at 1 AU is well outside this. Physically sensible.

import math

PI = math.pi
COEFF = 2.44  # fluid Roche limit coefficient — universal (Roche 1849)


def compute_roche_limit(R_star_m: float, M_star_kg: float,
                         rho_planet_kg_m3: float) -> float:
    """
    Fluid Roche limit [m].

    Parameters
    ----------
    R_star_m        : stellar radius [m] from Variable 03
    M_star_kg       : stellar mass [kg] from Variable 03
    rho_planet_kg_m3: mean bulk density of planet [kg/m^3] from Variable 02

    Returns
    -------
    a_Roche [m]
    """
    V_star = (4.0 / 3.0) * PI * R_star_m ** 3
    rho_star = M_star_kg / V_star
    return COEFF * R_star_m * (rho_star / rho_planet_kg_m3) ** (1.0 / 3.0)
