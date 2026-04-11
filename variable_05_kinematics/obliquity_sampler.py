# variable_05_kinematics/obliquity_sampler.py
#
# PURPOSE: Deterministically sample planetary obliquity (axial tilt).
#
# Obliquity cannot be derived from cascade inputs. It is set by stochastic
# giant impacts during late-stage accretion and later modified by secular
# spin-orbit resonances and tidal dissipation. N-body collisional history
# is not recoverable from M, R, a, and e alone.
#
# Distribution: isotropic spin axis distribution -> cos(obliquity) sampled
# uniformly on [-1, 1], giving obliquity uniform on [0, 180] degrees.
# Source: Theoretical N-body accretion models (Agnor et al. 1999;
# Chambers 2001). Physically motivated for terrestrial planets.
#
# ⚠️ Flag 36: Isotropic obliquity distribution is theoretically motivated
# but unconfirmed observationally for exoplanets. Exoplanet obliquity
# measurements are currently unavailable for most systems.
#
# PRNG: random.Random(seed + 4).
#
# Earth calibration: Earth's obliquity is 23.4 degrees, produced by the
# Moon-forming impact. This is one specific outcome of the isotropic
# distribution, not a central value.

import math
import random


def sample_obliquity(seed: int) -> float:
    """
    Deterministically sample planetary obliquity [degrees].

    Parameters
    ----------
    seed : cascade integer seed

    Returns
    -------
    obliquity_deg [degrees], in [0, 180]
    """
    rng = random.Random(seed + 4)
    cos_obl = rng.uniform(-1.0, 1.0)
    return math.degrees(math.acos(cos_obl))
