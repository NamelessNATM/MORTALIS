# variable_05_kinematics/orbital_eccentricity_sampler.py
#
# PURPOSE: Deterministically sample orbital eccentricity.
#
# Distribution: Beta(alpha=0.867, beta=3.03) for a >= 0.1 AU.
# Source: Kipping (2013), bias-corrected eccentricity distribution from
# radial velocity exoplanet survey. Confirmed across multiple RV surveys
# with significant scatter.
#
# Tidal circularisation: for a < 0.1 AU, eccentricity is damped to 0.0.
# Physical basis: tidal dissipation timescale << system age for short-period
# planets. Threshold 0.1 AU is empirically established across Solar System
# and exoplanet populations.
#
# Stability check: if periapsis a*(1-e) < a_inner (Roche limit), eccentricity
# is reduced until periapsis equals a_inner. This prevents orbits that would
# cause tidal disruption at closest approach.
#
# ⚠️ Flag 37: Beta distribution parameters (alpha=0.867, beta=3.03) from
# Kipping (2013). Fitted to RV survey. Confirmed across multiple surveys
# but with significant scatter at high eccentricity.
#
# PRNG: random.Random(seed + 3).

import random

AU_M = 1.496e11

_ALPHA = 0.867   # ⚠️ Flag 37 — Kipping (2013) empirical parameter
_BETA  = 3.03    # ⚠️ Flag 37 — Kipping (2013) empirical parameter
_TIDAL_CIRCULARISATION_AU = 0.1  # AU — empirical threshold


def _sample_beta(rng: random.Random, alpha: float, beta: float) -> float:
    """
    Sample from Beta(alpha, beta) using Python stdlib random.betavariate.
    """
    return rng.betavariate(alpha, beta)


def sample_eccentricity(seed: int, a_m: float, a_inner_m: float) -> float:
    """
    Deterministically sample orbital eccentricity.

    Parameters
    ----------
    seed      : cascade integer seed
    a_m       : semimajor axis [m]
    a_inner_m : Roche limit [m] — periapsis stability floor

    Returns
    -------
    e [dimensionless, 0 to <1]
    """
    rng = random.Random(seed + 3)

    a_au = a_m / AU_M

    if a_au < _TIDAL_CIRCULARISATION_AU:
        return 0.0

    e = _sample_beta(rng, _ALPHA, _BETA)

    # Enforce periapsis stability: a*(1-e) >= a_inner
    if a_m > 0.0 and a_inner_m > 0.0:
        e_max = 1.0 - (a_inner_m / a_m)
        e_max = max(0.0, min(e_max, 0.999))
        e = min(e, e_max)

    return e
