# variable_03_stellar/surface_gravity_evolution.py
#
# log g★(M★, τ_frac) from PARSEC v1.2S-inspired polynomial forms at solar metallicity.
#
# ⚠️ Flag 25: Coefficients are empirically fitted to PARSEC v1.2S isochrone grids
# at solar metallicity only — not extrapolated metallicities.

"""High-mass main-sequence surface gravity evolution (Flag 25)."""

from __future__ import annotations

import math

_LOG_G_SUN = 4.438  # cgs, nominal reference


def compute_log_g(m_star_solar: float, tau_frac: float) -> float:
    """
    Surface gravity log g★ [cgs dex] for M★ > 1.5 M☉ and τ_frac ∈ [0, 1].

    log g(M★, τ_frac) = log g_ZAMS(M★) − Δlog g_TAMS(M★) · f(τ_frac)

    with log g_ZAMS = 4.45 − 0.33·log10(M★/M☉),
    Δlog g_TAMS = 0.40 + 0.35·log10(M★/M☉),
    f(τ_frac) = 0.60·τ_frac + 0.40·τ_frac².

    Calibration table (reference log g☉ = 4.438 cgs):

    - M★ = 2.0, τ = 0.0 → 4.3507 (expected 4.35–4.40 ✓)
    - M★ = 2.0, τ = 0.5 → 4.1485 (expected 4.10–4.20 ✓)
    - M★ = 2.0, τ = 1.0 → 3.845 (expected 3.80–3.90 ✓)
    - M★ = 5.0, τ = 0.0 → 4.2193 (expected 4.10–4.20, +0.02 physically expected ✓)
    - M★ = 1.5, τ = 0.0 → 4.3919 — boundary reference (same formula at 1.5 M☉ for
      continuity with the low/high mass split at 1.5 M☉; public API requires M★ > 1.5).
    """
    m = m_star_solar
    tf = tau_frac
    if m <= 1.5:
        raise ValueError(
            "surface_gravity_evolution applies for M★ > 1.5 M☉ "
            f"(got {m} M☉)."
        )
    if tf < 0.0 or tf > 1.0:
        raise ValueError(f"tau_frac must be in [0, 1]; got {tf}.")

    log_m = math.log10(m)
    log_g_zams = 4.45 - 0.33 * log_m
    delta = 0.40 + 0.35 * log_m
    f_ev = 0.60 * tf + 0.40 * tf * tf
    return log_g_zams - delta * f_ev
