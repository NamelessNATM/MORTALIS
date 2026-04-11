# variable_03_stellar/mass_luminosity.py
#
# Eker et al. (2018) six-regime piecewise mass–luminosity relation from 509
# detached eclipsing binaries. Coefficients are empirically fitted and confirmed
# across multiple systems. No numbered cascade flag applies.

"""Bolometric luminosity from stellar mass (Eker et al. 2018)."""

from __future__ import annotations

import math

_L_SUN_W = 3.828e26

# (m_lo, m_hi, alpha, C) with log10(L/Lsun) = alpha * log10(M/Msun) + C
_MLR_REGIMES: tuple[tuple[float, float, float, float], ...] = (
    (0.179, 0.45, 2.028, -0.976),
    (0.45, 0.72, 4.572, -0.102),
    (0.72, 1.05, 5.743, -0.007),
    (1.05, 2.40, 4.329, 0.010),
    (2.40, 7.00, 3.967, 0.093),
    (7.00, 31.0, 2.865, 1.105),
)


def compute_stellar_luminosity(m_star_solar: float) -> tuple[float, float]:
    """
    Bolometric luminosity from Eker et al. (2018) piecewise MLR.

    Solar calibration: M★ = 1 M☉ lies in (0.72, 1.05]; log10(L/L☉) =
    5.743·0 − 0.007 = −0.007 → L ≈ 0.984 L☉ (~−1.6 % vs 1 L☉). The small
    negative offset is expected within empirical MLR scatter and band stitching.

    Parameters
    ----------
    m_star_solar : float
        Stellar mass [M☉].

    Returns
    -------
    L_star_solar : float
        Luminosity in solar units.
    L_star_W : float
        Luminosity [W]; L_sun = 3.828e26 W.
    """
    m = m_star_solar
    if m <= 0.179 or m > 31.0:
        raise ValueError(
            f"Mass {m} M☉ is outside the Eker et al. (2018) MLR domain "
            "(require 0.179 < M/M☉ ≤ 31)."
        )
    for m_lo, m_hi, alpha, c in _MLR_REGIMES:
        if m_lo < m <= m_hi:
            log_l = alpha * math.log10(m) + c
            l_solar = 10.0**log_l
            return l_solar, l_solar * _L_SUN_W
    raise ValueError(f"Mass {m} M☉ fell outside all MLR segments (logic error).")
