# variable_06_tectonics/mantle_viscosity.py
#
# FORMULA:
#   eta(T_m) = eta_0 * exp(E_a / (R_g * T_m))      [Arrhenius viscosity]
#   theta    = E_a * DeltaT / (R_g * T_m**2)        [Frank-Kamenetskii parameter]
#
# ARRHENIUS CALIBRATION:
#   eta_ref  = 1e21 Pa*s at T_ref = 1600 K (Earth upper mantle reference).
#   eta_0    = eta_ref * exp(-E_a / (R_g * T_ref))
#            = 1e21 * exp(-300000 / (8.314 * 1600))
#            = 1e21 * exp(-22.552)
#            = 1.606e11 Pa*s
#   Verification: eta(1600 K) = 1.606e11 * exp(22.552) = 1e21 Pa*s ✓
#
# NOTE on prior error: The Scaffold 008 implementation placed eta_ref = 1e21 Pa*s
# directly as the Arrhenius pre-exponential. This is incorrect — eta_ref is the
# observed viscosity at T_ref, not the pre-exponential. The corrected eta_0 is
# nine orders of magnitude lower. All prior outputs from mantle_viscosity.py are
# superseded by this correction.
#
# SOURCE: Arrhenius form — universal silicate rheology.
#         E_a, eta_ref, T_ref — V06 Follow-Up D, Question D1.
#
# ⚠️ EARTH FALLBACK — eta_0 = 1.606e11 Pa*s, E_a = 300000 J/mol, T_ref = 1600 K.
# Calibrated to dry Earth peridotite/olivine and post-glacial rebound (Haskell).
# Wet mantles can be orders of magnitude lower. Flag 54 — assumes dry rheology.
#
# ⚠️ EARTH FALLBACK — T_solidus coefficients (Flag 65).
# Simon-Glatzel fit from Fiquet et al. (2010) and Andrault et al. (2011).
# Terrestrial peridotite DAC experiments only.
#
# EARTH CALIBRATION (viscosity):
#   eta(1600 K) = 1e21 Pa*s ✓
#   eta(1650 K) = 5.08e20 Pa*s (slightly below reference — physically correct)
#
# EARTH CALIBRATION (solidus):
#   T_solidus(136 GPa) ≈ 4127 K  (Earth CMB target ~4000–4200 K) ✓
#   T_solidus(37.7 GPa) ≈ 2398 K (0.279 M_Earth CMB) ✓
#   T_solidus(0 GPa)    = 1400 K  (surface solidus) ✓

import math

from constants import R_GAS  # universal gas constant 8.314 J/(mol*K)

# Arrhenius parameters — ⚠️ EARTH FALLBACK dry peridotite. Flag 54.
_E_A = 300_000.0  # activation energy [J/mol]
_T_REF = 1_600.0  # reference temperature [K]
_ETA_REF = 1.0e21  # reference viscosity at T_REF [Pa*s]

# Correct Arrhenius pre-exponential derived from reference pair
_ETA_0 = _ETA_REF * math.exp(-_E_A / (R_GAS * _T_REF))  # ≈ 1.606e11 Pa*s

# Solidus coefficients — ⚠️ EARTH FALLBACK. Flag 65.
_T_SOLIDUS_0 = 1_400.0  # surface solidus [K]
_P_SOLIDUS_SC = 24.0  # pressure scale [GPa]
_P_SOLIDUS_EX = 0.57  # exponent [dimensionless]


def compute_mantle_viscosity(T_m: float) -> float:
    """
    Compute temperature-dependent mantle viscosity via Arrhenius law.

    Parameters
    ----------
    T_m : float — mantle temperature [K]

    Returns
    -------
    eta : float — dynamic viscosity [Pa*s]
    """
    return _ETA_0 * math.exp(_E_A / (R_GAS * T_m))


def compute_frank_kamenetskii(T_m: float, T_eq: float) -> float:
    """
    Compute the Frank-Kamenetskii parameter theta for the Nu-Ra scaling law.

    Parameters
    ----------
    T_m  : float — mantle temperature [K]
    T_eq : float — surface equilibrium temperature [K] (upper boundary proxy)

    Returns
    -------
    theta : float — dimensionless FK parameter
    """
    delta_T = max(T_m - T_eq, 0.0)
    return _E_A * delta_T / (R_GAS * T_m**2)


def compute_solidus(P_cmb_Pa: float) -> float:
    """
    Compute the pressure-dependent silicate solidus temperature.
    Used as a physical ceiling on T_m in the thermal evolution ODE.

    Formula: T_solidus = 1400 * (P_GPa / 24 + 1)^0.57
    Source: Simon-Glatzel fit, Fiquet et al. (2010); Andrault et al. (2011).
    ⚠️ EARTH FALLBACK — Flag 65.

    Parameters
    ----------
    P_cmb_Pa : float — core-mantle boundary pressure [Pa]

    Returns
    -------
    T_solidus : float — silicate solidus at P_cmb [K]
    """
    P_GPa = P_cmb_Pa / 1.0e9
    return _T_SOLIDUS_0 * (P_GPa / _P_SOLIDUS_SC + 1.0) ** _P_SOLIDUS_EX
