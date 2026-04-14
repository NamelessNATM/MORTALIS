# variable_08_volatile_inventory/nebular_ingassing.py
#
# Primordial nebular hydrogen ingassing into a magma ocean.
#
# Formula: t_disk=5×(M_star/M_☉)^−0.5 Myr; f_env=1.06e-5×(M/M_⊕)³×t_disk;
#          P_env=f_env×M×g/(4πR²); ΔX_H=0.419×(P_env/1e5) ppm
# Source: Ikoma & Genda (2006), Ikoma & Hori (2012); Mamajek (2009), Ribas et al. (2015)
# Earth calibration: t_disk=5 Myr, f_env=5.30e-5, P_env=60.87 bar, ΔX_H=25.5 ppm, ΔX_H2O=228 ppm
# Mars calibration: ΔX_H2O=0.04 ppm (negligible — correct scaling behaviour)
# Flag 118: k_H = 0.419 ppm/bar — Henry's Law for H2 in peridotitic melt. Lab measurement. Earth fallback.
# Flag 119: f_env coefficient 1.06e-5 — Ikoma & Genda (2006). Solar-analog calibration. Earth fallback.
# Flag 120: t_disk = 5×(M_star/M_☉)^−0.5 Myr — Mamajek (2009), Ribas et al. (2015).
#           Multi-stellar empirical fit. Model applicability limit at extreme stellar masses.
# Flag 131: FeO supply treated as non-limiting. 8 wt% FeO assumed. FeO content not a cascade variable.
#           Earth fallback.
# Flag 132: Equilibrium dissolution assumed. Convective mixing timescale (days) << disk lifetime (Myr).
#           Model applicability limit if magma ocean solidifies before disk dispersal.

import math

M_SUN_KG = 1.989e30
M_EARTH_KG = 5.972e24
K_H_PPM_BAR = 0.419  # ⚠️ Flag 118
F_ENV_COEFF = 1.06e-5  # ⚠️ Flag 119
T_DISK_SOLAR_MYR = 5.0  # Myr at 1 M_sun — Flag 120
T_DISK_EXPONENT = -0.5  # stellar mass scaling — Flag 120
MYR_TO_S = 3.154e13  # s/Myr (unused in ppm path; kept for documentation)
H2O_OVER_H = 18.015 / 2.016  # molar mass ratio


def compute_nebular_ingassing(
    M_kg: float, R_m: float, g: float, M_star_kg: float
) -> dict:
    """Nebular envelope mass fraction, surface pressure, and dissolved H / H2O (ppm)."""
    t_disk_myr = T_DISK_SOLAR_MYR * (M_star_kg / M_SUN_KG) ** T_DISK_EXPONENT
    f_env = F_ENV_COEFF * (M_kg / M_EARTH_KG) ** 3 * t_disk_myr
    p_env_pa = f_env * M_kg * g / (4.0 * math.pi * R_m**2)
    p_env_bar = p_env_pa / 1e5
    delta_x_h_ppm = K_H_PPM_BAR * p_env_bar
    delta_x_h2o_ppm = delta_x_h_ppm * H2O_OVER_H
    return {
        "delta_X_H_ppm": delta_x_h_ppm,
        "delta_X_H2O_ppm": delta_x_h2o_ppm,
        "f_env": f_env,
        "P_env_bar": p_env_bar,
        "t_disk_Myr": t_disk_myr,
    }
