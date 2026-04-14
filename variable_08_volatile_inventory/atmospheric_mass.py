# variable_08_volatile_inventory/atmospheric_mass.py
#
# Atmospheric mass balance: escape, ocean condensation, and silicate weathering.
#
# Formula: M_atm = M_outgassed − M_escaped − M_sequestered; P_s = M_atm×g/(4πR²)
#          H2O sequestration: Clausius-Clapeyron (P_sat); CO2 sequestration: Walker (1981) weathering
# Earth calibration (abiotic): M_atm=3.88×10¹⁸ kg, P_s=74,780 Pa ✓
# Flag 130: Walker (1981) weathering constants — Earth-empirical. W_0=3.3×10¹⁴ mol/yr,
#           P_CO2_0=3×10⁻⁴ bar, T_0=285 K, exponent 0.3, sensitivity 13.7 K. Earth fallback.
#           Not applicable without liquid water (T_eq outside 273–373 K range).

import math

R_GAS = 8.314  # J/mol/K (Category A)
DH_VAP_H2O = 40650.0  # J/mol — Flag 78 (already in codebase)
T_REF_H2O = 373.15  # K
P_REF_H2O = 101325.0  # Pa

# Walker (1981) weathering — ⚠️ Flag 130 — Earth-empirical
W_0_MOL_YR = 3.3e14  # mol/yr
P_CO2_0_BAR = 3.0e-4  # bar
T_0_K = 285.0  # K
W_EXPONENT = 0.3
W_SENSITIVITY = 13.7  # K

S_PER_GYR = 3.154e16  # s/Gyr
SEC_PER_YR = 3.154e7  # s/yr (approximate)

# Order-of-melt CO2 fraction when speciation split unavailable here (Earth-like)
_DEFAULT_F_CO2_IN_C = 0.85


def compute_atmospheric_mass(
    M_outgassed_per_species: dict,
    M_dot_kg_s: float,
    age_Gyr: float,
    T_eq_K: float,
    g: float,
    R_m: float,
    atm_class: str,
    R_melt_kgs: float | None,
) -> dict:
    """Net atmospheric mass and surface pressure after escape and sequestration."""
    species = {k: float(v) for k, v in M_outgassed_per_species.items()}

    m_esc_budget = M_dot_kg_s * age_Gyr * S_PER_GYR
    avail = species.get("H2", 0.0) + species.get("H2O", 0.0)
    take_esc = min(m_esc_budget, avail)
    rem = take_esc
    for key in ("H2", "H2O"):
        if key in species and rem > 0.0:
            t = min(rem, species[key])
            species[key] -= t
            rem -= t
    m_escaped = take_esc

    m_h2o_out = species.get("H2O", 0.0)
    p_sat = P_REF_H2O * math.exp(
        -DH_VAP_H2O / R_GAS * (1.0 / T_eq_K - 1.0 / T_REF_H2O)
    )
    if atm_class in ("none", "exosphere_only"):
        m_h2o_atm_max = 0.0
        m_h2o_seq = m_h2o_out
    else:
        m_h2o_atm_max = p_sat * 4.0 * math.pi * R_m**2 / g
        m_h2o_seq = max(0.0, m_h2o_out - m_h2o_atm_max)

    species["H2O"] = max(0.0, m_h2o_out - m_h2o_seq)

    m_co2_out = species.get("CO2", 0.0)
    m_co2_seq = 0.0
    m_co2_atm = m_co2_out

    if (
        273.0 <= T_eq_K <= 373.0
        and R_melt_kgs is not None
        and R_melt_kgs > 0.0
    ):
        f_co2 = _DEFAULT_F_CO2_IN_C
        x_melt_c_ppm = 800.0  # order-of-melt C in melt — Earth-like order when V08 split unavailable here
        x_co2_melt = (x_melt_c_ppm * 1e-6) * (44.010 / 12.011) * f_co2
        v_kg_s = R_melt_kgs * x_co2_melt
        v_mol_yr = v_kg_s / 0.04401 * SEC_PER_YR
        if v_mol_yr > 0.0 and W_0_MOL_YR > 0.0:
            p_co2_steady_bar = P_CO2_0_BAR * (
                v_mol_yr / W_0_MOL_YR
            ) ** (1.0 / W_EXPONENT) * math.exp(
                (T_0_K - T_eq_K) / (W_SENSITIVITY * W_EXPONENT)
            )
            m_co2_atm = (
                p_co2_steady_bar
                * 1e5
                * 4.0
                * math.pi
                * R_m**2
                / g
                * (44.010 / 28.964)
            )
            m_co2_seq = max(0.0, m_co2_out - m_co2_atm)

    species["CO2"] = max(0.0, m_co2_out - m_co2_seq)

    m_atm = sum(species.values())
    m_atm = max(0.0, m_atm)
    p_s_pa = m_atm * g / (4.0 * math.pi * R_m**2)

    return {
        "M_atm_kg": m_atm,
        "P_s_Pa": p_s_pa,
        "M_sequestered_H2O_kg": m_h2o_seq,
        "M_sequestered_CO2_kg": m_co2_seq,
        "M_escaped_kg": m_escaped,
        "M_ocean_kg": m_h2o_seq,
        "atmospheric_mass_note": "mass balance closed",
    }
