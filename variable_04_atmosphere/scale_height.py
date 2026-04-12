# variable_04_atmosphere/scale_height.py
#
# PURPOSE: Compute atmospheric scale height H = k_B * T / (m * g).
#
# Derivation: Ideal Gas Law (P = rho*k_B*T/m) combined with hydrostatic
# equilibrium, assuming an isothermal atmosphere. Exponential pressure
# profile P(z) = P_s * exp(-z/H) follows directly.
# Source: standard atmospheric physics; confirmed across Earth, Mars,
# Venus, Titan, Jupiter — universal.
#
# Temperature used: T_eq from Variable 05. This gives the scale height
# representative of the upper/emission atmosphere. True surface scale
# height requires greenhouse correction via tau_IR (Flag 43).
#
# Mean molecular mass per composition class:
#   H₂/He solar mix: mu = 0.0023 kg/mol (Jupiter/Saturn confirmed)
#   N₂/CO₂ rocky:    mu = 0.029–0.044 kg/mol (Flag 28)
#   Earth-like:       mu = 0.029 kg/mol
#
# Earth calibration:
#   mu = 0.029 kg/mol, g = 9.807 m/s², T = 288 K
#   H = (8.314 * 288) / (0.029 * 9.807) = 8,419 m
#   Known ~8,500 m ✓
#
# ⚠️ Flag 43: tau_IR greenhouse correction not applied. T_eq used as
# temperature approximation. Surface scale height is underestimated for
# planets with significant greenhouse warming.

# Fundamental physical constant (Rule 1 Category A)
R_STAR = 8.314  # J/(mol·K) — universal gas constant

# Mean molar masses [kg/mol]
MU_H2_HE  = 0.0023  # solar mix — Jupiter/Saturn confirmed
MU_EARTH  = 0.0290  # N₂/O₂ Earth mix
MU_CO2    = 0.0440  # CO₂-dominated (Mars/Venus)


def compute_scale_height(T_eq_K: float,
                          g_m_s2: float,
                          composition: str) -> float | None:
    """
    Atmospheric scale height H [m].

    Parameters
    ----------
    T_eq_K      : equilibrium temperature [K] from Variable 05
    g_m_s2      : surface gravity [m/s²] from Variable 02
    composition : composition string from regime_classifier.py

    Returns
    -------
    H [m] or None if no atmosphere
    """
    if composition == "H2_He":
        mu = MU_H2_HE
    elif composition == "N2_CO2_unknown":
        mu = MU_EARTH   # Flag 28: default; true mu composition-dependent
    elif composition == "none" or composition == "trace":
        return None
    else:
        return None

    if g_m_s2 <= 0.0:
        return None

    return (R_STAR * T_eq_K) / (mu * g_m_s2)
