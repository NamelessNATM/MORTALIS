# variable_03_stellar/mass_radius_lowmass.py
#
# Eker et al. (2018) quadratic mass–radius relation (M★ ≤ 1.5 M☉). Empirically
# fitted across 509 detached eclipsing binaries. No numbered cascade flag applies.

"""Low-mass stellar radius from Eker et al. (2018)."""

from __future__ import annotations

_R_SUN_M = 6.957e8


def compute_radius_lowmass(m_star_solar: float) -> tuple[float, float]:
    """
    Stellar radius for M★ ≤ 1.5 M☉ (Eker et al. 2018).

    R★/R☉ = 0.438 (M★/M☉)² + 0.479 (M★/M☉) + 0.075

    Solar calibration: M★ = 1 → R★/R☉ = 0.438 + 0.479 + 0.075 = 0.992 (~−0.8 %).

    Parameters
    ----------
    m_star_solar : float
        Stellar mass [M☉].

    Returns
    -------
    R_star_solar : float
        Radius in solar units.
    R_star_m : float
        Radius [m].
    """
    m = m_star_solar
    if m > 1.5:
        raise ValueError(
            f"Low-mass MRR applies for M★ ≤ 1.5 M☉; got {m} M☉."
        )
    r_solar = 0.438 * m * m + 0.479 * m + 0.075
    return r_solar, r_solar * _R_SUN_M
