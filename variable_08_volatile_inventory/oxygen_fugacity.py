# variable_08_volatile_inventory/oxygen_fugacity.py
#
# Mantle oxygen fugacity relative to iron–wüstite buffer.
#
# Formula: ΔIW = 2.54 × log10(P_cmb_Pa/1e9) − 1.91; IW buffer: log10(fO2,IW) = 6.776 − 27215/T
# Source: Armstrong et al. (2019), Deng et al. (2020); O'Neill (1987)
# Earth calibration: P_cmb=135 GPa → ΔIW=+3.50 ✓
# Mars calibration: P_cmb=14 GPa → ΔIW=+1.00 ✓
# Vesta calibration: P_cmb=1 GPa → ΔIW=−1.91 ✓
# Flag 121: Coefficients 2.54 and −1.91 — Armstrong et al. (2019), Deng et al. (2020).
#           Confirmed Earth, Mars, Vesta. Multi-body confirmed.
# Flag 122: No saturation above ~200 GPa. Extrapolation beyond experimental dataset.
#           Model applicability limit.

import math

A_FO2 = 2.54  # ⚠️ Flag 121
B_FO2 = -1.91  # ⚠️ Flag 121
A_IW = 6.776  # O'Neill (1987) — multi-body confirmed
B_IW = 27215.0  # O'Neill (1987)


def compute_oxygen_fugacity(P_cmb_Pa: float, T_m_K: float | None) -> dict:
    """ΔIW offset and absolute fO2 at mantle temperature T_m_K."""
    if T_m_K is None or T_m_K <= 0.0:
        return {"delta_IW": None, "log10_fO2": None, "fO2": None}

    delta_iw = A_FO2 * math.log10(P_cmb_Pa / 1e9) + B_FO2
    log10_fo2_iw = A_IW - B_IW / T_m_K
    log10_fo2 = log10_fo2_iw + delta_iw
    fo2 = 10.0 ** log10_fo2
    return {
        "delta_IW": delta_iw,
        "log10_fO2_IW": log10_fo2_iw,
        "log10_fO2": log10_fo2,
        "fO2": fo2,
    }
