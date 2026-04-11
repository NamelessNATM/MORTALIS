# variable_02_composition/mean_density.py
#
# Mean (bulk) density of a spherical body.
#
# Formula: rho_mean = M / ((4/3) * pi * R^3)
# Derivation: Definition — mass equals density times spherical volume.
# Rule 1 Category B.

import math

PI = math.pi


def compute_mean_density(M_kg: float, R_m: float) -> float:
    """
    Mean density rho_mean [kg/m^3].

    Earth calibration: M = 5.972e24 kg, R = 6.371e6 m → rho_mean = 5,514 kg/m^3
    (known value 5,514 kg/m^3 ✓).
    """
    volume = (4.0 / 3.0) * PI * (R_m**3)
    return M_kg / volume
