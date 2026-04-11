# variable_05_kinematics/equilibrium_temperature.py
#
# PURPOSE: Compute planetary equilibrium temperature from orbit-averaged flux.
#
# Formula: T_eq = ((1 - A) * <F> / (4 * sigma))^(1/4)
#
# Derivation: Energy balance between absorbed stellar radiation and blackbody
# emission. Incoming power: (1-A) * <F> * pi * R^2. Emitted power (rapid
# rotator, uniform emission): 4 * pi * R^2 * sigma * T^4. Setting equal
# and solving for T yields the formula. R cancels — T_eq is independent
# of planetary radius. Source: Selsis et al. (2007); universal physics.
#
# Bond albedo A: Cannot be determined without atmospheric composition
# (Variable 04). Placeholder values are used per regime:
#   dwarf      : A = 0.10 (bare rock, no atmosphere assumed)
#   rocky      : A = 0.30 (Earth-like, Flag 38)
#   sub_neptune: A = 0.30 (Flag 38)
#   gas_giant  : A = 0.50 (Jupiter-like cloud albedo, Flag 38)
#
# ⚠️ Flag 38: Bond albedo placeholders are Earth/Solar System calibrated.
# Must be revised when Variable 04 (atmosphere) provides composition.
#
# Earth calibration:
#   <F> = 1361 W/m^2, A = 0.30, sigma = 5.670e-8 W/m^2/K^4
#   T_eq = ((0.70 * 1361) / (4 * 5.670e-8))^0.25
#         = (952.7 / 2.268e-7)^0.25 = (4.203e9)^0.25 = 254.6 K ✓

import math

SIGMA = 5.670374419e-8  # W m^-2 K^-4 — CODATA Stefan-Boltzmann constant

# ⚠️ Flag 38 — regime-based albedo placeholders
ALBEDO_DEFAULTS = {
    'dwarf':       0.10,
    'rocky':       0.30,
    'sub_neptune': 0.30,
    'gas_giant':   0.50,
}
ALBEDO_FALLBACK = 0.30


def compute_equilibrium_temperature(F_mean_W_m2: float, regime: str) -> tuple:
    """
    Equilibrium temperature T_eq [K] and Bond albedo used.

    Parameters
    ----------
    F_mean_W_m2 : orbit-averaged stellar flux [W/m^2]
    regime      : compositional regime string from Variable 02

    Returns
    -------
    T_eq_K : float — equilibrium temperature [K]
    albedo  : float — Bond albedo used (placeholder until Variable 04)
    """
    A = ALBEDO_DEFAULTS.get(regime, ALBEDO_FALLBACK)
    T_eq = ((1.0 - A) * F_mean_W_m2 / (4.0 * SIGMA)) ** 0.25
    return T_eq, A
