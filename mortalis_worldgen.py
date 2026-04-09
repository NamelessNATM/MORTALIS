"""
MORTALIS World Generation Engine
Variable One: Planetary Mass
Variable Two: Bulk Composition (Core Mass Fraction)
Variable Three: Stellar Insolation (Host Star + Orbital Distance)
Ontogenetic simulation — physical first principles
"""

import math
import random
import argparse


# ============================================================
# PHYSICAL CONSTANTS
# ============================================================

G             = 6.67430e-11       # Gravitational constant (m³ kg⁻¹ s⁻²)
EARTH_MASS    = 5.9722e24         # kg
EARTH_RADIUS  = 6.371e6           # m
SOLAR_MASS    = 1.989e30          # kg
SOLAR_LUM     = 3.828e26          # W
AU            = 1.496e11          # m
STEFAN_BOLTZ  = 5.67e-8           # W m⁻² K⁻⁴
BOLTZMANN     = 1.38e-23          # J/K

# Temporary baseline constants — active until Variable Two replaces them
RHO_BULK_BASELINE      = 4400.0   # kg/m³
CHONDRITIC_HEAT_BASELINE = 0.087  # W/m²

# Rock properties for topographic clamping
ROCK_YIELD_STRENGTH = 3.0e8       # Pa
RHO_ROCK = 2700.0                 # kg/m³

# Variable One bounds
MASS_MIN    = 0.250
MASS_MAX    = 2.000
MASS_CENTER = 1.000
MASS_SIGMA  = 0.35

# Variable Two constants
RHO_IRON     = 7050.0
RHO_SILICATE = 3980.0
CMF_EARTH    = 0.325
CMF_MIN      = 0.00
CMF_MAX      = 0.80
CMF_CENTER   = 0.32
CMF_SIGMA    = 0.12

# Variable Three constants
STAR_MASS_MIN    = 0.50   # Solar masses — early M lower bound
STAR_MASS_MAX    = 1.30   # Solar masses — mid-F upper bound
STAR_MASS_CENTER = 0.95   # Shifted toward G-class (was 0.85)
STAR_MASS_SIGMA  = 0.22   # Slightly wider — more F/G draws (was 0.20)
ALBEDO_TEMP      = 0.30   # Bond albedo placeholder [temporary constant]
GREENHOUSE_TEMP  = 33.0   # Kelvin offset placeholder [temporary constant]

# Simulation age
SIMULATION_AGE_GYR = 4.5

# Atmospheric gases: (name, molecular mass kg, symbol)
ATMO_GASES = [
    ("Hydrogen",       3.34e-27, "H₂"),
    ("Helium",         6.64e-27, "He"),
    ("Water Vapor",    2.99e-26, "H₂O"),
    ("Nitrogen",       4.65e-26, "N₂"),
    ("Oxygen",         5.31e-26, "O₂"),
    ("Argon",          6.63e-26, "Ar"),
    ("Carbon Dioxide", 7.31e-26, "CO₂"),
]


# ============================================================
# VARIABLE ONE: MASS & DERIVED PROPERTIES
# ============================================================

def generate_mass(rng):
    while True:
        m = rng.gauss(MASS_CENTER, MASS_SIGMA)
        if MASS_MIN <= m <= MASS_MAX:
            return m

def compute_radius_baseline(mass_kg):
    mass_earth = mass_kg / EARTH_MASS
    return (mass_earth ** 0.274) * EARTH_RADIUS

def compute_radius_composition(mass_kg, cmf):
    mass_earth = mass_kg / EARTH_MASS
    return (1.07 - 0.21 * cmf) * (mass_earth ** (1.0 / 3.7)) * EARTH_RADIUS

def compute_surface_area(r):
    return 4.0 * math.pi * r ** 2

def compute_gravity(mass_kg, r):
    return G * mass_kg / r ** 2

def compute_escape_velocity(mass_kg, r):
    return math.sqrt(2.0 * G * mass_kg / r)

def compute_heat_flux_baseline(mass_kg, sa):
    earth_sa = 4.0 * math.pi * EARTH_RADIUS ** 2
    return CHONDRITIC_HEAT_BASELINE * (mass_kg / EARTH_MASS) / (sa / earth_sa)

def compute_heat_flux_composition(mass_kg, sa, cmf):
    return compute_heat_flux_baseline(mass_kg, sa) * ((1.0 - cmf) / (1.0 - CMF_EARTH))

def compute_geologic_lifespan(mass_kg, sa):
    earth_sa  = 4.0 * math.pi * EARTH_RADIUS ** 2
    earth_vol = (4.0 / 3.0) * math.pi * EARTH_RADIUS ** 3
    r   = math.sqrt(sa / (4.0 * math.pi))
    vol = (4.0 / 3.0) * math.pi * r ** 3
    ratio = (sa / vol) / (earth_sa / earth_vol)
    return 9.0 / ratio

def compute_rayleigh_active(heat_flux, gravity):
    return (gravity / 9.81) * (heat_flux / CHONDRITIC_HEAT_BASELINE) > 0.1

def compute_max_mountain_km(gravity):
    return ROCK_YIELD_STRENGTH / (RHO_ROCK * gravity) / 1000.0

def compute_isostatic_basin(gravity):
    depth = 11.0 * (9.81 / gravity)
    if depth > 15.0:   cat = "Extreme — towering continental margins, abyssal trenches"
    elif depth > 8.0:  cat = "Deep — distinct continents, varied ocean floor"
    elif depth > 4.0:  cat = "Moderate — shallow seas likely, some continental flooding"
    else:              cat = "Shallow — high probability of global ocean flooding"
    return depth, cat

def compute_horizon_km(r, eye=1.7):
    return math.sqrt(2.0 * r * eye) / 1000.0

def geologic_status(lifespan, rayleigh):
    if SIMULATION_AGE_GYR >= lifespan:
        return "INACTIVE — core solidified, tectonics ceased, dynamo collapsed"
    elif not rayleigh:
        return "MARGINAL — heat budget insufficient for sustained convection"
    return "ACTIVE — mantle convection running, tectonic simulation authorized"

def gravity_label(g_g):
    if g_g < 0.6:    return "Low gravity — extreme vertical terrain, thin atmosphere"
    elif g_g < 0.9:  return "Below standard — lighter, taller geography"
    elif g_g < 1.1:  return "Near Earth-standard — familiar physics"
    elif g_g < 1.5:  return "Above standard — denser flora/fauna, compressed terrain"
    return "High gravity — stocky life, flattened landscape"


# ============================================================
# VARIABLE TWO: COMPOSITION & NEW PROPERTIES
# ============================================================

def generate_cmf(rng):
    while True:
        c = rng.gauss(CMF_CENTER, CMF_SIGMA)
        if CMF_MIN <= c < CMF_MAX:
            return c

def compute_true_bulk_density(cmf):
    return 1.0 / (cmf / RHO_IRON + (1.0 - cmf) / RHO_SILICATE)

def compute_core_geometry(r, cmf):
    crf      = math.sqrt(cmf) if cmf > 0 else 0.0
    core_km  = r * crf / 1000.0
    mantle_km = (r - r * crf) / 1000.0
    return core_km, crf, mantle_km

def compute_dynamo(cmf, lifespan):
    if cmf <= 0.0:                        return False, "No iron core — dynamo impossible"
    if SIMULATION_AGE_GYR >= lifespan:    return False, "Core solidified — dynamo collapsed"
    return True, "Liquid outer core confirmed — magnetosphere active"

def tectonic_regime(heat_flux, cmf):
    if heat_flux < 0.040:                              return "STAGNANT LID — single-plate world"
    elif heat_flux < 0.065 or (1.0-cmf) < 0.45:       return "SLUGGISH — reduced mobility, episodic resurfacing"
    elif heat_flux < 0.100:                            return "ACTIVE — standard plate tectonics authorized"
    return "VIGOROUS — rapid plate cycling, frequent volcanism"

def cmf_class(cmf):
    if cmf < 0.10:   return "Pure silicate — no dynamo, anomalously large radius"
    elif cmf < 0.25: return "Silicate-rich — large radius, long radiogenic lifespan"
    elif cmf < 0.40: return "Earth-analog composition"
    elif cmf < 0.60: return "Iron-enriched — denser, higher gravity, reduced tectonic fuel"
    return "Super-Mercury class — extreme density, stunted tectonic lifespan"


# ============================================================
# VARIABLE THREE: STELLAR INSOLATION
# ============================================================

def generate_star_mass(rng):
    """
    Host star mass via truncated Gaussian approximating IMF
    within viable habitability window: 0.50–1.30 M☉
    """
    while True:
        m = rng.gauss(STAR_MASS_CENTER, STAR_MASS_SIGMA)
        if STAR_MASS_MIN <= m <= STAR_MASS_MAX:
            return m

def compute_star_luminosity(star_mass_solar):
    """Mass-luminosity relation: L ≈ M^3.5  (in solar units)"""
    return star_mass_solar ** 3.5

def compute_star_lifespan(star_mass_solar):
    """Main sequence lifespan: t ≈ 10^10 * M^-2.5  (years)"""
    return 1.0e10 * (star_mass_solar ** -2.5)

def stellar_classification(star_mass_solar):
    """Approximate spectral type from mass."""
    if star_mass_solar >= 1.20:  return "F-class (Yellow-White)"
    elif star_mass_solar >= 1.00: return "G-class (Yellow Dwarf)"
    elif star_mass_solar >= 0.80: return "K-class (Orange Dwarf)"
    elif star_mass_solar >= 0.60: return "K/M-class (Orange-Red)"
    return "Early M-class (Red Dwarf)"

def stellar_sky_note(star_mass_solar):
    """Sky color note based on stellar spectrum — atmospheric composition deferred."""
    if star_mass_solar >= 1.15:  return "Blue-white sky (ample short-wavelength flux)"
    elif star_mass_solar >= 0.95: return "Blue sky — Earth-analog spectrum"
    elif star_mass_solar >= 0.75: return "Pale cyan to peach sky — reduced blue flux"
    return "Orange-tinted sky — infrared dominant, flora likely dark-pigmented"

def compute_habitable_zone(lum_solar):
    """
    Kopparapu et al. (2014) habitable zone boundaries.
    Simplified flux-based formulation scaled to luminosity.
    Inner edge (runaway greenhouse): S_inner ≈ 1.107 S☉
    Outer edge (maximum greenhouse): S_outer ≈ 0.356 S☉
    d = sqrt(L / S_eff) in AU
    """
    hz_inner_au = math.sqrt(lum_solar / 1.107)
    hz_outer_au = math.sqrt(lum_solar / 0.356)
    return hz_inner_au, hz_outer_au

def generate_orbital_distance(rng, hz_inner, hz_outer):
    """Uniform draw within habitable zone — guarantees liquid water potential."""
    return rng.uniform(hz_inner, hz_outer)

def hz_position_label(d_au, hz_inner, hz_outer):
    frac = (d_au - hz_inner) / (hz_outer - hz_inner)
    if frac < 0.25:   return "Inner HZ — warm, higher evaporation"
    elif frac < 0.50: return "Center-Inner HZ — stable liquid water zone"
    elif frac < 0.75: return "Center-Outer HZ — cooler, glaciation risk"
    return "Outer HZ — cold, CO₂ greenhouse critical for liquid water"

def compute_orbital_period_days(d_au, star_mass_solar):
    """Kepler's Third Law: P² = d³/M_star → P in Earth years, converted to days."""
    period_years = math.sqrt(d_au ** 3 / star_mass_solar)
    return period_years * 365.25

def compute_equilibrium_temp(lum_watts, d_m, albedo=ALBEDO_TEMP):
    """
    Stefan-Boltzmann blackbody equilibrium temperature.
    T_eq = [ L * (1 - α) / (16π σ d²) ]^(1/4)
    """
    flux = lum_watts * (1.0 - albedo) / (16.0 * math.pi * STEFAN_BOLTZ * d_m ** 2)
    return flux ** 0.25

def compute_insolation_flux(lum_watts, d_m):
    """Incident stellar flux at planet surface: S = L / (4π d²)"""
    return lum_watts / (4.0 * math.pi * d_m ** 2)

def jeans_retention(ve_ms, t_eq_k):
    """
    Evaluate Jeans escape for each atmospheric gas.
    v_th = sqrt(2kT/m)
    Retained:  v_e >= 6 * v_th
    Marginal:  3 * v_th < v_e < 6 * v_th
    Lost:      v_e <= 3 * v_th
    Returns list of (name, symbol, v_th km/s, ratio, status)
    """
    results = []
    for name, mol_mass, symbol in ATMO_GASES:
        v_th = math.sqrt(2.0 * BOLTZMANN * t_eq_k / mol_mass)
        ratio = ve_ms / v_th
        if ratio >= 6.0:     status = "RETAINED"
        elif ratio >= 3.0:   status = "MARGINAL"
        else:                status = "LOST"
        results.append((name, symbol, v_th / 1000.0, ratio, status))
    return results

def magnetosphere_sputtering_note(dynamo_active, star_mass_solar):
    """
    Interaction between dynamo state and stellar wind activity.
    K and M dwarfs are more active — greater sputtering risk without magnetosphere.
    """
    if dynamo_active:
        return "Magnetosphere active — atmosphere shielded from stellar wind sputtering"
    if star_mass_solar < 0.80:
        return "WARNING: No magnetosphere + active K/M star — severe atmospheric sputtering risk"
    return "No magnetosphere — moderate stellar wind sputtering over geological time"


# ============================================================
# VARIABLE FOUR: ATMOSPHERE AND HYDROLOGY
# ============================================================

EARTH_OCEAN_KM3 = 1.335e9    # km³ per Earth Ocean

# Atmospheric pressure bounds (atm)
PRESSURE_MIN    = 0.006
PRESSURE_MAX    = 10.0
PRESSURE_CENTER = 1.0
PRESSURE_SIGMA  = 0.5        # log-normal sigma

# Water inventory bounds (Earth Oceans)
WATER_MIN    = 0.05
WATER_MAX    = 20.0
WATER_MU     = 0.0           # log-normal: ln(1.0) = 0
WATER_SIGMA  = 0.8

# Albedo reference values
ALBEDO_OCEAN = 0.06
ALBEDO_LAND  = 0.20
ALBEDO_ICE   = 0.65
ALBEDO_CLOUD = 0.50
CLOUD_FRAC   = 0.50          # [temporary constant — replaced by Variable Five]

# CO2 forcing constants
CO2_FORCING_ALPHA = 5.35     # W/m²
CLIMATE_SENSITIVITY = 0.8   # K / (W/m²)

# Runaway thresholds
RUNAWAY_TEMP   = 340.0       # K — runaway greenhouse
SNOWBALL_ICE   = 0.90        # fraction — snowball state
WATERWORLD_OCN = 0.95        # fraction — global waterworld
DESERT_WATER   = 0.1         # EO — desert world

# Triple point of water
TRIPLE_POINT_T = 273.15      # K
TRIPLE_POINT_P = 0.006       # atm


def compute_pressure_physical(rng, mass_kg, radius_m, gravity_ms2,
                               heat_flux, tectonic_regime_str,
                               t_eq, lum_solar, d_au, dynamo_active):
    """
    Physically derived surface pressure from mass balance over 4.5 Gyr.
    Replaces the arbitrary log-normal centered on 1.0 atm.

    P = M_atm * g / (4 * pi * R^2)
    M_atm = M_outgas - M_jeans - M_sputter

    Components:
      M_outgas  — volcanic outgassing scaled to heat flux, mass, tectonic regime
      M_jeans   — thermal escape (Jeans) integrated over simulation age
      M_sputter — stellar wind sputtering modulated by dynamo state

    A small lognormal volatile delivery factor (sigma=0.25) captures the
    stochastic nature of cometary bombardment — the one genuinely random
    element in atmospheric accumulation not derivable from our current variables.
    """
    DELTA_T       = 1.42e17        # 4.5 Gyr in seconds
    M_ATM_EARTH   = 5.15e18       # kg — Earth's atmospheric mass
    M_N2          = 4.65e-26      # kg — molecular mass of N2 (dominant gas)
    N_C_EXOBASE   = 1.0e13        # m^-3 — exobase number density (Earth baseline)
    M_DOT_BASE    = 0.1           # kg/s — baseline sputtering rate (Mars-analog)

    # ── 1. OUTGASSING ────────────────────────────────────────
    mass_earth = mass_kg / EARTH_MASS
    # Cap mass scaling above 3 M_earth — mantle pressure suppresses outgassing
    mass_factor = min(mass_earth, 3.0) if mass_earth <= 3.0 else 3.0 / (mass_earth - 2.0)
    hf_factor   = heat_flux / CHONDRITIC_HEAT_BASELINE

    if "STAGNANT" in tectonic_regime_str:
        f_tectonic = 0.10
    elif "SLUGGISH" in tectonic_regime_str:
        f_tectonic = 0.50
    elif "VIGOROUS" in tectonic_regime_str:
        f_tectonic = 1.30
    else:  # ACTIVE
        f_tectonic = 1.00

    # Small stochastic volatile delivery factor — cometary bombardment is random
    volatile_factor = math.exp(rng.gauss(0.0, 0.25))
    M_outgas = M_ATM_EARTH * mass_factor * hf_factor * f_tectonic * volatile_factor

    # ── 2. JEANS ESCAPE ──────────────────────────────────────
    # Jeans parameter: ratio of gravitational to thermal energy at exobase
    # Use T_eq as exobase temperature approximation
    t_exo   = max(t_eq, 150.0)
    lam     = (G * mass_kg * M_N2) / (BOLTZMANN * t_exo * radius_m)
    v_th    = math.sqrt(2.0 * BOLTZMANN * t_exo / M_N2)
    # Upward escape flux (particles/m²/s) — Jeans formula
    # e^-lambda approaches zero for large lambda (heavy molecules, high gravity)
    exp_lam = math.exp(-min(lam, 700.0))   # clamp to avoid underflow
    phi     = (N_C_EXOBASE * v_th / (2.0 * math.sqrt(math.pi))) * (1.0 + lam) * exp_lam
    M_jeans = phi * (4.0 * math.pi * radius_m ** 2) * M_N2 * DELTA_T

    # ── 3. SPUTTERING ────────────────────────────────────────
    # Magnetised planets deflect stellar wind — shielding factor ~0.05
    S_dynamo     = 0.05 if dynamo_active else 1.0
    M_sputter    = (M_DOT_BASE * lum_solar * (1.0 / d_au) ** 2
                    * S_dynamo * DELTA_T)

    # ── 4. MASS BALANCE & PRESSURE ───────────────────────────
    M_atm    = max(0.0, M_outgas - M_jeans - M_sputter)
    P_pa     = M_atm * gravity_ms2 / (4.0 * math.pi * radius_m ** 2)
    P_atm    = P_pa / 101325.0

    # Hard floor: below triple point of water, liquid is impossible regardless
    P_atm    = max(TRIPLE_POINT_P, P_atm)

    return P_atm, M_outgas, M_jeans, M_sputter


def generate_co2_ppm(rng, tectonic_regime_str, heat_flux):
    """
    Phase 1 (Variable Four): Heat-flux-anchored volcanic baseline CO2.
    Earth at 0.087 W/m2 sustains ~280 ppm steady-state.
    Scales with heat flux before actual boundary geometry is known.
    Lognormal variation (sigma=0.5) gives ~1.6x spread at 1-sigma —
    physically realistic volcanic variability without the wide uniform ranges
    that caused tension to fire on almost every world.
    Phase 2 reconciliation occurs in Variable Six once boundary inventory exists.
    """
    baseline = 280.0 * (heat_flux / CHONDRITIC_HEAT_BASELINE) ** 0.7
    co2 = baseline * math.exp(rng.gauss(0.0, 0.5))
    # Regime caps — stagnant and sluggish worlds can't sustain high outgassing
    if "STAGNANT" in tectonic_regime_str:
        co2 = min(co2, 400.0)
    elif "SLUGGISH" in tectonic_regime_str:
        co2 = min(co2, 1200.0)
    return max(50.0, co2)


def generate_argon_fraction(heat_flux):
    """Argon fraction tied to radiogenic K-40 decay budget."""
    earth_ar = 0.0093
    ratio = heat_flux / CHONDRITIC_HEAT_BASELINE
    return min(earth_ar * ratio, 0.05)


def compute_greenhouse(co2_ppm, pressure_atm):
    """
    ΔF = 5.35 * ln(C/C0) W/m²    [logarithmic CO2 forcing]
    ΔT = λ * ΔF * (P/1atm)^0.5  [pressure broadening multiplier]
    C0 = 1 ppm reference baseline
    """
    if co2_ppm <= 0:
        return 0.0, 0.0
    delta_f = CO2_FORCING_ALPHA * math.log(co2_ppm / 1.0)
    delta_t = CLIMATE_SENSITIVITY * delta_f * (pressure_atm ** 0.5)
    return delta_f, delta_t


def generate_water_inventory(rng):
    """Log-normal water inventory in Earth Oceans."""
    while True:
        w = math.exp(rng.gauss(WATER_MU, WATER_SIGMA))
        if WATER_MIN <= w <= WATER_MAX:
            return w


def compute_phase_partition(t_surf, pressure_atm, water_eo, basin_depth_km, surface_area_km2):
    """
    Partition total water inventory into ice, liquid ocean, and vapor.
    Returns (f_ocean, f_ice, f_land, world_note)
    """
    frozen = t_surf < TRIPLE_POINT_T or pressure_atm < TRIPLE_POINT_P

    if frozen:
        f_ice   = min(0.95, water_eo / 2.0)
        f_ocean = 0.0
        f_land  = 1.0 - f_ice
        return f_ocean, f_ice, f_land, "ice"
    else:
        # Estimate max ocean volume from basin depth and surface area
        basin_volume_km3 = basin_depth_km * surface_area_km2 * 0.35  # ~35% ocean floor
        water_volume_km3 = water_eo * EARTH_OCEAN_KM3
        if water_volume_km3 >= basin_volume_km3:
            f_ocean = 1.0
            f_ice   = 0.0
            f_land  = 0.0
            return f_ocean, f_ice, f_land, "flooded"
        else:
            f_ocean = min(0.95, water_volume_km3 / (surface_area_km2 * basin_depth_km * 0.5))
            f_ocean = max(0.05, f_ocean)
            f_ice   = max(0.0, 0.10 - f_ocean * 0.05)
            f_land  = max(0.0, 1.0 - f_ocean - f_ice)
            return f_ocean, f_ice, f_land, "liquid"


def compute_true_albedo(f_ocean, f_ice, f_land):
    """
    Weighted surface albedo + cloud contribution.
    α = f_ocean*α_ocean + f_land*α_land + f_ice*α_ice + cloud_term
    Cloud term: CLOUD_FRAC * ALBEDO_CLOUD * (1 - f_ice)
    """
    surface_albedo = (f_ocean * ALBEDO_OCEAN +
                      f_land  * ALBEDO_LAND  +
                      f_ice   * ALBEDO_ICE)
    cloud_contribution = CLOUD_FRAC * ALBEDO_CLOUD * (1.0 - f_ice * 0.5)
    return min(0.95, surface_albedo + cloud_contribution * 0.5)


def compute_teq_with_albedo(lum_watts, d_m, albedo):
    """Recompute T_eq with updated albedo."""
    flux = lum_watts * (1.0 - albedo) / (16.0 * math.pi * STEFAN_BOLTZ * d_m ** 2)
    return flux ** 0.25


def classify_world(t_surf, f_ocean, f_ice, water_eo):
    if t_surf > RUNAWAY_TEMP:
        return "RUNAWAY GREENHOUSE — oceans boiled, Venus-like conditions"
    if f_ice > SNOWBALL_ICE:
        return "SNOWBALL STATE / ICE WORLD — permanent global glaciation"
    if water_eo < DESERT_WATER:
        return "DESERT WORLD — minimal surface water, vast arid expanses"
    if f_ocean > WATERWORLD_OCN:
        return "GLOBAL WATERWORLD — no permanent landmasses"
    if t_surf < 273.15:
        return "COLD WORLD — below freezing, marginal habitability"
    if t_surf < 290.0:
        return "TEMPERATE OCEAN WORLD — liquid water, habitable conditions"
    if t_surf < 320.0:
        return "WARM OCEAN WORLD — tropical-dominant, minimal ice"
    return "HOT WORLD — extreme heat, habitability stressed"


def compute_sky_color(star_mass_solar, pressure_atm, co2_ppm, f_ice):
    """
    Rayleigh scattering ∝ 1/λ⁴ — shorter wavelengths scatter most.
    Sky color depends on stellar spectrum and atmospheric density.
    """
    if pressure_atm < 0.1:
        base = "Near-black sky — thin atmosphere, stars visible by day"
    elif star_mass_solar >= 1.10:
        base = "Deep blue sky — strong short-wavelength stellar output"
    elif star_mass_solar >= 0.90:
        base = "Blue sky — Earth-analog spectrum"
    elif star_mass_solar >= 0.75:
        base = "Pale blue to cyan sky — reduced blue flux from orange dwarf"
    else:
        base = "Cyan to peach sky — infrared-dominant stellar spectrum"

    if co2_ppm > 10000:
        base += ", orange-red tint at horizon from CO₂ scattering"
    if f_ice > 0.5:
        base += ", white-dominated surface reflection"

    return base


# ============================================================
# VARIABLE FIVE: PLANETARY KINEMATICS
# ============================================================

# Rotation bounds (sidereal day, hours)
ROT_MIN    = 5.0
ROT_MAX    = 80.0
ROT_CENTER = 20.0
ROT_SIGMA  = 12.0

# Axial tilt bounds (degrees) — Rayleigh distribution
TILT_SCALE = 20.0   # Rayleigh scale parameter (mode near 20°)
TILT_MAX   = 90.0

# Diurnal variation coefficients
DIURNAL_BASE = 30.0   # K — reference swing for 24h day at 1 atm, land surface

# Cloud fraction update coefficients
CLOUD_OCEAN_BOOST  = 0.08
CLOUD_ROTATION_REF = 24.0   # hours — Earth reference


def check_tidal_locking(star_mass_solar, d_au, mass_kg, radius_m, age_gyr=4.5):
    """
    Tidal locking timescale approximation.
    t_lock ∝ d^6 * M_planet * R^-3 / (M_star^2)
    Normalised to Earth-Moon system; returns (is_locked, t_lock_gyr).
    """
    # Simplified scaling from Kasting et al.
    # t_lock ~ 1.7e10 * (d_au^6 * mass_kg) / (star_mass_solar^2 * radius_m^3)  [years]
    t_lock_yr = (1.7e10 * (d_au ** 6) * (mass_kg / EARTH_MASS)) / \
                (star_mass_solar ** 2 * (radius_m / EARTH_RADIUS) ** 3)
    t_lock_gyr = t_lock_yr / 1e9
    return t_lock_gyr < age_gyr, t_lock_gyr


def generate_rotation(rng, tidally_locked, period_days):
    """
    Generate sidereal day length in hours.
    If tidally locked, sidereal day = orbital period.
    Otherwise Gaussian centred on 20 h, clamped 5–80 h.
    """
    if tidally_locked:
        return period_days * 24.0
    while True:
        r = rng.gauss(ROT_CENTER, ROT_SIGMA)
        if ROT_MIN <= r <= ROT_MAX:
            return r


def compute_solar_day(sidereal_h, period_days):
    """
    T_solar = T_sidereal * T_orbital / (T_orbital - T_sidereal)
    Both in same units (hours here).
    """
    period_h = period_days * 24.0
    if period_h <= sidereal_h:
        return sidereal_h  # tidally locked or near-locked
    return sidereal_h * period_h / (period_h - sidereal_h)


def compute_angular_velocity(sidereal_h):
    """Ω = 2π / T_sidereal   (rad/s)"""
    return 2.0 * math.pi / (sidereal_h * 3600.0)


def compute_coriolis(omega, lat_deg=45.0):
    """f = 2Ω sin(φ)  at given latitude."""
    return 2.0 * omega * math.sin(math.radians(lat_deg))


def generate_axial_tilt(rng):
    """
    Rayleigh distribution favouring 10–30°, tail to 90°.
    """
    while True:
        t = rng.weibullvariate(TILT_SCALE, 2.0)  # approx Rayleigh
        if 0.0 <= t <= TILT_MAX:
            return t


def generate_moon_flag(rng, tilt_deg):
    """
    Large stabilising moon more likely at moderate tilts.
    High tilts suggest chaotic history — moon less likely to have survived.
    """
    p_moon = max(0.1, 0.65 - tilt_deg / 200.0)
    return rng.random() < p_moon


def compute_hadley_boundary(omega, t_surf, radius_m):
    """
    Hadley cell boundary latitude scales roughly as Ω^-1.
    Earth: Ω_earth = 7.27e-5 rad/s, boundary ~30°.
    φ_H ≈ 30° * (Ω_earth / Ω)^0.5  — clamped 10°–70°.
    """
    omega_earth = 7.27e-5
    phi_h = 30.0 * ((omega_earth / omega) ** 0.5)
    return max(10.0, min(70.0, phi_h))


def compute_diurnal_range(solar_day_h, pressure_atm, f_ocean):
    """
    Diurnal range scales with day length and inversely with pressure.
    Oceans buffer — land amplifies.
    ΔT ≈ DIURNAL_BASE * (solar_day / 24) * (1 / pressure)^0.4 * (1 - f_ocean * 0.6)
    """
    day_factor  = solar_day_h / 24.0
    press_factor = (1.0 / max(0.01, pressure_atm)) ** 0.4
    ocean_buffer = 1.0 - f_ocean * 0.6
    return DIURNAL_BASE * day_factor * press_factor * ocean_buffer


def compute_seasonal_ice_status(tilt_deg, t_surf):
    """
    Threshold: tilt > 45° or T_surf near freezing → seasonal ice possible.
    Returns descriptive status string.
    """
    if t_surf > 280.0:
        return "None — too warm for persistent ice"
    elif tilt_deg > 55.0:
        return "Seasonal at poles — extreme tilt drives summer melt"
    elif tilt_deg > 30.0 and t_surf > 250.0:
        return "Seasonal at mid-latitudes, permanent at poles"
    elif t_surf < 240.0:
        return "Permanent across high latitudes — deep glaciation"
    else:
        return "Permanent at poles, seasonal at mid-latitudes"


def compute_updated_cloud_fraction(omega, t_surf, f_ocean):
    """
    Cloud fraction update replacing 0.50 placeholder.
    More ocean → more evaporation → more cloud.
    Faster rotation → more storm tracks → more cloud.
    Warmer → more cloud (up to a point).
    f_cloud = 0.35 + ocean_boost + rotation_boost + temp_boost
    """
    ocean_boost   = f_ocean * CLOUD_OCEAN_BOOST
    omega_earth   = 7.27e-5
    rot_boost     = 0.05 * min(1.5, omega / omega_earth)
    temp_boost    = max(0.0, min(0.05, (t_surf - 250.0) / 200.0))
    return min(0.75, max(0.15, 0.35 + ocean_boost + rot_boost + temp_boost))


def precipitation_profile(phi_h, tilt_deg):
    """Return qualitative precipitation band description."""
    itcz_edge   = phi_h / 2.0
    desert_edge = phi_h
    mid_lat     = (phi_h + 70.0) / 2.0
    monsoon     = " (monsoon migration likely)" if tilt_deg > 20.0 else ""

    return [
        f"Equatorial  (0°–{itcz_edge:.0f}°): Heavy precipitation — ITCZ{monsoon}",
        f"Subtropical ({itcz_edge:.0f}°–{desert_edge:.0f}°): Arid — descending dry air",
        f"Mid-Latitude ({desert_edge:.0f}°–65°): Moderate — frontal storm tracks",
        f"Polar        (65°–90°): Dry and cold — polar cell",
    ]


# ============================================================
# VARIABLE SIX: TECTONIC GEOMETRY
# ============================================================

# Tectonic regime plate count constants
REGIME_PLATE_CONSTANT = {
    "VIGOROUS": 18.0,
    "ACTIVE":   12.0,
    "SLUGGISH":  7.0,
    "STAGNANT":  1.0,
}

# Crustal density constants for isostasy
RHO_CONTINENTAL = 2750.0   # kg/m³ — felsic continental crust
RHO_MANTLE_ISOSTASY = 3300.0  # kg/m³ — upper mantle
CONTINENTAL_THICKNESS_KM = 35.0  # km — typical continental crust thickness

# Boundary type probability weights [convergent, divergent, transform]
BOUNDARY_WEIGHTS = [0.40, 0.35, 0.25]

EARTH_SURFACE_AREA_KM2 = 5.1e8   # km²
EARTH_QHF = 0.087                 # W/m²


def compute_plate_count(sa_km2, heat_flux, tectonic_str):
    """
    N_plates = floor(C_regime * (A/A_earth) * (Q_hf/Q_earth))
    Returns (total_plates, major_plates, minor_plates)
    """
    if "STAGNANT" in tectonic_str:
        return 1, 1, 0
    c = REGIME_PLATE_CONSTANT.get("ACTIVE", 12.0)
    for key in REGIME_PLATE_CONSTANT:
        if key in tectonic_str.upper():
            c = REGIME_PLATE_CONSTANT[key]
            break
    n = max(3, int(c * (sa_km2 / EARTH_SURFACE_AREA_KM2) *
                   (heat_flux / EARTH_QHF)))
    major = max(2, n // 3)
    minor = n - major
    return n, major, minor


def generate_clustering(rng):
    """
    Clustering parameter 0.0–1.0.
    0 = fully dispersed, 1 = supercontinent.
    Uniform — any configuration equally likely.
    """
    return rng.random()


def clustering_label(c):
    if c > 0.75:   return "Supercontinent", "single vast landmass, extreme interior aridity"
    elif c > 0.50: return "Semi-clustered", "2–3 large continents, moderate ocean barriers"
    elif c > 0.25: return "Dispersed",      "4–6 continents, significant oceanic separation"
    else:          return "Archipelagic",   "fragmented landmass, island-dominant, maritime world"


def compute_isostatic_freeboard(f_land, water_eo, basin_depth_km):
    """
    Freeboard = h_c * (rho_mantle - rho_crust) / rho_mantle
    Adjusted for ocean water column weight if liquid oceans present.
    Returns mean continental elevation above ocean floor (km).
    """
    base_freeboard = CONTINENTAL_THICKNESS_KM * \
        (RHO_MANTLE_ISOSTASY - RHO_CONTINENTAL) / RHO_MANTLE_ISOSTASY
    # If ocean exists, water weight depresses basin slightly
    ocean_depression = min(water_eo * 0.3, basin_depth_km * 0.15)
    return base_freeboard - ocean_depression


def assign_boundaries(rng, n_plates, tectonic_str):
    """
    Generate boundary inventory.
    Returns dict with counts of convergent, divergent, transform boundaries
    and derived topographic features.
    """
    if "STAGNANT" in tectonic_str:
        return {"convergent": 0, "divergent": 0, "transform": 0,
                "fold_mountains": 0, "subduction_trenches": 0,
                "rift_valleys": 0, "mid_ocean_ridges": 0}

    # Each plate has ~2 boundaries on average
    total_boundaries = max(4, int(n_plates * 2.2))
    convergent = int(total_boundaries * BOUNDARY_WEIGHTS[0])
    divergent  = int(total_boundaries * BOUNDARY_WEIGHTS[1])
    transform  = total_boundaries - convergent - divergent

    # Split convergent into collision vs subduction (~60/40)
    fold_mountains      = max(1, int(convergent * 0.60))
    subduction_trenches = convergent - fold_mountains

    # Split divergent into rift valleys vs mid-ocean ridges
    # Scale with land fraction — more land = more rift valleys
    rift_frac    = min(0.85, 0.4 + rng.random() * 0.4)
    rift_valleys = max(1, int(divergent * rift_frac))
    mid_ridges   = max(1, divergent - rift_valleys)

    return {
        "convergent":         convergent,
        "divergent":          divergent,
        "transform":          transform,
        "fold_mountains":     fold_mountains,
        "subduction_trenches": subduction_trenches,
        "rift_valleys":       rift_valleys,
        "mid_ocean_ridges":   mid_ridges,
    }


def compute_mountain_heights(rng, fold_count, h_max_km, gravity_g):
    """
    Mountain heights drawn from uniform distribution capped at h_max.
    Higher gravity compresses mountains — mean scales with 1/g.
    """
    if fold_count == 0:
        return 0.0, 0.0
    earth_mean = 4.5   # km — Earth mean orogen height
    scaled_mean = earth_mean / gravity_g
    heights = [rng.uniform(scaled_mean * 0.5, min(h_max_km, scaled_mean * 1.8))
               for _ in range(fold_count)]
    return sum(heights) / len(heights), max(heights)


def compute_trench_depth(gravity_g, basin_depth_km):
    """
    Trench depth inversely proportional to gravity.
    Earth: ~11 km at 1g. Clamped by isostatic basin depth.
    """
    return min(basin_depth_km, 11.0 / gravity_g)


def compute_hotspot_count(heat_flux):
    """Hotspot count scales with internal heat flux."""
    earth_hotspots = 45
    return max(2, int(earth_hotspots * (heat_flux / EARTH_QHF)))


def compute_rain_shadow_count(fold_count, phi_h, clustering):
    """
    Mountain ranges that intersect storm tracks.
    More mountains + more dispersed land = more intersections.
    """
    storm_exposure = 1.0 - clustering * 0.5
    return max(0, int(fold_count * storm_exposure * 0.6))


def compute_coastline_complexity(clustering, n_plates, f_land):
    """
    Fractal dimension D: 1.0 (smooth) to 1.3 (highly fragmented).
    Supercontinent → smooth (D near 1.0).
    Archipelagic → complex (D near 1.3).
    """
    base = 1.05 + (1.0 - clustering) * 0.20
    plate_factor = min(0.05, (n_plates - 6) * 0.005)
    return min(1.35, base + plate_factor)


def compute_aridity_index(clustering, phi_h, f_land):
    """
    Fraction of land > moisture transport limit from ocean.
    Transport limit ≈ Hadley cell width in km.
    Supercontinents have massive arid interiors.
    """
    # Moisture transport limit scales with Hadley width
    transport_limit_frac = phi_h / 90.0   # fraction of hemisphere
    interior_frac = clustering * f_land * (1.0 - transport_limit_frac)
    return min(0.95, max(0.0, interior_frac))


def compute_mean_continental_elevation(freeboard_km, fold_mean_km, f_land):
    """
    Weighted mean elevation: freeboard base + orogenic contribution
    scaled by fraction of land that is mountainous (~15%).
    """
    mountain_frac = 0.15
    return freeboard_km * (1.0 - mountain_frac) + fold_mean_km * mountain_frac


def reconcile_co2_with_tectonics(co2_v4, fold_count, divergent, heat_flux):
    """
    Phase 2 (Variable Six): Reconcile V4 CO2 against actual boundary inventory.
    V4 generated a heat-flux baseline before boundary geometry existed.
    Now that boundary count is known, compute what the tectonic budget truly supports
    and either confirm, flag, or adjust CO2 accordingly.

    Returns (final_co2_ppm, status_string, is_genuine_tension)

    Ratio thresholds:
      > 8x  — genuine geological anomaly. V4 CO2 is too high to be explained by
              steady-state tectonics. A flood basalt, major impact, or other
              extraordinary event is implied in the world's history. Keep V4 CO2.
      2.5–8x — elevated but within range of vigorous outgassing phases. Keep V4 CO2,
               note elevated status.
      < 2.5x — steady state. Reconcile CO2 downward to volcanic budget. This is
               the normal case and should no longer trigger on every world.
    """
    boundary_activity = (fold_count + divergent) * heat_flux / EARTH_QHF
    # Earth: ~30 active boundary segments at Earth heat flux → ~280 ppm
    volcanic_co2 = max(50.0, 280.0 * (boundary_activity / 30.0) ** 0.7)
    ratio = co2_v4 / max(1.0, volcanic_co2)

    if ratio > 8.0:
        msg = (f"TENSION — CO₂ {co2_v4:.0f} ppm >> volcanic budget "
               f"({volcanic_co2:.0f} ppm): flood basalt or major impact implied")
        return co2_v4, msg, True
    elif ratio > 2.5:
        msg = (f"ELEVATED — CO₂ {co2_v4:.0f} ppm > volcanic budget "
               f"({volcanic_co2:.0f} ppm): vigorous outgassing phase")
        return co2_v4, msg, False
    else:
        msg = (f"RECONCILED — CO₂ {co2_v4:.0f}→{volcanic_co2:.0f} ppm "
               f"(volcanic budget {volcanic_co2:.0f} ppm, ratio {ratio:.1f}x)")
        return volcanic_co2, msg, False


def compute_habitability_zones(t_surf, f_land, f_ice, aridity_index, phi_h):
    """
    First spatial habitability estimate.
    Zones must be: above freezing AND receiving precipitation.
    Returns fraction of land surface that qualifies.
    """
    if t_surf < 273.15:
        return 0.0, "None — surface below freezing globally"
    # Precipitation zones: ITCZ + mid-latitude storm tracks
    precip_land_frac = max(0.0, 1.0 - aridity_index)
    # Temperature: assume equatorial band (within ±30° of equator) is warmest
    temp_ok_frac = min(1.0, phi_h / 45.0)
    habitable = f_land * precip_land_frac * temp_ok_frac * (1.0 - f_ice)
    if habitable < 0.01:
        label = "Negligible — extreme cold and aridity"
    elif habitable < 0.10:
        label = "Marginal — narrow equatorial refugia only"
    elif habitable < 0.30:
        label = "Limited — scattered temperate zones"
    else:
        label = "Moderate — significant habitable land area"
    return habitable, label


# ============================================================
# VARIABLE SEVEN: HYDROLOGY
# ============================================================

ICE_DENSITY        = 917.0    # kg/m³
ICE_YIELD_STRESS   = 100000.0 # Pa — yield stress of ice
LAMBDA_ICE         = 2.1      # W/(m·K) — thermal conductivity of ice
LAMBDA_ROCK        = 3.0      # W/(m·K) — thermal conductivity of crustal rock
EARTH_OCEAN_VOL_KM3 = 1.335e9 # km³ per Earth Ocean

HACKS_LAW_C = 1.4
HACKS_LAW_H = 0.6
NAVIGABILITY_GRADIENT = 0.001  # m/m — 0.1% slope threshold


def compute_permafrost_depth(t_surf, heat_flux):
    """
    1D steady-state heat conduction: Z = lambda_rock * (273.15 - T_surf) / Q_hf
    Returns depth in metres. Zero if T_surf >= 273.15 K.
    """
    if t_surf >= 273.15:
        return 0.0
    return LAMBDA_ROCK * (273.15 - t_surf) / heat_flux


def compute_active_layer(t_surf, tilt_deg, diurnal_range):
    """
    Active layer: seasonal thaw zone above permafrost.
    Scales with temperature distance from melting point and seasonal range.
    """
    if t_surf >= 273.15:
        return 0.0
    # Seasonal peak warming contribution
    seasonal_boost = tilt_deg / 90.0 * 15.0  # up to 15 K seasonal swing
    peak_t = t_surf + diurnal_range * 0.5 + seasonal_boost
    if peak_t < 273.15:
        return 0.05   # minimal sublimation layer only
    warmth = peak_t - 273.15
    return min(5.0, 0.3 * warmth)   # metres


def compute_subglacial_melt_thickness(t_surf, heat_flux):
    """
    Minimum ice thickness for basal melting:
    H_min = lambda_ice * (273.15 - T_surf) / Q_hf
    """
    if t_surf >= 273.15:
        return 0.0
    return LAMBDA_ICE * (273.15 - t_surf) / heat_flux


def estimate_subglacial_lakes(water_eo, permafrost_depth_m, melt_threshold_m,
                               fold_mountains, rift_valleys):
    """
    Subglacial lakes form in topographic lows beneath ice thick enough to melt.
    More rift valleys and basins → more potential sites.
    """
    if melt_threshold_m <= 0 or water_eo <= 0:
        return 0
    basin_sites = rift_valleys + fold_mountains // 2
    # Scale with how much ice we have (more ice → more sites above threshold)
    ice_factor = min(1.0, water_eo / 0.5)
    return max(0, int(basin_sites * ice_factor * 2.5))


def compute_ice_distribution(water_eo, f_ice, clustering, fold_mountains):
    """
    Partition ice across polar caps, continental sheets, mountain glaciers.
    Supercontinents push ice toward continental sheets.
    """
    mountain_frac    = min(0.20, fold_mountains * 0.02)
    continental_frac = min(0.40, clustering * 0.35)
    polar_frac       = max(0.40, 1.0 - mountain_frac - continental_frac)
    total = polar_frac + continental_frac + mountain_frac
    return (polar_frac/total, continental_frac/total, mountain_frac/total)


def compute_drainage_basins(sa_km2, f_land, aridity_index, fold_mountains,
                             rift_valleys, clustering):
    """
    Total basin count scales with land area and tectonic complexity.
    Endorheic fraction scales with aridity and supercontinent configuration.
    """
    land_area_km2   = sa_km2 * f_land
    # Earth has ~200 major basins over 1.49e8 km² land
    total_basins    = max(10, int(200 * (land_area_km2 / 1.49e8) *
                                  (0.7 + fold_mountains * 0.05)))
    endorheic_frac  = min(0.70, aridity_index * 0.8 + clustering * 0.15)
    major_exorheic  = max(2, int(total_basins * (1 - endorheic_frac) * 0.065))
    major_endorheic = max(1, int(total_basins * endorheic_frac * 0.20))
    divides         = max(2, fold_mountains - 1)
    return total_basins, major_exorheic, major_endorheic, divides


def compute_river_networks(major_exorheic, major_endorheic, sa_km2, f_land,
                           aridity_index, t_surf):
    """
    Generate river count and navigable length via Hack's Law.
    L = C * A^h where C=1.4, h=0.6
    """
    land_area_km2 = sa_km2 * f_land
    total_major   = major_exorheic + major_endorheic
    avg_basin_km2 = land_area_km2 / max(1, total_major)
    avg_length_km = HACKS_LAW_C * (avg_basin_km2 ** HACKS_LAW_H)
    total_rivers  = max(5, total_major * 3)

    # Navigable length: low-gradient rivers in exorheic basins
    nav_fraction  = max(0.0, (1.0 - aridity_index) * 0.6)
    navigable_km  = int(major_exorheic * avg_length_km * nav_fraction)

    # Connectivity: fraction of land within 50 km of navigable water
    nav_reach_km2 = navigable_km * 100  # 50 km each side
    connectivity  = min(0.95, nav_reach_km2 / max(1, land_area_km2))

    valley_type = "U-shaped glacial valleys (ice-carved)" if t_surf < 273.15 \
                  else "V-shaped water-carved valleys"

    return total_rivers, int(avg_length_km), navigable_km, connectivity, valley_type


def compute_sea_level_rise(water_eo, sa_km2, f_land):
    """
    SLR if all ice melts: V_ice / A_ocean_basin
    Returns km.
    """
    ocean_frac  = 1.0 - f_land
    if ocean_frac <= 0:
        return 0.0
    ocean_area_km2 = sa_km2 * ocean_frac / 1e6   # already in km²... wait
    # sa_km2 is already in km² (we divided by 1e6 earlier in run())
    ocean_area     = sa_km2 * ocean_frac          # km²
    water_vol_km3  = water_eo * EARTH_OCEAN_VOL_KM3
    return water_vol_km3 / ocean_area             # km


def compute_activation_thresholds(t_surf, water_eo, aridity_index):
    """
    Temperatures needed to activate equatorial and full liquid hydrology.
    Equatorial rivers activate before global melt.
    """
    # Equatorial band is warmer than global mean by ~15-20 K typically
    equatorial_offset = 15.0
    equatorial_thresh = 273.15 - equatorial_offset
    global_thresh     = 273.15 + 2.0   # slight buffer above freezing
    return equatorial_thresh, global_thresh


# ============================================================
# VARIABLE EIGHT: SOIL AND REGOLITH
# ============================================================

# Weathering constants
GLACIAL_K       = 1.5e-4   # Glacial erosion constant (mm/yr at unit velocity)
ARRHENIUS_EA    = 60000.0  # J/mol — activation energy for silicate weathering
GAS_CONSTANT    = 8.314    # J/(mol·K)
EARTH_CHEM_RATE = 0.05     # mm/yr reference chemical weathering rate at 288 K

# Regolith depth references (km of weathering per Gyr at Earth conditions)
CRATON_DEPTH_RATE    = 3.0   # m per Gyr — stable continental interior
MOUNTAIN_DEPTH_RATE  = 0.05  # m per Gyr — rapid uplift strips material
BASIN_DEPTH_RATE     = 8.0   # m per Gyr — sediment trap
OASIS_DEPTH_RATE     = 0.5   # m per Gyr — fresh volcanic material

# Nutrient relative availability (0=none, 1=abundant)
NUTRIENT_BASELINES = {
    "Phosphorus": 0.40,
    "Potassium":  0.75,
    "Iron":       0.90,
    "Nitrogen":   0.02,   # abiotic — critically low
    "Calcium":    0.65,
    "Magnesium":  0.60,
}

SIMULATION_AGE_GYR_V8 = 4.5


def compute_glacial_erosion_rate(gravity_g, ice_thickness_m, slope=0.02):
    """
    E_g = K_g * U^2
    U (basal sliding velocity) scales with ice thickness, gravity, slope.
    Returns erosion rate in mm/yr.
    """
    g_norm = gravity_g / 1.0  # normalized to 1g
    U = (ice_thickness_m * g_norm * slope) ** 0.5 * 0.1  # m/yr approximate
    return GLACIAL_K * (U ** 2) * 1000.0  # mm/yr


def compute_chemical_weathering_rate(t_surf, co2_ppm, frozen=True):
    """
    Arrhenius temperature dependence for silicate weathering.
    r_T = r_0 * exp(-Ea/R * (1/T - 1/T_ref))
    At freezing temperatures, rate is severely suppressed.
    Subglacial and oasis zones get a warmer T applied separately.
    """
    t_ref = 288.0  # K — reference temperature (Earth surface)
    rate = EARTH_CHEM_RATE * math.exp(
        -ARRHENIUS_EA / GAS_CONSTANT * (1.0/t_surf - 1.0/t_ref))
    co2_factor = math.log(co2_ppm / 280.0 + 1.0) * 0.5 + 1.0
    return rate * co2_factor  # mm/yr


def compute_aeolian_rate(pressure_atm, gravity_g, particle_size_mm=0.05):
    """
    Bagnold's formula simplified: q ∝ (rho_air/g) * u*^3
    On a cold, high-gravity, thin-atmosphere world, aeolian transport is moderate.
    Returns relative transport index (0–1).
    """
    rho_air_norm = pressure_atm / 1.0
    g_factor = 1.0 / gravity_g
    d_factor = (0.05 / particle_size_mm) ** 0.5
    return min(1.0, rho_air_norm * g_factor * d_factor * 0.6)


def compute_regolith_depths(gravity_g, heat_flux, sa_km2, f_land, t_surf,
                             pressure_atm, water_eo, f_ice, tectonic_str,
                             fold_mountains, subduction_trenches, aridity_index,
                             active_layer_m, phi_h=29.0, clustering=0.5, basin_depth_m=8650.0):
    """
    Physically derived Source-to-Sink sediment budget model.
    Replaces hardcoded caps with mass balance equations.
    Returns dict of terrain class → equilibrium regolith depth in metres.
    """
    age_yr = SIMULATION_AGE_GYR_V8 * 1e9

    # ── Area estimation (km²) ──────────────────────────────────
    A_land   = sa_km2 * f_land
    A_mtn    = min(A_land * 0.20 * (fold_mountains / 6.0), A_land * 0.40)
    A_basin  = A_land * aridity_index * 0.60
    A_craton = max(A_land - A_mtn - A_basin, A_land * 0.10)

    # ── Weathering / production rates (m/yr) ──────────────────
    # Chemical weathering (Arrhenius)
    E_a_R  = 4000.0  # K — activation energy / gas constant
    W_chem = 2e-5 * math.exp(E_a_R * (1.0/288.15 - 1.0/max(t_surf, 200.0)))

    # Glacial grinding
    U_ice  = 15.0 * gravity_g * f_ice
    W_glac = 1e-4 * U_ice if f_ice > 0 else 0.0

    # Freeze-thaw cycling
    cycles = 15 if 260 < t_surf < 290 else (2 if active_layer_m > 0 else 0)
    W_ft   = 1e-5 * cycles * active_layer_m

    W_craton = W_chem + (W_glac if f_ice > 0.5 else 0.0) + W_ft
    W_mtn    = W_chem * 1.5 + W_glac + W_ft * 2.0

    # ── Transport capacities ───────────────────────────────────
    # Fluvial (zero below freezing)
    T_fluv = 0.0 if t_surf < 273.15 else 1e7 * water_eo * gravity_g

    # Aeolian — corrected Bagnold derivation with transport length
    R_planet_m  = math.sqrt(A_land * 1e6 / (4.0 * math.pi * f_land)) if f_land > 0 else 1e7
    L_path_m    = phi_h * (math.pi / 180.0) * R_planet_m * (1.0 + clustering)
    A_arid_m2   = A_land * aridity_index * 1e6
    W_path_m    = A_arid_m2 / L_path_m if L_path_m > 0 else 0.0
    rho_air     = 1.2 * pressure_atm   # kg/m³
    u_star      = 0.5                  # m/s
    C_bagnold   = 1.5
    rho_bulk    = 1500.0               # kg/m³
    q_mass_flux = C_bagnold * (rho_air / (gravity_g * 9.81)) * 1.0 * (u_star ** 3)
    sec_per_yr  = 31_536_000.0
    T_aeol      = (q_mass_flux * W_path_m / rho_bulk) * sec_per_yr  # m³/yr

    # Glacial
    T_glac = W_glac * A_land * f_ice * gravity_g * 1e6  # m³/yr

    # Net fluxes
    T_out_mtn    = min(W_mtn * A_mtn * 1e6,    T_fluv * 0.6 + T_aeol * 0.2 + T_glac * 0.8)
    T_out_craton = min(W_craton * A_craton * 1e6, T_fluv * 0.4 + T_aeol * 0.8 + T_glac * 0.2)
    T_in_basin   = T_out_mtn + T_out_craton

    # ── Sinks and equilibrium depths ──────────────────────────
    # Subduction removal
    is_active = "ACTIVE" in tectonic_str or "VIGOROUS" in tectonic_str
    subduction_rate = subduction_trenches * 1.5e9 if is_active else 0.0

    # Mountains (high erosion, low retention)
    if T_out_mtn > 0:
        D_mtn = (W_mtn * A_mtn * 1e6) / T_out_mtn
    else:
        D_mtn = W_mtn * age_yr
    D_mtn = min(max(D_mtn, 0.05), 2.0)

    # Continental cratons — net retention after transport removal
    D_craton = (W_craton * A_craton * 1e6 * age_yr - T_out_craton * age_yr) / max(A_craton * 1e6, 1.0)
    D_craton = max(D_craton, 0.0)
    if f_ice > 0.1:
        D_craton = min(max(D_craton, 5.0), 50.0)
    else:
        D_craton = min(max(D_craton, 10.0), 100.0)

    # Sedimentary basins — mass balance
    net_basin_influx = T_in_basin - subduction_rate
    if net_basin_influx > 0 and A_basin > 0:
        D_basin_total = (net_basin_influx * age_yr) / max(A_basin * 1e6, 1.0)
    elif A_basin > 0:
        D_basin_total = 0.0
    else:
        D_basin_total = W_craton * age_yr
    # Basin fills to topographic rim then overflows — physical ceiling is isostatic basin depth
    D_basin_total    = min(D_basin_total, basin_depth_m)
    # Lithification at 500 m: loose regolith vs compacted sedimentary rock
    D_basin_regolith = min(D_basin_total, 500.0)

    # Geothermal oases (accelerated local chemical weathering)
    D_geo = W_chem * 10.0 * age_yr * 0.01
    D_geo = min(max(D_geo, 0.5), 20.0)

    # Subglacial till
    D_subglac = (W_glac * age_yr * 0.5) if f_ice > 0 else 0.0
    D_subglac = min(max(D_subglac, 1.0), 50.0)

    return {
        "Continental Cratons":           round(D_craton, 1),
        "Active Mountain Belts":         round(D_mtn, 2),
        "Sedimentary Basins (regolith)": round(D_basin_regolith, 1),
        "Sedimentary Basins (total)":    round(D_basin_total, 1),
        "Geothermal Oases":              round(D_geo, 1),
        "Subglacial Till":               round(D_subglac, 1),
        "_transport": {
            "T_aeol_km3":      round(T_aeol / 1e9, 3),
            "T_glac_km3":      round(T_glac / 1e9, 4),
            "T_fluv_km3":      round(T_fluv / 1e9, 2),
            "subduction_km3":  round(subduction_rate / 1e9, 2),
            "T_in_basin_m3yr": T_in_basin,   # raw influx — subduction handled by compute_basin_overflow Level 4
        }
    }


def compute_mean_regolith_depth(depths, f_land, clustering, f_ice):
    """
    Weighted mean across terrain classes using updated keys.
    """
    weights = {
        "Continental Cratons":           0.45 * (1 - f_ice),
        "Active Mountain Belts":         0.10,
        "Sedimentary Basins (regolith)": 0.25 * clustering,
        "Sedimentary Basins (total)":    0.0,   # excluded — rock not regolith
        "Geothermal Oases":              0.05,
        "Subglacial Till":               0.15 * f_ice,
    }
    total_w = sum(weights.values())
    if total_w == 0:
        return 0.0
    mean = sum(depths[k] * weights[k] for k in depths if k in weights) / total_w
    return round(mean, 1)


def compute_regolith_ph(co2_ppm, hotspots, f_land):
    """
    pH balance: CO2 acidification vs. mafic rock buffering.
    More hotspots → more basaltic dust → higher pH (more alkaline).
    Higher CO2 → lower pH (more acidic).
    Earth baseline: ~6.5 surface regolith pH.
    """
    acid_factor  = math.log10(co2_ppm / 400.0 + 1.0) * 0.8
    buffer_factor = min(1.5, hotspots / 30.0) * 0.6
    return round(max(4.5, min(8.5, 6.5 - acid_factor + buffer_factor)), 1)


def compute_nutrients(cmf, hotspots, co2_ppm, t_surf, heat_flux):
    """
    Adjust baseline nutrients for this world's specific conditions.
    High iron world → very high Fe.
    Many hotspots → more P and Ca from basalt.
    Cold world → N even more limited (no lightning, minimal volcanic NH3).
    """
    nutrients = dict(NUTRIENT_BASELINES)
    # Iron scales with CMF
    nutrients["Iron"] = min(1.0, 0.5 + cmf * 0.8)
    # Phosphorus scales with hotspot count
    nutrients["Phosphorus"] = min(0.8, 0.15 + hotspots / 200.0)
    # Nitrogen: minimal on frozen world
    lightning_n = max(0.01, (t_surf - 220.0) / 600.0)
    volcanic_n  = heat_flux / CHONDRITIC_HEAT_BASELINE * 0.015
    nutrients["Nitrogen"] = round(min(0.08, lightning_n + volcanic_n), 3)
    return nutrients


def compute_biological_readiness(depths, ph, nutrients, t_surf,
                                  hotspots, permafrost_m):
    """
    Biological Readiness Index (BRI): 0.0–1.0
    Components:
      - Substrate depth (>0.5m on at least 50% of land): 0–0.25
      - pH in viable range (5.5–8.0): 0–0.20
      - Nutrient availability (weighted): 0–0.25
      - Temperature (warmer = better): 0–0.20
      - Liquid water access (geothermal oases): 0–0.10
    """
    # Depth score
    mean_d = sum(depths.values()) / len(depths)
    depth_score = min(0.25, mean_d / 20.0 * 0.25)

    # pH score
    ph_score = 0.20 if 5.5 <= ph <= 8.0 else 0.05

    # Nutrient score (average, weighted by importance)
    weights = {"Phosphorus": 2, "Potassium": 1, "Iron": 1,
               "Nitrogen": 4, "Calcium": 1, "Magnesium": 1}
    total_w = sum(weights.values())
    nut_avg = sum(nutrients[k] * weights[k] for k in weights) / total_w
    nut_score = min(0.25, nut_avg * 0.25)

    # Temperature score
    if t_surf >= 273.15:
        temp_score = 0.20
    elif t_surf >= 250.0:
        temp_score = 0.08
    else:
        temp_score = 0.02

    # Liquid water access
    water_score = min(0.10, hotspots / 500.0)

    bri = depth_score + ph_score + nut_score + temp_score + water_score
    return round(min(1.0, bri), 2)


def co2_tension_legacy(co2_ppm, heat_flux, fold_mountains, divergent):
    """
    Assess the legacy of the CO2 tension flagged in Variable Six.
    High CO2 vs. low volcanic activity implies a past thermal event.
    Returns description of buried geologic legacy.
    """
    expected = 280 * ((fold_mountains + divergent) * heat_flux / EARTH_QHF / 30.0) ** 0.7
    ratio = co2_ppm / max(1.0, expected)
    if ratio > 5.0:
        return ("Deep buried carbonate horizons and chemically weathered clay layers "
                "detected beneath permafrost — legacy of a past hyperthermal flood basalt event.")
    elif ratio > 2.0:
        return ("Moderate carbonate deposits in basin floors — elevated past outgassing "
                "episode implied, chemical weathering products preserved.")
    return "CO2 consistent with current tectonic activity — no major legacy event detected."


def compute_basin_overflow(
    T_in_basin, subduction_rate, age_yr,
    A_basin_m2, maj_endo, maj_exo,
    b2_km, rift_valleys, subduction_trenches,
    f_land, sa_km2, clustering, f_ice,
    tectonic_str, water_eo, freeboard_km, t_surf
):
    """
    4-Level Topographic Sink Hierarchy.
    Sediment cascades from endorheic basins → rift valleys → ocean margins → subduction.
    Replaces the isostatic depth cap with modelled overflow physics.
    Mass is conserved at every level.
    """
    # ── Level 1: Endorheic Basins ────────────────────────────
    shape_factor = 0.33   # bowl/conical depression approximation
    V_endo = A_basin_m2 * (b2_km * 1000.0) * shape_factor

    # Guard: T_in_basin must be non-negative — negative values indicate
    # subduction removal already exceeds influx (net drawdown, no accumulation)
    T_in_basin = max(0.0, T_in_basin)

    fill_time_yr = V_endo / T_in_basin if T_in_basin > 0 else float('inf')
    basin_fill_time_gyr = fill_time_yr / 1e9

    endo_in = T_in_basin * age_yr
    if endo_in <= V_endo:
        endo_stored  = endo_in
        overflow_1   = 0.0
        stranded_vol = 0.0
    else:
        endo_stored  = V_endo   # basin is full — depth = b2_km * 1000 * 0.33
        raw_overflow = endo_in - V_endo
        # Frozen worlds: ice viscosity traps most overflow locally on cratons
        ice_mod     = 0.20 if t_surf < 273.15 else 1.0
        # Supercontinents: enormous distance to coast strands sediment on plains
        cluster_mod = 0.50 if clustering > 0.70 else 1.0
        overflow_1   = raw_overflow * ice_mod * cluster_mod
        # Stranded sediment redistributes onto craton surface — NOT back into basin
        stranded_vol = raw_overflow - overflow_1

    D_basin_total     = endo_stored / A_basin_m2 if A_basin_m2 > 0 else 0.0
    overflow_volume_km3 = overflow_1 / 1e9

    # ── Level 2: Rift Valleys ────────────────────────────────
    L_rift = 1_000_000.0    # 1000 km per rift, in metres
    W_rift =    50_000.0    # 50 km width
    V_rift = rift_valleys * L_rift * W_rift * (b2_km * 1000.0) * 0.5

    rift_stored      = min(overflow_1, V_rift)
    rift_fill_frac   = (rift_stored / V_rift) if V_rift > 0 else (1.0 if overflow_1 > 0 else 0.0)
    overflow_2       = overflow_1 - rift_stored

    # ── Level 3: Ocean Margins / Continental Shelves ─────────
    R_planet_m    = math.sqrt((sa_km2 * 1e6) / (4.0 * math.pi))
    coast_factor  = 1.0 + (1.0 - clustering) * 0.5
    L_coast       = 2.0 * math.pi * R_planet_m * f_land * coast_factor
    W_shelf       = 100_000.0 * max(0.1, 2.0 - water_eo / 5.0)   # m
    V_shelf       = L_coast * W_shelf * (freeboard_km * 1000.0) * 0.5

    shelf_stored  = min(overflow_2, V_shelf)
    shelf_depth_m = shelf_stored / (L_coast * W_shelf) if (L_coast * W_shelf) > 0 else 0.0
    overflow_3    = overflow_2 - shelf_stored

    # ── Level 4: Subduction Trenches (ultimate sink) ─────────
    is_active     = "ACTIVE" in tectonic_str or "VIGOROUS" in tectonic_str
    if not is_active:
        subducted       = 0.0
        abyssal_excess  = overflow_3
    else:
        subducted_cap   = subduction_rate * age_yr
        subducted       = min(overflow_3, subducted_cap)
        abyssal_excess  = overflow_3 - subducted

    cascade_complete = abyssal_excess <= 1.0   # m³ tolerance

    return {
        "D_basin_total":        round(D_basin_total, 1),
        "overflow_volume_km3":  round(overflow_volume_km3, 2),
        "rift_fill_fraction":   round(rift_fill_frac, 3),
        "shelf_sediment_depth_m": round(shelf_depth_m, 1),
        "cascade_complete":     cascade_complete,
        "basin_fill_time_gyr":  round(basin_fill_time_gyr, 2),
        "stranded_vol_km3":     round(stranded_vol / 1e9, 2),
    }


# ============================================================
# RUN
# ============================================================

def run(seed=None, cmf_input=None, star_mass_input=None, orbital_d_input=None):
    if seed is None:
        seed = random.randint(0, 2**32 - 1)
    rng  = random.Random(seed)

    print("=" * 62)
    print("  MORTALIS WORLD GENERATION ENGINE")
    print("  Ontogenetic Simulation — Physical First Principles")
    print("=" * 62)
    print(f"\n  Seed: {seed}")

    # ── VARIABLE ONE ──────────────────────────────────────────

    print("\n══ VARIABLE ONE: PLANETARY MASS ════════════════════════════")
    mass_earth = generate_mass(rng)
    mass_kg    = mass_earth * EARTH_MASS

    r1   = compute_radius_baseline(mass_kg)
    sa1  = compute_surface_area(r1)
    g1   = compute_gravity(mass_kg, r1)
    g1_g = g1 / 9.81
    ve1  = compute_escape_velocity(mass_kg, r1)
    hf1  = compute_heat_flux_baseline(mass_kg, sa1)
    ls1  = compute_geologic_lifespan(mass_kg, sa1)
    ra1  = compute_rayleigh_active(hf1, g1)
    gs1  = geologic_status(ls1, ra1)
    mtn1 = compute_max_mountain_km(g1)
    b1_km, b1_cat = compute_isostatic_basin(g1)
    hor1 = compute_horizon_km(r1)

    print(f"\n── AXIOMATIC VARIABLE ──────────────────────────────────────")
    print(f"  Planetary Mass (M)     : {mass_earth:.4f} M⊕  ({mass_kg:.4e} kg)")
    print(f"  Baseline Bulk Density  : {RHO_BULK_BASELINE} kg/m³  [temporary constant]")
    print(f"  Isotope Fraction       : Chondritic baseline  [temporary constant]")
    print(f"\n── FIRST-ORDER: SPATIAL & GRAVITATIONAL FRAMEWORK ─────────")
    print(f"  Planetary Radius (R)   : {r1/1000:,.1f} km")
    print(f"  Surface Area (A)       : {sa1/1e6:.3e} km²")
    print(f"  Surface Gravity (g)    : {g1_g:.3f} g  ({g1:.2f} m/s²)")
    print(f"  Escape Velocity (Ve)   : {ve1/1000:.2f} km/s")
    print(f"  Horizon Distance       : {hor1:.2f} km  (at 1.7m observer height)")
    print(f"\n── SECOND-ORDER: THERMODYNAMIC ENGINE ──────────────────────")
    print(f"  Internal Heat Flux     : {hf1:.4f} W/m²  [Earth: {CHONDRITIC_HEAT_BASELINE} W/m²]")
    print(f"  Geologic Lifespan      : {ls1:.2f} billion years")
    print(f"  Current Simulation Age : {SIMULATION_AGE_GYR} billion years")
    print(f"  Mantle Convection      : {gs1}")
    print(f"\n── THIRD-ORDER: LITHOSPHERIC TOPOLOGY & POTENTIAL ─────────")
    print(f"  Max Mountain Height    : {mtn1:.2f} km  [Earth reference: ~8.85 km]")
    print(f"  Max Ocean Basin Depth  : {b1_km:.2f} km")
    print(f"  Basin Configuration    : {b1_cat}")
    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    print(f"  Gravity Profile        : {gravity_label(g1_g)}")
    print(f"\n  Variable One complete. Temporary constants active.")
    print(f"  Ready to receive Variable Two: Bulk Composition.")

    # ── VARIABLE TWO ──────────────────────────────────────────

    print(f"\n══ VARIABLE TWO: BULK COMPOSITION ══════════════════════════")
    if cmf_input is not None:
        if not (CMF_MIN <= cmf_input <= CMF_MAX):
            print(f"\n  ERROR: CMF {cmf_input} outside valid range [{CMF_MIN}, {CMF_MAX}]"); return
        cmf = cmf_input
        print(f"\n  Core Mass Fraction (CMF): {cmf:.4f}  [user specified]")
    else:
        cmf = generate_cmf(rng)
        print(f"\n  Core Mass Fraction (CMF): {cmf:.4f}  [procedurally generated]")

    true_rho = compute_true_bulk_density(cmf)
    print(f"  Composition            : {cmf*100:.1f}% iron core / {(1-cmf)*100:.1f}% silicate mantle")
    print(f"  True Bulk Density      : {true_rho:.1f} kg/m³  [replaces {RHO_BULK_BASELINE} kg/m³]")
    print(f"  Composition Class      : {cmf_class(cmf)}")

    print(f"\n── RECALCULATION CASCADE: VARIABLE ONE UPDATES ─────────────")
    r2      = compute_radius_composition(mass_kg, cmf)
    r2_km   = r2 / 1000.0
    r_delta = r2_km - r1 / 1000.0
    sa2     = compute_surface_area(r2)
    g2      = compute_gravity(mass_kg, r2)
    g2_g    = g2 / 9.81
    ve2     = compute_escape_velocity(mass_kg, r2)
    hf2     = compute_heat_flux_composition(mass_kg, sa2, cmf)
    ls2     = compute_geologic_lifespan(mass_kg, sa2)
    ra2     = compute_rayleigh_active(hf2, g2)
    gs2     = geologic_status(ls2, ra2)
    mtn2    = compute_max_mountain_km(g2)
    b2_km, b2_cat = compute_isostatic_basin(g2)
    hor2    = compute_horizon_km(r2)

    sign = "+" if r_delta >= 0 else ""
    print(f"  Planetary Mass (M)     : {mass_earth:.4f} M⊕  [locked — unchanged]")
    print(f"  Compressed Radius (R)  : {r2_km:,.1f} km  ({sign}{r_delta:.1f} km from baseline)")
    print(f"    [Zeng et al. 2016 two-layer empirical relation applied]")
    print(f"  Surface Area (A)       : {sa2/1e6:.3e} km²")
    print(f"  Surface Gravity (g)    : {g2_g:.3f} g  ({g2:.2f} m/s²)  [was {g1_g:.3f} g]")
    print(f"  Escape Velocity (Ve)   : {ve2/1000:.2f} km/s  [was {ve1/1000:.2f} km/s]")
    print(f"  Internal Heat Flux     : {hf2:.4f} W/m²  [was {hf1:.4f} W/m²]")
    print(f"    [Radiogenic budget corrected: {(1-cmf)*100:.1f}% mantle fraction]")
    print(f"  Geologic Lifespan      : {ls2:.2f} Gyr  [was {ls1:.2f} Gyr]")
    print(f"  Mantle Convection      : {gs2}")
    print(f"  Tectonic Regime        : {tectonic_regime(hf2, cmf)}")
    print(f"  Max Mountain Height    : {mtn2:.2f} km  [was {mtn1:.2f} km]")
    print(f"  Max Ocean Basin Depth  : {b2_km:.2f} km  [was {b1_km:.2f} km]")
    print(f"  Basin Configuration    : {b2_cat}")
    print(f"  Horizon Distance       : {hor2:.2f} km  [was {hor1:.2f} km]")

    print(f"\n── NEW PROPERTIES UNLOCKED BY VARIABLE TWO ─────────────────")
    core_km, crf, mantle_km = compute_core_geometry(r2, cmf)
    dynamo, dynamo_note     = compute_dynamo(cmf, ls2)
    print(f"  Core Radius Fraction   : {crf:.3f}  ({crf*100:.1f}% of planetary radius)")
    print(f"    [CRF = sqrt(CMF) — Zeng et al. approximation]")
    print(f"  Core Radius            : {core_km:,.1f} km")
    print(f"  Mantle Thickness       : {mantle_km:,.1f} km")
    print(f"  Magnetic Dynamo        : {'ACTIVE' if dynamo else 'INACTIVE'} — {dynamo_note}")

    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    print(f"  Gravity Profile        : {gravity_label(g2_g)}")
    print(f"  Magnetosphere          : {'Present — shielded from stellar wind' if dynamo else 'Absent — surface exposed to stellar radiation'}")
    print(f"\n  Variable Two complete. Temporary constants replaced.")
    print(f"  Planetary interior and geometry locked.")
    print(f"  Unresolved dependency: Surface temperature.")
    print(f"  Ready to receive Variable Three: Stellar Insolation.")

    # ── VARIABLE THREE ────────────────────────────────────────

    print(f"\n══ VARIABLE THREE: STELLAR INSOLATION ══════════════════════")

    # Generate star
    if star_mass_input is not None:
        if not (STAR_MASS_MIN <= star_mass_input <= STAR_MASS_MAX):
            print(f"\n  ERROR: Star mass {star_mass_input} outside valid range [{STAR_MASS_MIN}, {STAR_MASS_MAX}]"); return
        star_mass = star_mass_input
        print(f"\n  Generating Host Star via Initial Mass Function...")
        print(f"  Host Star Mass         : {star_mass:.3f} M☉  [user specified]")
    else:
        star_mass = generate_star_mass(rng)
        print(f"\n  Generating Host Star via Initial Mass Function...")
        print(f"  Host Star Mass         : {star_mass:.3f} M☉  [procedurally generated]")

    lum_solar  = compute_star_luminosity(star_mass)
    lum_watts  = lum_solar * SOLAR_LUM
    star_life  = compute_star_lifespan(star_mass) / 1e9   # Gyr
    spec_class = stellar_classification(star_mass)

    hz_inner, hz_outer = compute_habitable_zone(lum_solar)

    # Generate orbit
    if orbital_d_input is not None:
        if not (hz_inner <= orbital_d_input <= hz_outer):
            print(f"\n  WARNING: Orbital distance {orbital_d_input} AU outside HZ [{hz_inner:.3f}, {hz_outer:.3f}] AU")
        d_au = orbital_d_input
        print(f"  Calculating Habitable Zone Boundaries...")
        print(f"  Generating Orbital Distance...")
    else:
        d_au = generate_orbital_distance(rng, hz_inner, hz_outer)
        print(f"  Calculating Habitable Zone Boundaries...")
        print(f"  Generating Orbital Distance...")

    d_m          = d_au * AU
    period_days  = compute_orbital_period_days(d_au, star_mass)
    month_days   = period_days / 24.0
    hz_label     = hz_position_label(d_au, hz_inner, hz_outer)
    flux_wm2     = compute_insolation_flux(lum_watts, d_m)
    t_eq         = compute_equilibrium_temp(lum_watts, d_m)
    t_eq_c       = t_eq - 273.15
    t_surface    = t_eq + GREENHOUSE_TEMP
    t_surface_c  = t_surface - 273.15

    print(f"\n── AXIOMATIC VARIABLE: THE HOST STAR ──────────────────────")
    print(f"  Stellar Classification : {spec_class}")
    print(f"  Stellar Mass           : {star_mass:.3f} M☉")
    print(f"  Luminosity (L_star)    : {lum_solar:.3f} L☉  ({lum_watts:.3e} W)")
    print(f"  Main Sequence Lifespan : {star_life:.1f} billion years")
    print(f"  Current Simulation Age : {SIMULATION_AGE_GYR} billion years (Stable Phase)")
    print(f"  Sky Character          : {stellar_sky_note(star_mass)}")
    print(f"    [Final sky color deferred to Variable Four: Atmosphere]")

    print(f"\n── FIRST-ORDER: ORBITAL & CALENDAR DYNAMICS ───────────────")
    print(f"  Habitable Zone Inner   : {hz_inner:.3f} AU")
    print(f"  Semi-Major Axis (d)    : {d_au:.3f} AU  —  {hz_label}")
    print(f"  Habitable Zone Outer   : {hz_outer:.3f} AU")
    print(f"  Orbital Eccentricity   : 0.00  [temporary constant]")
    print(f"  Orbital Period (Year)  : {period_days:.1f} Earth days")
    print(f"  MORTALIS Calendar      : 24 months × {month_days:.2f} days/month")

    print(f"\n── SECOND-ORDER: THERMODYNAMIC ENERGY BUDGET ──────────────")
    print(f"  Bond Albedo (α)        : {ALBEDO_TEMP:.2f}  [temporary constant]")
    print(f"  Greenhouse Adjustment  : +{GREENHOUSE_TEMP:.0f} K  [temporary constant]")
    print(f"  Insolation Flux (S)    : {flux_wm2:.1f} W/m²  [Earth reference: 1361 W/m²]")
    print(f"  Internal Heat Flux     : {hf2:.4f} W/m²  [negligible to global T_eq]")
    print(f"  Equilibrium Temp (Teq) : {t_eq:.1f} K  ({t_eq_c:.1f} °C)")
    print(f"  Surface Temp w/ GH     : {t_surface:.1f} K  ({t_surface_c:.1f} °C)")
    print(f"    [True surface temp deferred to Variable Four: Atmosphere]")

    print(f"\n── THIRD-ORDER: ATMOSPHERIC RETENTION (JEANS ESCAPE) ──────")
    print(f"  Planet Escape Velocity : {ve2/1000:.2f} km/s")
    print(f"  Assessment Temperature : {t_eq:.1f} K  (T_eq)")
    print(f"\n  Gas Retention Profile:")
    retention = jeans_retention(ve2, t_eq)
    for name, symbol, v_th, ratio, status in retention:
        print(f"    {name:<18} ({symbol:<4}) v_th={v_th:.3f} km/s  ratio={ratio:5.1f}  {status}")

    sputtering = magnetosphere_sputtering_note(dynamo, star_mass)
    print(f"\n  Magnetosphere / Wind   : {sputtering}")

    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    # Climate character
    if t_surface_c < -40:   climate = "Frozen — CO₂ greenhouse may be insufficient; glaciation likely"
    elif t_surface_c < -10: climate = "Cold — marginal habitability, ice ages probable"
    elif t_surface_c < 20:  climate = "Temperate — liquid water plausible across broad latitudes"
    elif t_surface_c < 50:  climate = "Warm — tropical-dominant world, ice caps minimal"
    else:                   climate = "Hot — runaway conditions possible; ocean boiling risk"
    print(f"  Climate Character      : {climate}")
    print(f"  Year Length            : {period_days:.1f} days  ({period_days/365.25:.2f} Earth years)")
    print(f"  Calendar Month         : {month_days:.2f} days")

    print(f"\n  Variable Three complete. External energy budget locked.")
    print(f"  Temporary constants still active:")
    print(f"    — Bond Albedo (α = {ALBEDO_TEMP}) — replaced by Variable Four")
    print(f"    — Greenhouse offset (+{GREENHOUSE_TEMP:.0f} K) — replaced by Variable Four")
    print(f"    — Orbital eccentricity (e = 0.00) — deferred")
    print(f"  Ready to receive Variable Four: Atmosphere & Hydrology.")

    # ── VARIABLE FOUR ─────────────────────────────────────────

    print(f"\n══ VARIABLE FOUR: ATMOSPHERE & HYDROLOGY ═══════════════════")

    print(f"\n  Deriving Atmospheric Mass from Physical Balance...")
    tect_regime  = tectonic_regime(hf2, cmf)
    pressure_atm, M_outgas, M_jeans, M_sputter = compute_pressure_physical(
        rng, mass_kg, r2, g2, hf2, tect_regime,
        t_eq, lum_solar, d_au, dynamo)
    pressure_pa  = pressure_atm * 101325.0

    print(f"  Generating Atmospheric Composition...")
    co2_ppm      = generate_co2_ppm(rng, tect_regime, hf2)
    ar_frac      = generate_argon_fraction(hf2)
    co2_frac     = co2_ppm / 1e6
    o2_frac      = 0.0          # abiotic — no free oxygen yet
    n2_frac      = max(0.0, 1.0 - co2_frac - ar_frac - o2_frac)

    print(f"  Generating Total Water Inventory...")
    water_eo = generate_water_inventory(rng)

    print(f"\n── 1. ATMOSPHERIC PROFILE ──────────────────────────────────")
    print(f"  Pressure Derivation    : [M_outgas - M_jeans - M_sputter] × g / A")
    print(f"    Outgassed Mass       : {M_outgas:.3e} kg")
    print(f"    Jeans Escape Loss    : {M_jeans:.3e} kg")
    print(f"    Sputtering Loss      : {M_sputter:.3e} kg")
    print(f"  Surface Pressure       : {pressure_atm:.3f} atm  ({pressure_pa:,.0f} Pa)")
    print(f"  Composition (Vol %)    :")
    print(f"    Nitrogen  (N₂)       : {n2_frac*100:.1f}%")
    print(f"    CO₂                  : {co2_frac*100:.2f}%  [{co2_ppm:.0f} ppm]")
    print(f"    Argon     (Ar)       : {ar_frac*100:.2f}%  [radiogenic K-40 indicator]")
    print(f"    Oxygen    (O₂)       : {o2_frac*100:.1f}%  [abiotic — placeholder]")

    delta_f, delta_t_gh = compute_greenhouse(co2_ppm, pressure_atm)
    print(f"  Greenhouse Forcing ΔF  : {delta_f:+.1f} W/m²")
    print(f"  True Greenhouse ΔT_GH  : {delta_t_gh:+.1f} K  [replaces +{GREENHOUSE_TEMP:.0f} K placeholder]")
    print(f"    [Pressure broadening applied at {pressure_atm:.2f} atm]")

    # ── CLIMATE RESOLUTION SEQUENCE ───────────────────────────

    print(f"\n── 2. HYDROLOGY & PHASE PARTITIONING ───────────────────────")
    print(f"  Total Water Inventory  : {water_eo:.2f} EO  (Earth Oceans)")
    sa2_km2 = sa2 / 1e6

    print(f"\n── 3. CLIMATE RESOLUTION SEQUENCE ──────────────────────────")

    # Iteration 1
    t_surf_1 = t_eq + delta_t_gh
    print(f"\n  [Iteration 1]")
    print(f"  Initial T_eq (V3)      : {t_eq:.1f} K")
    print(f"  First-pass T_surf      : {t_surf_1:.1f} K  ({t_surf_1-273.15:.1f} °C)")

    f_ocean_1, f_ice_1, f_land_1, phase_1 = compute_phase_partition(
        t_surf_1, pressure_atm, water_eo, b2_km, sa2_km2)
    print(f"  Water Phase State      : {'FROZEN' if phase_1 == 'ice' else 'FLOODED' if phase_1 == 'flooded' else 'LIQUID'}")
    print(f"  Ocean Coverage         : {f_ocean_1:.2f}  |  Ice: {f_ice_1:.2f}  |  Land: {f_land_1:.2f}")

    alpha_1 = compute_true_albedo(f_ocean_1, f_ice_1, f_land_1)
    print(f"  True Albedo            : {alpha_1:.3f}  [replaces {ALBEDO_TEMP} placeholder]")

    # Iteration 2
    t_eq_2   = compute_teq_with_albedo(lum_watts, d_m, alpha_1)
    t_surf_2 = t_eq_2 + delta_t_gh
    print(f"\n  [Iteration 2]")
    print(f"  Recomputed T_eq        : {t_eq_2:.1f} K  (updated albedo applied)")
    print(f"  Final T_surf           : {t_surf_2:.1f} K  ({t_surf_2-273.15:.1f} °C)")

    f_ocean_2, f_ice_2, f_land_2, phase_2 = compute_phase_partition(
        t_surf_2, pressure_atm, water_eo, b2_km, sa2_km2)

    # Convergence check
    converged = (phase_1 == phase_2)
    print(f"  Water Phase State      : {'FROZEN' if phase_2 == 'ice' else 'FLOODED' if phase_2 == 'flooded' else 'LIQUID'}")
    print(f"  Convergence            : {'ACHIEVED — climate state locked' if converged else 'NOT CONVERGED — additional iteration needed'}")

    # Use iteration 2 as final
    t_surf_final = t_surf_2
    f_ocean_f    = f_ocean_2
    f_ice_f      = f_ice_2
    f_land_f     = f_land_2
    alpha_final  = compute_true_albedo(f_ocean_f, f_ice_f, f_land_f)

    world_type = classify_world(t_surf_final, f_ocean_f, f_ice_f, water_eo)
    sky_color  = compute_sky_color(star_mass, pressure_atm, co2_ppm, f_ice_f)

    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    print(f"  World Type             : {world_type}")
    print(f"  True Surface Temp      : {t_surf_final:.1f} K  ({t_surf_final-273.15:.1f} °C)")
    print(f"  True Bond Albedo       : {alpha_final:.3f}")
    print(f"  True Greenhouse ΔT     : {delta_t_gh:+.1f} K")
    print(f"  Ocean Coverage         : {f_ocean_f:.2f}  ({f_ocean_f*100:.0f}% of surface)")
    print(f"  Ice Coverage           : {f_ice_f:.2f}  ({f_ice_f*100:.0f}% of surface)")
    print(f"  Land Coverage          : {f_land_f:.2f}  ({f_land_f*100:.0f}% of surface)")
    print(f"  Water Inventory        : {water_eo:.2f} EO")
    print(f"  Sky Color              : {sky_color}")
    print(f"  Year Length            : {period_days:.1f} days  ({period_days/365.25:.2f} Earth years)")
    print(f"  Calendar Month         : {month_days:.2f} days")

    print(f"\n  Variable Four complete. Climate and albedo locked.")
    print(f"  Temporary constants still active:")
    print(f"    — Cloud fraction ({CLOUD_FRAC}) — replaced by Variable Five")
    print(f"    — Orbital eccentricity (0.00) — replaced by Variable Five")
    print(f"    — O₂/CH₄ fractions (0.0) — replaced by biology variable")
    print(f"  Unresolved dependency: Coriolis effect & weather patterns.")
    print(f"  Ready to receive Variable Five: Planetary Kinematics.")

    # ── VARIABLE FIVE ─────────────────────────────────────────

    print(f"\n══ VARIABLE FIVE: PLANETARY KINEMATICS ═════════════════════")

    print(f"\n  Checking Tidal Locking Constraints...")
    is_locked, t_lock_gyr = check_tidal_locking(
        star_mass, d_au, mass_kg, r2)
    print(f"  Generating Rotation Rate...")
    sidereal_h = generate_rotation(rng, is_locked, period_days)
    solar_h    = compute_solar_day(sidereal_h, period_days)
    omega      = compute_angular_velocity(sidereal_h)
    coriolis   = compute_coriolis(omega)

    print(f"  Generating Axial Tilt...")
    tilt_deg   = generate_axial_tilt(rng)
    moon_flag  = generate_moon_flag(rng, tilt_deg)

    phi_h      = compute_hadley_boundary(omega, t_surf_final, r2)
    diurnal    = compute_diurnal_range(solar_h, pressure_atm, f_ocean_f)
    seasonal   = compute_seasonal_ice_status(tilt_deg, t_surf_final)
    precip     = precipitation_profile(phi_h, tilt_deg)

    # Cloud fraction update + recalculation cascade
    f_cloud_new  = compute_updated_cloud_fraction(omega, t_surf_final, f_ocean_f)
    alpha_v5     = compute_true_albedo(f_ocean_f, f_ice_f, f_land_f)
    # Adjust albedo for new cloud fraction delta
    cloud_delta  = f_cloud_new - CLOUD_FRAC
    alpha_v5_adj = min(0.95, max(0.05, alpha_v5 + cloud_delta * ALBEDO_CLOUD * 0.5))
    t_eq_v5      = compute_teq_with_albedo(lum_watts, d_m, alpha_v5_adj)
    t_surf_v5    = t_eq_v5 + delta_t_gh

    print(f"\n── 1. ROTATIONAL PROFILE ────────────────────────────────────")
    print(f"  Tidal Locking          : {'TRUE — rotation = orbital period' if is_locked else f'FALSE  (t_lock ≈ {t_lock_gyr:.1f} Gyr > simulation age)'}")
    print(f"  Sidereal Day Length    : {sidereal_h:.2f} hours")
    print(f"  Solar Day Length       : {solar_h:.2f} hours")
    print(f"  Angular Velocity (Ω)   : {omega:.3e} rad/s")
    print(f"  Mid-Lat Coriolis (45°) : {coriolis:.3e} s⁻¹")

    print(f"\n── 2. ORIENTATION & SEASONALITY ─────────────────────────────")
    print(f"  Axial Tilt             : {tilt_deg:.1f}°")
    print(f"  Moon Flag              : {'TRUE — tilt stabilised over geological time' if moon_flag else 'FALSE — chaotic tilt oscillation possible'}")
    print(f"  Seasonal Ice Status    : {seasonal}")
    print(f"  Diurnal Temp Range     : {diurnal:.1f} K")

    print(f"\n── 3. ATMOSPHERIC CIRCULATION & WEATHER ─────────────────────")
    print(f"  Hadley Cell Boundary   : ±{phi_h:.1f}° latitude")
    print(f"  Precipitation Profile  :")
    for band in precip:
        print(f"    {band}")
    print(f"  Updated Cloud Fraction : {f_cloud_new:.2f}  [replaces {CLOUD_FRAC} placeholder]")

    print(f"\n── 4. CLIMATE RECALCULATION (CLOUD FRACTION UPDATE) ─────────")
    print(f"  Cloud Δ                : {cloud_delta:+.2f}  ({'less cloud → lower albedo' if cloud_delta < 0 else 'more cloud → higher albedo'})")
    print(f"  Updated Bond Albedo    : {alpha_v5_adj:.3f}  [was {alpha_final:.3f}]")
    print(f"  Updated T_eq           : {t_eq_v5:.1f} K")
    print(f"  Updated T_surf         : {t_surf_v5:.1f} K  ({t_surf_v5-273.15:.1f} °C)  [was {t_surf_final-273.15:.1f} °C]")

    print(f"\n── 5. MORTALIS TIME SYSTEM LOCKED ───────────────────────────")
    days_per_year  = period_days
    days_per_month = period_days / 24.0
    print(f"  Year Length            : {days_per_year:.1f} solar days")
    print(f"  Months per Year        : 24")
    print(f"  Days per Month         : {days_per_month:.2f} solar days")
    print(f"  Hours per Day          : {solar_h:.2f} hours")
    print(f"  [1 real-world second = {solar_h:.2f} subjective in-game hours]")

    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    world_type_v5 = classify_world(t_surf_v5, f_ocean_f, f_ice_f, water_eo)
    print(f"  World Type             : {world_type_v5}")
    print(f"  Final Surface Temp     : {t_surf_v5:.1f} K  ({t_surf_v5-273.15:.1f} °C)")
    print(f"  Rotation Character     : {'Tidally locked — permanent day/night sides' if is_locked else ('Fast rotator — vigorous weather' if sidereal_h < 14 else 'Moderate rotator — stable circulation' if sidereal_h < 40 else 'Slow rotator — extreme diurnal variation')}")
    print(f"  Tilt Character         : {'Near-zero — no seasons' if tilt_deg < 5 else 'Mild — moderate seasons' if tilt_deg < 25 else 'High — dramatic seasons' if tilt_deg < 50 else 'Extreme — catastrophic seasons'}")

    print(f"\n  Variable Five complete. Kinematics and circulation locked.")
    print(f"  Temporary constants still active:")
    print(f"    — Orbital eccentricity (0.00) — deferred")
    print(f"    — O₂/CH₄ fractions (0.0) — deferred to biology variable")
    print(f"  Unresolved dependency: Continental layout & topography.")
    print(f"  Ready to receive Variable Six: Tectonic Geometry.")

    # ── VARIABLE SIX ──────────────────────────────────────────

    print(f"\n══ VARIABLE SIX: TECTONIC GEOMETRY ═════════════════════════")
    print(f"\n  Generating Tectonic Skeleton...")
    print(f"  Calculating Isostatic Freeboard...")
    print(f"  Intersecting Climate Bands...")

    sa2_km2_v6  = sa2 / 1e6
    tect_str    = tectonic_regime(hf2, cmf)
    n_plates, n_major, n_minor = compute_plate_count(sa2_km2_v6, hf2, tect_str)
    clustering  = generate_clustering(rng)
    cluster_label, cluster_desc = clustering_label(clustering)
    freeboard   = compute_isostatic_freeboard(f_land_f, water_eo, b2_km)
    boundaries  = assign_boundaries(rng, n_plates, tect_str)
    mtn_mean, mtn_max = compute_mountain_heights(
        rng, boundaries["fold_mountains"], mtn2, g2_g)
    trench_depth = compute_trench_depth(g2_g, b2_km)
    hotspots     = compute_hotspot_count(hf2)
    rain_shadows = compute_rain_shadow_count(
        boundaries["fold_mountains"], phi_h, clustering)
    coastline_d  = compute_coastline_complexity(clustering, n_plates, f_land_f)
    aridity_idx  = compute_aridity_index(clustering, phi_h, f_land_f)
    mean_elev    = compute_mean_continental_elevation(freeboard, mtn_mean, f_land_f)
    mean_ocean_d = min(b2_km, b2_km * (1.0 - f_land_f * 0.3))
    co2_ppm, co2_check, co2_tension = reconcile_co2_with_tectonics(
        co2_ppm, boundaries["fold_mountains"], boundaries["divergent"], hf2)

    # If CO2 was reconciled downward, recascade greenhouse and T_surf
    if not co2_tension:
        delta_f, delta_t_gh = compute_greenhouse(co2_ppm, pressure_atm)
        t_surf_v5 = t_eq_v5 + delta_t_gh
        # Repartition water phase at new temperature
        sa2_km2_v6b = sa2 / 1e6
        f_ocean_f, f_ice_f, f_land_f, _ = compute_phase_partition(
            t_surf_v5, pressure_atm, water_eo, b2_km, sa2_km2_v6b)
        # Update atmospheric fractions
        co2_frac = co2_ppm / 1e6
        n2_frac  = max(0.0, 1.0 - co2_frac - ar_frac - o2_frac)

    hab_frac, hab_label = compute_habitability_zones(
        t_surf_v5, f_land_f, f_ice_f, aridity_idx, phi_h)

    print(f"\n── 1. PLATE DISTRIBUTION & CONFIGURATION ───────────────────")
    print(f"  Plate Count            : {n_plates} ({n_major} major, {n_minor} minor)")
    print(f"  Continental Config     : {cluster_label} (clustering: {clustering:.2f})")
    print(f"    [{cluster_desc}]")
    print(f"  Crustal Distribution   : {f_land_f*100:.0f}% continental / {(1-f_land_f)*100:.0f}% oceanic")
    print(f"  Isostatic Freeboard    : {freeboard:.2f} km  [continental elevation above ocean floor]")
    print(f"    [Airy isostasy: h_c={CONTINENTAL_THICKNESS_KM:.0f} km, ρ_crust={RHO_CONTINENTAL:.0f} kg/m³]")

    print(f"\n── 2. BOUNDARY INVENTORY & TOPOGRAPHY ──────────────────────")
    print(f"  Convergent Boundaries  : {boundaries['convergent']}")
    print(f"    Fold Mountains       : {boundaries['fold_mountains']}  "
          f"(mean {mtn_mean:.1f} km, max {mtn_max:.1f} km, ceiling {mtn2:.2f} km)")
    print(f"    Subduction Trenches  : {boundaries['subduction_trenches']}  "
          f"(depth ~{trench_depth:.1f} km — gravity-compressed)")
    print(f"  Divergent Boundaries   : {boundaries['divergent']}")
    print(f"    Rift Valleys         : {boundaries['rift_valleys']}")
    print(f"    Mid-Ocean Ridges     : {boundaries['mid_ocean_ridges']}")
    print(f"  Transform Boundaries   : {boundaries['transform']}")
    print(f"  Hotspot Count          : {hotspots}  (mantle plumes, shield volcanoes)")

    print(f"\n── 3. CLIMATE-TERRAIN INTEGRATION ──────────────────────────")
    print(f"  Rain Shadow Flags      : {rain_shadows} major ranges intersect storm tracks")
    print(f"  Continental Aridity    : {aridity_idx:.2f}  ({aridity_idx*100:.0f}% of land beyond moisture limit)")
    print(f"  Coastline Complexity   : D={coastline_d:.2f}  "
          f"({'smooth, continental' if coastline_d < 1.10 else 'moderate complexity' if coastline_d < 1.20 else 'highly fragmented'})")
    print(f"  Volcanic CO₂ Check     : {co2_check}")

    print(f"\n── 4. TOPOGRAPHIC STATISTICS ────────────────────────────────")
    print(f"  Mean Continental Elev  : {mean_elev:.2f} km above ocean floor")
    print(f"  Mean Ocean Depth       : {mean_ocean_d:.2f} km")
    print(f"  Mountain Ranges        : {boundaries['fold_mountains']}  "
          f"(mean {mtn_mean:.1f} km, max clamped at {mtn2:.2f} km)")
    print(f"  Volcanic Arcs          : {boundaries['subduction_trenches']}")
    print(f"  Rift Valleys           : {boundaries['rift_valleys']}")

    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    if n_plates == 1:
        terrain_char = "Single-plate stagnant lid — no mobile tectonics, mantle plume dominated"
    elif clustering > 0.75:
        terrain_char = f"Vast supercontinent with {boundaries['fold_mountains']} mountain chains — extreme interior aridity"
    elif clustering > 0.50:
        terrain_char = f"Semi-clustered continents — moderate ocean barriers, diverse terrain"
    else:
        terrain_char = f"Dispersed landmasses — maritime-dominant geography, island-rich"
    print(f"  Terrain Character      : {terrain_char}")
    print(f"  Habitability Zones     : {hab_frac:.2f} ({hab_frac*100:.0f}% of surface) — {hab_label}")

    print(f"\n  Variable Six complete. Tectonic skeleton locked.")
    print(f"  Temporary constants still active:")
    print(f"    — Orbital eccentricity (0.00) — deferred")
    print(f"    — O₂/CH₄ fractions (0.0) — deferred to biology variable")
    print(f"  Unresolved dependency: Freshwater distribution and flow.")
    print(f"  Ready to receive Variable Seven: Hydrology & River Systems.")

    # ── VARIABLE SEVEN ────────────────────────────────────────

    print(f"\n══ VARIABLE SEVEN: HYDROLOGY & RIVER SYSTEMS ═══════════════")
    print(f"\n  Mapping Topographic Divides...")
    print(f"  Executing D8 Flow Routing...")
    print(f"  Calculating Ice Mass Balance & Glacial Flow...")

    frozen = t_surf_v5 < 273.15

    permafrost_m    = compute_permafrost_depth(t_surf_v5, hf2)
    active_layer_m  = compute_active_layer(t_surf_v5, tilt_deg, diurnal)
    melt_thresh_m   = compute_subglacial_melt_thickness(t_surf_v5, hf2)
    subglacial_lakes = estimate_subglacial_lakes(
        water_eo, permafrost_m, melt_thresh_m,
        boundaries["fold_mountains"], boundaries["rift_valleys"])

    polar_f, cont_f, mtn_f = compute_ice_distribution(
        water_eo, f_ice_f, clustering, boundaries["fold_mountains"])

    total_basins, maj_exo, maj_endo, divides = compute_drainage_basins(
        sa2_km2_v6, f_land_f, aridity_idx,
        boundaries["fold_mountains"], boundaries["rift_valleys"], clustering)

    n_rivers, avg_len_km, nav_km, connectivity, valley_type = compute_river_networks(
        maj_exo, maj_endo, sa2_km2_v6, f_land_f, aridity_idx, t_surf_v5)

    slr_km = compute_sea_level_rise(water_eo, sa2_km2_v6, f_land_f)
    eq_thresh, global_thresh = compute_activation_thresholds(
        t_surf_v5, water_eo, aridity_idx)

    print(f"\n── 1. FROZEN STATE HYDROLOGY (CURRENT) ─────────────────────")
    if frozen:
        print(f"  Global Water Phase     : SOLID (Ice Sheets & Glaciers)")
        print(f"  Ice Distribution       :")
        print(f"    Polar Caps           : {polar_f*100:.0f}% of inventory (thickest sheets)")
        print(f"    Continental Sheets   : {cont_f*100:.0f}% (mid-latitude coverage)")
        print(f"    Mountain Glaciers    : {mtn_f*100:.0f}% (highland accumulation centres)")
        print(f"  Permafrost Depth       : {permafrost_m:.0f} m")
        print(f"    [Z = λ_rock × (273.15 - T_surf) / Q_hf]")
        print(f"  Active Layer Depth     : {active_layer_m:.1f} m  (seasonal thaw zone)")
        print(f"  Subglacial Melt Thresh : {melt_thresh_m:.0f} m of ice required for basal melt")
        print(f"  Subglacial Hydrology   : {'ACTIVE' if subglacial_lakes > 0 else 'INACTIVE'}")
        if subglacial_lakes > 0:
            print(f"    Est. Subglacial Lakes: {subglacial_lakes} large reservoirs detected")
    else:
        print(f"  Global Water Phase     : LIQUID — surface rivers active")
        print(f"  Permafrost Depth       : 0 m  (surface above freezing)")
        print(f"  Active Layer           : N/A")

    print(f"\n── 2. DRAINAGE BASIN INVENTORY ──────────────────────────────")
    print(f"  Total Basins Delineated: {total_basins}")
    print(f"  Major Exorheic Basins  : {maj_exo}  (drain to ocean)")
    print(f"  Major Endorheic Basins : {maj_endo}  (landlocked sinks)")
    print(f"  Continental Divides    : {divides} primary ridge lines")
    print(f"    [Endorheic fraction driven by aridity index {aridity_idx:.2f}]")

    print(f"\n── 3. RIVER NETWORK {'POTENTIAL (LATENT)' if frozen else '(ACTIVE)'} ─────────────────────────")
    print(f"  Major River Channels   : {n_rivers}  ({valley_type})")
    print(f"  Mean River Length      : {avg_len_km:,} km  [Hack's Law: L = 1.4 × A^0.6]")
    print(f"  Navigable River Length : {nav_km:,} km  {'(at liquid activation)' if frozen else '(active)'}")
    print(f"  Hydrological Connect.  : {connectivity:.2f}  ({'LOW' if connectivity < 0.25 else 'MODERATE' if connectivity < 0.55 else 'HIGH'})")
    print(f"    [Fraction of land within 50 km of navigable water]")

    print(f"\n── 4. ACTIVATION POTENTIAL (LIQUID TRANSITION) ──────────────")
    if frozen:
        print(f"  Equatorial Thaw Thresh : T_surf > {eq_thresh:.1f} K  ({eq_thresh-273.15:.1f} °C)")
        print(f"  Global Liquid Threshold: T_surf > {global_thresh:.1f} K  ({global_thresh-273.15:.1f} °C)")
        print(f"  Meltwater Pulse Volume : {water_eo * EARTH_OCEAN_VOL_KM3:.2e} km³")
        print(f"  Projected Sea Level Rise: +{slr_km:.2f} km")
        print(f"    [Fits within basin depth of {b2_km:.2f} km — no global flooding]"
              if slr_km < b2_km else
              f"    [WARNING: Exceeds basin depth {b2_km:.2f} km — continental flooding likely]")
    else:
        print(f"  Hydrology already in liquid state — no activation required.")

    print(f"\n── WORLD SUMMARY ───────────────────────────────────────────")
    if frozen:
        print(f"  Hydrological State     : Glacially locked — {n_rivers} latent river channels")
        print(f"    beneath {permafrost_m:.0f} m of permafrost, {subglacial_lakes} subglacial lakes active")
        print(f"    deep below the ice. {nav_km:,} km of navigable river potential")
        print(f"    dormant, awaiting a {global_thresh-t_surf_v5:.1f} K warming event.")
    else:
        print(f"  Hydrological State     : Active — {nav_km:,} km of navigable rivers")
        print(f"    connecting {maj_exo} major exorheic basins.")

    print(f"\n  Variable Seven complete. Hydrological skeleton locked.")
    print(f"  Temporary constants still active:")
    print(f"    — Orbital eccentricity (0.00) — deferred")
    print(f"    — O₂/CH₄ fractions (0.0) — deferred to biology variable")
    print(f"  Unresolved dependency: Surface substrate / weathering.")
    print(f"  Ready to receive Variable Eight: Soil & Regolith.")

    # ── VARIABLE EIGHT ────────────────────────────────────────

    print(f"\n══ VARIABLE EIGHT: SOIL & REGOLITH (ABIOTIC SUBSTRATE) ═════")
    print(f"\n  Processing Glacial Grinding & Aeolian Transport...")
    print(f"  Applying Goldich Dissolution & Arrhenius Chemical Weathering...")
    print(f"  Resolving Historic CO₂ Tension...")

    glacial_rate  = compute_glacial_erosion_rate(g2_g, melt_thresh_m)
    chem_rate     = compute_chemical_weathering_rate(t_surf_v5, co2_ppm, frozen=frozen)
    aeolian_idx   = compute_aeolian_rate(pressure_atm, g2_g)

    depths = compute_regolith_depths(
        g2_g, hf2, sa2_km2_v6, f_land_f, t_surf_v5,
        pressure_atm, water_eo, f_ice_f, tectonic_regime(hf2, cmf),
        boundaries["fold_mountains"], boundaries["subduction_trenches"],
        aridity_idx, active_layer_m, phi_h, clustering,
        basin_depth_m=b2_km * 1000.0)

    transport = depths.pop("_transport", {})

    # Basin overflow cascade — replaces isostatic depth cap
    # Need T_in_basin — recompute from transport terms for the call
    _T_in = transport.get("T_in_basin_m3yr", 0)
    overflow = compute_basin_overflow(
        T_in_basin    = _T_in,
        subduction_rate = transport.get("subduction_km3", 0) * 1e9,
        age_yr        = SIMULATION_AGE_GYR_V8 * 1e9,
        A_basin_m2    = sa2_km2_v6 * f_land_f * aridity_idx * 0.60 * 1e6,
        maj_endo      = maj_endo,
        maj_exo       = maj_exo,
        b2_km         = b2_km,
        rift_valleys  = boundaries["rift_valleys"],
        subduction_trenches = boundaries["subduction_trenches"],
        f_land        = f_land_f,
        sa_km2        = sa2_km2_v6,
        clustering    = clustering,
        f_ice         = f_ice_f,
        tectonic_str  = tectonic_regime(hf2, cmf),
        water_eo      = water_eo,
        freeboard_km  = freeboard,
        t_surf        = t_surf_v5,
    )
    # Update basin depth from overflow model (no cap — emerges from cascade)
    depths["Sedimentary Basins (total)"]   = overflow["D_basin_total"]
    depths["Sedimentary Basins (regolith)"] = min(overflow["D_basin_total"], 500.0)

    mean_depth  = compute_mean_regolith_depth(depths, f_land_f, clustering, f_ice_f)
    regolith_ph = compute_regolith_ph(co2_ppm, hotspots, f_land_f)
    nutrients   = compute_nutrients(cmf, hotspots, co2_ppm, t_surf_v5, hf2)
    bri         = compute_biological_readiness(
        depths, regolith_ph, nutrients, t_surf_v5, hotspots, permafrost_m)
    co2_legacy  = co2_tension_legacy(
        co2_ppm, hf2, boundaries["fold_mountains"], boundaries["divergent"])

    print(f"\n── 1. WEATHERING & MINERALOGY PROFILE ──────────────────────")
    print(f"  Dominant Weathering    : {'Mechanical (Glacial Grinding)' if frozen else 'Chemical + Mechanical (Liquid)'}")
    print(f"  Glacial Erosion Rate   : {glacial_rate:.3f} mm/yr")
    print(f"  Chemical Weathering    : {chem_rate:.4f} mm/yr  "
          f"({'SEVERELY DEPRESSED — T=' + str(round(t_surf_v5,1)) + 'K' if frozen else 'ACTIVE'})")
    print(f"    [Arrhenius: r_T = r₀ × exp(-Ea/R × (1/T - 1/T_ref))]")
    print(f"  Aeolian Transport      : {transport.get('T_aeol_km3', 0):.3f} km³/yr")
    print(f"    [Bagnold + L_path from φ_H={phi_h:.0f}° × R_planet × (1+clustering)]")
    print(f"  Glacial Transport      : {transport.get('T_glac_km3', 0):.4f} km³/yr")
    print(f"  Fluvial Transport      : {transport.get('T_fluv_km3', 0):.2f} km³/yr  {'(frozen — zero)' if frozen else ''}")
    print(f"  Subduction Removal     : {transport.get('subduction_km3', 0):.2f} km³/yr  ({boundaries['subduction_trenches']} active trenches)")
    print(f"  Global Mean Regolith pH: {regolith_ph}")
    print(f"  Parent Rock (Cratons)  : Felsic granite — quartz-rich, kaolinite/illite clays")
    print(f"  Parent Rock (Arcs/Oases): Mafic basalt — iron-rich, smectite clays, Ca-buffered")

    print(f"\n── 2. SEDIMENT CASCADE (4-LEVEL SINK HIERARCHY) ────────────")
    print(f"  Basin Fill Time        : {overflow['basin_fill_time_gyr']:.2f} Gyr "
          f"({'basins reached capacity early' if overflow['basin_fill_time_gyr'] < 1.0 else 'basins filled during simulation' if overflow['basin_fill_time_gyr'] < 4.5 else 'basins still accumulating'})")
    if overflow['overflow_volume_km3'] > 0:
        print(f"  Overflow Status        : Basins exceeded capacity — cascade triggered")
        print(f"  Interior Trapping      : {'~80% stranded — ice viscosity + supercontinent distance' if frozen and clustering > 0.7 else '~50% stranded — supercontinent interior' if clustering > 0.7 else 'Moderate trapping'}")
        print(f"  Rift Valley Fill       : {overflow['rift_fill_fraction']*100:.0f}%  "
              f"({'fully buried' if overflow['rift_fill_fraction'] >= 1.0 else 'partially filled'})")
        print(f"  Shelf Sediment Depth   : {overflow['shelf_sediment_depth_m']:.0f} m")
        print(f"  Cascade Complete       : {'YES' if overflow['cascade_complete'] else 'NO — abyssal excess'}")
    else:
        print(f"  Overflow Status        : No overflow — basins still accumulating after 4.5 Gyr")

    print(f"\n── 3. DEPTH & TEXTURE BY TERRAIN CLASS ─────────────────────")
    print(f"  Global Mean Depth      : {mean_depth} m  (highly variable)")
    print(f"  Dominant Texture Class : Silt-Loam (bimodal glacial till)")
    for terrain, depth in depths.items():
        if terrain == "Sedimentary Basins (total)":
            print(f"    {'  → Total basin rock':<28}: {depth:>8.1f} m  (compacted sedimentary rock below 500m)")
        else:
            print(f"    {terrain:<28}: {depth:>8.1f} m")
    if frozen:
        print(f"  Active Layer Dynamics  : Severe frost-heave & solifluction at {active_layer_m:.1f} m")
        print(f"    [Clay minerals expand/contract cyclically — periglacial churning]")

    print(f"\n── 4. ABIOTIC NUTRIENT AVAILABILITY ────────────────────────")
    limiting = min(nutrients, key=nutrients.get)
    for nut, val in nutrients.items():
        bar = "█" * int(val * 20)
        flag = " ← PRIMARY LIMITING NUTRIENT" if nut == limiting else ""
        print(f"  {nut:<12}: {val:.3f}  {bar}{flag}")

    print(f"\n── 5. SEED 1 SPECIAL FEATURES ───────────────────────────────")
    print(f"  Periglacial Flags      : Frost polygons active across exposed land")
    print(f"  CO₂ Tension Legacy     : {co2_legacy}")
    print(f"  Geothermal Oases       : {hotspots} sites")
    print(f"    [Liquid water, elevated temps, active chemical weathering,]")
    print(f"    [abiotic NH₃ synthesis from FeS catalysis at volcanic vents]")

    print(f"\n── BIOLOGICAL LANDING PAD ASSESSMENT ───────────────────────")
    print(f"  Global Mean Regolith   : {mean_depth} m")
    print(f"  Dominant Texture       : Silt-Loam (Glacial Till)")
    print(f"  Mean pH                : {regolith_ph}")
    print(f"  Primary Limiting Nutrient: {limiting} (index {nutrients[limiting]:.3f})")
    print(f"  Geothermal Oases       : {hotspots} sites with liquid water potential")
    print(f"  Biological Readiness   : {bri:.2f} / 1.00  "
          f"({'Hostile' if bri < 0.20 else 'Marginal' if bri < 0.40 else 'Moderate' if bri < 0.65 else 'Favourable'})")

    if bri < 0.20:
        best_site = f"Geothermal oases at the {hotspots} hotspot vents — only sites with liquid water and active chemistry"
    elif f_land_f > 0.5:
        best_site = "Equatorial lowland basins — deepest regolith, closest to moisture"
    else:
        best_site = "Coastal margins — liquid water + regolith depth + nutrient flux"

    print(f"  Most Promising Site    : {best_site}")

    print(f"\n  Variable Eight complete. Abiotic substrate locked.")
    print(f"  All physical prerequisites for biology satisfied:")
    print(f"    ✓ Physical substrate (regolith)")
    print(f"    ✓ Liquid water (subglacial lakes + {hotspots} geothermal oases)")
    print(f"    ✓ Energy source (stellar insolation + geothermal)")
    print(f"    ✓ Inorganic nutrients (P, K, Fe, Ca, Mg available)")
    print(f"    ✓ Atmospheric pressure and retained gases")
    print(f"  Temporary constants still active:")
    print(f"    — Orbital eccentricity (0.00) — deferred")
    print(f"    — O₂/CH₄ fractions (0.0) — replaced by Variable Nine")
    print(f"  Central dramatic question: Can biology warm this world")
    print(f"  by {(275.1 - t_surf_v5):.1f} K and trigger the meltwater pulse?")
    print(f"  Ready to receive Variable Nine: Biology (The Biosphere).")
    print("=" * 62)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MORTALIS World Generation Engine — Variables One through Four"
    )
    parser.add_argument("--seed",      type=int,   default=None, help="Random seed")
    parser.add_argument("--cmf",       type=float, default=None, help="Core Mass Fraction (0.0–0.80)")
    parser.add_argument("--star-mass", type=float, default=None, help="Host star mass in solar masses (0.50–1.30)")
    parser.add_argument("--orbit",     type=float, default=None, help="Orbital distance in AU")
    args = parser.parse_args()
    run(seed=args.seed, cmf_input=args.cmf,
        star_mass_input=args.star_mass, orbital_d_input=args.orbit)
