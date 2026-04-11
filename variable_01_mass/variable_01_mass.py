# variable_01_mass/variable_01_mass.py
#
# Variable 01: Planetary Mass
# Entry point. Imports sub-functions. Assembles outputs. Contains no physics.
#
# Cascade outputs:
#   M_kg  — planetary mass [kg]
#   mu    — standard gravitational parameter [m^3 s^-2]
#
# Deferred outputs (require radius R from Variable 02):
#   g     — surface gravity        -> moves to Variable 02
#   v_e   — escape velocity        -> moves to Variable 02
#   P_c   — central pressure       -> moves to Variable 02
#
# Deferred outputs (require stellar mass and semimajor axis):
#   R_H   — Hill radius            -> moves to Variable 05

from variable_01_mass.mass_sampler import sample_mass
from variable_01_mass.gravitational_parameter import compute_gravitational_parameter


def run(seed: int) -> dict:
    """
    Execute Variable 01: sample planetary mass from seed and compute
    gravitational parameter.

    Parameters
    ----------
    seed : integer seed (from main.py cascade)

    Returns
    -------
    dict with keys:
        'M_kg' : planetary mass [kg]
        'mu'   : standard gravitational parameter [m^3 s^-2]
    """
    M_kg = sample_mass(seed)
    mu   = compute_gravitational_parameter(M_kg)

    return {
        'M_kg': M_kg,
        'mu':   mu,
    }
