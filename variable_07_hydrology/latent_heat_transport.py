# variable_07_hydrology/latent_heat_transport.py
#
# Upper bound on latent heat transport from global PET ceiling.

import math

from variable_07_hydrology.volatile_phase_state import SPECIES_DATA

DH_VAP_H2O = 40650.0  # J/mol — same as precipitation_energy_limit.py
# ⚠️ EARTH-MEASURED MOLECULAR CONSTANT
# Flag 78.


def compute_latent_heat_transport(PET_kg_m2_s: float, R_m: float):
    """
    Q_latent_max = λ * PET * (4π R²).
    """
    M_mol = SPECIES_DATA["H2O"]["molar_mass"]
    lambda_J_kg = DH_VAP_H2O / M_mol
    A_planet = 4.0 * math.pi * R_m**2
    Q_latent_max_W = lambda_J_kg * PET_kg_m2_s * A_planet
    return {
        "Q_latent_max_W": Q_latent_max_W,
        "lambda_J_kg": lambda_J_kg,
        "note": "Upper bound on latent heat transport. Actual flux requires circulation model.",
    }
