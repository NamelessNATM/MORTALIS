# variable_09_atmospheric_column/homopause_altitude.py
#
# Homopause altitude where K_zz = D_light (Scaffold §13.2).

from __future__ import annotations

import numpy as np

from variable_08_volatile_inventory.b12_coefficients import get_b12

_K_B = 1.381e-23
_CM_TO_M = 1.0e2


def compute_homopause_altitude_m(
    *,
    z_m: np.ndarray,
    P_arr_Pa: np.ndarray,
    T_arr_K: np.ndarray,
    K_zz_cm2_s: np.ndarray,
    dominant_light: str,
    dominant_heavy: str,
) -> float:
    """
    Bisection on discrete grid: K_zz(z) - D(z) = 0 with D = b_12 / n [m²/s].

    Uses V08 b₁₂ formalism (Hunten convention) at local T, P.
    """
    if len(z_m) != len(P_arr_Pa) or len(z_m) != len(T_arr_K) or len(z_m) != len(K_zz_cm2_s):
        raise ValueError("homopause: array length mismatch.")

    n_m = len(z_m)
    d_m2_s = np.zeros(n_m, dtype=float)
    for i in range(n_m):
        t = float(T_arr_K[i])
        p = float(P_arr_Pa[i])
        info = get_b12(dominant_light, dominant_heavy, t)
        b12_cm = info["b12_cm_inv_s_inv"]
        if b12_cm is None:
            raise RuntimeError(
                f"Rule 2: b₁₂ unavailable for pair "
                f"{dominant_light}-{dominant_heavy}: {info.get('notes')}"
            )
        b12_m = float(b12_cm) * _CM_TO_M
        n_num = p / (_K_B * t)
        d_m2_s[i] = b12_m / max(n_num, 1e-30)

    kzz_m2_s = K_zz_cm2_s * 1e-4
    diff = kzz_m2_s - d_m2_s
    if diff[0] >= 0.0:
        return float(z_m[0])
    if diff[-1] <= 0.0:
        return float(z_m[-1])
    for i in range(n_m - 1):
        if diff[i] * diff[i + 1] <= 0.0:
            # linear cross
            f = abs(diff[i]) / (abs(diff[i]) + abs(diff[i + 1]) + 1e-30)
            return float(z_m[i] * (1.0 - f) + z_m[i + 1] * f)
    return float(z_m[n_m // 2])
