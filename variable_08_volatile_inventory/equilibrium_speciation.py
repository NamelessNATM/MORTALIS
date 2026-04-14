# variable_08_volatile_inventory/equilibrium_speciation.py
#
# High-temperature volcanic gas equilibrium speciation from fO2 and NIST-JANAF K(T).
#
# Formula: log10(K_i) = A_i + B_i/T; ratios from K_i × fO2^0.5
# Source: NIST-JANAF thermochemical tables. Valid 1200–2500 K.
# Earth calibration (T=1600K, ΔIW=+3.5): H2O/H2=159, CO2/CO=22.6 ✓
# Mars calibration (T=1500K, ΔIW=+1.0): H2O/H2=8.14, CO2/CO=1.42 ✓
# Flag 123: K1–K6 A, B coefficients — NIST-JANAF. Universal molecular thermodynamics.
#           Valid 1200–2500 K only. Model applicability limit outside this range.

import math

from variable_08_volatile_inventory.oxygen_fugacity import A_IW, B_IW

# log10(K) = A + B/T — Flag 123, NIST-JANAF, valid 1200–2500 K
K_COEFFS = {
    "K1_H2O_H2": {"A": -2.324, "B": 12628.0},
    "K2_CO2_CO": {"A": -4.517, "B": 14780.0},
    "K3_CH4": {"A": -0.277, "B": 41912.0},
    "K4_SO2": {"A": -3.713, "B": 15501.0},
    "K5_H2S": {"A": -0.287, "B": 11552.0},
    "K6_NH3": {"A": -5.173, "B": 2397.0},
}


def _log10_k(name: str, T_m_K: float) -> float:
    c = K_COEFFS[name]
    return c["A"] + c["B"] / T_m_K


def compute_outgassing_speciation(
    T_m_K: float | None,
    log10_fO2: float | None,
    X_mantle: dict,
) -> dict:
    """
    Mole-fraction speciation for major volcanic gases; keys match V07 SPECIES_DATA.
    """
    if T_m_K is None or log10_fO2 is None:
        return {"speciation": None, "speciation_note": "fO2 or T_m unavailable"}

    log10_fo2_iw = A_IW - B_IW / T_m_K
    delta_iw = log10_fO2 - log10_fo2_iw

    fo2_half = 10.0 ** (log10_fO2 / 2.0)

    log_k1 = _log10_k("K1_H2O_H2", T_m_K)
    log_k2 = _log10_k("K2_CO2_CO", T_m_K)
    log_k4 = _log10_k("K4_SO2", T_m_K)
    log_k5 = _log10_k("K5_H2S", T_m_K)
    log_k6 = _log10_k("K6_NH3", T_m_K)

    k1 = 10.0 ** log_k1
    k2 = 10.0 ** log_k2
    k4 = 10.0 ** log_k4
    k5 = 10.0 ** log_k5
    k6 = 10.0 ** log_k6

    r_h2o_h2 = k1 * fo2_half
    r_co2_co = k2 * fo2_half

    h2o_h2_ratio = r_h2o_h2
    co2_co_ratio = r_co2_co

    # Elemental mole pools (mol per kg mantle, relative scale)
    w_h = max(X_mantle.get("X_mantle_H_ppm", 0.0) * 1e-6 / 0.001008, 1e-30)
    w_c = max(X_mantle.get("X_mantle_C_ppm", 0.0) * 1e-6 / 0.012011, 1e-30)
    w_n = max(X_mantle.get("X_mantle_N_ppm", 0.0) * 1e-6 / 0.014007, 1e-30)
    w_s = max(X_mantle.get("X_mantle_S_ppm", 0.0) * 1e-6 / 0.032065, 1e-30)

    # Carbon: CO2 vs CO
    r_c = r_co2_co
    n_co2 = w_c * r_c / (1.0 + r_c)
    n_co = w_c / (1.0 + r_c)

    # Sulfur: SO2 vs H2S
    r_sh = (k4 * fo2_half) / max(k5, 1e-99)
    n_so2 = w_s * r_sh / (1.0 + r_sh)
    n_h2s = w_s / (1.0 + r_sh)

    # Methane suppressed at oxidising conditions
    n_ch4 = 0.0
    note_parts = []
    if delta_iw > 0.0:
        note_parts.append("CH4 and NH3 suppressed at ΔIW>0")

    # Nitrogen: N2 vs NH3 from ΔIW relative to −1
    if delta_iw >= -1.0:
        n_nh3 = 0.0
        n_n2 = w_n / 2.0
        note_parts.append("N as N2 (ΔIW≥−1)")
    else:
        r_n = k6 * fo2_half
        n_nh3 = w_n * r_n / (1.0 + r_n)
        n_n2 = (w_n - n_nh3) / 2.0
        note_parts.append("NH3 correction via K6 (ΔIW<−1)")

    if delta_iw > 0.0:
        n_nh3 = 0.0
        n_n2 = w_n / 2.0

    # Hydrogen budget: H2O / H2 after other hydrides
    h_in_h2s = 2.0 * n_h2s
    h_in_ch4 = 4.0 * n_ch4
    h_in_nh3 = 3.0 * n_nh3
    h_remain = max(w_h - h_in_h2s - h_in_ch4 - h_in_nh3, 1e-30)

    r_hw = r_h2o_h2
    n_h2o = h_remain * r_hw / (2.0 * (1.0 + r_hw))
    n_h2 = h_remain / (2.0 * (1.0 + r_hw))

    moles = {
        "H2O": n_h2o,
        "CO2": n_co2,
        "CO": n_co,
        "H2": n_h2,
        "N2": max(n_n2, 0.0),
        "SO2": n_so2,
        "H2S": n_h2s,
        "CH4": n_ch4,
        "NH3": max(n_nh3, 0.0),
    }

    total = sum(moles.values())
    if total <= 0.0:
        return {
            "speciation": None,
            "H2O_H2_ratio": h2o_h2_ratio,
            "CO2_CO_ratio": co2_co_ratio,
            "speciation_note": "zero mole pools",
        }

    speciation = {}
    for sp, nm in moles.items():
        xf = nm / total
        if xf > 1e-15:
            speciation[sp] = xf

    return {
        "speciation": speciation,
        "H2O_H2_ratio": h2o_h2_ratio,
        "CO2_CO_ratio": co2_co_ratio,
        "speciation_note": "; ".join(note_parts),
    }
