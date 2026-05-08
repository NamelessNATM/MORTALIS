# variable_03_stellar/main_sequence_lifetime.py
#
# Stellar main-sequence lifetime t_MS(M, Z) — Hurley, Pols & Tout (2000)
# closed-form analytical formulation. Replaces the prior simplified
# scaling t_MS = 10 (M*/M_sun)^-2.5 Gyr that ignored metallicity.
#
# Closes Flag 16 fully:
#   - cascade-level Z exposure: completed in Phase A (metallicity_sampler.py)
#   - source-side Hurley residual: completed in Phase B (this rewrite)
#
# Source: Hurley J.R., Pols O.R., Tout C.A. (2000), MNRAS 315, 543.
#         t_MS = max(t_hook, x * t_BGB)  (Eq. 5)
#
# Notes attached at this layer (added at implementation time, see below):
#   - Note 190: HPT2000 polynomial fits to Pols 1998 detailed tracks
#                achieve RMS error 1.9% per the original paper.
#   - Note 191: SSE Z-validity range 0.0001 <= Z <= 0.03. Cascade
#                typical Z (0.007–0.024) sits inside. Extreme tail at
#                Z ~ 0.04 is mild polynomial extrapolation.
#   - Note 192: t_MS returned is the nuclear timescale at the surface
#                mass given. Wind mass loss (Vink, Wolf-Rayet, rotation)
#                is not modelled. For 25 M_sun stars without winds,
#                t_MS ≈ 7 Myr; with realistic winds, observational
#                lifetime can shorten to ~3–5 Myr. The cascade does
#                not currently model post-formation mass loss; t_MS at
#                face value is the answer.
#   - Note 193: Verbatim primary-source coefficients; values from
#                SSE Fortran zdata.h, mirrored at mcluster repository,
#                cross-referenced to HPT2000 Table 1 structure.

"""Stellar main-sequence lifetime t_MS(M, Z) — Hurley 2000."""

from __future__ import annotations

from .t_bgb import t_bgb
from .t_hook_fraction import t_hook_fraction
from .x_limiter import x_limiter

_MYR_PER_GYR = 1000.0


def main_sequence_lifetime(M_star_solar: float, Z: float) -> float:
    """
    Main-sequence lifetime [Gyr] from Hurley, Pols & Tout (2000).

    t_MS = max(t_hook, x * t_BGB)
        where t_hook = m(M, Z) * t_BGB(M, Z)
        and   x      = x_limiter(Z)

    Parameters
    ----------
    M_star_solar : float
        Stellar mass [M_sun]. Cascade Kroupa range 0.179 <= M <= 31.
    Z : float
        Metal mass fraction at formation. Cascade typical range
        ~0.007–0.024 from the JJ2010 SFH-driven AMR; PARSEC initial
        proto-solar Z⊙_init = 0.01524 is the calibration anchor.

    Returns
    -------
    t_MS : float
        Main-sequence lifetime [Gyr].

    Calibration (PARSEC solar Z = 0.01524):
        M = 0.5 M_sun:  t_MS ≈ 123 Gyr  (>> Hubble time; expected)
        M = 1.0 M_sun:  t_MS ≈ 10.2 Gyr (canonical solar)
        M = 1.5 M_sun:  t_MS ≈ 2.58 Gyr
        M = 8.0 M_sun:  t_MS ≈ 37.7 Myr  (CCSN progenitor)
        M = 25  M_sun:  t_MS ≈ 7.07 Myr  (canonical Pols 1998 grids,
                                          no wind treatment)
    """
    t_BGB_myr = t_bgb(M_star_solar, Z)            # Myr
    m         = t_hook_fraction(M_star_solar, Z)  # dimensionless
    x         = x_limiter(Z)                       # dimensionless

    t_hook_myr = m * t_BGB_myr
    t_MS_myr   = max(t_hook_myr, x * t_BGB_myr)

    return t_MS_myr / _MYR_PER_GYR
