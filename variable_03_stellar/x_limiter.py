# variable_03_stellar/x_limiter.py
#
# Main-sequence fractional duration limiter x — verbatim from the SSE
# Fortran source (zcnsts.f, zpars(8)). This is the form actually used
# in the canonical SSE implementation; it differs from the form
# published in HPT2000 paper Eq. 6 (which used lzs) by being a piecewise
# function in Z directly. Both forms produce nearly identical results
# in the cascade's operational Z range (0.007–0.024); the SSE source
# form is adopted as the canonical implementation.
#
# Source: SSE Fortran source distribution, zcnsts.f line for zpars(8).
#         Mirror at https://github.com/ahwkuepper/mcluster/blob/master/zcnsts.f
#
# Calibration (verbatim test cases):
#   Z = 0.001  -> x = 0.98
#   Z = 0.005  -> x = 0.967
#   Z = 0.01   -> x = 0.95
#   Z = 0.01524 -> x = 0.95
#   Z = 0.02   -> x = 0.95
#   Z = 0.04   -> x = 0.95

"""x-limiter for HPT2000 t_MS (SSE Fortran source form)."""

from __future__ import annotations


def x_limiter(Z: float) -> float:
    """
    Main-sequence fractional duration limiter x [dimensionless].

    For low-mass stars without a convective-core hook,
    t_MS = x * t_BGB.

    Parameters
    ----------
    Z : float
        Metal mass fraction.

    Returns
    -------
    x : float
        Fractional limiter, bounded in [0.95, 0.99].
    """
    if Z <= 0.0:
        raise ValueError("Metallicity Z must be positive.")

    inner_min = min(0.99, 0.98 - (100.0 / 7.0) * (Z - 0.001))
    inner_max = max(0.95 - (10.0 / 3.0) * (Z - 0.01), inner_min)
    return max(0.95, inner_max)
