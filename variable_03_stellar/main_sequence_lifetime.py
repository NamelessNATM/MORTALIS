# variable_03_stellar/main_sequence_lifetime.py
#
# Simplified main-sequence lifetime scaling. Metallicity-dependent Hurley (2000)
# grids are deferred.
#
# ⚠️ Flag 16: Hurley precision lifetime model deferred (metallicity-dependent).

"""Simplified main-sequence lifetime (Flag 16)."""

from __future__ import annotations


def compute_main_sequence_lifetime(m_star_solar: float) -> float:
    """
    t_MS = 10 (M★/M☉)^−2.5 Gyr.

    Solar calibration: M★ = 1 M☉ → 10.0 Gyr.
    """
    m = m_star_solar
    if m <= 0.0:
        raise ValueError("Mass must be positive.")
    return 10.0 * (m ** (-2.5))
