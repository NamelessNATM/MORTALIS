# variable_04_atmosphere/variable_04_atmosphere.py
#
# Variable 04: Atmosphere
# Entry point. Imports sub-functions. Assembles outputs. Contains no physics.
#
# Two-pass architecture for T_exo / composition circularity:
#   Pass 1: assign m_mean from regime. Compute T_exo. Evaluate lambda per species.
#           Classify atmosphere and composition.
#   Pass 2: if dominant species for the Pass-1 regime does not meet Jeans
#           retention threshold, strip it. Recompute m_mean from retained
#           species. Recompute T_exo with refined m_mean.
#
# Cascade inputs required:
#   v01: M_kg
#   v02: regime, R_m, g_m_s2, v_e_m_s
#   v03: age_Gyr
#   v05: F_XUV_W_m2, T_eq_K, M_dot_kg_s
#
# Outputs:
#   T_exo_K       — exobase temperature [K] or None (dwarf/brown_dwarf)
#   jeans         — lambda per species and retention flag, or None
#   atm_class     — atmospheric class string
#   composition   — dominant composition string
#   P_s_Pa        — surface pressure [Pa] or None if blocked or no atmosphere
#   gamma_d_K_m   — dry adiabatic lapse rate [K/m]
#   H_m           — scale height [m] or None
#   h_identity    — dominant hydrogen species at exobase (hydrogen_identity)
#   notes         — flag summary string

from variable_04_atmosphere.exobase_temperature import (
    compute_exobase_temperature,
    M_MEAN_ROCKY_KG,
    M_MEAN_GIANT_KG,
)
from variable_04_atmosphere.hydrogen_identity import select_dominant_hydrogen
from variable_04_atmosphere.jeans_parameter import (
    compute_all_species,
    SPECIES_MASS_KG,
)
from variable_04_atmosphere.regime_classifier import (
    attach_photochemically_limited_species,
    classify_atmosphere,
)
from variable_04_atmosphere.surface_pressure import get_surface_pressure
from variable_04_atmosphere.lapse_rate import compute_lapse_rate
from variable_04_atmosphere.scale_height import compute_scale_height


def _dominant_species_retained(regime: str, jeans: dict) -> bool:
    """
    Return True if the dominant species for a regime meets Jeans retention.
    Used to decide whether Pass 2 refinement is needed.

    Gas giant / sub-Neptune: dominant species is H (lightest, hardest to retain).
    Rocky: dominant species are N2 and CO2.
    """
    if regime in ('gas_giant', 'sub_neptune'):
        return jeans.get('H', {}).get('retained', False)
    return (jeans.get('N2', {}).get('retained', False) and
            jeans.get('CO2', {}).get('retained', False))


def _refined_m_mean(jeans: dict) -> float:
    """
    Pass-2 mean molecular mass: mass of lightest retained species,
    or M_MEAN_ROCKY_KG if nothing is retained (atmosphere stripped).
    """
    for species in ('H', 'He', 'O', 'H2O', 'N2', 'CO2'):
        if jeans.get(species, {}).get('retained', False):
            return SPECIES_MASS_KG[species]
    return M_MEAN_ROCKY_KG


def run(seed: int,
        v01: dict,
        v02: dict,
        v03: dict,
        v05: dict) -> dict:
    """
    Execute Variable 04: atmosphere classification and structure.

    Parameters
    ----------
    seed : int — cascade seed (reserved for future stochastic inputs)
    v01  : dict — output of variable_01_mass.run()
    v02  : dict — output of variable_02_composition.run()
    v03  : dict — output of variable_03_stellar.run()
    v05  : dict — output of variable_05_kinematics.run()

    Returns
    -------
    dict with keys: T_exo_K, jeans, atm_class, composition,
                    P_s_Pa, gamma_d_K_m, H_m, h_identity, notes
    """
    M_kg       = v01['M_kg']
    regime     = v02['regime']
    R_m        = v02['R_m']
    g_m_s2     = v02['g_m_s2']
    v_e_m_s    = v02['v_e_m_s']
    age_Gyr    = v03['age_Gyr']
    F_XUV      = v05['F_XUV_W_m2']
    T_eq_K     = v05['T_eq_K']
    M_dot_kg_s = v05['M_dot_kg_s']

    # Brown dwarf — outside planetary atmosphere domain
    if regime == 'brown_dwarf' or R_m is None:
        return {
            'T_exo_K':     None,
            'jeans':       None,
            'atm_class':   'none',
            'composition': 'none',
            'P_s_Pa':      None,
            'gamma_d_K_m': 0.0,
            'H_m':         None,
            'h_identity':  select_dominant_hydrogen(None),
            'notes':       'Brown dwarf — outside planetary atmosphere domain.',
        }

    # Dwarf — no continuum atmosphere; conduction model does not apply
    if regime == 'dwarf':
        return {
            'T_exo_K':     None,
            'jeans':       None,
            'atm_class':   'none',
            'composition': 'none',
            'P_s_Pa':      0.0,
            'gamma_d_K_m': 0.0,
            'H_m':         None,
            'h_identity':  select_dominant_hydrogen(None),
            'notes':       'Dwarf regime; gravity insufficient to retain any '
                           'species. Conduction model does not apply.',
        }

    # --- Pass 1: regime-default m_mean ---
    T_exo_pass1 = compute_exobase_temperature(F_XUV, g_m_s2, T_eq_K, regime)
    jeans_pass1 = compute_all_species(v_e_m_s, T_exo_pass1)

    # --- Pass 2: refine m_mean if dominant species does not survive ---
    if not _dominant_species_retained(regime, jeans_pass1):
        m_mean_refined = _refined_m_mean(jeans_pass1)
        T_exo = compute_exobase_temperature(
            F_XUV, g_m_s2, T_eq_K, regime, m_mean_kg=m_mean_refined
        )
        jeans = compute_all_species(v_e_m_s, T_exo)
        pass2_applied = True
    else:
        T_exo = T_exo_pass1
        jeans = jeans_pass1
        pass2_applied = False

    h_identity = select_dominant_hydrogen(T_exo)

    atm = classify_atmosphere(regime, jeans, M_kg, M_dot_kg_s, age_Gyr)
    # H2S/SO2: Flag 154 — attach for all rocky atm classes that carry a Jeans
    # table (secondary_possible per spec; exosphere_only shares the same
    # outgassed species and needs the same V04 markers for V08 escape).
    if regime == "rocky" and atm["atm_class"] in (
        "secondary_possible",
        "exosphere_only",
    ):
        jeans = attach_photochemically_limited_species(jeans)

    P_s     = get_surface_pressure(atm['atm_class'], g_m_s2, R_m)
    gamma_d = compute_lapse_rate(g_m_s2, atm['composition'])
    H       = compute_scale_height(T_eq_K, g_m_s2, atm['composition'])

    notes = atm['notes']
    if pass2_applied:
        notes += ' Pass-2 m_mean refinement applied.'

    return {
        'T_exo_K':     T_exo,
        'jeans':       jeans,
        'atm_class':   atm['atm_class'],
        'composition': atm['composition'],
        'P_s_Pa':      P_s,
        'gamma_d_K_m': gamma_d,
        'H_m':         H,
        'h_identity':  h_identity,
        'notes':       notes,
    }
