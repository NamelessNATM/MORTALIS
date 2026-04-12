# MORTALIS World Generation Engine
# Entry point. Orchestrates the variable cascade in order.
# Contains no physics. All physics lives in variable sub-function files.

from world_config.world_config import build_config
from coordinate_system.coordinate_system import run as run_coordinate_system
from map_generator.map_generator import run as run_map_generator
from outputs.manifest import next_version
from variable_01_mass.variable_01_mass import run as run_variable_01
from variable_02_composition.variable_02_composition import run as run_variable_02
from variable_03_stellar.variable_03_stellar import run as run_variable_03
from variable_05_kinematics.variable_05_kinematics import run as run_variable_05
from variable_05_kinematics.bond_albedo import compute_pass2_albedo
from variable_04_atmosphere import variable_04_atmosphere
from variable_06_tectonics.variable_06_tectonics import run_variable_06


def run(seed: int, config: dict):
    v01 = run_variable_01(seed, regime=config['regime'])
    v02 = run_variable_02(seed, v01["M_kg"], v01["mu"])

    active_variables = ["v01", "v02", "v03", "v05", "v04", "v06"]
    version, npz_path, png_path = next_version(seed, active_variables)

    grid, meta = run_coordinate_system(v02, npz_path)

    v03 = run_variable_03(seed, stability=config.get('stability'))
    v05 = run_variable_05(seed, v01, v02, v03)
    v04 = variable_04_atmosphere.run(seed, v01, v02, v03, v05)

    # Bond albedo Pass 2 — post-atmospheric refinement (Flag 38)
    A_B, T_eq_final_K = compute_pass2_albedo(
        A_proxy=v05["albedo_proxy"],
        atm_class=v04["atm_class"],
        composition=v04["composition"],
        F_mean_W_m2=v05["F_mean_W_m2"],
        T_eff_K=v03["T_eff_K"],
        regime=v02["regime"],
    )
    v05["albedo_final"] = A_B
    v05["T_eq_K"] = T_eq_final_K

    v06 = run_variable_06(v01, v02, v03, v05, v04)

    run_map_generator(grid, meta, png_path)

    return {
        "v01": v01,
        "v02": v02,
        "v03": v03,
        "v05": v05,
        "v04": v04,
        "v06": v06,
        "version": version,
        "npz_path": npz_path,
        "png_path": png_path,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='MORTALIS World Generation Engine')
    parser.add_argument('seed', type=int, nargs='?', default=None,
                        help='Integer seed. If omitted, a random seed is generated.')
    parser.add_argument('--world-type', type=str, default=None,
                        dest='world_type',
                        help='World type: rocky, sub_neptune, gas_giant, dwarf. '
                             'Default: unrestricted galactic draw.')
    args = parser.parse_args()

    import random as _random
    seed = args.seed if args.seed is not None else _random.randint(0, 2**31 - 1)
    world_type_arg = args.world_type

    config = build_config(world_type=world_type_arg)

    result = run(seed, config)
    v01 = result["v01"]
    v02 = result["v02"]
    v03 = result["v03"]
    v05 = result["v05"]
    v04 = result["v04"]
    v06 = result["v06"]

    M_EARTH_KG = 5.972e24
    M_JUP_KG = 1.8982e27
    R_EARTH_M = 6.371e6

    print(f"\n=== MORTALIS World Engine — Seed {seed} ===")
    print(f"\n--- World Config ---")
    print(f"  world_type : {config['world_type'] or 'unrestricted (galactic draw)'}")
    print(f"\n--- Variable 01: Mass ---")
    print(f"  M        : {v01['M_kg']:.4e} kg")
    print(f"  M_earth  : {v01['M_kg'] / M_EARTH_KG:.4f}")
    print(f"  M_jupiter: {v01['M_kg'] / M_JUP_KG:.4f}")
    print(f"  mu       : {v01['mu']:.4e} m^3/s^2")

    print(f"\n--- Variable 02: Composition & Radius ---")
    print(f"  Regime   : {v02['regime']}")
    if v02["R_m"] is not None:
        print(f"  R        : {v02['R_m']:.4e} m")
        print(f"  R_earth  : {v02['R_m'] / R_EARTH_M:.4f}")
        print(f"  rho_mean : {v02['rho_mean_kg_m3']:.2f} kg/m^3")
        print(f"  g        : {v02['g_m_s2']:.4f} m/s^2")
        print(f"  v_e      : {v02['v_e_m_s']:.2f} m/s")
        print(f"  P_c      : {v02['P_c_Pa']:.4e} Pa")

    print(f"\n--- Variable 03: Stellar ---")
    print(f"  M_star        : {v03['M_star_solar']:.6f} M_sun ({v03['M_star_kg']:.4e} kg)")
    print(f"  stability     : {v03['stability']}")
    print(f"  stable        : {v03['stable']}")
    print(f"  age_Gyr       : {v03['age_Gyr']:.6f} Gyr")
    print(f"  tau_frac      : {v03['tau_frac']:.6f}")
    print(f"  L_star        : {v03['L_star_solar']:.6f} L_sun ({v03['L_star_W']:.4e} W)")
    print(f"  R_star        : {v03['R_star_solar']:.6f} R_sun ({v03['R_star_m']:.4e} m)")
    if v03["log_g"] is None:
        print(f"  log_g         : — (cgs)")
    else:
        print(f"  log_g         : {v03['log_g']:.4f} (cgs dex)")
    print(f"  T_eff         : {v03['T_eff_K']:.2f} K")
    print(f"  t_MS          : {v03['t_MS_Gyr']:.6f} Gyr")
    print(f"  L_XUV/L       : {v03['L_XUV_fraction']:.4e}")
    print(f"  L_XUV         : {v03['L_XUV_W']:.4e} W")

    AU_M = 1.496e11

    print(f"\n--- Variable 05: Kinematics ---")
    print(f"  a            : {v05['a_m']:.4e} m ({v05['a_m']/AU_M:.4f} AU)")
    print(f"  e            : {v05['e']:.6f}")
    print(f"  obliquity    : {v05['obliquity_deg']:.2f} deg")
    print(f"  T_orb        : {v05['T_orb_s']:.4e} s ({v05['T_orb_s']/86400:.2f} days)")
    print(f"  <F>          : {v05['F_mean_W_m2']:.4e} W/m^2")
    print(f"  F_XUV        : {v05['F_XUV_W_m2']:.4e} W/m^2")
    print(f"  albedo_proxy : {v05['albedo_proxy']:.4f}  (Pass 1)")
    print(f"  T_eq^(0)     : {v05['T_eq_proxy_K']:.2f} K")
    print(f"  albedo_final : {v05['albedo_final']:.4f}  (Pass 2)")
    print(f"  T_eq         : {v05['T_eq_K']:.2f} K")
    print(f"  R_H          : {v05['R_H_m']:.4e} m")
    print(f"  M_dot        : {v05['M_dot_kg_s']:.4e} kg/s")
    print(f"  a_Roche      : {v05['a_roche_m']:.4e} m ({v05['a_roche_m']/AU_M:.6f} AU)")
    print(f"  a_max        : {v05['a_max_m']:.4e} m ({v05['a_max_m']/AU_M:.2f} AU)")

    print(f"\n--- Variable 04: Atmosphere ---")
    if v04["T_exo_K"] is None:
        print(f"  T_exo        : — (K)")
    else:
        print(f"  T_exo        : {v04['T_exo_K']:.2f} K")
    print(f"  atm_class    : {v04['atm_class']}")
    print(f"  composition  : {v04['composition']}")
    if v04["P_s_Pa"] is None:
        print(f"  P_s          : — (Pa)")
    else:
        print(f"  P_s          : {v04['P_s_Pa']:.4e} Pa")
    print(f"  Gamma_d      : {v04['gamma_d_K_m']:.4e} K/m")
    if v04["H_m"] is None:
        print(f"  H            : — (m)")
    else:
        print(f"  H            : {v04['H_m']:.4e} m")
    print(f"  notes        : {v04['notes']}")

    print("\n--- Variable 06: Tectonics ---")
    print(f"  Note:            {v06['tectonic_note']}")
    print(f"  Tectonic regime: {v06['tectonic_regime']}")
    if v06.get("solidus_K") is not None:
        print(f"  Solidus (P_cmb): {v06['solidus_K']:.1f} K")
    if v06.get("solidus_reached") is not None:
        print(f"  Solidus reached: {v06['solidus_reached']}")
    if v06["E_acc_J"] is not None:
        print(f"  E_acc:           {v06['E_acc_J']:.3e} J")
    else:
        print("  E_acc:           None")
    if v06["R_core_m"] is not None:
        print(f"  R_core:          {v06['R_core_m']/1e3:.1f} km")
    else:
        print("  R_core:          None")
    if v06["P_cmb_Pa"] is not None:
        print(f"  P_cmb:           {v06['P_cmb_Pa']/1e9:.1f} GPa")
    else:
        print("  P_cmb:           None")
    if v06["H_rad_W"] is not None:
        print(f"  H_rad:           {v06['H_rad_W']/1e12:.2f} TW")
    else:
        print("  H_rad:           None")
    if v06["T_m_K"] is not None:
        print(f"  T_m:             {v06['T_m_K']:.1f} K")
    else:
        print("  T_m:             None")
    if v06["Ra"] is not None:
        print(f"  Ra:              {v06['Ra']:.3e}")
    else:
        print("  Ra:              None")
    if v06["q_s_total_TW"] is not None:
        print(f"  q_s total:       {v06['q_s_total_TW']:.2f} TW")
    else:
        print("  q_s total:       None")
    if v06["t_lock_Gyr"] is not None:
        print(f"  t_lock:          {v06['t_lock_Gyr']:.2f} Gyr")
    else:
        print("  t_lock:          None")
    print(f"  is_locked:       {v06['is_locked']}")
    if v06["P_tidal_W"] is not None:
        print(f"  P_tidal:         {v06['P_tidal_W']:.3e} W")
    else:
        print("  P_tidal:         None")
    if v06["R_melt_kgs"] is not None:
        print(f"  R_melt:          {v06['R_melt_kgs']:.3e} kg/s")
    else:
        print("  R_melt:          None")
    print(f"  Speciation:      {v06['speciation']}")
    print(f"  Outgassed mass:  {v06['outgassed_mass']}")

    print(f"\n--- Map Output ---")
    print(f"  Version  : v{result['version']:03d}")
    print(f"  NPZ      : {result['npz_path']}")
    print(f"  PNG      : {result['png_path']}")
