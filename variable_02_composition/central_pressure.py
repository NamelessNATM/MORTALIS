# variable_02_composition/central_pressure.py
#
# Approximate central pressure for a uniform-density sphere.
#
# Formula: P_c = (3 * G * M^2) / (8 * pi * R^4)
# Derivation: Hydrostatic equation dP/dr = -rho*g(r) integrated for uniform rho.
# Rule 1 Category B with caveat (real bodies are differentiated).
#
# ⚠️ Flag 11: Uniform density assumption. Real interior is differentiated;
# actual P_c is higher. Approximate lower bound only.
#
# Earth calibration: M = 5.972e24 kg, R = 6.371e6 m → P_c ≈ 1.71e11 Pa
# (~171 GPa). Known Earth central pressure ~364 GPa — factor-of-2
# underestimate expected from uniform-density approximation.

import math

G = 6.674e-11
PI = math.pi


def compute_central_pressure(M_kg: float, R_m: float) -> float:
    """Central pressure P_c [Pa] (uniform-density sphere approximation)."""
    return (3.0 * G * M_kg * M_kg) / (8.0 * PI * (R_m**4))
