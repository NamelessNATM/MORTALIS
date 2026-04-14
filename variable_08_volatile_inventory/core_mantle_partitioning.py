# variable_08_volatile_inventory/core_mantle_partitioning.py
#
# Core–mantle partitioning of lithophile/siderophile volatile budgets.
#
# Formula: D_i = (K_D − 1) / (1 + CMF × (K_D − 1)); X_mantle,i = X_bulk,i × (1 − D_i × CMF)
# Source: Armstrong et al. (2019), Deng et al. (2020) high-pressure experiments
# Earth calibration (P_cmb=135 GPa): C=1.89 ppm, N=1.53 ppm, S=27.66 ppm, H=0.79 ppm
# Flag 108: K_D,H=29 at Earth P_cmb — diamond anvil cell + SIMS. Lab measurement. Earth fallback.
# Flag 109: K_D,C=107 at Earth P_cmb — experimental petrology. Earth fallback.
# Flag 110: K_D,N=14 at Earth P_cmb — experimental petrology. Earth fallback.
# Flag 111: K_D,S=100 at Earth P_cmb — thermodynamic models. Earth fallback.
# Flag 112: K_D,H=1 at Mars P_cmb (14 GPa) — H approaches neutral below 20 GPa. Lab data.
# Flag 113: K_D,C=500 at Mars P_cmb (14 GPa) — C inversely pressure dependent. Lab data.
# Flag 114: K_D,N and K_D,S pressure scaling at Mars P_cmb not resolved. Earth anchor values
#           used for all pressures below Earth P_cmb. Earth fallback pending low-pressure data.

import math

P_EARTH_PA = 135.0e9  # Pa — Earth CMB pressure anchor
P_MARS_PA = 14.0e9  # Pa — Mars CMB pressure anchor

# K_D at Earth anchor (135 GPa)
KD_EARTH = {"H": 29.0, "C": 107.0, "N": 14.0, "S": 100.0}

# K_D at Mars anchor (14 GPa) — ⚠️ Flags 112, 113, 114
KD_MARS = {"H": 1.0, "C": 500.0, "N": 14.0, "S": 100.0}  # N, S: Flag 114 fallback


def _interpolate_kd(element: str, P_cmb_Pa: float) -> float:
    """Log-linear interpolation of K_D in pressure space between Mars and Earth anchors."""
    p = max(P_MARS_PA, min(P_EARTH_PA, P_cmb_Pa))
    if P_cmb_Pa >= P_EARTH_PA:
        return KD_EARTH[element]
    if P_cmb_Pa <= P_MARS_PA:
        return KD_MARS[element]
    log_p = math.log10(p)
    t = (log_p - math.log10(P_MARS_PA)) / (
        math.log10(P_EARTH_PA) - math.log10(P_MARS_PA)
    )
    kd_m = KD_MARS[element]
    kd_e = KD_EARTH[element]
    log_kd = math.log10(kd_m) + t * (math.log10(kd_e) - math.log10(kd_m))
    return 10.0 ** log_kd


def _kd_to_di(K_D: float, CMF: float) -> float:
    return (K_D - 1.0) / (1.0 + CMF * (K_D - 1.0))


def compute_core_partitioning(X_bulk: dict, CMF: float, P_cmb_Pa: float) -> dict:
    """Partition bulk ppm into mantle after core segregation. Ar follows H lithophile proxy."""
    out = {}
    for el, key_bulk, key_m in (
        ("H", "X_bulk_H_ppm", "X_mantle_H_ppm"),
        ("C", "X_bulk_C_ppm", "X_mantle_C_ppm"),
        ("N", "X_bulk_N_ppm", "X_mantle_N_ppm"),
        ("S", "X_bulk_S_ppm", "X_mantle_S_ppm"),
    ):
        kd = _interpolate_kd(el, P_cmb_Pa)
        di = _kd_to_di(kd, CMF)
        xb = X_bulk[key_bulk]
        out[key_m] = xb * (1.0 - di * CMF)

    # Argon: lithophile carrier not in K_D set; use H-like partitioning coefficient
    kd_ar = _interpolate_kd("H", P_cmb_Pa)
    di_ar = _kd_to_di(kd_ar, CMF)
    out["X_mantle_Ar_ppm"] = X_bulk["X_bulk_Ar_ppm"] * (1.0 - di_ar * CMF)

    return out
