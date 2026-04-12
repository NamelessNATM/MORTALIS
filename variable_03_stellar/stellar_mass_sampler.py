# variable_03_stellar/stellar_mass_sampler.py
#
# Kroupa (2001) broken power-law IMF, inverse transform on integer seed.
#
# Literature IMF integration limits M_min = 0.01 M☉ and M_max = 150 M☉ are
# standard conventions (empirically established, not first-principles). This
# cascade renormalises the same piecewise ξ(m) on the draw interval
# (0.179, 31] M☉ so bolometric luminosity from Eker et al. (2018) remains in
# calibration; regime-1 masses are therefore not realised here, but k_i and α
# follow the full three-segment Kroupa construction.
#
# ⚠️ Flag 20: Kroupa alpha exponents are empirically fitted, confirmed across
# multiple star-forming regions and the Galactic field.

"""Stellar mass sampling from the Kroupa (2001) IMF (Flag 20)."""

from __future__ import annotations

import random

# Literature Kroupa breakpoints [M☉] (used for continuity of k_i)
_M0, _M1, _M2, _M3 = 0.01, 0.08, 0.50, 150.0
_ALPHAS = (0.3, 1.3, 2.3)

# Draw interval — Eker et al. (2018) MLR domain (open at lower bound in MLR)
_DRAW_LO = 0.179
_DRAW_HI = 31.0

_STABILITY_BOUNDS = {
    'stable':         (0.5,  1.5),
    'unstable_low':   (0.179, 0.5),
    'unstable_high':  (1.5,  31.0),
}

# Continuity: ξ_i(m) = k_i m^{-α_i}; match at each internal boundary.
_K1 = 1.0
_K2 = _K1 * (_M1 ** (_ALPHAS[1] - _ALPHAS[0]))
_K3 = _K2 * (_M2 ** (_ALPHAS[2] - _ALPHAS[1]))

_M_SUN_KG = 1.989e30


def _segment_weight(k: float, alpha: float, m_lo: float, m_hi: float) -> float:
    """∫ k m^{-α} dm = k/(1-α) * (m_hi^{1-α} - m_lo^{1-α}); α ≠ 1."""
    one_minus_alpha = 1.0 - alpha
    return (k / one_minus_alpha) * (m_hi**one_minus_alpha - m_lo**one_minus_alpha)


def _build_truncated_segments(
    draw_lo: float, draw_hi: float
) -> list[tuple[float, float, float, float]]:
    """Intersect each Kroupa regime with [draw_lo, draw_hi]; drop empties."""
    raw = [
        (_K1, _ALPHAS[0], _M0, _M1),
        (_K2, _ALPHAS[1], _M1, _M2),
        (_K3, _ALPHAS[2], _M2, _M3),
    ]
    out: list[tuple[float, float, float, float]] = []
    for k, alpha, m_lo, m_hi in raw:
        lo = max(m_lo, draw_lo)
        hi = min(m_hi, draw_hi)
        if lo < hi:
            out.append((k, alpha, lo, hi))
    assert out, "Truncated IMF must contain at least one segment"
    return out


def _build_cdf_tables(
    draw_lo: float, draw_hi: float
) -> tuple[
    list[float], list[float], list[float], list[float], list[float]
]:
    segments = _build_truncated_segments(draw_lo, draw_hi)
    weights = [_segment_weight(k, a, lo, hi) for k, a, lo, hi in segments]
    w_sum = sum(weights)
    assert w_sum > 0.0

    cumulative: list[float] = []
    acc = 0.0
    for w in weights:
        acc += w / w_sum
        cumulative.append(acc)

    assert abs(cumulative[-1] - 1.0) <= 1e-10, f"CDF tail must be 1.0, got {cumulative[-1]}"

    m_lo = [s[2] for s in segments]
    m_hi = [s[3] for s in segments]
    k_vals = [s[0] for s in segments]
    alphas = [s[1] for s in segments]
    return m_lo, m_hi, k_vals, alphas, cumulative


_M_LO, _M_HI, _K_SEG, _ALPHA_SEG, _CDF_EDGES = _build_cdf_tables(_DRAW_LO, _DRAW_HI)

# Earth/Solar calibration: 1 M☉ must lie in regime 3 (m ≥ 0.50, α = 2.3)
assert 1.0 >= _M2


def sample_stellar_mass(seed: int,
                        stability: str | None = None) -> tuple[float, float]:
    """
    Deterministically sample stellar mass from the truncated Kroupa (2001) IMF.

    Parameters
    ----------
    seed : int
        Integer seed; uses ``random.Random(seed)`` for U ∈ [0, 1).
    stability : str or None
        Optional stability key to clamp the draw interval before CDF build.

    Returns
    -------
    M_star_solar : float
        Mass in solar masses.
    M_star_kg : float
        Mass in kg (M_sun = 1.989e30 kg).
    """
    draw_lo = _DRAW_LO
    draw_hi = _DRAW_HI

    if stability is not None:
        bounds = _STABILITY_BOUNDS.get(stability)
        if bounds is None:
            raise ValueError(f"Unknown stability for stellar mass conditioning: '{stability}'")
        draw_lo = max(_DRAW_LO, bounds[0])
        draw_hi = min(_DRAW_HI, bounds[1])
        if draw_lo >= draw_hi:
            raise ValueError(
                f"Conditioned stellar mass range [{draw_lo}, {draw_hi}] is empty "
                f"for stability '{stability}'."
            )

    if stability is None:
        m_lo_list = _M_LO
        m_hi_list = _M_HI
        k_seg = _K_SEG
        alpha_seg = _ALPHA_SEG
        cdf_edges = _CDF_EDGES
    else:
        m_lo_list, m_hi_list, k_seg, alpha_seg, cdf_edges = _build_cdf_tables(
            draw_lo, draw_hi
        )

    rng = random.Random(seed)
    u = rng.random()

    f_prev = 0.0
    seg_idx = len(cdf_edges) - 1
    for i, f_edge in enumerate(cdf_edges):
        if u <= f_edge:
            seg_idx = i
            break
        f_prev = f_edge

    m_lo = m_lo_list[seg_idx]
    m_hi = m_hi_list[seg_idx]
    k = k_seg[seg_idx]
    alpha = alpha_seg[seg_idx]
    one_minus_alpha = 1.0 - alpha

    p_seg = cdf_edges[seg_idx] - f_prev
    if p_seg <= 0.0:
        u_local = 0.0
    else:
        u_local = (u - f_prev) / p_seg
        if u_local >= 1.0:
            u_local = 1.0 - 1e-15
        if u_local <= 0.0:
            u_local = 1e-15

    t_lo = m_lo**one_minus_alpha
    t_hi = m_hi**one_minus_alpha
    t_m = t_lo + u_local * (t_hi - t_lo)
    m_star = t_m ** (1.0 / one_minus_alpha)

    m_kg = m_star * _M_SUN_KG
    return m_star, m_kg
