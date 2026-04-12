# variable_06_tectonics/volcanic_melt_rate.py
#
# FORMULA — absolute volcanic melt production rate [kg/s]:
#
#   u       = 2(Nu-1) × k / (rho_mantle × C_p × D) × (T_m - T_s) / (T_m - T_c)
#   R_melt  = 4π R² × u × rho_mantle × (rho_crust × Z_crust × g / |P_f - P_o|)
#
# SOURCE: Kite, Manga, and Gaidos (2009).
#   Equation 24 (upwelling velocity), Equation 25 (normalized melt rate).
#   The un-normalized absolute form is used here directly: R_melt = A × u × rho × phi.
#   The /M_planet normalization in Eq. 25 is discarded — it converts to yr⁻¹;
#   the un-normalized form gives kg/s directly.
#
# REGIME-DEPENDENT BOUNDARY TEMPERATURE T_c:
#   Mobile lid:   T_c = T_s   → ratio (T_m - T_s)/(T_m - T_c) = 1.0 exactly.
#   Stagnant lid: T_c = T_m - 2.23 × (T_m² / A_0)
#                 where A_0 = E_a / R_g (activation temperature).
#                 Source: Grasset and Parmentier (1998).
#   Source: Kite et al. (2009) Eq. 24 derivation.
#
# ERRORS CORRECTED (Scaffold 009):
#   Error 1 — prior denominator used P_c / (rho_mean × g), which has units
#   of metres, not Kelvin. Subtracting metres from Kelvin is dimensionally
#   invalid. Replaced with the correct thermal boundary temperature T_c.
#   Error 2 — prior R_melt divided by M, producing units of 1/s, not kg/s.
#   Division by M discarded. Un-normalized form produces kg/s directly.
#
# EARTH CALIBRATION (mobile lid, Kite et al. constants):
#   Nu=31.2, T_m=1540 K, T_s=288 K, k=4.18, c=914, rho=3400,
#   D=2.891e6 m, R=6.371e6 m, Z_crust=7000 m (oceanic), P_f=0, P_o=3e9 Pa
#   → u = 2.81e-11 m/s, melt_fraction = 0.0655, R_melt = 3.19e6 kg/s
#   Target: ~3.2e6 kg/s (Kite et al. 2009; confirmed by research session).
#
# CALIBRATION NOTE (our code's constants vs Kite):
#   Using k=3.5 (Flag 67) and C_p=1200 (Flag 52) produces R_melt ≈ 2.03e6 kg/s,
#   ~36% below Kite's target. Discrepancy is entirely from differing Earth
#   fallback constants, not from formula error.
#
# ⚠️ EARTH FALLBACK constants (all flags carried forward from prior implementation):
#   rho_crust = 2900 kg/m³  — Flag 56
#   Z_crust   = 50000 m     — Flag 56 (stagnant lid analogue; 7000 m for mobile lid)
#   P_f       = 1e9 Pa      — Flag 56
#   P_o       = 3e9 Pa      — Flag 56
#   C_p       = 1200 J/kg/K — Flag 52
#   k         = 3.5 W/m/K  — Flag 67 (Kite et al. use 4.18)
#
# ⚠️ Flag 68: Kite (2009) parameterization invalid above ~3 M_Earth.
#   Dorn et al. (2018), Noack et al. (2017): pressure suppression nonlinearly
#   truncates melting column. R_melt overestimated for massive super-Earths.
#   Flag for review if M_planet > 3 M_Earth and R_melt_kgs used as output.

import math

# E_A must match the value in mantle_viscosity.py (Flag 54 — Earth-calibrated)
_E_A = 300_000.0       # J/mol — activation energy; ⚠️ EARTH FALLBACK — Flag 54
_R_GAS = 8.314         # J/(mol·K) — universal gas constant (Category A)
_A_0 = _E_A / _R_GAS  # K — activation temperature; ⚠️ EARTH FALLBACK — Flag 69

_RHO_CRUST = 2900.0    # kg/m³ — ⚠️ EARTH FALLBACK — Flag 56
_Z_CRUST = 50_000.0    # m     — ⚠️ EARTH FALLBACK — Flag 56
_P_F = 1.0e9           # Pa    — ⚠️ EARTH FALLBACK — Flag 56
_P_O = 3.0e9           # Pa    — ⚠️ EARTH FALLBACK — Flag 56
_CP = 1200.0           # J/(kg·K) — ⚠️ EARTH FALLBACK — Flag 52
_K = 3.5               # W/(m·K)  — ⚠️ EARTH FALLBACK — Flag 67


def compute_volcanic_melt_rate(
    Nu: float,
    T_m: float,
    T_eq: float,
    R: float,
    g: float,
    D: float,
    rho_mantle: float,
    tectonic_regime: str,
) -> float:
    """
    Compute volcanic melt production rate [kg/s] via Kite et al. (2009)
    decompression melting parameterisation (un-normalized absolute form).

    Parameters
    ----------
    Nu             : float — Nusselt number (dimensionless)
    T_m            : float — mantle temperature [K]
    T_eq           : float — equilibrium/surface temperature proxy [K]
    R              : float — planetary radius [m]
    g              : float — surface gravity [m/s²]
    D              : float — mantle depth (R − R_core) [m]
    rho_mantle     : float — mantle bulk density [kg/m³]
    tectonic_regime: str   — 'mobile_lid', 'stagnant_lid', or 'sluggish_lid'

    Returns
    -------
    R_melt : float — volcanic melt production rate [kg/s]
    """
    if Nu <= 1.0:
        return 0.0

    # Thermal diffusivity [m²/s]
    kappa = _K / (rho_mantle * _CP)

    # Regime-dependent boundary temperature and velocity ratio
    if tectonic_regime == "mobile_lid":
        # T_c = T_s; ratio (T_m - T_s)/(T_m - T_c) = 1 exactly
        u_ratio = 1.0
    else:
        # Stagnant lid and sluggish lid: Grasset & Parmentier (1998) scaling
        # T_c = T_m - 2.23 * T_m² / A_0
        # denom = T_m - T_c = 2.23 * T_m² / A_0
        denom_T = 2.23 * (T_m ** 2) / _A_0
        if denom_T <= 0.0:
            return 0.0
        numer_T = T_m - T_eq
        if numer_T <= 0.0:
            return 0.0
        u_ratio = numer_T / denom_T

    # Upwelling velocity [m/s]
    u = 2.0 * (Nu - 1.0) * (kappa / D) * u_ratio

    # Mean melt fraction (dimensionless) — ρ_crust × Z_crust × g / |P_f - P_o|
    delta_P = abs(_P_F - _P_O)
    if delta_P == 0.0:
        return 0.0
    melt_fraction = (_RHO_CRUST * _Z_CRUST * g) / delta_P

    # Absolute melt rate [kg/s] — un-normalized; no division by M
    surface_area = 4.0 * math.pi * R ** 2
    R_melt = surface_area * u * rho_mantle * melt_fraction

    return max(0.0, R_melt)
