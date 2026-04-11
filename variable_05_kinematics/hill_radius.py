# variable_05_kinematics/hill_radius.py
#
# PURPOSE: Compute the Hill radius — the sphere of planetary gravitational
# dominance against the host star.
#
# Formula: R_H = a * (M / (3 * M_star))^(1/3)
#
# Derivation: In the circular restricted three-body problem, the Lagrange
# points L1 and L2 define the boundary of the Roche lobe. Expanding the
# effective potential about L1/L2 for M << M_star yields the Hill radius
# as the first-order approximation. Accurate to first order for e << 1.
# Source: Hill (1878); Murray & Dermott (1999). Universal — confirmed
# across Solar System moon systems and exoplanet architectures.
#
# Downstream uses:
#   - Stable satellite orbits exist within ~0.3 to 0.5 R_H
#   - Maximum exosphere extent before atmospheric escape to the star
#   - Ring system stability boundary
#
# Earth calibration:
#   a = 1.496e11 m, M = 5.972e24 kg, M_star = 1.989e30 kg
#   R_H = 1.496e11 * (5.972e24 / (3 * 1.989e30))^(1/3)
#        = 1.496e11 * (1.001e-6)^(1/3)
#        = 1.496e11 * 0.01000 = 1.496e9 m ✓ (known ~235 Earth radii)


def compute_hill_radius(a_m: float, M_kg: float, M_star_kg: float) -> float:
    """
    Hill radius R_H [m].

    Parameters
    ----------
    a_m       : semimajor axis [m]
    M_kg      : planetary mass [kg] from Variable 01
    M_star_kg : stellar mass [kg] from Variable 03

    Returns
    -------
    R_H [m]
    """
    return a_m * (M_kg / (3.0 * M_star_kg)) ** (1.0 / 3.0)
