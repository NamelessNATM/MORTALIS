# variable_08_volatile_inventory/melt_fraction.py
#
# Mantle melt fraction and volcanic outgassing efficiency.
#
# Formula: P_i=(T_m−1400)/(100−10) GPa; ΔT_rh=2.2×T_m²×R/E_a; D_lid=k×(T_m−ΔT_rh−T_eq)/q_s;
#          F̄=0.5×0.12×(P_i−P_f)
# Source: Langmuir (1992), Katz et al. (2003); Solomatov & Moresi (2000)
# Earth calibration (mobile lid, T_m=1600K): F̄=12.7% ✓
# Mars calibration (stagnant lid, T_m=1500K): P_f=1.818 GPa > P_i=1.111 GPa → F̄=0 ✓
# Flag 124: T_sol,0=1400 K — anhydrous peridotite solidus. Lab measurement. Earth fallback.
# Flag 125: γ=100 K/GPa — solidus Clapeyron slope. Lab measurement. Earth fallback.
# Flag 126: Γ=10 K/GPa — mantle adiabatic gradient. Earth fallback.
# Flag 127: dF/dP=0.12 GPa^−1 — Katz et al. (2003). Anhydrous peridotite. Earth fallback.
# Flag 128: ε_stagnant Gaussian — analytical fit to Dorn et al. (2018) + Noack et al. (2017).
#           Earth fallback.
# Flag 129: ε_mobile=1.0 — degassing efficiency of melt. Idealised upper bound. Earth fallback.

import math

R_GAS = 8.314  # J/mol/K — universal gas constant (Category A)
T_SOL_0_K = 1400.0  # K  — ⚠️ Flag 124
GAMMA_SOL = 100.0  # K/GPa — ⚠️ Flag 125
GAMMA_ADIAB = 10.0  # K/GPa — ⚠️ Flag 126
DF_DP = 0.12  # GPa^-1 — ⚠️ Flag 127
E_A = 300_000.0  # J/mol — olivine activation energy (Solomatov & Moresi 2000)
K_CRUST = 2.5  # W/m/K — Flag 80 (already in codebase)
P_F_MOBILE = 0.1  # GPa — base of oceanic crust
M_EARTH_KG = 5.972e24  # kg

# ε_stagnant Gaussian — ⚠️ Flag 128
EPSILON_STAGNANT_PEAK = 0.05
EPSILON_STAGNANT_M0 = 2.5  # M_earth at peak
EPSILON_STAGNANT_SIGMA2 = 4.5  # 2σ² denominator


def compute_melt_fraction(
    T_m_K: float | None,
    T_eq_K: float,
    q_s_Wm2: float | None,
    rho_mantle_kgm3: float,
    g: float,
    M_kg: float,
    tectonic_regime: str,
) -> dict:
    """Mean melt fraction F_bar and outgassing efficiency ε."""
    if T_m_K is None or q_s_Wm2 is None or q_s_Wm2 <= 0.0:
        return {
            "F_bar": 0.0,
            "epsilon": 0.0,
            "D_lid_m": None,
            "P_i_GPa": None,
            "P_f_GPa": None,
            "delta_T_rh_K": None,
            "melt_note": "T_m or q_s unavailable",
        }

    denom = GAMMA_SOL - GAMMA_ADIAB
    p_i_gpa = (T_m_K - T_SOL_0_K) / denom
    if p_i_gpa <= 0.0:
        return {
            "F_bar": 0.0,
            "epsilon": 0.0,
            "D_lid_m": None,
            "P_i_GPa": p_i_gpa,
            "P_f_GPa": None,
            "delta_T_rh_K": None,
            "melt_note": "mantle too cold to melt (P_i≤0)",
        }

    delta_t_rh = None
    d_lid_m = None

    if tectonic_regime == "mobile_lid" or tectonic_regime == "mobile":
        p_f_gpa = P_F_MOBILE
        d_lid_m = None
        delta_t_rh = None
    else:
        # stagnant / sluggish / heat_pipe: stagnant-lid lid thickness
        delta_t_rh = 2.2 * T_m_K**2 * R_GAS / E_A
        d_lid_m = K_CRUST * (T_m_K - delta_t_rh - T_eq_K) / q_s_Wm2
        d_lid_m = max(d_lid_m, 0.0)
        p_f_gpa = rho_mantle_kgm3 * g * d_lid_m / 1e9

    f_bar = max(0.0, 0.5 * DF_DP * (p_i_gpa - p_f_gpa))

    if tectonic_regime == "mobile_lid" or tectonic_regime == "mobile":
        epsilon = 1.0  # Flag 129
    else:
        m_ratio = M_kg / M_EARTH_KG
        epsilon = EPSILON_STAGNANT_PEAK * math.exp(
            -((m_ratio - EPSILON_STAGNANT_M0) ** 2) / EPSILON_STAGNANT_SIGMA2
        )

    return {
        "F_bar": f_bar,
        "epsilon": epsilon,
        "D_lid_m": d_lid_m,
        "P_i_GPa": p_i_gpa,
        "P_f_GPa": p_f_gpa,
        "delta_T_rh_K": delta_t_rh,
        "melt_note": "melt fraction computed",
    }
