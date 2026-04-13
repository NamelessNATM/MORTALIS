# variable_07_hydrology/precipitation_energy_limit.py
#
# Energy-limited potential evapotranspiration (PET) ceiling.

from variable_07_hydrology.volatile_phase_state import SPECIES_DATA

DH_VAP_H2O = 40650.0  # J/mol — latent heat of vaporisation at 373 K
# ⚠️ EARTH-MEASURED MOLECULAR CONSTANT — NIST.
# Intrinsic to H2O; universal.
# Flag 78.

SECONDS_PER_YEAR = 3.156e7


def compute_pet(
    F_mean_Wm2: float,
    albedo_final: float,
    dominant_volatile: str = "H2O",
):
    """
    PET upper bound from net radiation and latent heat of vaporisation.
    """
    if dominant_volatile != "H2O":
        return None

    R_n = F_mean_Wm2 * (1.0 - albedo_final)
    M_mol = SPECIES_DATA["H2O"]["molar_mass"]
    lambda_J_kg = DH_VAP_H2O / M_mol
    PET_kg_m2_s = R_n / lambda_J_kg
    PET_mm_yr = PET_kg_m2_s * 1000.0 * SECONDS_PER_YEAR
    return {
        "PET_kg_m2_s": PET_kg_m2_s,
        "PET_mm_yr": PET_mm_yr,
        "R_n_Wm2": R_n,
    }
