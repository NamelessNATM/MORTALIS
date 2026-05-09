# variable_01_5_disk_chemistry/mantle_mg_si_ratio.py
#
# FORMULA: Mg/Si_mantle = N_Mg / N_Si
#
# Mantle Mg/Si molar ratio. Determines bulk mantle mineralogy:
#   Mg/Si > 1: olivine-dominated (Earth-like, lower viscosity)
#   Mg/Si < 1: pyroxene + free SiO2-dominated (higher viscosity)
#
# Companion output for downstream V02 (future composition-dependent
# mass-radius) and V06 tectonics consumers.
#
# Earth calibration ([Mg/H] = [Si/H] = 0): Mg/Si = 1.0471


def compute_mg_si_ratio(N_Mg: float, N_Si: float) -> float:
    """Return mantle Mg/Si molar ratio."""
    return N_Mg / N_Si
