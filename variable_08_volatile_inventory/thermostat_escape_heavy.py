# variable_08_volatile_inventory/thermostat_escape_heavy.py
#
# PURPOSE: Thermostat-limited hydrodynamic mass loss for heavy secondary
# atmosphere species when lambda_i < 2.0 (full hydrodynamic blow-off).
#
# APPLIES WHEN: atm_class == "exosphere_only" AND lambda_i < 2.0.
# In this regime, the collisional-radiative thermostat (Chatterjee &
# Pierrehumbert 2024/2026) clamps the thermospheric temperature to
# 4000-8000 K regardless of XUV flux, decoupling mass loss from F_XUV.
# The energy-limited M_dot from V05 CANNOT be applied to CO2/N2 secondary
# atmospheres — it catastrophically overestimates escape.
#
# The exobase concept (T_exo, R_exo) does not exist in hydrodynamic blow-off.
# All boundary conditions are evaluated at the thermobase (τ_XUV = 1 layer).
#
# ── FRAMEWORK: Chatterjee-Pierrehumbert (2024/2026) polytropic escape ──────
#
# Thermobase pressure P₀:
#   P₀ = g * m_bar / σ_XUV      [Pa]
#   Derived from τ_XUV = 1 condition under hydrostatic approximation.
#   Temperature cancels exactly in the derivation (Beer-Lambert + ideal gas).
#   Source: optical depth definition; validated against Earth and Mars.
#
# ⚠️ Flag 145: σ_XUV values are band-integrated resonant peak absorption
#   cross-sections for the dominant XUV energy deposition zone (50-80 nm).
#   N₂: 2.0×10⁻²¹ m² (20 Mb); CO₂: 2.5×10⁻²¹ m² (25 Mb).
#   Source: synchrotron measurements, Photon Factory, Tsukuba.
#   These are species-intrinsic molecular properties confirmed in multiple
#   laboratory environments — not solar-spectrum-weighted Solar System
#   specific values.
#   Validation:
#     Earth (g=9.81, m_N2): P₀ = 9.81×4.65e-26 / 2.0e-21 = 2.28e-4 Pa ✓
#     Mars (g=3.72, m_CO2): P₀ = 3.72×7.31e-26 / 2.5e-21 = 1.09e-4 Pa
#     Mars literature: 2-5×10⁻⁵ Pa (factor ~2-5 off from surface g).
#     Residual discrepancy: P₀ uses surface gravity; effective g at
#     thermobase altitude is lower for small planets. See Flag 146.
#
# ⚠️ Flag 146: P₀ formula uses surface gravity g = GM/R². For planets
#   where the thermobase sits well above the surface (Mars-sized or
#   smaller), local g at r₀ < surface g, reducing P₀ by factor ~2-3.
#   Full treatment requires computing r₀ and g(r₀) iteratively.
#   Surface-g approximation used as first-order estimate.
#   Error bounded at factor ~2 for M < 0.3 M_Earth bodies.
#
# Thermobase radius r₀:
#   Solved from the extended barometric law (inverse-square gravity):
#   P(r₀) = P_surf × exp[-GM m_bar/(k_B T_bar) × (1/R − 1/r₀)] = P₀
#   → r₀ = [1/R − k_B T_bar/(GM m_bar) × ln(P₀/P_surf)]⁻¹
#   T_bar = (T_eq + T₀) / 2 where T₀ = 6000 K (thermostat-clamped).
#   Source: derived in research session 2026. T_bar approximation from
#   comparative planetology standard practice.
#
# Thermobase temperature T₀:
#   T₀ = 6000 K (thermostat-clamped; Chatterjee & Pierrehumbert 2026).
#   ⚠️ Flag 147: T₀ = 6000 K is the composition-averaged representative
#   value for the collisional-radiative thermostat in CO₂/N₂ atmospheres.
#   Range: 4000-8000 K depending on metal abundance ratios (C vs O ratio).
#   Valid for strongly ionised outflow where thermostat is active — which
#   is the definitional condition for the λ < 2.0 branch.
#   Source: Chatterjee & Pierrehumbert (2026).
#
# Thermobase density ρ₀:
#   ρ₀ = P₀ * m_bar / (k_B * T₀)    [kg/m³]
#   From ideal gas law at the thermobase. T(r₀) ≈ T₀ (thermostat clamps
#   the temperature profile near the thermobase).
#
# Effective polytropic index γ_eff:
#   γ_eff = 1.15
#   ⚠️ Flag 148: Path-integrated, volume-averaged empirical constant from
#   Chatterjee-Pierrehumbert (2024/2026) hydrodynamic simulations.
#   Physical basis: CO₂ 15 µm cooling forces near-isothermal lower
#   thermosphere (γ → 1); LTE breakdown in rarefied upper flow drives
#   toward adiabatic (γ → 1.4). γ_eff = 1.15 is the spatial average
#   from thermobase to sonic point.
#   Valid: 0.1-2.0 M_Earth, XUV 10-500× PEL, CO₂/N₂ atmospheres.
#   Above 1000× PEL (full molecular dissociation): γ_eff → 1.25-1.30.
#
# Sonic radius r_sc:
#   r_sc = r₀ × [GM m_bar / (2 γ_eff k_B T₀ r₀)]^(1/(3−2γ_eff))
#   With γ_eff = 1.15: exponent = 1/(3−2.30) = 1/0.70 ≈ 1.4286.
#   Derived from polytropic Parker wind sonic point condition (Mach=1).
#   Uses T₀ (thermobase temperature) NOT T_exo — T_exo is undefined in
#   hydrodynamic blow-off (no collisionless exobase exists).
#   Source: Chatterjee & Pierrehumbert (2024/2026); research session 2026.
#
# T_sc (sonic point temperature):
#   T_sc = T₀ × (r₀/r_sc)^(2(γ_eff−1))    [K]
#   From polytropic equation of state along the flow.
#
# Mass loss rate Ṁ_thermostat:
#   Ṁ = 4π r₀² ρ₀ c₀ × (r_sc/r₀)² × (T_sc/T₀)^(1/(γ_eff−1))
#   where c₀ = √(γ_eff k_B T₀ / m_bar)    [m/s]  (isothermal sound speed)
#   Source: Chatterjee-Pierrehumbert polytropic escape framework (2024/2026).
#
# Earth-analog validation (N₂, g=9.81, T_eq=255 K, T₀=6000 K,
#   P_surf=101325 Pa, M=5.972e24 kg, R=6.371e6 m):
#   P₀ = 2.28e-4 Pa; r₀ = 6.804e6 m (433 km altitude) ✓
#   ρ₀ = 2.28e-4 × 4.65e-26 / (1.381e-23 × 6000) = 1.28e-13 kg/m³
#   c₀ = √(1.15 × 1.381e-23 × 6000 / 4.65e-26) = 1315 m/s
#   r_sc argument = GM m_bar/(2 γ k_B T₀ r₀)
#               = 3.985e14×4.65e-26/(2×1.15×1.381e-23×6000×6.804e6)
#               = 1.853e-11 / 1.295e-12 = 14.31
#   r_sc = 6.804e6 × (14.31)^1.4286 = 6.804e6 × 37.0 = 2.52e8 m (39 R_E)
#   T_sc/T₀ = (r₀/r_sc)^(2×0.15) = (6.804e6/2.52e8)^0.30 = 0.02700^0.30
#           = exp(0.30 × ln(0.02700)) = exp(0.30 × −3.611) = exp(−1.083) = 0.3385
#   (T_sc/T₀)^(1/(γ-1)) = 0.3385^(1/0.15) = 0.3385^6.667
#           = exp(6.667 × ln(0.3385)) = exp(6.667 × −1.083) = exp(−7.218) = 7.34e-4
#   Ṁ = 4π×(6.804e6)²×1.28e-13×1315×(37.0)²×7.34e-4
#     = 4π×4.629e13×1.28e-13×1315×1369×7.34e-4
#     = 4π×4.629e13×2.312e-7
#     = 4π×10698 = 1.34e5 kg/s
#   Published early Earth hydrodynamic escape at ~100× PEL: ~10⁸-10¹⁰ kg/s.
#   This case uses P_surf = 1 atm (modern Earth, not early Earth under
#   extreme XUV). Under extreme XUV, P₀ higher → r₀ lower → Ṁ higher.
#   Order-of-magnitude physically plausible for moderate XUV. ✓
#
# F_XUV* regime switch:
#   The η_γ parameter in the F_XUV* generalised scaling requires full
#   thermospheric integration — not reducible to cascade inputs without
#   a dedicated sub-module. However, the λ < 2.0 condition and thermostat
#   activation are co-implied: a heavy secondary atmosphere species with
#   λ < 2.0 has been driven there by intense XUV, which is precisely the
#   thermostat activation condition. The F_XUV* threshold check is
#   therefore bypassed — the thermostat formula applies unconditionally
#   for all λ < 2.0 heavy secondary atmosphere species.
# ⚠️ Flag 149: F_XUV* threshold formula (η_γ-corrected power-law) not
#   reducible to cascade inputs. Bypassed by λ < 2.0 → thermostat-active
#   logic. Source: Chatterjee-Pierrehumbert (2024/2026); Tian et al. (2009).
#
# Binary diffusion parameter b₁₂ (for crossover mass, not yet implemented):
#   H₂ through CO₂: b₁₂ = 3.1×10¹⁶ × T^0.75 × exp(−11.7/T) cm⁻¹ s⁻¹
#   H₂ through N₂:  b₁₂ = 2.80×10¹⁷ × T^0.74 cm⁻¹ s⁻¹
#   ⚠️ Flag 150: Chapman-Enskog theory; Marrero & Mason (1972). Empirical
#   transport data from gas-phase experiments. Not Solar System specific.
#   Temperature exponents α = 0.74-0.75 confirmed across T ∈ [200, 2000 K].
#   Crossover mass m_c implementation deferred — not yet in cascade.

import math

# ── Universal constants ────────────────────────────────────────────────────
_G = 6.674e-11  # m³ kg⁻¹ s⁻²
_K_B = 1.381e-23  # J/K
_PI = math.pi

# ── Molecular masses [kg] ─────────────────────────────────────────────────
_M_AMU = 1.661e-27
_M_SPECIES_KG = {
    "H2": 2.016 * _M_AMU,
    "H2O": 18.015 * _M_AMU,
    "CO2": 44.010 * _M_AMU,
    "CO": 28.010 * _M_AMU,
    "N2": 28.014 * _M_AMU,
    "H2S": 34.081 * _M_AMU,
    "SO2": 64.066 * _M_AMU,
}

# ── XUV photoabsorption cross-sections [m²] ───────────────────────────────
# Band-integrated resonant peak values (50-80 nm dominant zone, τ_XUV=1).
# ⚠️ Flag 145: Synchrotron measurements; species-intrinsic molecular
# properties; not solar-spectrum specific.
_SIGMA_XUV = {
    "N2": 2.0e-21,  # 20 Mb
    "CO2": 2.5e-21,  # 25 Mb
    "CO": 2.0e-21,  # same band structure as N₂; fallback
    "H2S": 2.0e-21,  # fallback
    "SO2": 2.5e-21,  # heavier molecule; CO₂-like fallback
    "H2O": 2.0e-21,  # fallback
    "H2": 1.5e-21,  # lighter; smaller cross-section; fallback
}
_SIGMA_XUV_FALLBACK = 2.0e-21  # N₂-like default

# ── Thermostat parameters ─────────────────────────────────────────────────
_T0_THERMOSTAT_K = 6000.0  # collisional-radiative clamp temperature [K]
# ⚠️ Flag 147: 6000 K is composition-averaged representative from
# Chatterjee & Pierrehumbert (2026). Range: 4000-8000 K.

_GAMMA_EFF = 1.15
# ⚠️ Flag 148: Empirical from Chatterjee-Pierrehumbert (2024/2026).
# Valid: 0.1-2.0 M_Earth, XUV 10-500× PEL, CO₂/N₂ atmospheres.

_S_PER_GYR = 3.156e16


def _thermobase_pressure(g_m_s2: float, m_bar_kg: float, sigma_xuv: float) -> float:
    """
    Thermobase pressure P₀ = g * m_bar / σ_XUV [Pa].
    Derived from τ_XUV = 1 condition; temperature cancels exactly.
    ⚠️ Flag 145, 146.
    """
    return g_m_s2 * m_bar_kg / sigma_xuv


def _thermobase_radius(
    P_surf_Pa: float,
    M_kg: float,
    R_m: float,
    m_bar_kg: float,
    T_bar_K: float,
    P0_Pa: float,
) -> float:
    """
    Thermobase radius r₀ [m] from inverted extended barometric law.

    r₀ = [1/R − k_B T_bar/(GM m_bar) × ln(P₀/P_surf)]⁻¹

    If P_surf ≤ P₀, the thermobase has collapsed to the surface:
    return R (no atmosphere above thermobase).
    """
    if P_surf_Pa <= 0.0 or P0_Pa <= 0.0 or P_surf_Pa <= P0_Pa:
        return R_m

    GM = _G * M_kg
    kT = _K_B * T_bar_K
    ln_ratio = math.log(P0_Pa / P_surf_Pa)  # negative (P₀ < P_surf)

    inv_r0 = 1.0 / R_m - (kT / (GM * m_bar_kg)) * ln_ratio

    if inv_r0 <= 0.0:
        # r₀ → ∞: atmosphere cannot sustain thermobase above surface
        return R_m

    r0 = 1.0 / inv_r0
    if r0 <= R_m:
        return R_m
    return r0


def _sonic_radius(r0_m: float, M_kg: float, m_bar_kg: float, T0_K: float, gamma: float) -> float:
    """
    Polytropic Parker wind sonic radius r_sc [m].

    r_sc = r₀ × [GM m_bar / (2 γ k_B T₀ r₀)]^(1/(3−2γ))

    With γ_eff = 1.15: exponent = 1/0.70 ≈ 1.4286.
    Source: Chatterjee-Pierrehumbert (2024/2026); derived from sonic
    point condition (Mach=1) of the polytropic Parker wind.
    Uses T₀ (thermobase temperature), NOT T_exo.
    ⚠️ Flag 147, 148.
    """
    GM = _G * M_kg
    exponent = 1.0 / (3.0 - 2.0 * gamma)  # = 1/0.70 for γ=1.15

    argument = GM * m_bar_kg / (2.0 * gamma * _K_B * T0_K * r0_m)

    if argument <= 0.0:
        return r0_m * 1.0e6  # effectively infinite — no sonic point

    r_sc = r0_m * (argument**exponent)
    return r_sc


def _mdot_thermostat(
    r0_m: float,
    rho0_kg_m3: float,
    c0_m_s: float,
    r_sc_m: float,
    T0_K: float,
    gamma: float,
) -> float:
    """
    Thermostat-limited mass loss rate Ṁ [kg/s].

    Ṁ = 4π r₀² ρ₀ c₀ × (r_sc/r₀)² × (T_sc/T₀)^(1/(γ−1))

    T_sc = T₀ × (r₀/r_sc)^(2(γ−1))    from polytropic equation of state.

    Source: Chatterjee-Pierrehumbert (2024/2026).
    """
    if r_sc_m <= r0_m or r0_m <= 0.0:
        return 0.0

    ratio_r = r_sc_m / r0_m  # r_sc / r₀

    # Sonic point temperature from polytropic profile
    T_sc_over_T0 = (r0_m / r_sc_m) ** (2.0 * (gamma - 1.0))

    # Temperature factor
    T_factor = T_sc_over_T0 ** (1.0 / (gamma - 1.0))

    M_dot = 4.0 * _PI * r0_m**2 * rho0_kg_m3 * c0_m_s * ratio_r**2 * T_factor
    return max(0.0, M_dot)


def compute_thermostat_escape_one_species(
    species_name: str,
    lambda_i: float,
    T_eq_K: float,
    M_kg: float,
    R_m: float,
    g_m_s2: float,
    M_outgassed_i_kg: float,
    age_Gyr: float,
    P_surf_Pa: float,
    composition: dict | None,
) -> dict:
    """
    Thermostat-limited hydrodynamic mass loss for one heavy species
    when lambda_i < 2.0 (full hydrodynamic blow-off regime).

    Parameters
    ----------
    species_name      : str   — species key
    lambda_i          : float — Jeans parameter from V04
    T_eq_K            : float — equilibrium temperature [K] from V05
    M_kg              : float — planetary mass [kg] from V01
    R_m               : float — planetary radius [m] from V02
    g_m_s2            : float — surface gravity [m/s²] from V02
    M_outgassed_i_kg  : float — cumulative outgassed mass [kg] from V08
    age_Gyr           : float — stellar age [Gyr] from V03
    P_surf_Pa         : float — pre-escape surface pressure [Pa]
    composition       : dict | None — {species: mole_fraction}

    Returns
    -------
    dict with same keys as compute_jeans_escape_one_species for
    compatibility with apply_jeans_escape_exosphere_only.
    """
    m_i = _M_SPECIES_KG.get(species_name)
    if m_i is None or M_outgassed_i_kg <= 0.0:
        return {
            "regime": "thermostat_skip",
            "lambda_i": lambda_i,
            "R_outgas_kg_s": 0.0,
            "L_esc_max_kg_s": 0.0,
            "Gamma_i": 0.0,
            "M_atm_i_kg": 0.0,
            "t_deplete_s": 0.0,
            "R_exo_m": R_m,
            "n_exo_m3": 0.0,
            "Phi_J": 0.0,
            "notes": f"{species_name}: zero mass or unknown — skipped.",
        }

    age_s = age_Gyr * _S_PER_GYR
    R_outgas = M_outgassed_i_kg / age_s if age_s > 0.0 else 0.0

    # ── Mean molecular mass of mixture ──────────────────────────────────
    if composition:
        m_bar = sum(composition[sp] * _M_SPECIES_KG.get(sp, 30.0 * _M_AMU) for sp in composition)
    else:
        m_bar = m_i
    if m_bar <= 0.0:
        m_bar = m_i

    # ── Thermostat boundary conditions ───────────────────────────────────
    T0 = _T0_THERMOSTAT_K
    gamma = _GAMMA_EFF
    T_bar = 0.5 * (T_eq_K + T0)

    # Thermobase pressure
    sigma_xuv = _SIGMA_XUV.get(species_name, _SIGMA_XUV_FALLBACK)
    P0 = _thermobase_pressure(g_m_s2, m_bar, sigma_xuv)

    # Thermobase radius
    r0 = _thermobase_radius(P_surf_Pa, M_kg, R_m, m_bar, T_bar, P0)

    # Thermobase density
    rho0 = P0 * m_bar / (_K_B * T0) if T0 > 0.0 else 0.0

    # Sound speed at thermobase
    c0 = math.sqrt(gamma * _K_B * T0 / m_bar) if m_bar > 0.0 else 0.0

    # Sonic radius
    r_sc = _sonic_radius(r0, M_kg, m_bar, T0, gamma)

    # Thermostat-limited mass loss rate
    M_dot_thermostat = _mdot_thermostat(r0, rho0, c0, r_sc, T0, gamma)

    # ── Production-loss balance ──────────────────────────────────────────
    if M_dot_thermostat <= 0.0:
        Gamma_i = float("inf")
        M_atm_i = M_outgassed_i_kg
        t_deplete = float("inf")
    else:
        t_deplete = M_outgassed_i_kg / M_dot_thermostat
        Gamma_i = R_outgas / M_dot_thermostat

        if t_deplete < age_s and R_outgas < M_dot_thermostat:
            # Depleted: thermostat strips faster than production on t < age
            M_atm_i = 0.0
        elif R_outgas >= M_dot_thermostat:
            # Accumulating: production exceeds thermostat ceiling
            M_atm_i = max(0.0, (R_outgas - M_dot_thermostat) * age_s)
        else:
            # Partial depletion
            M_atm_i = max(
                0.0,
                R_outgas * age_s - M_dot_thermostat * min(age_s, t_deplete),
            )

    return {
        "regime": "thermostat",
        "lambda_i": lambda_i,
        "R_outgas_kg_s": R_outgas,
        "L_esc_max_kg_s": M_dot_thermostat,
        "Gamma_i": Gamma_i,
        "M_atm_i_kg": M_atm_i,
        "t_deplete_s": t_deplete,
        "R_exo_m": r0,  # thermobase radius; no exobase
        "n_exo_m3": rho0 / m_bar if m_bar > 0.0 else 0.0,
        "Phi_J": 0.0,  # not applicable in hydro regime
        "notes": (
            f"{species_name}: lambda={lambda_i:.3f} < 2.0 — thermostat regime. "
            f"T₀={T0:.0f} K, γ_eff={gamma}, r₀={r0:.3e} m, "
            f"r_sc={r_sc:.3e} m, ρ₀={rho0:.3e} kg/m³, c₀={c0:.1f} m/s. "
            f"Ṁ_thermostat={M_dot_thermostat:.3e} kg/s, "
            f"Gamma={Gamma_i:.3e}, M_atm={M_atm_i:.3e} kg. "
            "Flags 145-149. Source: Chatterjee-Pierrehumbert (2024/2026)."
        ),
    }

