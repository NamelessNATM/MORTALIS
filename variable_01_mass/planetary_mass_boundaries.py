# variable_01_mass/planetary_mass_boundaries.py
#
# PURPOSE: Compute the lower and upper physical boundaries of planetary mass.
#
# LOWER BOUNDARY — Hydrostatic Equilibrium Threshold (M_min)
# Formula: M_min = (9 / (2 * rho**2)) * (sigma_rbf / (pi * G))**(3/2)
# Derivation: Integrating the hydrostatic equation dP/dr = -rho*g(r) for a
# uniform sphere, the central pressure is P_c = (2/3)*pi*G*rho^2*R^2.
# Setting P_c equal to the material yield strength sigma_rbf and solving for R,
# then substituting into M = (4/3)*pi*R^3*rho yields M_min.
# Source: Lineweaver & Norman (2010); research session 2026-04-11 Section 7.
# Earth calibration: sigma_rbf=10e6 Pa, rho=3500 kg/m^3 -> M_min ~ 10^18-10^21 kg
# (boundary is soft and composition-dependent — see Flag 04 below)
#
# ⚠️ EARTH FALLBACK — sigma_rbf derived from terrestrial rock and ice mechanics.
# Universal applicability not confirmed. Flagged per Rule 3.
# Flag 04: yield strength of silicate rock (~10 MPa) and ice (~5 MPa) are
# Earth-measured laboratory values. M_min is therefore composition-dependent.
#
# UPPER BOUNDARY — Deuterium Burning Threshold (M_max)
# Value: 13 Jupiter masses = 13 * 1.8982e27 kg = 2.4677e28 kg
# Derivation: Numerical integration of stellar structure equations (hydrostatic
# equilibrium, mass conservation, energy transport, polytropic equation of state
# n=1.5) shows that central temperature T_c ~ 10^6 K required for deuterium
# fusion is reached at approximately 13 M_J before electron degeneracy halts
# contraction. Exact range is 11.0-16.3 M_J depending on metallicity.
# Source: Saumon & Marley (2008); Molliere & Mordasini (2012);
# research session 2026-04-11 Section 7.
#
# ⚠️ Flag 06: 13 M_J is a simulation-derived convention, not a closed-form
# derivable constant. Stored here as the standard astrophysical convention.
# Review if metallicity inputs become available in a later variable.

import math

# Fundamental physical constants (Rule 1 Category A)
G = 6.674e-11        # gravitational constant [m^3 kg^-1 s^-2]
PI = math.pi

# Jupiter mass — derived from observational astronomy, confirmed universally
M_JUPITER_KG = 1.8982e27  # kg

# ⚠️ EARTH FALLBACK — yield strength values from terrestrial measurements
SIGMA_RBF_ROCK_PA = 10e6   # Pa — silicate rock yield strength
SIGMA_RBF_ICE_PA  =  5e6   # Pa — water ice yield strength


def compute_m_min(rho_kg_m3: float, sigma_rbf_pa: float) -> float:
    """
    Compute the minimum planetary mass for hydrostatic equilibrium.

    Parameters
    ----------
    rho_kg_m3   : bulk density of the body [kg/m^3]
    sigma_rbf_pa: compressive yield strength of the material [Pa]
                  Use SIGMA_RBF_ROCK_PA for rocky bodies,
                  SIGMA_RBF_ICE_PA for icy bodies.

    Returns
    -------
    M_min [kg]
    """
    inner = sigma_rbf_pa / (PI * G)
    return (9.0 / (2.0 * rho_kg_m3**2)) * inner**1.5


def compute_m_max() -> float:
    """
    Return the upper planetary mass boundary (deuterium burning threshold).

    Returns
    -------
    M_max [kg] — 13 Jupiter masses (standard astrophysical convention)
    """
    return 13.0 * M_JUPITER_KG
