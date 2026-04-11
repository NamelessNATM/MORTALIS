# variable_05_kinematics/atmospheric_escape.py
#
# PURPOSE: Compute energy-limited atmospheric mass loss rate.
#
# Formula: M_dot = epsilon * pi * R_XUV^3 * F_XUV / (G * M)
#
# Derivation: Energy-limited escape assumes a fixed fraction epsilon of
# absorbed XUV energy is converted to PdV work lifting gas out of the
# gravity well. Watson et al. (1981); Owen & Wu (2017).
#
# epsilon: XUV heating efficiency. Empirical. Earth/Venus/Mars suggest
# 0.1 to 0.3. Midpoint 0.15 used as default.
# ⚠️ Flag 34: epsilon is Solar System calibrated only. Non-universal.
#
# R_XUV: radius at which atmosphere is optically thick to XUV.
# Approximated as R for dense terrestrial planets, 1.1*R for
# gas giants and sub-Neptunes. Empirical, not derived.
# ⚠️ Flag 35: R_XUV approximation is empirical, not derived.
#
# Earth calibration:
#   G = 6.674e-11, M = 5.972e24 kg, R = 6.371e6 m
#   F_XUV at 1 AU ~ 0.005 W/m^2, epsilon = 0.15, R_XUV = R
#   M_dot = 0.15 * pi * (6.371e6)^3 * 0.005 / (6.674e-11 * 5.972e24)
#          = 0.15 * pi * 2.585e20 * 0.005 / 3.985e14
#          = 0.15 * 4.061e18 / 3.985e14
#          = 1529 kg/s ~ 4.8e10 kg/yr
#   Modern Earth hydrogen escape ~ 3 kg/s (atmosphere nearly fully retained).
#   Discrepancy expected — early Earth had much higher F_XUV; formula
#   represents maximum energy-limited rate, not current rate.

import math

G = 6.674e-11  # m^3 kg^-1 s^-2

# ⚠️ Flag 34 — Solar System calibrated only
EPSILON_DEFAULT = 0.15

# ⚠️ Flag 35 — empirical R_XUV multipliers per regime
R_XUV_MULTIPLIER = {
    'dwarf':       1.0,
    'rocky':       1.0,
    'sub_neptune': 1.1,
    'gas_giant':   1.1,
}
R_XUV_FALLBACK = 1.0


def compute_atmospheric_escape(F_XUV_W_m2: float, R_m: float,
                                 M_kg: float, regime: str) -> float:
    """
    Energy-limited atmospheric mass loss rate M_dot [kg/s].

    Parameters
    ----------
    F_XUV_W_m2 : orbit-averaged XUV flux [W/m^2] from stellar_flux.py
    R_m        : planetary radius [m] from Variable 02
    M_kg       : planetary mass [kg] from Variable 01
    regime     : compositional regime string from Variable 02

    Returns
    -------
    M_dot [kg/s]
    """
    mult = R_XUV_MULTIPLIER.get(regime, R_XUV_FALLBACK)
    R_xuv = R_m * mult
    return (EPSILON_DEFAULT * math.pi * R_xuv ** 3 * F_XUV_W_m2) / (G * M_kg)
