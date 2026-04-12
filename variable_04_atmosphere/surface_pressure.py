# variable_04_atmosphere/surface_pressure.py
#
# PURPOSE: Compute surface pressure P_s from atmospheric column mass M_atm.
#
# Formula: P_s = M_atm * g / (4 * pi * R²)
#
# Derivation: Hydrostatic equilibrium dP/dz = -rho*g integrated from top of
# atmosphere to surface, assuming thin atmosphere (H << R) so g is constant.
# Source: standard atmospheric physics; confirmed across Earth, Mars, Venus,
# Titan — universally applicable in thin-atmosphere limit.
#
# Corrections documented but not applied:
# - Thick atmospheres (sub-Neptunes): gravity varies with altitude; P_s is
#   overestimated by thin-atmosphere formula. No closed-form correction.
#   Deferred. (Flag 43 adjacent)
# - Tidal locking atmospheric collapse: deferred to Variable 06. (Flag 44)
#
# Rocky planet M_atm: BLOCKED. X_vol not in cascade (Flag 40).
# Gas giant / sub-Neptune: no solid surface; P_s undefined. Not computed.
#
# Earth calibration (back-calculation):
#   P_s = 101,325 Pa, g = 9.807 m/s², R = 6.371e6 m
#   → M_atm = 5.27e18 kg (known 5.15e18 kg; 2.3% error ✓)

import math

PI = math.pi


def compute_surface_pressure(M_atm_kg: float,
                              g_m_s2: float,
                              R_m: float) -> float:
    """
    Surface pressure P_s [Pa].

    Parameters
    ----------
    M_atm_kg : atmospheric column mass [kg]
    g_m_s2   : surface gravity [m/s²] from Variable 02
    R_m      : planetary radius [m] from Variable 02

    Returns
    -------
    P_s [Pa]
    """
    return (M_atm_kg * g_m_s2) / (4.0 * PI * R_m ** 2)


def get_surface_pressure(atm_class: str,
                          g_m_s2: float,
                          R_m: float) -> float | None:
    """
    Return surface pressure where computable; None where blocked.

    Rocky planets: M_atm blocked (Flag 40) → returns None.
    Gas giant / sub-Neptune: no solid surface → returns None.
    Dwarf / no atmosphere: returns 0.0.

    Parameters
    ----------
    atm_class : atmospheric class string from regime_classifier.py
    g_m_s2    : surface gravity [m/s²] from Variable 02
    R_m       : planetary radius [m] from Variable 02

    Returns
    -------
    P_s [Pa] or None
    """
    if atm_class == "none":
        return 0.0
    if atm_class in ("primary_retained", "primary_stripped"):
        return None  # no solid surface
    if atm_class == "secondary_possible":
        return None  # Flag 40: M_atm blocked; X_vol not in cascade
    return None
