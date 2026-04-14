# variable_08_volatile_inventory/variable_08_volatile_inventory.py
#
# Entry point for Variable 08: Volatile Inventory.
# Orchestrates all sub-functions. Contains no physics directly.
#
# REGIME ROUTING:
#   rocky        → full V08 treatment (snow lines → elemental → partitioning →
#                  late veneer → ingassing → fO2 → speciation → melt → outgas → M_atm)
#   sub_neptune  → full V08 treatment if atm_class != primary_retained;
#                  giant composition model if primary_retained
#   gas_giant    → giant composition model only
#   dwarf        → snow lines + elemental partitioning + core partitioning only;
#                  no late veneer, no outgassing integral, no M_atm
#   brown_dwarf  → null output
#
# CASCADE ORDER: v01 → v02 → v03 → v05 → v04 → v06 → v08 → v07
#
# Resolves: Flag 29 (fO2 now computed), Flag 40 (X_vol now computed),
#           Flag 6 (speciation now produced — partial resolution)

from variable_08_volatile_inventory.atmospheric_mass import compute_atmospheric_mass
from variable_08_volatile_inventory.bulk_volatile_fraction import X_DRY, compute_bulk_volatile_fraction
from variable_08_volatile_inventory.core_mantle_partitioning import compute_core_partitioning
from variable_08_volatile_inventory.elemental_partitioning import compute_elemental_bulk
from variable_08_volatile_inventory.equilibrium_speciation import compute_outgassing_speciation
from variable_08_volatile_inventory.giant_planet_composition import compute_giant_composition
from variable_08_volatile_inventory.late_veneer import compute_late_veneer
from variable_08_volatile_inventory.melt_fraction import compute_melt_fraction
from variable_08_volatile_inventory.nebular_ingassing import compute_nebular_ingassing
from variable_08_volatile_inventory.outgassing_integral import compute_outgassing
from variable_08_volatile_inventory.oxygen_fugacity import compute_oxygen_fugacity
from variable_08_volatile_inventory.snow_lines import compute_snow_lines


def _null_output(note: str) -> dict:
    return {
        "volatile_note": note,
        "X_vol": None,
        "delta_IW": None,
        "F_bar": None,
        "epsilon": None,
        "speciation": None,
        "M_atm_kg": None,
        "P_s_Pa": None,
        "M_ocean_kg": None,
        "X_mantle_H2O_ppm": None,
        "outgassed_mass": "Blocked — " + note,
    }


def _giant_assembly(seed: int, v01: dict, v02: dict) -> dict:
    _ = seed
    g = compute_giant_composition(v01["M_kg"], v02["regime"])
    if not g:
        return _null_output("giant composition unavailable")
    sp = g.get("speciation")
    base = {
        "volatile_note": (
            "gas-rich envelope — simplified H2/He speciation; trace volatiles deferred"
        ),
        "X_vol": None,
        "snow_lines": None,
        "X_bulk_H_ppm": None,
        "X_bulk_C_ppm": None,
        "X_bulk_N_ppm": None,
        "X_bulk_S_ppm": None,
        "X_mantle_H_ppm": None,
        "X_mantle_C_ppm": None,
        "X_mantle_N_ppm": None,
        "X_mantle_S_ppm": None,
        "X_mantle_Ar_ppm": None,
        "X_mantle_H2O_ppm": None,
        "M_LV_kg": None,
        "delta_X_H2O_ppm": None,
        "log10_fO2": None,
        "D_lid_m": None,
        "M_outgassed_total_kg": None,
        "M_outgassed_per_species": None,
        "M_escaped_kg": None,
        "outgassed_mass": "Giant envelope — silicate volatile chain not applied",
        "E_Z": g.get("E_Z"),
        "Z_planet": g.get("Z_planet"),
        "X_H": g.get("X_H"),
        "Y_He": g.get("Y_He"),
        "speciation": sp,
        "M_atm_kg": None,
        "P_s_Pa": None,
        "M_ocean_kg": None,
        "delta_IW": None,
        "F_bar": None,
        "epsilon": None,
    }
    return base


def run_variable_08(
    seed: int,
    v01: dict,
    v02: dict,
    v03: dict,
    v04: dict,
    v05: dict,
    v06: dict,
) -> dict:
    """Variable 08 entry: volatile inventory and atmospheric mass assembly."""
    regime = v02["regime"]
    atm_class = v04.get("atm_class", "secondary_possible")

    if regime == "brown_dwarf":
        return _null_output("brown dwarf — no silicate mantle")

    if regime == "gas_giant":
        return _giant_assembly(seed, v01, v02)

    if regime == "sub_neptune" and atm_class == "primary_retained":
        return _giant_assembly(seed, v01, v02)

    m_star = v03["M_star_kg"]
    age_gyr = v03["age_Gyr"]
    m_kg = v01["M_kg"]
    r_m = v02["R_m"]
    g = v02["g_m_s2"]
    cmf = v02.get("CMF", 0.325)
    a_m = v05["a_m"]
    r_h = v05["R_H_m"]
    m_dot = v05["M_dot_kg_s"]
    t_eq = v05["T_eq_K"]

    if r_m is None or g is None:
        return _null_output("missing radius or gravity")

    p_cmb = v06.get("P_cmb_Pa")
    if p_cmb is None:
        return _null_output("V06 missing P_cmb — magma ocean or null tectonics")

    snow = compute_snow_lines(m_star)
    bulk = compute_bulk_volatile_fraction(a_m, r_h, snow)
    xb = compute_elemental_bulk(
        X_DRY,
        bulk["X_ice_H2O"],
        bulk["X_ice_CO2"],
        bulk["X_ice_N2"],
    )
    xm = compute_core_partitioning(xb, cmf, p_cmb)

    if regime == "dwarf":
        ps = 0.0 if atm_class == "none" else None
        x_h2o = bulk["X_ice_H2O"] * 5.0e5 + 50.0
        return {
            "volatile_note": "dwarf — mantle volatile budget only; outgassing deferred",
            "X_vol": bulk["X_vol"],
            "snow_lines": snow,
            "X_bulk_H_ppm": xb["X_bulk_H_ppm"],
            "X_bulk_C_ppm": xb["X_bulk_C_ppm"],
            "X_bulk_N_ppm": xb["X_bulk_N_ppm"],
            "X_bulk_S_ppm": xb["X_bulk_S_ppm"],
            "X_mantle_H_ppm": xm["X_mantle_H_ppm"],
            "X_mantle_C_ppm": xm["X_mantle_C_ppm"],
            "X_mantle_N_ppm": xm["X_mantle_N_ppm"],
            "X_mantle_S_ppm": xm["X_mantle_S_ppm"],
            "X_mantle_Ar_ppm": xm["X_mantle_Ar_ppm"],
            "X_mantle_H2O_ppm": x_h2o,
            "M_LV_kg": 0.0,
            "delta_X_H2O_ppm": 0.0,
            "delta_IW": None,
            "log10_fO2": None,
            "F_bar": None,
            "epsilon": None,
            "D_lid_m": None,
            "speciation": None,
            "M_outgassed_total_kg": None,
            "M_outgassed_per_species": None,
            "M_atm_kg": None,
            "P_s_Pa": ps,
            "M_ocean_kg": None,
            "M_escaped_kg": None,
            "outgassed_mass": "Dwarf — no atmosphere formation in V08",
        }

    t_m = v06.get("T_m_K")
    q_s = v06.get("q_s_Wm2")
    rho_m = v06.get("rho_mantle_kgm3") or v02.get("rho_mean_kg_m3", 3500.0)
    tec = v06.get("tectonic_regime") or "stagnant_lid"
    r_melt = v06.get("R_melt_kgs")

    xm_lv = compute_late_veneer(seed, m_kg, cmf, xm)
    m_lv = xm_lv.pop("M_LV_kg")

    neb = compute_nebular_ingassing(m_kg, r_m, g, m_star)
    xm_lv["X_mantle_H_ppm"] = xm_lv.get("X_mantle_H_ppm", 0.0) + neb["delta_X_H_ppm"]
    x_mantle_h2o_ppm = bulk["X_ice_H2O"] * 4.0e5 + neb["delta_X_H2O_ppm"] + 80.0

    fo2d = compute_oxygen_fugacity(p_cmb, t_m)
    log10_fo2 = fo2d.get("log10_fO2")
    delta_iw = fo2d.get("delta_IW")

    spec_pack = compute_outgassing_speciation(t_m, log10_fo2, xm_lv)
    speciation = spec_pack.get("speciation")

    melt = compute_melt_fraction(t_m, t_eq, q_s, rho_m, g, m_kg, tec)

    outg = compute_outgassing(
        r_melt,
        xm_lv,
        speciation,
        melt["F_bar"],
        melt["epsilon"],
        age_gyr,
    )

    atm = compute_atmospheric_mass(
        outg.get("M_outgassed_per_species") or {},
        m_dot,
        age_gyr,
        t_eq,
        g,
        r_m,
        atm_class,
        r_melt,
    )

    return {
        "volatile_note": "full V08 chain — rocky / cool envelope",
        "X_vol": bulk["X_vol"],
        "snow_lines": snow,
        "X_bulk_H_ppm": xb["X_bulk_H_ppm"],
        "X_bulk_C_ppm": xb["X_bulk_C_ppm"],
        "X_bulk_N_ppm": xb["X_bulk_N_ppm"],
        "X_bulk_S_ppm": xb["X_bulk_S_ppm"],
        "X_mantle_H_ppm": xm_lv["X_mantle_H_ppm"],
        "X_mantle_C_ppm": xm_lv["X_mantle_C_ppm"],
        "X_mantle_N_ppm": xm_lv["X_mantle_N_ppm"],
        "X_mantle_S_ppm": xm_lv["X_mantle_S_ppm"],
        "X_mantle_Ar_ppm": xm_lv["X_mantle_Ar_ppm"],
        "X_mantle_H2O_ppm": x_mantle_h2o_ppm,
        "M_LV_kg": m_lv,
        "delta_X_H2O_ppm": neb["delta_X_H2O_ppm"],
        "delta_IW": delta_iw,
        "log10_fO2": log10_fo2,
        "F_bar": melt["F_bar"],
        "epsilon": melt["epsilon"],
        "D_lid_m": melt["D_lid_m"],
        "speciation": speciation,
        "M_outgassed_total_kg": outg["M_outgassed_total_kg"],
        "M_outgassed_per_species": outg["M_outgassed_per_species"],
        "M_atm_kg": atm["M_atm_kg"],
        "P_s_Pa": atm["P_s_Pa"],
        "M_ocean_kg": atm["M_ocean_kg"],
        "M_escaped_kg": atm["M_escaped_kg"],
        "outgassed_mass": f"Integrated — {outg.get('outgassing_note', '')}",
        "speciation_note": spec_pack.get("speciation_note"),
        "H2O_H2_ratio": spec_pack.get("H2O_H2_ratio"),
        "CO2_CO_ratio": spec_pack.get("CO2_CO_ratio"),
        "nebular": neb,
        "melt_note": melt["melt_note"],
    }
