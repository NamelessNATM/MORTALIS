# variable_09_atmospheric_column/gas_envelope_internal_heat.py
#
# Kelvin–Helmholtz internal flux scaling for gas giants / massive envelopes.

import math

# ⚠️ Note 165 — Jupiter F_int normalization point (Hanel et al. 1981).
F_INT_JUPITER_W_PER_M2 = 5.4
M_JUPITER_KG = 1.898e27
TAU_JUPITER_GYR = 4.5

# ⚠️ Note 166 — Saturn helium-rain supplement.
F_INT_HELIUM_RAIN_SATURN_W_PER_M2 = 0.4
SATURN_HELIUM_RAIN_MASS_RANGE_KG = (3e26, 1e27)


def compute_f_int(M_kg: float, age_Gyr: float) -> float:
    """
    Kelvin-Helmholtz internal flux scaling.

    F_int = F_int_Jupiter · (age/tau_Jupiter)^(-1/3) · (M/M_Jupiter)^1

    ⚠️ Note 167 — Valid mass range >0.1 M_Jup (~30 M_earth).
    """
    M_EARTH = 5.972e24
    if M_kg < 30.0 * M_EARTH:
        raise ValueError(
            f"F_int formula not valid below ~30 M_earth; M_kg={M_kg:.2e}. "
            'Sub-Neptune cores require separate scaling (Note 167).'
        )
    f_kh = (
        F_INT_JUPITER_W_PER_M2
        * (float(age_Gyr) / TAU_JUPITER_GYR) ** (-1.0 / 3.0)
        * (float(M_kg) / M_JUPITER_KG)
    )
    lo, hi = SATURN_HELIUM_RAIN_MASS_RANGE_KG
    if lo <= M_kg <= hi:
        f_kh += F_INT_HELIUM_RAIN_SATURN_W_PER_M2
    return float(f_kh)


def compute_f_int_sub_neptune_safe(M_kg: float, age_Gyr: float) -> tuple[float | None, dict | None]:
    """
    Wrapper: returns (None, flag dict) below 30 M_earth; otherwise (F_int, None).
    """
    M_EARTH = 5.972e24
    if M_kg < 30.0 * M_EARTH:
        return None, {"flag": 167, "note": "F_int scaling not valid below ~30 M_Earth."}
    return compute_f_int(M_kg, age_Gyr), None
