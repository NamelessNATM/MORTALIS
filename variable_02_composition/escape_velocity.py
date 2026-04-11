# variable_02_composition/escape_velocity.py
#
# Escape speed at the surface.
#
# Formula: v_e = sqrt(2 * G * M / R)
# Derivation: Energy conservation — kinetic energy equals gravitational binding
# at escape. Rule 1 Category B.

import math

G = 6.674e-11


def compute_escape_velocity(M_kg: float, R_m: float) -> float:
    """
    Escape velocity v_e [m/s].

    Earth calibration: M = 5.972e24 kg, R = 6.371e6 m → v_e = 11,186 m/s
    (known value 11,186 m/s ✓).
    """
    return math.sqrt(2.0 * G * M_kg / R_m)
