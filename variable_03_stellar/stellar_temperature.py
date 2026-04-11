# variable_03_stellar/stellar_temperature.py
#
# Stefan–Boltzmann effective temperature from L and R. Sole T_eff path for both
# mass regimes — empirical mass–temperature relations are not used here.
#
# ⚠️ Flag 24: MTR-based temperature is excised; T_eff follows L and R only.

"""Effective temperature from the Stefan–Boltzmann law (Flag 24)."""

from __future__ import annotations

import math

_SIGMA = 5.670374419e-8  # W m^-2 K^-4 (CODATA)


def compute_temperature(l_star_w: float, r_star_m: float) -> float:
    """
    T_eff = (L★ / (4π R★² σ))^(1/4).

    Solar calibration: L = 3.828e26 W, R = 6.957e8 m → T_eff ≈ 5772 K.

    Parameters
    ----------
    l_star_w : float
        Bolometric luminosity [W].
    r_star_m : float
        Stellar radius [m].

    Returns
    -------
    float
        Effective temperature [K].
    """
    if r_star_m <= 0.0 or l_star_w < 0.0:
        raise ValueError("L must be non-negative and R must be positive.")
    denom = 4.0 * math.pi * r_star_m * r_star_m * _SIGMA
    return (l_star_w / denom) ** 0.25
