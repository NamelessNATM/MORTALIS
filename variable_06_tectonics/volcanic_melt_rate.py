# variable_06_tectonics/volcanic_melt_rate.py
#
# FORMULA (stagnant lid):
#   u       = 2*(Nu-1) * k / (rho_mantle * C_p * D) * (T_m - T_eq) / (T_m - P_c/(rho_mean*g))
#   R_melt  = (4*pi*R**2 * u * rho_mantle / M) * (rho_crust * Z_crust * g / |P_f - P_o|)
#
# SOURCE: Kite et al. (2009); decompression melting parameterisation.
#         Thermodynamic physics of decompression melting is universal.
#         Coefficients below are ⚠️ EARTH FALLBACK.
#
# ⚠️ EARTH FALLBACK constants (Flag 56):
#   rho_crust = 2900 kg/m³  (basaltic crust density)
#   Z_crust   = 50000 m     (50 km — stagnant lid analogue, Venus/early Earth)
#   P_f       = 1e9 Pa      (top of melting zone)
#   P_o       = 3e9 Pa      (base of melting zone)
#   C_p       = 1200 J/(kg*K) (Flag 52)
#   k         = 3.5 W/(m*K)   (Flag — Earth silicate)
#
# EARTH CALIBRATION (stagnant lid):
#   R_melt ≈ 1.1e6 kg/s at t = 4.5 Gyr for 1 M_Earth stagnant lid planet.
#   Verified at runtime after ODE integration produces T_m and Nu. Rule 9 applies.
#
# NOTE: This function is only called for rocky and sub-Neptune (solid mantle)
# planets in convecting or sluggish lid regimes. Stagnant lid planets with
# Ra < Ra_c use the conductive heat flux and produce R_melt via conduction path.
# Entry point handles regime routing.

import math

_RHO_CRUST = 2900.0  # ⚠️ EARTH FALLBACK — Flag 56
_Z_CRUST = 50_000.0  # ⚠️ EARTH FALLBACK — Flag 56
_P_F = 1.0e9  # ⚠️ EARTH FALLBACK — Flag 56
_P_O = 3.0e9  # ⚠️ EARTH FALLBACK — Flag 56
_CP = 1200.0  # ⚠️ EARTH FALLBACK — Flag 52
_K = 3.5  # ⚠️ EARTH FALLBACK


def compute_volcanic_melt_rate(
    Nu: float,
    T_m: float,
    T_eq: float,
    P_c: float,
    R: float,
    M: float,
    g: float,
    D: float,
    rho_mantle: float,
    rho_mean: float,
) -> float:
    """
    Compute volcanic melt production rate for a stagnant lid planet.

    Parameters
    ----------
    Nu         : float — Nusselt number
    T_m        : float — mantle temperature [K]
    T_eq       : float — surface temperature proxy [K]
    P_c        : float — central pressure [Pa]
    R          : float — planetary radius [m]
    M          : float — planetary mass [kg]
    g          : float — surface gravity [m/s²]
    D          : float — mantle depth [m]
    rho_mantle : float — mantle density [kg/m³]
    rho_mean   : float — mean bulk density [kg/m³]

    Returns
    -------
    R_melt : float — volcanic melt rate [kg/s]
    """
    denom_T = T_m - P_c / (rho_mean * g)
    if denom_T <= 0.0:
        return 0.0

    u = 2.0 * (Nu - 1.0) * _K / (rho_mantle * _CP * D) * (T_m - T_eq) / denom_T

    melt_fraction = _RHO_CRUST * _Z_CRUST * g / abs(_P_F - _P_O)
    R_melt = (4.0 * math.pi * R**2 * u * rho_mantle / M) * melt_fraction

    return max(0.0, R_melt)
