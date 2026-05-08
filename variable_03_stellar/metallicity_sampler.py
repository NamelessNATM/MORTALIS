"""Stellar metallicity Z and elemental abundances (Flag 16 cascade-level)."""

from __future__ import annotations

# variable_03_stellar/metallicity_sampler.py
#
# Stellar metallicity Z and individual element abundances from cascade
# inputs. Closed-form derivation chain (Flag 16 cascade-level resolution).
#
# Sources:
#   - Linear AMR slope ∂[Fe/H]/∂τ = -0.057 dex/Gyr:
#       Feuillet et al. (2018), APOGEE-2 thin-disk red giants
#       (Multi-survey statistical fit)
#   - Linear AMR intercept 0.2622:
#       Calibration-anchored to Sun at τ = 4.6 Gyr → [Fe/H] = 0.
#       The [X/H] zero-point is by definition the Sun, so this anchor is
#       the [X/H] scale's definition, not an empirical fit to a planet.
#   - α/Fe piecewise slopes (-0.20 below solar, -0.10 at-or-above solar):
#       Multi-survey thin-disk Tinsley-Wallerstein consensus from APOGEE,
#       GALAH, Gaia-ESO loci. Specific named-fit citation pending.
#   - Trager A = 0.93:
#       Closed-form coefficient from solar α-element mass fraction
#       (Trager et al. 2000)
#   - PARSEC initial proto-solar values:
#       Z⊙_init = 0.01524, Y⊙_init = 0.273, (Z/X)⊙_init = 0.0214
#       (theoretical closed-form; required for downstream PARSEC
#       isochrone consistency in surface_gravity_evolution.py)
#   - Primordial helium Y_p = 0.2485:
#       Big Bang nucleosynthesis consensus
#       (multi-survey statistical fit)
#   - ΔY/ΔZ = (Y⊙_init − Y_p) / Z⊙_init = 1.6076:
#       Closed-form linear enrichment ratio
#
# ⚠️ Note 183: Linear AMR intercept calibration-anchored to Sun at
#   τ = 4.6 Gyr; this is the [X/H] zero-point definition, not an
#   empirical Solar System fit.
# ⚠️ Note 184: α/Fe piecewise slope discontinuity at [Fe/H] = 0 —
#   deterministic median-track approximation; smooth Tinsley-Wallerstein
#   locus replaced by piecewise linear.
# ⚠️ Note 185: AMR scatter ±0.15–0.20 dex (radial migration) suppressed
#   by the deterministic median track — inherent survey-scope limit;
#   the cascade's deterministic seed structure cannot represent
#   stochastic migration history.
# ⚠️ Flag 188: α/Fe piecewise slopes (-0.20, -0.10) attributed to
#   multi-survey thin-disk Tinsley-Wallerstein consensus; specific
#   named-fit citation pending verification.
# ⚠️ Flag 189: C, N, S age-dependent abundance derivations missing.
#   V08 elemental_partitioning.py currently uses EH3 chondrite
#   fallback fractions (Flags 107, 117). The new metallicity sampler
#   exposes [Fe/H] and [α/Fe], which is sufficient for Mg, Si, O
#   (α-elements) but not for C (AGB-dominated), N (AGB + CCSN), or
#   S (CCSN with different timescales). A follow-up research cycle
#   is required to derive C/N/S age-metallicity relations for the
#   thin disk and supersede the EH3 fallback.

# Solar / PARSEC anchor constants
_Z_SUN_INIT = 0.01524
_Y_SUN_INIT = 0.273
_Y_PRIMORD = 0.2485
_ZX_SUN_INIT = 0.0214
_DY_DZ = 1.6076  # (Y⊙_init − Y_p) / Z⊙_init

# Age-metallicity relation (Feuillet 2018 thin-disk fit, Sun-anchored intercept)
_AMR_SLOPE = -0.057  # dex Gyr⁻¹
_AMR_INTERCEPT = 0.2622  # dex (chosen so [Fe/H](4.6 Gyr) = 0)

# α/Fe piecewise slopes (multi-survey thin-disk consensus)
_ALPHA_SLOPE_NEG = -0.20  # for [Fe/H] < 0
_ALPHA_SLOPE_POS = -0.10  # for [Fe/H] ≥ 0

# Trager scaled-metallicity coefficient (closed-form from solar α-fraction)
_TRAGER_A = 0.93


def derive_metallicity(tau_gyr: float) -> dict:
    """
    Derive stellar metallicity Z and elemental abundances from stellar age.

    Parameters
    ----------
    tau_gyr : float
        Stellar age [Gyr], from the Just & Jahreiß SFH sampler in
        stellar_age_sampler.py.

    Returns
    -------
    dict with keys:
        Z       — metal mass fraction (dimensionless)
        Y       — helium mass fraction (dimensionless)
        X       — hydrogen mass fraction (dimensionless)
        FeH     — [Fe/H] in dex
        alphaFe — [α/Fe] in dex
        MH      — total scaled metallicity [M/H] in dex
        MgH     — [Mg/H] in dex
        SiH     — [Si/H] in dex
        OH      — [O/H] in dex

    Solar calibration (τ = 4.6 Gyr):
        [Fe/H] = 0.0000, [α/Fe] = 0.0000, [M/H] = 0.0000,
        Z = 0.01523 ≈ Z⊙_init = 0.01524, X+Y+Z = 1.0 (exact).

    Range across JJ2010 envelope (τ = 0.5–12 Gyr):
        [Fe/H] ∈ [+0.234, −0.422], Z ∈ [0.0240, 0.0071].
    """
    if tau_gyr < 0:
        raise ValueError("Stellar age must be non-negative.")

    # Step 1: linear age-metallicity relation
    FeH = _AMR_INTERCEPT + _AMR_SLOPE * tau_gyr

    # Step 2: piecewise α-enhancement
    if FeH < 0:
        alphaFe = _ALPHA_SLOPE_NEG * FeH
    else:
        alphaFe = _ALPHA_SLOPE_POS * FeH

    # Step 3: total scaled metallicity (Trager 2000)
    MH = FeH + _TRAGER_A * alphaFe

    # Step 4: scaling constant K = Z/X
    K = _ZX_SUN_INIT * 10.0**MH

    # Step 5: closed-form Z from K and linear He enrichment
    #   Y(Z) = Y_p + (ΔY/ΔZ) Z
    #   X(Z) = 1 − Y(Z) − Z = (1 − Y_p) − (1 + ΔY/ΔZ) Z
    #   Z = K · X(Z)  ⇒  Z = K(1 − Y_p) − K(1 + ΔY/ΔZ)·Z
    #   Z [1 + K(1 + ΔY/ΔZ)] = K(1 − Y_p)
    one_minus_Yp = 1.0 - _Y_PRIMORD  # 0.7515
    one_plus_dYdZ = 1.0 + _DY_DZ  # 2.6076
    Z = (one_minus_Yp * K) / (1.0 + one_plus_dYdZ * K)

    # Helium and hydrogen mass fractions
    Y = _Y_PRIMORD + _DY_DZ * Z
    X = 1.0 - Y - Z

    # Individual elemental abundances
    # In the local thin disk, Mg/Si/O track the α/Fe ratio with intrinsic
    # scatter ~0.03–0.04 dex (below cascade precision); treat as locked.
    MgH = alphaFe + FeH
    SiH = alphaFe + FeH
    OH = alphaFe + FeH

    return {
        "Z": Z,
        "Y": Y,
        "X": X,
        "FeH": FeH,
        "alphaFe": alphaFe,
        "MH": MH,
        "MgH": MgH,
        "SiH": SiH,
        "OH": OH,
    }

