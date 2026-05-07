# variable_09_atmospheric_column/eddy_diffusion_kzz.py
#
# Eddy diffusion K_zz troposphere + mesosphere (Scaffold §13.1).

from __future__ import annotations

import math
from typing import Mapping

import numpy as np

_K_B = 1.381e-23


def compute_kzz_profile_cm2_s(
    *,
    P_arr_Pa: np.ndarray,
    T_arr_K: np.ndarray,
    P_tropopause_Pa: float,
    m_bar_kg_mol: float,
    g_m_s2: float,
    T_surface_K: float,
    albedo_final: float,
    F_mean_W_m2: float,
) -> tuple[np.ndarray, float]:
    """
    Return (K_zz_cm2_s array same length as P, K_zz_ref_cm2_s at mesopause).

    Troposphere P > P_tropopause: ⚠️ Note 176 mixing-length closure.
    Above: ⚠️ Note 177 Lindzen (1981) n(z)^(-1/2) scaling vs reference level.
    """
    nlev = len(P_arr_Pa)
    kzz = np.zeros(nlev, dtype=float)
    r_gas = _K_B / float(m_bar_kg_mol)
    # crude: use planetary mean absorbed shortwave as scale for convective driving
    f_conv = max(1.0, float(F_mean_W_m2) * (1.0 - float(albedo_final)) * 0.25)

    idx_ref = None
    for i in range(nlev):
        p = float(P_arr_Pa[i])
        t = max(50.0, float(T_arr_K[i]))
        h = r_gas * t / float(g_m_s2)
        r_univ = 8.314462618  # J/(mol K)
        rho = p * float(m_bar_kg_mol) / (r_univ * t)
        c_p_mass = 1005.0  # ⚠️ EMPIRICAL — Note 176b air c_p [J/kg/K] order-of-magnitude
        if p >= P_tropopause_Pa:
            w_conv = (
                float(g_m_s2)
                * h
                * f_conv
                / (max(rho, 1e-6) * c_p_mass * t + 1e-30)
            ) ** (1.0 / 3.0)
            tau_conv = h / max(w_conv, 1e-6)
            kzz_m2_s = h * h / tau_conv
            kzz[i] = kzz_m2_s * 1e4  # m^2/s -> cm^2/s
            idx_ref = i
        else:
            if idx_ref is None:
                idx_ref = max(0, i - 1)
            p_ref = float(P_arr_Pa[idx_ref])
            t_ref = float(T_arr_K[idx_ref])
            n_ref = p_ref / (_K_B * t_ref)
            n_z = p / (_K_B * t)
            # ⚠️ Note 177 — K_ref ~1e5 cm^2/s at Earth mesopause (order-of-magnitude)
            k_ref_cm2_s = 1.0e5
            kzz[i] = k_ref_cm2_s * (n_ref / max(n_z, 1e-30)) ** 0.5
    kzz_ref = float(kzz[-1]) if nlev else 0.0
    return kzz, kzz_ref
