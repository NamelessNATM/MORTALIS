# variable_09_atmospheric_column/t_p_profile.py
#
# Vertical T(P) on log-spaced pressure grid (Scaffold §11).

from __future__ import annotations

import math
import numpy as np

_K_B = 1.381e-23


def compute_t_p_profile(
    *,
    P_s_Pa: float,
    T_surface_K: float,
    T_skin_K: float,
    tau_zero: float,
    tau_rc: float,
    beta: float,
    n: float,
    g_m_s2: float,
    m_bar_kg_mol: float,
    T_exo_K: float | None,
    D: float = 1.5,
    n_layers: int = 50,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Log-spaced P from P_s to 1 Pa; convective below P(τ_rc), radiative above.

    Thermosphere: Bates profile with T_mesopause ≈ T_skin (⚠️ Note 170).
    """
    if P_s_Pa <= 0.0:
        raise ValueError("P_s must be positive.")
    p_arr = np.logspace(math.log10(P_s_Pa), math.log10(1.0), n_layers)
    p_rc = float(P_s_Pa) * (float(tau_rc) / float(tau_zero)) ** (1.0 / float(n))
    r_gas = _K_B / float(m_bar_kg_mol)  # J/(kg K) specific gas constant ~ R_univ/m_bar

    # Hydrostatic altitude (m), z[0]=0 at surface
    z_arr = np.zeros(n_layers, dtype=float)
    for i in range(1, n_layers):
        p0, p1 = float(p_arr[i - 1]), float(p_arr[i])
        # mid-layer T for scale height (iterate once with previous T)
        t_mid = float(T_surface_K) * (math.sqrt(p0 * p1) / float(P_s_Pa)) ** float(beta)
        h = r_gas * t_mid / float(g_m_s2)
        z_arr[i] = z_arr[i - 1] + h * math.log(p0 / p1)

    t_arr = np.zeros(n_layers, dtype=float)
    for i in range(n_layers):
        p = float(p_arr[i])
        if p > p_rc:
            t_arr[i] = float(T_surface_K) * (p / float(P_s_Pa)) ** float(beta)
        else:
            tau_p = float(tau_zero) * (p / float(P_s_Pa)) ** float(n)
            t_arr[i] = float(T_skin_K) * (1.0 + float(D) * tau_p) ** 0.25

    # ⚠️ Note 170 — mesopause temperature approximation (T_skin as T_mesopause)
    if T_exo_K is not None and math.isfinite(float(T_exo_K)):
        t_exo = float(T_exo_K)
        t_meso = float(T_skin_K)
        # Mesopause height: P ≈ 100 Pa (procedural engine level; not from cascade)
        p_meso_pa = 100.0
        idx_m = int(np.argmin(np.abs(p_arr - p_meso_pa)))
        z_meso = float(z_arr[idx_m])
        # ⚠️ EMPIRICAL — Note 170b Bates e-folding scale [1/m]; Earth-thermosphere
        # order-of-magnitude; extrasolar applicability not derived.
        s_bates = 2.0e-4
        for i in range(n_layers):
            if float(z_arr[i]) > z_meso:
                t_arr[i] = t_exo - (t_exo - t_meso) * math.exp(
                    -s_bates * (float(z_arr[i]) - z_meso)
                )
    return p_arr, t_arr, z_arr
