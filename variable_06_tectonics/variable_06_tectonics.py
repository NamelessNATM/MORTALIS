# variable_06_tectonics/variable_06_tectonics.py
#
# Entry point for Variable 06: Tectonics.
# Orchestrates all sub-functions. Contains no physics directly.
#
# REGIME ROUTING:
#   rocky        → full V06 treatment
#   sub_neptune  → V06 treatment IF T_eq < T_SOLIDUS; else magma_ocean (all None)
#   gas_giant    → not applicable; all tectonic outputs None
#   brown_dwarf  → not applicable; all tectonic outputs None
#   dwarf        → stagnant lid mandated; reduced output set
#
# T_SOLIDUS = 1500 K — silicate solidus threshold for sub-Neptune magma ocean check.
# ⚠️ EARTH FALLBACK — Flag 58.
#
# CASCADE ORDER (confirmed): v01 → v02 → v03 → v05 → v04 → v06 → map_generator

import math

from variable_06_tectonics.accretional_energy import compute_accretional_energy
from variable_06_tectonics.cmb_pressure import compute_cmb_pressure
from variable_06_tectonics.core_geometry import compute_core_geometry
from variable_06_tectonics.mantle_temperature import integrate_mantle_temperature
from variable_06_tectonics.mantle_viscosity import (
    compute_frank_kamenetskii,
    compute_mantle_viscosity,
)
from variable_06_tectonics.radiogenic_heating import compute_radiogenic_heating
from variable_06_tectonics.rayleigh_number import compute_rayleigh_number
from variable_06_tectonics.surface_heat_flux import compute_surface_heat_flux
from variable_06_tectonics.tectonic_regime import classify_tectonic_regime
from variable_06_tectonics.tidal_heating import compute_tidal_heating
from variable_06_tectonics.tidal_locking import compute_tidal_locking
from variable_06_tectonics.volcanic_melt_rate import compute_volcanic_melt_rate

_T_SOLIDUS = 1500.0  # ⚠️ EARTH FALLBACK — Flag 58


def _null_output(note: str) -> dict:
    return {
        "tectonic_note": note,
        "tectonic_regime": None,
        "E_acc_J": None,
        "R_core_m": None,
        "rho_mantle_kgm3": None,
        "rho_core_kgm3": None,
        "P_cmb_Pa": None,
        "H_rad_W": None,
        "T_m_K": None,
        "Ra": None,
        "q_s_Wm2": None,
        "q_s_total_TW": None,
        "t_lock_Gyr": None,
        "is_locked": None,
        "P_tidal_W": None,
        "R_melt_kgs": None,
        "speciation": None,
        "outgassed_mass": "Blocked — fO2 and volatile inventory absent from cascade",
    }


def run_variable_06(v01: dict, v02: dict, v03: dict, v05: dict, v04: dict) -> dict:
    """
    Compute tectonic and internal dynamics outputs for the simulated planet.

    Parameters
    ----------
    v01 : dict — Variable 01 outputs (M_kg, mu)
    v02 : dict — Variable 02 outputs (regime, R_m, g, P_c_Pa, rho_mean, CMF optional)
    v03 : dict — Variable 03 outputs (M_star_kg, age_Gyr)
    v05 : dict — Variable 05 outputs (a_m, e, T_orb_s, T_eq_K, F_mean_Wm2)
    v04 : dict — Variable 04 outputs (atm_class)

    Returns
    -------
    dict — V06 output variables
    """
    regime = v02["regime"]
    M = v01["M_kg"]
    R = v02["R_m"]
    g = v02["g_m_s2"]
    P_c = v02["P_c_Pa"]
    rho_mean = v02["rho_mean_kg_m3"]
    CMF = v02.get("CMF", 0.325)
    age_Gyr = v03["age_Gyr"]
    age_s = age_Gyr * 3.15576e16
    M_star = v03["M_star_kg"]
    a = v05["a_m"]
    e = v05["e"]
    T_orb = v05["T_orb_s"]
    T_eq = v05["T_eq_K"]

    # Gas giant and brown dwarf: no solid mantle, V06 not applicable
    if regime in ("gas_giant", "brown_dwarf"):
        return _null_output("V06 not applicable — no solid silicate mantle")

    # Sub-Neptune: check for magma ocean
    if regime == "sub_neptune" and T_eq >= _T_SOLIDUS:
        return _null_output(
            f"Sub-Neptune magma ocean — T_eq={T_eq:.1f} K >= T_solidus={_T_SOLIDUS} K. "
            "No solid lithosphere; tectonic classification not applicable."
        )

    # --- Quantities computed for rocky, dwarf, and cool sub-Neptune ---

    accretion = compute_accretional_energy(M, R)
    core_geom = compute_core_geometry(R, CMF, rho_mean)
    R_core = core_geom["R_core_m"]
    rho_mantle = core_geom["rho_mantle_kgm3"]
    rho_core = core_geom["rho_core_kgm3"]
    D = R - R_core  # mantle depth [m]
    P_cmb = compute_cmb_pressure(R, R_core, M, CMF, rho_mantle)

    # Tidal quantities (universal across solid-body regimes)
    tidal_lock = compute_tidal_locking(M, R, CMF, a, M_star, age_s)
    P_tidal = compute_tidal_heating(M_star, R, a, e, T_orb)

    # Dwarf: stagnant lid mandated — simplified thermal path
    if regime == "dwarf":
        M_mantle = M * (1.0 - CMF)
        H_rad = compute_radiogenic_heating(M_mantle, age_Gyr)
        q_s, _ = compute_surface_heat_flux(300.0, T_eq, D, convecting=False)
        q_total = 4.0 * math.pi * R**2 * q_s / 1e12

        return {
            "tectonic_note": "Dwarf — stagnant lid mandated by secular cooling physics",
            "tectonic_regime": "stagnant_lid",
            "E_acc_J": accretion["E_total_J"],
            "R_core_m": R_core,
            "rho_mantle_kgm3": rho_mantle,
            "rho_core_kgm3": rho_core,
            "P_cmb_Pa": P_cmb,
            "H_rad_W": H_rad,
            "T_m_K": None,  # ODE not run for dwarfs; secular cooling too rapid
            "Ra": None,
            "q_s_Wm2": q_s,
            "q_s_total_TW": q_total,
            "t_lock_Gyr": tidal_lock["t_lock_Gyr"],
            "is_locked": tidal_lock["is_locked"],
            "P_tidal_W": P_tidal,
            "R_melt_kgs": 0.0,
            "speciation": None,
            "outgassed_mass": "Blocked — fO2 and volatile inventory absent from cascade",
        }

    # --- Rocky and cool sub-Neptune: full thermal evolution ---

    def q_s_func(T_m, T_eq, D):
        """Wrapper for ODE integrator. Returns (q_s_Wm2, Nu)."""
        eta = compute_mantle_viscosity(T_m)
        theta = compute_frank_kamenetskii(T_m, T_eq)
        Ra_d = compute_rayleigh_number(rho_mantle, g, T_m, T_eq, D, eta)
        # Classify regime at current T_m for Nu-Ra formula selection
        t_reg = classify_tectonic_regime(Ra_d["Ra"], Ra_d["Ra_c"])
        return compute_surface_heat_flux(
            T_m,
            T_eq,
            D,
            Ra=Ra_d["Ra"],
            Ra_c=Ra_d["Ra_c"],
            theta=theta,
            tectonic_regime=t_reg,
            convecting=Ra_d["convecting"],
        )

    thermal = integrate_mantle_temperature(
        M, CMF, R, T_eq, D, P_cmb, q_s_func, age_Gyr
    )
    T_m = thermal["T_m_K"]
    solidus_reached = thermal["solidus_reached"]
    solidus_K = thermal["solidus_K"]
    M_mantle = M * (1.0 - CMF)
    H_rad = compute_radiogenic_heating(M_mantle, age_Gyr)
    eta = compute_mantle_viscosity(T_m)
    theta = compute_frank_kamenetskii(T_m, T_eq)
    Ra_result = compute_rayleigh_number(rho_mantle, g, T_m, T_eq, D, eta)
    Ra = Ra_result["Ra"]
    Ra_c = Ra_result["Ra_c"]
    tec_regime = classify_tectonic_regime(Ra, Ra_c)

    q_s, Nu_final = compute_surface_heat_flux(
        T_m,
        T_eq,
        D,
        Ra=Ra,
        Ra_c=Ra_c,
        theta=theta,
        tectonic_regime=tec_regime,
        convecting=Ra_result["convecting"],
    )
    q_total_TW = 4.0 * math.pi * R**2 * q_s / 1e12

    R_melt = (
        compute_volcanic_melt_rate(
            Nu_final, T_m, T_eq, R, g, D, rho_mantle, tec_regime
        )
        if Ra_result["convecting"]
        else 0.0
    )

    return {
        "tectonic_note": (
            f"Regime: {tec_regime}. Solidus reached — magma ocean or heat-pipe regime."
            if solidus_reached
            else f"Regime: {tec_regime}. Full thermal evolution computed."
        ),
        "tectonic_regime": tec_regime,
        "solidus_K": solidus_K,
        "solidus_reached": solidus_reached,
        "E_acc_J": accretion["E_total_J"],
        "R_core_m": R_core,
        "rho_mantle_kgm3": rho_mantle,
        "rho_core_kgm3": rho_core,
        "P_cmb_Pa": P_cmb,
        "H_rad_W": H_rad,
        "T_m_K": T_m,
        "Ra": Ra,
        "q_s_Wm2": q_s,
        "q_s_total_TW": q_total_TW,
        "t_lock_Gyr": tidal_lock["t_lock_Gyr"],
        "is_locked": tidal_lock["is_locked"],
        "P_tidal_W": P_tidal,
        "R_melt_kgs": R_melt,
        "speciation": None,
        "outgassed_mass": "Blocked — fO2 and volatile inventory absent from cascade",
    }
