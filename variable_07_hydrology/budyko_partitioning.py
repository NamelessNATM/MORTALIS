# variable_07_hydrology/budyko_partitioning.py
#
# Mezentsev–Choudhury–Yang Budyko curve (ET/P ratio).

N_BUDYKO = 2.0  # dimensionless — MCY shape parameter
# ⚠️ EARTH FALLBACK — calibrated for moderate terrestrial
# catchments with vegetation. Bare rocky surface baseline.
# Varies 1.5–3.0 with biology; 2.0 used as abiotic default.
# Flag 83.


def compute_budyko_ratio(PET_kg_m2_s, P_kg_m2_s=None):
    """
    Dimensionless ET/P from dryness index DI = PET/P.
    """
    if P_kg_m2_s is None:
        return {
            "ET_over_P": None,
            "note": (
                "Absolute precipitation rate blocked — M_vol unavailable (Flag 90). "
                "ET/P ratio requires P as input."
            ),
        }

    DI = PET_kg_m2_s / P_kg_m2_s
    ET_over_P = DI / (1.0 + DI**N_BUDYKO) ** (1.0 / N_BUDYKO)
    R_run_fraction = 1.0 - ET_over_P
    return {"DI": DI, "ET_over_P": ET_over_P, "R_run_fraction": R_run_fraction}
