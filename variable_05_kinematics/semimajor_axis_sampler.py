# variable_05_kinematics/semimajor_axis_sampler.py
#
# PURPOSE: Deterministically sample semimajor axis from a regime-conditioned
# broken power-law distribution using inverse-CDF sampling.
#
# Distribution: dN/d(log a) ∝ a^beta, i.e. PDF f(a) ∝ a^(beta-1)
# Two-regime broken power law with break at a_break.
#
# Gas giants (0.1 to 20 M_J):
#   a_break = 1.8 AU, beta_1 = 0.95, beta_2 = -0.95
#   Source: Fernandes et al. (2019). Confirmed across Kepler + RV surveys.
#   Hot Jupiter override: 1% Bernoulli draw -> a = 0.045 AU (Flag 33).
#
# Rocky and sub-Neptune (all other non-dwarf regimes):
#   a_break = 0.1 AU, beta_1 = 0.38, beta_2 = 0.0 (log-uniform plateau)
#   Source: Hsu et al. (2019); Petigura et al. (2013). Kepler bias-corrected.
#
# Dwarf regime: uses rocky/sub-Neptune parameters (Flag 32).
#
# ⚠️ Flag 32: Rocky and dwarf planet semimajor axes use sub-Neptune
# distribution parameters (Hsu et al. 2019). No separate rocky-only or
# dwarf-only demographic fit exists at required precision.
# ⚠️ Flag 33: Hot Jupiter 1% Bernoulli override. Occurrence rate from
# Kepler/RV surveys of Sun-like stars. Not confirmed across all stellar
# mass ranges.
#
# PRNG: random.Random(seed + 2) — offset from mass (seed) and age (seed+1).
# Determinism guarantee: same seed always produces same semimajor axis.

import math
import random

AU_M = 1.496e11

# Gas giant parameters (Fernandes et al. 2019)
_GG_A_BREAK_M = 1.8 * AU_M
_GG_BETA_1 = 0.95
_GG_BETA_2 = -0.95
_GG_HJ_PROB = 0.01
_GG_HJ_A_M = 0.045 * AU_M

# Rocky / sub-Neptune / dwarf parameters (Hsu et al. 2019; Petigura et al. 2013)
_RD_A_BREAK_M = 0.1 * AU_M
_RD_BETA_1 = 0.38
_RD_BETA_2 = 0.0  # log-uniform plateau


def _segment_integral(beta: float, a_lo: float, a_hi: float,
                       amplitude: float = 1.0) -> float:
    """
    Integral of amplitude * a^(beta-1) from a_lo to a_hi.
    For beta != 0: amplitude * (a_hi^beta - a_lo^beta) / beta
    For beta == 0: amplitude * ln(a_hi / a_lo)
    """
    if abs(beta) < 1e-12:
        return amplitude * math.log(a_hi / a_lo)
    return amplitude * (a_hi ** beta - a_lo ** beta) / beta


def _sample_broken_powerlaw(u: float, a_in: float, a_max: float,
                              a_break: float, beta_1: float,
                              beta_2: float) -> float:
    """
    Inverse-CDF sample from a two-regime broken power-law PDF.

    Parameters
    ----------
    u       : uniform draw in [0, 1)
    a_in    : inner boundary [m]
    a_max   : outer boundary [m]
    a_break : break radius [m]
    beta_1  : power-law index, inner regime
    beta_2  : power-law index, outer regime

    Returns
    -------
    a [m]
    """
    # Clamp break to valid domain
    a_break_eff = max(a_in, min(a_break, a_max))

    # Amplitudes: inner A=1, outer A=a_break^(beta_1 - beta_2) for continuity
    if a_break_eff > a_in:
        amp_inner = 1.0
        i1 = _segment_integral(beta_1, a_in, a_break_eff, amp_inner)
    else:
        amp_inner = 1.0
        i1 = 0.0

    if a_max > a_break_eff:
        amp_outer = a_break_eff ** (beta_1 - beta_2) if a_break_eff > 0 else 1.0
        i2 = _segment_integral(beta_2, a_break_eff, a_max, amp_outer)
    else:
        amp_outer = 1.0
        i2 = 0.0

    total = i1 + i2
    assert total > 0.0, "Broken power-law CDF total must be positive"

    p_inner = i1 / total

    if u < p_inner:
        # Sample from inner regime
        target = u * total
        if abs(beta_1) < 1e-12:
            return a_in * math.exp(target / amp_inner)
        base = a_in ** beta_1 + target * beta_1 / amp_inner
        return max(a_in, base ** (1.0 / beta_1))
    else:
        # Sample from outer regime
        target = (u - p_inner) * total
        if abs(beta_2) < 1e-12:
            return a_break_eff * math.exp(target / amp_outer)
        base = a_break_eff ** beta_2 + target * beta_2 / amp_outer
        return max(a_break_eff, base ** (1.0 / beta_2))


def sample_semimajor_axis(seed: int, regime: str,
                           a_inner_m: float, a_outer_m: float) -> float:
    """
    Deterministically sample semimajor axis [m].

    Parameters
    ----------
    seed      : cascade integer seed
    regime    : one of dwarf, rocky, sub_neptune, gas_giant
    a_inner_m : inner boundary [m] — Roche limit from roche_limit.py
    a_outer_m : outer boundary [m] — disk outer boundary

    Returns
    -------
    a [m]
    """
    rng = random.Random(seed + 2)

    # Hot Jupiter override for gas giants
    if regime == 'gas_giant':
        u_hj = rng.random()
        if u_hj < _GG_HJ_PROB:
            return _GG_HJ_A_M
        u = rng.random()
        a_break = _GG_A_BREAK_M
        b1, b2 = _GG_BETA_1, _GG_BETA_2
    else:
        # rocky, sub_neptune, dwarf all use same parameters (Flag 32)
        u = rng.random()
        a_break = _RD_A_BREAK_M
        b1, b2 = _RD_BETA_1, _RD_BETA_2

    a_in = max(a_inner_m, 0.001 * AU_M)  # floor at 0.001 AU
    a_out = max(a_outer_m, a_in * 2.0)

    return _sample_broken_powerlaw(u, a_in, a_out, a_break, b1, b2)
