# variable_03_stellar/t_bgb.py
#
# Time to the base of the giant branch (t_BGB) — Hurley, Pols & Tout (2000)
# rational polynomial in M_star (Eq. 4) with metallicity-dependent
# coefficients (Eq. 1, Table 1).
#
# Source: Hurley J.R., Pols O.R., Tout C.A. (2000), MNRAS 315, 543
#         "Comprehensive analytic formulae for stellar evolution as a
#          function of mass and metallicity". Equation 4.
#
# Coefficient values: verbatim from the SSE Fortran source distribution
#   (zdata.h, xt array indices 1-17), the canonical implementation by
#   the original authors. Mirror verified at:
#     https://github.com/ahwkuepper/mcluster/blob/master/zdata.h
#   Cross-referenced against the published HPT2000 Table 1 structure.
#
# Calibration validated against:
#   M=1.0, Z=0.01524 (PARSEC solar):  t_BGB = 10729 Myr
#   M=1.0, Z=0.02 (HPT2000 native):   t_BGB = 11582 Myr  (matches paper)
#   M=8.0, Z=0.01524:                 t_BGB =    37.79 Myr (canonical CCSN)
#   M=25,  Z=0.01524:                 t_BGB =     7.08 Myr (canonical Pols
#                                                           1998 grids)
#
# Asymptotic high-mass nuclear-timescale floor: 1/a5 = 1/0.3426 = 2.92 Myr.

"""t_BGB(M, Z) — Hurley 2000 Eq. 4 rational polynomial."""

from __future__ import annotations
from math import log10

# Verbatim coefficients from SSE zdata.h xt(1)-xt(17).
# Each a_n (for n=1..4) is a cubic polynomial in lzs = log10(Z/0.02):
#     a_n = alpha_n + beta_n*lzs + gamma_n*lzs^2 + eta_n*lzs^3
# a_5 is constant in lzs.

_a1_alpha, _a1_beta, _a1_gamma, _a1_eta = 1.593890e+3, 2.053038e+3, 1.231226e+3, 2.327785e+2
_a2_alpha, _a2_beta, _a2_gamma, _a2_eta = 2.706708e+3, 1.483131e+3, 5.772723e+2, 7.411230e+1
_a3_alpha, _a3_beta, _a3_gamma, _a3_eta = 1.466143e+2, -1.048442e+2, -6.795374e+1, -1.391127e+1
_a4_alpha, _a4_beta, _a4_gamma, _a4_eta = 4.141960e-2, 4.564888e-2, 2.958542e-2, 5.571483e-3
_a5_const = 3.426349e-1

_Z_REF_SSE = 0.02   # HPT2000 reference solar metallicity (NOT modified for PARSEC; see Note)


def t_bgb(M_star_solar: float, Z: float) -> float:
    """
    Time to the base of the giant branch [Myr] from HPT2000 Eq. 4.

    Parameters
    ----------
    M_star_solar : float
        Stellar mass [M_sun]. Validated 0.1 <= M <= 50 M_sun in HPT2000;
        cascade Kroupa range 0.179 <= M <= 31 sits inside.
    Z : float
        Metal mass fraction (PARSEC scale Z⊙_init = 0.01524 ok). SSE
        validity range 0.0001 <= Z <= 0.03; cascade typical range
        0.007–0.024 sits inside; extreme cases up to ~0.04 are mild
        polynomial extrapolations.

    Returns
    -------
    t_BGB : float
        Time to base of giant branch [Myr].
    """
    if M_star_solar <= 0.0:
        raise ValueError("Stellar mass must be positive.")
    if Z <= 0.0:
        raise ValueError("Metallicity Z must be positive.")

    lzs = log10(Z / _Z_REF_SSE)

    # Coefficient assembly (HPT2000 Eq. 1)
    a1 = _a1_alpha + lzs * (_a1_beta + lzs * (_a1_gamma + lzs * _a1_eta))
    a2 = _a2_alpha + lzs * (_a2_beta + lzs * (_a2_gamma + lzs * _a2_eta))
    a3 = _a3_alpha + lzs * (_a3_beta + lzs * (_a3_gamma + lzs * _a3_eta))
    a4 = _a4_alpha + lzs * (_a4_beta + lzs * (_a4_gamma + lzs * _a4_eta))
    a5 = _a5_const

    # Eq. 4: t_BGB rational polynomial
    M = M_star_solar
    M2 = M * M
    M4 = M2 * M2
    M55 = M**5.5
    M7 = M2 * M2 * M2 * M

    numerator   = a1 + a2 * M4 + a3 * M55 + M7
    denominator = a4 * M2 + a5 * M7

    return numerator / denominator
