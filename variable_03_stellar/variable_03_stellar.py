# variable_03_stellar/variable_03_stellar.py
#
# Variable 03: Stellar properties
# Entry point. Imports sub-functions. Assembles outputs. Contains no physics.

from variable_03_stellar.stellar_mass_sampler import sample_stellar_mass
from variable_03_stellar.stellar_stability import classify_stellar_stability
from variable_03_stellar.stellar_age_sampler import sample_stellar_age
from variable_03_stellar.mass_luminosity import compute_stellar_luminosity
from variable_03_stellar.mass_radius_lowmass import compute_radius_lowmass
from variable_03_stellar.surface_gravity_evolution import compute_log_g
from variable_03_stellar.stellar_radius_highmass import compute_radius_highmass
from variable_03_stellar.stellar_temperature import compute_temperature
from variable_03_stellar.main_sequence_lifetime import compute_main_sequence_lifetime
from variable_03_stellar.xuv_luminosity import compute_xuv


def run(seed: int, stability: str | None = None) -> dict:
    """
    Execute Variable 03: stellar mass, age, luminosity, radius, temperature, XUV.

    Parameters
    ----------
    seed : int
        Cascade seed (mass uses ``seed``; age uses ``seed + 1`` internally).
    stability : str or None
        Optional key passed to the stellar mass sampler for draw conditioning.

    Returns
    -------
    dict
        Keys as defined in the Variable 03 cascade specification.
    """
    m_solar, m_kg = sample_stellar_mass(seed, stability=stability)
    stab = classify_stellar_stability(m_solar)
    age_gyr, tau_frac = sample_stellar_age(seed, m_solar)
    l_solar, l_w = compute_stellar_luminosity(m_solar)

    log_g = None
    if m_solar <= 1.5:
        r_solar, r_m = compute_radius_lowmass(m_solar)
    else:
        log_g = compute_log_g(m_solar, tau_frac)
        r_solar, r_m = compute_radius_highmass(m_solar, log_g)

    t_eff = compute_temperature(l_w, r_m)
    t_ms = compute_main_sequence_lifetime(m_solar)
    lxuv_frac, lxuv_w = compute_xuv(age_gyr, l_w)

    return {
        "M_star_solar": m_solar,
        "M_star_kg": m_kg,
        "stability": stab["stability"],
        "stable": stab["stable"],
        "age_Gyr": age_gyr,
        "tau_frac": tau_frac,
        "L_star_solar": l_solar,
        "L_star_W": l_w,
        "R_star_solar": r_solar,
        "R_star_m": r_m,
        "log_g": log_g,
        "T_eff_K": t_eff,
        "t_MS_Gyr": t_ms,
        "L_XUV_fraction": lxuv_frac,
        "L_XUV_W": lxuv_w,
    }
