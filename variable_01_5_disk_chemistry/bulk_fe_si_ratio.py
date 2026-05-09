# variable_01_5_disk_chemistry/bulk_fe_si_ratio.py
#
# FORMULA: Fe/Si_bulk = (N_Fe × μ_Fe) / (N_Si × μ_Si)
#
# Bulk planetary iron-to-silicon mass ratio. Pre-partitioning, immune
# to χ_ox uncertainty. Primary structural diagnostic for comparative
# exoplanetology.
#
# Earth calibration: Fe/Si = (0.8710 × 55.845) / (1.000 × 28.085)
#                          = 1.7320

from variable_01_5_disk_chemistry.solar_abundance_constants import (
    MU_FE_GMOL,
    MU_SI_GMOL,
)


def compute_fe_si_ratio(N_Fe: float, N_Si: float) -> float:
    """Return bulk Fe/Si mass ratio."""
    return (N_Fe * MU_FE_GMOL) / (N_Si * MU_SI_GMOL)
