# variable_03_stellar/main_sequence_lifetime.py
#
# Simplified main-sequence lifetime scaling. Metallicity-dependent Hurley (2000)
# grids are deferred.
#
# ⚠️ Flag 16 (cascade-level resolved, source-side residual open):
#   Stellar metallicity Z is now exposed by the cascade via
#   metallicity_sampler.py. The simplified t_MS = 10 (M★/M☉)^−2.5 Gyr
#   formula remains in place pending a follow-up scaffold that imports
#   the Hurley, Pols & Tout (2000) Z-dependent analytical formulation
#   in full. Z is available in the V03 outputs as 'Z' for the future
#   rewrite.

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
