# variable_03_stellar/xuv_luminosity.py
#
# Ribas et al. (2005) XUV saturation and power-law decay ("Sun in Time").
# f_sat, t_sat, and β are empirically fitted. No numbered cascade flag applies.

"""XUV luminosity fraction vs age (Ribas et al. 2005)."""

from __future__ import annotations

_F_SAT = 1e-3
_T_SAT_GYR = 0.1
_BETA_XUV = -1.23


def compute_xuv(age_gyr: float, l_star_w: float) -> tuple[float, float]:
    """
    XUV luminosity fraction and XUV luminosity [W].

    If age ≤ t_sat: L_XUV / L_bol = f_sat.
    If age > t_sat: fraction = f_sat · (age / t_sat)^β.

    Solar calibration: age = 4.57 Gyr → fraction ≈ 9.1e-6, within 10⁻⁶–10⁻⁵.
    """
    if age_gyr < 0.0:
        raise ValueError("age_gyr must be non-negative.")
    if l_star_w < 0.0:
        raise ValueError("l_star_w must be non-negative.")

    if age_gyr <= _T_SAT_GYR:
        frac = _F_SAT
    else:
        frac = _F_SAT * ((age_gyr / _T_SAT_GYR) ** _BETA_XUV)
    return frac, frac * l_star_w
