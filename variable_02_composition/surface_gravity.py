# variable_02_composition/surface_gravity.py
#
# Surface gravity from Newtonian gravity at the surface.
#
# Formula: g = G * M / R^2
# Derivation: Newton's law of universal gravitation + F = ma at the surface.
# Rule 1 Category B derived quantity.

G = 6.674e-11


def compute_surface_gravity(M_kg: float, R_m: float) -> float:
    """
    Surface gravity g [m/s^2].

    Earth calibration: M = 5.972e24 kg, R = 6.371e6 m → g ≈ 9.82 m/s^2
    (known 9.807 m/s^2; ~0.1% from constant rounding).
    """
    return G * M_kg / (R_m * R_m)
