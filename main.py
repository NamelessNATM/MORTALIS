# MORTALIS World Generation Engine
# Entry point. Orchestrates the variable cascade in order.
# Contains no physics. All physics lives in variable sub-function files.

from variable_01_mass.variable_01_mass import run as run_variable_01
from variable_02_composition.variable_02_composition import run as run_variable_02


def run(seed: int):
    v01 = run_variable_01(seed)
    v02 = run_variable_02(seed, v01["M_kg"], v01["mu"])
    return {"v01": v01, "v02": v02}


if __name__ == "__main__":
    import sys
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 42

    result = run(seed)
    v01 = result["v01"]
    v02 = result["v02"]

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
    if v02['R_m'] is not None:
        print(f"  R        : {v02['R_m']:.4e} m")
        print(f"  R_earth  : {v02['R_m'] / R_EARTH_M:.4f}")
        print(f"  rho_mean : {v02['rho_mean_kg_m3']:.2f} kg/m^3")
        print(f"  g        : {v02['g_m_s2']:.4f} m/s^2")
        print(f"  v_e      : {v02['v_e_m_s']:.2f} m/s")
        print(f"  P_c      : {v02['P_c_Pa']:.4e} Pa")
    else:
        print("  R and derived quantities: None (brown dwarf — outside simulation domain)")
