# MORTALIS World Generation Engine
# Entry point. Orchestrates the variable cascade in order.
# Contains no physics. All physics lives in variable sub-function files.

import sys

from coordinate_system.coordinate_system import run as run_coordinate_system
from map_generator.map_generator import run as run_map_generator
from outputs.manifest import next_version
from variable_01_mass.variable_01_mass import run as run_variable_01
from variable_02_composition.variable_02_composition import run as run_variable_02
from variable_03_stellar.variable_03_stellar import run as run_variable_03


def run(seed: int):
    v01 = run_variable_01(seed)
    v02 = run_variable_02(seed, v01["M_kg"], v01["mu"])
    v03 = run_variable_03(seed)

    active_variables = ["v01", "v02", "v03"]
    version, npz_path, png_path = next_version(seed, active_variables)

    grid, meta = run_coordinate_system(v02, npz_path)
    run_map_generator(grid, meta, png_path)

    return {
        "v01": v01,
        "v02": v02,
        "v03": v03,
        "version": version,
        "npz_path": npz_path,
        "png_path": png_path,
    }


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42

    result = run(seed)
    v01 = result["v01"]
    v02 = result["v02"]
    v03 = result["v03"]

    M_EARTH_KG = 5.972e24
    M_JUP_KG = 1.8982e27
    R_EARTH_M = 6.371e6

    print(f"\n=== MORTALIS World Engine — Seed {seed} ===")
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

    print(f"\n--- Map Output ---")
    print(f"  Version  : v{result['version']:03d}")
    print(f"  NPZ      : {result['npz_path']}")
    print(f"  PNG      : {result['png_path']}")
