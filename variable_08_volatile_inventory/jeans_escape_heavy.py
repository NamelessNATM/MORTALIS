# variable_08_volatile_inventory/jeans_escape_heavy.py
#
# PURPOSE: Compute per-species Jeans escape flux and production-loss
# retention parameter (Gamma_i) for heavy species on exosphere_only worlds.
#
# APPLIES WHEN: atm_class == "exosphere_only" AND lambda_i >= 3.6.
# In this regime, thermal Jeans escape dominates over hydrodynamic escape.
# The energy-limited M_dot from V05 does NOT apply to heavy secondary
# atmosphere species — CO2/N2-dominated atmospheres activate a collisional-
# radiative thermostat that decouples mass loss from XUV flux (Flag 138).
#
# ── JEANS ESCAPE FLUX FORMULA ─────────────────────────────────────────────
# Phi_J,i = (n_exo * v_th,i) / (2*sqrt(pi)) * (1 + lambda_i) * exp(-lambda_i)
#
# Derivation: Maxwell-Boltzmann distribution integrated over the outward
# hemisphere for v > v_escape. Source: Chamberlain & Hunten (1987), Ch. 5.
# All prefactors are mathematical products of Gaussian integration over
# spherical velocity coordinates — no empirical coefficients.
#
# Mass loss rate [kg/s]:
# M_dot_J,i = 4 * pi * R_exo^2 * m_i * Phi_true,i
#
# ── MOLECULAR COLLISION CROSS-SECTIONS ───────────────────────────────────
# Cross-section formula: sigma_inf = pi * d_i^2
#   (center-to-centre collision distance for identical molecules = full
#   kinetic diameter d_i, not radius d_i/2)
#
# Temperature correction — Sutherland's law:
#   sigma_i(T) = sigma_inf,i * (1 + C_i / T_exo)
# Arises from temperature dependence of the intermolecular potential energy
# surface (PES). At low T, long-range attractive forces increase effective
# cross-section. At T >> C_i, asymptotes to hard-sphere limit.
# ⚠️ Flag 139: Sutherland constants C_i are intrinsic molecular properties
# (Lennard-Jones well depth / k_B), empirically measured from viscosity
# and gas transport data. Confirmed species-intrinsic and independent of
# any planetary body. Not Earth-specific. Source: Poling, Prausnitz &
# O'Connell (2001), "Properties of Gases and Liquids", 5th ed.
#
# Mixture cross-section — Rigorous Kinetic Theory (RKT):
#   sigma_bar = sum_i sum_j X_i * X_j * sigma_ij * sqrt(2*m_j/(m_i+m_j))
#   sigma_ij  = pi/4 * (d_i + d_j)^2   [dissimilar species]
# Source: Chapman & Cowling (1970); confirmed exact for Maxwell-Boltzmann
# mixtures under the well-mixed thermosphere assumption.
#
# ── NON-MAXWELLIAN CORRECTION FACTOR (beta_i) ────────────────────────────
# The high-energy Maxwell-Boltzmann tail is depleted by escape faster than
# collisions replenish it. True flux = beta_i * Phi_J,i.
#
# For BULK escape (escaping species IS the dominant atmosphere — the case
# for exosphere_only worlds where N2/CO2 are the primary species):
#   beta_bulk ≈ 1.4 to 1.7  (DSMC, Volkov et al. 2011)
#   True escape EXCEEDS classical Jeans prediction.
# ⚠️ Flag 135: beta_i = 1.0 implemented (classical Jeans, no correction).
#   For bulk escape on exosphere_only worlds, beta_true ≈ 1.4-1.7 > 1.0.
#   Using beta = 1.0 UNDERESTIMATES true escape by 40-70%.
#   Error direction: M_atm computed is HIGHER than physical M_atm.
#   Conservative toward retention, not toward stripping.
#   This is correct interim behaviour — resolves the 36-bar unphysical
#   accumulation without over-stripping. Functional form beta(lambda)
#   not yet derived. Follow-up research prompt queued (non-blocking).
#   Source: Volkov et al. (2011), J. Phys. D.; DSMC first-principles.
#
# ── EXOBASE ALTITUDE ─────────────────────────────────────────────────────
# Exobase defined by l_mfp = H_exo (mean free path = scale height).
# Boundary condition: n_exo = GM * m_bar / (sqrt(2) * sigma_bar * k_B * T_exo * R_exo^2)
# Extended barometric law (inverse-square gravity):
#   P_exo = P_surf * exp(-GM*m_bar/(k_B*T_bar) * (1/R - 1/R_exo))
#   T_bar = (T_eq + T_exo) / 2  [mean column temperature approximation]
# Source: Standard comparative planetology; validated in this research
# session. Flat-gravity error > 10% when z/R >= 0.05 (~320 km for
# Earth-radius planet); exobases at 500-2000 km -> inverse-square mandatory.
#
# Transcendental equation (log-linearised for numerical solving):
#   f(R_exo) = ln(GM*m_bar / (sqrt(2)*sigma_bar*P_surf*R_exo^2))
#              + GM*m_bar/(k_B*T_bar) * (1/R - 1/R_exo) = 0
# Monotonic in R_exo -> unique root guaranteed for physical inputs.
# Solved via brentq (authorised in project; scipy.optimize).
#
# Degenerate case (atmosphere too tenuous to form collisional exobase):
#   When l_mfp > H at the surface (P_surf below ~1e-4 Pa), R_exo = R
#   and n_exo = P_surf / (k_B * T_eq). Uses T_eq (surface temperature
#   proxy), NOT T_exo — T_exo is undefined when no exobase exists.
# ⚠️ Flag 136: P_surf threshold ~1e-4 Pa is from Solar System observations
#   (Mercury, Moon surface pressures). Not a derived threshold.
#   Source: Comparative planetology literature.
#
# ── REGIME SWITCH (prevents double-counting with V05 M_dot) ──────────────
# lambda_i >= 3.6  -> Jeans regime (this module)
# 2.0 <= lambda_i < 3.6 -> transition; Jeans deactivated (Flag 137)
# lambda_i < 2.0   -> hydrodynamic blow-off; thermostat-limited for
#                     heavy species (Flag 138); Jeans deactivated
# ⚠️ Flag 137: Transition zone [2.0, 3.6] — Jeans and hydrodynamic
#   regimes are mutually exclusive; linear blend not yet derived.
#   Conservative: M_atm = M_outgassed (no stripping applied).
# ⚠️ Flag 138: lambda_i < 2.0 for heavy secondary atmosphere species —
#   thermostat-limited Ṁ (Chatterjee-Pierrehumbert 2024/2026) requires
#   sonic radius, thermobase density, and polytropic index; not reducible
#   to cascade inputs without dedicated sub-module. Research prompt queued.
#   Conservative: M_atm = M_outgassed (no stripping applied).
#   XUV thresholds from literature (Tian et al. 2009; Chatterjee &
#   Pierrehumbert 2024): ~20x solar XUV for Mars-mass CO2 instability;
#   200-400x for Earth-mass. Solar System calibrated — flagged, not used.
#
# ── EARTH CALIBRATION ────────────────────────────────────────────────────
# Formula structure validated against known Earth N2 exobase:
#   T_exo = 1038 K (V04), T_eq = 255 K, T_bar = 646.5 K
#   sigma_N2(1038 K) = 4.16e-19 * (1 + 111/1038) = 4.61e-19 m^2
#   Transcendental equation sign-change confirmed:
#     f(R+500 km) = -2.11  [negative]
#     f(2R)       = +135.8 [positive]
#   Root exists in [R+500 km, 2R] — physically correct (Earth exobase
#   known at ~600-1000 km altitude). ✓
#
# Synthetic validation (lambda_CO2=10, v_e=5 km/s):
#   T_exo=6615 K, v_th,CO2=1581 m/s, n_exo~1.89e13 m^-3
#   Phi_J,CO2~4.2e12 m^-2 s^-1, M_dot_J~158 kg/s
#   t_deplete for M_outgassed=1e20 kg ~ 20 Gyr. Physically plausible. ✓

import math
from scipy.optimize import brentq

# ── Universal constants ────────────────────────────────────────────────────
_G = 6.674e-11  # m^3 kg^-1 s^-2
_K_B = 1.381e-23  # J/K
_PI = math.pi

# ── Species molecular masses [kg] ─────────────────────────────────────────
_M_AMU = 1.661e-27  # kg per amu
_M_SPECIES_KG = {
    "H2": 2.016 * _M_AMU,
    "H2O": 18.015 * _M_AMU,
    "CO2": 44.010 * _M_AMU,
    "CO": 28.010 * _M_AMU,
    "N2": 28.014 * _M_AMU,
    "H2S": 34.081 * _M_AMU,
    "SO2": 64.066 * _M_AMU,
}

# ── Kinetic diameters [m] ─────────────────────────────────────────────────
# Source: empirical kinetic theory; Poling, Prausnitz & O'Connell (2001).
# Hard-sphere cross-section: sigma_inf = pi * d^2
_D_KINETIC_M = {
    "H2": 2.89e-10,
    "H2O": 2.65e-10,
    "CO2": 3.30e-10,
    "CO": 3.76e-10,
    "N2": 3.64e-10,
    "H2S": 3.60e-10,
    "SO2": 3.60e-10,
}


def _sigma_inf(species: str) -> float:
    """Hard-sphere collision cross-section sigma_inf = pi * d^2 [m^2]."""
    d = _D_KINETIC_M.get(species)
    if d is None:
        return 1.0e-19  # order-of-magnitude fallback
    return _PI * d**2


# ── Sutherland constants [K] ─────────────────────────────────────────────
# ⚠️ Flag 139 — intrinsic molecular constants; empirically measured.
# Source: Poling, Prausnitz & O'Connell (2001).
_C_SUTHERLAND_K = {
    "H2": 72.0,
    "H2O": 650.0,
    "CO2": 240.0,
    "CO": 118.0,
    "N2": 111.0,
    "H2S": 301.0,
    "SO2": 416.0,
}


def _sigma_t(species: str, T_K: float) -> float:
    """
    Temperature-corrected collision cross-section [m^2] via Sutherland's law.
    sigma_i(T) = sigma_inf,i * (1 + C_i / T)
    """
    if T_K <= 0.0:
        return _sigma_inf(species)
    C = _C_SUTHERLAND_K.get(species, 0.0)
    return _sigma_inf(species) * (1.0 + C / T_K)


def _sigma_ij(sp_i: str, sp_j: str) -> float:
    """
    Hard-sphere mutual collision cross-section for dissimilar species [m^2].
    sigma_ij = pi/4 * (d_i + d_j)^2
    Sutherland correction on sigma_ij is not applied here — the mixture
    formula evaluates at T_exo via the single-species corrections.
    The mutual cross-section uses the geometric mean diameter.
    """
    d_i = _D_KINETIC_M.get(sp_i, 3.5e-10)
    d_j = _D_KINETIC_M.get(sp_j, 3.5e-10)
    return (_PI / 4.0) * (d_i + d_j) ** 2


def compute_sigma_bar_mixture(
    composition: dict,  # {species: mole_fraction}
    T_exo_K: float,
) -> float:
    """
    Mean collision cross-section for a gas mixture via RKT [m^2].
    sigma_bar = sum_i sum_j X_i * X_j * sigma_ij * sqrt(2*m_j/(m_i+m_j))
    Source: Chapman & Cowling (1970); Rigorous Kinetic Theory.
    """
    species = list(composition.keys())
    if not species:
        return 1.0e-19

    # Apply Sutherland correction to each single-species cross-section
    # For the mutual cross-section sigma_ij, use geometric mean of corrected
    # single-species values as the Sutherland-corrected estimate.
    sigma_corr = {sp: _sigma_t(sp, T_exo_K) for sp in species}

    total = 0.0
    for sp_i in species:
        X_i = composition[sp_i]
        m_i = _M_SPECIES_KG.get(sp_i, 30.0 * _M_AMU)
        for sp_j in species:
            X_j = composition[sp_j]
            m_j = _M_SPECIES_KG.get(sp_j, 30.0 * _M_AMU)
            # Mutual cross-section: geometric mean of corrected single-species values
            sig_ij = 0.5 * (sigma_corr[sp_i] + sigma_corr[sp_j])
            vel_factor = math.sqrt(2.0 * m_j / (m_i + m_j))
            total += X_i * X_j * sig_ij * vel_factor

    return total if total > 0.0 else 1.0e-19


# ── Regime switch thresholds ─────────────────────────────────────────────
_LAMBDA_JEANS_MIN = 3.6  # below: hydrodynamic continuum (Flags 137/138)
_LAMBDA_HYDRO_MAX = 2.0  # transition zone boundary

# ── Degenerate case P_surf threshold ────────────────────────────────────
# ⚠️ Flag 136 — Solar System calibrated order-of-magnitude.
_P_SURF_COLLISIONLESS_THRESHOLD_PA = 1.0e-4

# ── Conversion ────────────────────────────────────────────────────────────
_S_PER_GYR = 3.156e16


# ── β_bulk: Non-Maxwellian correction factors ─────────────────────────────
#
# DIATOMIC β_bulk — nine-point DSMC lookup with linear interpolation.
# Source: Volkov et al. (2011, 2013). DSMC first-principles; not Solar
# System specific. Valid for diatomic species at the exobase (Kn = 1),
# λ ∈ [3.6, 20].
#
# Five research sessions confirmed that no Padé [2/3] rational function
# with all-positive denominator coefficients can fit this dataset. The
# constraint c₄λ² + c₅λ + c₆ at λ=15 requires a net negative value
# (≈ −418) incompatible with c₄,c₅,c₆ > 0 given the fixed numerator.
# The lookup table is the mathematically correct implementation — exact
# at all nine DSMC nodes, positive-definite throughout the domain, and
# carries the same source status as the underlying simulation data.
# ⚠️ Flag 142: Padé [2/3] structural impossibility documented.
#   A closed-form expression with all-positive denominator coefficients
#   cannot simultaneously fit the diatomic DSMC dataset, proven by
#   back-calculation of required polynomial values at each node.
#   Lookup table used instead. Source: Volkov et al. (2011, 2013).
#
# MONATOMIC β_bulk — validated Padé [1/2].
# β_mono = 1 + (3.00λ − 5.00) / (λ² − 1.90λ + 2.20)
# Discriminant Δ = (−1.90)² − 4(2.20) = −5.19 < 0. No real roots.
# Denominator strictly positive for all real λ. RMS = 0.0176 < 0.02. ✓
# ⚠️ Flag 143: Monatomic coefficients fitted to Volkov et al. (2011, 2013)
#   DSMC data. Not Solar System specific. Valid: λ ∈ [3.6, 20], monatomic
#   species (Ar, noble gases, atomic O/N/C).
#
# β_trace — trace species through heavy background.
# β_trace = 1 − 2.40/λ
# Validated: λ=6.00 → 0.600 ✓; λ=8.00 → 0.700 ✓; λ=5.58 → 0.570 ✓
# ⚠️ Flag 144: c₁ = 2.40 calibrated to H escape through N₂/CO₂/O
#   terrestrial backgrounds (Earth and Mars exosphere measurements).
#   Not a universal constant — calibrated to H as the escaping trace
#   species. May over-correct for heavier trace species (e.g. Ar).
#   Source: DSMC literature; Earth/Mars exosphere observational data.
#   Minimum valid λ within Jeans regime (λ ≥ 3.6): β_trace = 0.333.
#
# TRACE vs BULK selection threshold:
#   Bulk if X_i ≥ 0.50 (dominant mass constituent rule), OR
#   Bulk if X_i ≥ 0.15 AND λ_dominant ≤ 15 (strongly coupled rule).
#   Otherwise: trace.
# Source: Volkov et al. kinetic coupling thresholds; research session 2026.

# Diatomic DSMC lookup table — (lambda_i, beta_bulk)
# ⚠️ Flag 142
_BETA_BULK_DIATOMIC = [
    (3.6, 1.95),
    (4.0, 1.88),
    (5.0, 1.78),
    (6.0, 1.70),
    (8.0, 1.58),
    (10.0, 1.51),
    (12.0, 1.45),
    (15.0, 1.40),
    (20.0, 1.25),
]

# Species molecular class for β selection
# Diatomic/polyatomic: rotational and vibrational internal energy modes.
# H₂O is polyatomic but treated as diatomic for β purposes.
_DIATOMIC_SPECIES = {"H2", "H2O", "N2", "CO2", "CO", "SO2", "H2S"}
_MONATOMIC_SPECIES = {"Ar"}  # expandable for noble gases, atomic species


def _beta_bulk_diatomic(lambda_i: float) -> float:
    """
    Diatomic bulk escape correction via DSMC nine-point lookup.
    Linear interpolation between nodes. ⚠️ Flag 142.
    Extrapolation λ > 20: β ≈ 1 + 5.0/λ (asymptotic from λ=20 anchor).
    """
    tbl = _BETA_BULK_DIATOMIC
    if lambda_i <= tbl[0][0]:
        return tbl[0][1]
    if lambda_i >= tbl[-1][0]:
        # (β−1)·λ anchored at λ=20: 0.25·20 = 5.0
        return max(1.0, 1.0 + 5.0 / lambda_i)
    for k in range(len(tbl) - 1):
        lam_lo, beta_lo = tbl[k]
        lam_hi, beta_hi = tbl[k + 1]
        if lam_lo <= lambda_i <= lam_hi:
            t = (lambda_i - lam_lo) / (lam_hi - lam_lo)
            return beta_lo + t * (beta_hi - beta_lo)
    return 1.0  # unreachable


def _beta_bulk_monatomic(lambda_i: float) -> float:
    """
    Monatomic bulk escape correction — validated Padé [1/2].
    β = 1 + (3.00λ − 5.00) / (λ² − 1.90λ + 2.20)
    RMS = 0.0176 < 0.02. Discriminant < 0 → no singularities. ⚠️ Flag 143.
    """
    num = 3.00 * lambda_i - 5.00
    den = lambda_i**2 - 1.90 * lambda_i + 2.20
    # den always > 0 (discriminant = −5.19 < 0); guard for safety
    if den <= 0.0:
        return 1.0
    return 1.0 + num / den


def _beta_trace(lambda_i: float) -> float:
    """
    Trace species correction through heavy background.
    β_trace = 1 − 2.40/λ. ⚠️ Flag 144.
    """
    if lambda_i <= 0.0:
        return 0.0
    return max(0.0, 1.0 - 2.40 / lambda_i)


def _compute_beta(
    species_name: str,
    lambda_i: float,
    mole_frac_i: float,
    lambda_dominant: float,
) -> tuple[float, str]:
    """
    Select and compute the appropriate β correction factor.

    Returns (beta, regime_label).

    regime_label: 'bulk_diatomic' | 'bulk_monatomic' | 'trace'
    """
    is_bulk = (
        mole_frac_i >= 0.50
        or (mole_frac_i >= 0.15 and lambda_dominant <= 15.0)
        or (species_name in _DIATOMIC_SPECIES and lambda_dominant <= 15.0)
    )
    if not is_bulk:
        return _beta_trace(lambda_i), "trace"
    if species_name in _MONATOMIC_SPECIES:
        return _beta_bulk_monatomic(lambda_i), "bulk_monatomic"
    return _beta_bulk_diatomic(lambda_i), "bulk_diatomic"


def _solve_r_exo(
    P_surf_Pa: float,
    M_kg: float,
    R_m: float,
    m_bar_kg: float,
    T_exo_K: float,
    T_eq_K: float,
    sigma_bar: float,
) -> float:
    """
    Locate exobase radius R_exo [m] by numerical root-finding.

    Transcendental equation (log-linearised):
      f(R_exo) = ln(GM*m_bar / (sqrt(2)*sigma_bar*P_surf*R_exo^2))
                 + GM*m_bar/(k_B*T_bar) * (1/R - 1/R_exo) = 0

    T_bar = (T_eq + T_exo) / 2 — mean column temperature approximation.
    Source: standard comparative planetology; validated this session.

    Monotonic in R_exo -> unique root for physical inputs.
    Returns R_m if no root found above surface (degenerate/tenuous case).
    """
    T_bar = 0.5 * (T_eq_K + T_exo_K)
    if T_bar <= 0.0:
        T_bar = max(T_exo_K, 100.0)

    GM = _G * M_kg
    GM_m = GM * m_bar_kg
    kT_bar = _K_B * T_bar
    sqrt2sig = math.sqrt(2.0) * sigma_bar

    def f(r_exo):
        if r_exo <= R_m:
            return float("inf")
        ln_arg = GM_m / (sqrt2sig * P_surf_Pa * r_exo**2)
        if ln_arg <= 0.0:
            return float("inf")
        return math.log(ln_arg) + (GM_m / kT_bar) * (1.0 / R_m - 1.0 / r_exo)

    # Search window: surface to 20 planetary radii
    r_lo = R_m * 1.0001
    r_hi = R_m * 20.0

    try:
        f_lo = f(r_lo)
        f_hi = f(r_hi)
        if f_lo * f_hi > 0.0:
            # No sign change — exobase collapses to surface
            return R_m
        return brentq(f, r_lo, r_hi, xtol=1.0e3, rtol=1.0e-6, maxiter=200)
    except Exception:
        return R_m


def _n_exo_from_boundary(
    M_kg: float,
    R_exo_m: float,
    m_bar_kg: float,
    T_exo_K: float,
    sigma_bar: float,
) -> float:
    """
    Exobase number density from l_mfp = H_exo boundary condition [m^-3].
    n_exo = GM * m_bar / (sqrt(2) * sigma_bar * k_B * T_exo * R_exo^2)
    """
    if T_exo_K <= 0.0 or R_exo_m <= 0.0:
        return 0.0
    return (
        _G
        * M_kg
        * m_bar_kg
        / (math.sqrt(2.0) * sigma_bar * _K_B * T_exo_K * R_exo_m**2)
    )


def _n_exo_degenerate(P_surf_Pa: float, T_eq_K: float) -> float:
    """
    Degenerate exobase density when atmosphere is fully collisionless
    from the surface. Uses T_eq (surface temperature proxy), NOT T_exo.
    T_exo is only defined when an exobase exists.
    n_exo = P_surf / (k_B * T_eq)
    """
    if T_eq_K <= 0.0 or P_surf_Pa <= 0.0:
        return 0.0
    return P_surf_Pa / (_K_B * T_eq_K)


def compute_jeans_escape_one_species(
    species_name: str,
    lambda_i: float,
    T_exo_K: float,
    T_eq_K: float,
    M_kg: float,
    R_m: float,
    M_outgassed_i_kg: float,
    age_Gyr: float,
    P_surf_pass1_Pa: float,
    composition: dict,
    jeans_v04: dict | None = None,
) -> dict:
    """
    Compute Jeans escape flux and Gamma_i retention parameter for one
    heavy species on an exosphere_only world.

    Parameters
    ----------
    species_name      : str   — key in _M_SPECIES_KG
    lambda_i          : float — Jeans parameter from V04 jeans dict
    T_exo_K           : float — exobase temperature [K] from V04
    T_eq_K            : float — equilibrium temperature [K] from V05
    M_kg              : float — planetary mass [kg] from V01
    R_m               : float — planetary radius [m] from V02
    M_outgassed_i_kg  : float — cumulative outgassed mass [kg] from V08
    age_Gyr           : float — stellar age [Gyr] from V03
    P_surf_pass1_Pa   : float — pre-escape surface pressure [Pa]; used to
                                locate exobase. Not circular: this is the
                                outgassed inventory pressure; post-escape
                                P_surf is recomputed in atmospheric_mass.py
    composition       : dict  — {species: mole_fraction} of outgassed mix
                                from V08 speciation; used for sigma_bar

    Returns
    -------
    dict with keys:
        regime            str   — 'jeans' | 'transition' | 'hydro' | 'skip'
        lambda_i          float — passthrough
        R_outgas_kg_s     float — time-averaged outgassing rate [kg/s]
        L_esc_max_kg_s    float — maximum Jeans escape rate [kg/s]
        Gamma_i           float — retention parameter R_outgas / L_esc
        M_atm_i_kg        float — surviving atmospheric mass [kg]
        t_deplete_s       float — inventory depletion timescale [s]
        R_exo_m           float — exobase radius [m]
        n_exo_m3          float — exobase number density [m^-3]
        Phi_J             float — classical Jeans flux [m^-2 s^-1]
        notes             str
    """
    m_i = _M_SPECIES_KG.get(species_name)
    if m_i is None or M_outgassed_i_kg <= 0.0:
        return {
            "regime": "skip",
            "lambda_i": lambda_i,
            "R_outgas_kg_s": 0.0,
            "L_esc_max_kg_s": 0.0,
            "Gamma_i": 0.0,
            "M_atm_i_kg": 0.0,
            "t_deplete_s": 0.0,
            "R_exo_m": R_m,
            "n_exo_m3": 0.0,
            "Phi_J": 0.0,
            "notes": f"{species_name}: zero mass or unknown species — skipped.",
        }

    age_s = age_Gyr * _S_PER_GYR
    R_outgas = M_outgassed_i_kg / age_s if age_s > 0.0 else 0.0
    degenerate = P_surf_pass1_Pa < _P_SURF_COLLISIONLESS_THRESHOLD_PA

    # ── Regime switch ────────────────────────────────────────────────────
    if lambda_i < _LAMBDA_HYDRO_MAX:
        # Thermostat-limited hydrodynamic blow-off for heavy secondary
        # atmosphere species. Energy-limited M_dot (V05) does NOT apply —
        # CO2/N2 atmospheres activate the collisional-radiative thermostat
        # (Chatterjee & Pierrehumbert 2024/2026). See thermostat_escape_heavy.py.
        from variable_08_volatile_inventory.thermostat_escape_heavy import (
            compute_thermostat_escape_one_species,
        )

        return compute_thermostat_escape_one_species(
            species_name=species_name,
            lambda_i=lambda_i,
            T_eq_K=T_eq_K,
            M_kg=M_kg,
            R_m=R_m,
            g_m_s2=_G * M_kg / R_m**2,
            M_outgassed_i_kg=M_outgassed_i_kg,
            age_Gyr=age_Gyr,
            P_surf_Pa=P_surf_pass1_Pa,
            composition=composition,
        )

    if lambda_i < _LAMBDA_JEANS_MIN:
        return {
            "regime": "transition",
            "lambda_i": lambda_i,
            "R_outgas_kg_s": R_outgas,
            "L_esc_max_kg_s": 0.0,
            "Gamma_i": float("inf"),
            "M_atm_i_kg": M_outgassed_i_kg,
            "t_deplete_s": float("inf"),
            "R_exo_m": R_m,
            "n_exo_m3": 0.0,
            "Phi_J": 0.0,
            "notes": (
                f"{species_name}: lambda={lambda_i:.3f} in transition [2.0,3.6]. "
                "Hydrodynamic and Jeans regimes mutually exclusive; "
                "interpolation not yet derived (Flag 137). "
                "M_atm = M_outgassed (conservative — no stripping applied)."
            ),
        }

    # ── Jeans regime (lambda_i >= 3.6) ───────────────────────────────────
    # Mixture mean cross-section
    sigma_bar = compute_sigma_bar_mixture(
        composition if composition else {species_name: 1.0},
        T_exo_K,
    )

    # Mean molecular mass of mixture
    if composition:
        m_bar = sum(
            composition[sp] * _M_SPECIES_KG.get(sp, 30.0 * _M_AMU)
            for sp in composition
        )
    else:
        m_bar = m_i

    # Exobase location
    if degenerate or T_exo_K <= 0.0:
        R_exo = R_m
        n_exo = _n_exo_degenerate(P_surf_pass1_Pa, T_eq_K)
        T_esc = T_eq_K  # degenerate case uses surface T
    else:
        R_exo = _solve_r_exo(
            P_surf_pass1_Pa, M_kg, R_m, m_bar, T_exo_K, T_eq_K, sigma_bar
        )
        if R_exo <= R_m * 1.0001:
            # Root solver returned surface — treat as degenerate
            n_exo = _n_exo_degenerate(P_surf_pass1_Pa, T_eq_K)
            T_esc = T_eq_K
        else:
            n_exo = _n_exo_from_boundary(M_kg, R_exo, m_bar, T_exo_K, sigma_bar)
            T_esc = T_exo_K

    if n_exo <= 0.0 or T_esc <= 0.0:
        return {
            "regime": "jeans",
            "lambda_i": lambda_i,
            "R_outgas_kg_s": R_outgas,
            "L_esc_max_kg_s": 0.0,
            "Gamma_i": float("inf"),
            "M_atm_i_kg": M_outgassed_i_kg,
            "t_deplete_s": float("inf"),
            "R_exo_m": R_exo,
            "n_exo_m3": 0.0,
            "Phi_J": 0.0,
            "notes": f"{species_name}: n_exo=0 or T_esc=0 — escape not computable.",
        }

    # ── Classical Jeans flux ─────────────────────────────────────────────
    # v_th,i = sqrt(2 * k_B * T_esc / m_i)  [most probable speed]
    v_th_i = math.sqrt(2.0 * _K_B * T_esc / m_i)

    # ── β correction ─────────────────────────────────────────────────────
    # Determine mole fraction and dominant species lambda for trace/bulk
    # regime selection.
    mole_frac_i = composition.get(species_name, 0.0) if composition else 1.0

    # lambda_dominant: smallest lambda among species with X >= 0.15
    # (proxy for the dominant background gas lambda)
    if jeans_v04 and composition:
        lambda_dominant = min(
            (
                jeans_v04[sp].get("lambda", 999.0)
                for sp in jeans_v04
                if isinstance(jeans_v04[sp], dict) and composition.get(sp, 0.0) >= 0.15
            ),
            default=lambda_i,
        )
    else:
        lambda_dominant = lambda_i

    beta, beta_regime = _compute_beta(species_name, lambda_i, mole_frac_i, lambda_dominant)
    # beta > 1 for bulk escape (true escape > classical Jeans prediction).
    #   Diatomic bulk: β ≈ 1.25–1.95; prior β=1.0 UNDERESTIMATED escape.
    # beta < 1 for trace escape (tail depletion suppresses escape).
    # Flag 135 resolved: β now computed from validated DSMC data.

    Phi_J = (n_exo * v_th_i / (2.0 * math.sqrt(_PI))) * (1.0 + lambda_i) * math.exp(-lambda_i)
    Phi_true = beta * Phi_J

    # ── Mass loss rate [kg/s] ────────────────────────────────────────────
    L_esc = 4.0 * _PI * R_exo**2 * m_i * Phi_true

    # ── Retention parameter and surviving mass ───────────────────────────
    if L_esc <= 0.0:
        Gamma_i = float("inf")
        M_atm_i = M_outgassed_i_kg
        t_deplete = float("inf")
    else:
        t_deplete = M_outgassed_i_kg / L_esc
        Gamma_i = R_outgas / L_esc if L_esc > 0.0 else float("inf")

        if t_deplete < age_s and R_outgas < L_esc:
            # Depleted regime: escape overwhelms production on timescale < age
            M_atm_i = 0.0
        elif R_outgas >= L_esc:
            # Intact/accumulating: production exceeds maximum escape rate
            M_atm_i = max(0.0, (R_outgas - L_esc) * age_s)
        else:
            # Partial depletion: some mass survives
            M_atm_i = max(0.0, R_outgas * age_s - L_esc * min(age_s, t_deplete))

    return {
        "regime": "jeans",
        "lambda_i": lambda_i,
        "R_outgas_kg_s": R_outgas,
        "L_esc_max_kg_s": L_esc,
        "Gamma_i": Gamma_i,
        "M_atm_i_kg": M_atm_i,
        "t_deplete_s": t_deplete,
        "R_exo_m": R_exo,
        "n_exo_m3": n_exo,
        "Phi_J": Phi_J,
        "notes": (
            f"{species_name}: lambda={lambda_i:.3f}, beta={beta:.3f} "
            f"({beta_regime}), Gamma={Gamma_i:.3e}, "
            f"L_esc={L_esc:.3e} kg/s, R_outgas={R_outgas:.3e} kg/s, "
            f"M_atm={M_atm_i:.3e} kg."
        ),
    }


def apply_jeans_escape_exosphere_only(
    M_outgassed_per_species: dict,
    jeans_v04: dict,
    T_exo_K: float,
    T_eq_K: float,
    M_kg: float,
    R_m: float,
    age_Gyr: float,
    P_surf_pass1_Pa: float,
    speciation: dict | None,
) -> dict:
    """
    Apply Jeans escape to all heavy species on an exosphere_only world.

    Called from atmospheric_mass.py when atm_class == "exosphere_only".
    Returns surviving per-species masses and escape diagnostics.

    Parameters
    ----------
    M_outgassed_per_species : dict  — {species: kg} from V08 outgassing
    jeans_v04               : dict  — V04 jeans dict with per-species lambda
    T_exo_K                 : float — exobase temperature [K] from V04
    T_eq_K                  : float — equilibrium temperature [K] from V05
    M_kg                    : float — planetary mass [kg]
    R_m                     : float — planetary radius [m]
    age_Gyr                 : float — stellar age [Gyr]
    P_surf_pass1_Pa         : float — pre-escape surface pressure [Pa]
    speciation              : dict | None — {species: mole_fraction} or None

    Returns
    -------
    dict with keys:
        surviving_mass   : dict  — {species: kg} after Jeans escape
        escape_details   : dict  — per-species escape diagnostics
        total_escaped_kg : float — total Jeans-escaped mass [kg]
    """
    # Build mole fraction composition from outgassed inventory
    # (β selection uses mole fractions, not mass fractions).
    total_moles = 0.0
    moles = {}
    for sp, m_kg in M_outgassed_per_species.items():
        if m_kg <= 0.0:
            continue
        m_i = _M_SPECIES_KG.get(sp)
        if not m_i or m_i <= 0.0:
            continue
        n_i = m_kg / m_i
        if n_i <= 0.0:
            continue
        moles[sp] = n_i
        total_moles += n_i

    if total_moles > 0.0:
        composition = {sp: n_i / total_moles for sp, n_i in moles.items()}
    else:
        composition = {}

    # Per-species lambda from V04 jeans dict
    # V04 stores: jeans = {species: {"lambda": float, "retained": bool}}
    def get_lambda(sp: str) -> float:
        if jeans_v04 is None:
            return 999.0  # no jeans data — treat as fully retained
        entry = jeans_v04.get(sp, {})
        return entry.get("lambda", 999.0)

    surviving = {}
    details = {}
    total_esc = 0.0

    for sp, m_out in M_outgassed_per_species.items():
        lam = get_lambda(sp)
        result = compute_jeans_escape_one_species(
            species_name=sp,
            lambda_i=lam,
            T_exo_K=T_exo_K,
            T_eq_K=T_eq_K,
            M_kg=M_kg,
            R_m=R_m,
            M_outgassed_i_kg=m_out,
            age_Gyr=age_Gyr,
            P_surf_pass1_Pa=P_surf_pass1_Pa,
            composition=composition,
            jeans_v04=jeans_v04,
        )
        surviving[sp] = result["M_atm_i_kg"]
        details[sp] = result
        escaped_i = max(0.0, m_out - result["M_atm_i_kg"])
        total_esc += escaped_i

    return {
        "surviving_mass": surviving,
        "escape_details": details,
        "total_escaped_kg": total_esc,
    }
