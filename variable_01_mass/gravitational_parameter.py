# variable_01_mass/gravitational_parameter.py
#
# PURPOSE: Compute the standard gravitational parameter mu = G * M.
#
# Formula: mu = G * M
# Derivation: From Newton's law of universal gravitation F = GMm/r^2 and
# Newton's second law F = ma, the product GM appears as a single composite
# quantity governing all gravitational dynamics. It is more precisely
# measurable than G or M individually and appears directly in orbital
# mechanics equations (vis-viva, Kepler's third law).
# Source: Classical mechanics; confirmed universally across all gravitating
# bodies. Rule 1 Category A constant G, Category B derived quantity mu.
#
# Earth calibration:
#   M_earth = 5.972e24 kg
#   mu = 6.674e-11 * 5.972e24 = 3.986e14 m^3 s^-2  ✓

# Fundamental physical constant (Rule 1 Category A)
G = 6.674e-11  # m^3 kg^-1 s^-2


def compute_gravitational_parameter(M_kg: float) -> float:
    """
    Compute the standard gravitational parameter.

    Parameters
    ----------
    M_kg : planetary mass [kg]

    Returns
    -------
    mu [m^3 s^-2]
    """
    return G * M_kg
