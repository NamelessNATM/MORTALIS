# variable_03_stellar/stellar_radius_highmass.py
#
# Torres (2010) gravitational identity verified on eclipsing binaries; Moya et al.
# (2018) extended samples. High-mass radius is tied to log g★, not an empirical
# mass–radius polynomial (MTR excised from this path).
#
# ⚠️ Flag 24: Mass–temperature-radius polynomial (MTR) is not used on the
# high-mass radius path; radius follows from M and log g★.

"""High-mass stellar radius from the Torres (2010) identity (Flag 24)."""

from __future__ import annotations

import math

_LOG_G_SUN = 4.438  # cgs, IAU 2015 nominal
_R_SUN_M = 6.957e8


def compute_radius_highmass(m_star_solar: float, log_g: float) -> tuple[float, float]:
    """
    log10(R★/R☉) = 0.5·log10(M★/M☉) − 0.5·(log g★ − log g☉).

    Exact rearrangement of g = G M / R² in solar-normalised logarithmic form.

    Valid for M★ > 1.5 M☉. Calibration examples:

    - Sirius A: M = 2.063, log g = 4.33 → R = 1.626 R☉ (known 1.711, −4.9 % ✓)
    - Fomalhaut: M = 1.920, log g = 4.21 → R = 1.801 R☉ (known 1.842, −2.2 % ✓)
    - Vega: M = 2.135, log g = 4.10 → R = 2.156 R☉ (known 2.362, −8.7 %;
      residual from oblate geometry ✓)
    """
    m = m_star_solar
    if m <= 1.5:
        raise ValueError(
            f"Torres identity branch applies for M★ > 1.5 M☉; got {m} M☉."
        )
    log_r = 0.5 * math.log10(m) - 0.5 * (log_g - _LOG_G_SUN)
    r_solar = 10.0**log_r
    return r_solar, r_solar * _R_SUN_M
