# variable_07_hydrology/variable_07_hydrology.py
#
# Variable 07: Hydrology — entry point. No physics here; assembly and regime routing only.

from variable_07_hydrology.budyko_partitioning import compute_budyko_ratio
from variable_07_hydrology.crustal_porosity import compute_compaction_depth
from variable_07_hydrology.ice_line_latitude import compute_ice_line_latitude
from variable_07_hydrology.fluvial_gravity_scaling import compute_fluvial_gravity_scaling
from variable_07_hydrology.glacial_gravity_scaling import compute_glacial_gravity_scaling
from variable_07_hydrology.latent_heat_transport import compute_latent_heat_transport
from variable_07_hydrology.precipitation_energy_limit import compute_pet
from variable_07_hydrology.subsurface_liquid_horizon import compute_subsurface_liquid_horizon
from variable_07_hydrology.volatile_phase_state import evaluate_all_species


def _null_hydrology(note: str) -> dict:
    return {
        "phase_states": None,
        "z_subsurface_liquid_m": None,
        "z_compaction_depth_m": None,
        "PET_kg_m2_s": None,
        "PET_mm_yr": None,
        "R_n_Wm2": None,
        "budyko_ET_over_P": None,
        "fluvial_U_scaling": None,
        "fluvial_Q_scaling": None,
        "glacial_U_scaling": None,
        "Q_latent_max_W": None,
        "ice_line_lat_deg": None,
        "ice_line_state": None,
        "ice_line_T0_C": None,
        "ice_line_T2_C": None,
        "ice_line_T_f_K": None,
        "ice_line_notes": None,
        "hydrology_note": note,
    }


def run_variable_07(
    v01: dict, v02: dict, v03: dict, v04: dict, v05: dict, v06: dict, v08: dict
) -> dict:
    _ = (v01, v03)
    regime = v02["regime"]

    if regime in ("gas_giant", "brown_dwarf"):
        return _null_hydrology("no solid surface; hydrology not applicable")

    if regime == "dwarf":
        phase_states = evaluate_all_species(
            speciation_dict=v08.get("speciation"),
            T_eq_K=v05["T_eq_K"],
            P_s_Pa=0.0,
        )
        return {
            "phase_states": phase_states,
            "z_subsurface_liquid_m": None,
            "z_compaction_depth_m": None,
            "PET_kg_m2_s": None,
            "PET_mm_yr": None,
            "R_n_Wm2": None,
            "budyko_ET_over_P": None,
            "fluvial_U_scaling": None,
            "fluvial_Q_scaling": None,
            "glacial_U_scaling": None,
            "Q_latent_max_W": None,
            "ice_line_lat_deg": None,
            "ice_line_state": None,
            "ice_line_T0_C": None,
            "ice_line_T2_C": None,
            "ice_line_T_f_K": None,
            "ice_line_notes": None,
            "hydrology_note": (
                "Dwarf — volatile phase state only (P_s = 0 Pa); "
                "full hydrology deferred for non-rocky surface context"
            ),
        }

    # rocky, sub_neptune
    g = v02["g_m_s2"]
    R_m = v02["R_m"]
    rho_mean = v02["rho_mean_kg_m3"]
    P_s = v04["P_s_Pa"]
    if P_s is None:
        P_s = v08.get("P_s_Pa")

    phase_states = evaluate_all_species(
        speciation_dict=v08.get("speciation"),
        T_eq_K=v05["T_eq_K"],
        P_s_Pa=P_s,
    )

    P_sub = P_s if P_s is not None else 0.0
    subsurface = compute_subsurface_liquid_horizon(
        T_eq_K=v05["T_eq_K"],
        q_s_Wm2=v06["q_s_Wm2"],
        g=g,
        P_s_Pa=P_sub,
        rho_mean_kgm3=rho_mean,
    )

    z_e_m = compute_compaction_depth(g=g)

    pet = compute_pet(
        F_mean_Wm2=v05["F_mean_W_m2"],
        albedo_final=v05["albedo_final"],
    )

    budyko = compute_budyko_ratio(
        PET_kg_m2_s=pet["PET_kg_m2_s"] if pet else None,
        P_kg_m2_s=None,
    )

    fluvial = compute_fluvial_gravity_scaling(g=g)
    glacial = compute_glacial_gravity_scaling(g=g)

    pet_rate = pet["PET_kg_m2_s"] if pet else 0.0
    latent = compute_latent_heat_transport(PET_kg_m2_s=pet_rate, R_m=R_m)

    ice_line = compute_ice_line_latitude(
        F_mean_W_m2=v05["F_mean_W_m2"],
        T_eq_K=v05["T_eq_K"],
        obliquity_deg=v05["obliquity_deg"],
        albedo_final=v05.get("albedo_final", v05.get("albedo_proxy", 0.30)),
        atm_class=v04.get("atm_class", "secondary_possible"),
        phase_states=phase_states,
    )

    return {
        "phase_states": phase_states,
        "z_subsurface_liquid_m": subsurface,
        "z_compaction_depth_m": z_e_m,
        "PET_kg_m2_s": pet["PET_kg_m2_s"] if pet else None,
        "PET_mm_yr": pet["PET_mm_yr"] if pet else None,
        "R_n_Wm2": pet["R_n_Wm2"] if pet else None,
        "budyko_ET_over_P": budyko["ET_over_P"],
        "fluvial_U_scaling": fluvial["U_scaling"],
        "fluvial_Q_scaling": fluvial["Q_scaling"],
        "glacial_U_scaling": glacial["U_ice_scaling"],
        "Q_latent_max_W": latent["Q_latent_max_W"],
        "ice_line_lat_deg": ice_line["ice_line_lat_deg"],
        "ice_line_state": ice_line["ice_line_state"],
        "ice_line_T0_C": ice_line["T0_C"],
        "ice_line_T2_C": ice_line["T2_C"],
        "ice_line_T_f_K": ice_line["T_f_K"],
        "ice_line_notes": ice_line["ice_line_notes"],
        "hydrology_note": "Regime: rocky or sub_neptune — full Variable 07 assembly",
    }
