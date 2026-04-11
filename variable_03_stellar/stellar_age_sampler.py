# variable_03_stellar/stellar_age_sampler.py
#
# Just & Jahreiß (2010) Model A SFH in the Milky Way solar neighbourhood.
#
# ⚠️ Flag 22: JJ2010 parameters are empirically fitted to a single measurement
# context (solar neighbourhood SFH).
# ⚠️ Flag 23: τ_min(M★) Keplerian assembly anchor is a Solar System / chronometry
# fallback, not a general galactic constraint.
# ⚠️ Flag 15: Stellar age is resolved by sampling the JJ2010 SFH (inverse transform).
# τ_max uses a simplified MS lifetime capped at t_p; metallicity-dependent Hurley
# (2000) precision is deferred (see Flag 16 in main_sequence_lifetime.py).

"""Stellar age sampling from Just & Jahreiß (2010) Model A (Flags 15, 22, 23)."""

from __future__ import annotations

import math
import random

from scipy.optimize import brentq

# JJ2010 Model A — single solar-neighbourhood context (Flag 22)
_T0 = 5.6   # Gyr — shape parameter
_T1 = 8.2   # Gyr — shape parameter
# t_n = 9.9 Gyr appears in JJ2010 as a constant SFR prefactor; it cancels in the CDF ratio.
_T_P = 12.0  # Gyr — present-day thin-disk age


def _tau_min_gyr(m_solar: float) -> float:
    """Keplerian assembly floor [Gyr]; Solar System / Hf–W anchor (Flag 23)."""
    return 0.1 * (m_solar ** (-0.5))


def _tau_max_gyr(m_solar: float) -> float:
    """Simplified MS lifetime cap [Gyr]; metallicity precision deferred (Flag 16)."""
    return min(10.0 * (m_solar ** (-2.5)), _T_P)


def _I_of_t(t: float) -> float:
    """
    Antiderivative I(t) for the JJ2010 Model A SFR integrand (same t units as paper).

    I(t) = [t0·t − t1²] / [2·t1²·(t² + t1²)] + t0/(2·t1³) · arctan(t/t1)
    """
    t1_sq = _T1 * _T1
    denom = 2.0 * t1_sq * (t * t + t1_sq)
    term_a = (_T0 * t - t1_sq) / denom
    term_b = (_T0 / (2.0 * _T1**3)) * math.atan(t / _T1)
    return term_a + term_b


def sample_stellar_age(seed: int, m_star_solar: float) -> tuple[float, float]:
    """
    Deterministic stellar age τ [Gyr] and fractional MS age τ_frac ∈ [0, 1].

    Uses birth-time coordinate t with τ = t_p − t, inverse-CDF via brentq.
    PRNG: ``random.Random(seed + 1)`` (offset from mass seed).

    Solar calibration (M★ = 1 M☉): τ_min = 0.1 Gyr, τ_max = 10.0 Gyr,
    t_start = 2.0 Gyr, t_end = 11.9 Gyr. For U = 0.5 (median uniform draw on the
    truncated JJ2010 CDF), numerical inversion gives τ ≈ 6.58 Gyr under the
    stated I(t) and bounds (verified; ~t0 is a shape parameter, not the median age).
    """
    m = m_star_solar
    tau_min = _tau_min_gyr(m)
    tau_max = _tau_max_gyr(m)
    t_end = _T_P - tau_min
    t_start = max(0.0, _T_P - tau_max)

    i_start = _I_of_t(t_start)
    i_end = _I_of_t(t_end)
    c_integral = i_end - i_start
    assert c_integral > 0.0, "JJ2010 truncated CDF width must be positive"

    rng = random.Random(seed + 1)
    u = rng.random()
    target = u * c_integral + i_start

    def f_root(t: float) -> float:
        return _I_of_t(t) - target

    t_sample = brentq(f_root, t_start, t_end, xtol=1e-9, rtol=1e-9)
    age_gyr = _T_P - t_sample

    denom = tau_max - tau_min
    if denom <= 0.0:
        tau_frac = 0.0
    else:
        tau_frac = (age_gyr - tau_min) / denom
    tau_frac = max(0.0, min(1.0, tau_frac))

    return age_gyr, tau_frac
