# variable_06_tectonics/mantle_temperature.py
#
# PURPOSE: Integrate the stagnant lid thermal evolution ODE to obtain T_m(age).
#
# ODE:
#   M_m * C_p * dT_m/dt = H_rad(t) - 4*pi*R**2 * q_s(T_m, t)
#
# INITIAL CONDITION:
#   T_m(0) = 1700 K  [canonical cool-start value from stagnant lid literature]
#
# SOLIDUS CEILING:
#   If T_m >= T_solidus(P_cmb), the Arrhenius solid-state creep model is invalid.
#   Partial melting begins; liquid-state convection takes over. The ODE is halted
#   and T_m is set to T_solidus. The regime is flagged as 'magma_ocean_or_heat_pipe'.
#   Source: V06 Follow-Up D, Question D3b; D3c.
#
# SOURCE:
#   ODE structure: V06 Follow-Up B, Question B1.
#   T_m(0): V06 Follow-Up C, Question C2 — canonical cool-start.
#   Solidus: V06 Follow-Up D, Question D3c — Simon-Glatzel fit.
#
# ⚠️ EARTH FALLBACK — T_m(0) = 1700 K. Cannot be derived from cascade inputs;
# requires accretion timescale tau absent from cascade. Flag 57.
#
# ⚠️ EARTH FALLBACK — C_p = 1200 J/(kg*K). Earth silicate calibration. Flag 52.
#
# ⚠️ SIMPLIFICATION — Q_core = 0. Core basal heat flux neglected. Flag 53.
#
# EARTH CALIBRATION:
#   T_m(4.5 Gyr) ≈ 1650 K (target). Verified at runtime per Rule 9.

import math

from variable_06_tectonics.mantle_viscosity import compute_solidus
from variable_06_tectonics.radiogenic_heating import compute_radiogenic_heating

# ⚠️ EARTH FALLBACK — Flag 52
_CP = 1200.0  # specific heat capacity [J/(kg*K)]
_TM0 = 1700.0  # initial mantle temperature [K] — ⚠️ Flag 57
_N_STEPS = 1000  # integration steps over full system age


def integrate_mantle_temperature(
    M: float,
    CMF: float,
    R: float,
    T_eq: float,
    D: float,
    P_cmb_Pa: float,
    q_s_func,
    age_Gyr: float,
) -> dict:
    """
    Integrate the thermal evolution ODE forward from t=0 to t=age_Gyr.

    Uses forward Euler with _N_STEPS uniform steps. Applies a solidus ceiling:
    if T_m reaches T_solidus(P_cmb), integration halts and regime is flagged.

    Parameters
    ----------
    M          : float   — planetary mass [kg]
    CMF        : float   — core mass fraction [dimensionless]
    R          : float   — planetary radius [m]
    T_eq       : float   — equilibrium surface temperature [K]
    D          : float   — mantle depth [m]
    P_cmb_Pa   : float   — core-mantle boundary pressure [Pa]
    q_s_func   : callable — (T_m, T_eq, D) -> (q_s_Wm2, Nu)
    age_Gyr    : float   — system age [Gyr]

    Returns
    -------
    dict with keys:
        T_m_K           : float — present mantle temperature [K]
        solidus_K       : float — solidus at P_cmb [K]
        solidus_reached : bool  — True if ODE hit the solidus ceiling
        T_m_history     : list  — (t_Gyr, T_m_K) pairs at each step
    """
    M_mantle = M * (1.0 - CMF)
    dt_Gyr = age_Gyr / _N_STEPS
    dt_s = dt_Gyr * 3.15576e16
    T_solidus = compute_solidus(P_cmb_Pa)

    T_m = _TM0
    history = [(0.0, T_m)]
    solidus_reached = False

    for step in range(_N_STEPS):
        t_Gyr = step * dt_Gyr

        H_rad = compute_radiogenic_heating(M_mantle, t_Gyr)
        q_s, _Nu = q_s_func(T_m, T_eq, D)
        q_total_W = 4.0 * math.pi * R**2 * q_s

        dT = (H_rad - q_total_W) / (M_mantle * _CP) * dt_s
        T_m = max(T_eq, T_m + dT)

        # Solidus ceiling — halt if mantle reaches melting point
        if T_m >= T_solidus:
            T_m = T_solidus
            solidus_reached = True
            history.append((t_Gyr + dt_Gyr, T_m))
            break

        history.append((t_Gyr + dt_Gyr, T_m))

    return {
        "T_m_K": T_m,
        "solidus_K": T_solidus,
        "solidus_reached": solidus_reached,
        "T_m_history": history,
    }
