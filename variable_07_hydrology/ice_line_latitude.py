# variable_07_hydrology/ice_line_latitude.py
#
# PURPOSE: Compute the annual-mean ice-line latitude using a one-dimensional
# analytical Energy Balance Model with Legendre polynomial decomposition.
#
# FORMULA — Budyko-Sellers-North EBM, analytical P2 solution:
#
#   Q        = F_mean / 4                            [W/m²]
#   s2(β)    = -(5/8) * (3cos²β - 1) / 2            [dimensionless]
#   σ T_eq⁴  = A + B*T0  →  T0 = (σ T_eq⁴ - A) / B [°C]
#   T2       = Q(1-α) s2 / (B + 6D)                 [°C]
#   P2(x)    = (T_f - T0) / T2                       [dimensionless]
#   x_ice    = sqrt((2*P2 + 1) / 3)                  [sinφ]
#   φ_ice    = arcsin(x_ice)                          [degrees]
#
# SOURCES:
#   North, Cahalan & Coakley (1981) — analytical EBM P2 solution.
#   Sellers (1969) — meridional diffusion parameterisation.
#   Budyko (1969) — OLR linearisation.
#   Research session 2026-04-13 (MORTALIS Flag 92 research response).
#
# EARTH CALIBRATION (pre-implementation, verified by Claude):
#   F_mean=1361, β=23.44°, α=0.30, T_eq=255 K, T_f=273.15 K
#   → s2 = -0.477, T0 = 14.85°C, T2 = -20.28°C, φ_ice = 65.0°
#   Expected: ~70° N/S; 5° residual consistent with P2 truncation error.
#
# ⚠️ FLAG 94 — A = 210 W/m²: OLR linear intercept. Earth-calibrated empirical
#   coefficient, curve-fitted to Earth's top-of-atmosphere radiation budget.
#   Fails for dense CO2 atmospheres (Venus) or H2/He envelopes (giants).
#   Universal applicability not confirmed. Dynamic grey-gas scaling (via
#   T_eq, P_s, atm_class) required for non-Earth regimes; not yet derived.
#
# ⚠️ FLAG 95 — B = 2.0 W/m²/K: OLR temperature sensitivity. Earth-calibrated.
#   Encodes Earth's water-vapour feedback. Fails for non-H2O atmospheres.
#   Universal applicability not confirmed.
#
# ⚠️ FLAG 96 — D = 0.6 W/m²/K: meridional thermal diffusion coefficient.
#   Earth-calibrated only. Must scale with rotation rate (∝ Ω⁻²) and
#   atmospheric column mass. Rotation rate is absent from the cascade.
#   Two resolution gates: (1) rotation rate research + V05 implementation;
#   (2) D scaling law derivation and numerical validation. Both outstanding.
#
# ⚠️ FLAG 97 (model limitation) — P2 Legendre truncation. Ignoring P4 and
#   higher modes introduces 3–7% error on φ_ice as a function of obliquity.
#   Not patchable without a spatial grid.
#
# ⚠️ FLAG 98 (model limitation) — Ice-albedo feedback absent. Global mean
#   albedo used at the ice-edge. Local albedo step at the glaciation boundary
#   is not modelled. Underestimates ice extent near runaway glaciation states.
#
# ⚠️ FLAG 99 (model limitation) — EBM annual-mean assumption breaks down at
#   e > 0.3. At extreme eccentricity, apoastron winters may drive volatile
#   condensation or atmospheric collapse events that the annual-mean formula
#   cannot capture. Outputs on worlds with e > 0.3 should be treated as
#   lower-bound estimates of glaciation extent.

import math

# ── Universal physical constants (Rule 1, Category A) ─────────────────────
SIGMA = 5.670e-8          # Stefan-Boltzmann constant [W m⁻² K⁻⁴]

# ── Earth-empirical OLR coefficients (Budyko 1969) ────────────────────────
# ⚠️ FLAGS 94, 95 — Earth calibration only. See header.
# A and B are defined in the Celsius domain. T0 and T_f must be supplied
# to the solver in Celsius. T_eq from the cascade is in Kelvin; conversion
# is applied internally.
_A_WM2      = 210.0       # OLR intercept [W/m²] — Flag 94
_B_WM2K     = 2.0         # OLR temperature sensitivity [W/m²/K] — Flag 95

# ── Earth-empirical meridional diffusion coefficient ──────────────────────
# ⚠️ FLAG 96 — Earth calibration only; rotation rate dependency unresolved.
_D_WM2K     = 0.6         # meridional thermal diffusion [W/m²/K] — Flag 96

# ── Species triple-point temperatures (T_f fallback when P_s is None) ─────
# Intrinsic molecular constants from NIST thermochemical tables.
# Used when surface pressure is unavailable (Flag 40 deferred items).
# Inherit flag status from V07 Flags 71-77; no new flag required.
_T_TP_K = {
    "H2O": 273.16,
    "CO2": 216.58,
    "SO2": 197.69,
    "CH4":  90.67,
    "NH3": 195.40,
}

# ── Dominant condensable species by atmospheric class ─────────────────────
# Derived from V04 atm_class output. Used to select T_f species.
_ATM_CLASS_TO_SPECIES = {
    "secondary_possible": "H2O",
    "primary_stripped":   "H2O",
    "primary_retained":   None,   # H2/He giant — no condensable ice-line
    "none":               None,
    "exosphere_only":     None,
}


def _select_tf(atm_class: str, phase_states: dict | None) -> float | None:
    """
    Return the freezing temperature T_f [K] of the dominant condensable
    volatile, selected by atmospheric class.

    Returns None if no condensable ice-line is physically meaningful
    (e.g., H2/He giant, bare exosphere).
    """
    species = _ATM_CLASS_TO_SPECIES.get(atm_class, "H2O")
    if species is None:
        return None

    # If phase_states reports the species as present, use its triple point.
    # Phase_states confirms the species exists; T_f is the condensation gate.
    if phase_states and species in phase_states:
        return _T_TP_K[species]

    # Default to H2O triple point if phase_states absent or species missing.
    return _T_TP_K["H2O"]


def compute_ice_line_latitude(
    F_mean_W_m2: float,
    T_eq_K: float,
    obliquity_deg: float,
    albedo_final: float,
    atm_class: str,
    phase_states: dict | None = None,
) -> dict:
    """
    Compute the annual-mean ice-line latitude via the analytical P2 EBM.

    Parameters
    ----------
    F_mean_W_m2   : orbit-averaged bolometric stellar flux [W/m²]
    T_eq_K        : global mean equilibrium temperature [K]
    obliquity_deg : planetary obliquity [degrees, 0–180]
    albedo_final  : final Bond albedo (dimensionless, 0–1)
    atm_class     : V04 atmospheric classification string
    phase_states  : V07 per-species phase state dict (may be None)

    Returns
    -------
    dict with keys:
      ice_line_lat_deg  : float | None — ice-line latitude in degrees
                          None if ice-free or fully glaciated
      ice_line_state    : str — "polar_caps" | "tropical_belt" |
                          "ice_free" | "full_glaciation" | "no_condensable"
      T0_C              : float — global mean surface temperature [°C]
      T2_C              : float | None — equator-to-pole gradient amplitude [°C]
      T_f_K             : float | None — freezing temperature used [K]
      s2                : float | None — insolation gradient coefficient
      ice_line_notes    : str — physical interpretation
    """
    # ── 1. Select freezing temperature ────────────────────────────────────
    T_f_K = _select_tf(atm_class, phase_states)
    if T_f_K is None:
        return {
            "ice_line_lat_deg": None,
            "ice_line_state":   "no_condensable",
            "T0_C":             None,
            "T2_C":             None,
            "T_f_K":            None,
            "s2":               None,
            "ice_line_notes":   (
                f"atm_class={atm_class!r}: no condensable volatile with "
                "a meaningful surface ice-line for this regime."
            ),
        }

    T_f_C = T_f_K - 273.15

    # ── 2. Global mean insolation ──────────────────────────────────────────
    Q = F_mean_W_m2 / 4.0

    # ── 3. Insolation gradient coefficient s2 ─────────────────────────────
    beta_rad = math.radians(obliquity_deg)
    cos_beta = math.cos(beta_rad)
    s2 = -(5.0 / 8.0) * (3.0 * cos_beta ** 2 - 1.0) / 2.0

    # ── 4. Global mean surface temperature T0 (Celsius domain) ────────────
    olr_global = SIGMA * T_eq_K ** 4          # [W/m²]
    T0_C = (olr_global - _A_WM2) / _B_WM2K

    # ── 5. Temperature gradient amplitude T2 ──────────────────────────────
    # Guard: s2 = 0 at β = 54.74° → uniform insolation, T2 = 0.
    denom_diffusion = _B_WM2K + 6.0 * _D_WM2K    # = 5.6 at Earth defaults
    forcing = Q * (1.0 - albedo_final) * s2

    if abs(s2) < 1e-10:
        # Uniform insolation — whole planet at T0; no spatial gradient.
        if T0_C <= T_f_C:
            return _full_glaciation_result(T0_C, T_f_K, s2)
        else:
            return _ice_free_result(T0_C, T_f_K, s2)

    T2_C = forcing / denom_diffusion

    # ── 6. Legendre polynomial value at the ice boundary ──────────────────
    p2_ice = (T_f_C - T0_C) / T2_C

    # Physical domain of P2 is [-0.5, 1.0] for x in [-1, 1].
    if s2 < 0.0:
        # Normal regime (β < 54.74°): equator is warmest, poles coldest.
        # p2_ice < -0.5: even the warmest point (equator) is below T_f → full glaciation.
        # p2_ice > 1.0:  even the coldest point (pole) is above T_f → ice free.
        if p2_ice < -0.5:
            return _full_glaciation_result(T0_C, T_f_K, s2, T2_C)
        if p2_ice > 1.0:
            return _ice_free_result(T0_C, T_f_K, s2, T2_C)
    else:
        # Inverted regime (β > 54.74°): poles are warmest, equator coldest.
        # p2_ice < -0.5: even the coldest point (equator) is above T_f → ice free.
        # p2_ice > 1.0:  even the warmest point (pole) is below T_f → full glaciation.
        if p2_ice < -0.5:
            return _ice_free_result(T0_C, T_f_K, s2, T2_C)
        if p2_ice > 1.0:
            return _full_glaciation_result(T0_C, T_f_K, s2, T2_C)

    # ── 7. Solve for x_ice = sin(φ_ice) ───────────────────────────────────
    # From P2(x) = (3x² - 1)/2 = p2_ice → x² = (2*p2_ice + 1)/3
    x_ice_sq = (2.0 * p2_ice + 1.0) / 3.0

    if x_ice_sq < 0.0:
        # Numerically shouldn't occur given p2_ice > -0.5 check above,
        # but guard against floating-point edge cases.
        return _ice_free_result(T0_C, T_f_K, s2, T2_C)

    x_ice = math.sqrt(x_ice_sq)
    # Clamp to valid arcsin domain.
    x_ice = min(x_ice, 1.0)
    phi_ice_deg = math.degrees(math.asin(x_ice))

    # ── 8. Determine ice-line geometry from obliquity regime ───────────────
    if s2 < 0.0:
        # Normal regime (β < 54.74°): poles colder → polar ice caps.
        state = "polar_caps"
        notes = (
            f"Polar ice caps. Annual-mean ice boundary at ±{phi_ice_deg:.1f}°. "
            f"β={obliquity_deg:.1f}°, T0={T0_C:.1f}°C, T2={T2_C:.1f}°C, "
            f"T_f={T_f_K:.2f} K. "
            "Flags 94–99 active: A/B/D Earth-calibrated; rotation rate absent "
            "from cascade (D static); P2 truncation ±3–7%; ice-albedo feedback absent."
        )
    else:
        # Inverted regime (β > 54.74°): equator colder → tropical ice belt.
        state = "tropical_belt"
        notes = (
            f"Inverted insolation regime (β={obliquity_deg:.1f}° > 54.74°). "
            f"Equatorial ice belt poleward boundary at ±{phi_ice_deg:.1f}°. "
            f"Poles warmer than equator in annual mean. "
            f"T0={T0_C:.1f}°C, T2={T2_C:.1f}°C, T_f={T_f_K:.2f} K. "
            "Flags 94–99 active."
        )

    return {
        "ice_line_lat_deg": phi_ice_deg,
        "ice_line_state":   state,
        "T0_C":             T0_C,
        "T2_C":             T2_C,
        "T_f_K":            T_f_K,
        "s2":               s2,
        "ice_line_notes":   notes,
    }


def _ice_free_result(T0_C, T_f_K, s2, T2_C=None):
    return {
        "ice_line_lat_deg": None,
        "ice_line_state":   "ice_free",
        "T0_C":             T0_C,
        "T2_C":             T2_C,
        "T_f_K":            T_f_K,
        "s2":               s2,
        "ice_line_notes":   (
            f"Ice-free planet. Minimum annual-mean surface temperature "
            f"({T0_C - abs(T2_C or 0.0) * 0.5:.1f}°C) exceeds T_f "
            f"({T_f_K - 273.15:.2f}°C) everywhere. No surface ice."
        ),
    }


def _full_glaciation_result(T0_C, T_f_K, s2, T2_C=None):
    return {
        "ice_line_lat_deg": None,
        "ice_line_state":   "full_glaciation",
        "T0_C":             T0_C,
        "T2_C":             T2_C,
        "T_f_K":            T_f_K,
        "s2":               s2,
        "ice_line_notes":   (
            f"Fully glaciated planet. Global mean surface temperature "
            f"({T0_C:.1f}°C) at or below T_f ({T_f_K - 273.15:.2f}°C) "
            "everywhere. Complete surface ice coverage."
        ),
    }
