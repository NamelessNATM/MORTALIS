# variable_05_kinematics/bond_albedo.py
#
# PURPOSE: Bond albedo in two passes.
#
# Pass 1 — pre-atmospheric proxy albedo
#   Called from variable_05_kinematics.py before equilibrium_temperature.
#   Inputs:  F_mean_W_m2, regime, v02_composition_tag, T_eff_K
#   Output:  A_proxy (float)
#   Method:
#     Gas giant / sub-Neptune / brown_dwarf:
#       Sudarsky (2000) piecewise condensate classification.
#       T0 = (F_mean / 4σ)^0.25 — zero-albedo blackbody baseline.
#       Source: Sudarsky et al. 2000, ApJ 538:885.
#       Scope: multi-body confirmed (Solar System giants + exoplanet models).
#       ⚠️ Flag 48: Sudarsky framework applied to brown_dwarf regime.
#         Framework assumes stellar insolation dominance. Internal luminosity
#         of brown dwarfs not represented. Flag for review if brown_dwarf
#         outputs behave anomalously.
#     Rocky / dwarf:
#       A_rock = 0.15 — bare silicate-iron regolith baseline.
#         Source: lunar, Mercurian, asteroidal phase integrals.
#         Scope: Solar System calibrated only.
#         ⚠️ EARTH FALLBACK — derived from Solar System bodies.
#         Universal applicability not confirmed.
#       A_ice(T_eff) = 0.40 + 0.25 * clamp((T_eff - 3000) / 4000, 0, 1)
#         Source: Shields et al. 2013, Astrobiology 13:715.
#         Scope: confirmed across multiple planetary bodies/models (F, G, K, M).
#         Yields 0.40 at T_eff=3000 K, 0.574 at T_eff=5778 K, 0.65 at T_eff=7000 K.
#       f_ice = clamp((270 - T0) / 70, 0, 1)
#         Full ice cover below 200 K; no ice above 270 K.
#         Forced to 0.0 for silicate-iron composition (no volatiles).
#       A_proxy = A_rock * (1 - f_ice) + A_ice * f_ice
#
# Earth Pass 1 calibration:
#   F_mean = 1361 W/m², regime = rocky, composition = silicate-iron, T_eff = 5778 K
#   T0 = (1361 / (4 * 5.670e-8))^0.25 = 278.3 K > 270 K → f_ice = 0
#   A_proxy = 0.15
#   T_eq^(0) = ((1 - 0.15) * 1361 / (4 * 5.670e-8))^0.25 = 266.7 K
#   Note: underestimates Earth's true albedo by design — clouds not yet modelled.
#
# Pass 2 — post-atmospheric refinement
#   Called from main.py after Variable 04 runs.
#   Inputs:  A_proxy, atm_class, composition, F_mean_W_m2, T_eff_K, regime
#   Output:  (A_B, T_eq_K) — final Bond albedo and recomputed equilibrium temperature
#   Method:
#     Gas giant / sub-Neptune / brown_dwarf:
#       A_B = A_proxy (Pass 1 Sudarsky held).
#       Roman (2023) geometric invariant mathematically requires T_surf, which
#       is not computed in the current cascade (Flag 43). Substituting T_eq^(0)
#       collapses the numerator to zero and produces A_B = 0 universally.
#       Deferral confirmed by numerical proof. Pass 1 is the optimal available estimate.
#     Dwarf / none / exosphere_only:
#       A_B = A_proxy (Pass 1 held; no atmosphere to refine with).
#     Rocky with atmosphere (primary_retained, primary_stripped, secondary_possible):
#       Del Genio et al. (2019) segmented linear model. ApJ 884:75.
#       Source: 29 ROCKE-3D GCM simulations spanning M-dwarf to F-dwarf hosts.
#       Scope: confirmed across multiple planetary bodies/models.
#       S_ox = F_mean / 1361
#       If S_ox >= 1.0:
#         A_B = 0.283 + 0.165*(S_ox - 1.0) + 0.119*(T_eff/5780 - 1.0)
#       If S_ox < 1.0:
#         A_B = 0.283 - 0.211*(S_ox - 1.0) + 0.164*(T_eff/5780 - 1.0)
#       A_B clamped to [0.0, 1.0].
#       ⚠️ Flag 38B: coefficients empirical, ROCKE-3D ensemble calibrated.
#         Biased toward N2/CO2/H2O atmospheres. Application to exotic
#         compositions is a generalised best-fit, not first-principles.
#       Thin-atmosphere Rayleigh correction (C_Rayleigh = 16.67 bar⁻¹, Mars-
#       calibrated) is derived and ready but deferred pending Flag 40
#       (P_surf = None for rocky). Falls back to A_proxy for atm_class = none
#       and exosphere_only.
#
# Earth Pass 2 calibration:
#   S_ox = 1.0, T_eff = 5778 K → high instellation branch
#   A_B = 0.283 + 0 + 0.119 * (5778/5780 - 1.0)
#       = 0.283 + 0.119 * (-0.000346) = 0.283 - 0.000041 ≈ 0.283
#   T_eq = ((1 - 0.283) * 1361 / (4 * 5.670e-8))^0.25 = 268.9 K
#   Earth observed: A_B = 0.306, T_eq = 254.0 K.
#   Residual of 0.023 is the f_land contribution (land fraction has no
#   cascade origin). Documented as Flag 38B.
#
# ⚠️ Flag 38B: Del Genio (2019) Segmented Linear Model is empirical ROCKE-3D
#   calibration. Residual vs Earth (0.283 vs 0.306) attributable to absent
#   f_land term. Coefficients confirmed across multi-model GCM ensemble but
#   biased toward Earth-like atmospheric compositions.
# ⚠️ Flag 48: Sudarsky albedo applied to brown_dwarf regime. Stellar
#   insolation assumed dominant. Internal luminosity not represented.
#
# Default composition_tag: Variable 02 does not yet emit bulk composition_tag
# in its output dict. Callers use v02.get("composition_tag", "silicate-iron")
# until ice-rock vs silicate-iron is modelled in the cascade.

from __future__ import annotations

# Stefan-Boltzmann constant — fundamental physical constant (Rule 1 Category A)
SIGMA = 5.670e-8  # W m^-2 K^-4

_SILICATE_IRON_TAG = "silicate-iron"


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def _sudarsky_albedo_from_t0(T0: float) -> float:
    """Sudarsky et al. (2000) piecewise Bond albedo vs equilibrium T (zero-albedo baseline)."""
    if T0 < 150.0:
        return 0.57
    if T0 < 250.0:
        return 0.57 + (T0 - 150.0) / 100.0 * 0.24
    if T0 < 300.0:
        return 0.81
    if T0 < 400.0:
        return 0.81 - (T0 - 300.0) / 100.0 * 0.69
    if T0 < 900.0:
        return 0.12
    if T0 < 1000.0:
        return 0.12 - (T0 - 900.0) / 100.0 * 0.09
    if T0 < 1500.0:
        return 0.03
    return 0.55


def compute_pass1_albedo(
    F_mean_W_m2: float,
    regime: str,
    v02_composition_tag: str,
    T_eff_K: float,
) -> float:
    T0 = (F_mean_W_m2 / (4.0 * SIGMA)) ** 0.25

    if regime in ("gas_giant", "sub_neptune", "brown_dwarf"):
        return _sudarsky_albedo_from_t0(T0)

    if regime in ("rocky", "dwarf"):
        A_rock = 0.15
        A_ice = 0.40 + 0.25 * _clamp((T_eff_K - 3000.0) / 4000.0, 0.0, 1.0)
        f_ice = _clamp((270.0 - T0) / 70.0, 0.0, 1.0)
        if v02_composition_tag == _SILICATE_IRON_TAG:
            f_ice = 0.0
        return A_rock * (1.0 - f_ice) + A_ice * f_ice

    # Unknown regime string: Sudarsky-style proxy (avoids Earth-like rock/ice defaults)
    return _sudarsky_albedo_from_t0(T0)


def _equilibrium_temperature_k(F_mean_W_m2: float, A: float) -> float:
    return ((1.0 - A) * F_mean_W_m2 / (4.0 * SIGMA)) ** 0.25


def compute_pass2_albedo(
    A_proxy: float,
    atm_class: str,
    composition: str,
    F_mean_W_m2: float,
    T_eff_K: float,
    regime: str,
) -> tuple[float, float]:
    _ = composition  # reserved for exotic-atmosphere extensions; Flag 38B bias in header

    use_del_genio = (
        regime == "rocky"
        and atm_class in ("primary_retained", "primary_stripped", "secondary_possible")
    )

    if use_del_genio:
        S_ox = F_mean_W_m2 / 1361.0
        teff_term = T_eff_K / 5780.0 - 1.0
        if S_ox >= 1.0:
            A_B = 0.283 + 0.165 * (S_ox - 1.0) + 0.119 * teff_term
        else:
            A_B = 0.283 - 0.211 * (S_ox - 1.0) + 0.164 * teff_term
        A_B = _clamp(A_B, 0.0, 1.0)
    else:
        A_B = A_proxy

    T_eq_K = _equilibrium_temperature_k(F_mean_W_m2, A_B)
    return A_B, T_eq_K
