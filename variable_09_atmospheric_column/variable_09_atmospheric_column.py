# variable_09_atmospheric_column/variable_09_atmospheric_column.py
#
# Variable 09 entry: orchestration only (no embedded physics formulas).

from __future__ import annotations

from typing import Any, Mapping

import numpy as np

from variable_09_atmospheric_column.eddy_diffusion_kzz import compute_kzz_profile_cm2_s
from variable_09_atmospheric_column.gas_envelope_internal_heat import (
    compute_f_int,
    compute_f_int_sub_neptune_safe,
)
from variable_09_atmospheric_column.homopause_altitude import compute_homopause_altitude_m
from variable_09_atmospheric_column.joined_solution_t_surface import (
    compute_t_surface,
    compute_t_surface_gas_envelope,
)
from variable_09_atmospheric_column.kombayashi_ingersoll_limit import evaluate_runaway_flag
from variable_09_atmospheric_column.line_absorption_coefficients import verify_earth_line_closure
from variable_09_atmospheric_column.moist_adiabat_beta import compute_beta_moist
from variable_09_atmospheric_column.photolysis_rates import compute_photolysis_rates_toa
from variable_09_atmospheric_column.radical_steady_state import compute_radical_steady_state
from variable_09_atmospheric_column.regime_router import resolve_v09_routing
from variable_09_atmospheric_column.species_lifetimes import compute_species_lifetimes_s
from variable_09_atmospheric_column.t_p_profile import compute_t_p_profile
from variable_09_atmospheric_column.tau_rc_implicit_solver import compute_tau_rc_implicit
from variable_09_atmospheric_column.tau_zero_compositional import (
    MOLAR_MASS_KG_MOL,
    compute_tau_zero,
)
from variable_09_atmospheric_column.titan_tholin_anti_greenhouse import (
    compute_t_skin_eff_titan,
)
from variable_09_atmospheric_column.venus_shortwave_attenuation import (
    build_venus_branch_metadata,
)


def _skip_output(v05: Mapping[str, Any], reason: str) -> dict[str, Any]:
    return {
        "T_surface_K": float(v05["T_eq_K"]),
        "T_skin_K": None,
        "tau_zero": None,
        "tau_rc": None,
        "beta": None,
        "n": None,
        "F_int_W_m2": None,
        "P_array_Pa": None,
        "T_array_K": None,
        "K_zz_cm2_s": None,
        "K_zz_tropopause_cm2_s": None,
        "z_homo_m": None,
        "photolysis_J": None,
        "tau_chem_s": None,
        "radical_regime": None,
        "OH_cm3": None,
        "H_cm3": None,
        "runaway_flag": None,
        "OLR_KI_W_m2": None,
        "regime_class": "skip",
        "terrestrial_route": None,
        "notes": [reason],
        "venus_metadata": None,
    }


def run(
    seed: int,
    v01: Mapping[str, Any],
    v02: Mapping[str, Any],
    v03: Mapping[str, Any],
    v04: Mapping[str, Any],
    v05: Mapping[str, Any],
    v06: Mapping[str, Any],
    v08: Mapping[str, Any],
) -> dict[str, Any]:
    _ = (seed, v06)
    atm_class = str(v04.get("atm_class", "secondary_possible"))
    regime = str(v02.get("regime", "rocky"))
    P_s = v04.get("P_s_Pa")
    if P_s is None:
        P_s = v08.get("P_s_Pa")
    speciation = v08.get("speciation")
    if not isinstance(speciation, Mapping):
        speciation = {}

    route = resolve_v09_routing(
        regime=regime,
        atm_class=atm_class,
        P_s_Pa=float(P_s) if P_s is not None else None,
        T_eq_K=float(v05["T_eq_K"]),
        speciation=speciation,
    )
    notes: list[str] = []
    if route.kind == "skip":
        return _skip_output(v05, route.skip_reason or "skip")

    # V04 leaves P_s undefined for gas giants / thick envelopes (no solid surface).
    if P_s is None and route.kind == "gas_envelope":
        # ⚠️ EARTH FALLBACK — Flag 179 photospheric reference pressure for gray
        # τ₀ column when hydrostatic P_s is absent from cascade.
        P_s = 1.0e5
        notes.append(
            "Flag 179: P_s absent — using 1 bar photospheric reference for gas envelope."
        )

    g = float(v02["g_m_s2"])
    T_eq = float(v05["T_eq_K"])

    # --- gas envelope -------------------------------------------------
    if route.kind == "gas_envelope":
        f_solar = float(v05["F_mean_W_m2"]) * (1.0 - float(v05["albedo_final"]))
        age = float(v03["age_Gyr"])
        m_kg = float(v01["M_kg"])
        f_int = None
        if regime == "gas_giant":
            try:
                f_int = compute_f_int(m_kg, age)
            except ValueError as e:
                raise RuntimeError(f"Rule 2: gas giant F_int: {e}") from e
        else:
            f_int, flag167 = compute_f_int_sub_neptune_safe(m_kg, age)
            if flag167 is not None:
                notes.append(str(flag167))
        try:
            tau_z = compute_tau_zero(
                P_s_Pa=float(P_s),
                g_m_s2=g,
                T_eq_K=T_eq,
                speciation=speciation,
                branch="gas_envelope",
            )
        except NotImplementedError as e:
            raise RuntimeError(
                f"Rule 2 / missing data for gas envelope τ₀: {e}"
            ) from e
        beta = compute_beta_moist(speciation, T_eq, None)
        n = float(route.n or 2)
        tau_rc = compute_tau_rc_implicit(beta, n)
        t_surf = compute_t_surface_gas_envelope(
            f_solar, tau_rc, tau_z, beta, n, f_int, D=1.5
        )
        p_arr, t_arr, z_arr = compute_t_p_profile(
            P_s_Pa=float(P_s),
            T_surface_K=t_surf,
            T_skin_K=T_eq / (2.0**0.25),
            tau_zero=tau_z,
            tau_rc=tau_rc,
            beta=beta,
            n=n,
            g_m_s2=g,
            m_bar_kg_mol=_mean_molar_mass(speciation),
            T_exo_K=v04.get("T_exo_K"),
        )
        kzz, kzz_ref = compute_kzz_profile_cm2_s(
            P_arr_Pa=p_arr,
            T_arr_K=t_arr,
            P_tropopause_Pa=float(P_s) * (tau_rc / tau_z) ** (1.0 / n),
            m_bar_kg_mol=_mean_molar_mass(speciation),
            g_m_s2=g,
            T_surface_K=t_surf,
            albedo_final=float(v05["albedo_final"]),
            F_mean_W_m2=float(v05["F_mean_W_m2"]),
        )
        i_rc = int(np.argmin(np.abs(p_arr - float(P_s) * (tau_rc / tau_z) ** (1.0 / n))))
        kzz_trop = float(kzz[i_rc])
        light, heavy = _dominant_diffusion_pair(speciation)
        z_homo = compute_homopause_altitude_m(
            z_m=z_arr,
            P_arr_Pa=p_arr,
            T_arr_K=t_arr,
            K_zz_cm2_s=kzz,
            dominant_light=light,
            dominant_heavy=heavy,
        )
        j_photo = compute_photolysis_rates_toa(
            speciation, float(v05["F_XUV_W_m2"]), 0.0
        )
        rad = compute_radical_steady_state(
            speciation=speciation,
            T_K=t_surf,
            P_s_Pa=float(P_s),
            m_bar_kg_mol=_mean_molar_mass(speciation),
            photolysis_J=j_photo,
            F_xuv_W_m2=float(v05["F_XUV_W_m2"]),
        )
        tau_chem = compute_species_lifetimes_s(
            speciation=speciation,
            photolysis_J=j_photo,
            T_K=t_surf,
            OH_cm3=rad.get("OH_cm3"),
        )
        rw, olr = evaluate_runaway_flag(
            F_mean_W_m2=float(v05["F_mean_W_m2"]),
            albedo_final=float(v05["albedo_final"]),
            g_m_s2=g,
        )
        return {
            "T_surface_K": float(t_surf),
            "T_skin_K": None,
            "tau_zero": float(tau_z),
            "tau_rc": float(tau_rc),
            "beta": float(beta),
            "n": int(route.n or 2),
            "F_int_W_m2": f_int,
            "P_array_Pa": p_arr,
            "T_array_K": t_arr,
            "K_zz_cm2_s": kzz,
            "K_zz_tropopause_cm2_s": kzz_trop,
            "z_homo_m": z_homo,
            "photolysis_J": j_photo,
            "tau_chem_s": tau_chem,
            "radical_regime": rad.get("regime"),
            "OH_cm3": rad.get("OH_cm3"),
            "H_cm3": rad.get("H_cm3"),
            "runaway_flag": rw,
            "OLR_KI_W_m2": olr,
            "regime_class": "gas_envelope",
            "terrestrial_route": None,
            "notes": notes,
            "venus_metadata": None,
        }

    # --- terrestrial ---------------------------------------------------
    tr = route.terrestrial_route or "thick_terrestrial"
    m_bar = _mean_molar_mass(speciation)
    beta = compute_beta_moist(speciation, T_eq, tr)
    n = int(route.n if route.n is not None else 2)
    if route.tau_rc_override is not None:
        tau_rc = float(route.tau_rc_override)
    else:
        tau_rc = compute_tau_rc_implicit(beta, float(n))
        if n == 2 and tr != "venus_class":
            if not (0.05 <= tau_rc <= 0.5):
                raise RuntimeError(
                    f"Rule 2: τ_rc={tau_rc} outside [0.05, 0.5] for terrestrial n=2 "
                    f"(route={tr})."
                )

    try:
        tau_z = compute_tau_zero(
            P_s_Pa=float(P_s),
            g_m_s2=g,
            T_eq_K=T_eq,
            speciation=speciation,
            branch=tr,
        )
    except NotImplementedError as e:
        raise RuntimeError(f"Rule 2: τ₀ composition blocked: {e}") from e

    if tr == "titan_class":
        t_skin = compute_t_skin_eff_titan(T_eq)
    else:
        t_skin = T_eq / (2.0**0.25)

    venus_meta = None
    if tr == "venus_class":
        venus_meta = build_venus_branch_metadata()
        notes.append("Flag 163: Venus gray T_surface is lower bound for thick CO2.")

    t_surf = compute_t_surface(t_skin, tau_z, tau_rc, beta, n, D=1.5)

    p_arr, t_arr, z_arr = compute_t_p_profile(
        P_s_Pa=float(P_s),
        T_surface_K=t_surf,
        T_skin_K=t_skin,
        tau_zero=tau_z,
        tau_rc=tau_rc,
        beta=beta,
        n=float(n),
        g_m_s2=g,
        m_bar_kg_mol=m_bar,
        T_exo_K=v04.get("T_exo_K"),
    )
    p_rc = float(P_s) * (tau_rc / tau_z) ** (1.0 / float(n))
    kzz, _ = compute_kzz_profile_cm2_s(
        P_arr_Pa=p_arr,
        T_arr_K=t_arr,
        P_tropopause_Pa=p_rc,
        m_bar_kg_mol=m_bar,
        g_m_s2=g,
        T_surface_K=t_surf,
        albedo_final=float(v05["albedo_final"]),
        F_mean_W_m2=float(v05["F_mean_W_m2"]),
    )
    i_rc = int(np.argmin(np.abs(p_arr - p_rc)))
    kzz_trop = float(kzz[i_rc])
    light, heavy = _dominant_diffusion_pair(speciation)
    z_homo = compute_homopause_altitude_m(
        z_m=z_arr,
        P_arr_Pa=p_arr,
        T_arr_K=t_arr,
        K_zz_cm2_s=kzz,
        dominant_light=light,
        dominant_heavy=heavy,
    )
    j_photo = compute_photolysis_rates_toa(
        speciation, float(v05["F_XUV_W_m2"]), 0.0
    )
    rad = compute_radical_steady_state(
        speciation=speciation,
        T_K=t_surf,
        P_s_Pa=float(P_s),
        m_bar_kg_mol=m_bar,
        photolysis_J=j_photo,
        F_xuv_W_m2=float(v05["F_XUV_W_m2"]),
    )
    oh = rad.get("OH_cm3")
    tau_chem = compute_species_lifetimes_s(
        speciation=speciation,
        photolysis_J=j_photo,
        T_K=t_surf,
        OH_cm3=oh,
    )
    rw, olr = evaluate_runaway_flag(
        F_mean_W_m2=float(v05["F_mean_W_m2"]),
        albedo_final=float(v05["albedo_final"]),
        g_m_s2=g,
    )

    return {
        "T_surface_K": float(t_surf),
        "T_skin_K": float(t_skin),
        "tau_zero": float(tau_z),
        "tau_rc": float(tau_rc),
        "beta": float(beta),
        "n": int(n),
        "F_int_W_m2": None,
        "P_array_Pa": p_arr,
        "T_array_K": t_arr,
        "K_zz_cm2_s": kzz,
        "K_zz_tropopause_cm2_s": kzz_trop,
        "z_homo_m": z_homo,
        "photolysis_J": j_photo,
        "tau_chem_s": tau_chem,
        "radical_regime": rad.get("regime"),
        "OH_cm3": rad.get("OH_cm3"),
        "H_cm3": rad.get("H_cm3"),
        "runaway_flag": rw,
        "OLR_KI_W_m2": olr,
        "regime_class": f"terrestrial:{tr}",
        "terrestrial_route": tr,
        "notes": notes,
        "venus_metadata": venus_meta,
    }


def _mean_molar_mass(speciation: Mapping[str, Any]) -> float:
    m_bar = 0.0
    for sp, x in speciation.items():
        if x is None or float(x) <= 0.0:
            continue
        mm = MOLAR_MASS_KG_MOL.get(str(sp))
        if mm is None:
            continue
        m_bar += float(x) * mm
    if m_bar <= 0.0:
        raise ValueError("V09: m_bar undefined — speciation missing masses.")
    return float(m_bar)


def _dominant_diffusion_pair(
    speciation: Mapping[str, Any],
) -> tuple[str, str]:
    """Choose (light, heavy) for homopause b₁₂ lookup."""
    x_h2 = float(speciation.get("H2", 0.0) or 0.0)
    x_he = float(speciation.get("He", 0.0) or 0.0)
    light = "H2" if x_h2 >= x_he else "He"
    candidates = [
        ("N2", float(speciation.get("N2", 0.0) or 0.0)),
        ("CO2", float(speciation.get("CO2", 0.0) or 0.0)),
        ("CO", float(speciation.get("CO", 0.0) or 0.0)),
    ]
    heavy = max(candidates, key=lambda t: t[1])[0]
    if max(c[1] for c in candidates) <= 0.0:
        heavy = "CO2"
    return light, heavy


def run_calibration_checks() -> None:
    """§16 calibration — raises RuntimeError on Rule 2 failure."""
    # Earth — joined + τ₀ band + line closure
    ps_e = 101325.0
    g_e = 9.80665
    x_earth = {"N2": 0.78, "O2": 0.21, "Ar": 0.01, "H2O": 0.01, "CO2": 400e-6}
    m_e = _mean_molar_mass(x_earth)
    verify_earth_line_closure(
        P_s_Pa=ps_e,
        g_m_s2=g_e,
        m_bar_kg_mol=m_e,
        x_h2o=0.01,
        x_co2=400e-6,
    )
    tau_e = compute_tau_zero(
        P_s_Pa=ps_e,
        g_m_s2=g_e,
        T_eq_K=255.0,
        speciation=x_earth,
        branch="thick_terrestrial",
    )
    if not (1.5 <= tau_e <= 2.5):
        raise RuntimeError(f"Rule 2: Earth τ₀={tau_e} outside [1.5, 2.5].")
    beta_e = 0.19
    n_e = 2
    trc_e = compute_tau_rc_implicit(beta_e, float(n_e))
    if not (0.05 <= trc_e <= 0.5):
        raise RuntimeError(f"Rule 2: Earth τ_rc={trc_e} outside [0.05, 0.5].")
    t_skin_e = 214.4
    # §16 Earth T check: scaffold calibration text uses τ_rc ≈ 0.1 (Robinson &
    # Catling joined RC anchor); implicit τ_rc above is verified separately.
    t_s_e = compute_t_surface(t_skin_e, tau_e, 0.1, beta_e, n_e)
    if not (278.0 <= t_s_e <= 298.0):
        raise RuntimeError(f"Rule 2: Earth T_surface={t_s_e} outside [278,298] K.")

    # Mars — joined fixture (prescribed optical depths)
    beta_m = 0.22
    n_m = 2
    trc_m = compute_tau_rc_implicit(beta_m, float(n_m))
    t_skin_m = 240.0 / (2.0**0.25)
    tau_z_m = 0.087
    t_s_m = compute_t_surface(t_skin_m, tau_z_m, trc_m, beta_m, n_m)
    if not (199.0 <= t_s_m <= 221.0):
        raise RuntimeError(f"Rule 2: Mars T_surface={t_s_m} outside [199,221] K.")

    # Titan
    tsk = compute_t_skin_eff_titan(82.0)
    trc_t = compute_tau_rc_implicit(0.2, 2.0)
    t_s_t = compute_t_surface(tsk, 2.0, trc_t, 0.2, 2)
    if not (89.0 <= t_s_t <= 99.0):
        raise RuntimeError(f"Rule 2: Titan T_surface={t_s_t} outside [89,99] K.")

    # Venus
    t_s_v = compute_t_surface(195.1, 400.0, 1.0, 0.1643, 1)
    if not (620.0 <= t_s_v <= 700.0):
        raise RuntimeError(f"Rule 2: Venus T_surface={t_s_v} outside [620,700] K.")

    # Saturn F_int
    m_sat = 5.6834e26
    f_i = compute_f_int(m_sat, 4.5)
    if not (1.4 <= f_i <= 2.6):
        raise RuntimeError(f"Rule 2: Saturn F_int={f_i} outside [1.4, 2.6] W/m².")

    # Earth OH calibration
    jfix = {"O3": 1.1e-6, "H2O": 1e-10}
    rad_e = compute_radical_steady_state(
        speciation={
            "N2": 0.78,
            "O2": 0.21,
            "H2O": 0.01,
            "CO": 300e-9,
            "O3": 30e-9,
        },
        T_K=288.0,
        P_s_Pa=101325.0,
        m_bar_kg_mol=m_e,
        photolysis_J=jfix,
        F_xuv_W_m2=1e-3,
    )
    oh_e = rad_e.get("OH_cm3")
    if oh_e is None or not (1.0e5 <= oh_e <= 1.0e7):
        raise RuntimeError(f"Rule 2: Earth calib [OH]={oh_e} outside [1e5,1e7].")

    print("V09 calibration: all §16 checks PASSED.")
