# variable_03_stellar/t_hook_fraction.py
#
# Fractional t_hook / t_BGB ratio (m parameter) — Hurley, Pols & Tout
# (2000) Eq. 7 with metallicity-dependent coefficients a6-a10.
#
# Physical purpose: For stars with convective cores (above ~1.2 M_sun
# for solar-Z, lower for higher-Z), the main-sequence terminus is
# marked by a rapid contraction "hook" feature. m captures the
# fractional duration of t_hook relative to t_BGB.
#
# Source: Hurley J.R., Pols O.R., Tout C.A. (2000), MNRAS 315, 543,
#         Equation 7. Coefficient values verbatim from SSE Fortran
#         source xt(18)-xt(31).
#
# Calibration:
#   M=0.5,  Z=0.01524: m = 0.500 (floor; star has radiative core,
#                                  hook does not apply)
#   M=1.0,  Z=0.01524: m ≈ 0.81
#   M=1.5,  Z=0.01524: m ≈ 0.97
#   M=8.0,  Z=0.01524: m ≈ 0.997 (full convective-core regime)
#   M=25,   Z=0.01524: m ≈ 0.999

"""m(M, Z) — HPT2000 Eq. 7 t_hook fractional duration."""

from __future__ import annotations
from math import log10

# Verbatim coefficients from SSE zdata.h xt(18)-xt(31).
_a6_alpha, _a6_beta, _a6_gamma, _a6_eta = 1.949814e+1, 1.758178e+0, -6.008212e+0, -4.470533e+0
_a7_const = 4.903830e+0
_a8_alpha, _a8_beta, _a8_gamma, _a8_eta = 5.212154e-2, 3.166411e-2, -2.750074e-3, -2.271549e-3
_a9_alpha, _a9_beta, _a9_gamma, _a9_eta = 1.312179e+0, -3.294936e-1, 9.231860e-2, 2.610989e-2
_a10_const = 8.073972e-1

_Z_REF_SSE = 0.02


def t_hook_fraction(M_star_solar: float, Z: float) -> float:
    """
    Fractional t_hook / t_BGB ratio [dimensionless] from HPT2000 Eq. 7.

    Parameters
    ----------
    M_star_solar : float
        Stellar mass [M_sun].
    Z : float
        Metal mass fraction.

    Returns
    -------
    m : float
        Fractional t_hook duration. m * t_BGB = t_hook in Myr.
    """
    if M_star_solar <= 0.0:
        raise ValueError("Stellar mass must be positive.")
    if Z <= 0.0:
        raise ValueError("Metallicity Z must be positive.")

    lzs = log10(Z / _Z_REF_SSE)

    a6  = _a6_alpha + lzs * (_a6_beta + lzs * (_a6_gamma + lzs * _a6_eta))
    a7  = _a7_const
    a8  = _a8_alpha + lzs * (_a8_beta + lzs * (_a8_gamma + lzs * _a8_eta))
    a9  = _a9_alpha + lzs * (_a9_beta + lzs * (_a9_gamma + lzs * _a9_eta))
    a10 = _a10_const

    inner_left  = a6 / M_star_solar**a7
    inner_right = a8 + a9 / M_star_solar**a10

    return max(0.5, 1.0 - 0.01 * max(inner_left, inner_right))
