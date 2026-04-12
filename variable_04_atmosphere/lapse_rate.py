# variable_04_atmosphere/lapse_rate.py
#
# PURPOSE: Compute dry adiabatic lapse rate Gamma_d = g / c_p.
#
# Derivation: First Law of Thermodynamics for an adiabatic process
# (c_p dT = v dP) combined with hydrostatic equilibrium (dP = -rho*g*dz).
# Cancelling and rearranging: dT/dz = -g/c_p. Universal physics.
# Source: standard atmospheric thermodynamics.
#
# c_p values per regime:
#   H₂/He (gas giant, sub-Neptune): c_p ~ 12,000 J/(kg·K) for solar mix.
#     Source: confirmed across Jupiter (Galileo probe) and Saturn.
#   N₂ (rocky): c_p ~ 1,040 J/(kg·K). Universal thermodynamic property.
#   CO₂ (rocky): c_p ~ 840 J/(kg·K). Universal thermodynamic property.
#   Earth air (N₂/O₂ mix): c_p ~ 1,004 J/(kg·K).
#
# Earth calibration: g = 9.807, c_p = 1,004 → Gamma_d = 9.77 K/km ✓
# Jupiter calibration: g = 24.79, c_p = 12,000 → Gamma_d = 2.07 K/km ✓
#
# ⚠️ Flag 28: c_p for rocky planet atmospheres is composition-dependent.
# N₂ and CO₂ values used as bounding cases. True c_p requires volatile
# inventory not currently in cascade.

# c_p values [J/(kg·K)] — confirmed thermodynamic properties
C_P_H2_HE  = 12_000.0   # solar mix H₂/He — Jupiter/Saturn confirmed
C_P_N2     =  1_040.0   # pure N₂ — universal
C_P_CO2    =    840.0   # pure CO₂ — universal
C_P_EARTH  =  1_004.0   # N₂/O₂ Earth mix — used as rocky default


def compute_lapse_rate(g_m_s2: float, composition: str) -> float:
    """
    Dry adiabatic lapse rate Gamma_d [K/m].

    Parameters
    ----------
    g_m_s2      : surface gravity [m/s²] from Variable 02
    composition : composition string from regime_classifier.py

    Returns
    -------
    Gamma_d [K/m]
    """
    if composition == "H2_He":
        c_p = C_P_H2_HE
    elif composition == "N2_CO2_unknown":
        c_p = C_P_EARTH  # Flag 28: Earth-mix default; true c_p composition-dependent
    else:
        return 0.0  # no atmosphere

    return g_m_s2 / c_p
