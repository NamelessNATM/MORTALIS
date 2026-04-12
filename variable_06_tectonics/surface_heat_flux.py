# variable_06_tectonics/surface_heat_flux.py
#
# FORMULAS:
#
#   Stagnant lid (Ra < Ra_c or tectonic_regime == 'stagnant_lid'):
#     Nu  = A_p * (Ra / Ra_c)^(1/3) * theta^(-4/3)   [Solomatov 1995]
#     q_s = k * DeltaT / D * Nu
#
#   Mobile lid (tectonic_regime == 'mobile_lid'):
#     Nu  = A_mob * Ra^(1/3)                           [isoviscous scaling]
#     q_s = k * DeltaT / D * Nu
#
#   Sluggish lid (tectonic_regime == 'sluggish_lid'):
#     Nu  = A_mob * Ra^(1/3)                           [mobile approximation, Flag 64]
#     q_s = k * DeltaT / D * Nu
#
#   Conductive (Ra < Ra_c, no convection):
#     q_s = k * DeltaT / D
#
# SOURCE:
#   Stagnant lid: Solomatov (1995). Exponents 1/3 and -4/3 universal (fluid mechanics).
#   Mobile lid: isoviscous boundary layer theory. Universal exponent 1/3.
#   A_p and A_mob: empirically calibrated — see flags below.
#
# ⚠️ EARTH FALLBACK — A_mob = 0.122. Derived from Earth calibration constraint:
#   q_s = 47 TW for Earth inputs (T_m=1650 K, T_eq=255 K, D=2.878e6 m, Ra=8.58e7).
#   Within the numerically established range 0.1-0.2. Flag 62.
#
# ⚠️ EARTH FALLBACK — A_p = 0.50. Mid-point of 0.47-0.53 range from numerical
#   convection simulations (Solomatov 1995). No planetary calibration available —
#   Earth is not a stagnant lid planet. Flag 63.
#
# ⚠️ EARTH FALLBACK — k = 3.5 W/(m*K). Terrestrial silicate calibration.
#
# ⚠️ APPROXIMATION — Sluggish lid uses mobile lid formula. No separate
#   transitional scaling implemented. Flag 64.
#
# EARTH CALIBRATION (mobile lid — Earth):
#   Ra = 8.58e7, DeltaT = 1395 K, D = 2.878e6 m
#   Nu  = 0.122 * (8.58e7)^(1/3) = 0.122 * 443.4 = 54.1
#   q_s = 3.5 * 1395/2.878e6 * 54.1 = 0.0920 W/m²
#   Global integral = 46.98 TW  (target 47 ± 2 TW) ✓

import math

_K = 3.5  # thermal conductivity [W/(m*K)] — ⚠️ EARTH FALLBACK
_A_P = 0.50  # stagnant lid prefactor [dimensionless] — ⚠️ EARTH FALLBACK Flag 63
_A_MOB = 0.122  # mobile/sluggish lid prefactor [dimensionless] — ⚠️ EARTH FALLBACK Flag 62


def compute_nusselt(
    Ra: float,
    Ra_c: float,
    theta: float,
    tectonic_regime: str,
    convecting: bool,
) -> float:
    """
    Compute Nusselt number from Rayleigh number using regime-appropriate scaling.

    Parameters
    ----------
    Ra               : float — Rayleigh number
    Ra_c             : float — critical Rayleigh number
    theta            : float — Frank-Kamenetskii parameter (stagnant lid only)
    tectonic_regime  : str   — 'stagnant_lid', 'mobile_lid', or 'sluggish_lid'
    convecting       : bool  — True if Ra > Ra_c

    Returns
    -------
    Nu : float — Nusselt number (>= 1.0)
    """
    if not convecting or Ra <= Ra_c:
        return 1.0  # purely conductive

    if tectonic_regime == "stagnant_lid":
        if theta <= 0.0:
            return 1.0
        Nu = _A_P * (Ra / Ra_c) ** (1.0 / 3.0) * theta ** (-4.0 / 3.0)
    else:
        # mobile_lid or sluggish_lid (Flag 64: sluggish uses mobile approximation)
        Nu = _A_MOB * Ra ** (1.0 / 3.0)

    return max(1.0, Nu)  # Nu < 1 is physically impossible


def compute_surface_heat_flux(
    T_m: float,
    T_eq: float,
    D: float,
    Ra: float = None,
    Ra_c: float = None,
    theta: float = None,
    tectonic_regime: str = "stagnant_lid",
    convecting: bool = True,
) -> tuple:
    """
    Compute surface heat flux and Nusselt number using regime-appropriate formula.

    Parameters
    ----------
    T_m              : float — mantle temperature [K]
    T_eq             : float — surface equilibrium temperature [K]
    D                : float — mantle depth [m]
    Ra               : float — Rayleigh number
    Ra_c             : float — critical Rayleigh number
    theta            : float — Frank-Kamenetskii parameter
    tectonic_regime  : str   — 'stagnant_lid', 'mobile_lid', or 'sluggish_lid'
    convecting       : bool  — True if Ra > Ra_c

    Returns
    -------
    (q_s, Nu) : tuple of (float, float)
        q_s : surface heat flux [W/m²]
        Nu  : Nusselt number [dimensionless]
    """
    delta_T = max(T_m - T_eq, 0.0)
    q_cond = _K * delta_T / D  # conductive baseline

    if not convecting or Ra is None or Ra <= Ra_c:
        return q_cond, 1.0

    Nu = compute_nusselt(Ra, Ra_c, theta, tectonic_regime, convecting)
    q_s = q_cond * Nu
    return q_s, Nu
