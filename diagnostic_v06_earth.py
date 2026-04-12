# diagnostic_v06_earth.py
# Feeds Earth-analog inputs directly into V06, bypassing the mass sampler.
# Confirms Earth calibration targets for T_m, Ra, q_s.

from variable_06_tectonics.variable_06_tectonics import run_variable_06

v01 = {"M_kg": 5.97e24, "mu": 3.986e14}
v02 = {
    "regime": "rocky",
    "R_m": 6.371e6,
    "g_m_s2": 9.807,
    "P_c_Pa": 1.71e11,
    "rho_mean_kg_m3": 5515.0,
    "CMF": 0.325,
}
v03 = {"M_star_kg": 1.989e30, "age_Gyr": 4.5}
v05 = {
    "a_m": 1.496e11,
    "e": 0.0167,
    "T_orb_s": 3.156e7,
    "T_eq_K": 255.0,
    "F_mean_Wm2": 1361.0,
}
v04 = {"atm_class": "secondary_possible"}

result = run_variable_06(v01, v02, v03, v05, v04)

print(f"T_m_K:         {result['T_m_K']:.1f} K      (target: ~1650 K)")
print(f"Ra:            {result['Ra']:.3e}  (target: 1e7–1e8)")
print(f"q_s_total_TW:  {result['q_s_total_TW']:.2f} TW   (target: 47 ± 2 TW)")
print(f"H_rad_W:       {result['H_rad_W']/1e12:.2f} TW   (target: 20–24 TW)")
print(f"R_core_km:     {result['R_core_m']/1e3:.1f} km  (target: ~3480 km)")
print(f"P_cmb_GPa:     {result['P_cmb_Pa']/1e9:.1f} GPa (target: ~123 GPa)")
print(f"t_lock_Gyr:    {result['t_lock_Gyr']:.1f} Gyr  (target: >50 Gyr)")
print(f"tectonic_regime: {result['tectonic_regime']}")
