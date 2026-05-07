# variable_09_atmospheric_column/titan_tholin_anti_greenhouse.py
#
# Titan tholin shortwave transmission (anti-greenhouse skin temperature).

# ⚠️ Note 164 — Titan tholin shortwave transmission factor.
TITAN_THOLIN_TRANSMISSION = 0.45


def compute_t_skin_eff_titan(T_eq: float, f_trans: float = TITAN_THOLIN_TRANSMISSION) -> float:
    """
    T_skin_eff^4 = T_eq^4 · f_trans  →  T_skin_eff = T_eq · f_trans^(1/4)

    Titan calibration: T_eq=82 K, f_trans=0.45 → T_skin_eff ≈ 67 K
    (research stated 69 K; formula governs — Note 164).
    """
    teq = float(T_eq)
    f = float(f_trans)
    t_skin = teq * (f**0.25)
    if abs(teq - 82.0) < 1.0 and abs(f - 0.45) < 0.01:
        if not (60.0 <= t_skin <= 75.0):
            raise RuntimeError(
                f"Rule 2: Titan T_skin_eff {t_skin:.2f} K outside [60, 75] K for "
                "T_eq=82 K, f_trans=0.45 (§17)."
            )
    return t_skin
