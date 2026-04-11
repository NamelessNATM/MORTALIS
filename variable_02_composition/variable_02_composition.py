# variable_02_composition/variable_02_composition.py
#
# Variable 02: Bulk Composition & Radius
# Entry point. Imports sub-functions. Assembles outputs. Contains no physics
# beyond orchestration.

import logging

from variable_02_composition.regime_classifier import classify_regime
from variable_02_composition.mass_radius_rocky import compute_radius_rocky
from variable_02_composition.mass_radius_subneptune import compute_radius_subneptune
from variable_02_composition.mass_radius_gasgiant import compute_radius_gasgiant
from variable_02_composition.surface_gravity import compute_surface_gravity
from variable_02_composition.escape_velocity import compute_escape_velocity
from variable_02_composition.central_pressure import compute_central_pressure
from variable_02_composition.mean_density import compute_mean_density

_LOG = logging.getLogger(__name__)


def run(seed: int, M_kg: float, mu: float) -> dict:
    """
    Execute Variable 02: classify regime, compute radius and bulk quantities.

    Parameters
    ----------
    seed : int
        Cascade seed (reserved for future stochastic composition inputs).
    M_kg : float
        Planetary mass [kg] from Variable 01.
    mu : float
        Standard gravitational parameter [m^3 s^-2] from Variable 01.

    Returns
    -------
    dict with keys:
        'regime'           — one of rocky, sub_neptune, gas_giant, brown_dwarf
        'R_m'              — radius [m], or None if brown_dwarf
        'rho_mean_kg_m3'   — mean density [kg/m^3], or None if brown_dwarf
        'g_m_s2'           — surface gravity [m/s^2], or None if brown_dwarf
        'v_e_m_s'          — escape velocity [m/s], or None if brown_dwarf
        'P_c_Pa'           — approximate central pressure [Pa], or None if brown_dwarf
    """
    regime = classify_regime(M_kg)

    if regime == "brown_dwarf":
        _LOG.info(
            "Regime brown_dwarf: mass exceeds planetary simulation domain; "
            "radius and derived bulk quantities not computed (R = None)."
        )
        return {
            "regime": regime,
            "R_m": None,
            "rho_mean_kg_m3": None,
            "g_m_s2": None,
            "v_e_m_s": None,
            "P_c_Pa": None,
        }

    if regime == "rocky":
        R_m = compute_radius_rocky(M_kg)
    elif regime == "sub_neptune":
        R_m = compute_radius_subneptune(M_kg)
    else:
        R_m = compute_radius_gasgiant(M_kg)

    rho_mean = compute_mean_density(M_kg, R_m)
    g = compute_surface_gravity(M_kg, R_m)
    v_e = compute_escape_velocity(M_kg, R_m)
    p_c = compute_central_pressure(M_kg, R_m)

    return {
        "regime": regime,
        "R_m": R_m,
        "rho_mean_kg_m3": rho_mean,
        "g_m_s2": g,
        "v_e_m_s": v_e,
        "P_c_Pa": p_c,
    }
