# variable_06_tectonics/cmb_pressure.py
#
# FORMULA (analytically integrated from dP/dr = -rho(r)*g(r)):
#   P_cmb = G * rho_mantle * M_core * (1/R_core - 1/R)
#           + (4*pi/3) * G * rho_mantle**2
#             * (R**2/2 - 3*R_core**2/2 + R_core**3/R)
#
# SOURCE: V06 Follow-Up A, Question A2. Hydrostatic equilibrium integrated
#         analytically across the mantle layer assuming uniform density per layer.
#         Formula was reconstructed from the provided derivation steps because the
#         research response was truncated; reconstruction validated numerically.
#
# ⚠️ INHERENT MODEL LIMITATION — uniform-density-per-layer assumption ignores
# self-compression. Introduces ~9.5% underestimate at Earth conditions. Flag 51.
#
# EARTH CALIBRATION:
#   M_core ≈ 1.94e24 kg, R_core ≈ 3.487e6 m, R = 6.37e6 m,
#   rho_mantle ≈ 4457 kg/m³
#   P_cmb ≈ 123 GPa  (target 136 GPa; 9.5% error from uniform-density assumption) ✓

import math

from constants import G


def compute_cmb_pressure(
    R: float,
    R_core: float,
    M: float,
    CMF: float,
    rho_mantle: float,
) -> float:
    """
    Compute core-mantle boundary pressure via hydrostatic integration.

    Parameters
    ----------
    R          : float — planetary radius [m]
    R_core     : float — core radius [m]
    M          : float — planetary mass [kg]
    CMF        : float — core mass fraction [dimensionless]
    rho_mantle : float — mean mantle density [kg/m³]

    Returns
    -------
    P_cmb : float — pressure at core-mantle boundary [Pa]
    """
    M_core = CMF * M

    part1 = G * rho_mantle * M_core * (1.0 / R_core - 1.0 / R)
    part2 = (4.0 * math.pi / 3.0) * G * rho_mantle**2 * (
        R**2 / 2.0 - 3.0 * R_core**2 / 2.0 + R_core**3 / R
    )

    return part1 + part2
